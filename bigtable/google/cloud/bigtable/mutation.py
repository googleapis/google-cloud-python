from google.cloud.bigtable_v2.proto import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.proto.bigtable_pb2 import MutateRowsRequest


class RowMutations():

    def __init__(self, row_key, table_name):
        self.row_key = row_key
        self.table_name = table_name
        self.mutations = []

    def set_cell(self, row_key, family_name, column_id, value, timestamp=None):
        # create the SetCellMutation
        # add the mutation to list
        mutation = SetCellMutation(family_name, column_id, value, timestamp)
        self.mutations.append(mutation.mutation_request)

    def delete_from_column(self, row_key, family_name, column_id,
                           time_range=None):
        # create the DeleteFromColumnMutation
        # add the mutation to list
        mutation = DeleteFromColumnMutation(family_name, column_id, time_range)
        self.mutations.append(mutation.mutation_request)

    def create_entry(self):
        # create the Entry for the mutations
        entry = MutateRowsRequest.Entry(row_key=self.row_key)
        for mutation in self.mutations:
            # create Mutation
            entry.mutations.add().CopyFrom(mutation)
        return entry


class MutateRows():
    def __init__(self, table_name, client):
        self.table_name = table_name
        self.client = client
        self.entries = []

    def add_row_mutations(self, row_mutations):
        # turn the row_mutations into an Entry
        entry = row_mutations.create_entry()
        self.entries.append(entry)

    def create_request(self):
        request = MutateRowsRequest(table_name=self.table_name,
                                    entries=self.entries)
        return self.client._mutate_rows(request)


class SetCellMutation(object):
    def __init__(self, family_name, column_id, value, timestamp):
        super(SetCellMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.value = value
        self.timestamp = timestamp

    @property
    def mutation_request(self):
        set_cell_mutation = data_v2_pb2.Mutation.SetCell(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            timestamp_micros=self.timestamp,
            value=self.value,
        )
        return data_v2_pb2.Mutation(set_cell=set_cell_mutation)


class DeleteFromColumnMutation(object):
    def __init__(self, family_name, column_id, time_range):
        super(DeleteFromColumnMutation, self).__init__()
        self.family_name = family_name
        self.column_id = column_id
        self.time_range = time_range

    @property
    def mutation_request(self):
        delete_from_column_mutation = data_v2_pb2.Mutation.DeleteFromColumn(
            family_name=self.family_name,
            column_qualifier=self.column_id,
            time_range=self.time_range
        )
        return data_v2_pb2.Mutation(
            delete_from_column=delete_from_column_mutation)
