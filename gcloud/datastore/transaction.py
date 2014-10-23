"""Create / interact with gcloud datastore transactions."""

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore import helpers


class Transaction(object):
    """An abstraction representing datastore Transactions.

    Transactions can be used
    to build up a bulk mutuation
    as well as provide isolation.

    For example,
    the following snippet of code
    will put the two ``save`` operations
    (either ``insert_auto_id`` or ``upsert``)
    into the same mutation, and execute those within a transaction::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
      >>> with dataset.transaction(bulk_mutation=True)  # The default.
      ...   entity1.save()
      ...   entity2.save()

    By default, the transaction is rolled back if the transaction block
    exits with an error::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
      >>> with dataset.transaction() as t:
      ...   do_some_work()
      ...   raise Exception() # rolls back

    If the transaction block exists without an exception,
    it will commit by default.

    .. warning::
      Inside a transaction,
      automatically assigned IDs for entities
      will not be available at save time!
      That means,
      if you try::

        >>> with dataset.transaction():
        ...   entity = dataset.entity('Thing').save()

      ``entity`` won't have a complete Key
      until the transaction is committed.

      Once you exit the transaction (or call ``commit()``),
      the automatically generated ID will be assigned
      to the entity::

        >>> with dataset.transaction():
        ...   entity = dataset.entity('Thing')
        ...   entity.save()
        ...   assert entity.key().is_partial()  # There is no ID on this key.
        >>> assert not entity.key().is_partial()  # There *is* an ID.

    .. warning::
      If you're using the automatically generated ID functionality,
      it's important that you only use
      :func:`gcloud.datastore.entity.Entity.save`
      rather than using
      :func:`gcloud.datastore.connection.Connection.save_entity` directly.

      If you mix the two,
      the results will have extra IDs generated
      and it could jumble things up.

    If you don't want to use the context manager
    you can initialize a transaction manually::

      >>> transaction = dataset.transaction()
      >>> transaction.begin()

      >>> entity = dataset.entity('Thing')
      >>> entity.save()

      >>> if error:
      ...   transaction.rollback()
      ... else:
      ...   transaction.commit()

    For now,
    this library will enforce a rule of
    one transaction per connection.
    That is,
    If you want to work with two transactions at the same time
    (for whatever reason),
    that must happen over two separate
    :class:`gcloud.datastore.connection.Connection` s.

    For example, this is perfectly valid::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
      >>> with dataset.transaction():
      ...   dataset.entity('Thing').save()

    However, this **wouldn't** be acceptable::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
      >>> with dataset.transaction():
      ...   dataset.entity('Thing').save()
      ...   with dataset.transaction():
      ...     dataset.entity('Thing').save()

    Technically, it looks like the Protobuf API supports this type of pattern,
    however it makes the code particularly messy.
    If you really need to nest transactions, try::

      >>> from gcloud import datastore
      >>> dataset1 = datastore.get_dataset('dataset-id', email, key_path)
      >>> dataset2 = datastore.get_dataset('dataset-id', email, key_path)
      >>> with dataset1.transaction():
      ...   dataset1.entity('Thing').save()
      ...   with dataset2.transaction():
      ...     dataset2.entity('Thing').save()

    :type dataset: :class:`gcloud.datastore.dataset.Dataset`
    :param dataset: The dataset to which this :class:`Transaction` belongs.
    """

    def __init__(self, dataset):
        self._dataset = dataset
        self._id = None
        self._mutation = datastore_pb.Mutation()
        self._auto_id_entities = []

    def connection(self):
        """Getter for current connection over which the transaction will run.

        :rtype: :class:`gcloud.datastore.connection.Connection`
        :returns: The connection over which the transaction will run.
        """

        return self.dataset().connection()

    def dataset(self):
        """Getter for the current dataset.

        :rtype: :class:`gcloud.datastore.dataset.Dataset`
        :returns: The dataset to which the transaction belongs.
        """

        return self._dataset

    def id(self):
        """Getter for the transaction ID.

        :rtype: string
        :returns: The ID of the current transaction.
        """

        return self._id

    def mutation(self):
        """Getter for the current mutation.

        Every transaction is committed
        with a single Mutation
        representing the 'work' to be done as part of the transaction.
        Inside a transaction,
        calling ``save()`` on an entity
        builds up the mutation.
        This getter returns the Mutation protobuf
        that has been built-up so far.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`
        :returns: The Mutation protobuf to be sent in the commit request.
        """
        return self._mutation

    def add_auto_id_entity(self, entity):
        """Adds an entity to the list of entities to update with IDs.

        When an entity has a partial key,
        calling ``save()`` adds an insert_auto_id entry in the mutation.
        In order to make sure we update the Entity
        once the transaction is committed,
        we need to keep track of which entities to update
        (and the order is important).

        When you call ``save()`` on an entity inside a transaction,
        if the entity has a partial key,
        it adds itself to the list of entities to be updated
        once the transaction is committed
        by calling this method.
        """
        self._auto_id_entities.append(entity)

    def begin(self):
        """Begins a transaction.

        This method is called automatically when entering a with statement,
        however it can be called explicitly
        if you don't want to use a context manager.
        """
        self._id = self.connection().begin_transaction(self.dataset().id())
        self.connection().transaction(self)

    def rollback(self):
        """Rolls back the current transaction.

        This method has necessary side-effects:

        - Sets the current connection's transaction reference to None.
        - Sets the current transaction's ID to None.
        """
        self.connection().rollback_transaction(self.dataset().id())
        self.connection().transaction(None)
        self._id = None

    def commit(self):
        """Commits the transaction.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly
        if you don't want to use a context manager.

        This method has necessary side-effects:

        - Sets the current connection's transaction reference to None.
        - Sets the current transaction's ID to None.
        - Updates paths for any keys that needed an automatically generated ID.
        """
        # It's possible that they called commit() already, in which case
        # we shouldn't do any committing of our own.
        if self.connection().transaction():
            result = self.connection().commit(self.dataset().id(),
                                              self.mutation())

            # For any of the auto-id entities, make sure we update their keys.
            for i, entity in enumerate(self._auto_id_entities):
                key_pb = result.insert_auto_id_key[i]
                key = helpers.key_from_protobuf(key_pb)
                entity.key(entity.key().path(key.path()))

        # Tell the connection that the transaction is over.
        self.connection().transaction(None)

        # Clear our own ID in case this gets accidentally reused.
        self._id = None

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
