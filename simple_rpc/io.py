from struct import calcsize, pack, unpack


_end_of_string = b'\0'


def _read_bytes_until(stream, delimiter):
    """Read bytes from {stream} until the first encounter of {delimiter}.

    :arg stream stream: Stream object.
    :arg bytes delimiter: Delimiter.

    :returns bytes: Byte string.
    """
    data = b''

    while True:
        char = stream.read(1)
        if char == delimiter:
            break
        data += char

    return data


def _read_basic(stream, endianness, basic_type):
    """Read a value of basic type from a stream.

    :arg stream stream: Stream object.
    :arg bytes endianness: Endianness.
    :arg bytes basic_type: Type of {value}.

    :returns any: Value of type {basic_type}.
    """
    if basic_type == b's':
        return _read_bytes_until(stream, _end_of_string)

    full_type = endianness + basic_type

    return unpack(full_type, stream.read(calcsize(full_type)))[0]


def _write_basic(stream, endianness, basic_type, value):
    """Write a value of basic type to a stream.

    :arg stream stream: Stream object.
    :arg bytes endianness: Endianness.
    :arg bytes basic_type: Type of {value}.
    :arg any value: Value to write.
    """
    if basic_type == b's':
        stream.write(value + _end_of_string)
        return

    full_type = endianness + basic_type

    stream.write(pack(full_type, cast(basic_type)(value)))


def cast(c_type):
    """Select the appropriate casting function given a C type.

    :arg bytes c_type: C type.

    :returns obj: Casting function.
    """
    if c_type == b'?':
        return bool
    if c_type in [b'c', b's']:
        return bytes
    if c_type in [b'f', b'd']:
        return float
    return int


def read(stream, endianness, size_t, obj_type):
    """Read an object from a stream.

    :arg stream stream: Stream object.
    :arg bytes endianness: Endianness.
    :arg bytes size_t: Type of size_t.
    :arg any obj_type: Type object.

    :returns any: Object of type {obj_type}.
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


def read_byte_string(stream):
    return _read_bytes_until(stream, _end_of_string)


def write(stream, endianness, size_t, obj_type, obj):
    """Write an object to a stream.

    :arg stream stream: Stream object.
    :arg bytes endianness: Endianness.
    :arg bytes size_t: Type of size_t.
    :arg any obj_type: Type object.
    :arg any obj: Object of type {obj_type}.
    """
    if isinstance(obj_type, list):
        _write_basic(stream, endianness, size_t, len(obj) // len(obj_type))
    if isinstance(obj_type, list) or isinstance(obj_type, tuple):
        for item_type, item in zip(obj_type * len(obj), obj):
            write(stream, endianness, size_t, item_type, item)
    else:
        _write_basic(stream, endianness, obj_type, obj)
