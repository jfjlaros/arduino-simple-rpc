from io import BytesIO

from simple_rpc.io import (
    _end_of_string, _read_basic, _read_bytes_until, _write_basic, cast, read,
    write)


def _test_invariance_basic(
        f_read, f_write, endianness, basic_type, data, value):
    stream = BytesIO(data)
    value_ = f_read(stream, endianness, basic_type)
    assert value_ == value

    stream = BytesIO()
    f_write(stream, endianness, basic_type, value)
    assert stream.getvalue() == data


def _test_invariance(f_read, f_write, endianness, size_t, obj_def, data, obj):
    stream = BytesIO(data)
    obj_ = f_read(stream, endianness, size_t, obj_def)
    assert obj_ == obj

    stream = BytesIO()
    f_write(stream, endianness, size_t, obj_def, obj)
    assert stream.getvalue() == data


def test_cast():
    assert cast(b'?') == bool
    assert cast(b'c') == bytes
    assert cast(b's') == bytes
    assert cast(b'f') == float
    assert cast(b'd') == float
    assert cast(b'h') == int
    assert cast(b'i') == int


def test_read_bytes_until():
    stream = BytesIO(b'abcdef\0abc')

    assert _read_bytes_until(stream, _end_of_string) == b'abcdef'


def test_basic_string():
    _test_invariance_basic(
        _read_basic, _write_basic, b'<', b's', b'abcdef\0', b'abcdef')


def test_basic_int_le():
    _test_invariance_basic(
        _read_basic, _write_basic, b'<', b'i', b'\2\0\0\0', 2)


def test_basic_int_be():
    _test_invariance_basic(
        _read_basic, _write_basic, b'>', b'i', b'\0\0\0\2', 2)


def test_list_char():
    _test_invariance(
        read, write, b'<', b'h', [b'c'], b'\3\0a\0c', [b'a', b'\0', b'c'])


def test_list_nibble():
    _test_invariance(
        read, write, b'<', b'h', [b'h'], b'\3\0\1\0\2\0\3\0', [1, 2, 3])


def test_list_list():
    _test_invariance(
        read, write, b'<', b'h', [[b'b']], b'\2\0\2\0\0\1\2\0\2\3',
        [[0, 1], [2, 3]])


def test_object_char_int():
    _test_invariance(
        read, write, b'<', b'h', (b'c', b'i'), b'a\3\0\0\0', (b'a', 3))


def test_object_nibble_string_char():
    _test_invariance(
        read, write, b'<', b'h', (b'h', b's', b'c'), b'\2\0abcdef\0x',
        (2, b'abcdef', b'x'))


def test_object_object():
    _test_invariance(
        read, write, b'<', b'h', (((b'c', ), ), (b'c', ), ), b'ab',
        (((b'a', ), ), (b'b', )))


def test_list_tuple():
    _test_invariance(
        read, write, b'<', b'h', [b'c', b'c', b'c'], b'\2\0abcabc',
        [b'a', b'b', b'c', b'a', b'b', b'c'])


def test_list_object():
    _test_invariance(
        read, write, b'<', b'h', [(b'c', b'c', b'c')], b'\2\0abcabc',
        [(b'a', b'b', b'c'), (b'a', b'b', b'c')])


def test_list_object_tuple():
    _test_invariance(
        read, write, b'<', b'h', [(b'c', b'c'), b'c'], b'\2\0abcabc',
        [(b'a', b'b'), b'c', (b'a', b'b'), b'c'])
