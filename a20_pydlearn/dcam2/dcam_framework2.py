from datetime import datetime, timedelta

now = datetime.now
empty = timedelta()


def get_zero_oclock(days_offset=0):
    return now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_offset)


class TimeFragment:
    def __init__(self, start_time: datetime, end_time: datetime, purpose='', enabled=True, purchased=False):
        self.start = start_time
        self.end = end_time
        self.purpose = purpose
        self.enabled = enabled
        self.purchased = purchased

    def __contains__(self, time_or_fragment):
        if isinstance(time_or_fragment, datetime):
            return self.start <= time_or_fragment < self.end
        elif isinstance(time_or_fragment, TimeFragment):
            return self.start <= time_or_fragment.start and time_or_fragment.end <= self.end
        return False

    def get_duration(self):
        return self.end - self.start

    def __bool__(self):
        return self.get_duration() > empty

    def conflicts_with(self, other_fragment):
        if isinstance(other_fragment, TimeFragment):
            return self.end > other_fragment.start and other_fragment.end > self.start
        return False

    def __lt__(self, other):
        if isinstance(other, TimeFragment):
            if self.start < other.start:
                return True
            elif self.start == other.start:
                return self.end < other.end
        return False

    def __eq__(self, other):
        return isinstance(other, TimeFragment) and self.start == other.start and self.end == other.end

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __ne__(self, other):
        return not (self == other)

    def compare(self, fragment):
        if not isinstance(fragment, TimeFragment):
            return None, None
        start1 = min(self.start, fragment.start)
        if start1 == self.start:
            return self, fragment
        else:
            return fragment, self

    def __mul__(self, other):
        if isinstance(other, TimeFragment):
            if self in other:
                return self
            elif other in self:
                return other
            frag1, frag2 = self.compare(other)
            if frag1.end <= frag2.start:
                return None
            else:
                return TimeFragment(frag2.start, frag1.end, frag1.purpose
                                , frag1.enabled and frag2.enabled
                                , frag1.purchased or frag2.purchased)
        return None

    def __add__(self, other):
        if isinstance(other, TimeFragment):
            if self in other:
                return other
            elif other in self:
                return self
            frag1, frag2 = self.compare(other)
            if frag1.end < frag2.start:
                return [frag1, frag2]
            else:
                return TimeFragment(frag1.start, frag2.end, frag1.purpose
                                , frag1.enabled and frag2.enabled
                                , frag1.purchased and frag2.purchased)
        return None

    def copy(self):
        return TimeFragment(self.start, self.end, self.purpose, self.enabled, self.purchased)

    def __str__(self):
        return str(self.start) + ' ~ ' + str(self.end) + ', purc=' + str(self.purchased)


def get_fragment(start=None, delta=timedelta(minutes=20), purpose='', enabled=True, purchased=False):
    if not start:
        start = now()
    return TimeFragment(start, start + delta, purpose, enabled, purchased)


class TimeCollection:
    def __init__(self):
        self.fragments = []
        self.pointer = None

    def __bool__(self):
        for fragment in self.fragments:
            if fragment:
                return True
        return False

    def __contains__(self, item):
        if isinstance(item, datetime) or isinstance(item, TimeFragment):
            for fragment in self.fragments:
                if item in fragment:
                    return True
        elif isinstance(item, TimeCollection):
            if not self:
                return False
            for frag in item.fragments:
                is_in = False
                for fragment in self.fragments:
                    if frag in fragment:
                        is_in = True
                        break
                if not is_in:
                    return False
            return True
        return False

    def get_duration(self):
        d = timedelta()
        for fragment in self.fragments:
            d += fragment.get_duration()
        return d

    def get_current_fragment(self):
        time = now()
        for fragment in self.fragments:
            if time in fragment:
                return fragment
        return None

    def __mul__(self, other):
        col = TimeCollection()
        if isinstance(other, TimeFragment):
            for fragment in self.fragments:
                col.fragments.append(fragment * other)
        elif isinstance(other, TimeCollection):
            for frag in other.fragments:
                col.fragments.append(self * frag)
        if col:
            return col
        else:
            return None

    def conflicts_with(self, fragment_or_collection):
        if isinstance(fragment_or_collection, TimeFragment):
            for fragment in self.fragments:
                if fragment_or_collection * fragment:
                    return fragment, fragment_or_collection
        elif isinstance(fragment_or_collection, TimeCollection):
            for fragment in self.fragments:
                conflicts = fragment_or_collection.conflicts_with(fragment)
                if conflicts:
                    return conflicts
        return None

    def add(self, fragment_or_collection):
        if isinstance(fragment_or_collection, TimeFragment):
            sum_ = fragment_or_collection.copy()
            sum_list = []
            for fragment in self.fragments:
                if sum_ * fragment:
                    sum_ += fragment
                elif isinstance(sum_ + fragment, list):
                    sum_list.append(fragment)
            sum_list.append(sum_)
            self.fragments.clear()
            self.fragments.extend(sum_list)
        elif isinstance(fragment_or_collection, TimeCollection):
            for fragment in fragment_or_collection.fragments:
                self.add(fragment)

    def clear(self):
        self.fragments.clear()

    def get_fragments_between(self, fragment1: TimeFragment, fragment2: TimeFragment):
        between = []
        for fragment in self.fragments:
            if fragment1.end <= fragment.start and fragment.end <= fragment2.start:
                between.append(fragment)
        return between

    def get_purchased_collection(self):
        col = TimeCollection()
        for fragment in self.fragments:
            if fragment.purchased:
                col.add(fragment)
        return col

    def get_purchased_duration(self):
        d = timedelta()
        for fragment in self.fragments:
            if not fragment.purchased:
                continue
            d += fragment.get_duration()
        return d

    def get_used_duration(self):
        d = timedelta()
        now_ = now()
        for fragment in self.fragments:
            if not fragment.enabled or not fragment.purchased:
                continue
            if now_ in fragment:
                d += now_ - fragment.start
            elif fragment.end < now_:
                d += fragment.get_duration()
        if self.pointer:
            d += now_ - self.pointer
        return d

    def print(self):
        if not self:
            print('Collection is empty.')
            return
        items = []
        for fragment in self.fragments:
            items.append((fragment.start, 0))
            items.append((fragment.end, 1))
        sorted_items = sorted(items)
        print('Collection begins:')
        for sorted_item in sorted_items:
            if not sorted_item[1]:
                flag = 'START'
            else:
                flag = 'END'
            print('  ' + flag + ':' + str(sorted_item[0]))
        print('Collection ends.')


