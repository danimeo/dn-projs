import requests
from PIL import Image
from io import BytesIO
import cv2
import numpy as np



url = 'http://danim.space:8091/video_feed'


# 定义一个函数来获取图像帧
def get_frame():
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                frame = chunk.split(b'\r\n')[-2]
                frame = Image.open(BytesIO(frame))
                frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                return frame
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

while True:
    frame = get_frame()
    if frame is not None:
        cv2.imshow('FROM SERVER', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

cv2.destroyAllWindows()