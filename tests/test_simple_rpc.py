from simple_rpc.simple_rpc import (
    SerialInterface, SocketInterface, Interface,
    _assert_protocol, _assert_version, _protocol, _version)

from conf import _devices


def test_assert_protocol_pass() -> None:
    _assert_protocol(_protocol)


def test_assert_protocol_fail() -> None:
    try:
        _assert_protocol('')
    except ValueError as error:
        assert str(error) == 'invalid protocol header'
    else:
        assert False


def test_assert_version_pass() -> None:
    _assert_version(_version)


def test_assert_version_fail() -> None:
    try:
        _assert_version((0, 0, 0))
    except ValueError as error:
        assert str(error).startswith('version mismatch')
    else:
        assert False


def test_SerialInterface() -> None:
    interface = Interface(_devices['serial'], autoconnect=False)
    assert isinstance(interface, SerialInterface)


def test_SocketInterface() -> None:
    interface = Interface(_devices['wifi'], autoconnect=False)
    assert isinstance(interface, SocketInterface)
