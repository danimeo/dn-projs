from datetime import datetime, timedelta

now = datetime.now
empty = timedelta()


class TimeSegment:
    def __init__(self, start_time: datetime, end_time: datetime, purpose=''):
        self.start = start_time
        self.end = end_time
        self.purpose = purpose

    def __contains__(self, time_or_segment):
        if isinstance(time_or_segment, datetime):
            return self.start <= time_or_segment < self.end
        elif isinstance(time_or_segment, TimeSegment):
            return self.start <= time_or_segment.start and time_or_segment.end <= self.end
        return False

    def get_duration(self):
        return self.end - self.start

    def __bool__(self):
        return self.get_duration() > empty

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

    def __mul__(self, other):
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
                return [frag1, frag2]
            else:
                return TimeSegment(frag1.start, frag2.end, frag1.purpose)
        return None

    def copy(self):
        return TimeSegment(self.start, self.end, self.purpose)

    def __str__(self):
        return str(self.start) + ' ~ ' + str(self.end)