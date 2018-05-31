from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import _to_bytes
from google.cloud.bigtable_v2.proto import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.proto import (
    bigtable_pb2 as table_v2_pb2)


class RowMutations(object):
    """Create Entry using list of mutations

        Arguments:
            row_key (str): Key of the Row in string.
    """
    ALL_COLUMNS = object()
    """Sentinel value used to indicate all columns in a column family."""

    def __init__(self, row_key, app_profile_id=None):
        self.row_key = _to_bytes(row_key)
        self.app_profile_id = app_profile_id
        self.mutations = []

    def set_cell(self, family_name, column_id, value, timestamp=None):
        """Create the mutation request message for SetCell and add it to the
            list of mutations

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (str):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            value (str):
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
            column_qualifier=_to_bytes(column_id),
            timestamp_micros=timestamp_micros,
            value=_to_bytes(value)
        )
        mutation_message = data_v2_pb2.Mutation(set_cell=set_cell_mutation)
        self.mutations.append(mutation_message)

    def delete_cells(self, family_name, columns, time_range=None):
        """Create the mutation request message for DeleteFromColumn and
            add it to the list of mutations

        Arguments:
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            columns (list):
                The columns within the column family that will have cells
                deleted. If :attr:`ALL_COLUMNS` is used then the entire
                column family will be deleted from the row.
            time_range (TimestampRange):
                (optional) The range of timestamps within which cells should be
                deleted.
        """
        if columns is self.ALL_COLUMNS:
            self.delete_from_family(family_name)
        else:
            for column_id in columns:
                delete_from_column_mutation = (
                    data_v2_pb2.Mutation.DeleteFromColumn(
                        family_name=family_name,
                        column_qualifier=_to_bytes(column_id),
                        time_range=time_range))

                mutation_message = data_v2_pb2.Mutation(
                    delete_from_column=delete_from_column_mutation)
                self.mutations.append(mutation_message)

    def delete_from_family(self, family_name):
        """Create the mutation request message for DeleteFromFamily and add
        it to the list of mutations

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
        self.mutations.append(mutation_message)

    def delete(self):
        """Create the mutation request message for DeleteFromRow and add it
        to the list of mutations"""
        delete_from_row_mutation = data_v2_pb2.Mutation.DeleteFromRow()
        mutation_message = data_v2_pb2.Mutation(
            delete_from_row=delete_from_row_mutation)
        self.mutations.append(mutation_message)

    def create_entry(self):
        """Create a MutateRowsRequest Entry from the list of mutations

        Returns:
            `Entry <google.bigtable.v2.MutateRowsRequest.Entry>`
             An ``Entry`` for a MutateRowsRequest message.
        """
        entry = table_v2_pb2.MutateRowsRequest.Entry(row_key=self.row_key)
        for mutation in self.mutations:
            entry.mutations.add().CopyFrom(mutation)
        return entry
