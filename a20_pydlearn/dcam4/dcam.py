import sqlite3
from datetime import datetime, timedelta

from core import TimeSegment

conn, cur = None, None


def err(error_type: str):
    if error_type == 'time_conflict':
        print('该时间段已被占用。')
    elif error_type == 'no_available_time':
        print('无可用时间。')


def connect():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    sql_text_1 = '''CREATE TABLE IF NOT EXISTS account_info(
                username TEXT,
                balance NUMBER,
                available_minutes NUMBER
                );'''
    sql_text_2 = '''CREATE TABLE IF NOT EXISTS time_usage(
                username TEXT,
                start_time TEXT,
                end_time TEXT,
                purpose TEXT,
                occupied NUMBER
                );'''
    cur.execute(sql_text_1)
    cur.execute(sql_text_2)

    return conn, cur


def conflicts(username: str, segment):
    sql_text_3 = f"SELECT * FROM time_usage WHERE username=='{username}'"
    cur.execute(sql_text_3)
    time_usage = cur.fetchall()
    # print(time_usage)
    segments = [TimeSegment(datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f'),
                            datetime.strptime(e, '%Y-%m-%d %H:%M:%S.%f'),
                            p) for _, s, e, p in time_usage]
    for seg in segments:
        if seg * segment:
            return True
    return False


def buy_time(username: str, segment: TimeSegment, purpose: str):
    if not conflicts(username, segment):
        sql_text = f"INSERT INTO time_usage VALUES('{username}', '{segment.start}', '{segment.end}', '{purpose}')"
        print(sql_text)
        cur.execute(sql_text)
    else:
        err('time_conflict')


def use_time(username: str):
    sql_text_3 = f"SELECT * FROM time_usage WHERE username=='{username}, occupied=0'"
    cur.execute(sql_text_3)
    time_usage = cur.fetchall()
    if not time_usage:
        err('no_available_time')
        return
    segments = [TimeSegment(datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f'),
                            datetime.strptime(e, '%Y-%m-%d %H:%M:%S.%f'),
                            p) for _, s, e, p in time_usage]
    for seg in segments:
        sql_text = f"UPDATE table_name SET occupied=1 WHERE username=='{username}', start_time=='{seg.start}', end_time='{seg.end}';"
        cur.execute(sql_text)



def commit():
    global conn
    conn.commit()


if __name__ == '__main__':
    conn, cur = connect()
    seg1 = TimeSegment(datetime.now() + timedelta(minutes=40), datetime.now() + timedelta(minutes=60))
    buy_time('dajun', seg1, '学习概率论')
    use_time()
    commit()
