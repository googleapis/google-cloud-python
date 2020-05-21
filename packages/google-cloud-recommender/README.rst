Python Client for Recommender API
=================================

|ga| |pypi| |versions|

`Recommender API`_: Recommender provides recommendations for using resources on Google Cloud.
These recommendations are per-product or per-service, and are generated based on heuristic methods,
machine learning, and current resource usage.

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-recommender.svg
   :target: https://pypi.org/project/google-cloud-recommender/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-recommender.svg
   :target: https://pypi.org/project/google-cloud-recommender/
.. _Recommender API: https://cloud.google.com/recommender
.. _Client Library Documentation: https://googleapis.dev/python/recommender/latest
.. _Product Documentation:  https://cloud.google.com/recommender/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Recommender API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Recommender API.:  https://cloud.google.com/recommender
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


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-recommender


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-recommender

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Recommender API
   API to see other available methods on the client.
-  Read the `Recommender API Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Recommender API Product documentation:  https://cloud.google.com/recommender
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
