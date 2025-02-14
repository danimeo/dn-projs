
### 在 RWKV-Runner 中使用

#### RWKV (ai-creator API)
API URL: `https://rwkv.ai-creator.net/chntuned`
API Key: 
API聊天模型名: `rwkv`
API续写模型名: `rwkv`
核心 API URL: 

#### 通义千问 API
API URL: `https://dashscope.aliyuncs.com/compatible-mode`
API Key: `sk-`
API聊天模型名: `qwen-turbo-latest`
API续写模型名: `qwen-turbo-latest`
核心 API URL: 




---

### Python调用
```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-turbo-latest", 
    # 其他：qwen-plus, qwen-vl-max-1030, qwen-vl-plus-0809
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
    )
    
print(completion.model_dump_json())
```