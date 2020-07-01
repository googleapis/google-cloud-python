Python Client for Stackdriver Logging
=====================================

|pypi| |versions|

`Stackdriver Logging API`_: Writes log entries and manages your Stackdriver
Logging configuration.

- `Client Library Documentation`_
- `Product Documentation`_

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-logging.svg
   :target: https://pypi.org/project/google-cloud-logging/
.. _Stackdriver Logging API: https://cloud.google.com/logging
.. _Client Library Documentation: https://googleapis.dev/python/logging/latest
.. _Product Documentation:  https://cloud.google.com/logging/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Stackdriver Logging API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Stackdriver Logging API.:  https://cloud.google.com/logging
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `venv`_ using pip. `venv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `venv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`venv`: https://docs.python.org/3/library/venv.html


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.5

Deprecated Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7. Python 2.7 support was removed on January 1, 2020.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-logging


Windows
^^^^^^^

.. code-block:: console

    python -m venv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-logging

Using the API
-------------

.. code:: python

    from google.cloud import logging_v2
    client = logging_v2.LoggingServiceV2Client()

    resource = {
        "type": "global",
        "labels": {
            "project_id": "[PROJECT_ID]"
        }
    }

    """
    Log entries can be either LogEntry or dict.
    You can describe the same data in the following format:

    e = {
        "log_name": "projects/[PROJECT_ID]/logs/test-logging",
        "resource": resource,
        "text_payload": "this is a log statement",
    }
    """
    e = logging_v2.types.LogEntry(
        log_name="projects/[PROJECT_ID]/logs/test-logging", # optional
        resource=resource, # optional
        text_payload="this is a log statement")

    entries = [e]
    response = client.write_log_entries(entries)

.. code:: python

    from google.cloud import logging
    client = logging.Client()
    logger = client.logger('log_name')
    logger.log_text('A simple entry')  # API call

Example of fetching entries:

.. code:: python

    from google.cloud import logging
    client = logging.Client()
    logger = client.logger('log_name')
    for entry in logger.list_entries():
        print(entry.payload)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for to see other available
   methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
