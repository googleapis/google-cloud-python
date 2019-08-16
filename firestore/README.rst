Python Client for Google Cloud Firestore
========================================

|beta| |pypi| |versions| 

The `Google Cloud Firestore`_ API is a flexible, scalable
database for mobile, web, and server development from Firebase and Google
Cloud Platform. Like Firebase Realtime Database, it keeps your data in
sync across client apps through realtime listeners and offers offline support
for mobile and web so you can build responsive apps that work regardless of
network latency or Internet connectivity. Cloud Firestore also offers seamless
integration with other Firebase and Google Cloud Platform products,
including Cloud Functions.

-  `Product Documentation`_
-  `Client Library Documentation`_

.. |beta| image:: https://img.shields.io/badge/support-beta-silver.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#beta-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-firestore.svg
   :target: https://pypi.org/project/google-cloud-firestore/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-firestore.svg
.. _Google Cloud Firestore: https://cloud.google.com/firestore/
.. _Product Documentation: https://cloud.google.com/firestore/docs/
.. _Client Library Documentation: https://googleapis.dev/python/firestore/latest

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Firestore API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Firestore API.:  https://cloud.google.com/firestore
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
    <your-env>/bin/pip install google-cloud-firestore


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-firestore


Example Usage
~~~~~~~~~~~~~

.. code:: python

    from google.cloud import firestore

    # Add a new document
    db = firestore.Client()
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

    # Then query for documents
    users_ref = db.collection(u'users')
    docs = users_ref.get()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Firestore API
   API to see other available methods on the client.
-  Read the `Product Documentation`_ to learn
   more about the product and see How-to Guides.
