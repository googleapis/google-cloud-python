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


import unittest

from google.cloud._helpers import _to_bytes


class TestMutateRows(unittest.TestCase):
    from grpc import StatusCode

    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    TABLE_ID = 'table-id'
    ROW_KEY = 'row-key'
    ROW_KEY_1 = 'row-key-1'
    ROW_KEY_2 = 'row-key-2'
    FAMILY_NAME = 'family'
    QUALIFIER = b'qualifier'
    TIMESTAMP_MICROS = 100
    VALUE = b'value'
    RETRYABLE = StatusCode.DEADLINE_EXCEEDED.value[0]
    SUCCESS = StatusCode.OK.value[0]

    @staticmethod
    def _get_target_class():
        from google.cloud.bigtable.mutation import RowMutations

        return RowMutations

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_set_cell(self):
        request = _MutateRowsRequestPB()
        request.SetCell(
            family_name=self.FAMILY_NAME,
            column_qualifier=_to_bytes(self.QUALIFIER),
            value=_to_bytes(self.VALUE)
        )

        mutate_rows = self._make_one(row_key=self.ROW_KEY)

        mutate_rows.set_cell(
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE
        )

        expected_result = mutate_rows.mutations[0]

        self.assertEqual(request.SetCell, expected_result.SetCell)

    def test_delete_cells(self):
        columns = ['column1']
        request = _MutateRowsRequestPB()
        request.DeleteFromColumn(
            family_name=self.FAMILY_NAME,
            column_qualifier=_to_bytes(columns[0])
        )

        mutate_rows = self._make_one(row_key=self.ROW_KEY)

        columns = ['column1']

        mutate_rows.delete_cells(
            self.FAMILY_NAME,
            columns
        )

        expected_result = mutate_rows.mutations[0]

        self.assertEqual(request.DeleteFromColumn,
                         expected_result.DeleteFromColumn)

    def test_delete_from_family(self):
        request = _MutateRowsRequestPB()
        request.DeleteFromFamily(
            family_name=self.FAMILY_NAME
        )

        mutate_rows = self._make_one(row_key=self.ROW_KEY)

        mutate_rows.delete_from_family(
            self.FAMILY_NAME
        )

        expected_result = mutate_rows.mutations[0]

        self.assertEqual(request.DeleteFromFamily,
                         expected_result.DeleteFromFamily)

    def test_delete(self):
        request = _MutateRowsRequestPB()
        request.DeleteFromRow()

        mutate_rows = self._make_one(row_key=self.ROW_KEY)

        mutate_rows.delete()

        expected_result = mutate_rows.mutations[0]

        self.assertEqual(request.DeleteFromRow,
                         expected_result.DeleteFromRow)


def _MutateRowsRequestPB(*args, **kw):
    from google.cloud.bigtable_v2.proto.data_pb2 import Mutation

    return Mutation(*args, **kw)
