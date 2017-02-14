# Copyright 2016 Google Inc. All rights reserved.
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

"""Spanner read-write transaction support."""

from google.cloud.proto.spanner.v1.transaction_pb2 import TransactionSelector
from google.cloud.proto.spanner.v1.transaction_pb2 import TransactionOptions

from google.cloud._helpers import _pb_timestamp_to_datetime
from google.cloud.spanner._helpers import _options_with_prefix
from google.cloud.spanner.snapshot import _SnapshotBase
from google.cloud.spanner.batch import _BatchBase


class Transaction(_SnapshotBase, _BatchBase):
    """Implement read-write transaction semantics for a session."""
    committed = None
    """Timestamp at which the transaction was successfully committed."""

    def __init__(self, session):
        super(Transaction, self).__init__(session)
        self._id = None
        self._rolled_back = False

    def _check_state(self):
        """Helper for :meth:`commit` et al.

        :raises: :exc:`ValueError` if the object's state is invalid for making
                 API requests.
        """
        if self._id is None:
            raise ValueError("Transaction is not begun")

        if self.committed is not None:
            raise ValueError("Transaction is already committed")

        if self._rolled_back:
            raise ValueError("Transaction is already rolled back")

    def _make_txn_selector(self):
        """Helper for :meth:`read`.

        :rtype:
            :class:`~.transaction_pb2.TransactionSelector`
        :returns: a selector configured for read-write transaction semantics.
        """
        self._check_state()
        return TransactionSelector(id=self._id)

    def begin(self):
        """Begin a transaction on the database.

        :rtype: bytes
        :returns: the ID for the newly-begun transaction.
        :raises: ValueError if the transaction is already begun, committed,
                 or rolled back.
        """
        if self._id is not None:
            raise ValueError("Transaction already begun")

        if self.committed is not None:
            raise ValueError("Transaction already committed")

        if self._rolled_back:
            raise ValueError("Transaction is already rolled back")

        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        txn_options = TransactionOptions(
            read_write=TransactionOptions.ReadWrite())
        response = api.begin_transaction(
            self._session.name, txn_options, options=options)
        self._id = response.id
        return self._id

    def rollback(self):
        """Roll back a transaction on the database."""
        self._check_state()
        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        api.rollback(self._session.name, self._id, options=options)
        self._rolled_back = True

    def commit(self):
        """Commit mutations to the database.

        :rtype: datetime
        :returns: timestamp of the committed changes.
        :raises: :exc:`ValueError` if there are no mutations to commit.
        """
        self._check_state()

        if len(self._mutations) == 0:
            raise ValueError("No mutations to commit")

        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        response = api.commit(
            self._session.name, self._mutations,
            transaction_id=self._id, options=options)
        self.committed = _pb_timestamp_to_datetime(
            response.commit_timestamp)
        return self.committed

    def __enter__(self):
        """Begin ``with`` block."""
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End ``with`` block."""
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
