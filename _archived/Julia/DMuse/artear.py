import pyaudio
import time

p = pyaudio.PyAudio()

#获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备
def findDevice(p):
    #要找查的设备名称中的关键字
    target = 'Microsoft 声音映射器 - Input'
    #逐一查找声音设备  
    for i in range(p.get_device_count()):
        devInfo = p.get_device_info_by_index(i)
        print(devInfo)
        if devInfo['name'].find(target)>=0 and devInfo['hostApi'] == 0 :      
            #print('已找到内录设备,序号是 ',i)
            return i
    print('无法找到内录设备!')
    return -1    

# 在打开输入流时指定输入设备
stream = p.open(output_device_index=8,
                format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=256)

frames = []

# 循环读取输入流
init_t = time.time()
while (time.time() - init_t) < 2:
    data = stream.read(256)
    print(data)
    frames.append(data)

# 停止读取输入流
stream.stop_stream()
# 关闭输入流
stream.close()
# 结束pyaudio
p.terminate()
