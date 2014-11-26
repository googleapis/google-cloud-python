The ``gcloud`` library is ``pip`` install-able:

.. code-block:: console

 	$ pip install gcloud

If you have trouble installing
``pycrypto`` or ``pyopenssl``
(and you're on Ubuntu),
you can try install the precompiled packages:

.. code-block:: console

	$ sudo apt-get install python-crypto python-openssl

If you want to install everything with ``pip``,
try installing the ``dev`` packages beforehand:

.. code-block:: console

	$ sudo apt-get install python-dev libssl-dev

If you want to install `gcloud-python` from source,
you can clone the repository from GitHub:

.. code-block:: console

	$ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
	$ cd gcloud-python
	$ python setup.py install

----