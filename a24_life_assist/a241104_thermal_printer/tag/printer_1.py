# -*- coding: utf-8 -*-
import win32ui, time

hDC = win32ui.CreateDC()
hDC.CreatePrinterDC('Xprinter XP-D10')
hDC.StartDoc("标签名")
hDC.StartPage()

Ctime = time.strftime("%y/%m/%d %H:%M",time.localtime())
Num   = 'A201'
Name  = '张三 男 66'

DataList = [
    [15 , 14, '编号:', {'name': '宋体', 'height': 27}],
    [15 , 54, '姓名:', {'name': '宋体', 'height': 27}],
    [15 , 94, '项目:', {'name': '宋体', 'height': 27}],
    [90 , 10,  Num   , {'name': '宋体', 'height': 33, 'weight': 1000}],
    [190, 14,  Ctime , {'name': '宋体', 'height': 25}],
    [90 , 52,  Name  , {'name': '宋体', 'height': 33, 'weight': 1000}],
    ]

for data in DataList:
    font = win32ui.CreateFont(data[3])
    hDC.SelectObject(font)
    hDC.TextOut(data[0], data[1], data[2])

# hDC.DrawText(txt,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT)

项目 = '个人档案、个人档案、个人档案、个人档案、个人档案、个人档案、个人档案、个人档案、个人档案、个人档案'
font = win32ui.CreateFont({'name':'宋体', 'height': 22,})
hDC.SelectObject(font)

#长文本换行
fsize  = 22  # 字体大小
min_x  = 24  # X轴最小值
max_x  = 360 # X轴最大值
text_x = 90  # 字X坐标
text_y = 100 # 字Y坐标

font = win32ui.CreateFont({'name':'宋体', 'height': fsize})
hDC.SelectObject(font)

#用list(项目)转为列表，后用for加位置判断一个个字打入，实现换行
for text in list(项目):
    if text_x > max_x and text not in ['、']: #判断 text_x是否超过最大设定值 及 是否'、'开头
        text_y += fsize + 3 # 行间距3
        text_x = min_x
    hDC.TextOut(text_x, text_y, text)
    text_x += fsize + 0 # 字间距0


hDC.EndPage()
hDC.EndDoc()