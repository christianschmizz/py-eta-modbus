#!/usr/bin/env python
import os
import time
from etamodbus import ETAModbusClient, Configuration

def main():
    cfg = Configuration.from_file('../modbusTcpService.xml')
    conn = ETAModbusClient(os.getenv('ETA_ADDRESS'), cfg)
    while True:
        for desc, val in conn.read_all():
            print('[{}] {}: {} (uri: {}) {}'.format(desc.fub_name, desc.param_name, val, desc.uri, desc.addr))
        time.sleep(15)

if __name__ == '__main__':
    main()
