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

import base64
import datetime
import decimal
import math
import unittest
import zoneinfo

import pyarrow as pa
from google.protobuf.struct_pb2 import ListValue, Struct, Value

import google_cloud_spanner_arrow as sa
from google_cloud_spanner_arrow import cext, python


class TestSpannerArrowCExtension(unittest.TestCase):
    def test_implementation_is_c(self):
        self.assertEqual(sa.implementation, "c")

    def test_empty_rows(self):
        fields = [("id", 2), ("name", 6)]
        batch = sa.rows_to_arrow_batch(fields, [])
        self.assertEqual(batch.num_rows, 0)
        self.assertEqual(batch.num_columns, 2)
        self.assertEqual(batch.schema.names, ["id", "name"])
        self.assertEqual(batch.schema.field("id").type, pa.int64())
        self.assertEqual(batch.schema.field("name").type, pa.string())

    def test_basic_types(self):
        fields = [
            ("id", 2),
            ("name", 6),
            ("active", 1),
            ("score", 3),
            ("f32", 15),
        ]
        rows = [
            ["1", "Alice", True, 95.5, 12.5],
            ["2", "Bob", False, 82.0, -0.5],
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)
        self.assertEqual(batch.column("id").to_pylist(), [1, 2])
        self.assertEqual(batch.column("name").to_pylist(), ["Alice", "Bob"])
        self.assertEqual(batch.column("active").to_pylist(), [True, False])
        self.assertEqual(batch.column("score").to_pylist(), [95.5, 82.0])
        self.assertAlmostEqual(batch.column("f32").to_pylist()[0], 12.5, places=4)
        self.assertAlmostEqual(batch.column("f32").to_pylist()[1], -0.5, places=4)

    def test_protobuf_value_objects(self):
        fields = [
            ("id", 2),
            ("name", 6),
            ("active", 1),
            ("score", 3),
        ]
        rows = [
            [
                Value(string_value="10"),
                Value(string_value="Charlie"),
                Value(bool_value=True),
                Value(number_value=88.5),
            ],
            [
                Value(string_value="20"),
                Value(string_value="David"),
                Value(bool_value=False),
                Value(number_value=99.0),
            ],
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)
        self.assertEqual(batch.column("id").to_pylist(), [10, 20])
        self.assertEqual(batch.column("name").to_pylist(), ["Charlie", "David"])
        self.assertEqual(batch.column("active").to_pylist(), [True, False])
        self.assertEqual(batch.column("score").to_pylist(), [88.5, 99.0])

    def test_null_values(self):
        fields = [
            ("id", 2),
            ("name", 6),
            ("date_col", 5),
            ("ts_col", 4),
            ("num_col", 10),
            ("bytes_col", 7),
        ]
        rows = [
            [None, None, None, None, None, None],
            [
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
            ],
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)
        for col_name in ["id", "name", "date_col", "ts_col", "num_col", "bytes_col"]:
            self.assertEqual(batch.column(col_name).to_pylist(), [None, None])

    def test_advanced_types_date_timestamp_numeric_bytes(self):
        fields = [
            ("date_col", 5),
            ("ts_col", 4),
            ("num_col", 10),
            ("bytes_col", 7),
        ]
        raw_bytes = b"quantum-accelerator-bytes"
        b64_bytes = base64.b64encode(raw_bytes).decode("ascii")

        rows = [
            [
                Value(string_value="2023-01-15"),
                Value(string_value="2023-01-15T10:30:00.123456Z"),
                Value(string_value="12345.678900000"),
                Value(string_value=b64_bytes),
            ],
            [
                "2024-12-31",
                "2024-12-31T23:59:59.999999Z",
                "-0.000000001",
                raw_bytes,
            ],
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 2)

        # Dates
        self.assertEqual(
            batch.column("date_col").to_pylist(),
            [datetime.date(2023, 1, 15), datetime.date(2024, 12, 31)],
        )

        # Timestamps (UTC)
        utc = zoneinfo.ZoneInfo("UTC")
        self.assertEqual(
            batch.column("ts_col").to_pylist(),
            [
                datetime.datetime(2023, 1, 15, 10, 30, 0, 123456, tzinfo=utc),
                datetime.datetime(2024, 12, 31, 23, 59, 59, 999999, tzinfo=utc),
            ],
        )

        # Numerics
        self.assertEqual(
            batch.column("num_col").to_pylist(),
            [decimal.Decimal("12345.678900000"), decimal.Decimal("-0.000000001")],
        )

        # Bytes
        self.assertEqual(batch.column("bytes_col").to_pylist(), [raw_bytes, raw_bytes])

    def test_float_nan_and_infinities(self):
        fields = [("val_f64", 3), ("val_f32", 15)]
        rows = [
            [Value(string_value="NaN"), Value(string_value="NaN")],
            [Value(string_value="Infinity"), Value(string_value="Infinity")],
            [Value(string_value="-Infinity"), Value(string_value="-Infinity")],
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 3)

        f64_list = batch.column("val_f64").to_pylist()
        self.assertTrue(math.isnan(f64_list[0]))
        self.assertEqual(f64_list[1], float("inf"))
        self.assertEqual(f64_list[2], float("-inf"))

        f32_list = batch.column("val_f32").to_pylist()
        self.assertTrue(math.isnan(f32_list[0]))
        self.assertEqual(f32_list[1], float("inf"))
        self.assertEqual(f32_list[2], float("-inf"))

    def test_arrays_and_structs(self):
        fields = [
            ("arr", 8, ("item", 6)),
            (
                "st",
                9,
                (
                    ("f_int", 2),
                    ("f_str", 6),
                ),
            ),
        ]
        rows = [
            [
                Value(
                    list_value=ListValue(
                        values=[Value(string_value="x"), Value(string_value="y")]
                    )
                ),
                Value(
                    struct_value=Struct(
                        fields={
                            "f_int": Value(string_value="10"),
                            "f_str": Value(string_value="hello"),
                        }
                    )
                ),
            ]
        ]
        batch = sa.rows_to_arrow_batch(fields, rows)
        self.assertEqual(batch.num_rows, 1)
        self.assertEqual(batch.column("arr").to_pylist(), [["x", "y"]])
        self.assertEqual(
            batch.column("st").to_pylist(), [{"f_int": 10, "f_str": "hello"}]
        )


if __name__ == "__main__":
    unittest.main()
