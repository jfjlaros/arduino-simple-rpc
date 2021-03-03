from os.path import exists

from pytest import mark

from simple_rpc import Interface
from simple_rpc.simple_rpc import _version


class _TestLib(object):
    def test_pre_open(self: object) -> None:
        assert not _interface.is_open()
        assert _interface.methods == {}

    def test_open(self: object) -> None:
        _interface.open()
        assert _interface.is_open()
        assert _interface.methods != {}

    def test_version(self: object) -> None:
        assert _interface._version == _version

    def test_ping(self: object) -> None:
        assert _interface.ping(3) == 3

    def test_type_1(self: object) -> None:
        assert _interface.methods['ping']['return']['typename'] == 'int'

    def test_fmt_1(self: object) -> None:
        assert _interface.methods['ping']['return']['fmt'] == b'B'

    def test_param_1(self: object) -> None:
        assert _interface.methods['ping']['parameters'][0]['typename'] == 'int'

    def test_param_2(self: object) -> None:
        assert _interface.methods['ping']['parameters'][0]['fmt'] == b'B'

    def test_param_3(self: object) -> None:
        assert _interface.methods['ping']['parameters'][0]['name'] == 'data'

    def test_doc_1(self: object) -> None:
        assert _interface.methods['ping']['doc'] == 'Echo a value.'

    def test_doc_2(self: object) -> None:
        assert _interface.methods['ping']['parameters'][0]['doc'] == 'Value.'

    def test_close(self: object) -> None:
        assert _interface.is_open()
        assert _interface.methods != {}
        _interface.close()

    def test_post_close(self: object) -> None:
        assert not _interface.is_open()
        assert _interface.methods == {}


def test_init_serial() -> None:
    global _interface
    _interface = Interface('/dev/ttyACM0', autoconnect=False)


@mark.test_device('serial')
class TestSerial(_TestLib):
    pass


def test_init_wifi() -> None:
    global _interface
    _interface = Interface('socket://192.168.21.53:1025', autoconnect=False)


@mark.test_device('wifi')
class TestWiFi(_TestLib):
    pass


def test_init_bluetooth() -> None:
    global _interface
    _interface = Interface('/dev/rfcomm0', autoconnect=False)


@mark.test_device('bt')
class TestBluetooth(_TestLib):
    pass
