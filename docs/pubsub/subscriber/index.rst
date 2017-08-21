Subscribing to Messages
=======================

Subscribing to messages is handled through the
:class:`~.pubsub_v1.subscriber.client.Client` class (aliased as
``google.cloud.pubsub.SubscriberClient``). This class provides a
:meth:`~.pubsub_v1.subscriber.client.Client.subscribe` method to
attach to subscriptions on existing topics,  and (most importantly) a
:meth:`~.pubsub_v1.subscriber.policy.thread.Policy.open` method that
consumes messages from Pub/Sub.

Instantiating a subscriber client is straightforward:

.. code-block:: python

    from google.cloud import pubsub
    subscriber = pubsub.SubscriberClient()


Creating a Subscription
-----------------------

In Pub/Sub, a **subscription** is a discrete pull of messages from a topic.
If multiple clients pull the same subscription, then messages are split
between them. If multiple clients create a subscription each, then each client
will get every message.

.. note::

    Remember that Pub/Sub operates under the principle of "everything at least
    once". Even in the case where multiple clients pull the same subscription,
    *some* redundancy is likely.

Creating a subscription requires that you already know what topic you want
to subscribe to, and it must already exist. Once you have that, it is easy:

.. code-block:: python

    # Substitute {project}, {topic}, and {subscription} with appropriate
    # values for your application.
    topic_name = 'projects/{project}/topics/{topic}'
    sub_name = 'projects/{project}/subscriptions/{subscription}'
    subscriber.create_subscription(topic_name, sub_name)


Pulling a Subscription
----------------------

Once you have created a subscription (or if you already had one), the next
step is to pull data from it. This entails two steps: first you must call
:meth:`~.pubsub_v1.subscriber.client.Client.subscribe`, passing in the
subscription string.

.. code-block:: python

    # As before, substitute {project} and {subscription} with appropriate
    # values for your application.
    subscription = subscriber.subscribe(
        'projects/{project}/subscriptions/{subscription}',
    )

This will return an object with an
:meth:`~.pubsub_v1.subscriber.policy.thread.Policy.open` method; calling
this method will actually begin consumption of the subscription.


Learn More
----------

.. toctree::
  :maxdepth: 2

  api/client
  api/policy
  api/message
