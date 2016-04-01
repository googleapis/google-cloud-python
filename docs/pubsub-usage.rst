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

List topics for the default project:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START client_list_topics]
   :end-before: [END client_list_topics]

Create a new topic for the default project:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_create]
   :end-before: [END topic_create]

Check for the existence of a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_exists]
   :end-before: [END topic_exists]

Delete a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_delete]
   :end-before: [END topic_delete]

Fetch the IAM policy for a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_get_iam_policy]
   :end-before: [END topic_get_iam_policy]

Update the IAM policy for a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_set_iam_policy]
   :end-before: [END topic_set_iam_policy]

Test permissions allowed by the current IAM policy on a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_check_iam_permissions]
   :end-before: [END topic_check_iam_permissions]


Publish messages to a topic
---------------------------

Publish a single message to a topic, without attributes:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_publish_simple_message]
   :end-before: [END topic_publish_simple_message]

Publish a single message to a topic, with attributes:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_publish_message_with_attrs]
   :end-before: [END topic_publish_message_with_attrs]

Publish a set of messages to a topic (as a single request):

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_batch]
   :end-before: [END topic_batch]

.. note::

   The only API request happens during the ``__exit__()`` of the topic
   used as a context manager, and only if the block exits without raising
   an exception.


Manage subscriptions to topics
------------------------------

List all subscriptions for the default project:

.. doctest::

.. literalinclude:: pubsub_snippets.py
   :start-after: [START client_list_subscriptions]
   :end-before: [END client_list_subscriptions]

List subscriptions for a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_list_subscriptions]
   :end-before: [END topic_list_subscriptions]

Create a new pull subscription for a topic, with defaults:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_subscription_defaults]
   :end-before: [END topic_subscription_defaults]

Create a new pull subscription for a topic with a non-default ACK deadline:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_subscription_ack90]
   :end-before: [END topic_subscription_ack90]

Create a new push subscription for a topic:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START topic_subscription_push]
   :end-before: [END topic_subscription_push]

Check for the existence of a subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_exists]
   :end-before: [END subscription_exists]

Convert a pull subscription to push:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_pull_push]
   :end-before: [END subscription_pull_push]

Convert a push subscription to pull:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_push_pull]
   :end-before: [END subscription_push_pull]

Re-synchronize a subscription with the back-end:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_reload]
   :end-before: [END subscription_reload]

Delete a subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_delete]
   :end-before: [END subscription_delete]


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

Fetch the IAM policy for a subscription

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> policy = subscription.get_iam_policy()  # API request
   >>> policy.etag
   'DEADBEEF'
   >>> policy.owners
   ['user:phred@example.com']
   >>> policy.writers
   ['systemAccount:abc-1234@systemaccounts.example.com']
   >>> policy.readers
   ['domain:example.com']

Update the IAM policy for a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> policy = subscription.get_iam_policy()  # API request
   >>> policy.writers.add(policy.group('editors-list@example.com'))
   >>> subscription.set_iam_policy(policy)  # API request

Test permissions allowed by the current IAM policy on a subscription:

.. doctest::

   >>> from gcloud import pubsub
   >>> from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
   >>> client = pubsub.Client()
   >>> topic = client.topic('topic_name')
   >>> subscription = topic.subscription('subscription_name')
   >>> allowed = subscription.check_iam_permissions(
   ...     [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE])  # API request
   >>> allowed == [VIEWER_ROLE, EDITOR_ROLE]
   True
