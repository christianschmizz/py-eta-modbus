import collections

from etamodbus.status import status


class SimpleNumericValue(collections.namedtuple('SimpleNumeric', 'val unit scale')):
    @classmethod
    def from_register(cls, r, unit, scale=1):
        if len(r) != 2:
            raise ValueError("two components needed")
        result = (r[0] << 16) | r[1]
        return cls(val=result, unit=unit, scale=scale)

    def __str__(self):
        return '{:.2f} {}'.format(self.value, self.unit)

    @property
    def value(self):
        return self.val/self.scale


class TextValue(collections.namedtuple('Text', 'code desc')):
    @classmethod
    def from_register(cls, r):
        code = int(r[1])
        return cls(code=code, desc=status[code])

    def __str__(self):
        return '{} ({})'.format(self.desc, self.code)

    @property
    def value(self):
        return self.code


class TimeSlotValue(collections.namedtuple('TimeSlot', 'temperature begin end')):
    @classmethod
    def from_register(cls, r):
        if len(r) != 2:
            raise ValueError("two components needed")
        temp = r[0]
        end = r[1] & 0xff
        begin = r[1] >> 8 & 0xff
        return cls(temp=temp, begin=begin, end=end)
