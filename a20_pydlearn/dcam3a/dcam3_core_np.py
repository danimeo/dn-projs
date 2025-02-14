
from datetime import datetime, timedelta
import numpy as np


now = datetime.now
empty = timedelta()


def get_zero_oclock(days_offset=0):
    return now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_offset)



def track_to_str(collection: TimeCollection):
    if not collection:
        return 'Collection is empty.'
        
    s1 = ''
    items = []
    for segment in collection.segments:
        items.append((segment.start, 0))
        items.append((segment.end, 1))
    sorted_items = sorted(items)
    s1 += 'Collection begins:\n'
    for sorted_item in sorted_items:
        if not sorted_item[1]:
            flag = 'START'
        else:
            flag = 'END'
        s1 += '  {}:{}\n'.format(flag, str(sorted_item[0]))
    s1 += 'Collection ends.\n'
    return s1


def get_collection(start=get_zero_oclock(), delta=timedelta(days=1), purpose=''):
    collection = TimeCollection()
    collection.segments.append(get_segment(start, delta, purpose))
    return collection


def timedelta_to_str(td: timedelta, mode=''):
    if mode == 'by_minutes':
        return str(td.total_seconds() / 60) + ' min'
    elif mode == 'by_hours':
        return str(td.total_seconds() / 3600) + ' h'
    elif mode == 'by_seconds':
        return str(td.total_seconds()) + ' s'
    else:
        if td.days:
            days = str(td.days) + 'd '
        else:
            days = ''

        hours_num = int(td.total_seconds() // 3600 % 24)
        if hours_num:
            hours = str(hours_num) + 'h '
        else:
            hours = ''

        minutes_num = int(td.total_seconds() // 60 % 60)
        if minutes_num:
            minutes = str(minutes_num) + 'min '
        else:
            minutes = ''

        seconds_num = int(td.total_seconds() % 60)
        if seconds_num:
            seconds = str(seconds_num) + 's '
        else:
            if td.days or hours_num or minutes_num:
                seconds = ''
            else:
                seconds = '0s'
        time_str = days + hours + minutes + seconds
        if time_str.endswith(' '):
            time_str = time_str[:-1]
        return time_str


class Task:
    def __init__(self, name: str, code: str, full_duration=timedelta(hours=5)):
        self.name = name
        self.code = code
        self.timings = TimeCollection()
        self.full_duration = full_duration

    def get_past_time_timedelta(self):
        ## to do
        return self.time_collection.get_past_time_collection()

    def __bool__(self):
        if self.time_collection.get_past_time_collection() > empty:
            return bool(self.time_collection)
        return False

    def start(self):
        if self.full_time_collection <= self.get_past_time_collection():
            return
        now_ = now()
        if not self.time_collection.pointer:
            self.time_collection.pointer = now_

    def pause(self):
        if self.time_collection.pointer:
            frag = TimeSegment(self.time_collection.pointer, now(), self.code)
            self.time_collection |= frag
            self.time_collection.pointer = None

    def stop(self):
        self.pause()
        self.time_collection.clear()
        self.time_collection.pointer = None

    def isrunning(self):
        return self.time_collection.pointer is not None

def task_to_str(task: Task):
    s = ''
    s += '{} {}\n'.format(task.code, task.name)
    segments = sorted(task.duration.segments)
    for segment in segments:
        s += '  [{}]\n'.format(str(segment))
    if task.duration.pointer:
        s += '  [{}]\n'.format(str(TimeSegment(task.duration.pointer, now(), task.code)))
    
    s += '{} {}\n'.format(timedelta_to_str(task.get_past_timedelta()), timedelta_to_str(task.full_duration))
    # print('  [' + str(TimeSegment(task.time_collection.pointer, now(), task.code)) + ']')
    # print('[' + timedelta_to_str(task.get_past_timedelta()) + ' / ' + timedelta_to_str(task.full_duration) + ']')
    return s


### Make a good temporal/sequential operation processing framework!

class TimeContainer:
    def __init__(self, name: str, capacity=get_collection()):
        self.name = name
        self.timings = np.zeros((), dtype=np.float32)
        self.event_type_indices = np.zeros((), dtype=np.uint8)
        self.capacity = capacity

    def __contains__(self, item):
        if isinstance(item, Task):  # if the timing of a task is in the container
            return item.duration in self.content
        elif isinstance(item, np.array):
            pass
        elif isinstance(item, tuple):
            return item in self.content
        return False

    def __or__(self, item):
        track = TimeTrack()
        track.content.segments = self.content.segments.copy()
        if isinstance(item, Task):
                track.content |= item.duration
        elif isinstance(item, TimeSegment) or isinstance(item, TimeCollection):
                track.content |= item
        elif isinstance(item, TimeTrack):
            track |= item.content
        return track


    def load(self, content: str):
        self.content.clear()

        lines = content.split('\n')
        for line in lines:
            if not line:
                continue
            attrs = line.split(',')
            start = datetime.strptime(attrs[0], '%Y-%m-%d %H:%M:%S.%f')
            end = datetime.strptime(attrs[1], '%Y-%m-%d %H:%M:%S.%f')
            self.content.add(TimeSegment(start, end, purpose=attrs[2]))

        zero = get_zero_oclock()
        for i, segment in enumerate(self.content.segments):
            if segment.start < zero or segment.end < zero:
                self.content.clear()
                break

    def text(self):
        output = ''
        for segment in self.content.segments:
            output += str(segment.start) + ',' + str(segment.end) + ',' + segment.purpose + '\n'
        return output

    def utilization_ratio(self, purpose=''):
        if purpose:
            pass
        else:
            return self.content.get_duration('used') / self.capacity.get_duration()



base_timing = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)




def add_timing(timing_arr: np.ndarray, timing: datetime, duration: timedelta, event: int):
    pass


def intersection_of(timing_arr1: np.ndarray, timing_arr2: np.ndarray):
    pass

def union_of(timing_arr1: np.ndarray, timing_arr2: np.ndarray):
    pass

def difference_of(timing_arr1: np.ndarray, timing_arr2: np.ndarray):
    pass



def datetimes_to_timing_arr(dts: list[datetime]):
    timings = []
    for dt in dts:
        timings.append(np.array([(dt - base_timing).total_seconds()])
    return np.array(timings).reshape((1, 1, 1))
