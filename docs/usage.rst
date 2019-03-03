Usage
=====

The command line interface can be useful for method discovery and testing
purposes. It currently has two subcommands: ``list``, which shows a list of
available methods and ``call`` for calling methods. For more information, use
the ``-h`` option.

.. code::

    simple_rpc -h


Example
-------

If the Arduino has exposed the functions ``inc`` and ``set_led`` like in the
example_ given in the device library documentation, the ``list`` subcommand
will show the following.

.. code::

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

.. code::

    $ simple_rpc call inc 1
    2


.. _example: https://simplerpc.readthedocs.io/en/latest/usage_device.html#example
