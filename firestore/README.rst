Python Client for Google Cloud Firestore
========================================

    Python idiomatic client for `Cloud Firestore`_

.. _Cloud Firestore: https://cloud.google.com/firestore/docs/

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-firestore

Fore more information on setting up your Python development environment, such as installing ``pip`` and on your system, please refer to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

.. _Python Development Environment Setup Guide: https://cloud.google.com/python/setup

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: https://google-cloud-python.readthedocs.io/en/latest/core/auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/google-cloud-common/tree/master/authentication

Using the API
-------------

`Cloud Firestore`_ (`Firestore API docs`_) is a flexible, scalable
database for mobile, web, and server development from Firebase and Google
Cloud Platform. Like Firebase Realtime Database, it keeps your data in
sync across client apps through realtime listeners and offers offline support
for mobile and web so you can build responsive apps that work regardless of
network latency or Internet connectivity. Cloud Firestore also offers seamless
integration with other Firebase and Google Cloud Platform products,
including Cloud Functions.

.. _Firestore API docs: https://cloud.google.com/firestore/docs/

See the ``google-cloud-python`` API `firestore documentation`_ to learn how to
interact with the Cloud Firestore using this Client Library.

.. _firestore documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html

See the `official Cloud Firestore documentation`_ for more details on
how to activate Cloud Firestore for your project.

.. _official Cloud Firestore documentation: https://cloud.google.com/firestore/docs/

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
