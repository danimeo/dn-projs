import cv2
import requests
import time

server_url = 'http://danim.space:8091'


# 捕获摄像头视频流


while True:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        break

    # 将图像转换为JPEG格式
    _, img_encoded = cv2.imencode('.jpg', frame)

    # 发送HTTP POST请求
    response = requests.post(server_url + '/upload', files={'image': img_encoded.tobytes()})

    if response.status_code != 200:
        print(f"发送失败，状态码: {response.status_code}")
    
    cap.release()
    time.sleep(1)
