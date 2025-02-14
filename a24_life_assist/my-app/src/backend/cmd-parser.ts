import * as fs from 'fs';
import * as path from 'path';
import * as sqlite3 from 'sqlite3';
import { pinyin } from 'pinyin-pro';
import { Decimal } from 'decimal.js';
import { Vault, VaultConf } from './committer';

interface Med {
    id: number;
    name: string[];
    generic_name: string[];
    specs: [string, Decimal, Decimal, Decimal][];
}


export class MedicationManager {
    private db: sqlite3.Database;
    private data: { meds: Med[] };
    private vaultConf: VaultConf;
    private v: any; // 假设 Vault 是一个外部库

    constructor(dbFile: string, dataFile: string) {
        this.db = new sqlite3.Database(dbFile);
        this.data = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
        this.vaultConf = {
            remote_path: '',
            local_path: '',
            username: '',
            email: '',
            branch: 'master'
        };
    }

    private parseText(command: string): [string, string, number, number, string][] {
        const m_ = command.trim().match(/(add +)?([A-Za-z_]+[^\r\n]*)/);

        if (!m_) {
            throw new Error(`❌ 命令输入有误: ${command}`);
        }

        const medsTaken: [string, string, number, number, string][] = [];

        const regex = /([A-Za-z_]+)([0-9./]+)?[\s\t\n,]*([0-9./]+)?/g;
        for (const m_1 of Array.from(m_[2].matchAll(regex))) {
            let name = m_1[1]?.trim();
            if (!name) continue;

            let pillsTaken_ = m_1[3]?.trim();
            let pillsTaken: number;
            if (pillsTaken_ && new Decimal(pillsTaken_).greaterThan(0)) {
                pillsTaken = new Decimal(pillsTaken_).toNumber();
            } else {
                pillsTaken = 1;
            }

            let med: Med | null = null;
            for (const m of this.data.meds) {
                if (m.name.includes(name)) {
                    med = m;
                    break;
                }
            }

            if (!med) {
                const maxId = Math.max(...this.data.meds.map(m => m.id));
                med = {
                    id: maxId + 1,
                    name: [name],
                    generic_name: ['<Unknown>', '', '', ''],
                    specs: [['<?>', new Decimal(0), new Decimal(0), new Decimal(0)]]
                };
                this.data.meds.push(med);
            } else {
                med.name.push(name);
            }

            let dosageMgTaken_ = m_1[2]?.trim();
            let dosageMgTaken: number;
            if (dosageMgTaken_) {
                dosageMgTaken = new Decimal(dosageMgTaken_).toNumber();
            } else {
                dosageMgTaken = med.specs[0][1].toNumber();
            }

            if (!med.specs.some(spec => spec[1].equals(new Decimal(dosageMgTaken)))) {
                med.specs.push(['<?>', new Decimal(dosageMgTaken), new Decimal(0), new Decimal(0)]);
            }

            let pillsPerStrip = '?';
            for (const spec of med.specs) {
                if (spec[1].equals(new Decimal(dosageMgTaken))) {
                    pillsPerStrip = spec[2].toNumber() > 0 ? spec[2].toString() : '?';
                    break;
                }
            }

            const medName = pinyin(med.generic_name[0], { type: 'string' }).toLowerCase();
            const timingStr = new Date().toISOString().slice(2, 16).replace(/[-:]/g, '');

            medsTaken.push([timingStr, medName, dosageMgTaken, pillsTaken, pillsPerStrip]);
        }

        return medsTaken;
    }

    private createTable(tableName: string, columns: { [key: string]: string }) {
        const columnDefs = Object.entries(columns).map(([key, type]) => `${key} ${type}`).join(', ');
        this.db.run(`CREATE TABLE IF NOT EXISTS ${tableName} (id INTEGER PRIMARY KEY AUTOINCREMENT, ${columnDefs})`);
    }

    private queryVaultConf(): VaultConf[] {
        const results: VaultConf[] = [];
        this.db.each('SELECT remote_path, local_path, username, email FROM vault_conf', (err, row) => {
            if (err) throw err;
            results.push({
                remote_path: row.remote_path,
                local_path: row.local_path,
                username: row.username,
                email: row.email,
                branch: 'master'
            });
        });
        return results;
    }

    private writeVaultConf(conf: VaultConf) {
        const values = [conf.remote_path, conf.local_path, conf.username, conf.email];
        this.db.run('INSERT INTO vault_conf (remote_path, local_path, username, email) VALUES (?, ?, ?, ?)', values);
    }

    public logMeds(text: string, vaultConf: VaultConf) {
        this.vaultConf = { ...this.vaultConf, ...vaultConf };

        this.createTable('vault_conf', {
            remote_path: 'TEXT',
            local_path: 'TEXT',
            username: 'TEXT',
            email: 'TEXT'
        });

        const _confs = this.queryVaultConf();
        if (!_confs.length) {
            throw new Error('vault config not found');
        }

        this.v = new Vault(this.vaultConf);

        const medsTaken = this.parseText(text);

        const logFilePath = path.join(this.vaultConf.local_path, 'meds/meds-2024c.txt');
        let logs: string[] = fs.existsSync(logFilePath) ? fs.readFileSync(logFilePath, 'utf-8').split('\n') : [];

        for (const [timingStr, medName, dosageMgTaken, pillsTaken, pillsPerStrip] of medsTaken) {
            logs.push(`${timingStr} ${medName}${dosageMgTaken},${pillsTaken} s${pillsPerStrip} t?/?`);
        }

        fs.writeFileSync(logFilePath, logs.join('\n'));

        this.v.write(logFilePath, logs.join('\n'), `took meds: ${medsTaken.map(([_, medName, dosageMgTaken, pillsTaken]) => `\`${medName}\` ${dosageMgTaken}mg × ${pillsTaken}`).join(' ')}`);
    }
}


