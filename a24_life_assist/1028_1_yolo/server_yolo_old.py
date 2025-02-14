import time
# from flask import Flask, request, Response, make_response, jsonify
import json
# from http import HTTPStatus
from datetime import datetime
import cv2
from threading import Thread
import os
import boto3

# app = Flask(__name__)

image_data = b''
history = []
prompt = {}

def upload():
    global image_data

    while True:
        cap = cv2.VideoCapture(45)

        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

        ret, frame = cap.read()
        
        if not ret:
            print("无法读取帧")
            time.sleep(0.2)
            continue

        frame = cv2.resize(frame, (480, 320))

        # 将图像转换为JPEG格式
        # _, img_encoded = cv2.imencode('.jpg', frame)
        img_encoded = frame


        # 上传文件
        now = datetime.now()
        filename = '{}-{}.jpg'.format(monitor_node_name, now.strftime('%Y-%m-%d-%H-%M-%S-%f'))
        local_file_path = './{}'.format(filename)  # 本地文件路径

        cv2.imwrite(local_file_path, img_encoded)

        s3_file_key = '{}/{}/{}/{}/{}'.format(now.year, now.month, now.day, now.hour, filename)  # S3中的文件名，可以包括文件夹
        s3.upload_file(local_file_path, bucket, s3_file_key)
        print(f'Successfully uploaded {filename}')
        os.remove(local_file_path)


        image_data = img_encoded.tobytes()

        
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
    bucket = 'monitor-1'
    endpoint_url = 'https://{}.oss-cn-heyuan.aliyuncs.com'.format(bucket)
    access_key = 'LTAI5tB3JEkng4ZGbm39DfDf'
    # secret_key = input('Paste secret:')
    with open('1.key', 'rt') as f:
        secret_key = f.read().strip()
    
    # 创建 S3 客户端实例并指定 endpoint 和凭证信息
    s3 = boto3.client('s3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    verify=False)  # 如果不需要SSL验证，可以设置verify=False，即http或者https
    
    upload_thread = Thread(target=upload)
    upload_thread.start()

    # app.run(host='0.0.0.0', port=8091)

