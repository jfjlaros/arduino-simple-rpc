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
    def __init__(self, device, baudrate=9600):
        """
        :arg str device: Device name.
        :arg int baudrate: Baud rate.
        """
        self._connection = serial_for_url(
            device, do_not_open=True, baudrate=baudrate)
        self._version = (0, 0, 0)
        self._endianness = b'<'
        self._size_t = b'H'
        self.methods = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _open(self):
        try:
            self._connection.open()
        except SerialException as error:
            raise IOError(error.strerror.split(':')[0])

    def _close(self):
        self._connection.close()

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
        write(self._connection, self._endianness, self._size_t, obj_type, obj)

    def _read_byte_string(self):
        return read_byte_string(self._connection)

    def _read(self, obj_type):
        """Read a return value from a remote procedure call.

        :arg str obj_type: Return type.

        :returns any: Return value.
        """
        return read(self._connection, self._endianness, self._size_t, obj_type)

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
        self.methods = self._get_methods()
        for method in self.methods.values():
            setattr(
                self, method['name'], MethodType(make_function(method), self))

    def close(self):
        """Disconnect from device."""
        for method in self.methods:
            delattr(self, method)
        self.methods.clear()

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


class SerialInterface(Interface):
    def __init__(self, device, baudrate=9600, wait=2, autoconnect=True):
        """
        :arg str device: Device name.
        :arg int baudrate: Baud rate.
        :arg int wait: Time in seconds before communication starts.
        :arg bool autoconnect: Automatically connect.
        """
        super().__init__(device, baudrate)
        self._wait = wait

        if autoconnect:
            self.open()

    def is_open(self):
        """Query interface state."""
        return self._connection.isOpen()

    def open(self):
        """Connect to device."""
        self._open()
        sleep(self._wait)
        super().open()

    def close(self):
        """Disconnect from device."""
        super().close()
        self._close()


class SocketInterface(Interface):
    def __init__(self, device, baudrate=9600, autoconnect=True):
        """
        :arg str device: Device name.
        :arg int baudrate: Baud rate.
        """
        super().__init__(device, baudrate)

        if autoconnect:
            self.open()
            self._close()

    def _auto_open(f):
        """Decorator for automatic opening and closing of ethernet sockets."""
        def _auto_open_wrapper(self, *args, **kwargs):
            self._open()
            result = f(self, *args, **kwargs)
            self._close()

            return result

        return _auto_open_wrapper

    @_auto_open
    def _get_methods(self):
        """Get remote procedure call methods.

        :returns dict: Method objects indexed by name.
        """
        return super()._get_methods()

    def is_open(self):
        """Query interface state."""
        return len(self.methods) > 0

    @_auto_open
    def call_method(self, name, *args):
        """Execute a method.

        :arg str name: Method name.
        :arg list *args: Method parameters.

        :returns any: Return value of the method.
        """
        return super().call_method(name, *args)
