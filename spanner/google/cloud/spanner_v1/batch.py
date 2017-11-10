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

"""Context manager for Cloud Spanner batched writes."""

from google.cloud.spanner_v1.proto.mutation_pb2 import Mutation
from google.cloud.spanner_v1.proto.transaction_pb2 import TransactionOptions

# pylint: disable=ungrouped-imports
from google.cloud._helpers import _pb_timestamp_to_datetime
from google.cloud.spanner_v1._helpers import _SessionWrapper
from google.cloud.spanner_v1._helpers import _make_list_value_pbs
from google.cloud.spanner_v1._helpers import _options_with_prefix
# pylint: enable=ungrouped-imports


class _BatchBase(_SessionWrapper):
    """Accumulate mutations for transmission during :meth:`commit`.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit
    """
    def __init__(self, session):
        super(_BatchBase, self).__init__(session)
        self._mutations = []

    def _check_state(self):
        """Helper for :meth:`commit` et al.

        Subclasses must override

        :raises: :exc:`ValueError` if the object's state is invalid for making
                 API requests.
        """
        raise NotImplementedError

    def insert(self, table, columns, values):
        """Insert one or more new table rows.

        :type table: str
        :param table: Name of the table to be modified.

        :type columns: list of str
        :param columns: Name of the table columns to be modified.

        :type values: list of lists
        :param values: Values to be modified.
        """
        self._mutations.append(Mutation(
            insert=_make_write_pb(table, columns, values)))

    def update(self, table, columns, values):
        """Update one or more existing table rows.

        :type table: str
        :param table: Name of the table to be modified.

        :type columns: list of str
        :param columns: Name of the table columns to be modified.

        :type values: list of lists
        :param values: Values to be modified.
        """
        self._mutations.append(Mutation(
            update=_make_write_pb(table, columns, values)))

    def insert_or_update(self, table, columns, values):
        """Insert/update one or more table rows.

        :type table: str
        :param table: Name of the table to be modified.

        :type columns: list of str
        :param columns: Name of the table columns to be modified.

        :type values: list of lists
        :param values: Values to be modified.
        """
        self._mutations.append(Mutation(
            insert_or_update=_make_write_pb(table, columns, values)))

    def replace(self, table, columns, values):
        """Replace one or more table rows.

        :type table: str
        :param table: Name of the table to be modified.

        :type columns: list of str
        :param columns: Name of the table columns to be modified.

        :type values: list of lists
        :param values: Values to be modified.
        """
        self._mutations.append(Mutation(
            replace=_make_write_pb(table, columns, values)))

    def delete(self, table, keyset):
        """Delete one or more table rows.

        :type table: str
        :param table: Name of the table to be modified.

        :type keyset: :class:`~google.cloud.spanner_v1.keyset.Keyset`
        :param keyset: Keys/ranges identifying rows to delete.
        """
        delete = Mutation.Delete(
            table=table,
            key_set=keyset.to_pb(),
        )
        self._mutations.append(Mutation(
            delete=delete))


class Batch(_BatchBase):
    """Accumulate mutations for transmission during :meth:`commit`.
    """
    committed = None
    """Timestamp at which the batch was successfully committed."""

    def _check_state(self):
        """Helper for :meth:`commit` et al.

        Subclasses must override

        :raises: :exc:`ValueError` if the object's state is invalid for making
                 API requests.
        """
        if self.committed is not None:
            raise ValueError("Batch already committed")

    def commit(self):
        """Commit mutations to the database.

        :rtype: datetime
        :returns: timestamp of the committed changes.
        """
        self._check_state()
        database = self._session._database
        api = database.spanner_api
        options = _options_with_prefix(database.name)
        txn_options = TransactionOptions(
            read_write=TransactionOptions.ReadWrite())
        response = api.commit(self._session.name, self._mutations,
                              single_use_transaction=txn_options,
                              options=options)
        self.committed = _pb_timestamp_to_datetime(
            response.commit_timestamp)
        return self.committed

    def __enter__(self):
        """Begin ``with`` block."""
        self._check_state()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """End ``with`` block."""
        if exc_type is None:
            self.commit()


def _make_write_pb(table, columns, values):
    """Helper for :meth:`Batch.insert` et aliae.

    :type table: str
    :param table: Name of the table to be modified.

    :type columns: list of str
    :param columns: Name of the table columns to be modified.

    :type values: list of lists
    :param values: Values to be modified.

    :rtype: :class:`google.cloud.spanner_v1.proto.mutation_pb2.Mutation.Write`
    :returns: Write protobuf
    """
    return Mutation.Write(
        table=table,
        columns=columns,
        values=_make_list_value_pbs(values),
    )
