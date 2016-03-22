Using the API
=============

Authentication / Configuration
------------------------------

- Use :class:`Client <gcloud.pubsub.client.Client>` objects to configure
  your applications.

- :class:`Client <gcloud.pubsub.client.Client>` objects hold both a ``project``
  and an authenticated connection to the PubSub service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <gcloud.pubsub.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <gcloud.pubsub.client.Client.from_service_account_p12>`.

- After setting ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables, create a :class:`Client <gcloud.pubsub.client.Client>`

  .. doctest::

     >>> from gcloud import pubsub
     >>> client = pubsub.Client()


Manage topics for a project
---------------------------

Create a new topic for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.create()  # API request

Check for the existence of a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.exists()  # API request
   True

List topics for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topics, next_page_token = client.list_topics()  # API request
   >>> [topic.name for topic in topics]
   ['topic_name']

Delete a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.delete()  # API request

Fetch the IAM policy for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> policy = topic.get_iam_policy()  # API request
   >>> policy.etag
   'DEADBEEF'
   >>> policy.owners
   ['user:phred@example.com']
   >>> policy.writers
   ['systemAccount:abc-1234@systemaccounts.example.com']
   >>> policy.readers
   ['domain:example.com']

Update the IAM policy for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> policy = topic.get_iam_policy()  # API request
   >>> policy.writers.add(policy.group('editors-list@example.com'))
   >>> topic.set_iam_policy(policy)  # API request

Test permissions allowed by the current IAM policy on a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.test_iam_permissions(
   ...     ['roles/reader', 'roles/writer', 'roles/owner'])  # API request
   ['roles/reader', 'roles/writer']


Publish messages to a topic
---------------------------

Publish a single message to a topic, without attributes:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.publish('this is the message_payload')  # API request
   <message_id>

Publish a single message to a topic, with attributes:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> topic.publish('this is another message_payload',
   ...               attr1='value1', attr2='value2')  # API request
   <message_id>

Publish a set of messages to a topic (as a single request):

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
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

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> subscription.create()  # API request

Create a new pull subscription for a topic with a non-default ACK deadline:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name', ack_deadline=90)
   >>> subscription.create()  # API request

Create a new push subscription for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> ENDPOINT = 'https://example.com/hook'
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name',
   ...                                   push_endpoint=ENDPOINT)
   >>> subscription.create()  # API request

Check for the existence of a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> subscription.exists()  # API request
   True

Convert a pull subscription to push:

.. doctest::

   >>> from gcloud import pubsub
   >>> ENDPOINT = 'https://example.com/hook'
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> subscription.modify_push_configuration(push_endpoint=ENDPOINT)  # API request

Convert a push subscription to pull:

.. doctest::

   >>> from gcloud import pubsub
   >>> ENDPOINT = 'https://example.com/hook'
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name',
   ...                                   push_endpoint=ENDPOINT)
   >>> subscription.modify_push_configuration(push_endpoint=None)  # API request

List subscriptions for a topic:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscriptions, next_page_token = topic.list_subscriptions()  # API request
   >>> [subscription.name for subscription in subscriptions]
   ['subscription_name']

List all subscriptions for the default project:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> subscription, next_page_tokens = client.list_subscriptions()  # API request
   >>> [subscription.name for subscription in subscriptions]
   ['subscription_name']

Delete a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> subscription.delete()  # API request


Pull messages from a subscription
---------------------------------

Fetch pending messages for a pull subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> with topic.batch() as batch:
   ...     batch.publish('this is the first message_payload')
   ...     batch.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> received = subscription.pull()  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.message_id for message in messages]
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

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> with topic.batch() as batch:
   ...     batch.publish('this is the first message_payload')
   ...     batch.publish('this is the second message_payload',
   ...                   attr1='value1', attr2='value2')
   >>> received = subscription.pull(max_messages=1)  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.message_id for message in messages]

Fetch messages for a pull subscription without blocking (none pending):

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> received = subscription.pull(return_immediately=True)  # API request
   >>> messages = [recv[1] for recv in received]
   >>> [message.message_id for message in messages]
   []
