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

    Transactions can be used to build up a bulk mutation and ensure all
    or none succeed (transactionally).

    For example, the following snippet of code will put the two ``save``
    operations (either ``insert`` or ``upsert``) into the same
    mutation, and execute those within a transaction::

      >>> from gcloud import datastore
      >>> client = datastore.Client()
      >>> with client.transaction():
      ...     client.put_multi([entity1, entity2])

    Because it derives from :class:`Batch <.datastore.batch.Batch>`,
    :class:`Transaction` also provides :meth:`put` and :meth:`delete` methods::

      >>> with client.transaction() as xact:
      ...     xact.put(entity1)
      ...     xact.delete(entity2.key)

    By default, the transaction is rolled back if the transaction block
    exits with an error::

      >>> with client.transaction():
      ...     do_some_work()
      ...     raise SomeException()  # rolls back

    If the transaction block exists without an exception, it will commit
    by default.

    .. warning:: Inside a transaction, automatically assigned IDs for
       entities will not be available at save time!  That means, if you
       try::

         >>> with client.transaction():
         ...     entity = datastore.Entity(key=client.key('Thing'))
         ...     client.put(entity)

       ``entity`` won't have a complete key until the transaction is
       committed.

       Once you exit the transaction (or call :meth:`commit`), the
       automatically generated ID will be assigned to the entity::

         >>> with client.transaction():
         ...     entity = datastore.Entity(key=client.key('Thing'))
         ...     client.put(entity)
         ...     print(entity.key.is_partial)  # There is no ID on this key.
         ...
         True
         >>> print(entity.key.is_partial)  # There *is* an ID.
         False

    If you don't want to use the context manager you can initialize a
    transaction manually::

      >>> transaction = client.transaction()
      >>> transaction.begin()
      >>>
      >>> entity = datastore.Entity(key=client.key('Thing'))
      >>> transaction.put(entity)
      >>>
      >>> if error:
      ...     transaction.rollback()
      ... else:
      ...     transaction.commit()

    :type client: :class:`gcloud.datastore.client.Client`
    :param client: the client used to connect to datastore.
    """

    def __init__(self, client):
        super(Transaction, self).__init__(client)
        self._id = None

    @property
    def id(self):
        """Getter for the transaction ID.

        :rtype: string
        :returns: The ID of the current transaction.
        """
        return self._id

    def current(self):
        """Return the topmost transaction.

        .. note::

            If the topmost element on the stack is not a transaction,
            returns None.

        :rtype: :class:`gcloud.datastore.transaction.Transaction` or None
        """
        top = super(Transaction, self).current()
        if isinstance(top, Transaction):
            return top

    def begin(self):
        """Begins a transaction.

        This method is called automatically when entering a with
        statement, however it can be called explicitly if you don't want
        to use a context manager.

        :raises: :class:`ValueError` if the transaction has already begun.
        """
        super(Transaction, self).begin()
        self._id = self.connection.begin_transaction(self.project)

    def rollback(self):
        """Rolls back the current transaction.

        This method has necessary side-effects:

        - Sets the current connection's transaction reference to None.
        - Sets the current transaction's ID to None.
        """
        try:
            self.connection.rollback(self.project, self._id)
        finally:
            super(Transaction, self).rollback()
            # Clear our own ID in case this gets accidentally reused.
            self._id = None

    def commit(self):
        """Commits the transaction.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly if you don't want to use a
        context manager.

        This method has necessary side-effects:

        - Sets the current transaction's ID to None.
        """
        try:
            super(Transaction, self).commit()
        finally:
            # Clear our own ID in case this gets accidentally reused.
            self._id = None
