#!/usr/bin/env python
import os
import time

# pip install pymodbus
# https://forum.iobroker.net/assets/uploads/files/1571694770504-etatouch_modbustcp.pdf
from etamodbus import ETAModbusClient, Configuration

def outside_temp():
    cfg = Configuration.from_file(os.path.join(os.path.dirname(__file__), '..', 'modbusTcpService.xml'))
    conn = ETAModbusClient(os.getenv('ETA_ADDRESS', '192.168.1.252'), cfg)
    descs = list(cfg.startswith('40/10241/0/0/12197'))
    desc = next(iter(descs), None)
    if desc:
        vals = conn.read(desc.addr)
        print('[{}] {}: {} -> {} (uri: {}) {}'.format(desc.fub_name, desc.param_name, vals, desc.value(vals), desc.uri, desc.addr))

if __name__ == '__main__':
    outside_temp()