import time
import requests
import json


url = 'http://danim.space:8091/get-output'
# headers = {'Content-Type': 'application/json'}

history = []
prompt = {}

def get_output(_input: str):
    response = requests.post(url, json=prompt)
    if response.status_code == 200:
        data = response.json()
        content = json.loads(data['text'])
        print(content["output"])
        history.append(data)
        json.dump(history, open(r"DNet\202409\0922_1_cam_serv_api\conversation.json", 'w'), ensure_ascii=False,)
        # with open('output.txt', 'w') as f:
        #     f.write('\n\n'.join([json.loads(data['text']) for data in history]))
    else:
        print(f"请求失败，状态码: {response.status_code}")


if __name__=='__main__':
    history = json.load(open(r"DNet\202409\0922_1_cam_serv_api\conversation.json", 'r'))
    init_prompt = json.load(open(r"DNet\202409\0922_1_cam_serv_api\init_prompt.json", 'r'))
    while True:
        print(get_output(init_prompt["user_prompt"]))
        time.sleep(2)