Python Client for Network Connectivity Center
=================================================

|alpha| |pypi| |versions|

`Network Connectivity Center`_: The Network Connectivity API will be home
to various services which provide information pertaining to network connectivity. 
This includes information like interconnects, VPNs, VPCs, routing information, ip
address details, etc. This information will help customers verify their
network configurations and helps them to discover misconfigurations,
inconsistencies, etc.

- `Client Library Documentation`_
- `Product Documentation`_

.. |alpha| image:: https://img.shields.io/badge/support-alpha-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#alpha-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-network-connectivity.svg
   :target: https://pypi.org/project/google-cloud-network-connectivity/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-network-connectivity.svg
   :target: https://pypi.org/project/google-cloud-network-connectivity/
.. _Network Connectivity Center: https://cloud.google.com/network-connectivity/
.. _Client Library Documentation: https://googleapis.dev/python/networkconnectivity/latest
.. _Product Documentation:  https://cloud.google.com/network-connectivity/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Network Connectivity Center.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Network Connectivity Center.:  https://cloud.google.com/network-connectivity/docs
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
    <your-env>/bin/pip install google-cloud-network-connectivity


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-network-connectivity

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Network Connectivity Center
   to see other available methods on the client.
-  Read the `Network Connectivity Center Product documentation`_ to learn
   more about the product and see How-to Guides.
-  View this `README`_ to see the full list of Cloud
   APIs that we cover.

.. _Network Connectivity Center Product documentation:  https://cloud.google.com/network-connectivity/docs
.. _README: https://github.com/googleapis/google-cloud-python/blob/master/README.rst
