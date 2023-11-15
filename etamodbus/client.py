from pyModbusTCP.client import ModbusClient


class ETAModbusClient:
    def __init__(self, host, config):
        self._config = config
        self._client = ModbusClient(host, port=502, unit_id=1, auto_open=True)

    def read(self, reg_addr, length=2):
        if reg_addr % 2 != 0:
            raise ValueError("invalid reg, has to be even")
        if length % 2 != 0:
            raise ValueError("invalid length, has to be even")
        return self._client.read_holding_registers(reg_addr, length)

    def read_all(self):
        num_registers = len(self._config) * 2
        reg_vals = self.read(self._config.first_addr, num_registers)
        i = 0
        for reg_addr in range(self._config.first_addr, self._config.last_addr, 2):
            desc = self._config.resolve(reg_addr)
            val = desc.value([reg_vals[i], reg_vals[i+1]])
            yield desc, val
            i += 2
