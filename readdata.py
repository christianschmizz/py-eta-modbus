#!/usr/bin/env python3


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
class Configuration:
    @classmethod
    def loadFromFile(cls, file):
        data = ''
        with open(file, 'r') as f:
            data = f.read()
        tree = ET.fromstring(data)
        root = tree.getroot()
        print(root.attrib['version'])
        version = root.attrib['version']
        if version != '1.0':
            raise ValueError('unsupported version')
        cfg = Configuration()
        for v in root.findall(".//variable"):
            var = Variable(v.attrib['name'])
            print(var)
            cfg.register(v.parent.get('id'))

    def register(self, var):
        self.variables.append(var)


class Variable(collections.namedtuple('Var', 'reg_id name node_id fub_id fkt_id io_id var_id scale unit min max')):
    pass

class ETAHeating:
    def __init__(self, host, config):
        self.config = config
        self.client = ModbusClient(host, port=502, unit_id=1, auto_open=True)

    def read(self, reg, length=2):
        if reg % 2 != 0:
            raise ValueError("invalid reg, has to be even")
        if length % 2 != 0:
            raise ValueError("invalid length, has to be even")

        return self.client.read_holding_registers(reg, length)

    def read_numeric(self, reg, scale=1):
        r = self.read(reg)
        return SimpleNumericValue.fromRegister(r, 10)



def main():
    cfg = Configuration.loadFromFile('config.xml')
    eta = ETAHeating("192.168.1.252", cfg)
    # print(eta.read_numeric(1000, 10))
    # print(eta.read_numeric(1002, 10))
    # print(eta.read_numeric(1004, 10))
    # print(eta.read_numeric(1006, 10))
    # print(eta.read_numeric(1008, 10))
    return
    while True:
        #print(c.read_input_registers(1000, 2))

        # read 10 registers at address 0, store result in regs list
        regs_l = c.read_holding_registers(1000, 10)

        # if success display registers
        if regs_l:
            print('reg ad #0 to 9: %s' % regs_l)
        else:
            print('unable to read registers')

        # sleep 2s before next polling
        time.sleep(2)

if __name__ == '__main__':
    main()
