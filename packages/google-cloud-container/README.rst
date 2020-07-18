Python Client for Google Kubernetes Engine API
==============================================

|ga| |pypi| |versions|

`Google Kubernetes Engine API`_: The Google Kubernetes Engine API is used for
building and managing container based applications, powered by the open source
Kubernetes technology.

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#ga-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
   :target: https://pypi.org/project/google-cloud-container/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-container.svg
   :target: https://pypi.org/project/google-cloud-container/
.. _Google Kubernetes Engine API: https://cloud.google.com/kubernetes-engine
.. _Client Library Documentation: https://googleapis.dev/python/container/latest
.. _Product Documentation:  https://cloud.google.com/kubernetes-engine

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the Google Container Engine API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the Google Container Engine API.:  https://cloud.google.com/container
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-container==1.0.1


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-container


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-container


Next Steps
~~~~~~~~~~

-  Read the `Client API Documentation`_ to see other available methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.

.. _Client API Documentation: https://googleapis.dev/python/container/latest
