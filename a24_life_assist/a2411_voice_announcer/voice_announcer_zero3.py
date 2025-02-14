# pm2 delete announcer
# pm2 start -n announcer 'D:\git_repos\d-notes\repos\pn\codes\a24_life_assist\a2411_voice_announcer\voice_announcer_zero3.py'
# pm2 save

# zero3_ubuntu:
# pm2 delete announcer
# pm2 start -n announcer '/data/pn-2/codes/a24_life_assist/a2411_voice_announcer/announcer.sh'
# pm2 save

# 参考来源：https://blog.csdn.net/white_hat_2009/article/details/124784680

from io import BytesIO
import json
import os
import threading
import time
from datetime import datetime
import pyaudio
from pytz import timezone

tzchina = timezone('Asia/Chongqing')
get_now = lambda: datetime.now(tzchina)

from openai import OpenAI

use_vision = False

# -------------------记得：语音报时附带其他提醒是备用提醒手段，尽量少用！


def get_time_range_name(t1: datetime):
    if t1.hour <= 5:
        time_range_name = '凌晨'
    elif t1.hour <= 11:
        time_range_name = '上午'
    elif t1.hour <= 13:
        time_range_name = '中午'
    elif t1.hour <= 17:
        time_range_name = '下午'
    else:
        time_range_name = '晚上'
    return time_range_name


get_hour_name = lambda t1: f'{t1.hour % 12 if t1.hour % 12 else 12}点'
get_announce_time_text = lambda t1: f'现在是{get_time_range_name(t1)}{get_hour_name(t1)}{"{:02d}分".format(t1.minute) if t1.minute else "整"}'


def llm_call(inp):
    global client
    text = inp
    completion = client.chat.completions.create(
        model="qwen-max",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'{text}'}],
        )

    data = json.loads(completion.model_dump_json())
    content = data["choices"][0]["message"]["content"]
    output_text = content
    return output_text


def llm_reminder(t1: datetime, todo_list: list, announce_time_text: str):
    
    def api_call():
        for i, todo in enumerate(todo_list):
            date, text = todo['date'], todo['text']
            t2 = datetime.strptime(date, "%Y-%m-%d %H:%M")
            if t1.hour == t2.hour:
            
                inp = f"{announce_time_text}。请用一句话提醒这个人去“{todo['text']}”：“"
            
                output_text = llm_call(inp)
                
                output_text = output_text.split('。')[0]
                print('Assistant:', output_text)
                say(f'{output_text}')
    
    try:
        if use_vision:
            inference.messages.clear()
            image_url = f"https://danim-2.oss-cn-heyuan.aliyuncs.com/danim-2/{t1.year}/{t1.month}/{t1.day}/{t1.hour}/latest.jpg"
            print(image_url)
            if not '没' in inference.infer('画面中是否有人', image_url=image_url):
                print('已检测到画面中有人')
                api_call()
            else:
                print('未检测到画面中有人')
        else:
            api_call()
    except Exception as ex:
        print(ex)


def announce_time(t1: datetime, do_not_disturb: bool = False):
    if do_not_disturb and 0 <= t1.hour < 9:
        return

    announce_time_text = get_announce_time_text(t1)

    say(announce_time_text)
    # say(announce_time_text)
    
    todo_list = []
    todo_list += [
        {
            "date": "2024-11-27 09:00",
            "text": "起床",
        },
        {
            "date": "2024-11-27 18:00",
            "text": "去吃晚饭",
        },
        {
            "date": "2024-11-27 21:00",
            "text": "吃托莫西汀、四分之一片阿普唑仑",
        },
        {
            "date": "2024-11-27 22:00",
            "text": "今天的首要任务是早睡",
        },
        {
            "date": "2024-11-27 23:00",
            "text": "不要熬夜",
        },
    ]

    llm_reminder(t1, todo_list, announce_time_text)
    

def playing(out, data_list: list[bytes], n_channels, sample_rate):
    while True:
        if data_list:
            data = data_list.pop(0)
        else:
            data = b''
        if data != b'':
            out.write(data)


