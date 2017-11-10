# Copyright 2017 Google LLC All rights reserved.
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

"""Helpers for applying Google Cloud Firestore changes in a transaction."""


import random
import time

import google.gax.errors
import google.gax.grpc
import grpc
import six

from google.cloud.firestore_v1beta1 import _helpers
from google.cloud.firestore_v1beta1 import batch
from google.cloud.firestore_v1beta1 import types


MAX_ATTEMPTS = 5
"""int: Default number of transaction attempts (with retries)."""
_CANT_BEGIN = (
    'The transaction has already begun. Current transaction ID: {!r}.')
_MISSING_ID_TEMPLATE = (
    'The transaction has no transaction ID, so it cannot be {}.')
_CANT_ROLLBACK = _MISSING_ID_TEMPLATE.format('rolled back')
_CANT_COMMIT = _MISSING_ID_TEMPLATE.format('committed')
_WRITE_READ_ONLY = 'Cannot perform write operation in read-only transaction.'
_INITIAL_SLEEP = 1.0
"""float: Initial "max" for sleep interval. To be used in :func:`_sleep`."""
_MAX_SLEEP = 30.0
"""float: Eventual "max" sleep time. To be used in :func:`_sleep`."""
_MULTIPLIER = 2.0
"""float: Multiplier for exponential backoff. To be used in :func:`_sleep`."""
_EXCEED_ATTEMPTS_TEMPLATE = 'Failed to commit transaction in {:d} attempts.'
_CANT_RETRY_READ_ONLY = 'Only read-write transactions can be retried.'


class Transaction(batch.WriteBatch):
    """Accumulate read-and-write operations to be sent in a transaction.

    Args:
        client (~.firestore_v1beta1.client.Client): The client that
            created this transaction.
        max_attempts (Optional[int]): The maximum number of attempts for
            the transaction (i.e. allowing retries). Defaults to
            :attr:`~.firestore_v1beta1.transaction.MAX_ATTEMPTS`.
        read_only (Optional[bool]): Flag indicating if the transaction
            should be read-only or should allow writes. Defaults to
            :data:`False`.
    """

    def __init__(self, client, max_attempts=MAX_ATTEMPTS, read_only=False):
        super(Transaction, self).__init__(client)
        self._max_attempts = max_attempts
        self._read_only = read_only
        self._id = None

    def _add_write_pbs(self, write_pbs):
        """Add `Write`` protobufs to this transaction.

        Args:
            write_pbs (List[google.cloud.proto.firestore.v1beta1.\
                write_pb2.Write]): A list of write protobufs to be added.

        Raises:
            ValueError: If this transaction is read-only.
        """
        if self._read_only:
            raise ValueError(_WRITE_READ_ONLY)

        super(Transaction, self)._add_write_pbs(write_pbs)

    def _options_protobuf(self, retry_id):
        """Convert the current object to protobuf.

        The ``retry_id`` value is used when retrying a transaction that
        failed (e.g. due to contention). It is intended to be the "first"
        transaction that failed (i.e. if multiple retries are needed).

        Args:
            retry_id (Union[bytes, NoneType]): Transaction ID of a transaction
                to be retried.

        Returns:
            Optional[google.cloud.firestore_v1beta1.types.TransactionOptions]:
            The protobuf ``TransactionOptions`` if ``read_only==True`` or if
            there is a transaction ID to be retried, else :data:`None`.

        Raises:
            ValueError: If ``retry_id`` is not :data:`None` but the
                transaction is read-only.
        """
        if retry_id is not None:
            if self._read_only:
                raise ValueError(_CANT_RETRY_READ_ONLY)

            return types.TransactionOptions(
                read_write=types.TransactionOptions.ReadWrite(
                    retry_transaction=retry_id,
                ),
            )
        elif self._read_only:
            return types.TransactionOptions(
                read_only=types.TransactionOptions.ReadOnly())
        else:
            return None

    @property
    def in_progress(self):
        """Determine if this transaction has already begun.

        Returns:
            bool: Indicates if the transaction has started.
        """
        return self._id is not None

    @property
    def id(self):
        """Get the current transaction ID.

        Returns:
            Optional[bytes]: The transaction ID (or :data:`None` if the
            current transaction is not in progress).
        """
        return self._id

    def _begin(self, retry_id=None):
        """Begin the transaction.

        Args:
            retry_id (Optional[bytes]): Transaction ID of a transaction to be
                retried.

        Raises:
            ValueError: If the current transaction has already begun.
        """
        if self.in_progress:
            msg = _CANT_BEGIN.format(self._id)
            raise ValueError(msg)

        transaction_response = self._client._firestore_api.begin_transaction(
            self._client._database_string,
            options_=self._options_protobuf(retry_id),
            options=self._client._call_options,
        )
        self._id = transaction_response.transaction

    def _clean_up(self):
        """Clean up the instance after :meth:`_rollback`` or :meth:`_commit``.

        This intended to occur on success or failure of the associated RPCs.
        """
        self._write_pbs = []
        self._id = None

    def _rollback(self):
        """Roll back the transaction.

        Raises:
            ValueError: If no transaction is in progress.
        """
        if not self.in_progress:
            raise ValueError(_CANT_ROLLBACK)

        try:
            # NOTE: The response is just ``google.protobuf.Empty``.
            self._client._firestore_api.rollback(
                self._client._database_string, self._id,
                options=self._client._call_options)
        finally:
            self._clean_up()

    def _commit(self):
        """Transactionally commit the changes accumulated.

        Returns:
            List[google.cloud.proto.firestore.v1beta1.\
                write_pb2.WriteResult, ...]: The write results corresponding
            to the changes committed, returned in the same order as the
            changes were applied to this transaction. A write result contains
            an ``update_time`` field.

        Raises:
            ValueError: If no transaction is in progress.
        """
        if not self.in_progress:
            raise ValueError(_CANT_COMMIT)

        with _helpers.remap_gax_error_on_commit():
            commit_response = _commit_with_retry(
                self._client, self._write_pbs, self._id)

        self._clean_up()
        return list(commit_response.write_results)


