Python Client for Google Cloud Bigtable
=======================================

|beta| |pypi| |versions| 

`Google Cloud Bigtable`_ is Google's NoSQL Big Data database service. It's the
same database that powers many core Google services, including Search,
Analytics, Maps, and Gmail.

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-silver.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigtable.svg
   :target: https://pypi.org/project/google-cloud-bigtable/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigtable.svg
   :target: https://pypi.org/project/google-cloud-bigtable/
.. _Google Cloud Bigtable: https://cloud.google.com/bigtable
.. _Client Library Documentation: https://googleapis.dev/python/bigtable/latest
.. _Product Documentation:  https://cloud.google.com/bigtable/docs

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
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support will be removed on January 1, 2020.


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

``google-cloud-happybase``
--------------------------

In addition to the core ``google-cloud-bigtable``, we provide a
`google-cloud-happybase
<http://google-cloud-python-happybase.readthedocs.io/en/latest/>`__ library
with the same interface as the popular `HappyBase
<https://happybase.readthedocs.io/en/latest/>`__ library. Unlike HappyBase,
``google-cloud-happybase`` uses ``google-cloud-bigtable`` under the covers,
rather than Apache HBase.
