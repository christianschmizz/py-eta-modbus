from etamodbus.register import RegisterDescription
import pytest


def test_resolve(cfg):
    assert len(list(cfg.items())) == 30
    assert cfg.resolve(1010) == RegisterDescription(addr=1010, name='GM-C 0: HK WH - Vorlauf', node_id='120', fub_id='10102', fkt_id='0', io_id='0', var_id='12241', scale=10, unit='°C', min='', max='', default='')
    assert cfg.resolve(1050) == RegisterDescription(addr=1050, name='PE-C 0: Kessel - Kessel', node_id='40', fub_id='10021', fkt_id='0', io_id='0', var_id='12000', scale=1, unit='', min='', max='', default='')

def test_startswith(cfg):
    assert len(list(cfg.startswith('40/'))) == 16
    assert len(list(cfg.startswith('40/10021'))) == 13
    assert len(list(cfg.startswith('40/10021/0/0'))) == 11
    assert len(list(cfg.startswith('40/10021/0/0/12'))) == 11
    assert len(list(cfg.startswith('120/'))) == 14
