import socket
import time

from dcam_distribution import TimeCollection

distribution_filename = 'dcam_data/distributions/time_collection.txt'
balance_filename = 'dcam_data/finance/balance.txt'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(True)
server.bind(('127.0.0.1', 8215))
print(socket.gethostname())
server.listen(10)

client, c_addr = server.accept()
print('已连接到客户端' + str(c_addr))

with open(balance_filename, 'rt', encoding='utf-8') as file_input:
    balance = file_input.readline()
with open(distribution_filename, 'rt', encoding='utf-8') as file_input:
    lines = file_input.readlines()

client.send((balance + '\n' + ''.join(lines)).encode('utf-8'))

client.close()

while True:
    client, c_addr = server.accept()

    output = client.recv(16384).decode('utf-8')
    lines = output.split('\n')

    with open(balance_filename, 'wt', encoding='utf-8') as file_output:
        file_output.write(lines[0])
    with open(distribution_filename, 'wt', encoding='utf-8') as file_output:
        file_output.write('\n'.join(lines[1:]))

    time.sleep(2)

    client.close()
