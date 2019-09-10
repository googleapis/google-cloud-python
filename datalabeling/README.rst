Python Client for Data Labeling API (`Beta`_)
==============================================



`Data Labeling API`_: Public API for Google Cloud AI Data Labeling Service.

- `Client Library Documentation`_
- `Product Documentation`_

.. _Beta: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
.. _Data Labeling API: https://cloud.google.com/data-labeling
.. _Client Library Documentation: https://googleapis.dev/python/datalabeling/latest
.. _Product Documentation:  https://cloud.google.com/data-labeling/docs/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Data Labeling API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Data Labeling API.:  https://cloud.google.com/data-labeling
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
    <your-env>/bin/pip install google-cloud-datalabeling


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-datalabeling

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Data Labeling API
   API to see other available methods on the client.
-  Read the `Data Labeling API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `repository’s main README`_ to see the full list of Cloud
   APIs that we cover.

.. _Data Labeling API Product documentation:  https://cloud.google.com/data-labeling/docs
.. _repository’s main README: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/README.rst
