Python Client for Google Container Engine API
=============================================

|alpha| |pypi| |versions|

`Google Container Engine API`_: The Google Kubernetes Engine API is used for building and managing container
based applications, powered by the open source Kubernetes technology.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-container.svg
   :target: https://pypi.org/project/google-cloud-container/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-container.svg
   :target: https://pypi.org/project/google-cloud-container/
.. _Google Container Engine API: https://cloud.google.com/container
.. _Client Library Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/container/index.html
.. _Product Documentation:  https://cloud.google.com/container

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable the Google Container Engine API.`_
3. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable the Google Container Engine API.:  https://cloud.google.com/container
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
    <your-env>/bin/pip install google-cloud-container


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-container

Example Usage
~~~~~~~~~~~~~

.. code:: py

    from google.cloud import container_v1

    client = container_v1.ClusterManagerClient()

    project_id = ''
    zone = ''

    response = client.list_clusters(project_id, zone)

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Container Engine API
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn more about the product and see
   How-to Guides.
