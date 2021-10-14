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
