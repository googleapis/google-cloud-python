Python Client for Cloud IDS
===========================

|beta| |pypi| |versions|

`Cloud IDS`_: is an intrusion detection service that provides threat detection for intrusions, 
malware, spyware, and command-and-control attacks on your network. Cloud IDS works by creating
a Google-managed peered network with mirrored VMs. Traffic in the peered network is mirrored,
and then inspected by Palo Alto Networks threat protection technologies to provide advanced
threat detection. 

- `Client Library Documentation`_
- `Product Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-ids.svg
   :target: https://pypi.org/project/google-cloud-ids/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-ids.svg
   :target: https://pypi.org/project/google-cloud-ids/
.. _Cloud IDS: https://cloud.google.com/intrusion-detection-system
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/ids/latest
.. _Product Documentation:  https://cloud.google.com/intrusion-detection-system/docs

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Set up IAM permissions.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Set up IAM permissions.:  https://cloud.google.com/intrusion-detection-system/docs/configuring-ids
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
    <your-env>/bin/pip install google-cloud-ids


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-ids

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Cloud IDS
   to see other available methods on the client.
-  Read the `Cloud IDS Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Cloud IDS Product documentation:  https://cloud.google.com/intrusion-detection-system
.. _README: https://github.com/googleapis/google-cloud-python/blob/main/README.rst