Python Client for Stackdriver Error Reporting
=============================================

    Python idiomatic client for `Stackdriver Error Reporting`_

.. _Stackdriver Error Reporting: https://cloud.google.com/error-reporting/

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/error-reporting/usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-error-reporting

Fore more information on setting up your Python development environment, such as installing ``pip`` and on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Using the API
-------------

The Stackdriver `Error Reporting`_ API (`Error Reporting API docs`_)
counts, analyzes and aggregates the crashes in your running cloud services.
A centralized error management interface displays the results with sorting
and filtering capabilities. A dedicated view shows the error details: time
chart, occurrences, affected user count, first and last seen dates and a
cleaned exception stack trace. Opt-in to receive email and mobile alerts
on new errors.

.. _Error Reporting: https://cloud.google.com/error-reporting/
.. _Error Reporting API docs: https://cloud.google.com/error-reporting/reference/

See the ``google-cloud-python`` API Error Reporting `Documentation`_ to learn
how to get started using this library.

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-error-reporting.svg
   :target: https://pypi.org/project/google-cloud-error-reporting/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-error-reporting.svg
   :target: https://pypi.org/project/google-cloud-error-reporting/
