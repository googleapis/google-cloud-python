Python Client for Stackdriver Monitoring API (`Alpha`_)
=======================================================

`Stackdriver Monitoring API`_: Manages your Stackdriver Monitoring data and configurations. Most projects
must be associated with a Stackdriver account, with a few exceptions as
noted on the individual method pages.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Stackdriver Monitoring API: https://cloud.google.com/monitoring/api/ref_v3/rest/
.. _Client Library Documentation: https://google-cloud-python.readthedocs.io/en/latest/monitoring/
.. _Product Documentation:  https://cloud.google.com/monitoring/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Stackdriver Monitoring API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Stackdriver Monitoring API.:  https://cloud.google.com/monitoring/api/enable-api
.. _Setup Authentication.: http://google-cloud-python.readthedocs.io/en/latest/core/auth.html

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
    <your-env>/bin/pip install google-cloud-monitoring


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-monitoring

Preview
~~~~~~~

MetricServiceClient
^^^^^^^^^^^^^^^^^^^

.. code:: py

    from google.cloud import monitoring_v3

    client = monitoring_v3.MetricServiceClient()

    name = client.project_path('[PROJECT]')


    # Iterate over all results
    for element in client.list_monitored_resource_descriptors(name):
        # process element
        pass

    # Or iterate over results one page at a time
    for page in client.list_monitored_resource_descriptors(name, options=CallOptions(page_token=INITIAL_PAGE)):
        for element in page:
            # process element
            pass

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Stackdriver Monitoring API
   API to see other available methods on the client.
-  Read the `Stackdriver Monitoring API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Stackdriver Monitoring API Product documentation:  https://cloud.google.com/monitoring
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst

Api Reference
-------------
.. toctree::
    :maxdepth: 2

    query.rst
    gapic/v3/api
    gapic/v3/types
