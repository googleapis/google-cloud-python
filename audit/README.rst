Cloud Audit Protobuf Messages
=============================

|alpha| |pypi| |versions| |compat_check_pypi| |compat_check_github|

`Cloud Audit Logs`_: Gain visibility into who did what, when, and where for all user activity on Google Cloud Platform.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-audit.svg
   :target: https://pypi.org/project/google-cloud-audit/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-audit.svg
   :target: https://pypi.org/project/google-cloud-audit/
.. |compat_check_pypi| image:: https://python-compatibility-tools.appspot.com/one_badge_image?package=google-cloud-audit
   :target: https://python-compatibility-tools.appspot.com/one_badge_target?package=google-cloud-audit
.. |compat_check_github| image:: https://python-compatibility-tools.appspot.com/one_badge_image?package=git%2Bgit%3A//github.com/googleapis/google-cloud-python.git%23subdirectory%3Daudit
   :target: https://python-compatibility-tools.appspot.com/one_badge_target?package=git%2Bgit%3A//github.com/googleapis/google-cloud-python.git%23subdirectory%3Daudit
.. _Cloud Audit Logs: https://cloud.google.com/audit-logs/
.. _Client Library Documentation: https://googleapis.github.io/google-cloud-python/latest/audit/index.html
.. _Product Documentation:  https://cloud.google.com/audit-logs/

Quick Start
-----------


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
    <your-env>/bin/pip install google-cloud-audit


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-audit

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Audit Logs
   to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
