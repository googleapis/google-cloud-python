Python Client for Google Cloud Pub / Sub
========================================

    Python idiomatic client for `Google Cloud Pub / Sub`_

.. _Google Cloud Pub / Sub: https://cloud.google.com/pubsub/docs

|pypi| |versions|

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/latest/pubsub/

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-pubsub

For more information on setting up your Python development environment,
such as installing ``pip`` and ``virtualenv`` on your system, please refer
to `Python Development Environment Setup Guide`_ for Google Cloud Platform.

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

.. _Pub/Sub documentation: http://google-cloud-python.readthedocs.io/en/latest/pubsub/index.html


Publishing
----------

To publish data to Cloud Pub/Sub you must create a topic, and then publish
messages to it

.. code-block:: python

    import os
    from google.cloud import pubsub

    publisher = pubsub.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    )
    publisher.create_topic(topic_name)
    publisher.publish(topic_name, b'My first message!', spam='eggs')

To learn more, consult the `publishing documentation`_.

.. _publishing documentation: http://google-cloud-python.readthedocs.io/en/latest/pubsub/publisher/index.html


Subscribing
-----------

To subscribe to data in Cloud Pub/Sub, you create a subscription based on
the topic, and subscribe to that.

.. code-block:: python

    import os
    from google.cloud import pubsub

    subscriber = pubsub.SubscriberClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    )
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        sub='MY_SUBSCRIPTION_NAME',  # Set this to something appropriate.
    )
    subscriber.create_subscription(
        name=subscription_name, topic=topic_name)
    subscription = subscriber.subscribe(subscription_name)

The subscription is opened asychronously, and messages are processed by
use of a callback.

.. code-block:: python

    def callback(message):
        print(message.data)
        message.ack()
    subscription.open(callback)

To learn more, consult the `subscriber documentation`_.

.. _subscriber documentation: http://google-cloud-python.readthedocs.io/en/latest/pubsub/subscriber/index.html


.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-pubsub.svg
   :target: https://pypi.org/project/google-cloud-pubsub/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-pubsub.svg
   :target: https://pypi.org/project/google-cloud-pubsub/
