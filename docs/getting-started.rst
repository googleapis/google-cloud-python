Getting started with gcloud
===========================

Installing gcloud
-----------------

The ``gcloud`` library is ``pip`` install-able::

  $ pip install gcloud

If you have trouble installing
``pycrypto`` or ``pyopenssl``
(and you're on Ubuntu),
you can try install the precompiled packages::

  $ sudo apt-get install python-crypto python-openssl

If you want to install everything with ``pip``,
try installing the ``dev`` packages beforehand::

  $ sudo apt-get install python-dev libssl-dev

If you want to install `gcloud-python` from source,
you can clone the repository from GitHub::

  $ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
  $ cd gcloud-python
  $ python setup.py install
