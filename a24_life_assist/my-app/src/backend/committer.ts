import * as fs from 'fs';
import * as path from 'path';
import * as git from 'isomorphic-git';
import * as http from 'isomorphic-git/http/node';


export interface VaultConf {
    remote_path: string;
    local_path: string;
    username: string;
    email: string;
    branch: string;
}

export class Vault {
    private vaultName: string;
    private localPath: string;
    private remotePath: string;
    private userInfo: { username: string; email: string };
    private branch: string;
    private repo: any;

    constructor(config: VaultConf) {
        this.userInfo = { username: config.username, email: config.email };
        this.vaultName = 'default';
        // 使用 config 对象中的属性
        this.remotePath = config.remote_path;
        this.localPath = config.local_path;
        this.branch = config.branch;
        this.init();
    }

    private async branchExists(branchName: string): Promise<boolean> {
        const branches = await git.listBranches({ fs, dir: this.localPath });
        return branches.includes(branchName);
    }

    private async init() {
        const vaultPath = path.join(this.localPath);
    
        if (!fs.existsSync(vaultPath)) {
            await git.clone({
                fs,
                http,
                dir: vaultPath,
                url: this.remotePath,
                ref: this.branch,
                singleBranch: true
            });
        } else {
            const dotGit = path.join(vaultPath, '.git');
            if (!fs.existsSync(dotGit)) {
                await git.init({ fs, dir: vaultPath, defaultBranch: this.branch });
            }
    
            const remotes = await git.listRemotes({ fs, dir: vaultPath });
            if (remotes.length === 0) {
                await git.addRemote({
                    fs,
                    dir: vaultPath,
                    remote: 'origin',
                    url: this.remotePath
                });
            } else {
                const remote = remotes[0];
                if (remote.url !== this.remotePath) {
                    await git.deleteRemote({ fs, dir: vaultPath, remote: 'origin' });
                    await git.addRemote({
                        fs,
                        dir: vaultPath,
                        remote: 'origin',
                        url: this.remotePath
                    });
                }
            }
    
            await git.fetch({
                fs,
                http,
                dir: vaultPath,
                ref: this.branch,
                singleBranch: true
            });
    
            if (!(await this.branchExists(this.branch))) {
                await git.checkout({
                    fs,
                    dir: vaultPath,
                    ref: `refs/remotes/origin/${this.branch}`
                });
                await git.branch({
                    fs,
                    dir: vaultPath,
                    ref: this.branch,
                    checkout: true
                });
            } else {
                await git.checkout({
                    fs,
                    dir: vaultPath,
                    ref: this.branch
                });
            }
    
            const readmePath = path.join(vaultPath, 'README.md');
            if (!fs.existsSync(readmePath)) {
                fs.writeFileSync(readmePath, `# S-Note Vault ${this.vaultName}\n---\nWelcome.\n`);
            }
    
            if (await git.statusMatrix({ fs, dir: vaultPath }).then(matrix => matrix.length > 0)) {
                await git.add({ fs, dir: vaultPath, filepath: '.' });
                await git.commit({
                    fs,
                    dir: vaultPath,
                    message: 'auto commit',
                    author: {
                        name: this.userInfo.username,
                        email: this.userInfo.email
                    }
                });
            }
    
            if (!(await this.branchExists(this.branch))) {
                await git.branch({
                    fs,
                    dir: vaultPath,
                    ref: this.branch,
                    checkout: true
                });
            }
    
            if ((await git.currentBranch({ fs, dir: vaultPath })) !== this.branch) {
                await git.checkout({
                    fs,
                    dir: vaultPath,
                    ref: this.branch
                });
            }
    
            await git.setConfig({
                fs,
                dir: vaultPath,
                path: 'user.name',
                value: this.userInfo.username
            });
    
            await git.setConfig({
                fs,
                dir: vaultPath,
                path: 'user.email',
                value: this.userInfo.email
            });
    
            await git.push({
                fs,
                http,
                dir: vaultPath,
                remote: 'origin',
                ref: this.branch
            });
        }
    }

    public async write(relativePath: string, content: string, commitMsg: string) {
        const vaultPath = path.join(this.localPath, this.vaultName);
        const fileDirName = path.join(vaultPath, path.dirname(relativePath));
        if (!fs.existsSync(fileDirName)) {
            fs.mkdirSync(fileDirName, { recursive: true });
        }
        const filePath = path.join(vaultPath, relativePath);
        fs.writeFileSync(filePath, content);

        await git.add({ fs, dir: vaultPath, filepath: relativePath });

        try {
            await git.fetch({
                fs,
                http,
                dir: vaultPath,
                ref: this.branch,
                singleBranch: true
            });

            if (!(await this.branchExists(this.branch))) {
                await git.checkout({
                    fs,
                    dir: vaultPath,
                    ref: `refs/remotes/origin/${this.branch}`
                });
                await git.branch({
                    fs,
                    dir: vaultPath,
                    ref: this.branch,
                    checkout: true
                });
            } else {
                await git.checkout({
                    fs,
                    dir: vaultPath,
                    ref: this.branch
                });
            }

            await git.add({ fs, dir: vaultPath, filepath: '.' });
            await git.commit({
                fs,
                dir: vaultPath,
                message: commitMsg,
                author: {
                    name: this.userInfo.username,
                    email: this.userInfo.email
                }
            });
        } catch (e) {
            console.error(e);
        }

        try {
            await git.push({
                fs,
                http,
                dir: vaultPath,
                remote: 'origin',
                ref: this.branch
            });
        } catch (e) {
            console.error(e);
        }
    }
}