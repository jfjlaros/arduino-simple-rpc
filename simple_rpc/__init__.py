from os.path import dirname, abspath

from configparser import ConfigParser

from .simple_rpc import Interface
from .extras import dict_to_object, object_to_dict


config = ConfigParser()
with open('{}/setup.cfg'.format(dirname(abspath(__file__)))) as handle:
    config.read_file(handle)

_copyright_notice = 'Copyright (c) {} {} <{}>'.format(
    config.get('metadata', 'copyright'),
    config.get('metadata', 'author'),
    config.get('metadata', 'author_email'))

usage = [config.get('metadata', 'description'), _copyright_notice]


def doc_split(func):
    return func.__doc__.split('\n\n')[0]


def version(name):
    return '{} version {}\n\n{}\nHomepage: {}'.format(
        config.get('metadata', 'name'),
        config.get('metadata', 'version'),
        _copyright_notice,
        config.get('metadata', 'url'))
