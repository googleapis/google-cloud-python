# Copyright 2016 Google LLC All rights reserved.
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

from google.protobuf.struct_pb2 import Struct

from google.cloud._helpers import _pb_timestamp_to_datetime
from google.cloud.spanner_v1._helpers import _make_value_pb
from google.cloud.spanner_v1._helpers import _metadata_with_prefix
from google.cloud.spanner_v1.proto.transaction_pb2 import TransactionSelector
from google.cloud.spanner_v1.proto.transaction_pb2 import TransactionOptions
from google.cloud.spanner_v1.snapshot import _SnapshotBase
from google.cloud.spanner_v1.batch import _BatchBase


class Transaction(_SnapshotBase, _BatchBase):
    """Implement read-write transaction semantics for a session.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit

    :raises ValueError: if session has an existing transaction
    """

    committed = None
    """Timestamp at which the transaction was successfully committed."""
    _rolled_back = False
    _multi_use = True
    _execute_sql_count = 0

    def __init__(self, session):
        if session._transaction is not None:
            raise ValueError("Session has existing transaction.")

        super(Transaction, self).__init__(session)

    def _check_state(self):
        """Helper for :meth:`commit` et al.

        :raises: :exc:`ValueError` if the object's state is invalid for making
                 API requests.
        """
        if self._transaction_id is None:
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
        return TransactionSelector(id=self._transaction_id)

    def begin(self):
        """Begin a transaction on the database.

        :rtype: bytes
        :returns: the ID for the newly-begun transaction.
        :raises ValueError:
            if the transaction is already begun, committed, or rolled back.
        """
        if self._transaction_id is not None:
            raise ValueError("Transaction already begun")

        if self.committed is not None:
            raise ValueError("Transaction already committed")

        if self._rolled_back:
            raise ValueError("Transaction is already rolled back")

        database = self._session._database
        api = database.spanner_api
        metadata = _metadata_with_prefix(database.name)
        txn_options = TransactionOptions(read_write=TransactionOptions.ReadWrite())
        response = api.begin_transaction(
            self._session.name, txn_options, metadata=metadata
        )
        self._transaction_id = response.id
        return self._transaction_id

    def rollback(self):
        """Roll back a transaction on the database."""
        self._check_state()
        database = self._session._database
        api = database.spanner_api
        metadata = _metadata_with_prefix(database.name)
        api.rollback(self._session.name, self._transaction_id, metadata=metadata)
        self._rolled_back = True
        del self._session._transaction

    def commit(self):
        """Commit mutations to the database.

        :rtype: datetime
        :returns: timestamp of the committed changes.
        :raises ValueError: if there are no mutations to commit.
        """
        self._check_state()

        database = self._session._database
        api = database.spanner_api
        metadata = _metadata_with_prefix(database.name)
        response = api.commit(
            self._session.name,
            self._mutations,
            transaction_id=self._transaction_id,
            metadata=metadata,
        )
        self.committed = _pb_timestamp_to_datetime(response.commit_timestamp)
        del self._session._transaction
        return self.committed

    def execute_update(self, dml, params=None, param_types=None, query_mode=None):
        """Perform an ``ExecuteSql`` API request with DML.

        :type dml: str
        :param dml: SQL DML statement

        :type params: dict, {str -> column value}
        :param params: values for parameter replacement.  Keys must match
                       the names used in ``dml``.

        :type param_types: dict[str -> Union[dict, .types.Type]]
        :param param_types:
            (Optional) maps explicit types for one or more param values;
            required if parameters are passed.

        :type query_mode:
            :class:`google.cloud.spanner_v1.proto.ExecuteSqlRequest.QueryMode`
        :param query_mode: Mode governing return of results / query plan. See
            https://cloud.google.com/spanner/reference/rpc/google.spanner.v1#google.spanner.v1.ExecuteSqlRequest.QueryMode1

        :rtype: int
        :returns: Count of rows affected by the DML statement.
        """
        if params is not None:
            if param_types is None:
                raise ValueError("Specify 'param_types' when passing 'params'.")
            params_pb = Struct(
                fields={key: _make_value_pb(value) for key, value in params.items()}
            )
        else:
            params_pb = None

        database = self._session._database
        metadata = _metadata_with_prefix(database.name)
        transaction = self._make_txn_selector()
        api = database.spanner_api

        response = api.execute_sql(
            self._session.name,
            dml,
            transaction=transaction,
            params=params_pb,
            param_types=param_types,
            query_mode=query_mode,
            seqno=self._execute_sql_count,
            metadata=metadata,
        )

        self._execute_sql_count += 1
        return response.stats.row_count_exact

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
