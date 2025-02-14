import sounddevice as sd
import numpy as np
import librosa



# 采样率
fs = 44100
# 持续时间（秒）
duration = 5

# 回调函数
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    # 在此处处理音频数据
    outdata[:] = indata  # 直接将输入数据复制到输出数据中，形成回声
    # sample = librosa.resample(outdata, fs, )
    print(outdata.shape)

# 打开音频流
with sd.Stream(callback=callback, samplerate=fs, channels=2) as stream:
    # 准备开始录制五秒音频
    sd.sleep(int(duration * 1000))  # 暂停主线程，允许音频流处理音频数据