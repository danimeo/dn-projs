from musicpy import read
import numpy as np
import os
from tensorflow.keras.utils import to_categorical
import threading
from ssqueezepy import ssq_stft
import queue
import librosa
import asyncio
from scipy.signal import windows, convolve

mid_dir = 'G:/编曲资源'
wav_gen_dir = 'C:/dev_spa/artear_1/wav_gen'
data_gen_dir = 'C:/dev_spa/artear_1/data_gen'
data_buffer_dir = 'C:/dev_spa/artear_1/data_gen/buffer'


mid_queue = queue.Queue()
q_count = 0
n_top = 100


def get_mid_files(directory, num):
    global mid_queue
    n = 0
    for paths in [[os.path.join(dirpath, name).replace('\\', '/') for name in filenames if name.endswith('.mid')]
                  for dirpath, dirnames, filenames in os.walk(directory)]:
        for path in paths:
            if n == num:
                return
            mid_queue.put(path)
            n += 1


def get_files(directory, ext):
    path_list = []
    for paths in [[os.path.join(dirpath, name).replace('\\', '/') for name in filenames if name.endswith('.' + ext)] for
                  dirpath, dirnames, filenames in os.walk(directory)]:
        path_list.extend(paths)
    return path_list


print('正在获取MIDI和WAV文件路径……')
get_mid_files(mid_dir, n_top)
max_size = mid_queue.qsize()
wav_paths = get_files(wav_gen_dir, 'wav')

producers = []
n_active_pros = 0
lock = threading.RLock()
q_count = 0
prefixes = ['input_', 'output_n_', 'output_d_', 'output_t_']


def fun(x):
    r = int(round(x / 0.0625))
    return r if r <= 31 else 31


def resample(input_signal,src_fs,tar_fs):
    dtype = input_signal.dtype
    audio_len = len(input_signal)
    audio_time_max = 1.0*(audio_len-1) / src_fs
    src_time = 1.0 * np.linspace(0,audio_len,audio_len) / src_fs
    tar_time = 1.0 * np.linspace(0,np.int(audio_time_max*tar_fs),np.int(audio_time_max*tar_fs)) / tar_fs
    output_signal = np.interp(tar_time,src_time,input_signal).astype(dtype)
    return output_signal
        

class Producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index

    def run(self):
        global mid_queue, max_size, q_count, n_top, n_active_pros
        
        while not mid_queue.empty():
            # print('[' + str(q_count) + '/' + str(max_size) + '] 线程' + str(self.index + 1) + ' Start working...')
            mid = mid_queue.get()
            
            try:
                t = 0.
                bpm, a = read(mid)[:2]
                len_a = len(a)
                # assert len_a > 3
                if len_a > 32:
                    a = a[:33]
                    len_a = len(a)
                len_added = (32 - len_a if len_a <= 32 else 32)
                lst_ = to_categorical(
                    np.array([i.degree for i in a] + [0.] * len_added, dtype='uint8'), 128)
                lst_d = to_categorical(np.array([fun(i.duration) for i in a] + [0] * len_added, dtype='uint8'), 32)

                lst_time = []
                for interval in a.interval:
                    lst_time.append(t)
                    t += interval
                lst_t = np.array(lst_time + [0.] * len_added, dtype='float32')
            except ValueError as e:
                print(' Wrong value. ' + str(e))
                max_size -= 1
                continue
            except AssertionError:
                print(' Too short.')
                max_size -= 1
                continue
            

            wav_file = os.path.join(wav_gen_dir, os.path.splitext( os.path.basename(mid))[0]) + '.wav'
            if not os.path.exists(wav_file):
                print(' File \'' + wav_file + '\' does not exist.')
                max_size -= 1
                continue
            wav_data, sr = librosa.load(wav_file)
            data, _, *_ = ssq_stft(wav_data)
            # data = data.transpose((1, 0))

            factor = 194, 87945    # 64x256
            kernel_1d = windows.boxcar(factor[0]), windows.boxcar(factor[1])
            data = convolve(data, np.outer(*kernel_1d), mode='valid')
            shp_data = data.shape
            # print(shp_data)
            
            file_list = []
            
            for pref in prefixes:
                filename = os.path.join(data_buffer_dir, pref + str(q_count + 1))
                file_list.append(filename)
            
            for filename, data in zip(file_list, (data, lst_, lst_d, lst_t)):
                np.save(filename, data)
            
            q_count += 1
            mid_queue.task_done()
            print('[' + str(q_count) + '/' + str(max_size) + '] 线程' + str(self.index + 1) + ' ' + str(shp_data) + ' Done.')
            
        n_active_pros -= 1
            



for i in range(1):
    pro = Producer(i)
    n_active_pros += 1
    pro.start()
    producers.append(pro)

for pro in producers:
    pro.join()

    
print(' Done.')


print('正在保存数据为numpy数组……')
list_input, list_output_n, list_output_d, list_output_t = [], [], [], []

for filename in get_files(data_buffer_dir, 'npy'):
    if os.path.basename(filename).startswith('input_'):
        list_input.append(np.load(filename))
    elif os.path.basename(filename).startswith('output_n_'):
        list_output_n.append(np.load(filename))
    elif os.path.basename(filename).startswith('output_d_'):
        list_output_d.append(np.load(filename))
    elif os.path.basename(filename).startswith('output_t_'):
        list_output_t.append(np.load(filename))
    else:
        continue
    # os.remove(filename)
    
print(len(list_input), len(list_output_n), len(list_output_d), len(list_output_t), sep='\n')

len_input, input_ = len(list_input), np.concatenate(list_input)
del list_input
input_ = input_.reshape((len_input, -1, input_.shape[1], 1))
np.save(os.path.join(data_gen_dir, 'input_data'), input_)
shp_input_ = input_.shape
del input_

output_n = np.concatenate(list_output_n).reshape((len(list_output_n), -1))
output_d = np.concatenate(list_output_d).reshape((len(list_output_d), -1))
output_t = np.concatenate(list_output_t).reshape((len(list_output_t), -1))
np.save(os.path.join(data_gen_dir, 'output_n_data'), output_n)
np.save(os.path.join(data_gen_dir, 'output_d_data'), output_d)
np.save(os.path.join(data_gen_dir, 'output_t_data'), output_t)

print(shp_input_, output_n.shape, output_d.shape, output_t.shape, sep='\n')

print('完成。')
