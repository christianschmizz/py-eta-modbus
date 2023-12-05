from etamodbus import Configuration
import pytest


@pytest.fixture
def cfg():
    return Configuration.from_file('../modbusTcpService.xml')