from io import BytesIO

from simple_rpc.io import (
    _cast, _read_basic, _read_bytes_until, _write_basic, end_of_string, read,
    write)


class TestIO(object):
    def setup(self):
        pass

    def _test_invariance_basic(
            self, f_read, f_write, endianness, basic_type, data, value):
        stream = BytesIO(data)
        value_ = f_read(stream, endianness, basic_type)
        assert value_ == value

        stream = BytesIO()
        f_write(stream, endianness, basic_type, value)
        assert stream.getvalue() == data

    def _test_invariance(
            self, f_read, f_write, endianness, size_t, obj_def, data, obj):
        stream = BytesIO(data)
        obj_ = f_read(stream, endianness, size_t, obj_def)
        assert obj_ == obj

        stream = BytesIO()
        f_write(stream, endianness, size_t, obj_def, obj)
        assert stream.getvalue() == data

    def test_cast(self):
        assert _cast(b'?') == bool
        assert _cast(b'c') == bytes
        assert _cast(b's') == bytes
        assert _cast(b'f') == float
        assert _cast(b'd') == float
        assert _cast(b'h') == int
        assert _cast(b'i') == int

    def test_read_bytes_until(self):
        stream = BytesIO(b'abcdef\0abc')
        assert _read_bytes_until(stream, end_of_string) == b'abcdef'

    def test_basic_string(self):
        self._test_invariance_basic(
            _read_basic, _write_basic, b'<', b's', b'abcdef\0', b'abcdef')

    def test_basic_int_le(self):
        self._test_invariance_basic(
            _read_basic, _write_basic, b'<', b'i', b'\2\0\0\0', 2)

    def test_basic_int_be(self):
        self._test_invariance_basic(
            _read_basic, _write_basic, b'>', b'i', b'\0\0\0\2', 2)

    def test_list_char(self):
        self._test_invariance(
            read, write, b'<', b'h', [b'c'], b'\3\0a\0c', [b'a', b'\0', b'c'])

    def test_list_nibble(self):
        self._test_invariance(
            read, write, b'<', b'h', [b'h'], b'\3\0\1\0\2\0\3\0', [1, 2, 3])

    def test_list_list(self):
        self._test_invariance(
            read, write, b'<', b'h', [[b'b']], b'\2\0\2\0\0\1\2\0\2\3',
            [[0, 1], [2, 3]])

    def test_object_char_int(self):
        self._test_invariance(
            read, write, b'<', b'h', (b'c', b'i'), b'a\3\0\0\0', (b'a', 3))

    def test_object_nibble_string_char(self):
        self._test_invariance(
            read, write, b'<', b'h', (b'h', b's', b'c'), b'\2\0abcdef\0x',
            (2, b'abcdef', b'x'))

    def test_object_object(self):
        self._test_invariance(
            read, write, b'<', b'h', (((b'c', ), ), (b'c', ), ), b'ab',
            (((b'a', ), ), (b'b', )))

    def test_list_tuple(self):
        self._test_invariance(
            read, write, b'<', b'h', [b'c', b'c', b'c'], b'\2\0abcabc',
            [b'a', b'b', b'c', b'a', b'b', b'c'])

    def test_list_object(self):
        self._test_invariance(
            read, write, b'<', b'h', [(b'c', b'c', b'c')], b'\2\0abcabc',
            [(b'a', b'b', b'c'), (b'a', b'b', b'c')])

    def test_list_object_tuple(self):
        self._test_invariance(
            read, write, b'<', b'h', [(b'c', b'c'), b'c'], b'\2\0abcabc',
            [(b'a', b'b'), b'c', (b'a', b'b'), b'c'])
