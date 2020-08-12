# Copyright 2014 Google LLC
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

"""Create / interact with Google Cloud Datastore transactions."""

from google.cloud.datastore.batch import Batch
from google.cloud.datastore_v1.types import TransactionOptions


def _make_retry_timeout_kwargs(retry, timeout):
    """Helper: make optional retry / timeout kwargs dict."""
    kwargs = {}

    if retry is not None:
        kwargs["retry"] = retry

    if timeout is not None:
        kwargs["timeout"] = timeout

    return kwargs


class Transaction(Batch):
    """An abstraction representing datastore Transactions.

    Transactions can be used to build up a bulk mutation and ensure all
    or none succeed (transactionally).

    For example, the following snippet of code will put the two ``save``
    operations (either ``insert`` or ``upsert``) into the same
    mutation, and execute those within a transaction:

    .. testsetup:: txn-put-multi, txn-api

        import os
        import uuid

        from google.cloud import datastore
        from tests.system.test_system import Config  # system tests

        unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
        client = datastore.Client(namespace='ns{}'.format(unique))
        key1 = client.key('_Doctest')
        entity1 = datastore.Entity(key=key1)
        entity1['foo'] = 1337

        key2 = client.key('_Doctest', 'abcd1234')
        entity2 = datastore.Entity(key=key2)
        entity2['foo'] = 42

        Config.TO_DELETE.extend([entity1, entity2])

    .. doctest:: txn-put-multi

        >>> with client.transaction():
        ...     client.put_multi([entity1, entity2])

    Because it derives from :class:`~google.cloud.datastore.batch.Batch`,
    :class:`Transaction` also provides :meth:`put` and :meth:`delete` methods:

    .. doctest:: txn-api

       >>> with client.transaction() as xact:
       ...     xact.put(entity1)
       ...     xact.delete(entity2.key)

    By default, the transaction is rolled back if the transaction block
    exits with an error:

    .. testsetup:: txn-error

        import os
        import uuid

        from google.cloud import datastore

        unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
        client = datastore.Client(namespace='ns{}'.format(unique))

        def do_some_work():
            return

        class SomeException(Exception):
            pass

    .. doctest:: txn-error

        >>> with client.transaction():
        ...     do_some_work()
        ...     raise SomeException  # rolls back
        Traceback (most recent call last):
          ...
        SomeException

    If the transaction block exits without an exception, it will commit
    by default.

    .. warning::

        Inside a transaction, automatically assigned IDs for
        entities will not be available at save time!  That means, if you
        try:

        .. testsetup:: txn-entity-key, txn-entity-key-after, txn-manual

            import os
            import uuid

            from google.cloud import datastore
            from tests.system.test_system import Config  # system tests

            unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
            client = datastore.Client(namespace='ns{}'.format(unique))

            def Entity(*args, **kwargs):
                entity = datastore.Entity(*args, **kwargs)
                Config.TO_DELETE.append(entity)
                return entity

        .. doctest:: txn-entity-key

            >>> with client.transaction():
            ...     entity = Entity(key=client.key('Thing'))
            ...     client.put(entity)

       ``entity`` won't have a complete key until the transaction is
       committed.

       Once you exit the transaction (or call :meth:`commit`), the
       automatically generated ID will be assigned to the entity:

       .. doctest:: txn-entity-key-after

          >>> with client.transaction():
          ...     entity = Entity(key=client.key('Thing'))
          ...     client.put(entity)
          ...     print(entity.key.is_partial)  # There is no ID on this key.
          ...
          True
          >>> print(entity.key.is_partial)  # There *is* an ID.
          False

    If you don't want to use the context manager you can initialize a
    transaction manually:

    .. doctest:: txn-manual

       >>> transaction = client.transaction()
       >>> transaction.begin()
       >>>
       >>> entity = Entity(key=client.key('Thing'))
       >>> transaction.put(entity)
       >>>
       >>> transaction.commit()

    :type client: :class:`google.cloud.datastore.client.Client`
    :param client: the client used to connect to datastore.

    :type read_only: bool
    :param read_only: indicates the transaction is read only.
    """

    _status = None

    def __init__(self, client, read_only=False):
        super(Transaction, self).__init__(client)
        self._id = None
        if read_only:
            options = TransactionOptions(read_only=TransactionOptions.ReadOnly())
        else:
            options = TransactionOptions()
        self._options = options

    @property
    def id(self):
        """Getter for the transaction ID.

        :rtype: str
        :returns: The ID of the current transaction.
        """
        return self._id

    def current(self):
        """Return the topmost transaction.

        .. note::

            If the topmost element on the stack is not a transaction,
            returns None.

        :rtype: :class:`google.cloud.datastore.transaction.Transaction` or None
        :returns: The current transaction (if any are active).
        """
        top = super(Transaction, self).current()
        if isinstance(top, Transaction):
            return top

    def begin(self, retry=None, timeout=None):
        """Begins a transaction.

        This method is called automatically when entering a with
        statement, however it can be called explicitly if you don't want
        to use a context manager.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry:
            A retry object used to retry requests. If ``None`` is specified,
            requests will be retried using a default configuration.

        :type timeout: float
        :param timeout:
            Time, in seconds, to wait for the request to complete.
            Note that if ``retry`` is specified, the timeout applies
            to each individual attempt.

        :raises: :class:`~exceptions.ValueError` if the transaction has
                 already begun.
        """
        super(Transaction, self).begin()

        kwargs = _make_retry_timeout_kwargs(retry, timeout)

        try:
            response_pb = self._client._datastore_api.begin_transaction(
                self.project, **kwargs
            )
            self._id = response_pb.transaction
        except:  # noqa: E722 do not use bare except, specify exception instead
            self._status = self._ABORTED
            raise

    def rollback(self, retry=None, timeout=None):
        """Rolls back the current transaction.

        This method has necessary side-effects:

        - Sets the current transaction's ID to None.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry:
            A retry object used to retry requests. If ``None`` is specified,
            requests will be retried using a default configuration.

        :type timeout: float
        :param timeout:
            Time, in seconds, to wait for the request to complete.
            Note that if ``retry`` is specified, the timeout applies
            to each individual attempt.
        """
        kwargs = _make_retry_timeout_kwargs(retry, timeout)

        try:
            # No need to use the response it contains nothing.
            self._client._datastore_api.rollback(self.project, self._id, **kwargs)
        finally:
            super(Transaction, self).rollback()
            # Clear our own ID in case this gets accidentally reused.
            self._id = None

    def commit(self, retry=None, timeout=None):
        """Commits the transaction.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly if you don't want to use a
        context manager.

        This method has necessary side-effects:

        - Sets the current transaction's ID to None.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry:
            A retry object used to retry requests. If ``None`` is specified,
            requests will be retried using a default configuration.

        :type timeout: float
        :param timeout:
            Time, in seconds, to wait for the request to complete.
            Note that if ``retry`` is specified, the timeout applies
            to each individual attempt.
        """
        kwargs = _make_retry_timeout_kwargs(retry, timeout)

        try:
            super(Transaction, self).commit(**kwargs)
        finally:
            # Clear our own ID in case this gets accidentally reused.
            self._id = None

    def put(self, entity):
        """Adds an entity to be committed.

        Ensures the transaction is not marked readonly.
        Please see documentation at
        :meth:`~google.cloud.datastore.batch.Batch.put`

        :type entity: :class:`~google.cloud.datastore.entity.Entity`
        :param entity: the entity to be saved.

        :raises: :class:`RuntimeError` if the transaction
                 is marked ReadOnly
        """
        if self._options.HasField("read_only"):
            raise RuntimeError("Transaction is read only")
        else:
            super(Transaction, self).put(entity)
