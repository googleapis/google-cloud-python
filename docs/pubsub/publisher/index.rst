Publishing Messages
===================

Publishing messages is handled through the :class:`.publisher.Client` class.
This class provides methods to create topics, and (most importantly) a
:meth:`~.pubsub_v1.publisher.Client.publish` method that publishes
messages to Pub/Sub.

Instantiating a publishing client is straightforward::

.. code-block:: python

    from google.cloud import pubsub
    publish_client = pubsub.publisher.Client()


Publish a Message
-----------------

To publish a message, use the :meth:`~.pubsub_v1.publisher.Client.publish`
method. This method accepts two positional arguments: the topic to publish to,
and the body of the message. It also accepts arbitrary keyword arguments,
which are passed along as attributes of the message.

The topic is passed along as a string; all topics have the canonical form of
``projects/{project_name}/topics/{topic_name}``.

Therefore, a very basic publishing call looks like::

.. code-block:: python

    topic = 'projects/{project}/topics/{topic}''
    publish_client.publish(topic, b'This is my message.')

.. note::

    The message data in Pub/Sub is an opaque blob of bytes, and as such, you
    _must_ send a ``bytes`` object in Python 3 (``str`` object in Python 2).
    If you send a text string (``str`` in Python 3, ``unicode`` in Python 2),
    the method will raise :exc:`TypeError`.

    The reason it works this way is because there is no reasonable guarantee
    that the same language or environment is being used by the subscriber,
    and so it is the responsibility of the publisher to properly encode
    the payload.

If you want to include attributes, simply add keyword arguments:

.. code-block:: python

    topic = 'projects/{project}/topics/{topic}''
    publish_client.publish(topic, b'This is my message.', foo='bar')


Batching
--------

Whenever you publish a message, a
:class:`~.pubsub_v1.publisher.batch.thread.Batch` is automatically created.
This way, if you publish a large volume of messages, it reduces the number of
requests made to the server.
