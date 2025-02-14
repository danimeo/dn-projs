from datetime import datetime, timedelta
import time
from threading import Thread

from dcam_framework2 import TimeFragment, TimeContainer, get_fragment, TimeCollection, Task, empty

now = datetime.now


class DistrCore:
    def __init__(self, balance_filename: str, distribution_filename: str, prices_filename: str):
        self.balance = 0.0
        self.tasks = []
        self.current_task_index = 0

        self.available_range = TimeFragment(now().replace(hour=8, minute=25, second=0, microsecond=0)
                 , now().replace(hour=23, minute=30, second=0, microsecond=0))
        available_content = TimeCollection()
        available_content.add(self.available_range)
        self.distribution = TimeContainer(capacity=available_content)

        self.prices = {}
        self.filenames = {'balance': balance_filename,
                          'distribution': distribution_filename,
                          'prices': prices_filename
                          }

    def load(self):
        with open(self.filenames['balance'], 'rt', encoding='utf-8') as file_input:
            self.balance = float(file_input.readline())

        with open(self.filenames['distribution'], 'rt', encoding='utf-8') as file_input:
            text = file_input.read()
        self.distribution.load(text)

        with open(self.filenames['prices'], 'rt', encoding='utf-8') as file_input:
            prices_list = [line.strip() for line in file_input.readlines()]
        for price_line in prices_list:
            if price_line.startswith('\ufeff'):
                price_line = price_line[1:]
            code_purpose_price = price_line.split('\t')
            self.prices[code_purpose_price[0]] = (code_purpose_price[1], float(code_purpose_price[2]))

    def save(self):
        with open(self.filenames['balance'], 'wt', encoding='utf-8') as file_output:
            file_output.write(str(self.balance))

        with open(self.filenames['distribution'], 'wt', encoding='utf-8') as file_output:
            file_output.write(self.distribution.text())

        prices_output = ''
        for code in self.prices:
            prices_output += code + '\t' + self.prices[code][0] + '\t' + str(self.prices[code][1]) + '\n'
        with open(self.filenames['prices'], 'wt', encoding='utf-8') as file_output:
            file_output.write(prices_output)

    def purchase_time(self, delta: timedelta, start=None):
        if now() not in self.distribution.capacity:
            print('现在不是可交易时间')
            return False

        if not start:
            start = now()
        self.distribution.add(get_fragment(start, delta, purchased=True))
        balance_change = -0.2 * delta.total_seconds() / 60
        print(balance_change, delta)

        if self.balance + balance_change >= 0:
            self.balance += balance_change
            print('时间段[' + str(start) + ' ~ ' + str(start + delta) + ']购买成功！当前余额为：' + str(self.balance))
        else:
            print('当前余额为：' + str(self.balance) + '，余额不足，无法购买时间')
            return False
        return True

    def purchase(self, task: Task):
        if now() not in self.distribution.capacity:
            print('现在不是可交易时间')
            return False

        task.pause()
        if not task.code or task.code not in self.prices or not task:
            print('交易失败：', task.code)
            return False

        balance_change = self.prices[task.code][1] * task.get_past_duration().total_seconds() / 60
        print(balance_change, self.prices[task.code][1], task.get_past_duration())
        task.stop()
        if self.balance + balance_change >= 0:
            self.balance += balance_change
            print('交易成功！当前余额为：' + str(self.balance))
        else:
            print('当前余额为：' + str(self.balance) + '，余额不足以完成交易')
        return True

    def purchase_all_tasks(self):
        successful = True
        for task in self.tasks:
            if not self.purchase(task):
                successful = False
        return successful

    def get_task_index(self, code: str):
        for i, task in enumerate(self.tasks):
            if task.code == code:
                return i
        return -1

    def __contains__(self, item):
        if isinstance(item, Task):
            for task in self.tasks:
                if item.name == task.name and item.code == task.code:
                    return True
        elif isinstance(item, str):
            for task in self.tasks:
                if item == task.code:
                    return True
        return False

    def print_prices(self):
        print('价目表：')
        for code in self.prices:
            print(' ', code, self.prices[code][0], self.prices[code][1])

    def print_details(self):
        print('已购时间清单：')
        col = self.distribution.content.get_purchased_collection()
        fragments = sorted(col.fragments)
        for fragment in fragments:
            print('  [' + str(fragment) + ']')
        print('余额：' + str(self.balance))


