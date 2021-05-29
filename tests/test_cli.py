from io import StringIO

from pytest import mark
from yaml import FullLoader, load

from simple_rpc.cli import _describe_method, rpc_call, rpc_list
from simple_rpc.extras import json_utf8_decode, json_utf8_encode

from conf import _devices, _interface


def test_json_utf8_encode() -> None:
    assert json_utf8_encode(['a', ['b', 10]]) == [b'a', [b'b', 10]]
    assert json_utf8_encode(('a', ('b', 10))) == [b'a', [b'b', 10]]


def test_json_utf8_decode() -> None:
    assert json_utf8_decode([b'a', [b'b', 10]]) == ['a', ['b', 10]]
    assert json_utf8_decode((b'a', (b'b', 10))) == ['a', ['b', 10]]


def test_describe_method() -> None:
    assert (_describe_method({
        'name': 'test',
        'doc': 'Test.',
        'parameters': [
            {'name': 'a', 'typename': 'int', 'doc': 'Parameter a.'},
            {'name': 'b', 'typename': 'str', 'doc': 'Parameter b.'}],
        'return': {
            'fmt': b'f', 'typename': 'float', 'doc': 'Return value.'}}) ==
            'test a b\n    Test.\n\n    int a: Parameter a.\n'
            '    str b: Parameter b.\n\n    returns float: Return value.')


@mark.test_device('serial')
def test_rpc_list() -> None:
    handle = StringIO()

    rpc_list(handle, _devices['serial'], 9600, 1, None)
    assert 'ping data\n    Echo a value.\n' in handle.getvalue()


@mark.test_device('serial')
def test_rpc_list_save() -> None:
    handle = StringIO()
    iface_handle = StringIO()

    rpc_list(handle, _devices['serial'], 9600, 1, iface_handle)
    iface_handle.seek(0)
    device = load(iface_handle, Loader=FullLoader)
    assert device['methods']['ping']['doc'] == 'Echo a value.'


@mark.test_device('serial')
def test_rpc_call() -> None:
    handle = StringIO()

    rpc_call(handle, _devices['serial'], 9600, 1, None, 'ping', ['10'])
    assert handle.getvalue() == '10\n'


@mark.test_device('serial')
def test_rpc_call_load() -> None:
    handle = StringIO()
    iface_handle = StringIO(_interface)

    rpc_call(
        handle, _devices['serial'], 9600, 1, iface_handle, 'ping', ['10'])
    assert handle.getvalue() == '10\n'


@mark.test_device('serial')
def test_rpc_call_load_() -> None:
    handle = StringIO()
    iface_handle = StringIO(_interface)

    try:
        rpc_call(
            handle, _devices['serial'], 9600, 1, iface_handle, 'inc', ['1'])
    except ValueError as error:
        assert str(error) == 'invalid method name: inc'
    else:
        assert False
