Python Client for Stackdriver Trace API (`Alpha`_)
==================================================================================================

Idiomatic Python client for `Stackdriver Trace API`_

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Stackdriver Trace API: https://cloud.google.com/trace
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/trace-usage
.. _Product Documentation:  https://cloud.google.com/trace

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the monitoring api.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the trace api.:  https://cloud.google.com/trace
.. _Setup Authentication.: https://googlecloudplatform.github.io/google-cloud-python/latest/google-cloud-auth

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install gapic-google-cloud-trace-v1


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install gapic-google-cloud-trace-v1

Fore more information on setting up your Python development environment, such as installing ``pip`` and ``virtualenv`` on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Preview
~~~~~~~

TraceServiceClient
^^^^^^^^^^^^^^^^^^^^^^

.. code:: py

  from google.cloud.gapic.trace.v1 import trace_service_client
  from google.gax import CallOptions, INITIAL_PAGE
  client = trace_service_client.TraceServiceClient()
  project_id = ''

  # Iterate over all results
  for element in client.list_traces(project_id):
      # process element
      pass

  # Or iterate over results one page at a time
  for page in client.list_traces(project_id, options=CallOptions(page_token=INITIAL_PAGE)):
      for element in page:
          # process element
          pass

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Stackdriver Trace API
   API to see other available methods on the client.
-  Read the `Stackdriver Trace API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Stackdriver Trace API Product documentation:  https://cloud.google.com/trace
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
