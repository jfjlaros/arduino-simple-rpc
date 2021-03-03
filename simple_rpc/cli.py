from argparse import ArgumentParser, FileType, RawDescriptionHelpFormatter
from json import dumps, loads
from json.decoder import JSONDecodeError
from sys import stdout
from time import sleep
from typing import BinaryIO

from . import doc_split, usage, version
from .extras import json_utf8_decode, json_utf8_encode
from .simple_rpc import Interface


def _describe_method(method: dict) -> str:
    """Make a human readable description of a method.

    :arg method: Method object.

    :returns: Method data in readable form.
    """
    description = method['name']

    for parameter in method['parameters']:
        description += ' {}'.format(parameter['name'])

    if method['doc']:
        description += '\n    {}'.format(method['doc'])

    if method['parameters']:
        description += '\n'
    for parameter in method['parameters']:
        description += '\n    {} {}'.format(
            parameter['typename'], parameter['name'])
        if parameter['doc']:
            description += ': {}'.format(parameter['doc'])

    if method['return']['fmt']:
        description += '\n\n    returns {}'.format(
            method['return']['typename'])
        if method['return']['doc']:
            description += ': {}'.format(method['return']['doc'])

    return description


def _loads(string: str) -> str:
    try:
        return loads(string)
    except JSONDecodeError:
        return string


def rpc_list(handle: BinaryIO, device: str, baudrate: int, wait: int) -> None:
    """List the device methods.

    :arg handle: Output handle.
    :arg device: Device.
    :arg baudrate: Baud rate.
    :arg wait: Time in seconds before communication starts.
    """
    with Interface(device, baudrate, wait) as interface:
        for method in interface.methods.values():
            handle.write(_describe_method(method) + '\n\n\n')


def rpc_call(
        handle: BinaryIO, device: str, baudrate: int, wait: int, name: str,
        args: list) -> None:
    """Execute a method.

    :arg handle: Output handle.
    :arg device: Device.
    :arg baudrate: Baud rate.
    :arg wait: Time in seconds before communication starts.
    :arg name: Method name.
    :arg args: Method parameters.
    """
    args_ = list(map(lambda x: json_utf8_encode(_loads(x)), args))

    with Interface(device, baudrate, wait) as interface:
        result = interface.call_method(name, *args_)

        if result != None:
            handle.write('{}\n'.format(dumps(json_utf8_decode(result))))


def main() -> None:
    """Main entry point."""
    output_parser = ArgumentParser(add_help=False)
    output_parser.add_argument(
        '-o', dest='handle', metavar='OUTPUT', type=FileType('w'),
        default=stdout, help='output file')

    common_parser = ArgumentParser(add_help=False, parents=[output_parser])
    common_parser.add_argument(
        'device', metavar='DEVICE', type=str, help='device (%(type)s)')
    common_parser.add_argument(
        '-b', dest='baudrate', type=int, default=9600,
        help='baud rate (%(type)s default=%(default)s)')
    common_parser.add_argument(
        '-w', dest='wait', type=int, default=2,
        help='time before communication starts (%(type)s default=%(default)s)')

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument(
        '-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    subparser = subparsers.add_parser(
        'list', parents=[common_parser], description=doc_split(rpc_list))
    subparser.set_defaults(func=rpc_list)

    subparser = subparsers.add_parser(
        'call', parents=[common_parser], description=doc_split(rpc_call))
    subparser.set_defaults(func=rpc_call)
    subparser.add_argument(
        'name', metavar='NAME', type=str, help='command name')
    subparser.add_argument(
        'args', metavar='ARG', type=str, nargs='*', help='command parameter')

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    try:
        args.func(**{k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except (IOError, TypeError, ValueError) as error:
        parser.error(error)


if __name__ == '__main__':
    main()
