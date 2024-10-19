from simple_rpc.simple_rpc import _version


_devices = {
    'serial': '/dev/ttyUSB0',
    'wifi': 'socket://192.168.21.53:1025',
    'bt': '/dev/rfcomm0'}
_interface = """
endianness: <
methods:
  ping:
    doc: Echo a value.
    index: 0
    name: ping
    parameters:
    - doc: Value.
      fmt: B
      name: data
      typename: int
    return:
      doc: Value of data.
      fmt: B
      typename: int
protocol: simpleRPC
size_t: H
version: !!python/tuple
- 4
- 0
- 0
""".format(''.join(map('- {}\n'.format, _version)))
