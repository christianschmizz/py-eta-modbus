import collections
import re
from functools import lru_cache

from etamodbus.values import SimpleNumericValue, TextValue

class Register(collections.namedtuple('Register', 'id high low')):
    pass

class RegisterDescription(collections.namedtuple('RegisterDescription', 'addr name node_id fub_id fkt_id io_id var_id scale unit min max default')):
    def value(self, reg_vals):
        if '12153' == self.var_id:
            return SimpleNumericValue.from_register(reg_vals, unit="h", scale=3600)
        elif self.is_state:
            return TextValue.from_register(reg_vals)
        else:
            return SimpleNumericValue.from_register(reg_vals, unit=self.unit, scale=self.scale)

    @lru_cache(maxsize=None)
    def x(self):
        return re.search('^(?P<node>[^:]+):(?P<fub>[^-]+)\-(?P<param>[^-]+)(-([^-]+))?$', self.name)

    @property
    def fub_name(self):
        match = self.x()
        if match:
            return match.group('fub').strip()

    @property
    def param_name(self):
        match = self.x()
        if match:
            return match.group('param').strip()

    @property
    def uri(self):
        return '/'.join([self.node_id, self.fub_id, self.fkt_id, self.io_id, self.var_id])

    @property
    def is_state(self):
        return not self.unit and (('Zustand' in self.name or 'Anforderung' in self.name) or self.var_id == '12000')