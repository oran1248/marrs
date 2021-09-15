Introduction
-------------------

Marrs is a Python package for Android Java apps researchers, built on top of tools like ``frida`` and ``adb``.

Using Marrs you can write Python code that modifies fields' value, calls methods, creates instances, hooks methods and more.

Prerequisites
-------------------

1. Python >= 3.7
2. Connected device with USB Debugging enabled (or an Android emulator).
3. Features involving frida require rooted device (``su`` is required).

Installation
-------------------

Using pip:

.. code-block:: bash

    pip install marrs

Or from source:

.. code-block:: bash

    git clone https://github.com/oran1248/marrs.git
    cd marrs
    python setup.py install

Getting started
-------------------
First, import marrs package:

.. code-block:: bash

    import marrs

Second, get your connected device object:

.. code-block:: bash

    device = marrs.get_device()

Now, you can start playing.

For the Device class documentation, please see :py:class:`~marrs.device.Device`.
