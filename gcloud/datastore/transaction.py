# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create / interact with gcloud datastore transactions."""

from gcloud.datastore.batch import Batch


class Transaction(Batch):
    """An abstraction representing datastore Transactions.

    Transactions can be used to build up a bulk mutuation as well as
    provide isolation.

    For example, the following snippet of code will put the two ``save``
    operations (either ``insert_auto_id`` or ``upsert``) into the same
    mutation, and execute those within a transaction::

      >>> from gcloud import datastore
      >>> from gcloud.datastore.transaction import Transaction

      >>> datastore.set_default_connection()
      >>> datastore.set_default_dataset_id()

      >>> with Transaction()
      ...     entity1.save()
      ...     entity2.save()

    Because it derives from :class:`Batch`, :class`Transaction` also provides
    :meth:`put` and :meth:`delete` methods::

      >>> with Transaction()
      ...     transaction.put(entity1)
      ...     transaction.delete(entity2.key)

    By default, the transaction is rolled back if the transaction block
    exits with an error::

      >>> with Transaction() as txn:
      ...     do_some_work()
      ...     raise SomeException()  # rolls back

    If the transaction block exists without an exception, it will commit
    by default.

    .. warning:: Inside a transaction, automatically assigned IDs for
       entities will not be available at save time!  That means, if you
       try::

         >>> with Transaction():
         ...     entity = Entity(key=Key('Thing'))
         ...     entity.save()

       ``entity`` won't have a complete Key until the transaction is
       committed.

       Once you exit the transaction (or call ``commit()``), the
       automatically generated ID will be assigned to the entity::

         >>> with Transaction():
         ...     entity = Entity(key=Key('Thing'))
         ...     entity.save()
         ...     assert entity.key.is_partial  # There is no ID on this key.
         >>> assert not entity.key.is_partial  # There *is* an ID.

    .. warning:: If you're using the automatically generated ID
       functionality, it's important that you only use
       :meth:`gcloud.datastore.entity.Entity.save` rather than using
       :meth:`gcloud.datastore.connection.Connection.save_entity`
       directly.

       If you mix the two, the results will have extra IDs generated and
       it could jumble things up.

    If you don't want to use the context manager you can initialize a
    transaction manually::

      >>> transaction = Transaction()
      >>> transaction.begin()

      >>> entity = Entity(key=Key('Thing'))
      >>> entity.save()

      >>> if error:
      ...     transaction.rollback()
      ... else:
      ...     transaction.commit()

    For now, this library will enforce a rule of one transaction per
    connection.  That is, If you want to work with two transactions at
    the same time (for whatever reason), that must happen over two
    separate :class:`gcloud.datastore.connection.Connection` s.

    For example, this is perfectly valid::

      >>> with Transaction():
      ...     entity = Entity(key=Key('Thing'))
      ...     entity.save()

    However, this **wouldn't** be acceptable::

      >>> with Transaction():
      ...     Entity(key=Key('Thing')).save()
      ...     with Transaction():
      ...         Entity(key=Key('Thing')).save()

    Technically, it looks like the Protobuf API supports this type of
    pattern, however it makes the code particularly messy.

    :type dataset_id: string
    :param dataset_id: The ID of the dataset.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: The connection used to connect to datastore.

    :raises: :class:`ValueError` if either a connection or dataset ID
             are not set.
    """

    def __init__(self, dataset_id=None, connection=None):
        super(Transaction, self).__init__(dataset_id, connection)
        self._id = None

    @property
    def id(self):
        """Getter for the transaction ID.

        :rtype: string
        :returns: The ID of the current transaction.
        """
        return self._id

    def begin(self):
        """Begins a transaction.

        This method is called automatically when entering a with
        statement, however it can be called explicitly if you don't want
        to use a context manager.
        """
        self._id = self.connection.begin_transaction(self._dataset_id)
        self.connection.transaction(self)

    def rollback(self):
        """Rolls back the current transaction.

        This method has necessary side-effects:

        - Sets the current connection's transaction reference to None.
        - Sets the current transaction's ID to None.
        """
        self.connection.rollback(self._dataset_id)
        self.connection.transaction(None)
        self._id = None

    def commit(self):
        """Commits the transaction.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly if you don't want to use a
        context manager.

        This method has necessary side-effects:

        - Sets the current connection's transaction reference to None.
        - Sets the current transaction's ID to None.
        - Updates paths for any keys that needed an automatically generated ID.
        """
        # It's possible that they called commit() already, in which case
        # we shouldn't do any committing of our own.
        if self.connection.transaction():
            super(Transaction, self).commit()

        # Tell the connection that the transaction is over.
        self.connection.transaction(None)

        # Clear our own ID in case this gets accidentally reused.
        self._id = None
