Pandas Data Types for SQL systems (BigQuery, Spanner)
=====================================================

|beta| |pypi| |versions|

`Pandas extension data types`_ for data from SQL systems such as `BigQuery`_.

- `Library Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/db-dtypes.svg
   :target: https://pypi.org/project/db-dtypes/
.. |versions| image:: https://img.shields.io/pypi/pyversions/db-dtypes.svg
   :target: https://pypi.org/project/db-dtypes/
.. _Pandas extension data types: https://pandas.pydata.org/pandas-docs/stable/ecosystem.html#ecosystem-extensions
.. _BigQuery: https://cloud.google.com/bigquery/docs/
.. _Library Documentation: https://googleapis.dev/python/db-dtypes/latest


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. [Optional] `Enable billing for your project.`_
3. `Enable the BigQuery Storage API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the BigQuery Storage API.: https://console.cloud.google.com/apis/library/bigquery.googleapis.com
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
------------

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
Python <= 3.5.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install db-dtypes


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install db-dtypes
