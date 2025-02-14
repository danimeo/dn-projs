import datetime
from serial import Serial


def datetime_str():
    return str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '')


def read_signal_from_serial_and_save(directory, duration=10):
    ser = Serial('COM5', 57600, timeout=None)
    filename_ = directory + '/' + datetime_str() + '.bin'
    start_time = datetime.datetime.now()
    cycles = 0
    while duration == -1 or (datetime.datetime.now() - start_time).total_seconds() < duration:
        a = ser.read()
        with open(filename_, 'ab') as file_output:
            file_output.write(a)
        cycles += 1
        if cycles % 1024 == 0:
            print(str(int(cycles / 1024)) + ' KB of data written')
    return filename_


def parse_raw_eeg_from_file_and_save(input_filename, output_directory):
    output_filename = output_directory + '/' + datetime_str() + '.scd'
    buffer = []
    cycles = 0
    with open(input_filename, 'rb') as file_input:
        while True:
            if len(buffer) < 8:
                a = file_input.read(1)
                if not a:
                    break
                buffer.append(ord(a))
            else:
                if False not in [b1 == b2 for b1, b2 in zip(buffer[:5], (0xAA, 0xAA, 0x04, 0x80, 0x02))] \
                        and (((0x80 + 0x02 + buffer[5] + buffer[6]) ^ 0xFFFFFFFF) & 0xFF) == buffer[7]:
                    # value = int(((buffer[5] << 8) | buffer[6]) / 256)
                    # print(value, hex(buffer[5]), hex(buffer[6]))
                    with open(output_filename, 'ab') as file_output:
                        file_output.write(bytes(buffer[5:7]))
                    cycles += 1
                    if (cycles * 2) % 1024 == 0:
                        print(str(int(cycles * 2 / 1024)) + ' KB of data parsed')
                    buffer.clear()
                else:
                    buffer.pop(0)
    return output_filename


def real_time_read_and_parse(port, b_rate=57600, callback=None, params=()):
    ser = Serial(port, b_rate, timeout=None)
    buffer = []
    cycles = 0
    while True:
        a = ser.read()
        if len(buffer) < 8:
            a = ser.read(1)
            if not a:
                break
            buffer.append(ord(a))
        else:
            if False not in [b1 == b2 for b1, b2 in zip(buffer[:5], (0xAA, 0xAA, 0x04, 0x80, 0x02))] \
                    and (((0x80 + 0x02 + buffer[5] + buffer[6]) ^ 0xFFFFFFFF) & 0xFF) == buffer[7]:
                # value = int(((buffer[5] << 8) | buffer[6]) / 256)
                # print(value, hex(buffer[5]), hex(buffer[6]))
                cycles += 1
                if (cycles * 2) % 1024 == 0:
                    print(str(int(cycles * 2 / 1024)) + ' KB of data parsed')
                buffer.clear()
            else:
                buffer.pop(0)
        if callback:
            callback(*params)


if __name__ == '__main__':
    # filename = read_signal_from_serial_and_save(directory='tgam_data', duration=120)
    filename = 'tgam_data/2021-06-23_212712.bin'
    filename = parse_raw_eeg_from_file_and_save(filename, output_directory='tgam_data/eeg_raw')
    print(filename)
