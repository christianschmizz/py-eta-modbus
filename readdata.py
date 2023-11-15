#!/usr/bin/env python
import time

# pip install pymodbus
# https://forum.iobroker.net/assets/uploads/files/1571694770504-etatouch_modbustcp.pdf
from etamodbus import ETAModbusClient, Configuration

def main():
    cfg = Configuration.from_file('modbusTcpService.xml')
    conn = ETAModbusClient("192.168.1.252", cfg)
    while True:
        for desc, val in conn.read_all():
            print('[{}] {}: {} (uri: {})'.format(desc.fub_name, desc.param_name, val, desc.uri))
        time.sleep(5)

if __name__ == '__main__':
    main()
