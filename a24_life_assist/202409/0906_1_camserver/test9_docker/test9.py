from flask import Flask, Response
import cv2

app = Flask(__name__)

# 初始化摄像头
camera = cv2.VideoCapture(0)

def gen_frames():
    """视频流生成器"""
    while True:
        success, frame = camera.read()  # 读取摄像头画面
        if not success:
            break
        else:
            # 将OpenCV图像转换为JPEG格式
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 按需添加数据头

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return "Welcome! To see the camera stream, open the video_feed URL."

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
