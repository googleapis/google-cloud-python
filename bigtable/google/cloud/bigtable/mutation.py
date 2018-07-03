# Copyright 2018 Google LLC
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

"""User-friendly container for Google Cloud Bigtable Instance."""


from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import _to_bytes
from google.cloud.bigtable_v2.proto import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.proto import (
    bigtable_pb2 as table_v2_pb2)


class RowMutations(object):
    """ Provides methods to create row mutations, which are added to a
        google.bigtable.v2.MutateRowsRequest.Entry

        Arguments:
            row_key (bytes): Key of the Row in string.
    """

    def __init__(self, row_key):
        self.entry = table_v2_pb2.MutateRowsRequest.Entry(row_key=row_key)

    @property
    def mutations_entry(self):
        """ The MutateRowsRequest.Entry

        Returns:
            `Entry <google.bigtable.v2.MutateRowsRequest.Entry>`
             An ``Entry`` for a MutateRowsRequest message.
        """
        return self.entry

    def set_cell(self, family_name, column_id, value, timestamp=None):
        """Create the mutation request message for SetCell and add it to the
            list of mutations in the MutateRowsRequest.Entry

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (bytes):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            value (bytes):
                The value to be written into the specified cell.
            timestamp (datetime.datetime):
                (optional) The timestamp of the cell into which new data should
                be written. Use -1 for current Bigtable server time. Otherwise,
                the client should set this value itself, noting that the
                default value is a timestamp of zero if the field is left
                unspecified. Values must match the granularity of the table
                (e.g. micros, millis).
        """
        if timestamp is None:
            # Use -1 for current Bigtable server time.
            timestamp_micros = -1
        else:
            timestamp_micros = _microseconds_from_datetime(timestamp)
            # Truncate to millisecond granularity.
            timestamp_micros -= (timestamp_micros % 1000)

        set_cell_mutation = data_v2_pb2.Mutation.SetCell(
            family_name=family_name,
            column_qualifier=column_id,
            timestamp_micros=timestamp_micros,
            value=value
        )
        self.entry.mutations.add(set_cell=set_cell_mutation)

    def delete_cells(self, family_name, columns, time_range=None):
        """Create the mutation request message for DeleteFromColumn and
            add it to the list of mutations in the MutateRowsRequest.Entry

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            columns (list of bytes):
                The columns within the column family that will have cells
                deleted.
            time_range (TimestampRange):
                (optional) The range of timestamps within which cells should be
                deleted.
        """
        for column_id in columns:
            delete_from_column_mutation = (
                data_v2_pb2.Mutation.DeleteFromColumn(
                    family_name=family_name,
                    column_qualifier=column_id,
                    time_range=time_range))

            self.entry.mutations.add(delete_from_column=delete_from_column_mutation)

    def delete_from_family(self, family_name):
        """Create the mutation request message for DeleteFromFamily and add
            it to the list of mutations in the MutateRowsRequest.Entry

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
        """
        delete_from_family_mutation = data_v2_pb2.Mutation.DeleteFromFamily(
            family_name=family_name
        )
        mutation_message = data_v2_pb2.Mutation(
            delete_from_family=delete_from_family_mutation)
        self.entry.mutations.add(delete_from_family=delete_from_family_mutation)

    def delete_row(self):
        """Create the mutation request message for DeleteFromRow and add it
            to the list of mutations

        """
        delete_from_row_mutation = data_v2_pb2.Mutation.DeleteFromRow()
        self.entry.mutations.add(delete_from_row=delete_from_row_mutation)
