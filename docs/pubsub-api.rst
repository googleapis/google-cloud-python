``gcloud.pubsub`` API
=====================

Connection / Authorization
--------------------------

- Inferred defaults used to create connection if none configured explicitly:

  - credentials (derived from GAE / GCE environ if present).

  - ``project_id`` (derived from GAE / GCE environ if present).

  - ``scopes``


Manage topics for a project
---------------------------

Create a new topic for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.create_topic("topic_name")
   >>> topic.name
   'topic_name'

Create a new topic for an explicit project:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.create_topic("topic_name", project_id="my.project")
   >>> topic.name
   'topic_name'

Fetch an extant topic for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> topic.name
   'topic_name'

Fetch an extant topic for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name', project_id="my.project")
   >>> topic.name
   'topic_name'

Attempt to fetch a non-extant topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> pubsub.get_topic('nonesuch')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NotFound: ...

List extant topics for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> [topic.name for topic in pubsub.list_topics()]
   ['topic_name']

List extant topics for an explicit project:

.. doctest::

   >>> from gcloud import pubsub
   >>> [topic.name for topic in pubsub.list_topics(project_id="my.project")]
   ['topic_name']

Delete a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> topic.delete()


Publish messages to a topic
---------------------------

Publish a single message to a topic, without attributes:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> topic.publish('this is the message_payload')
   <message_id>

Publish a single message to a topic, with attributes:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> topic.publish('this is another message_payload',
   ...               attr1='value1', attr2='value2')
   <message_id>

Publish a set of messages to a topic (as a single request):

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> with topic:
   ...     topic.publish('this is the first message_payload')
   ...     topic.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   [<message_id1>, <message_id2>]


Manage subscriptions to topics
------------------------------

Create a new pull subscription for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.create_subscription('subscription_name')

Create a new pull subscription for a topic with a non-default ACK deadline:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.create_subscription('subscription_name',
   ...                                          ack_deadline=90)

Create a new push subscription for a topic:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.create_subscription('subscription_name',
   ...                                          push_endpoint=ENDPOINT)

Get an extant subscription for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')

Attempt to get a non-extant subscription for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('nonesuch')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NotFound: ...

Update the ACK deadline for a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> subscription.modify_ack_deadline(90)

Convert a pull subscription to push:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> subscription.modify_push_configuration(push_endpoint=ENDPOINT)

Convert a push subscription to pull:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.create_subscription('subscription_name',
   ...                                          push_endpoint=ENDPOINT)
   >>> subscription.modify_push_configuration(push_endpoint=None)

List extant subscriptions for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> [subscription.name for subscription in topic.list_subscriptions()]
   ['subscription_name']

Delete a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> subscription.delete()


Pull messages from a subscription
---------------------------------

Fetch pending messages for a pull subscription (the messages will have
been ACKed already):

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> [message.id for message in subscription.pull()]
   [<message_id1>, <message_id2>, ...]

Fetch a limited number of pending messages for a pull subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> [message.id for message in subscription.pull(max_messages=2)]
   [<message_id1>, <message_id2>]

Fetch messages for a pull subscription without blocking (none pending):

.. doctest::

   >>> from gcloud import pubsub
   >>> topic = pubsub.get_topic('topic_name')
   >>> subscription = topic.get_subscription('subscription_name')
   >>> [message.id for message in subscription.pull(return_immediately=True)]
   []