class _Transactional(object):
    """Provide a callable object to use as a transactional decorater.

    This is surfaced via
    :func:`~.firestore_v1beta1.transaction.transactional`.

    Args:
        to_wrap (Callable[~.firestore_v1beta1.transaction.Transaction, \
            Any]): A callable that should be run (and retried) in a
            transaction.
    """

    def __init__(self, to_wrap):
        self.to_wrap = to_wrap
        self.current_id = None
        """Optional[bytes]: The current transaction ID."""
        self.retry_id = None
        """Optional[bytes]: The ID of the first attempted transaction."""

    def _reset(self):
        """Unset the transaction IDs."""
        self.current_id = None
        self.retry_id = None

    def _pre_commit(self, transaction, *args, **kwargs):
        """Begin transaction and call the wrapped callable.

        If the callable raises an exception, the transaction will be rolled
        back. If not, the transaction will be "ready" for ``Commit`` (i.e.
        it will have staged writes).

        Args:
            transaction (~.firestore_v1beta1.transaction.Transaction): A
                transaction to execute the callable within.
            args (Tuple[Any, ...]): The extra positional arguments to pass
                along to the wrapped callable.
            kwargs (Dict[str, Any]): The extra keyword arguments to pass
                along to the wrapped callable.

        Returns:
            Any: result of the wrapped callable.

        Raises:
            Exception: Any failure caused by ``to_wrap``.
        """
        # Force the ``transaction`` to be not "in progress".
        transaction._clean_up()
        transaction._begin(retry_id=self.retry_id)

        # Update the stored transaction IDs.
        self.current_id = transaction._id
        if self.retry_id is None:
            self.retry_id = self.current_id
        try:
            return self.to_wrap(transaction, *args, **kwargs)
        except:
            # NOTE: If ``rollback`` fails this will lose the information
            #       from the original failure.
            transaction._rollback()
            raise

    def _maybe_commit(self, transaction):
        """Try to commit the transaction.

        If the transaction is read-write and the ``Commit`` fails with the
        ``ABORTED`` status code, it will be retried. Any other failure will
        not be caught.

        Args:
            transaction (~.firestore_v1beta1.transaction.Transaction): The
                transaction to be ``Commit``-ed.

        Returns:
            bool: Indicating if the commit succeeded.
        """
        try:
            transaction._commit()
            return True
        except google.gax.errors.GaxError as exc:
            if transaction._read_only:
                raise

            status_code = google.gax.grpc.exc_to_code(exc.cause)
            # If a read-write transaction returns ABORTED, retry.
            if status_code == grpc.StatusCode.ABORTED:
                return False
            else:
                raise

    def __call__(self, transaction, *args, **kwargs):
        """Execute the wrapped callable within a transaction.

        Args:
            transaction (~.firestore_v1beta1.transaction.Transaction): A
                transaction to execute the callable within.
            args (Tuple[Any, ...]): The extra positional arguments to pass
                along to the wrapped callable.
            kwargs (Dict[str, Any]): The extra keyword arguments to pass
                along to the wrapped callable.

        Returns:
            Any: The result of the wrapped callable.

        Raises:
            ValueError: If the transaction does not succeed in
                ``max_attempts``.
        """
        self._reset()

        for attempt in six.moves.xrange(transaction._max_attempts):
            result = self._pre_commit(transaction, *args, **kwargs)
            succeeded = self._maybe_commit(transaction)
            if succeeded:
                return result

            # Subsequent requests will use the failed transaction ID as part of
            # the ``BeginTransactionRequest`` when restarting this transaction
            # (via ``options.retry_transaction``). This preserves the "spot in
            # line" of the transaction, so exponential backoff is not required
            # in this case.

        transaction._rollback()
        msg = _EXCEED_ATTEMPTS_TEMPLATE.format(transaction._max_attempts)
        raise ValueError(msg)


