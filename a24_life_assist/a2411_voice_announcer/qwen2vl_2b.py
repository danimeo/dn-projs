from datetime import datetime

from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from modelscope import snapshot_download
import torch
from formatron.formatter import FormatterBuilder
from formatron.integrations.transformers import create_formatter_logits_processor_list



model_dir=snapshot_download("qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4")
# default: Load the model on the available device(s)
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_dir, torch_dtype="auto", device_map="auto"
)
device = model.device

# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     model_dir,
#     torch_dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

# default processer
tokenizer = AutoTokenizer.from_pretrained(model_dir)
processor = AutoProcessor.from_pretrained(model_dir)

# The default range for the number of visual tokens per image in the model is 4-16384. You can set min_pixels and max_pixels according to your needs, such as a token count range of 256-1280, to balance speed and memory usage.
# min_pixels = 256*28*28
# max_pixels = 1280*28*28
# processor = AutoProcessor.from_pretrained(model_dir, min_pixels=min_pixels, max_pixels=max_pixels)

messages = []


def infer(txt: str, image_url: str = ''):
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": image_url,
            },
            {"type": "text", "text": txt},
        ] if image_url else [{"type": "text", "text": txt}],
    })

    # Preparation for inference
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to(device)

    # Inference: Generation of the output
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    return output_text[0]


if __name__=='__main__':
    import pyttsx3
    engine = pyttsx3.init()  # 创建engine并初始化

    def say(text: str):
        engine.say(text)
        engine.runAndWait()  # 等待语音播报完毕

    say('监控系统移启动')

    while True:
        messages.clear()
        # inp = input('User: ')
        inp = ''
        t1 = datetime.now()
        time_range_name = ''
        if t1.hour <= 5:
            time_range_name = '凌晨'
        elif t1.hour <= 11:
            time_range_name = '上午'
        elif t1.hour <= 13:
            time_range_name = '中午'
        elif t1.hour <= 18:
            time_range_name = '下午'
        else:
            time_range_name = '晚上'

        hour_name = f'{t1.hour % 12 if t1.hour % 12 else 12}点'

        announce_time_text = f'现在是{time_range_name}{hour_name}{"{:02d}分".format(t1.minute) if t1.minute else "整"}'

        if not inp.strip():
            inp = f"{announce_time_text}。如果画面中有人"
        image_url = f"https://danim-2.oss-cn-heyuan.aliyuncs.com/danim-2/{t1.year}/{t1.month}/{t1.day}/{t1.hour}/latest.jpg"
        print(image_url)
        output_text = infer(inp, image_url=image_url)
        print('Assistant:', output_text)
        say(f'{announce_time_text}。{output_text}')



        # import torch
        # from formatron.integrations.transformers import create_formatter_logits_processor_list
        # from formatron.formatter import FormatterBuilder
        # from formatron.schemas.dict_inference import infer_mapping
        # # torch.manual_seed(520)

        # f = FormatterBuilder()
        # schema = infer_mapping({"med_unit_type": "pill", "color": "white", "size": "bigger", "amount": "1/2"}
        #                         )
        # f.append_line(f"{f.json(schema, capture_name='json')}")
        # logits_processor = create_formatter_logits_processor_list(tokenizer, f)
        # inputs = processor(["""<|system|>
        # You are a helpful assistant.<|end|>
        # <|user|>Extract information from the image into json.<|end|>
        # <|assistant|>"""],
        #     images=image_inputs,
        #     videos=video_inputs,
        #     padding=True,
        #     return_tensors="pt").to(device)
        # print(processor.batch_decode(model.generate(**inputs, 
        #                                             top_p=0.5, temperature=1,
        #                                             max_new_tokens=100, logits_processor=logits_processor),
        #                                             ))
        # print(logits_processor[0].formatters_captures)
        # # possible output:
        # # [{'json': {'name': '周明瑞', 'age': 34}}]
