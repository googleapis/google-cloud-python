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

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> topic.create()  # API request

Create a new topic for an explicit project:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name', project_id='my.project')
   >>> topic.create()  # API request

Check for the existance of a topic:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> topic.exists()  # API request
   True

List topics for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> [topic.name for topic in pubsub.list_topics()]  # API request
   ['topic_name']

List topics for an explicit project:

.. doctest::

   >>> from gcloud import pubsub
   >>> topics = pubsub.list_topics(project_id='my.project')  # API request
   >>> [topic.name for topic in topics]
   ['topic_name']

Delete a topic:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> topic.delete()  # API request


Publish messages to a topic
---------------------------

Publish a single message to a topic, without attributes:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> topic.publish('this is the message_payload')  # API request
   <message_id>

Publish a single message to a topic, with attributes:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> topic.publish('this is another message_payload',
   ...               attr1='value1', attr2='value2')  # API request
   <message_id>

Publish a set of messages to a topic (as a single request):

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> with topic as batch:
   ...     topic.publish('this is the first message_payload')
   ...     topic.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> batch
   [<message_id1>, <message_id2>]

.. note::

   The only API request happens during the ``__exit__()`` of the topic
   used as a context manager.


Manage subscriptions to topics
------------------------------

Create a new pull subscription for a topic:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.create()  # API request

Create a new pull subscription for a topic with a non-default ACK deadline:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', ack_deadline=90)
   >>> subscription.create()  # API request

Create a new push subscription for a topic:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', push_endpoint=ENDPOINT)
   >>> subscription.create()  # API request

Check for the existence of a subscription:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.exists()  # API request
   True

Convert a pull subscription to push:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.modify_push_configuration(push_endpoint=ENDPOINT)  # API request

Convert a push subscription to pull:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic,
   ...                             push_endpoint=ENDPOINT)
   >>> subscription.modify_push_configuration(push_endpoint=None)  # API request

List subscriptions for a topic:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> topic = Topic('topic_name')
   >>> subscriptions = topic.list_subscriptions()  # API request
   >>> [subscription.name for subscription in subscriptions]
   ['subscription_name']

Delete a subscription:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.delete()  # API request


Pull messages from a subscription
---------------------------------

Fetch pending messages for a pull subscription

.. note::

   The messages will have been ACKed already.

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> [message.id for message in subscription.pull()]
   [<message_id1>, <message_id2>, ...]

Fetch a limited number of pending messages for a pull subscription:

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> [message.id for message in subscription.pull(max_messages=2)]
   [<message_id1>, <message_id2>]

Fetch messages for a pull subscription without blocking (none pending):

.. doctest::

   >>> from gcloud.pubsub.topic import Topic
   >>> from gcloud.pubsub.subscription import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> [message.id for message in subscription.pull(return_immediately=True)]
   []

