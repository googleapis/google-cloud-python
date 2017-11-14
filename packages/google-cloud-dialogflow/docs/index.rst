Python Client for Dialogflow API (`Beta`_)
===========================================

`Dialogflow API`_: Dialogflow is an enterprise-grade NLU platform that makes it easy for
developers to design and integrate conversational user interfaces into
mobile apps, web applications, devices, and bots.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Beta: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Dialogflow API: https://cloud.google.com/dialogflow
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/dialogflow-usage
.. _Product Documentation:  https://cloud.google.com/dialogflow

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the Dialogflow API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the Dialogflow API.:  https://cloud.google.com/dialogflow
.. _Setup Authentication.: https://googlecloudplatform.github.io/google-cloud-python/stable/google-cloud-auth

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
    <your-env>/bin/pip install dialogflow


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install dialogflow

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Dialogflow API
   API to see other available methods on the client.
-  Read the `Dialogflow API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Dialogflow API Product documentation:  https://cloud.google.com/dialogflow
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst

Api Reference
-------------
.. toctree::
    :maxdepth: 2

    gapic/v2beta1/api
    gapic/v2beta1/types
