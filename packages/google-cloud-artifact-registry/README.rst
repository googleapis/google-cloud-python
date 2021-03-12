Python Client for Artifact Registry
=================================================

|beta| |pypi| |versions|

`Artifact Registry`_: is a single place for your organization
to manage container images and language packages (such as Maven and npm). It is
fully integrated with Google Cloud’s tooling and runtimes and comes with support
for native artifact protocols. This makes it simple to integrate it with your
CI/CD tooling to set up automated pipelines.

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-artifact-registry.svg
   :target: https://pypi.org/project/google-cloud-artifact-registry/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-artifact-registry.svg
   :target: https://pypi.org/project/google-cloud-artifact-registry/
.. _Artifact Registry: https://cloud.google.com/artifact-registry
.. _Client Library Documentation: https://googleapis.dev/python/artifactregistry/latest
.. _Product Documentation:  https://cloud.google.com/artifact-registry

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Artifact Registry.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Artifact Registry.:  https://cloud.google.com/artifact-registry/docs/enable-service
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


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-artifact-registry


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-artifact-registry

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Artifact Registry
   to see other available methods on the client.
-  Read the `Artifact Registry Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Artifact Registry Product documentation:  https://cloud.google.com/artifact-registry/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
