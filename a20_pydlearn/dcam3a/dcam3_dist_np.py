from datetime import datetime, timedelta
import socket
import sqlite3
import os
from git.repo import Repo

from dcam3_core import *


class Distributor:
    def __init__(self, filenames: dict, git_remote=('https://gitee.com/danimeo/personal_timing_server.git',)):
        self.tasks = []
        self.purchased = TimeTrack()
        self.classes = TimeTrack()
        self.master = TimeTrack()
        self.timing = TimeTrack()

        self.item_titles = [
            '',  # 0
            '',  # 1
        ]

        self.task_titles = [
            '',
            '', 
        ]

        # Specific tracks(timing_arr s): past, purchased, default.
        # Each tasks takes up a track.

        self.users_info = {
            'default': {
                'balance': 0.0,
                'tracks': {
                    'past': TimeTrack(),
                    'purchased': TimeTrack()
                }
            }
        }

        self.localizations = {}


        self.git_remote = git_remote

        self.filenames = filenames

        self.available_time_range = (datetime.now().replace(hour=8, minute=25, second=0, microsecond=0)
                        , datetime.now().replace(hour=23, minute=30, second=0, microsecond=0))
        self.default_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        self.db_conn = sqlite3.connect(self.filenames['database'])

        self.current_user = 'default'
        self.selected_track_index = 0



    def mono_task(self):
        mono = sum(self.users[self.current_user]['time_tracks'], start=TimeTrack())
        return mono
    
    def update_property(self, key: str = 'all'):
        if key == 'all':
            keys = self.users[self.current_user].keys()
        else:
            keys = [key]

        for k in keys:
            with open(self.filenames[k], 'wt', encoding='utf-8') as file_output:
                file_output.write(str(self.users[self.current_user][k]))
        

    def transact(self, code: str, duration: timedelta):
        if self.available_time_range[1] <= datetime.now() < self.available_time_range[0].replace(day=self.available_time_range[0].day + 1):
            return False, 'time-not-allowed-for-transaction'

        if not code or code not in self.prices or not duration.total_seconds():
            return False, ''

        balance_change = self.prices[code][1] * duration.total_seconds() / 60
        print(balance_change)
        if self.users[self.current_user]['balance'] + balance_change >= 0:
            self.users[self.current_user]['balance'] += balance_change
            self.update_balance()
            return True, 'transaction-successful'
        else:
            return False, 'balance-not-enough'


    def read_from_file(self, attr: str = 'distribution'):
        if str == 'distribution':

            with open(self.filenames['distribution'], 'rt', encoding='utf-8') as file_input:
                lines = [line.strip() for line in file_input.readlines()]
            self.users[self.current_user]['tracks'].fragments.clear()
            for line in lines:
                attrs = line.split(',')
                start = datetime.datetime.strptime(attrs[0], '%Y-%m-%d %H:%M:%S.%f')
                end = datetime.datetime.strptime(attrs[1], '%Y-%m-%d %H:%M:%S.%f')
                if attrs[3] == 'True':
                    purchased = True
                else:
                    purchased = False
                self.fragments.append(TimeSegment(start, end, purpose=attrs[2], purchased=purchased))

            zero = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            for i, fragment in enumerate(self.fragments):
                if fragment.start < zero or fragment.end < zero:
                    self.fragments = [TimeSegment(*self.available_time_range)]
                    self.save_to_file(self.filenames['distribution'])
                    break
            return '\n'.join(lines)
        elif attr == 'prices':
            with open(self.filenames['prices'], 'rt', encoding='utf-8') as file_input:
                prices_list = [line.strip() for line in file_input.readlines()]

            for price_line in prices_list:
                code_purpose_price = price_line.split('\t')
                self.prices[code_purpose_price[0]] = (code_purpose_price[1], float(code_purpose_price[2]))


        
    def save_to_file(self, filename: str):
        output = ''
        for fragment in self.fragments:
            output += fragment.start.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + fragment.end.strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + fragment.purpose + ',' + str(fragment.purchased) + '\n'
        with open(filename, 'wt', encoding='utf-8') as file_output:
            file_output.write(output)


    def read_from_db(self):
        pass


    def write_to_db(self):
        pass


    def init_db(self):
        # Create an empty table in each database

        c1 = self.users_db_conn.cursor()
        c1.execute('''CREATE TABLE COMPANY
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')
        self.users_db_conn.commit()

        c2 = self.time_db_conn.cursor()
        c2.execute('''CREATE TABLE tracks
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')
        self.time_db_conn.commit()

    
    
    def sync_from_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.remote)
        output = s.recv(16384).decode('utf-8')
        lines = output.split('\n')

        with open(self.filenames['balance'], 'wt', encoding='utf-8') as file_output:
            file_output.write(lines[0])
        with open(self.filenames['distribution'], 'wt', encoding='utf-8') as file_output:
            file_output.write('\n'.join(lines[1:]))

        self.users[self.current_user]['balance'] = float(lines[0])
        self.read_from_file(self.filenames['distribution'])

        s.close()

    def sync_to_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.remote)
        s.send((str(self.users[self.current_user]['balance']) + '\n' + self.read_from_file(self.filenames['distribution'])).encode('utf-8'))
        s.close()

    def purchase_all_idle_time(self):
        d = datetime.timedelta()
        for fragment in self.fragments:
            d += fragment.end - fragment.start
        if self.change_balance(False, True, d):
            for fragment in self.fragments:
                if not fragment.purchased:
                    fragment.purchased = True
            self.save_to_file(self.filenames['distribution'])
            self.sync_to_server()
            return True
        else:
            self.save_to_file(self.filenames['distribution'])
            self.sync_to_server()
            return False
        