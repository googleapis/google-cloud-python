Getting started
===============

google-cloud-trace will allow you to connect to the `Stackdriver Trace API`_ and access all its methods. In order to achieve this, you need to set up authentication as well as install the library locally.

.. _`Stackdriver Trace API`: https://developers.google.com/apis-explorer/?hl=en_US#p/cloudtrace/v1/


Installation
------------


Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Mac/Linux
~~~~~~~~~~

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-trace

Windows
~~~~~~~

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-trace


Using the API
-------------


Authentication
~~~~~~~~~~~~~~

To authenticate all your API calls, first install and setup the `Google Cloud SDK`_.
Once done, you can then run the following command in your terminal:

.. code-block:: console

    $ gcloud beta auth application-default login

or

.. code-block:: console

    $ gcloud auth login

Please see `gcloud beta auth application-default login`_ document for the difference between these commands.

.. _Google Cloud SDK: https://cloud.google.com/sdk/
.. _gcloud beta auth application-default login: https://cloud.google.com/sdk/gcloud/reference/beta/auth/application-default/login
.. code-block:: console

At this point you are all set to continue.


Examples
~~~~~~~~

.. code-block:: python

  from google.cloud.trace import client

  client = client.Client(project_id='your_project_id')

  # Patch traces, traces should be a dict
  client.patch_traces(traces=traces)

  # Get trace
  client.get_trace(trace_id='your_trace_id')

  # List traces
  traces = client.list_traces()

  for trace in traces:
      print trace
