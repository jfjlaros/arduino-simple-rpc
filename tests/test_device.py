from io import StringIO

from pytest import mark
from yaml import FullLoader, load

from simple_rpc import Interface
from simple_rpc.simple_rpc import _version

from .conf import _devices, _interface


class _TestDevice(object):
    def test_pre_open(self: object) -> None:
        assert not self._interface.is_open()
        assert self._interface.device['methods'] == {}

    def test_open(self: object) -> None:
        self._interface.open()
        assert self._interface.is_open()
        assert self._interface.device['methods'] != {}

    def test_version(self: object) -> None:
        assert self._interface.device['version'] == _version

    def test_ping(self: object) -> None:
        assert self._interface.ping(3) == 3

    def test_type_1(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['return']['typename']
            == 'int')

    def test_fmt_1(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['return']['fmt'] == 'B')

    def test_param_1(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['parameters'][0]['typename']
            == 'int')

    def test_param_2(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['parameters'][0]['fmt']
            == 'B')

    def test_param_3(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['parameters'][0]['name']
            == 'data')

    def test_doc_1(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['doc']
            == 'Echo a value.')

    def test_doc_2(self: object) -> None:
        assert (
            self._interface.device['methods']['ping']['parameters'][0]['doc']
            == 'Value.')

    def test_save(self: object) -> None:
        iface_handle = StringIO()

        self._interface.save(iface_handle)
        iface_handle.seek(0)
        device = load(iface_handle, Loader=FullLoader)
        assert device['methods']['ping']['doc'] == 'Echo a value.'

    def test_close(self: object) -> None:
        assert self._interface.is_open()
        assert self._interface.device['methods'] != {}
        self._interface.close()

    def test_post_close(self: object) -> None:
        assert not self._interface.is_open()
        assert self._interface.device['methods'] == {}

    def test_open_load(self: object) -> None:
        iface_handle = StringIO(_interface)

        self._interface.open(iface_handle)
        assert (
            self._interface.device['methods']['ping']['doc'] ==
            'Echo a value.')
        assert not self._interface.device['methods'].get('inc', None)


@mark.test_device('serial')
class TestSerial(_TestDevice):
    _interface = Interface(_devices['serial'], autoconnect=False)


@mark.test_device('wifi')
class TestWiFi(_TestDevice):
    _interface = Interface(_devices['wifi'], autoconnect=False)


@mark.test_device('bt')
class TestBluetooth(_TestDevice):
    _interface = Interface(_devices['bt'], autoconnect=False)
