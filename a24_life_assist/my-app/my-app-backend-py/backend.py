import datetime
from fractions import Fraction
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

import pypinyin

from vault_mgr import Vault

data = None
vault_conf = {}
v = None
app = Flask(__name__)
CORS(app)

# 数据库文件路径
db_file = 'data.db'
    

def parse_text(command):
    m_ = re.match(r'(add +)?([A-Za-z_]+[^\r\n]*)', command.strip())

    assert m_, "❌ 命令输入有误: " + command
    
    meds_taken = []

    for i, m_1 in enumerate(re.finditer(r'([A-Za-z_]+)([0-9\./]+)?[ \s\t\n\,]*([0-9\./]+)?', m_.group(2))):
    
        if m_1:
            # name
            name = m_1.group(1)
            if name is not None and name != '':
                name = name.strip()
            else:
                return

            # pills_taken
            pills_taken = m_1.group(3)
            if pills_taken is not None and pills_taken !='' and Fraction(pills_taken.strip()) > 0:
                if '/' in pills_taken:
                    pills_taken = Fraction(pills_taken.strip()) if len(str(Fraction(pills_taken.strip()))) < 4 else float(pills_taken.strip())
                else:
                    pills_taken = float(pills_taken.strip())
            else:
                pills_taken = Fraction(1)

            # med
            med = None
            for m in data["meds"]:
                if m is not None and name in m["name"]:
                    med = m
                    break
            else:
                if med is None:
                    med = {
                        "id": max(data["meds"], key=lambda x: x["id"])["id"] + 1,
                        "name": [name],
                        "generic_name": [f"<Unknown>", "", "", ""],
                        "specs": [("<?>", Fraction(0), Fraction(0), Fraction(0))]
                    }
                else:
                    med["name"].append(name)

            # dosage_mg_taken
            dosage_mg_taken_ = m_1.group(2)
            if dosage_mg_taken_ is not None:
                dosage_mg_taken_ = dosage_mg_taken_.strip()
                e = eval(dosage_mg_taken_)
                if re.search(r'[\+\-\*]', dosage_mg_taken_) is None:
                    a, b = Fraction(dosage_mg_taken_), float(dosage_mg_taken_)
                else:
                    a = Fraction(e)
                    if re.search(r'/', dosage_mg_taken_) is None:
                        b = float(dosage_mg_taken_)
                    else:
                        b = float(e)

                if b == e and a != e:
                    dosage_mg_taken = int(b) if str(b).endswith('.0') else b
                elif b != e and a == e:
                    dosage_mg_taken = a
                else:
                    slen = lambda x: len(str(x))
                    dosage_mg_taken, _ = sorted([a, b], key=slen)

                    if slen(a) == slen(b):
                        dosage_mg_taken = b
            else:
                dosage_mg_taken = med["specs"][0][1]


            if dosage_mg_taken not in (spec[1] for spec in med["specs"]):
                med["specs"].append(("<?>", dosage_mg_taken, Fraction(0), Fraction(0)))
            

            # pills_per_strip
            for spec in med["specs"]:
                if spec[1] == dosage_mg_taken:
                    if spec[2] > 0:
                        pills_per_strip = str(spec[2])
                    else:
                        pills_per_strip = '?'
                    break


            med_name = ''.join(pypinyin.lazy_pinyin(med["generic_name"][0], style=pypinyin.Style.FIRST_LETTER)).lower()
            timing_str = datetime.datetime.now().strftime('%m%d,%H%M')
            
            
            meds_taken.append((timing_str, med_name, dosage_mg_taken, pills_taken, pills_per_strip))
    return meds_taken




# 创建数据库表（如果不存在）
def create_table(table_name, **kwargs):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, {','.join('{} {}'.format(key, kwargs[key]) for key in kwargs)})''')
    conn.commit()
    conn.close()

# "vault_conf": {
#         "vault_name": "snote-001",
#         "vault_dir_path": "./test_vault_dir",
#         "remote_path_template": "http://r.danim.space/danim/{}.git",
#         "user_info": {"name": "danim", "email": "danimeon@outlook.com"}
#     },

def query_vault_conf():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT remote_path, local_path, username, email FROM vault_conf")
    results = cursor.fetchall()
    conn.close()
    conf = []
    for remote_path, local_path, username, email in results:
        conf.append({
            "remote_path": remote_path,
            "local_path": local_path,
            "username": username,
            "email": email,
        })
    return conf


def write_vault_conf(conf):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    values = tuple(conf[key] for key in ('remote_path', 'local_path', 'username', 'email'))
    cursor.execute(f"INSERT INTO vault_conf (remote_path, local_path, username, email) VALUES (?,?,?,?)", values)
    conn.commit()
    conn.close()


@app.route('/query_vault_conf', methods=['POST'])
def get_user_info():
    return jsonify(query_vault_conf())


@app.route('/log_meds', methods=['POST'])
def post_data():
    global data, vault_conf, v

    if data is None:
        data,  = [json.load(open(os.path.join(os.getcwd(), path), 'r')) for path in ('data.json', )]

        create_table("vault_conf", remote_path='TEXT', local_path='TEXT', username='TEXT', email='TEXT')
        _confs = query_vault_conf()
        assert _confs, "vault config not found"
        vault_conf = _confs[0] | {'branch':'master'}
        v = Vault(**vault_conf)

    dat = request.get_json()
    print(dat)
    if dat and 'text' in dat:
        vault_conf.update({'remote_path': dat['remotePath'], 
                           'branch':dat['branch']})
        write_vault_conf(vault_conf)
        vault_conf = _confs[0] | {'branch':'master'}
        v = Vault(**vault_conf)


        text = dat['text']
        meds_taken = parse_text(text)

        # try:
        # print(vault_conf['local_path'])
        log_file_path = os.path.join(vault_conf['local_path'], 'meds/meds-2024c.txt')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as fp:
                logs = fp.read().split('\n')
        else:
            logs = []

        for timing_str, med_name, dosage_mg_taken, pills_taken, pills_per_strip in meds_taken:
            logs.append(f"{timing_str} {med_name}{dosage_mg_taken},{pills_taken} s{'?'}/{pills_per_strip} t{'?'}/{'?'}")

        v.write(log_file_path, '\n'.join(logs), f'took meds: {" ".join(f"`{med_taken}` {dsg}mg × {pills_taken}" for id, med_taken, dsg, *_ in meds_taken)}')
        return 'Data written to database and pushed to Git successfully.', 200
        # except Exception as e:
        #     return f'Error pushing to Git: {str(e)}', 500
    else:
        return 'Invalid data format.', 400


if __name__ == '__main__':
    
    app.run(port=8035, debug=True)