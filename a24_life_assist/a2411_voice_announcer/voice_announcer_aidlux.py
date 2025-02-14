# 参考来源：https://blog.csdn.net/white_hat_2009/article/details/124784680

#导入pyttsx3库
import android
from threading import Thread
import time
from datetime import datetime


droid = android.Android()


def say(text: str):
    return droid.ttsSpeak(text)



# -------------------记得：语音报时附带其他提醒是备用提醒手段，能不用就不用！


def announce_time(t1: datetime, do_not_disturb: bool = False):
    if 0 <= t1.hour < 9:
        return

    time_range_name = ''
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

    hour_name = f'{t1.hour % 12 if t1.hour % 12 else 12}点'

    announce_time_text = f'现在是{time_range_name}{hour_name}{"{:02d}分".format(t1.minute) if t1.minute else "整"}'

    if not 0 <= t1.hour < 9:
        say(announce_time_text)
        say(announce_time_text)
        # say(f"记得看打印的清单")
    if t1.hour == 21:
        say(f'{hour_name}了，吃托莫西汀，和阿普唑仑')



if __name__ == '__main__':

    say('语音系统移启动')

    announce_time(datetime.now())

    while True:
        now = datetime.now()  # .replace(minute=0)

        # if (now.hour, now.minute) != (21, 35):
        #     continue

        time.sleep(1)

        if now.minute != 0:
            continue

        if now.second > 5:
            continue


        announce_time(now, do_not_disturb=True)
    

