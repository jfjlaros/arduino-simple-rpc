Arduino simpleRPC API client library and CLI
============================================

.. image:: https://img.shields.io/github/last-commit/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc/graphs/commit-activity
.. image:: https://travis-ci.org/jfjlaros/arduino-simple-rpc.svg?branch=master
   :target: https://travis-ci.org/jfjlaros/arduino-simple-rpc
.. image:: https://readthedocs.org/projects/simplerpc/badge/?version=latest
   :target: https://arduino-simple-rpc.readthedocs.io/en/latest
.. image:: https://img.shields.io/github/release-date/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc/releases
.. image:: https://img.shields.io/github/release/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc/releases
.. image:: https://img.shields.io/pypi/v/arduino-simple-rpc.svg
   :target: https://pypi.org/project/arduino-simple-rpc/
.. image:: https://img.shields.io/github/languages/code-size/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc
.. image:: https://img.shields.io/github/languages/count/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc
.. image:: https://img.shields.io/github/languages/top/jfjlaros/arduino-simple-rpc.svg
   :target: https://github.com/jfjlaros/arduino-simple-rpc
.. image:: https://img.shields.io/github/license/jfjlaros/arduino-simple-rpc.svg
   :target: https://raw.githubusercontent.com/jfjlaros/arduino-simple-rpc/master/LICENSE.md

----

This library provides a simple way to interface to Arduino_ functions exported
with the simpleRPC_ protocol. The exported method definitions are communicated
to the host, which is then able to generate an API interface using this
library.

**Features:**

- User friendly API library.
- Command line interface (CLI) for method discovery and testing.
- Function and parameter names are defined on the Arduino.
- API documentation is defined on the Arduino.
- Support for disconnecting and reconnecting.

Please see ReadTheDocs_ for the latest documentation.


Quick start
-----------

Export any function e.g., ``digitalRead()`` and ``digitalWrite()`` on the
Arduino, these functions will show up as member functions of the ``Interface``
class instance.

First, we make an ``Interface`` class instance and tell it to connect to the
serial device ``/dev/ttyACM0``.

.. code:: python

    >>> from simple_rpc import Interface
    >>> 
    >>> interface = Interface('/dev/ttyACM0')

We can use the built-in ``help()`` function to see the API documentation of any
exported method.

.. code:: python

    >>> help(interface.digital_read)
    Help on method digital_read:

    digital_read(pin) method of simple_rpc.simple_rpc.Interface instance
        Read digital pin.

        :arg int pin: Pin number.

        :returns int: Pin value.

All exposed methods can be called like any other class method.

.. code:: python

    >>> interface.digital_read(8)         # Read from pin 8.
    0
    >>> interface.digital_write(13, True) # Turn LED on.


Further reading
---------------

For more information about the host library and other interfaces, please see
the :doc:`usage` and :doc:`library` sections.


.. _Arduino: https://www.arduino.cc
.. _simpleRPC: https://simpleRPC.readthedocs.io
.. _ReadTheDocs: https://arduino-simple-rpc.readthedocs.io
