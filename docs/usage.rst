Usage
=====

The command line interface can be useful for method discovery and testing
purposes. It currently has two subcommands: ``list``, which shows a list of
available methods and ``call`` for calling methods. For more information, use
the ``-h`` option.

::

    $ simple_rpc -h

.. note::

    Please note that the initialisation procedure has a built in two second
    delay which can be modified with the ``-w`` parameter. For each invocation
    of ``list`` or ``call``, the device is reset and reinitialised, so using
    the command line interface for time critical or high speed applications is
    not advised. For these types of applications, the :doc:`library` should be
    used directly instead.


Connecting
----------

To detect serial devices, we recommend using the arduino-cli_ toolkit.

::

    $ arduino-cli board list
    Port         Type              Board Name                FQBN             Core
    /dev/ttyACM0 Serial Port (USB) Arduino Mega or Mega 2560 arduino:avr:mega arduino:avr

This command will not detect any devices connected via ethernet or WiFi. Use a
URL_ (e.g., ``socket://192.168.1.50:10000``) instead.


Method discovery
----------------

When the device is known, the ``list`` subcommand can be used to retrieve all
available methods.

::

    $ simple_rpc list /dev/ttyACM0

Alternatively, for ethernet and WiFi devices.

::

    $ simple_rpc list socket://192.168.1.50:10000

If the Arduino has exposed the functions ``inc`` and ``set_led`` like in the
example_ given in the device library documentation, the ``list`` subcommand
will show the following.

::

    inc a
        Increment a value.

        int a: Value.

        returns int: a + 1.


    set_led brightness
        Set LED brightness.

        int brightness: Brightness.


Calling a method
----------------

Any of the methods can be called by using the ``call`` subcommand.

::

    $ simple_rpc call /dev/ttyACM0 inc 1
    2

Alternatively, for ethernet or WiFi devices.

::

    $ simple_rpc call socket://192.168.1.50:10000 inc 1
    2

Please see the list of handlers_ for a full description of the supported
interface types.


Complex objects
---------------

Complex objects are passed on the command line interface as a JSON string.
Binary encoding and decoding is taken care of by the CLI. The following example
makes use of the demo_ sketch in the device examples.

::

    $ simple_rpc call /dev/ttyACM0 vector '[1, 2, 3, 4]'
    [1.40, 2.40, 3.40, 4.40]

    $ simple_rpc call /dev/ttyACM0 object '["a", [10, "b"]]'
    ["b", [11, "c"]]


.. _arduino-cli: https://arduino.github.io/arduino-cli/latest/
.. _demo: https://github.com/jfjlaros/simpleRPC/blob/master/examples/demo/demo.ino
.. _example: https://simplerpc.readthedocs.io/en/latest/usage.html#example
.. _handlers: https://pyserial.readthedocs.io/en/latest/url_handlers.html
