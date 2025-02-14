
import json
import aspose.pdf as ap
import win32gui
import win32print
import win32con
import win32ui
from PIL import Image, ImageWin, ImageDraw

from faster_whisper import WhisperModel

model_size = "large-v3"

# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("audio.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

from blabel import LabelWriter

import os
from openai import OpenAI

pat = os.path.join(os.getcwd(), r'DNet\1104_1_escpos\chat')
print(pat)
item_template = os.path.join(pat, r"template.html")
style = os.path.join(pat, r"style.css")
pdf_out = os.path.join(pat, r"1.pdf")

content = ''

# with open(os.path.join(pat, 'qw_api.key')) as f:
#     api_key=f.read()

# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=api_key,
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )


# text = '''1101,0027: 
# 有可能：转向以线下上课为中心管理精力和时间，必然导致对记录和思考心理的关注降低。
# 但是我们有“绝对优先”规则：任何情况下，无条件全力保障对自己心理和注意的观察和把控，使其永远占据注意内容的那“top 1%”。也就是说，但凡多出来一点精力，都要优先用来保障这一基本的自我觉察能力（大致是因为我资源有限），否则很难“翻盘”，历史已经给了我很多次教训（8~9月就是一个例子）。

# 主观上，人只应该维持或改善身心健康，没有商量的余地；注意力/精力状况只应该变好，因此既然我们付出了*有效*努力，变好就应该在意料之中。
# '''
# completion = client.chat.completions.create(
#     model="qwen-max", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': f'请把以下内容改写成简洁、通顺的句子，不能改变原意，也不能漏掉细节：\n{text}'}],
#     )
    
# data = json.loads(completion.model_dump_json())
# content = data["choices"][0]["message"]["content"]

content = content.replace('\n', '<br />')


label_writer = LabelWriter(item_template, default_stylesheets=(style,))
records = [
    dict(sample1_name=content, 
         size_name=13, size_date=11 ,),
]


label_writer.write_labels(records, target=pdf_out)



# os.startfile(pdf_out, "print")

 