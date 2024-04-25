IPython Magics for BigQuery
===========================

|GA| |pypi| |versions|

Querying massive datasets can be time consuming and expensive without the
right hardware and infrastructure. Google `BigQuery`_ solves this problem by
enabling super-fast, SQL queries against append-mostly tables, using the
processing power of Google's infrastructure.

-  `Client Library Documentation`_
-  `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. _BigQuery: https://cloud.google.com/bigquery/what-is-bigquery
.. _Client Library Documentation: https://googleapis.dev/python/bigquery/latest
.. _Product Documentation: https://cloud.google.com/bigquery/docs/reference/v2/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud BigQuery API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud BigQuery API.:  https://cloud.google.com/bigquery
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

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7, Python == 3.5, Python == 3.6.

The last version of this library compatible with Python 2.7 and 3.5 is
`google-cloud-bigquery==1.28.0`.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install bigquery-magics


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install bigquery-magics