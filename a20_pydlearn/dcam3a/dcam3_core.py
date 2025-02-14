from datetime import datetime, timedelta


now = datetime.now
empty = timedelta()


def get_zero_oclock(days_offset=0):
    return now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_offset)


class TimeSegment:
    def __init__(self, start_time: datetime, end_time: datetime, purpose='', purchased=False):
        self.start = start_time
        self.end = end_time
        self.purpose = purpose
        self.purchased = purchased

    def __contains__(self, time_or_segment):
        if isinstance(time_or_segment, datetime):
            return self.start <= time_or_segment < self.end
        elif isinstance(time_or_segment, TimeSegment):
            return self.start <= time_or_segment.start and time_or_segment.end <= self.end
        return False

    def get_timedelta(self):
        return self.end - self.start

    def __bool__(self):
        return self.get_timedelta() > empty

    def conflicts_with(self, other_segment):
        if isinstance(other_segment, TimeSegment):
            return self.end > other_segment.start and other_segment.end > self.start
        return False

    def __lt__(self, other):
        if isinstance(other, TimeSegment):
            if self.start < other.start:
                return True
            elif self.start == other.start:
                return self.end < other.end
        return False

    def __eq__(self, other):
        return isinstance(other, TimeSegment) and self.start == other.start and self.end == other.end

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __ne__(self, other):
        return not (self == other)

    def compare(self, segment):
        if not isinstance(segment, TimeSegment):
            return None, None
        start1 = min(self.start, segment.start)
        if start1 == self.start:
            return self, segment
        else:
            return segment, self

    def __and__(self, other):
        if isinstance(other, TimeSegment):
            if self in other:
                return self
            elif other in self:
                return other
            frag1, frag2 = self.compare(other)
            if frag1.end <= frag2.start:
                return None
            else:
                return TimeSegment(frag2.start, frag1.end, frag1.purpose)
        return None
    

    def __add__(self, other):
        if isinstance(other, TimeSegment):
            if self in other:
                return other
            elif other in self:
                return self
            frag1, frag2 = self.compare(other)
            if frag1.end < frag2.start:
                return TimeSegment(frag1.start, frag2.end - (frag2.start - frag1.end), frag1.purpose)
            else:
                return TimeSegment(frag1.start, frag2.end, frag1.purpose)
        elif isinstance(other, timedelta):
            return TimeSegment(frag1.start, frag2.end + other, frag1.purpose)
        return None
    
    def copy(self):
        return TimeSegment(self.start, self.end, self.purpose)

    def __str__(self):
        return str(self.start) + ' ~ ' + str(self.end)


def get_segment(start=None, delta=timedelta(minutes=20), purpose=''):
    if not start:
        start = now()
    return TimeSegment(start, start + delta, purpose)


class TimeCollection:
    def __init__(self):
        self.segments = []
        self.pointer = None

    def __bool__(self):
        for segment in self.segments:
            if segment:
                return True
        return False

    def __contains__(self, item):
        if isinstance(item, datetime) or isinstance(item, TimeSegment):
            for segment in self.segments:
                if item in segment:
                    return True
        elif isinstance(item, TimeCollection):
            if not self:
                return False
            for frag in item.segments:
                is_in = False
                for segment in self.segments:
                    if frag in segment:
                        is_in = True
                        break
                if not is_in:
                    return False
            return True
        return False

    def get_duration(self):
        d = timedelta()
        for segment in self.segments:
            d += segment.get_duration()
        return d

    def get_current_segment(self):
        time = now()
        for segment in self.segments:
            if time in segment:
                return segment
        return None

    def __and__(self, other):
        col = TimeCollection()
        if isinstance(other, TimeSegment):
            for segment in self.segments:
                col.segments.append(segment & other)
        elif isinstance(other, TimeCollection):
            for frag in other.segments:
                col.segments.append(self & frag)

        return col

    def conflicts_with(self, segment_or_collection):
        if isinstance(segment_or_collection, TimeSegment):
            for segment in self.segments:
                if segment_or_collection & segment:
                    return segment, segment_or_collection
        elif isinstance(segment_or_collection, TimeCollection):
            for segment in self.segments:
                conflicts = segment_or_collection.conflicts_with(segment)
                if conflicts:
                    return conflicts
        return None

    def __or__(self, segment_or_collection):
        collection = TimeCollection()
        if isinstance(segment_or_collection, TimeSegment):
            for seg in self.segments:
                if seg.end < segment_or_collection:
                    collection.segments.append(seg)
                    collection.segments.append(segment_or_collection)
                else:
                    s1 = TimeSegment(seg.start, segment_or_collection.end)
                    collection.segments.append(s1)

                collection.segments.append(seg)
            sum_ = segment_or_collection.copy()
            sum_list = []
            for segment in self.segments:
                if sum_ & segment:
                    sum_ |= segment
                elif isinstance(sum_ | segment, list):
                    sum_list.append(segment)
            sum_list.append(sum_)
            collection.segments = sum_list
        elif isinstance(segment_or_collection, TimeCollection):
            collection
        return collection

    def clear(self):
        self.segments.clear()

    def get_segments_between_segsments(self, segment1: TimeSegment, segment2: TimeSegment):
        between = []
        for segment in self.segments:
            if segment1.end <= segment.start and segment.end <= segment2.start:
                between.append(segment)
        return between
    
    def get_segments_between(self, t1: datetime, t2: datetime):
        between = []
        for segment in self.segments:
            if t1 <= segment.start and segment.end <= t2:
                between.append(segment)
        return between

    # def get_purchased_collection(self):
    #     col = TimeCollection()
    #     for segment in self.segments:
    #         if segment.purchased:
    #             col += segment
    #     return col

    # def get_purchased_timedelta(self):
    #     d = timedelta()
    #     for segment in self.segments:
    #         if not segment.purchased:
    #             continue
    #         d += segment.get_timedelta()
    #     return d

    # def get_used_duration(self):
    #     d = timedelta()
    #     now_ = now()
    #     for segment in self.segments:
    #         if not segment.enabled or not segment.purchased:
    #             continue
    #         if now_ in segment:
    #             d += now_ - segment.start
    #         elif segment.end < now_:
    #             d += segment.get_duration()
    #     if self.pointer:
    #         d += now_ - self.pointer
    #     return d

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
        self.time_collection = TimeCollection()
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


class TimeTrack:
    def __init__(self, name: str, capacity=get_collection()):
        self.name = name
        self.content = TimeCollection()
        self.capacity = capacity

    def __contains__(self, item):
        if isinstance(item, Task):
            return item.duration in self.content
        elif isinstance(item, TimeSegment) or isinstance(item, TimeCollection):
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
