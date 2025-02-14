---
title: mini-omni省力脚本
---


```bash
git clone https://github.com/gpt-omni/mini-omni.git
cd mini-omni

conda create -n omni python=3.10
conda activate omni
pip install -r requirements.txt

python3 server.py --ip '0.0.0.0' --port 60808


python3 webui/omni_gradio.py API_URL=http://0.0.0.0:60808/chat 
```
