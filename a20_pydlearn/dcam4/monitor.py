import time

import pyautogui
import pytesseract
from PIL import Image

# 设置 pytesseract 的路径
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# 获取屏幕分辨率
# screenWidth, screenHeight = pyautogui.size()

# pyautogui.click(x=100, y=100)

# screenshot = pyautogui.screenshot()

# screenshot.save('screenshot.png')
# image = Image.open('screenshot.png')
# text = pytesseract.image_to_string(image)
# while 'Python 3.10' in text and '(ds)' in text:
pc_box = pyautogui.locateOnScreen('pycharm_icon.png')
while pc_box:
    print('禁止写代码！')
    box = pyautogui.locateOnScreen('close_pycharm_1.png')
    pyautogui.click(x=box.left, y=box.top)
    time.sleep(0.2)
    # box = pyautogui.locateOnScreen('close_pycharm_2.png')
    # pyautogui.click(x=box.left, y=box.top)
    pyautogui.keyDown('enter')
    # screenshot.save('screenshot.png')
    # image = Image.open('screenshot.png')
    # text = pytesseract.image_to_string(image)
    pc_box = pyautogui.locateOnScreen('pycharm_icon.png')
# print(pytesseract.image_to_boxes(image))
# print(text)
# 查找特定文字在屏幕上的位置
# if 'hello world' in text:
    # x, y = pyautogui.locateOnScreen('hello_world.png')
    # # 点击找到的文字
    # pyautogui.click(x, y)