def transactional(to_wrap):
    """Decorate a callable so that it runs in a transaction.

    Args:
        to_wrap (Callable[~.firestore_v1beta1.transaction.Transaction, \
            Any]): A callable that should be run (and retried) in a
            transaction.

    Returns:
        Callable[~.firestore_v1beta1.transaction.Transaction, Any]: the
        wrapped callable.
    """
    return _Transactional(to_wrap)


def _commit_with_retry(client, write_pbs, transaction_id):
    """Call ``Commit`` on the GAPIC client with retry / sleep.

    This function is **distinct** from
    :func:`~.firestore_v1beta1._helpers.remap_gax_error_on_commit` in
    that it does not seek to re-wrap exceptions, it just seeks to retry.

    Retries the ``Commit`` RPC on Unavailable. Usually this RPC-level
    retry is handled by the underlying GAPICd client, but in this case it
    doesn't because ``Commit`` is not always idempotent. But here we know it
    is "idempotent"-like because it has a transaction ID. We also need to do
    our own retry to special-case the ``INVALID_ARGUMENT`` error.

    Args:
        client (~.firestore_v1beta1.client.Client): A client with
            GAPIC client and configuration details.
        write_pbs (List[google.cloud.proto.firestore.v1beta1.\
            write_pb2.Write, ...]): A ``Write`` protobuf instance to
            be committed.
        transaction_id (bytes): ID of an existing transaction that
            this commit will run in.

    Returns:
        google.cloud.firestore_v1beta1.types.CommitResponse:
        The protobuf response from ``Commit``.

    Raises:
        ~google.gax.errors.GaxError: If a non-retryable exception
            is encountered.
    """
    current_sleep = _INITIAL_SLEEP
    while True:
        try:
            return client._firestore_api.commit(
                client._database_string, write_pbs,
                transaction=transaction_id,
                options=client._call_options)
        except google.gax.errors.GaxError as exc:
            status_code = google.gax.grpc.exc_to_code(exc.cause)
            if status_code == grpc.StatusCode.UNAVAILABLE:
                pass  # Retry
            else:
                raise

        current_sleep = _sleep(current_sleep)


def _sleep(current_sleep, max_sleep=_MAX_SLEEP, multiplier=_MULTIPLIER):
    """Sleep and produce a new sleep time.

    .. _Exponential Backoff And Jitter: https://www.awsarchitectureblog.com/\
                                        2015/03/backoff.html

    Select a duration between zero and ``current_sleep``. It might seem
    counterintuitive to have so much jitter, but
    `Exponential Backoff And Jitter`_ argues that "full jitter" is
    the best strategy.

    Args:
        current_sleep (float): The current "max" for sleep interval.
        max_sleep (Optional[float]): Eventual "max" sleep time
        multiplier (Optional[float]): Multiplier for exponential backoff.

    Returns:
        float: Newly doubled ``current_sleep`` or ``max_sleep`` (whichever
        is smaller)
    """
    actual_sleep = random.uniform(0.0, current_sleep)
    time.sleep(actual_sleep)
    return min(multiplier * current_sleep, max_sleep)
