#!/usr/bin/env python


# pip install pymodbus
# https://forum.iobroker.net/assets/uploads/files/1571694770504-etatouch_modbustcp.pdf
from pyModbusTCP.client import ModbusClient
import time
import collections

class SimpleNumericValue(collections.namedtuple('SimpleNumeric', 'val scale')):
    @classmethod
    def fromRegister(cls, r, scale=1):
        if len(r) != 2:
            raise ValueError("two components needed")
        result = (r[0] << 16) | r[1]
        return cls(val=result, scale=scale)

    def __str__(self):
        return '{:.2f}'.format(self.val/self.scale)

class TextValue:
    pass

class TimeSlotValue(collections.namedtuple('TimeSlot', 'temperature begin end')):
    @classmethod
    def fromRegister(cls, r):
        if len(r) != 2:
            raise ValueError("two components needed")
        temp = r[0]
        end = r[1] & 0xff
        begin = r[1] >> 8 & 0xff
        return cls(temp=temp, begin=begin, end=end)

import xml.etree.ElementTree as ET
import re

snake = lambda name: re.sub('((?!^)(?<!_)[A-Z][a-z]+|(?<=[a-z0-9])[A-Z])', r'_\1', name).lower()

class Configuration:
    def __init__(self):
        self._registers = []

    @classmethod
    def loadFromFile(cls, file):
        data = ''
        with open(file, 'r') as f:
            data = f.read()
        root = ET.fromstring(data)
        print(root.attrib['version'])
        version = root.attrib['version']
        if version != '1':
            raise ValueError('unsupported version {}'.format(version))
        cfg = Configuration()
        for r in root.findall(".//register"):
            v = r.find('./variable')
            data = {
                "reg_id":int(r.get('id')),
                "name":v.get('name'),
                "node_id":v.get('nodeId'),
                "fub_id":v.get('fubId'),
                "fkt_id":v.get('fktId'),
                "io_id":v.get('ioId'),
                "var_id":v.get('varId'),
                "scale":int(v.get('scale')),
                "unit":v.get('unit'),
                "min":v.get('min'),
                "max":v.get('max'),
                "default":v.get('def')
            }
            cfg.register(Register(**data))
        return cfg

    def register(self, var):
        self._registers.append(var)
    
    def items(self):
        return iter(self._registers)



class Register(collections.namedtuple('Register', 'reg_id name node_id fub_id fkt_id io_id var_id scale unit min max default')):
    pass

class ETAHeating:
    def __init__(self, host, config):
        self._config = config
        self._client = ModbusClient(host, port=502, unit_id=1, auto_open=True)

    def read(self, reg, length=2):
        if reg % 2 != 0:
            raise ValueError("invalid reg, has to be even")
        if length % 2 != 0:
            raise ValueError("invalid length, has to be even")

        return self._client.read_holding_registers(reg, length)

    def read_numeric(self, reg, scale=1):
        r = self.read(reg)
        return SimpleNumericValue.fromRegister(r, 10)
    
    def fetch(self):
        val = self.read(1000, 28)
#        for v in self._config.items():
#            print(v)
        print(val)



def main():
    cfg = Configuration.loadFromFile('modbusTcpService.xml')
    eta = ETAHeating("192.168.1.252", cfg)
    eta.fetch()

if __name__ == '__main__':
    main()
