Installation
============

The software is distributed via PyPI_, it can be installed with ``pip``.

::

    pip install arduino-simple-rpc


From source
-----------

The source is hosted on GitHub_, to install the latest development version, use
the following commands.

::

    git clone https://github.com/jfjlaros/arduino-simple-rpc.git
    cd arduino-simple-rpc
    pip install .

Development
~~~~~~~~~~~

Tests are written in the pytest_ framework which can be installed with ``pip``.

:: 

    pip install pytest

To run the automated tests, run ``py.test`` in the root of the project folder.

By default, all tests that rely on particular hardware to be connected are
disabled. The ``--device`` parameter can be used to enable these device
specific tests.

To test the Bluetooth_ interface.

::

    py.test --device bt

To test the HardwareSerial_ interface.

::

    py.test --device serial

To test the WiFi_ interface.

::

    py.test --device wifi


.. _PyPI: https://pypi.org/project/arduino-simple-rpc
.. _GitHub: https://github.com/jfjlaros/arduino-simple-rpc.git
.. _pytest: https://docs.pytest.org/en/stable/index.html
.. _Bluetooth: https://github.com/jfjlaros/simpleRPC/tree/master/examples/bluetooth
.. _HardwareSerial: https://github.com/jfjlaros/simpleRPC/tree/master/examples/hardwareserial
.. _WiFi: https://github.com/jfjlaros/simpleRPC/tree/master/examples/esp32
