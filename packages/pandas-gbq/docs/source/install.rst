Installation
============

You can install pandas-gbq with ``conda``, ``pip``, or by installing from source.

Conda
-----

.. code-block:: shell

   $ conda install pandas-gbq --channel conda-forge

This installs pandas-gbq and all common dependencies, including ``pandas``.

Pip
---

To install the latest version of pandas-gbq: from the

.. code-block:: shell

    $ pip install pandas-gbq -U

This installs pandas-gbq and all common dependencies, including ``pandas``.


Install from Source
-------------------

.. code-block:: shell

    $ pip install git+https://github.com/pydata/pandas-gbq.git


Dependencies
------------

This module requires following additional dependencies:

- `httplib2 <https://github.com/httplib2/httplib2>`__: HTTP client
- `google-api-python-client <http://github.com/google/google-api-python-client>`__: Google's API client
- `oauth2client <https://github.com/google/oauth2client>`__: authentication and authorization for Google's API
