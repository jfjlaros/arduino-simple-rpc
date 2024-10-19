from importlib.metadata import metadata

from .extras import dict_to_object, object_to_dict
from .simple_rpc import Interface, SerialInterface, SocketInterface


_package_metadata = metadata('arduino_simple_rpc')
_copyright_notice = 'Copyright (c) {} <{}>'.format(
    _package_metadata['Author'], _package_metadata['Author-email'])
usage = [_package_metadata['Summary'], _copyright_notice]


def doc_split(func: callable) -> str:
    return func.__doc__.split('\n\n')[0]


def version(name: str) -> str:
    return '{} version {}\n\n{}\nHomepage: {}'.format(
        _package_metadata['Name'], _package_metadata['Version'],
        _copyright_notice, _package_metadata['Home-page'])
