Python Client for BigQuery Storage API
======================================

|ga| |pypi| |versions| 

`BigQuery Storage API`_:

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery-storage.svg
   :target: https://pypi.org/project/google-cloud-bigquery-storage/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery-storage.svg
   :target: https://pypi.org/project/google-cloud-bigquery-storage/
.. _BigQuery Storage API: https://cloud.google.com/bigquery/docs/reference/storage/
.. _Client Library Documentation: https://googleapis.dev/python/bigquerystorage/latest
.. _Product Documentation: https://cloud.google.com/bigquery/docs/reference/storage/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the BigQuery Storage API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the BigQuery Storage API.: https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com
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

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7, Python == 3.5.

The last version of this library compatible with Python 2.7 and 3.5 is
``google-cloud-bigquery-storage==1.1.0``.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-bigquery-storage


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigquery-storage

Optional Dependencies
^^^^^^^^^^^^^^^^^^^^^

Several features of ``google-cloud-bigquery-storage`` require additional
dependencies.

* Parse Arrow blocks in a ``read_rows()`` stream using `pyarrow
  <https://arrow.apache.org/docs/python/>`_.

  ``pip install 'google-cloud-bigquery-storage[pyarrow]'``
  

* Parse Avro blocks in a ``read_rows()`` stream using `fastavro
  <https://fastavro.readthedocs.io/en/latest/>`_.

  ``pip install google-cloud-bigquery-storage[fastavro]``

* Download rows to a `pandas <http://pandas.pydata.org/pandas-docs/stable/>`_
  dataframe.

  ``pip install 'google-cloud-bigquery-storage[pandas,pyarrow]'``

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for BigQuery Storage API
   API to see other available methods on the client.
-  Read the `BigQuery Storage API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _BigQuery Storage API Product documentation:  https://cloud.google.com/bigquery/docs/reference/storage/
.. _repository’s main README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
