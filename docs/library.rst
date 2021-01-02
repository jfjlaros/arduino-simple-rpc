Library
=======

The API library provides several interfaces, discussed below. All interfaces
share the methods described in Section `Generic methods`_.


Serial interface
----------------

A ``SerialInterface`` class instance is made by passing the path to a device to
the constructor.

.. code:: python

    >>> from simple_rpc import SerialInterface
    >>> interface = Interface('/dev/ttyACM0')

The constructor takes the following parameters.

.. list-table:: Constructor parameters.
   :header-rows: 1

   * - name
     - optional
     - description
   * - ``device``
     - no
     - Device name.
   * - ``baudrate``
     - yes
     - Baud rate.
   * - ``wait``
     - yes
     - Time in seconds before communication starts.
   * - ``autoconnect``
     - yes
     - Automatically connect.


Socket interface
----------------

A ``SocketInterface`` class instance is made by passing a URI to the
constructor.

.. code:: python

    >>> from simple_rpc import SocketInterface
    >>> interface = Interface('socket://192.168.1.50:10000')

The constructor takes the following parameters.

.. list-table:: Constructor parameters.
   :header-rows: 1

   * - name
     - optional
     - description
   * - ``device``
     - no
     - Device name.
   * - ``baudrate``
     - yes
     - Baud rate.
   * - ``autoconnect``
     - yes
     - Automatically connect.


Generic interface
-----------------

The ``Interface`` class can be used when the type of device is not known
beforehand,

When a path to a serial device is given, it returns a ``SerialInterface`` class
instance.

.. code:: python

    >>> from simple_rpc import Interface
    >>> interface = Interface('/dev/ttyACM0')
    >>> interface.__class__
    <class 'simple_rpc.simple_rpc.SerialInterface'>

When a URI is given, it returns a ``SocketInterface`` class instance.

.. code:: python

    >>> interface = Interface('socket://192.168.1.50:10000')
    >>> interface.__class__
    <class 'simple_rpc.simple_rpc.SocketInterface'>


Generic methods
---------------

The ``SerialInterface`` and the ``SocketInterface`` provide the following
standard methods.

.. list-table:: Class methods.
   :header-rows: 1

   * - name
     - description
   * - ``open()``
     - Connect to device.
   * - ``close()``
     - Disconnect from device.
   * - ``is_open()``
     - Query device state.
   * - ``call_method()``
     - Execute a method.

The ``open()`` function is used to connect to a device, this is needed when
``autoconnect=False`` is passed to the constructor.

.. code:: python

    >>> interface = SerialInterface('/dev/ttyACM0', autoconnect=False)
    >>> # Do something.
    >>> interface.open()

The connection state can be queried using the ``is_open()`` function and it can
be closed using the ``close()`` function.

.. code:: python

    >>> if interface.is_open():
    >>>     interface.close()

Additionally, the ``with`` statement is supported for easy opening and closing.

.. code:: python

    >>> with SerialInterface('/dev/ttyACM0') as interface:
    >>>     interface.ping(10)

The class instance has a public member variable named ``methods`` which
contains the definitions of the exported methods.

.. code:: python

    >>> list(interface.methods)
    ['inc', 'set_led']

Example of a method definition.

.. code:: python

    >>> interface.methods['inc']
    {
      'doc': 'Increment a value.',
      'index': 2,
      'name': 'inc',
      'parameters': [
        {
          'doc': 'Value.',
          'name': 'a',
          'fmt': b'h',
          'typename': 'int'
        }
      ],
      'return': {
        'doc': 'a + 1.',
        'fmt': b'h',
        'typename': 'int'}
    }

Every exported method will show up as a class method of the ``interface`` class
instance. These methods can be used like any normal class methods.
Alternatively, the exported methods can be called by name using the
``call_method()`` function.


Basic usage
-----------

In the example_ given in the device library documentation, the ``inc`` method
is exported, which is now present as a class method of the ``SerialInterface``
class instance.

.. code:: python

    >>> interface.inc(1)
    2

Alternatively, the exported method can be called using the ``call_mathod()``
function.

.. code:: python

    >>> interface.call_method('inc', 1)
    2

To get more information about this class method, the built-in ``help()``
function can be used.

.. code:: python

    >>> help(interface.inc)
    Help on method inc:

    inc(a) method of simple_rpc.simple_rpc.SerialInterface instance
        Increment a value.

        :arg int a: Value.

        :returns int: a + 1.

Note that strings should be encoded as ``bytes`` objects. If, for example, we
have a function named ``test`` that takes a string as parameter, we should call
this function as follows.

.. code:: python

    >>> interface.test(b'hello world')


Complex objects
---------------

Some methods may have complex objects like Tuples, Objects or Vectors as
parameters or return type.

In the following example, we call a method that takes a Vector of integers and
returns a Vector of floats.

.. code:: python

    >>> interface.vector([1, 2, 3, 4])
    [1.40, 2.40, 3.40, 4.40]

In this example, we call a method that takes an Object containing a byte and an
other Object. A similar Object is returned.

.. code:: python

    >>> interface.object((b'a', (10, b'b')))
    (b'b', (11, b'c'))



.. _example: https://simplerpc.readthedocs.io/en/latest/usage_device.html#example
