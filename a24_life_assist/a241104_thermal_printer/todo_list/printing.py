
import tempfile
import win32gui
import win32print
import win32con
import win32ui
from PIL import Image, ImageWin, ImageDraw


from blabel import LabelWriter

import os

fin = tempfile.TemporaryFile(mode='w', encoding='utf-8')


pat = os.path.join(os.getcwd(), r'codes\a24_life_assist\a241104_thermal_printer\todo_list')


def print_list(lst: list, **kwargs):

    print(pat)
    item_template = os.path.join(pat, r"templ.html")
    style = os.path.join(pat, r"style.css")
    pdf_out = os.path.join(pat, r"1.pdf")

    label_writer = LabelWriter(item_template, default_stylesheets=(style,))

    label_writer.write_labels([dict(lst=lst, **kwargs)], target=pdf_out)
    if 'test' not in kwargs.keys() or not kwargs['test']:
        os.startfile(pdf_out, "print")



if __name__ == '__main__':
    test_list = [{"text": "gwn yw", "value": True, "date": "2024-11-19 14:17:49"},
                 {"text": "吃饭和吃药", "value": True, "date": "2024-11-19 14:17:49"}]
    print_list([item | {"id": i + 1} for i, item in enumerate(test_list)])

