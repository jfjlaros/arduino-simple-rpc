from simple_rpc.protocol import (
    _add_doc, _parse_signature, _strip_split, _type_name, _parse_type,
    parse_line)


def test_parse_type_none() -> None:
    assert _parse_type(b'') == b''


def test_parse_type_basic() -> None:
    assert _parse_type(b'i') == b'i'


def test_parse_type_tuple() -> None:
    try:
        _parse_type(b'ic')
    except ValueError as error:
        assert str(error) == 'top level type can not be tuple'
    else:
        assert False

def test_parse_type_list_basic() -> None:
    assert _parse_type(b'[i]') == [b'i']


def test_parse_type_object_basic() -> None:
    assert _parse_type(b'(i)') == (b'i', )


def test_parse_type_list_tuple() -> None:
    assert _parse_type(b'[ic]') == [b'i', b'c']


def test_parse_type_list_object() -> None:
    assert _parse_type(b'[(ic)]') == [(b'i', b'c')]


def test_parse_type_list_list() -> None:
    assert _parse_type(b'[[i]]') == [[b'i']]


def test_parse_type_object_tuple() -> None:
    assert _parse_type(b'(ic)') == (b'i', b'c')


def test_parse_type_object_list() -> None:
    assert _parse_type(b'([i])') == ([b'i'], )


def test_parse_type_object_object() -> None:
    assert _parse_type(b'((ic))') == ((b'i', b'c'), )


def test_parse_type_complex() -> None:
    assert _parse_type(b'(((cc)c)i([c]))') == (
        ((b'c', b'c'), b'c'), b'i', ([b'c'], ), )


def test_type_name_none() -> None:
    assert _type_name(None) == ''


def test_type_name_basic() -> None:
    assert _type_name(b'c') == 'bytes'
    assert _type_name(b'i') == 'int'
    assert _type_name(b'?') == 'bool'
    assert _type_name(b'f') == 'float'


def test_type_name_tuple_basic() -> None:
    assert _type_name([b'i', b'c']) == '[int, bytes]'
    assert _type_name([b'?', b'f']) == '[bool, float]'


def test_type_name_list_basic() -> None:
    assert _type_name([[b'i']]) == '[[int]]'


def test_type_name_object_basic() -> None:
    assert _type_name([(b'i',)]) == '[(int)]'


def test_type_name_complex() -> None:
    assert (_type_name([((b'c', b'c'), b'c'), b'i', ([b'c'], )]) ==
        '[((bytes, bytes), bytes), int, ([bytes])]')


def test_parse_signature_basic() -> None:
    assert _parse_signature(1, b': c f') == {
        'doc': '',
        'index': 1,
        'name': 'method1',
        'parameters': [{
            'doc': '', 'fmt': b'c', 'name': 'arg0', 'typename': 'bytes'}, {
            'doc': '', 'fmt': b'f', 'name': 'arg1', 'typename': 'float'}],
        'return': {'doc': '', 'fmt': b'', 'typename': ''}}


def test_parse_signature_complex() -> None:
    assert _parse_signature(2, b'(ff): [c] (cf)') == {
        'doc': '',
        'index': 2,
        'name': 'method2',
        'parameters': [{
            'doc': '', 'fmt': [b'c'], 'name': 'arg0',
                'typename': '[bytes]'}, {
            'doc': '', 'fmt': (b'c', b'f'), 'name': 'arg1',
                'typename': '(bytes, float)'}],
        'return': {'doc': '', 'fmt': (b'f', b'f'),
            'typename': '(float, float)'}}


def test_split_strip() -> None:
    assert _strip_split(' p1 : Param 1. ', ':') == ['p1', 'Param 1.']
    assert _strip_split('p1:Param 1.', ':') == ['p1', 'Param 1.']


def test_add_doc_basic() -> None:
    method = _parse_signature(1, b'i: c f')
    _add_doc(method, b'name: Test. @p1: Char. @p2: Float. @return: Int.')

    assert method['name'] == 'name'
    assert method['doc'] == 'Test.'
    assert method['parameters'][0]['name'] == 'p1'
    assert method['parameters'][0]['doc'] == 'Char.'
    assert method['parameters'][1]['name'] == 'p2'
    assert method['parameters'][1]['doc'] == 'Float.'
    assert method['return']['doc'] == 'Int.'


def test_add_doc_missing_name() -> None:
    method = _parse_signature(1, b': c f')
    _add_doc(method, b'@p1: Char. @p2: Float.')

    assert method['name'] == 'method1'
    assert method['doc'] == ''
    assert method['parameters'][0]['name'] == 'arg0'


def test_add_doc_missing_parameter() -> None:
    method = _parse_signature(1, b': c f')
    _add_doc(method, b'name: Test. @p1: Char')

    assert method['name'] == 'name'
    assert method['parameters'][0]['name'] == 'p1'
    assert method['parameters'][1]['name'] == 'arg1'


def test_parse_line() -> None:
    method = parse_line(
        1, b'i: c f;name: Test. @p1: Char. @p2: Float. @return: Int.')

    assert method['index'] == 1
    assert method['name'] == 'name'
