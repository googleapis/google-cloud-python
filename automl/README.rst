Python Client for Cloud AutoML API (`Alpha`_)
=============================================

The `Cloud AutoML API`_ is a suite of machine learning products that enables
developers with limited machine learning expertise to train high-quality models
specific to their business needs, by leveraging Google’s state-of-the-art
transfer learning, and Neural Architecture Search technology.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Alpha: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Cloud AutoML API: https://cloud.google.com/automl
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/automl/index.html
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
.. _Setup Authentication.: https://googlecloudplatform.github.io/google-cloud-python/latest/core/auth.html

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
