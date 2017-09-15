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


Subscription Callbacks
----------------------

Because subscriptions in this Pub/Sub client are opened asychronously,
processing the messages that are yielded by the subscription is handled
through **callbacks**.

The basic idea: Define a function that takes one argument; this argument
will be a :class:`~.pubsub_v1.subscriber.message.Message` instance. This
function should do whatever processing is necessary. At the end, the
function should :meth:`~.pubsub_v1.subscriber.message.Message.ack` the
message.

When you call :meth:`~.pubsub_v1.subscriber.policy.thread.Policy.open`, you
must pass the callback that will be used.

Here is an example:

.. code-block:: python

    # Define the callback.
    # Note that the callback is defined *before* the subscription is opened.
    def callback(message):
        do_something_with(message)  # Replace this with your actual logic.
        message.ack()

    # Open the subscription, passing the callback.
    subscription.open(callback)

Explaining Ack
--------------

In Pub/Sub, the term **ack** stands for "acknowledge". You should ack a
message when your processing of that message *has completed*. When you ack
a message, you are telling Pub/Sub that you do not need to see it again.

It might be tempting to ack messages immediately on receipt. While there
are valid use cases for this, in general it is unwise. The reason why: If
there is some error or edge case in your processing logic, and processing
of the message fails, you will have already told Pub/Sub that you successfully
processed the message. By contrast, if you ack only upon completion, then
Pub/Sub will eventually re-deliver the unacknowledged message.

It is also possible to **nack** a message, which is the opposite. When you
nack, it tells Pub/Sub that you are unable or unwilling to deal with the
message, and that the service should redeliver it.


API Reference
-------------

.. toctree::
  :maxdepth: 2

  api/client
  api/policy
  api/message
