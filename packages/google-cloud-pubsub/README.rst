Python Client for Google Cloud Pub / Sub
========================================

    Python idiomatic client for `Google Cloud Pub / Sub`_

.. _Google Cloud Pub / Sub: https://cloud.google.com/pubsub/docs

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/pubsub-usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-pubsub

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Using the API
-------------

Google `Cloud Pub/Sub`_ (`Pub/Sub API docs`_) is designed to provide reliable,
many-to-many, asynchronous messaging between applications. Publisher
applications can send messages to a ``topic`` and other applications can
subscribe to that topic to receive the messages. By decoupling senders and
receivers, Google Cloud Pub/Sub allows developers to communicate between
independently written applications.

.. _Cloud Pub/Sub: https://cloud.google.com/pubsub/docs
.. _Pub/Sub API docs: https://cloud.google.com/pubsub/docs/reference/rest/

See the ``google-cloud-python`` API `Pub/Sub documentation`_ to learn how to connect
to Cloud Pub/Sub using this Client Library.

.. _Pub/Sub documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/pubsub-usage.html

To get started with this API, you'll need to create

.. code:: python

    from google.cloud import pubsub

    client = pubsub.Client()
    topic = client.topic('topic_name')
    topic.create()

    topic.publish('this is the message_payload',
                  attr1='value1', attr2='value2')

.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
   :target: https://pypi.python.org/pypi/google-cloud-pubsub
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-pubsub.svg
   :target: https://pypi.python.org/pypi/google-cloud-pubsub
