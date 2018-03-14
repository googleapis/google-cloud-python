from google.cloud.bigtable_v2.types import (
    data_pb2 as data_v2_pb2)
from google.cloud.bigtable_v2.types import bigtable_pb2


class MutateRows(object):
    def __init__(self, table_name, client):
        super(MutateRows, self).__init__()
        self.table_name = table_name
        self.client = client
        self.row_mutations = {}

    def set_cell(self, row_key, family_name, column_id, value, timestamp=None):
        row_mutations = self.row_mutations.setdefault(row_key, [])
        set_cell = SetCellMutation(family_name, column_id, value, timestamp)
        row_mutations.append(set_cell.mutation_request)

    def mutate(self):
        entries = []
        for row_key, mutations in self.row_mutations.items():
            entry = bigtable_pb2.MutateRowsRequest.Entry(
                row_key=row_key,
                mutations=mutations
            )
            entries.append(entry)

        return self.client.mutate_rows(self.table_name, entries, retry=None)


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
