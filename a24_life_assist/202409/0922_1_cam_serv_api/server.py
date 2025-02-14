from flask import Flask, request, Response, make_response, jsonify
import json
from http import HTTPStatus
from dashscope import Application

app = Flask(__name__)

image_data = b''
history = []
prompt = {}

@app.route('/upload', methods=['POST'])
def upload_image():
    global image_data
    # 从请求中获取图像数据
    image_data = request.files['image'].read()
    return b'OK'

def generate_frames():
    global image_data
    while True:
        frame = image_data
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    global image_data
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image', methods=['GET', 'POST'])
def image_feed():
    global image_data
    response = make_response(image_data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


@app.route('/get-prompt', methods=['POST'])
def get_prompt():
    global prompt
    if not prompt:
        prompt = json.load(open(r"./init_prompt.json", 'r'))
    return Response(json.dumps(prompt).encode('utf-8'))


@app.route('/get-output', methods=['POST'])
def get_output():
    global history, prompt
    prompt = request.get_json()

    response = Application.call(app_id='75c5ece0bbd44a7bad3e149fa0c4d54f',
                                prompt='Follow the instructions',
                                api_key='sk-0f5095a155d5413583fdfe2c7fea62a8',)

    if response.status_code != HTTPStatus.OK:
        print('request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
        return Response(None, status=response.status)
    else:
        print(response.output)
        
        history.append(response.output)
        json.dump(history, open(r"./conversation.json", 'w'))

        return jsonify(response.output)


@app.route('/get-history', methods=['POST'])
def get_history():
    data = json.load(open(r"./conversation.json", 'r'))
    return jsonify(data)


if __name__ == '__main__':
    history = json.load(open(r"./conversation.json", 'r'))
    prompt = json.load(open(r"./init_prompt.json", 'r'))
    app.run(host='0.0.0.0', port=8091)
