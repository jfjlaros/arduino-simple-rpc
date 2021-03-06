Usage
=====

The command line interface can be useful for method discovery and testing
purposes. It currently has two subcommands: ``list``, which shows a list of
available methods and ``call`` for calling methods. For more information, use
the ``-h`` option.

::

    simple_rpc -h


Basic usage
-----------

If the Arduino has exposed the functions ``inc`` and ``set_led`` like in the
example_ given in the device library documentation, the ``list`` subcommand
will show the following.

::

    $ simple_rpc list
    Available methods:


    inc a
        Increment a value.

        int a: Value.

        returns int: a + 1.


    set_led brightness
        Set LED brightness.

        int brightness: Brightness.


Any of these methods can be called by using the ``call`` subcommand.

::

    $ simple_rpc call inc 1
    2

The ``-d`` option is to select a device. For serial devices, a path can be
used.

::

    $ simple_rpc list -d /dev/ttyUSB0

For ethernet or WiFi devices, a URI can be used.

::

    $ simple_rpc call -d socket://192.168.1.50:10000 inc 1
    2

Please see the list of handlers_ for a full description of the supported
interface types.


Complex objects
---------------

Complex objects are passed on the command line interface as a JSON string.
Binary encoding and decoding is taken care of by the CLI. The following example
makes use of the demo_ sketch in the device examples.

::

    $ simple_rpc call vector '[1, 2, 3, 4]'
    [1.40, 2.40, 3.40, 4.40]

    $ simple_rpc call object '["a", [10, "b"]]'
    ["b", [11, "c"]]


.. _example: https://simplerpc.readthedocs.io/en/latest/usage.html#example
.. _demo: https://github.com/jfjlaros/simpleRPC/blob/master/examples/demo/demo.ino
.. _handlers: https://pyserial.readthedocs.io/en/latest/url_handlers.html
