from os.path import exists

from pytest import mark

from simple_rpc import Interface
from simple_rpc.simple_rpc import _version

from conf import _devices


class _TestDevice(object):
    def test_pre_open(self: object) -> None:
        assert not self._interface.is_open()
        assert self._interface.methods == {}

    def test_open(self: object) -> None:
        self._interface.open()
        assert self._interface.is_open()
        assert self._interface.methods != {}

    def test_version(self: object) -> None:
        assert self._interface._version == _version

    def test_ping(self: object) -> None:
        assert self._interface.ping(3) == 3

    def test_type_1(self: object) -> None:
        assert self._interface.methods['ping']['return']['typename'] == 'int'

    def test_fmt_1(self: object) -> None:
        assert self._interface.methods['ping']['return']['fmt'] == b'B'

    def test_param_1(self: object) -> None:
        assert (
            self._interface.methods['ping']['parameters'][0]['typename'] ==
            'int')

    def test_param_2(self: object) -> None:
        assert self._interface.methods['ping']['parameters'][0]['fmt'] == b'B'

    def test_param_3(self: object) -> None:
        assert (
            self._interface.methods['ping']['parameters'][0]['name'] == 'data')

    def test_doc_1(self: object) -> None:
        assert self._interface.methods['ping']['doc'] == 'Echo a value.'

    def test_doc_2(self: object) -> None:
        assert (
            self._interface.methods['ping']['parameters'][0]['doc'] ==
            'Value.')

    def test_close(self: object) -> None:
        assert self._interface.is_open()
        assert self._interface.methods != {}
        self._interface.close()

    def test_post_close(self: object) -> None:
        assert not self._interface.is_open()
        assert self._interface.methods == {}


@mark.test_device('serial')
class TestSerial(_TestDevice):
    _interface = Interface(_devices['serial'], autoconnect=False)


@mark.test_device('wifi')
class TestWiFi(_TestDevice):
    _interface = Interface(_devices['wifi'], autoconnect=False)


@mark.test_device('bt')
class TestBluetooth(_TestDevice):
    _interface = Interface(_devices['bt'], autoconnect=False)
