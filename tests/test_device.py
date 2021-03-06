from os.path import exists

from pytest import mark

from simple_rpc import Interface
from simple_rpc.simple_rpc import _version


_device = '/dev/ttyACM0'
if exists(_device):
    _interface = Interface(_device, autoconnect=False)


@mark.skipif(not exists(_device), reason='device not connected')
class TestLib(object):
    def test_pre_open(self):
        assert not _interface.is_open()
        assert _interface.methods == {}

    def test_open(self):
        _interface.open()
        assert _interface.is_open()
        assert _interface.methods != {}

    def test_version(self):
        assert _interface._version == _version

    def test_ping(self):
        assert _interface.ping(3) == 3

    def test_type_1(self):
        assert _interface.methods['ping']['return']['typename'] == 'int'

    def test_fmt_1(self):
        assert _interface.methods['ping']['return']['fmt'] == b'B'

    def test_param_1(self):
        assert _interface.methods['ping']['parameters'][0]['typename'] == 'int'

    def test_param_2(self):
        assert _interface.methods['ping']['parameters'][0]['fmt'] == b'B'

    def test_param_3(self):
        assert _interface.methods['ping']['parameters'][0]['name'] == 'data'

    def test_doc_1(self):
        assert _interface.methods['ping']['doc'] == 'Echo a value.'

    def test_doc_2(self):
        assert _interface.methods['ping']['parameters'][0]['doc'] == 'Value.'

    def test_close(self):
        assert _interface.is_open()
        assert _interface.methods != {}
        _interface.close()

    def test_post_close(self):
        assert not _interface.is_open()
        assert _interface.methods == {}
