#######
Pub/Sub
#######

`Google Cloud Pub/Sub`_ is a fully-managed real-time messaging service that
allows you to send and receive messages between independent applications. You
can leverage Cloud Pub/Sub’s flexibility to decouple systems and components
hosted on Google Cloud Platform or elsewhere on the Internet. By building on
the same technology Google uses, Cloud Pub/Sub is designed to provide “at
least once” delivery at low latency with on-demand scalability to 1 million
messages per second (and beyond).

.. _Google Cloud Pub/Sub: https://cloud.google.com/pubsub/

********************************
Authentication and Configuration
********************************

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`/core/auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd
  like to interact with. If the :envvar:`GOOGLE_CLOUD_PROJECT` environment
  variable is not present, the project ID from JSON file credentials is used.

  If you are using Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`~google.cloud.pubsub_v1.PublisherClient` or
  :class:`~google.cloud.pubsub_v1.SubscriberClient`.

.. code-block:: python

     >>> from google.cloud import pubsub
     >>> publisher = pubsub.PublisherClient()
     >>> subscriber = pubsub.SubscriberClient()

or pass in ``credentials`` explicitly.

.. code-block:: python

     >>> from google.cloud import pubsub
     >>> client = pubsub.PublisherClient(
     ...     credentials=creds,
     ... )

**********
Publishing
**********

To publish data to Cloud Pub/Sub you must create a topic, and then publish
messages to it

.. code-block:: python

    >>> import os
    >>> from google.cloud import pubsub
    >>>
    >>> publisher = pubsub.PublisherClient()
    >>> topic = 'projects/{project_id}/topics/{topic}'.format(
    ...     project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    ...     topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    ... )
    >>> publisher.create_topic(topic)  # raises conflict if topic exists
    >>> publisher.publish(topic, b'My first message!', spam='eggs')

To learn more, consult the :doc:`publishing documentation <publisher/index>`.


***********
Subscribing
***********

To subscribe to data in Cloud Pub/Sub, you create a subscription based on
the topic, and subscribe to that.

.. code-block:: python

    >>> import os
    >>> from google.cloud import pubsub
    >>>
    >>> subscriber = pubsub.SubscriberClient()
    >>> topic = 'projects/{project_id}/topics/{topic}'.format(
    ...     project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    ...     topic='MY_TOPIC_NAME',  # Set this to something appropriate.
    ... )
    >>> subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    ...     project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    ...     sub='MY_SUBSCRIPTION_NAME',  # Set this to something appropriate.
    ... )
    >>> subscription = subscriber.create_subscription(subscription_name, topic)

The subscription is opened asychronously, and messages are processed by
use of a callback.

.. code-block:: python

    >>> def callback(message):
    ...     print(message.data)
    ...     message.ack()
    >>> subscription.open(callback)

To learn more, consult the :doc:`subscriber documentation <subscriber/index>`.


**********
Learn More
**********

.. toctree::
  :maxdepth: 3

  publisher/index
  subscriber/index
  types
