import os
import re
import time
import requests
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

response = requests.get("https://mirrors.tencent.com/lede/snapshots/targets/sunxi/cortexa53/packages/", headers = headers)

# s = response.text
# print(s)

# filename = r"C:\Users\danim\Downloads\Index of _lede_snapshots_targets_sunxi_cortexa53_packages_.html"
filename = r"C:\Users\danim\Downloads\Index of _snapshots_targets_sunxi_cortexa53_packages_.html"

dir_path = os.path.join(r'C:\Users\danim\Downloads', 'ipk_6.6.47/')
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(filename,'r') as f:
    s = f.read()


lst = re.findall(r'https://[A-Za-z0-9_/\-\.]+/snapshots/targets/sunxi/cortexa53/packages/[^"/\\<>]*\.ipk', s)
print(lst)

saved_paths = []

for url in lst[::-1]:
    save_path = os.path.join(dir_path, os.path.basename(url))
    while True:
        try:
            # print(f'正在下载{url}')
            if os.path.exists(save_path):
                saved_paths.append(save_path)
                print(f'已完成: {len(saved_paths)}/{len(lst)} 文件已存在: {save_path}')
                break
            urllib.request.urlretrieve(url, save_path)
        except Exception as e:
            print(f'下载失败: {url} {str(e)}')
            time.sleep(0.5)
            continue
        else:
            saved_paths.append(save_path)
            print(f'已完成: {len(saved_paths)}/{len(lst)} 保存至: {save_path}')
            break


