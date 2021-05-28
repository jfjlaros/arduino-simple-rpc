from typing import BinaryIO
from struct import calcsize, pack, unpack


def _read_bytes_until(stream: BinaryIO, delimiter: bytes) -> bytes:
    """Read bytes from {stream} until the first encounter of {delimiter}.

    :arg stream: Stream object.
    :arg delimiter: Delimiter.

    :returns: Byte string.
    """
    return b''.join(until(lambda x: x == delimiter, stream.read, 1))


def _read_basic(stream: BinaryIO, endianness: str, basic_type: str) -> any:
    """Read a value of basic type from a stream.

    :arg stream: Stream object.
    :arg endianness: Endianness.
    :arg basic_type: Type of {value}.

    :returns: Value of type {basic_type}.
    """
    if basic_type == 's':
        return _read_bytes_until(stream, b'\0')

    full_type = (endianness + basic_type).encode('utf-8')

    return unpack(full_type, stream.read(calcsize(full_type)))[0]


def _write_basic(
        stream: BinaryIO, endianness: str, basic_type: str, value: any
        ) -> None:
    """Write a value of basic type to a stream.

    :arg stream: Stream object.
    :arg endianness: Endianness.
    :arg basic_type: Type of {value}.
    :arg value: Value to write.
    """
    if basic_type == 's':
        stream.write(value + b'\0')
        return

    full_type = (endianness + basic_type).encode('utf-8')

    stream.write(pack(full_type, cast(basic_type)(value)))


def cast(c_type: str) -> object:
    """Select the appropriate casting function given a C type.

    :arg c_type: C type.

    :returns: Casting function.
    """
    if c_type == '?':
        return bool
    if c_type in ['c', 's']:
        return bytes
    if c_type in ['f', 'd']:
        return float
    return int


def read(
        stream: BinaryIO, endianness: str, size_t: str, obj_type: any
        ) -> any:
    """Read an object from a stream.

    :arg stream: Stream object.
    :arg endianness: Endianness.
    :arg size_t: Type of size_t.
    :arg obj_type: Type object.

    :returns: Object of type {obj_type}.
    """
    if isinstance(obj_type, list):
        length = _read_basic(stream, endianness, size_t)
        return [
            read(stream, endianness, size_t, item) for _ in range(length)
            for item in obj_type]
    if isinstance(obj_type, tuple):
        return tuple(
            read(stream, endianness, size_t, item) for item in obj_type)
    return _read_basic(stream, endianness, obj_type)


def read_byte_string(stream: BinaryIO) -> bytes:
    return _read_bytes_until(stream, b'\0')


def write(
        stream: BinaryIO, endianness: str, size_t: str, obj_type: any,
        obj: any) -> None:
    """Write an object to a stream.

    :arg stream: Stream object.
    :arg endianness: Endianness.
    :arg size_t: Type of size_t.
    :arg obj_type: Type object.
    :arg obj: Object of type {obj_type}.
    """
    if isinstance(obj_type, list):
        _write_basic(stream, endianness, size_t, len(obj) // len(obj_type))
    if isinstance(obj_type, list) or isinstance(obj_type, tuple):
        for item_type, item in zip(obj_type * len(obj), obj):
            write(stream, endianness, size_t, item_type, item)
    else:
        _write_basic(stream, endianness, obj_type, obj)


def until(
        condition: callable, f: callable, *args: list, **kwargs: dict) -> None:
    """Call {f(*args, **kwargs)} until {condition} is true.

    :arg condition: Function that inspects the result of {f}.
    :arg f: Any function.
    :arg *args: Porisional arguments of {f}.
    :arg **kwargs: Keyword arguments of {f}.
    """
    while True:
        result = f(*args, **kwargs)
        if condition(result):
            break
        yield result
