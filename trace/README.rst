Python Client for Stackdriver Trace API
=======================================

|alpha| |pypi| |versions| 

The `Stackdriver Trace API`_ sends application trace data to Stackdriver Trace
for viewing. Trace data is collected for all App Engine applications by
default. Trace data from other applications can be provided using this API.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-trace.svg
   :target: https://pypi.org/project/google-cloud-trace/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-trace.svg
   :target: https://pypi.org/project/google-cloud-trace/
.. _Stackdriver Trace API: https://cloud.google.com/trace
.. _Client Library Documentation: https://googleapis.dev/python/cloudtrace/latest
.. _Product Documentation:  https://cloud.google.com/trace


Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the trace API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the trace API.:  https://cloud.google.com/trace
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html


Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing
system install permissions, and without clashing with the installed system
dependencies.

.. _virtualenv: https://virtualenv.pypa.io/en/latest/


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
    <your-env>/bin/pip install google-cloud-trace


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-trace

For more information on setting up your Python development environment,
such as installing ``pip`` and ``virtualenv`` on your system, please refer
to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup


Example Usage
~~~~~~~~~~~~~

.. code-block:: python

  from google.cloud.trace import trace_service_client

  client = trace_service_client.TraceServiceClient()
  project_id = 'your-project-123'

  # Iterate over all results
  for element in client.list_traces(project_id):
      # process element
      pass


Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Stackdriver Trace API
   to see other available methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
