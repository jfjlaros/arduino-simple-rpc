Arduino SimpleRPC Python client
===============================

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

Only one function call is needed to perform a remote procedure call.

Please see ReadTheDocs_ for the latest documentation.


Quick start
-----------

Export any function e.g., ``digitalRead()`` and ``digitalWrite()`` using the
``interface()`` function.

.. code:: cpp

    #include <simpleRPC.h>

    void setup(void) {
      Serial.begin(9600);
    }

    void loop(void) {
      interface(digitalRead, "", digitalWrite, "");
    }

These functions are now available on the host under name ``method2()`` and
``method3()``.

.. code:: python

    >>> from simple_rpc import Interface
    >>> 
    >>> interface = Interface('/dev/ttyACM0')
    >>> 
    >>> interface.method2(8)
    0
    >>> interface.method3(13, True)

The documentation string can be used to name and describe the method.

.. code:: cpp

    interface(
      digitalRead,
        "digital_read: Read digital pin. @pin: Pin number. @return: Pin value.",
      digitalWrite,
        "digital_write: Write to a digital pin. @pin: Pin number. @value: Pin value.");

This is reflected on the host.

.. code:: python

    >>> help(interface.digital_read)
    Help on method digital_read:

    digital_read(pin) method of simple_rpc.simple_rpc.Interface instance
        Read digital pin.

        :arg int pin: Pin number.

        :returns int: Pin value.

    >>> interface.digital_read(8)
    0
    >>> interface.digital_write(13, True)

For more information about the host library and other interfaces, please see
the :doc:`usage` section.


.. _Arduino: https://www.arduino.cc
.. _simpleRPC: https://simpleRPC.readthedocs.io/en/latest/index.html
.. _ReadTheDocs: https://simpleRPC.readthedocs.io/en/latest/index.html
