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

In our example, the ``list`` subcommand will show a description of the ``inc``
method and the ``set_led`` method.

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


A method can be called by using the ``call`` subcommand.

.. code::

    $ simple_rpc call inc 1
    2
