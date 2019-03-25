from struct import calcsize, pack, unpack

from .io import cast, end_of_string


def parse_type(type_str):
    """Parse a type definition string.

    :arg bytes type_str: Type definition string.

    :returns any: Type object.
    """
    def _construct_type(tokens):
        type_ = []

        for token in tokens:
            if token == b'[':
                type_.append(_construct_type(tokens))
            elif token == b'(':
                type_.append(tuple(_construct_type(tokens)))
            elif token in (b')', b']'):
                break
            else:
                type_.append(token)

        return type_

    return _construct_type((bytes([char]) for char in type_str))


def _type_name(c_type):
    """Python type name of a C type.

    :arg bytes c_type: C type.

    :returns str: Python type name.
    """
    if not c_type:
        return ''
    return cast(c_type).__name__


def _parse_signature(index, signature):
    """Parse a C function signature string.

    :arg int index: Function index.
    :arg bytes signature: Function signature.

    :returns dict: Method object.
    """
    method = {
        'doc': '',
        'index': index,
        'name': 'method{}'.format(index),
        'parameters': [],
        'return': {'doc': ''}}

    method['return']['fmt'], parameters = signature.split(b':')
    method['return']['typename'] = _type_name(method['return']['fmt'])

    for i, type_ in enumerate(parameters.split()):
        method['parameters'].append({
            'doc': '',
            'name': 'arg{}'.format(i),
            'fmt': type_,
            'typename': _type_name(type_)})

    return method


def _strip_split(string, delimiter):
    return list(map(lambda x: x.strip(), string.split(delimiter)))


def _add_doc(method, doc):
    """Add documentation to a method object.

    :arg dict method: Method object.
    :arg str doc: Method documentation.
    """
    parts = list(map(lambda x: _strip_split(x, ':'), doc.split('@')))

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


def _parse_line(index, line):
    """Parse a method definition line.

    :arg int index: Line number.
    :arg bytes line: Method definition.

    :returns dict: Method object.
    """
    signature, description = line.strip(end_of_string).split(b';', 1)

    method = _parse_signature(index, signature)
    _add_doc(method, description)

    return method
