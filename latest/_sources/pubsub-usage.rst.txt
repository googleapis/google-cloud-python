Using the API
=============

Authentication / Configuration
------------------------------

- Use :class:`Client <google.cloud.pubsub.client.Client>` objects to configure
  your applications.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- The library now enables the ``gRPC`` transport for the pubsub API by
  default, assuming that the required dependencies are installed and
  importable.  To *disable* this transport, set the
  :envvar:`GOOGLE_CLOUD_DISABLE_GRPC` environment variable to a
  non-empty string, e.g.:  ``$ export GOOGLE_CLOUD_DISABLE_GRPC=true``.

- :class:`Client <google.cloud.pubsub.client.Client>` objects hold both a ``project``
  and an authenticated connection to the PubSub service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <google.cloud.pubsub.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <google.cloud.pubsub.client.Client.from_service_account_p12>`.

- After setting ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GOOGLE_CLOUD_PROJECT``
  environment variables, create a :class:`Client <google.cloud.pubsub.client.Client>`

  .. code-block:: python

     >>> from google.cloud import pubsub
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

Fetch the IAM policy for a subscription

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_get_iam_policy]
   :end-before: [END subscription_get_iam_policy]

Update the IAM policy for a subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_set_iam_policy]
   :end-before: [END subscription_set_iam_policy]

Test permissions allowed by the current IAM policy on a subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_check_iam_permissions]
   :end-before: [END subscription_check_iam_permissions]

Delete a subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_delete]
   :end-before: [END subscription_delete]


Pull messages from a subscription
---------------------------------

Fetch pending messages for a pull subscription:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_pull]
   :end-before: [END subscription_pull]

Note that received messages must be acknowledged, or else the back-end
will re-send them later:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_acknowledge]
   :end-before: [END subscription_acknowledge]

Fetch messages for a pull subscription without blocking (none pending):

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_pull_return_immediately]
   :end-before: [END subscription_pull_return_immediately]

Update the acknowlegement deadline for pulled messages:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_modify_ack_deadline]
   :end-before: [END subscription_modify_ack_deadline]

Fetch pending messages, acknowledging those whose processing doesn't raise an
error:

.. literalinclude:: pubsub_snippets.py
   :start-after: [START subscription_pull_autoack]
   :end-before: [END subscription_pull_autoack]

.. note::

   The ``pull`` API request occurs at entry to the ``with`` block, and the
   ``acknowlege`` API request occurs at the end, passing only the ``ack_ids``
   which haven't been deleted from ``ack``
