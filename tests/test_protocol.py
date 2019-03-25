from simple_rpc.protocol import parse_type


def test_parse_type_basic():
    assert parse_type(b'i') == [b'i']


def test_parse_type_tuple_basic():
    assert parse_type(b'ic') == [b'i', b'c']


def test_parse_type_list_basic():
    assert parse_type(b'[i]') == [[b'i']]


def test_parse_type_object_basic():
    assert parse_type(b'(i)') == [(b'i', )]


def test_parse_type_tuple_list():
    assert parse_type(b'[i]c') == [[b'i'], b'c']


def test_parse_type_tuple_object():
    assert parse_type(b'(i)c') == [(b'i', ), b'c']


def test_parse_type_list_tuple():
    assert parse_type(b'[ic]') == [[b'i', b'c']]


def test_parse_type_list_object():
    assert parse_type(b'[(ic)]') == [[(b'i', b'c')]]


def test_parse_type_list_list():
    assert parse_type(b'[[i]]') == [[[b'i']]]


def test_parse_type_object_tuple():
    assert parse_type(b'(ic)') == [(b'i', b'c')]


def test_parse_type_object_list():
    assert parse_type(b'([i])') == [([b'i'], )]


def test_parse_type_object_object():
    assert parse_type(b'((ic))') == [((b'i', b'c'), )]


def test_parse_type_complex():
    assert parse_type(b'((cc)c)i([c])') == [
        ((b'c', b'c'), b'c'), b'i', ([b'c'], )]
