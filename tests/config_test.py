from unittest import TestCase

import etamodbus

class TestConfiguration(TestCase):
    def test_is_string(self):
        cfg = etamodbus.Configuration.from_file('../../modbusTcpService.xml')
