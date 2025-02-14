import math
import mmap
import time
mapping_size = 65536

# fileno = os.open('C:/REAPER/Scripts/1.mmap', os.O_RDWR)
mmap_send = mmap.mmap(-1, mapping_size, access=mmap.ACCESS_DEFAULT, tagname='flu_r2c')
mmap_recv = mmap.mmap(-1, mapping_size, access=mmap.ACCESS_DEFAULT, tagname='flu_c2r')

empty = b'\x00' * mapping_size


def send(msg):
    b2 = msg.encode(encoding='utf-8')
    while True:
        mmap_send.seek(0)
        mmap_send.write(empty)
        mmap_send.seek(0)
        mmap_send.write(b2)
        mmap_send.seek(0)
        if mmap_send.read(len(b2)) == b2:
            break


def recv():
    mmap_recv.seek(0)
    data = mmap_recv.read(mapping_size)
    length = len(data)
    if data == empty:
        return ''
    return data


while True:
    data = recv()
    if data:
        print(data)
    time.sleep(0.1)
