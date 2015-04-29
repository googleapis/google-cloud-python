Using the API
=============

Connection / Authorization
--------------------------

- Inferred defaults used to create connection if none configured explicitly:

  - credentials (derived from GAE / GCE environ if present).

  - ``project`` (derived from GAE / GCE environ if present).

  - ``scopes``


Manage topics for a project
---------------------------

Create a new topic for the default project:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> topic.create()  # API request

Create a new topic for an explicit project:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name', project='my.project')
   >>> topic.create()  # API request

Check for the existance of a topic:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> topic.exists()  # API request
   True

List topics for the default project:

.. doctest::

   >>> from gcloud.pubsub import list_topics
   >>> [topic.name for topic in list_topics()]  # API request
   ['topic_name']

List topics for an explicit project:

.. doctest::

   >>> from gcloud.pubsub import list_topics
   >>> topics = list_topics(project='my.project')  # API request
   >>> [topic.name for topic in topics]
   ['topic_name']

Delete a topic:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> topic.delete()  # API request


Publish messages to a topic
---------------------------

Publish a single message to a topic, without attributes:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> topic.publish('this is the message_payload')  # API request
   <message_id>

Publish a single message to a topic, with attributes:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> topic.publish('this is another message_payload',
   ...               attr1='value1', attr2='value2')  # API request
   <message_id>

Publish a set of messages to a topic (as a single request):

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> with topic.batch() as batch:
   ...     batch.publish('this is the first message_payload')
   ...     batch.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> list(batch)
   [<message_id1>, <message_id2>]

.. note::

   The only API request happens during the ``__exit__()`` of the topic
   used as a context manager.


Manage subscriptions to topics
------------------------------

Create a new pull subscription for a topic:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.create()  # API request

Create a new pull subscription for a topic with a non-default ACK deadline:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', ack_deadline=90)
   >>> subscription.create()  # API request

Create a new push subscription for a topic:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', push_endpoint=ENDPOINT)
   >>> subscription.create()  # API request

Check for the existence of a subscription:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.exists()  # API request
   True

Convert a pull subscription to push:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.modify_push_configuration(push_endpoint=ENDPOINT)  # API request

Convert a push subscription to pull:

.. doctest::

   >>> ENDPOINT = 'https://example.com/hook'
   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic,
   ...                             push_endpoint=ENDPOINT)
   >>> subscription.modify_push_configuration(push_endpoint=None)  # API request

List subscriptions for a topic:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> topic = Topic('topic_name')
   >>> subscriptions = topic.list_subscriptions()  # API request
   >>> [subscription.name for subscription in subscriptions]
   ['subscription_name']

List all subscriptions for the default project:

.. doctest::

   >>> from gcloud.pubsub import list_subscriptions
   >>> subscriptions = list_subscriptions()  # API request
   >>> [subscription.name for subscription in subscriptions]
   ['subscription_name']

Delete a subscription:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> subscription.delete()  # API request


Pull messages from a subscription
---------------------------------

Fetch pending messages for a pull subscription:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> with topic:
   ...     topic.publish('this is the first message_payload')
   ...     topic.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> received = subscription.pull()  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.id for message in messages]
   [<message_id1>, <message_id2>]
   >>> [message.data for message in messages]
   ['this is the first message_payload', 'this is the second message_payload']
   >>> [message.attributes for message in messages]
   [{}, {'attr1': 'value1', 'attr2': 'value2'}]

Note that received messages must be acknowledged, or else the back-end
will re-send them later:

.. doctest::

   >>> ack_ids = [recv[0] for recv in received]
   >>> subscription.acknowledge(ack_ids)

Fetch a limited number of pending messages for a pull subscription:

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> with topic:
   ...     topic.publish('this is the first message_payload')
   ...     topic.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> received = subscription.pull(max_messages=1)  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.id for message in messages]

Fetch messages for a pull subscription without blocking (none pending):

.. doctest::

   >>> from gcloud.pubsub import Topic
   >>> from gcloud.pubsub import Subscription
   >>> topic = Topic('topic_name')
   >>> subscription = Subscription('subscription_name', topic)
   >>> received = subscription.pull(max_messages=1)  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.id for message in messages]
   []
