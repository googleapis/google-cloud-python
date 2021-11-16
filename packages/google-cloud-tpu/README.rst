Python Client for Cloud TPU
===========================

|ga| |pypi| |versions|

`Cloud TPU`_: Cloud Tensor Processing Units (TPUs) are Google's custom-developed application-specific 
integrated circuits (ASICs) used to accelerate machine learning workloads. 

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#ga-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-tpu.svg
   :target: https://pypi.org/project/google-cloud-tpu/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-tpu.svg
   :target: https://pypi.org/project/google-cloud-tpu/
.. _Cloud TPU: https://cloud.google.com/tpu
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/tpu/latest
.. _Product Documentation:  https://cloud.google.com/tpu/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Creating a Google Cloud account and a Cloud TPU project.`_
2. `Setup Authentication.`_
3. `Read Cloud TPU Beginner's Guide.`

.. _Creating a Google Cloud account and a Cloud TPU project.: https://cloud.google.com/tpu/docs/setup-gcp-account#creating_a_account_and_a_project
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html
.. _Read Cloud TPU Beginner's Guide.: https://cloud.google.com/tpu/docs/beginners-guide

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
    <your-env>/bin/pip install google-cloud-tpu


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-tpu

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud TPU
   to see other available methods on the client.
-  Read the `Cloud TPU Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud TPU Product documentation:  https://cloud.google.com/tpu/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst