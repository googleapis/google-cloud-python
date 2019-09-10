Python Client for Google Cloud Datastore
========================================

|GA| |pypi| |versions| 

`Google Cloud Datastore API`_ is a fully managed, schemaless database for
storing non-relational data. Cloud Datastore automatically scales with your
users and supports ACID transactions, high availability of reads and writes,
strong consistency for reads and ancestor queries, and eventual consistency for
all other queries.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-datastore.svg
   :target: https://pypi.org/project/google-cloud-datastore/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-datastore.svg
   :target: https://pypi.org/project/google-cloud-datastore/
.. _Google Cloud Datastore API: https://cloud.google.com/datastore/docs
.. _Product Documentation:  https://cloud.google.com/datastore/docs
.. _Client Library Documentation: https://googleapis.dev/python/datastore/latest

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Datastore API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Datastore API.:  https://cloud.google.com/datastore
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
    <your-env>/bin/pip install google-cloud-datastore


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-datastore


Example Usage
~~~~~~~~~~~~~

.. code:: python

    from google.cloud import datastore
    # Create, populate and persist an entity with keyID=1234
    client = datastore.Client()
    key = client.key('EntityKind', 1234)
    entity = datastore.Entity(key=key)
    entity.update({
        'foo': u'bar',
        'baz': 1337,
        'qux': False,
    })
    client.put(entity)
    # Then get by key for this entity
    result = client.get(key)
    print(result)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Datastore API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
