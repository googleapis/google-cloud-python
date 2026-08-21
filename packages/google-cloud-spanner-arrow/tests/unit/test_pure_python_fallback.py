# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import decimal
import unittest
import zoneinfo

import pyarrow as pa
from google.protobuf.struct_pb2 import Value

from google_cloud_spanner_arrow import python


class TestSpannerArrowPurePythonFallback(unittest.TestCase):
    def test_basic_types(self):
        fields = [
            ("id", 2),
            ("name", 6),
            ("active", 1),
            ("score", 3),
        ]
        rows = [
            ["1", "Alice", True, 95.5],
            ["2", "Bob", False, 82.0],
        ]
        batch = python.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)
        self.assertEqual(batch.column("id").to_pylist(), [1, 2])
        self.assertEqual(batch.column("name").to_pylist(), ["Alice", "Bob"])
        self.assertEqual(batch.column("active").to_pylist(), [True, False])
        self.assertEqual(batch.column("score").to_pylist(), [95.5, 82.0])

    def test_nulls(self):
        fields = [("id", 2), ("name", 6)]
        rows = [[None, None], [Value(null_value=0), Value(null_value=0)]]
        batch = python.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)
        self.assertEqual(batch.column("id").to_pylist(), [None, None])
        self.assertEqual(batch.column("name").to_pylist(), [None, None])

    def test_advanced_types(self):
        fields = [
            ("date_col", 5),
            ("ts_col", 4),
            ("num_col", 10),
            ("bytes_col", 7),
        ]
        raw_bytes = b"fallback-bytes"
        rows = [
            [
                Value(string_value="2023-01-15"),
                Value(string_value="2023-01-15T10:30:00.123456Z"),
                Value(string_value="12345.678900000"),
                raw_bytes,
            ]
        ]
        batch = python.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 1)
        self.assertEqual(
            batch.column("date_col").to_pylist(), [datetime.date(2023, 1, 15)]
        )
        utc = zoneinfo.ZoneInfo("UTC")
        self.assertEqual(
            batch.column("ts_col").to_pylist(),
            [datetime.datetime(2023, 1, 15, 10, 30, 0, 123456, tzinfo=utc)],
        )
        self.assertEqual(
            batch.column("num_col").to_pylist(), [decimal.Decimal("12345.678900000")]
        )
        self.assertEqual(batch.column("bytes_col").to_pylist(), [raw_bytes])


if __name__ == "__main__":
    unittest.main()