if __name__ == '__main__':
    # repo_path = r'D:\git_repos\pn-2'
    repo_path = '/data/pn-2'  # zero3_ubuntu
    pat = os.path.join(repo_path, r'codes/a24_life_assist/a2411_voice_announcer')
    print(pat)

    os.system('ntpdate cn.pool.ntp.org')
    print(get_now())

    # import pyttsx3
    # engine = pyttsx3.init()

    # def say(text: str):
    #     engine.say(text)
    #     engine.runAndWait()  # 等待语音播报完毕

    import csv
    ak_filename = os.path.join(repo_path, r'codes/a24_life_assist/a2411_voice_announcer/voice-api_AK.csv.key')
    csv_reader = csv.reader(open(ak_filename, 'r'))
    next(csv_reader)
    for ak_id, secret in csv_reader:
        os.environ['ALIYUN_AK_ID'] = ak_id
        os.environ['ALIYUN_AK_SECRET'] = secret
        # print(ak_id, secret)

    from aliyun_api_caller import *
    import nls

    URL="wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
    # TOKEN = create_token()  #参考https://help.aliyun.com/document_detail/450255.html获取token
    APPKEY="4gcQGbnhYyTmN9DS"       #获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist

    class TestTts:
        def __init__(self, data_list: list, tid, n_channels, rate):
            self.__id = tid
            self.n_channels = n_channels
            self.rate = rate
            self.__f = BytesIO()
            self.data_list = data_list
            self.token = ''
    
        def start(self, text: str):
            self.token = create_token()
            self.__text = text
            # self.__th = threading.Thread(target=self.__test_run)
            # self.__th.start()
            self.__test_run()
        
        def test_on_metainfo(self, message, *args):
            pass

        def test_on_error(self, message, *args):
            pass

        def test_on_close(self, *args):
            pass
            
            

        def test_on_data(self, data, *args):
            try:
                if b'Errmsg' not in data:
                    self.__f.write(data)

            except Exception as e:
                print("write data failed:", e)

        def test_on_completed(self, message, *args):
            self.data_list.append(self.__f.getvalue())
            self.__f.seek(0)
            self.__f.truncate()

        def __test_run(self):
            try:
                tts = nls.NlsSpeechSynthesizer(url=URL,
                                            token=self.token,
                                            appkey=APPKEY,
                                            on_metainfo=self.test_on_metainfo,
                                            on_data=self.test_on_data,
                                            on_completed=self.test_on_completed,
                                            on_error=self.test_on_error,
                                            on_close=self.test_on_close,
                                            callback_args=[self.__id])
                print("{}: session start".format(self.__id))
                r = tts.start(self.__text, voice="zhiyue")
                print("{}: tts done with result:{}".format(self.__id, r))
            except Exception as e:
                print(e)
            
    n_channels = 1
    sample_rate = 16000
    data_list = []
    t = TestTts(data_list, 0, n_channels, sample_rate,)
    p = pyaudio.PyAudio()
    out = p.open(format=pyaudio.paInt16,
        channels=n_channels,
        rate=sample_rate,
        # frames_per_buffer=65536,
        output=True)
    

    playing_thread = threading.Thread(target=playing, args=(out, data_list, n_channels, sample_rate, ))
    playing_thread.start()

    def say_(text: str, delay: bool = True):
        t.start(text)
        if delay:
            time.sleep(0.3 * len(text))
        

    say = say_

    use_vision = False

    say('语音系统正在启动')
    # time.sleep(5)
    

    with open(os.path.join(pat, 'qw_api.key')) as f:
        api_key=f.read()

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
    say(llm_call('作为Danny的智能音箱，你会提醒吃药和按时作息等生活事项，请用一句话自我介绍：'))

    # import sys
    # sys.path.append(r'D:\git_repos\pn-2')
    # from codes.a24_life_assist.a2411_voice_announcer import qwen2vl_2b as inference
    if use_vision:
        import qwen2vl_2b as inference
    
    
    # say('你好，我是大泥猫的智能音箱！')
    # say('语音系统移启动')

    t1 = get_now()
    if t1.minute != 0:
        announce_time(t1)
    

    while True:
        time.sleep(1)
        t1 = get_now()  # .replace(minute=0)

        # if (t1.hour, t1.minute) != (21, 35):
        #     continue

        if t1.minute != 0:
            continue

        if t1.second > 5:
            continue

        announce_time(t1, do_not_disturb=True)

        # playing(out, buffer, n_channels, sample_rate, )

    
    # 停止数据流
    out.stop_stream()
    out.close()
    p.terminate()

