import mmap
import os
import time


import thread
'''from threading import Thread
RPR_ShowConsoleMsg = print


class thread:
    @staticmethod
    def start_new_thread(meth, tupl):
        thr = Thread(target=meth, args=tupl)
        thr.start()'''


msg = b''


def loop(name, num):
    mmap_file = mmap.mmap(-1, 1024, access=mmap.ACCESS_DEFAULT, tagname='rpr_r')
    empty = b'\x00'
    STX = b'\x02\x02\x02\x02'
    ETX = b'\x03'
    last_bytes_list = []
    global msg
    last_msg = b''
    while True:
        data = []
        mmap_file.seek(0)
        a = mmap_file.read(1)
        if a == empty:
            continue
        else:
            etx_count = 0
            while etx_count < 4:
                data.append(a)
                a = mmap_file.read(1)
                if a == ETX:
                    etx_count += 1
                else:
                    etx_count = 0
            data.append(a)
            dat = b''.join(data)
            if not dat.startswith(STX):
                continue
            if len(last_bytes_list) >= 3:
                flag = False
                for l_b in last_bytes_list:
                    if dat != l_b:
                        flag = True
                if not flag:
                    msg = dat[4:-4]
                    if msg != last_msg:
                        RPR_ShowConsoleMsg(msg)

                    #print('h', last_msg, msg, last_msg == msg)
                    last_msg = msg
                    last_bytes_list = []
                else:
                    last_bytes_list.append(dat)
                    if len(last_bytes_list) >= 3:
                        last_bytes_list.pop(0)
            else:
                last_bytes_list.append(dat)
        time.sleep(1)

RPR_ShowConsoleMsg('Dajun\'s Reaper Python remote: Started.')
thread.start_new_thread(loop, ("Thread-1", 2,))

while True:
    RPR_ShowConsoleMsg(msg)
    time.sleep(0.02)
