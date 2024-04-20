from typing import List
from xml.etree import ElementTree as ET

from etamodbus.register import RegisterDescription

MIN_REG_ADDR = 1000
class Configuration:
    def __init__(self):
        self._first_reg_addr = MIN_REG_ADDR
        self._last_reg_addr = self._first_reg_addr
        self._registers = {}

    @classmethod
    def from_file(cls, file):
        data = ''
        with open(file, 'r') as f:
            data = f.read()
        root = ET.fromstring(data)
        version = root.attrib['version']
        assert version == '1' # we only support version 1 and have no idea if there are any other versions outside
        cfg = Configuration()
        last_reg_addr = -1
        for r in root.findall(".//register"):
            v = r.find('./variable')
            current_reg_addr = int(r.get('id'))
            last_reg_addr = max(last_reg_addr, current_reg_addr)
            data = {
                "addr":current_reg_addr,
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
            cfg.register(RegisterDescription(**data))
            cfg._last_reg_addr = last_reg_addr
        return cfg

    def __len__(self) -> int:
        return len(self._registers)

    @property
    def first_addr(self):
        return self._first_reg_addr

    @property
    def last_addr(self):
        return self._last_reg_addr

    def register(self, desc: RegisterDescription) -> None:
        if desc.addr in self._registers:
            raise ValueError('Register already registered')
        self._registers[desc.addr] = desc

    def resolve(self, reg_addr) -> RegisterDescription:
        """Resolves the given register's description"""
        return self._registers[reg_addr]

    def startswith(self, uri) -> List[RegisterDescription]:
        for addr in self.items():
            desc = self.resolve(addr)
            if desc.uri.startswith(uri):
                yield desc

    def items(self):
        return iter(self._registers)
