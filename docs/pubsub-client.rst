Pub/Sub Client
==============

.. automodule:: gcloud.pubsub.client
  :show-inheritance:

  .. autoclass:: Client

    For example:

    .. doctest::

        >>> from gcloud import pubsub
        >>> client = pubsub.Client()

    .. automethod:: topic

        For example:

        .. doctest::

        >>> topic = client.topic('topic-name', timestamp_messages=True)

    .. automethod:: list_topics

        For example, to get a list of all the topics in the project:

        .. doctest::

        >>> topics, token = client.list_topics()
        >>> while token is not None:
        ...    next_batch, token = client.list_topics(token)
        ...    topics.extend(next_batch)

    .. automethod:: list_subscriptions

        For example, to get a list of all the subscriptions in the project:

        .. doctest::

        >>> subscriptions, token = client.list_subscriptions()
        >>> while token is not None:
        ...    next_batch, token = client.list_subscriptions(token)
        ...    subscriptions.extend(next_batch)

Connection
~~~~~~~~~~

.. automodule:: gcloud.pubsub.connection
  :members:
  :undoc-members:
  :show-inheritance:
