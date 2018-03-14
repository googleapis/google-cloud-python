# Copyright 2015 Google LLC
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

import mock


class TestMutateRows(unittest.TestCase):
    PROJECT_ID = 'project-id'
    INSTANCE_ID = 'instance-id'
    INSTANCE_NAME = ('projects/' + PROJECT_ID + '/instances/' + INSTANCE_ID)
    TABLE_ID = 'table-id'
    TABLE_NAME = INSTANCE_NAME + '/tables/' + TABLE_ID
    ROW_KEY = b'row-key'
    FAMILY_NAME = u'family'
    QUALIFIER = b'qualifier'
    TIMESTAMP_MICROS = 100
    VALUE = b'value'

    def test_mutate(self):
        from google.cloud.bigtable.mutation import MutateRows

        client = mock.MagicMock()

        mutate_rows = MutateRows(self.TABLE_NAME, client)

        mutate_rows.set_cell(
            self.ROW_KEY,
            self.FAMILY_NAME,
            self.QUALIFIER,
            self.VALUE,
            self.TIMESTAMP_MICROS
        )

        expected_result = mutate_rows.mutate()

        result = None
