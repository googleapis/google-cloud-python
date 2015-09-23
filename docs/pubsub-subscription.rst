Subscriptions
~~~~~~~~~~~~~

.. automodule:: gcloud.pubsub.subscription
  :show-inheritance:

   .. autoclass:: Subscription

     .. doctest::

        >>> from gcloud.pubsub import Subscription
        >>> subscription = Subscription('subscription-name', topic)

     Normally, application code would construct a ``Topic`` instance
     via the :meth:`gcloud.pubsub.client.Client.topic` factory rather
     than instantiating the class directly.  For example:

     .. doctest::

        >>> topic = client.topic('topic-name')

     .. autoattribute:: path

     The following methods cause the topic to make calls to the back-end API.

     .. automethod:: create

        .. doctest::

           >>> subscription.create()

     .. automethod:: exists

        .. doctest::

           >>> subscription.exists()
           True

     .. automethod:: reload

        .. doctest::

           >>> subscription.reload()

     .. automethod:: delete

        .. doctest::

           >>> subscription.delete()

     .. automethod:: modify_push_configuration

        .. doctest::

           >>> subscription.modify_push_configuration('http://example.com/callback')

     .. automethod:: pull

        .. doctest::

           >>> received = subscription.pull(max_messages=1)
           >>> messages = [recv[1] for recv in received]

     .. automethod:: modify_ack_deadline

        For instance, given the previous call to ``pull``, we can delay
        the deadline for acknowlegement:

        .. doctest::

           >>> ack_ids = [recv[0] for recv in received]
           >>> for ack_id in ack_ids:
           ...     subscription.modify_ack_deadline(ack_id, 3600)

     .. automethod:: acknowledge

        .. doctest::

           >>> subscription.acknowledge(ack_ids)