def execute(core: DistrCore, command: str):
    #try:
        successful = False
        cmds = command.split(' ')
        if cmds[0] == 'start':
            if len(cmds) > 1 and cmds[1]:
                index = core.get_task_index(cmds[1])
                if index >= 0:
                    task = core.tasks[index]
                    successful = True
                elif cmds[1] not in core:
                    task = Task('', cmds[1])
                    core.tasks.append(task)
                    successful = True
                else:
                    task = None
                    successful = False
            else:
                task = core.tasks[core.current_task_index]
                successful = True

            if successful:
                if now() in core.distribution.content.get_purchased_collection():
                    task.start()
                    core.save()
                    core.current_task_index = core.tasks.index(task)
                else:
                    print('你没有时间做这件事情')
                    successful = False
        elif cmds[0] == 'pause':
            if len(cmds) > 1 and cmds[1]:
                index = core.get_task_index(cmds[1])
                if index >= 0:
                    core.tasks[index].pause()
                    core.save()
                    print('时长：', core.tasks[index].get_past_duration())
                    successful = True
                else:
                    successful = False
            else:
                core.tasks[core.current_task_index].pause()
                core.save()
                print('时长：', core.tasks[core.current_task_index].get_past_duration())
                successful = True
        elif cmds[0] == 'stop':
            if len(cmds) > 1 and cmds[1]:
                index = core.get_task_index(cmds[1])
                if index >= 0:
                    core.tasks[index].end()
                    core.save()
                    successful = True
                else:
                    successful = False
            else:
                core.tasks[core.current_task_index].end()
                core.save()
                successful = True
        elif cmds[0] == 'clear':
            core.tasks.clear()
            core.save()
            successful = True
        elif cmds[0] == 'exit':
            exit(0)
        elif cmds[0] == 'pricechange' and len(cmds) > 2 and cmds[1] and cmds[2]:
            core.prices[cmds[1]] = (core.prices[cmds[1]][0], float(cmds[2]))
            core.save()
            successful = True
        elif cmds[0] == 'purchase':
            if len(cmds) == 1 or not cmds[1]:
                successful = core.purchase_all_tasks()
            elif cmds[1]:
                successful = core.purchase(core.tasks[core.get_task_index(cmds[1])])
            core.save()
        elif cmds[0] == 'buytime':
            if len(cmds) == 1 or not cmds[1]:
                core.purchase_time(timedelta(minutes=20))
                core.save()
                successful = True
            elif len(cmds) == 2 and cmds[1]:
                core.purchase_time(timedelta(minutes=float(cmds[1])))
                core.save()
                successful = True
            elif len(cmds) == 3 and cmds[1] and cmds[2]:
                _start_time = datetime.strptime(cmds[1], '%H:%M')
                start_time = now().replace(hour=_start_time.hour, minute=_start_time.minute, second=0, microsecond=0)
                _end_time = datetime.strptime(cmds[2], '%H:%M')
                if ':' in cmds[1] and ':' in cmds[2]:
                    core.purchase_time(_end_time - _start_time, start=start_time)
                    core.save()
                    successful = True
                elif ':' in cmds[1] and ':' not in cmds[2]:
                    core.purchase_time(timedelta(minutes=float(cmds[2])), start=start_time)
                    core.save()
                    successful = True
                else:
                    successful = False
            else:
                successful = False
        elif cmds[0] == 'buytimestart':
            execute(core, 'buytime ' + ' '.join(cmds[2:]))
            execute(core, 'start ' + cmds[1])
            successful = True
        elif cmds[0] == 'details':
            core.load()
            core.print_details()
            successful = True
        elif cmds[0] == 'prices':
            core.load()
            core.print_prices()
            successful = True
        elif cmds[0] == 'task':
            if len(cmds) > 1 and cmds[1]:
                index = core.get_task_index(cmds[1])
                if index >= 0:
                    task = core.tasks[index]
                    successful = True
                else:
                    task = None
                    successful = False
            else:
                task = core.tasks[core.current_task_index]
                successful = True
            if task is not None:
                task.print()

    #except Exception:
    #    successful = False

        for task in core.tasks:
            if task:
                task.duration.print()

        if successful:
            return '操作成功！'
        else:
            return '操作失败'


def loop(core):
    if isinstance(core, DistrCore):
        while True:
            for task in core.tasks:
                if task.isrunning() and task.duration not in core.distribution.content.get_purchased_collection():
                    task.pause()
                    print('时间耗尽，交易项代码为' + task.code + '的任务已停止计时')
            time.sleep(0.2)


if __name__ == '__main__':
    core = DistrCore(balance_filename='../dcam1/dcam_data/finance/balance.txt'
                     , distribution_filename='../dcam1/dcam_data/distributions/time_collection.txt'
                     , prices_filename='../dcam1/dcam_data/finance/prices.txt')
    core.load()
    core.print_prices()

    thread = Thread(target=loop, args=(core, ))
    thread.start()

    while True:
        inp = input('请输入命令：')
        if inp:
            print(execute(core, inp))
