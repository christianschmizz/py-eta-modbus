from pyModbusTCP.client import ModbusClient
import logging

class ReadingRegistersFailedException(Exception):
    pass

class ETAModbusClient:
    def __init__(self, host, config):
        self._config = config
        self._client = ModbusClient(host, port=502, unit_id=1, auto_open=True)

    def read(self, reg_addr, length=2):
        """
        Reads registers
        :param int reg_addr: Register's address to start reading
        :param int length: Number of register to read
        :return: List of registers data
        """
        if reg_addr % 2 != 0:
            raise ValueError("invalid reg, has to be even")
        if length % 2 != 0:
            raise ValueError("invalid length, has to be even")
        return self._client.read_holding_registers(reg_addr, length)

    def read_all(self):
        """
        Reads all registers at once as one big chunk. Registers
        should be sequentially. "holes" in the address range might
        lead to errors.
        """
        num_registers = len(self._config) * 2
        reg_vals = self.read(self._config.first_addr, num_registers)
        if reg_vals is None:
            raise ReadingRegistersFailedException(f'failed to read registers from {self._config.first_addr} ({num_registers})')
        i = 0
        for reg_addr in range(self._config.first_addr, self._config.last_addr + 2, 2):
            desc = self._config.resolve(reg_addr)
            val = desc.value(reg_vals[i:i+2])
            yield desc, val
            i += 2
