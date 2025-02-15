
# 参考来源（不完全）：
# https://blog.mzh.ren/zh/posts/2022/10/pyaudio-record/

import csv
import platform
import time
# from flask import Flask, request, Response, make_response, jsonify
import json
# from http import HTTPStatus
from datetime import datetime
import cv2
from threading import Thread
import os
from PIL import Image,ImageFont,ImageDraw
import numpy as np
import pyaudio
import wave
import boto3
from pytz import timezone
tzchina = timezone('Asia/Chongqing')

# app = Flask(__name__)

image_data = b''
history = []
prompt = {}

def try_video_id():
    for i in [0, 1, 45] + list(range(0, 50))[::-1]:
        cap = cv2.VideoCapture(i)
        ret, frame = cap.read()
        
        if ret:
            return i
        cap.release()
    return 45

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
rec_interval = 56
# WAVE_OUTPUT_FILENAME = "~/audio_recs/record.wav"


# 可以在创建 VAD 时设置主动性模式，如下所示
# vad = webrtcvad.Vad(3)

def get_now():
    return datetime.now(tzchina)

def record(output_path):
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        # is_speech_frame = vad.is_speech(data, RATE)
        # print(is_speech_frame)
        frames.append(data)
    print("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(output_path, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def audio_upload():

    while True:
        now = get_now()
        filename = '{}-{}.wav'.format(monitor_node_name, now.strftime('%Y-%m-%d-%H-%M-%S-%f'))
        dir_path = '{}/audios'.format(local_dir_path)
        dir_path = '{}/{}'.format(dir_path, monitor_node_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        local_file_path = '{}/{}'.format(dir_path, filename)
        
        record(local_file_path)
        upload_file(local_file_path, filename, now, dir_prefix=f'{monitor_node_name}/audio/')

        time.sleep(rec_interval)


def upload_file(local_file_path, filename, now, dir_prefix=''):
    if os.path.exists(local_file_path):
        s3_file_key = '{}{}/{}/{}/{}/{}'.format(dir_prefix, now.year, now.month, now.day, now.hour, filename)
        s3.upload_file(local_file_path, bucket, s3_file_key)
        s3_file_key = '{}{}/{}/{}/{}/{}'.format(dir_prefix, now.year, now.month, now.day, now.hour, 'latest.' + filename.split('.')[-1])
        s3.upload_file(local_file_path, bucket, s3_file_key)
        print(f'Successfully uploaded {filename}')
        os.remove(local_file_path)
    else:
        print(f'Failed to process {local_file_path}')




def upload():
    global image_data

    vid = try_video_id()
    print('vid:', vid)

    while True:

        cap = cv2.VideoCapture(vid)

        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # time.sleep(3)

        ret, frame = cap.read()
        now = get_now()
        
        if not ret or not frame.tobytes():
            print("无法读取帧")
            time.sleep(0.2)
            cap.release()
            continue

        # print(frame)
        # frame = cv2.resize(frame, (480, 320))
        
        font_style = ImageFont.truetype(font_path, 16, encoding="utf-8")
        #创建一张底图,用来绘制文字
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        #在图片上添加文字
        #fill用来设置绘制文字的颜色,(R,G,B)
        # #95bfdf
        date_text = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        draw.rectangle((0, 0, 480, 20), fill=(0xdf,0xbf,0x95))
        # draw.rectangle((0, 0, 270, 40), fill=(0xdf,0xbf,0x95))
        draw.text((5, 0), f'{date_text} [{monitor_node_name}]', fill=(255,255,255),font=font_style)
        # draw.text((5, 19), f'Dajun\'s {monitor_node_name}', fill=(255,255,255),font=font_style)
        frame = np.array(img)


        # 将图像转换为JPEG格式
        # _, img_encoded = cv2.imencode('.jpg', frame)
        img_encoded = frame


        # 上传文件
        filename = '{}-{}.jpg'.format(monitor_node_name, now.strftime('%Y-%m-%d-%H-%M-%S-%f'))
        dir_path = '{}/images'.format(local_dir_path)
        dir_path = '{}/{}'.format(dir_path, monitor_node_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        local_file_path = '{}/{}'.format(dir_path, filename)  # 本地文件路径
        
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
        cv2.imwrite(local_file_path, img_encoded)

        image_data = img_encoded.tobytes()

        upload_file(local_file_path, filename, now, dir_prefix=f'{monitor_node_name}/')

        cap.release()
        time.sleep(cap_interval)
    
    
# def generate_frames():
#     global image_data
#     while True:
#         frame = image_data
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed', methods=['GET', 'POST'])
# def video_feed():
#     global image_data
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/image', methods=['GET', 'POST'])
# def image_feed():
#     global image_data
#     response = make_response(image_data)
#     response.headers.set('Content-Type', 'image/jpeg')
#     return response



if __name__ == '__main__':

    cap_interval = 60
    monitor_node_name = 'monitor-1'
    bucket = 'danim-monitors'
    endpoint_url = 'https://{}.oss-cn-heyuan.aliyuncs.com'.format(bucket)
    # local_dir_path = '/home/nano/.cache'
    local_dir_path = '~/.cache'
    # secret_key = input('Paste secret:')

    def get_paths():
        os_name = platform.system()
        if os_name == "Windows":
            path_prefix = r'D:\git_repos\d-notes\repos'
        else:
            path_prefix = '/data/repos/d'  # zero3_ubuntu
        repo_path = f'{path_prefix}'
        ak_dir_path = os.path.join(repo_path, '.api_keys')
        # print(ak_dir_path, sep='\n')
        return repo_path, ak_dir_path
        
    def read_ak_from_csv(ak_csv_path, id_ev_key='', secret_ev_key=''):
        csv_reader = csv.reader(open(ak_csv_path, 'r'))
        next(csv_reader)
        ak_id, secret = next(csv_reader)
        if id_ev_key:
            os.environ['ALIYUN_AK_ID'] = ak_id
        if secret_ev_key:
            os.environ['ALIYUN_AK_SECRET'] = secret
        # print(ak_id, secret)
        return ak_id, secret
    
    repo_path, ak_dir_path = get_paths()
    font_path = os.path.join(repo_path, r'assets/fonts/YaHei_Consolas_Hybrid_1.12.ttf')
    print('font_path:', font_path)
    ak_csv_path = os.path.join(ak_dir_path, 'aliyun-oss-1.csv.key')
    access_key, secret_key = read_ak_from_csv(ak_csv_path, id_ev_key='ALIYUN_AK_ID', secret_ev_key='ALIYUN_AK_SECRET')

    os_name = platform.system()
    if os_name != "Windows":
        os.system('ntpdate cn.pool.ntp.org')

    print(get_now())
    
    # 创建 S3 客户端实例并指定 endpoint 和凭证信息
    s3 = boto3.client('s3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    verify=False)  # 如果不需要SSL验证，可以设置verify=False，即http或者https
    
    # upload_thread = Thread(target=audio_upload)
    # upload_thread.start()
    upload()

    # app.run(host='0.0.0.0', port=8091)

