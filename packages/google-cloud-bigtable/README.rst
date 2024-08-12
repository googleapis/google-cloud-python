Python Client for Google Cloud Bigtable
=======================================

|GA| |pypi| |versions| 

`Google Cloud Bigtable`_ is Google's NoSQL Big Data database service. It's the
same database that powers many core Google services, including Search,
Analytics, Maps, and Gmail.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
   :target: https://pypi.org/project/google-cloud-bigtable/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigtable.svg
   :target: https://pypi.org/project/google-cloud-bigtable/
.. _Google Cloud Bigtable: https://cloud.google.com/bigtable
.. _Client Library Documentation: https://googleapis.dev/python/bigtable/latest
.. _Product Documentation:  https://cloud.google.com/bigtable/docs


Async Data Client
-------------------------

:code:`v2.23.0` includes a release of the new :code:`BigtableDataClientAsync` client, accessible at the import path
:code:`google.cloud.bigtable.data`.

The new client brings a simplified API and increased performance using asyncio.
The new client is focused on the data API (i.e. reading and writing Bigtable data), with admin operations
remaining exclusively in the existing synchronous client.

Feedback and bug reports are welcome at cbt-python-client-v3-feedback@google.com,
or through the Github `issue tracker`_.


    .. note::

        It is generally not recommended to use the async client in an otherwise synchronous codebase. To make use of asyncio's
        performance benefits, the codebase should be designed to be async from the ground up.


.. _issue tracker: https://github.com/googleapis/python-bigtable/issues


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Bigtable API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Bigtable API.:  https://cloud.google.com/bigtable
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

Python >= 3.7

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Python 2.7:  the last released version which supported Python 2.7 was
  version 1.7.0, released 2021-02-09.

- Python 3.5:  the last released version which supported Python 3.5 was
  version 1.7.0, released 2021-02-09.

- Python 3.6:  the last released version which supported Python 3.6 was
  version v2.10.1, released 2022-06-03.

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-bigtable


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigtable

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Bigtable API
   to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
