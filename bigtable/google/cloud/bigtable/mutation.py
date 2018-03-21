from google.cloud.bigtable_v2.proto import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.proto.bigtable_pb2 import MutateRowsRequest


class MutateRowsEntry(object):
    """Creating Entry using list of mutations

    Arguments:
        row_key (bytes): Key of the Row in bytes.
    """

    def __init__(self, row_key):
        self.row_key = row_key
        self.mutations = []

    def set_cell(self, row_key, family_name, column_id, value, timestamp=None):
        """Creating the mutation request message for SetCell and adding it to
            the list of mutations

        Arguments:
            row_key (bytes): Key of the Row.
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (bytes):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            value (bytes):
                The value to be written into the specified cell.
            timestamp (int):
                (optional) The timestamp of the cell into which new data should
                be written. Use -1 for current Bigtable server time. Otherwise,
                the client should set this value itself, noting that the
                default value is a timestamp of zero if the field is left
                unspecified. Values must match the granularity of the table
                (e.g. micros, millis).
        """
        mutation = SetCellMutation(family_name, column_id, value, timestamp)
        self.mutations.append(mutation.mutation_request)

    def delete_from_column(self, row_key, family_name, column_id,
                           time_range=None):
        """Creating the mutation request message for DeleteFromColumn and
            adding it to the list of mutations

        Arguments:
            row_key (bytes): Key of the Row.
            family_name (str):
                The name of the family into which new data should be written.
                Must match ``[-_.a-zA-Z0-9]+``.
            column_id (bytes):
                The qualifier of the column into which new data should be
                written. Can be any byte string, including the empty string.
            time_range (TimestampRange):
                (optional) The range of timestamps within which cells should be
                deleted.
        """
        mutation = DeleteFromColumnMutation(family_name, column_id, time_range)
        self.mutations.append(mutation.mutation_request)

    def create_entry(self):
        """Create Entry from list of mutations

        Returns:
            `Entry <google.bigtable.v2.MutateRowsRequest.Entry>`
            A ``Entry`` message.
        """
        entry = MutateRowsRequest.Entry(row_key=self.row_key)
        for mutation in self.mutations:
            entry.mutations.add().CopyFrom(mutation)
        return entry


class MutateRows(object):
    """Creating Entry using list of mutations

    Arguments:
        table_name (bytes): Key of the Row in bytes.
        client (class):
            `Client <google.cloud.bigtable_v2.BigtableClient>`
            The client class of BigtableClient.
    """

    def __init__(self, table_name, client):
        self.table_name = table_name
        self.client = client
        self.entries = []

    def add_row_mutations_entry(self, mutate_rows_entry):
        """Create list of entries of ``Entry``

        Arguments:
            mutate_rows_entry (object): Class of ``MutateRowsEntry``
        """
        entry = mutate_rows_entry.create_entry()
        self.entries.append(entry)

    def mutate_rows(self):
        """Call on GAPIC API for MutateRows

        Returns:
            Iterable[~google.cloud.bigtable_v2.proto.MutateRowsResponse].
        """
        return self.client.mutate_rows(table_name=self.table_name,
                                       entries=self.entries)


class SetCellMutation(object):
    """Creating the mutation request message for SetCell and adding it to the
        list of mutations

    Arguments:
        family_name (str):
            The name of the family into which new data should be written.
            Must match ``[-_.a-zA-Z0-9]+``.
        column_id (bytes):
            The qualifier of the column into which new data should be
            written. Can be any byte string, including the empty string.
        value (bytes):
            The value to be written into the specified cell.
        timestamp (int):
            (optional) The timestamp of the cell into which new data should
            be written. Use -1 for current Bigtable server time. Otherwise,
            the client should set this value itself, noting that the
            default value is a timestamp of zero if the field is left
            unspecified. Values must match the granularity of the table
            (e.g. micros, millis).
    """

    def __init__(self, family_name, column_id, value, timestamp):
        super(SetCellMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.value = value
        self.timestamp = timestamp

    @property
    def mutation_request(self):
        """message: Mutation of the SetCell."""
        set_cell_mutation = data_v2_pb2.Mutation.SetCell(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            timestamp_micros=self.timestamp,
            value=self.value,
        )
        return data_v2_pb2.Mutation(set_cell=set_cell_mutation)


class DeleteFromColumnMutation(object):
    """Creating the mutation request message for DeleteFromColumn and
        adding it to the list of mutations

    Arguments:
        family_name (str):
            The name of the family into which new data should be written.
            Must match ``[-_.a-zA-Z0-9]+``.
        column_id (bytes):
            The qualifier of the column into which new data should be
            written. Can be any byte string, including the empty string.
        time_range (TimestampRange):
            (optional) The range of timestamps within which cells should be
            deleted.
    """

    def __init__(self, family_name, column_id, time_range):
        super(DeleteFromColumnMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.time_range = time_range

    @property
    def mutation_request(self):
        """message: Mutation of the DeleteFromColumn."""
        delete_from_column_mutation = data_v2_pb2.Mutation.DeleteFromColumn(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            time_range=self.time_range
        )
        return data_v2_pb2.Mutation(
            delete_from_column=delete_from_column_mutation)
