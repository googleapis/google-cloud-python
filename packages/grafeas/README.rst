Python Client for Grafeas API
=============================

|ga| |pypi| |versions|

`Grafeas API`_: An implementation of the Grafeas API, which stores, and enables querying and
retrieval of critical metadata about all of your software artifacts.

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/grafeas.svg
   :target: https://pypi.org/project/grafeas/
.. |versions| image:: https://img.shields.io/pypi/pyversions/grafeas.svg
   :target: https://pypi.org/project/grafeas/
.. _Grafeas API: https://grafeas.io/
.. _Client Library Documentation: https://googleapis.dev/python/grafeas/latest
.. _Product Documentation:  https://grafeas.io/

Installation
--------------

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.7

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7, Python == 3.6.

The last version of this library compatible with Python 2.7 is grafeas==0.4.1.

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install grafeas


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install grafeas

Next Steps
--------------

-  Read the `Client Library Documentation`_ for Grafeas API
   API to see other available methods on the client.
-  Read the `Grafeas API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Grafeas API Product documentation:  https://grafeas.io/
.. _repository’s main README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
