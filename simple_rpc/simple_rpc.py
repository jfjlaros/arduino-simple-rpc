from time import sleep
from types import MethodType

from serial import serial_for_url
from serial.serialutil import SerialException
from serial.urlhandler.protocol_socket import Serial as socket_serial

from .extras import make_function
from .io import read, read_byte_string, until, write
from .protocol import parse_line


_protocol = b'simpleRPC'
_version = (3, 0, 0)

_list_req = 0xff


class Interface(object):
    def __init__(self, device, baudrate=9600, wait=1, autoconnect=True):
        """Initialise the class.

        :arg str device: Device name.
        :arg int baudrate: Baud rate.
        :arg int wait: Time in seconds before communication starts.
        :arg bool autoconnect: Automatically connect.
        """
        self._wait = wait

        self._connection = serial_for_url(
            device, do_not_open=True, baudrate=baudrate)
        self._is_socket = isinstance(self._connection, socket_serial)
        self._version = (0, 0, 0)
        self._endianness = b'<'
        self._size_t = b'H'
        self.methods = {}

        if autoconnect:
            self.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _open(self):
        if self._connection.isOpen():
            return
        try:
            self._connection.open()
        except SerialException as error:
            raise IOError(error.strerror.split(':')[0])

    def _close(self):
        if not self._connection.isOpen():
            return
        self._connection.close()

    def _auto_open(f):
        """Decorator for automatic opening and closing of ethernet sockets."""
        def _auto_open_wrapper(self, *args, **kwargs):
            if self._is_socket:
                self._open()

            result = f(self, *args, **kwargs)

            if self._is_socket:
                self._close()

            return result

        return _auto_open_wrapper


    def _select(self, index):
        """Initiate a remote procedure call, select the method.

        :arg int index: Method index.
        """
        self._write(b'B', index)

    def _write(self, obj_type, obj):
        """Provide parameters for a remote procedure call.

        :arg bytes obj_type: Type of the parameter.
        :arg any obj: Value of the parameter.
        """
        write(
            self._connection, self._endianness, self._size_t, obj_type, obj)

    def _read_byte_string(self):
        return read_byte_string(self._connection)

    def _read(self, obj_type):
        """Read a return value from a remote procedure call.

        :arg str obj_type: Return type.

        :returns any: Return value.
        """
        return read(
            self._connection, self._endianness, self._size_t, obj_type)

    @_auto_open
    def _get_methods(self):
        """Get remote procedure call methods.

        :returns dict: Method objects indexed by name.
        """
        self._select(_list_req)

        if self._read_byte_string() != _protocol:
            raise ValueError('missing protocol header')

        self._version = tuple(self._read(b'B') for _ in range(3))
        if self._version[0] != _version[0] or self._version[1] > _version[1]:
            raise ValueError(
                'version mismatch (device: {}, client: {})'.format(
                    '.'.join(map(str, self._version)),
                    '.'.join(map(str, _version))))

        self._endianness, self._size_t = (
            bytes([c]) for c in self._read_byte_string())

        methods = {}
        for index, line in enumerate(
                until(lambda x: x == b'', self._read_byte_string)):
            method = parse_line(index, line)
            methods[method['name']] = method

        return methods

    def open(self):
        """Connect to device."""
        self._open()
        sleep(self._wait)

        self.methods = self._get_methods()
        for method in self.methods.values():
            setattr(
                self, method['name'], MethodType(make_function(method), self))

    def close(self):
        """Disconnect from device."""
        for method in self.methods:
            delattr(self, method)
        self.methods.clear()

        self._close()

    def is_open(self):
        """Query interface state."""
        if self._is_socket:
            return bool(self.methods)
        return self._connection.isOpen()

    @_auto_open
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

        # Call the method.
        self._select(method['index'])

        # Provide parameters (if any).
        if method['parameters']:
            for index, parameter in enumerate(method['parameters']):
                self._write(parameter['fmt'], args[index])

        # Read return value (if any).
        if method['return']['fmt']:
            return self._read(method['return']['fmt'])
        return None
