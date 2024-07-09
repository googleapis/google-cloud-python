Python Client for Cloud AutoML
==============================

|stable| |pypi| |versions|

`Cloud AutoML`_: **AutoML API Python Client is now available in Vertex AI. Please visit** `Vertex SDK for Python <https://github.com/googleapis/python-aiplatform>`_ **for the new Python Vertex AI client.** Vertex AI is our next generation AI Platform, with many new features that are unavailable in the current platform. `Migrate your resources to Vertex AI <https://cloud.google.com/vertex-ai/docs/start/migrating-to-vertex-ai>`_ to get the latest machine learning features, simplify end-to-end journeys, and productionize models with MLOps. The `Cloud AutoML API <https://cloud.google.com/automl>`_ is a suite of machine learning products that enables developers with limited machine learning expertise to train high-quality models specific to their business needs, by leveraging Google's state-of-the-art transfer learning, and Neural Architecture Search technology.

- `Client Library Documentation`_
- `Product Documentation`_

.. |stable| image:: https://img.shields.io/badge/support-stable-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-automl.svg
   :target: https://pypi.org/project/google-cloud-automl/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-automl.svg
   :target: https://pypi.org/project/google-cloud-automl/
.. _Cloud AutoML: https://cloud.google.com/automl/docs/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/automl/latest/summary_overview
.. _Product Documentation:  https://cloud.google.com/automl/docs/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud AutoML.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud AutoML.:  https://cloud.google.com/automl/docs/
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a virtual environment using `venv`_. `venv`_ is a tool that
creates isolated Python environments. These isolated environments can have separate
versions of Python packages, which allows you to isolate one project's dependencies
from the dependencies of other projects.

With `venv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`venv`: https://docs.python.org/3/library/venv.html


Code samples and snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

Code samples and snippets live in the `samples/`_ folder.

.. _samples/: https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-automl/samples


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Our client libraries are compatible with all current `active`_ and `maintenance`_ versions of
Python.

Python >= 3.7

.. _active: https://devguide.python.org/devcycle/#in-development-main-branch
.. _maintenance: https://devguide.python.org/devcycle/#maintenance-branches

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python <= 3.6

If you are using an `end-of-life`_
version of Python, we recommend that you update as soon as possible to an actively supported version.

.. _end-of-life: https://devguide.python.org/devcycle/#end-of-life-branches

Mac/Linux
^^^^^^^^^

.. code-block:: console

    python3 -m venv <your-env>
    source <your-env>/bin/activate
    pip install google-cloud-automl


Windows
^^^^^^^

.. code-block:: console

    py -m venv <your-env>
    .\<your-env>\Scripts\activate
    pip install google-cloud-automl

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud AutoML
   to see other available methods on the client.
-  Read the `Cloud AutoML Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud AutoML Product documentation:  https://cloud.google.com/automl/docs/
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst
