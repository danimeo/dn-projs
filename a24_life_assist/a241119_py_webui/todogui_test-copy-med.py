import json
from datetime import datetime
import os
import shutil

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

import sys
sys.path.append(os.getcwd())
from codes.a24_life_assist.a241104_thermal_printer.todo_list.printing import print_list

check_lst_path = ''
check_lst, checkboxes = [], []


def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

# with ui.row():
#     ui.checkbox('Checkbox', on_change=show)
#     ui.switch('Switch', on_change=show)
# ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
# with ui.row():
#     ui.input('Text input', on_change=show)
#     ui.select(['One', 'Two'], value='One', on_change=show)
# ui.link('And many...', '/documentation').classes('mt-8')


# class Demo:
#     def __init__(self):
#         self.number = 1
#         self.text = ''
        

# demo = Demo()
# v = ui.checkbox('visible', value=True)
# with ui.column().bind_visibility_from(v, 'value'):
#     ui.slider(min=1, max=3).bind_value(demo, 'number')
#     ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
#     ui.number().bind_value(demo, 'number')



get_time = lambda: datetime.now().strftime('%Y-%m-%d %H:%M')

class Item:
    def __init__(self, text: str, value: bool = False, date: str = get_time(), id=-1):
        self.id = id
        self.text = text
        self.value = value
        self.date = date

display_full = lambda item: f'{item.id} {item.text} {item.date}'

manual = False



def on_check(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    if manual:
        on_save(update_list_=True)

def update_boxes(checkboxes: list, check_lst: list):
    
    for cb in checkboxes:
        cb.delete()
    checkboxes.clear()

    with ui.column():
        for i in range(len(check_lst)):
            with ui.row():
                cb = ui.checkbox(display_full(check_lst[i]), on_change=on_check)
                # cb.
                cb.set_value(check_lst[i].value)
                checkboxes.append(cb)
            # checkboxes[i]._text = display_full(check_lst[i])
        # on_save()



def update_list(checkboxes: list, check_lst: list):
    
    for i in range(len(checkboxes)):
        check_lst[i].value = checkboxes[i].value




def update(check_lst: list, checkboxes: list, mode='r'):
    
    if mode == 'w':
        with open(check_lst_path, 'w') as fp:
            json.dump([vars(item) for item in check_lst], fp,
                      indent=4, sort_keys=True, ensure_ascii=False)
    else:
        with open(check_lst_path, 'r') as fp:
            check_lst.clear()
            check_lst += [Item(**itm) for itm in json.load(fp) if itm['id'] >= 0]


    # len_lst, len_boxes = len(check_lst), len(checkboxes)
    # len_diff = len_lst - len_boxes
    # if len_diff < 0:
    #     for i in range(len_lst, len_boxes):
    #         checkboxes[i].delete()
    #     del checkboxes[len_lst:]
    # elif len_diff > 0:
    #     for i in range(len_boxes, len_lst):
    #         with ui.row():
    #             cb = ui.checkbox(display_full(check_lst[i]), on_change=on_check)
    #             # cb.
    #             checkboxes.append(cb)



input_box = None
id_input_box = None

def on_add():
    now = get_time()
    item0 = Item(input_box.value, date=now, id=max([0] + [itm.id for itm in check_lst]) + 1)
    check_lst.append(item0)
    print('on_add')
    on_save(update_list_=False)
    update_boxes(checkboxes, check_lst)
    input_box.value = ''


def on_clear():
    now = get_time()
    check_lst.clear()
    print('on_clear')
    on_save(update_list_=False)
    update_boxes(checkboxes, check_lst)
    

def on_print():
    print_list([vars(item) for i, item in enumerate(check_lst)], date=get_time(), test=False)


def on_save(update_list_=True):
    # manual = True
    ui.notify(f'已保存')
    if update_list_:
        update_list(checkboxes, check_lst)
    update(check_lst, checkboxes, 'w')
    # len_boxes = len(checkboxes)
    # for i in range(len_boxes):
    #     checkboxes[i].delete()
    # del checkboxes[len(check_lst):]
    # update_boxes(checkboxes, check_lst)
    # manual = False



def delete_by_id():
    global check_lst
    text = id_input_box.value
    if text.isdigit():
        id = int(text) 
        itms = [itm for itm in check_lst if itm.id != id]
        check_lst.clear()
        check_lst += itms

        print('on_delete_by_id')
        on_save(update_list_=False)
        update_boxes(checkboxes, check_lst)


def updating():
    update(check_lst, checkboxes)
    update_boxes(checkboxes, check_lst)
    shutil.copy(check_lst_path, check_lst_backup_path)


with ui.column():
    with ui.row():
        input_box = ui.input('事项名称')
        ui.button('新增', on_click=on_add)
        ui.button('清空', on_click=on_clear)
        ui.button('打印', on_click=on_print)
        ui.button('保存', on_click=on_save)
        ui.button('刷新', on_click=updating)
    with ui.row():
        id_input_box = ui.input('要删除的ID')
        id_input_box.value = '-1'
        ui.button('删除', on_click=delete_by_id)


if __name__ in {"__main__", "__mp_main__"}:
    check_lst_path = r"D:\git_repos\snote-2\source\_posts\medtodo-today.json"
    
    if not os.path.exists(check_lst_path):
        with open(check_lst_path, 'w') as f:
            json.dump(check_lst, f)
            
    now = datetime.now()
    check_lst_backup_path =  os.path.join(os.path.dirname(check_lst_path), rf"../todo/{now.year}-{now.month}/{now.day}/")
    if not os.path.exists(check_lst_backup_path):
        os.makedirs(check_lst_backup_path)

    updating()

    ui.run(port=8091)
