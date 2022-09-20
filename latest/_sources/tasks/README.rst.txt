Python Client for Cloud Tasks API
=================================

|GA| |pypi| |versions| 

`Cloud Tasks API`_: Manages the execution of large numbers of distributed
requests.

- `Client Library Documentation`_
- `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-tasks.svg
   :target: https://pypi.org/project/google-cloud-tasks/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-tasks.svg
   :target: https://pypi.org/project/google-cloud-tasks/
.. _Cloud Tasks API: https://cloud.google.com/tasks
.. _Client Library Documentation: https://googleapis.dev/python/cloudtasks/latest
.. _Product Documentation:  https://cloud.google.com/tasks

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Cloud Tasks API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Cloud Tasks API.:  https://console.cloud.google.com/apis/library/cloudtasks.googleapis.com
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
    <your-env>/bin/pip install google-cloud-tasks


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-tasks

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud Tasks API
   to see other available methods on the client.
-  Read the `Cloud Tasks API Product documentation`_ to learn
   more about the product and see How-to Guides.

.. _Cloud Tasks API Product documentation:  https://cloud.google.com/tasks
