
import tempfile
import win32gui
import win32print
import win32con
import win32ui
from PIL import Image, ImageWin, ImageDraw


from blabel import LabelWriter

import os

fin = tempfile.TemporaryFile(mode='w', encoding='utf-8')


pat = os.path.join(os.getcwd(), r'DNet\1104_1_escpos')
print(pat)
item_template = os.path.join(pat, r"item_template.html")
style = os.path.join(pat, r"style.css")
pdf_out = os.path.join(pat, r"1.pdf")

label_writer = LabelWriter(item_template, default_stylesheets=(style,))
records = [
    dict(size_name=22, size_date=14,
         sample1_id="https://app.appsmith.com/app/my-first-application/page1-6712189db5c29c51ea495355?branch=master", 
         sample1_name="面包盒", 
         sample2_id="https://app.appsmith.com/app/my-first-application/page1-6712189db5c29c51ea495355?branch=master", 
         sample2_name="打印单收集盒",
         sample3_id="https://app.appsmith.com/app/my-first-application/page1-6712189db5c29c51ea495355?branch=master", 
         sample3_name="打印单收集盒"),
]

label_writer.write_labels(records, target=pdf_out)



os.startfile(pdf_out, "print")

 
# pdfDoc = fitz.open(pdf_out)
# for page in pdfDoc.pages():
#     # 将页面转换为图片
#     rotate = int(0)
#     # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
#     # 此处若是不做设置，默认图片大小为：792X612, dpi=72
#     # pix = page.get_pixmap()
#     zoom_x = 6
#     zoom_y = 6
#     # (1.33333333-->1056x816)   (2-->1584x1224)  (3-->3572x2526)
#     # x和y的值越大越清晰，图片越大，但处理也越耗时间，这里取决于你想要图片的清晰度
#     # 默认为1.333333，一般日常使用3就够了，不能设置太大，太大容易使电脑死机
#     mat = fitz.Matrix(zoom_x, zoom_y)
#     pix = page.get_pixmap(matrix=mat, dpi=None, colorspace='rgb', alpha=False)
#     imageName = pdf_out.split("\\")[len(pdf_out.split("\\"))-1]
#     target_img_name = pat + '\\%s.png' % imageName #构造图片名字
#     # 保存图片
#     pix.save(target_img_name)
 

#     # 创建一个内存DC
#     # mem_dc = win32gui.CreateCompatibleDC(None)
#     hDC = win32ui.CreateDC()
#     hDC.CreatePrinterDC('Xprinter XP-D10')
#     # printer_name = win32print.GetDefaultPrinter()

#     # 使用PIL库
#     # image = Image.new("RGB", (width, height), (255, 255, 255))
#     # image = Image.open(target_img_name)
#     # width, height = image.size

#     # 参考 http://timgolden.me.uk/python/win32_how_do_i/print.html#win32print



#     #printable_area = (300, 270) # 打印纸尺寸
#     #printer_size = (300, 270)

#     # 打开图片并缩放
#     bmp = Image.open(target_img_name)
#     if bmp.size[0] < bmp.size[1]:
#         bmp = bmp.rotate(90)

#     # ratios = [1.0 * printable_area[0] / bmp.size[1], 1.0 * printable_area[1] / bmp.size[0]]
#     # scale = min(ratios)
#     scale = 1

#     hDC.StartDoc(target_img_name)
#     hDC.StartPage()

#     dib = ImageWin.Dib(bmp)
#     scaled_width, scaled_height = [int(scale * i) for i in bmp.size]

#     x1 = 20 # 控制位置
#     y1 = -30
#     x2 = x1 + scaled_width
#     y2 = y1 + scaled_height
#     dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

#     hDC.EndPage()
#     hDC.EndDoc()
#     hDC.DeleteDC()


# 参考链接：
# https://blog.csdn.net/zbj18314469395/article/details/98329442
# https://blog.aspose.com/zh/pdf/print-pdf-in-python/
# https://www.cnblogs.com/catfeel/p/15727397.html
