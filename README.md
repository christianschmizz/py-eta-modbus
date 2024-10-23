# ETA Modbus Client (Python)

This package helps to read any data from your modbus/tcp enabled ETA heating system.

It's been mainly written for personal purposes to monitor our ETA heating system and 
analyse the impact of various parameters on the fuel consumption.

## Using this project

You can find some examples on how to use this packages at the `examples` directory
within this repository.

To ease access to your heating system I recommend exporting your current modbus 
configuration to a USB stick (aka `modbusTcpService.xml`) at your heating.

**Please note:** Connecting to you ETA heating system requires you to have enabled
                 the TCP web-services at the heating's control-panel beforehand. 

## Further information

- [ETA Modbus protocol](https://forum.iobroker.net/assets/uploads/files/1571694770504-etatouch_modbustcp.pdf)
- [ETA Modbus @ Lox](https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1542816341/ETA+Holzvergaser)
