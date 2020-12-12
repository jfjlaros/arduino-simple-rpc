from types import MethodType

from serial import serial_for_url
from serial.serialutil import SerialException

from .extras import make_function
from .io import read, read_byte_string, write
from .protocol import parse_line


_protocol = b'simpleRPC'
_version = (3, 0, 0)

_list_req = 0xff


class Interface(object):
    def __init__(self, device, baudrate=9600):
        """Initialise the class.

        :arg str device: Device name.
        :arg int baudrate: Baud rate.
        :arg int wait: Time in seconds before communication starts.
        :arg bool autoconnect: Automatically connect.
        """
        self._device = device
        self._baudrate = baudrate

        self._version = (0, 0, 0)
        self._endianness = b'<'
        self._size_t = b'H'

        self.methods = self._get_methods()
        for method in self.methods.values():
            setattr(
                self, method['name'], MethodType(make_function(method), self))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _select(self, connection, index):
        """Initiate a remote procedure call, select the method.

        :arg int index: Method index.
        """
        self._write(connection, b'B', index)

    def _write(self, connection, obj_type, obj):
        """Provide parameters for a remote procedure call.

        :arg bytes obj_type: Type of the parameter.
        :arg any obj: Value of the parameter.
        """
        write(connection, self._endianness, self._size_t, obj_type, obj)

    def _read_byte_string(self, connection):
        return read_byte_string(connection)

    def _read(self, connection, obj_type):
        """Read a return value from a remote procedure call.

        :arg str obj_type: Return type.

        :returns any: Return value.
        """
        return read(connection, self._endianness, self._size_t, obj_type)

    def _get_methods(self):
        """Get remote procedure call methods.

        :returns dict: Method objects indexed by name.
        """
        methods = {}

        try:
            with serial_for_url(self._device, baudrate=self._baudrate) as connection:
                self._select(connection, _list_req)

                if self._read_byte_string(connection) != _protocol:
                    raise ValueError('missing protocol header')

                self._version = tuple(self._read(connection, b'B') for _ in range(3))
                if self._version[0] != _version[0] or self._version[1] > _version[1]:
                    raise ValueError(
                        'version mismatch (device: {}, client: {})'.format(
                            '.'.join(map(str, self._version)),
                            '.'.join(map(str, _version))))

                self._endianness, self._size_t = (
                    bytes([c]) for c in self._read_byte_string(connection))

                index = 0
                line = self._read_byte_string(connection)
                while line:
                    method = parse_line(index, line)
                    methods[method['name']] = method
                    line = self._read_byte_string(connection)
                    index += 1

        except SerialException:
            pass

        return methods

    def call_method(self, name, *args):
        """Execute a method.

        :arg str name: Method name.
        :arg list *args: Method parameters.

        :returns any: Return value of the method.
        """
        if name not in self.methods:
            raise ValueError('invalid method name: {}'.format(name))
        method = self.methods[name]

        parameters = method['parameters']
        if len(args) != len(parameters):
            raise TypeError(
                '{} expected {} arguments, got {}'.format(
                    name, len(parameters), len(args)))

        result = None
        try:
            with serial_for_url(self._device, baudrate=self._baudrate) as connection:

                # Call the method.
                self._select(connection, method['index'])

                # Provide parameters (if any).
                if method['parameters']:
                    for index, parameter in enumerate(method['parameters']):
                        self._write(connection, parameter['fmt'], args[index])

                # Read return value (if any).
                if method['return']['fmt']:
                    result = self._read(connection, method['return']['fmt'])
        except SerialException:
            pass

        return result
