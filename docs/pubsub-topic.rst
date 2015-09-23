Topics
~~~~~~

.. automodule:: gcloud.pubsub.topic
  :show-inheritance:

  .. autoclass:: Topic

     For example:

     .. doctest::

        >>> from gcloud.pubsub import Topic
        >>> topic = Topic('topic-name', client)

     Normally, application code would construct a ``Topic`` instance
     via the :meth:`gcloud.pubsub.client.Client.topic` factory rather
     than instantiating the class directly.  For example:

     .. doctest::

        >>> topic = client.topic('topic-name')

     .. autoattribute:: project

     .. autoattribute:: path

     .. autoattribute:: full_name

     .. automethod:: subscription

        .. doctest::

           >>> subscription = topic.subscription('subscription-name')

     The following methods cause the topic to make calls to the back-end API.

     .. automethod:: create

        .. doctest::

           >>> topic.create()

     .. automethod:: exists

        .. doctest::

           >>> topic.exists()
           True

     .. automethod:: delete

        .. doctest::

           >>> topic.delete()

     .. automethod:: publish

        For example:

        .. doctest::

           >>> topic.publish(b'MESSAGE_BYTES', some_key='value')

     Batching allows the application to publish a set of messages to a
     topic via a single API request.

     .. automethod:: batch

  .. autoclass:: Batch

     .. doctest::

        >>> from gcloud.pubsub.topic import Batch
        >>> batch = Batch(topic, client)

     Normally, application code would construct a ``Batch`` instance
     via the :meth:`gcloud.pubsub.topic.Topic.batch` factory rather
     than instantiating the class directly.  For example:

     .. doctest::

        >>> batch = topic.batch()

     .. automethod:: publish

        .. doctest::

           >>> batch = topic.batch()
           >>> batch.publish('this is the first message_payload')
           >>> batch.publish('this is the second message_payload',
           ...                   attr1='value1', attr2='value2')
           >>> list(batch)
           [<message_id1>, <message_id2>]

     .. automethod:: commit

        For example, given the previous calls to ``pubilsh``:

        .. doctest::

           >>> batch.commit()

        When the ``Batch`` is used as a context manager, its ``commit``
        method is called automatically when the context manager exits
        without an exception. For example, ``commit`` is called as the
        ``with`` block exits:

        .. doctest::

           >>> with topic.batch() as batch:
           ...     batch.publish('this is the first message_payload')
           ...     batch.publish('this is the second message_payload',
           ...                   attr1='value1', attr2='value2')