def get_collection(start=get_zero_oclock(), delta=timedelta(days=1), purpose='', enabled=True, purchased=False):
    collection = TimeCollection()
    collection.fragments.append(get_fragment(start, delta, purpose, enabled, purchased))
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
        self.duration = TimeCollection()
        self.full_duration = full_duration

    def get_past_duration(self):
        return self.duration.get_used_duration()

    def __bool__(self):
        if self.duration.get_used_duration() > empty:
            return bool(self.duration)
        return False

    def start(self):
        if self.full_duration <= self.get_past_duration():
            return
        now_ = now()
        if not self.duration.pointer:
            self.duration.pointer = now_

    def pause(self):
        if self.duration.pointer:
            frag = TimeFragment(self.duration.pointer, now(), self.code, purchased=True)
            self.duration.add(frag)
            self.duration.pointer = None

    def stop(self):
        self.pause()
        self.duration.clear()
        self.duration.pointer = None

    def isrunning(self):
        return self.duration.pointer is not None

    def print(self):
        print(self.code + ' ' + self.name)
        fragments = sorted(self.duration.fragments)
        for fragment in fragments:
            print('  [' + str(fragment) + ']')
        if self.duration.pointer:
            print('  [' + str(TimeFragment(self.duration.pointer, now(), self.code, purchased=True)) + ']')
        print('[' + timedelta_to_str(self.get_past_duration()) + ' / ' + timedelta_to_str(self.full_duration) + ']')


class TimeContainer:
    def __init__(self, capacity=get_collection()):
        self.content = TimeCollection()
        self.capacity = capacity

    def __contains__(self, item):
        if isinstance(item, Task):
            return item.duration in self.content
        elif isinstance(item, TimeFragment) or isinstance(item, TimeCollection):
            return item in self.content
        return False

    def add(self, item):
        cont = TimeCollection()
        cont.fragments = self.content.fragments.copy()
        if isinstance(item, Task):
            cont.add(item.duration)
            if cont.get_duration() <= self.capacity.get_duration():
                self.content.add(item.duration)
        elif isinstance(item, TimeFragment) or isinstance(item, TimeCollection):
            cont.add(item)
            if cont.get_duration() <= self.capacity.get_duration():
                self.content.add(item)

    def load(self, content: str):
        self.content.clear()

        lines = content.split('\n')
        for line in lines:
            if not line:
                continue
            attrs = line.split(',')
            start_str, end_str = attrs[0], attrs[1]
            if '.' in start_str:
                start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S.%f')
            else:
                start = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
            if '.' in end_str:
                end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S.%f')
            else:
                end = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
            if attrs[3] == 'True':
                purchased = True
            else:
                purchased = False
            self.content.add(TimeFragment(start, end, purpose=attrs[2], purchased=purchased))

        zero = get_zero_oclock()
        for i, fragment in enumerate(self.content.fragments):
            if fragment.start < zero or fragment.end < zero:
                self.content.clear()
                break

    def text(self):
        output = ''
        for fragment in self.content.fragments:
            output += str(fragment.start) + ',' + str(fragment.end) + ',' + fragment.purpose + ',' + str(
                fragment.purchased) + '\n'
        return output