Python Client for Cloud AutoML API
==================================

|alpha| |pypi| |versions| 

The `Cloud AutoML API`_ is a suite of machine learning products that enables
developers with limited machine learning expertise to train high-quality models
specific to their business needs, by leveraging Google’s state-of-the-art
transfer learning, and Neural Architecture Search technology.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-automl.svg
   :target: https://pypi.org/project/google-cloud-automl/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-automl.svg
   :target: https://pypi.org/project/google-cloud-automl/
.. _Cloud AutoML API: https://cloud.google.com/automl
.. _Client Library Documentation: https://googleapis.dev/python/automl/latest
.. _Product Documentation:  https://cloud.google.com/automl

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud AutoML API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud AutoML API.:  https://cloud.google.com/automl
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
    <your-env>/bin/pip install google-cloud-automl


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-automl

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

   from google.cloud.automl_v1beta1 import PredictionServiceClient

   client = PredictionServiceClient()
   model_path = client.model_path('my-project-123', 'us-central', 'model-name')
   payload = {...}
   params = {'foo': 1}
   response = client.predict(model_path, payload, params=params)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud AutoML API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.

Making & Testing Local Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to make changes to this library, here is how to set up your
development environment:

1. Make sure you have `virtualenv`_ installed and activated as shown above.
2. Run the following one-time setup (it will be persisted in your virtualenv):

   .. code-block:: console

       pip install -r ../docs/requirements.txt
       pip install -U nox mock pytest

3. If you want to run all tests, you will need a billing-enabled 
   `GCP project`_, and a `service account`_ with access to the AutoML APIs.
   Note: the first time the tests run in a new project it will take a _long_
   time, on the order of 2-3 hours. This is one-time setup that will be skipped
   in future runs.

.. _service account: https://cloud.google.com/iam/docs/creating-managing-service-accounts
.. _GCP project: https://cloud.google.com/resource-manager/docs/creating-managing-projects

.. code-block:: console

    export PROJECT_ID=<project-id> GOOGLE_APPLICATION_CREDENTIALS=</path/to/creds.json>
    nox

