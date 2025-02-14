
from io import BytesIO
import time
from PIL import Image,ImageFont,ImageDraw
from datetime import datetime

from flask import Flask, request, Response, make_response, jsonify


app = Flask(__name__)

image_data = b''


def draw_text():
    #加载字体文件
    font_style = ImageFont.truetype(r"C:\Users\danim\Music\simsun.ttf", 42, encoding="utf-8")
    #创建一张底图,用来绘制文字
    img = Image.new("RGB",(512,512),(0,0,0))
    draw = ImageDraw.Draw(img)
    #在图片上添加文字
    #fill用来设置绘制文字的颜色,(R,G,B)
    now = datetime.now()
    draw.text((50,120), now.strftime('%Y-%m-%d %H:%M:%S') ,fill=(255,255,255),font=font_style)
    # draw.text((100,200),"你好",fill=(0,255,0),font=font_style)
    #保存图片
    # img.save("draw_img.jpg")

    img_byte = BytesIO()
    img.save(img_byte, format='JPEG') # format: PNG or JPEG
    binary_content = img_byte.getvalue()  # im对象转为二进制流
    
    return binary_content


def generate_frames():
    global image_data
    while True:
        frame = draw_text()
        time.sleep(0.1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    global image_data
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port=8091)


