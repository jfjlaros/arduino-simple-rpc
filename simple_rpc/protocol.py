from typing import BinaryIO

from .io import cast, read_byte_string


def _parse_type(type_str: bytes) -> any:
    """Parse a type definition string.

    :arg type_str: Type definition string.

    :returns: Type object.
    """
    def _construct_type(tokens: tuple):
        obj_type = []

        for token in tokens:
            if token == b'[':
                obj_type.append(_construct_type(tokens))
            elif token == b'(':
                obj_type.append(tuple(_construct_type(tokens)))
            elif token in (b')', b']'):
                break
            else:
                obj_type.append(token.decode())

        return obj_type

    obj_type = _construct_type((bytes([char]) for char in type_str))

    if len(obj_type) > 1:
        raise ValueError('top level type can not be tuple')
    if not obj_type:
        return ''
    return obj_type[0]


def _type_name(obj_type: any) -> str:
    """Python type name of a C object type.

    :arg obj_type: C object type.

    :returns: Python type name.
    """
    if not obj_type:
        return ''
    if isinstance(obj_type, list):
        return '[' + ', '.join([_type_name(item) for item in obj_type]) + ']'
    if isinstance(obj_type, tuple):
        return '(' + ', '.join([_type_name(item) for item in obj_type]) + ')'
    return cast(obj_type).__name__


def _parse_signature(index: int, signature: bytes) -> dict:
    """Parse a C function signature string.

    :arg index: Function index.
    :arg signature: Function signature.

    :returns: Method object.
    """
    method = {
        'doc': '',
        'index': index,
        'name': 'method{}'.format(index),
        'parameters': [],
        'return': {'doc': ''}}

    fmt, parameters = signature.split(b':')
    method['return']['fmt'] = _parse_type(fmt)
    method['return']['typename'] = _type_name(method['return']['fmt'])

    for index, fmt in enumerate(parameters.split()):
        type_ = _parse_type(fmt)
        method['parameters'].append({
            'doc': '',
            'name': 'arg{}'.format(index),
            'fmt': type_,
            'typename': _type_name(type_)})

    return method


def _strip_split(string: str, delimiter: str) -> list:
    return list(map(lambda x: x.strip(), string.split(delimiter)))


def _add_doc(method: dict, doc: bytes) -> None:
    """Add documentation to a method object.

    :arg method: Method object.
    :arg doc: Method documentation.
    """
    parts = list(map(
        lambda x: _strip_split(x, ':'), doc.decode('utf-8').split('@')))

    if list(map(lambda x: len(x), parts)) != [2] * len(parts):
        return

    method['name'], method['doc'] = parts[0]

    index = 0
    for part in parts[1:]:
        name, description = part

        if name != 'return':
            if index < len(method['parameters']):
                method['parameters'][index]['name'] = name
                method['parameters'][index]['doc'] = description
            index += 1
        else:
            method['return']['doc'] = description


def parse_line(index: int, line: bytes) -> dict:
    """Parse a method definition line.

    :arg index: Line number.
    :arg line: Method definition.

    :returns: Method object.
    """
    signature, description = line.split(b';', 1)

    method = _parse_signature(index, signature)
    _add_doc(method, description)

    return method


def hardware_defs(stream: BinaryIO) -> tuple:
    return tuple(bytes([char]) for char in read_byte_string())
