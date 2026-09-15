# Copyright 2026 Google LLC All rights reserved.
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

import base64
import decimal
import unittest
from unittest import mock

from google.protobuf.struct_pb2 import ListValue, Struct, Value

from google.cloud.spanner_v1 import _arrow, StructType, Type
from google.cloud.spanner_v1.streamed import StreamedResultSet
from google.cloud.spanner_v1.types.result_set import (
    PartialResultSet,
    ResultSetMetadata,
)
from google.cloud.spanner_v1.types.type import TypeCode

try:
    import pyarrow as pa
    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False


class _MockIterator(object):
    def __init__(self, *values):
        self._values = list(values)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._values:
            raise StopIteration
        return self._values.pop(0)


@unittest.skipUnless(_HAS_PYARROW, "pyarrow is required for these tests")
class TestArrowHelpers(unittest.TestCase):
    def test_spanner_type_to_arrow_type(self):
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.BOOL)), pa.bool_())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.INT64)), pa.int64())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.FLOAT32)), pa.float32())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.FLOAT64)), pa.float64())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.STRING)), pa.string())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.BYTES)), pa.binary())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.TIMESTAMP)), pa.timestamp("us", tz="UTC"))
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.DATE)), pa.date32())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.NUMERIC)), pa.decimal128(38, 9))
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.JSON)), pa.string())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.PROTO)), pa.binary())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.ENUM)), pa.int64())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.INTERVAL)), pa.string())
        self.assertEqual(_arrow.spanner_type_to_arrow_type(Type(code=TypeCode.UUID)), pa.string())

        # Array of INT64
        array_type = Type(code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64))
        self.assertEqual(_arrow.spanner_type_to_arrow_type(array_type), pa.list_(pa.int64()))

        # Struct
        struct_type = Type(
            code=TypeCode.STRUCT,
            struct_type=StructType(
                fields=[
                    StructType.Field(name="f1", type_=Type(code=TypeCode.STRING)),
                    StructType.Field(name="f2", type_=Type(code=TypeCode.INT64)),
                ]
            ),
        )
        expected_struct = pa.struct([pa.field("f1", pa.string()), pa.field("f2", pa.int64())])
        self.assertEqual(_arrow.spanner_type_to_arrow_type(struct_type), expected_struct)

    def test_spanner_schema_to_arrow_schema(self):
        fields = [
            StructType.Field(name="col_id", type_=Type(code=TypeCode.INT64)),
            StructType.Field(name="col_name", type_=Type(code=TypeCode.STRING)),
        ]
        schema = _arrow.spanner_schema_to_arrow_schema(fields)
        self.assertEqual(len(schema), 2)
        self.assertEqual(schema.field("col_id").type, pa.int64())
        self.assertEqual(schema.field("col_name").type, pa.string())

    def test_extract_cell_value(self):
        # Null
        val_null = Value(null_value=0)
        self.assertIsNone(_arrow._extract_cell_value(val_null, TypeCode.INT64))

        # Bool
        val_bool = Value(bool_value=True)
        self.assertTrue(_arrow._extract_cell_value(val_bool, TypeCode.BOOL))

        # Number
        val_num = Value(number_value=3.14)
        self.assertEqual(_arrow._extract_cell_value(val_num, TypeCode.FLOAT64), 3.14)

        # String int64
        val_int = Value(string_value="123456")
        self.assertEqual(_arrow._extract_cell_value(val_int, TypeCode.INT64), "123456")

        # Bytes (base64)
        raw_bytes = b"hello world"
        b64_str = base64.b64encode(raw_bytes).decode("ascii")
        val_bytes = Value(string_value=b64_str)
        self.assertEqual(_arrow._extract_cell_value(val_bytes, TypeCode.BYTES), raw_bytes)

        # Float NaN
        val_nan = Value(string_value="NaN")
        import math
        self.assertTrue(math.isnan(_arrow._extract_cell_value(val_nan, TypeCode.FLOAT64)))

        # List
        val_list = Value(list_value=ListValue(values=[Value(string_value="a"), Value(string_value="b")]))
        self.assertEqual(_arrow._extract_cell_value(val_list, TypeCode.ARRAY), ["a", "b"])

    def test_check_pyarrow_missing(self):
        with mock.patch("google.cloud.spanner_v1._arrow._HAS_PYARROW", False):
            with self.assertRaises(ImportError):
                _arrow._check_pyarrow()


@unittest.skipUnless(_HAS_PYARROW, "pyarrow is required for these tests")
class TestStreamedResultSetArrow(unittest.TestCase):
    def _make_metadata(self, fields):
        metadata = ResultSetMetadata(
            row_type=StructType(fields=[])
        )
        for name, code in fields:
            metadata.row_type.fields.append(
                StructType.Field(name=name, type_=Type(code=code))
            )
        return metadata

    def _make_partial_result_set(
        self, values=(), metadata=None, stats=None, chunked_value=False, last=False
    ):
        results = PartialResultSet(
            metadata=metadata, stats=stats, chunked_value=chunked_value, last=last
        )
        for v in values:
            results.values.append(v)
        return results

    def test_to_arrow_empty(self):
        iterator = _MockIterator()
        streamed = StreamedResultSet(iterator)
        table = streamed.to_arrow()
        self.assertEqual(table.num_rows, 0)
        self.assertEqual(table.num_columns, 0)

    def test_to_arrow_basic_query(self):
        metadata = self._make_metadata([
            ("id", TypeCode.INT64),
            ("name", TypeCode.STRING),
            ("active", TypeCode.BOOL),
            ("score", TypeCode.FLOAT64),
        ])

        prs1 = self._make_partial_result_set(
            metadata=metadata,
            values=[
                Value(string_value="1"),
                Value(string_value="Alice"),
                Value(bool_value=True),
                Value(number_value=95.5),
                Value(string_value="2"),
                Value(string_value="Bob"),
                Value(bool_value=False),
                Value(number_value=82.0),
            ],
            last=True,
        )

        streamed = StreamedResultSet(_MockIterator(prs1))
        table = streamed.to_arrow()

        self.assertEqual(table.num_rows, 2)
        self.assertEqual(table.num_columns, 4)
        self.assertEqual(table.column("id").to_pylist(), [1, 2])
        self.assertEqual(table.column("name").to_pylist(), ["Alice", "Bob"])
        self.assertEqual(table.column("active").to_pylist(), [True, False])
        self.assertEqual(table.column("score").to_pylist(), [95.5, 82.0])

    def test_to_arrow_batches_chunk_size(self):
        metadata = self._make_metadata([("id", TypeCode.INT64)])
        values = [Value(string_value=str(i)) for i in range(10)]
        prs = self._make_partial_result_set(metadata=metadata, values=values, last=True)

        streamed = StreamedResultSet(_MockIterator(prs))
        batches = list(streamed.to_arrow_batches(max_chunk_size=3))

        self.assertEqual(len(batches), 4)  # 3, 3, 3, 1
        self.assertEqual(batches[0].num_rows, 3)
        self.assertEqual(batches[1].num_rows, 3)
        self.assertEqual(batches[2].num_rows, 3)
        self.assertEqual(batches[3].num_rows, 1)

        # Verify combined
        table = pa.Table.from_batches(batches)
        self.assertEqual(table.column("id").to_pylist(), list(range(10)))

    def test_to_arrow_with_chunked_values(self):
        metadata = self._make_metadata([
            ("id", TypeCode.INT64),
            ("description", TypeCode.STRING),
        ])

        # Chunk 1: id=1, description='hello ' (chunked)
        prs1 = self._make_partial_result_set(
            metadata=metadata,
            values=[Value(string_value="1"), Value(string_value="hello ")],
            chunked_value=True,
        )
        # Chunk 2: 'world' (continuation), id=2, description='test'
        prs2 = self._make_partial_result_set(
            values=[
                Value(string_value="world"),
                Value(string_value="2"),
                Value(string_value="test"),
            ],
            last=True,
        )

        streamed = StreamedResultSet(_MockIterator(prs1, prs2))
        table = streamed.to_arrow()

        self.assertEqual(table.num_rows, 2)
        self.assertEqual(table.column("id").to_pylist(), [1, 2])
        self.assertEqual(table.column("description").to_pylist(), ["hello world", "test"])

    def test_to_arrow_advanced_types(self):
        metadata = self._make_metadata([
            ("date_col", TypeCode.DATE),
            ("ts_col", TypeCode.TIMESTAMP),
            ("num_col", TypeCode.NUMERIC),
            ("bytes_col", TypeCode.BYTES),
        ])

        raw_bytes = b"sample_bytes"
        prs = self._make_partial_result_set(
            metadata=metadata,
            values=[
                Value(string_value="2023-01-15"),
                Value(string_value="2023-01-15T10:30:00.123456Z"),
                Value(string_value="12345.678900000"),
                Value(string_value=base64.b64encode(raw_bytes).decode("ascii")),
            ],
            last=True,
        )

        streamed = StreamedResultSet(_MockIterator(prs))
        table = streamed.to_arrow()

        self.assertEqual(table.num_rows, 1)
        self.assertEqual(table.column("num_col").to_pylist(), [decimal.Decimal("12345.678900000")])
        self.assertEqual(table.column("bytes_col").to_pylist(), [raw_bytes])

    def test_to_dataframe(self):
        try:
            import pandas as pd
        except ImportError:
            return  # Skip if pandas is not installed

        metadata = self._make_metadata([("id", TypeCode.INT64), ("name", TypeCode.STRING)])
        prs = self._make_partial_result_set(
            metadata=metadata,
            values=[Value(string_value="42"), Value(string_value="Answer")],
            last=True,
        )

        streamed = StreamedResultSet(_MockIterator(prs))
        df = streamed.to_dataframe()

        self.assertEqual(len(df), 1)
        self.assertEqual(df["id"].iloc[0], 42)
        self.assertEqual(df["name"].iloc[0], "Answer")

    def test_to_arrow_nulls(self):
        metadata = self._make_metadata([
            ("id", TypeCode.INT64),
            ("name", TypeCode.STRING),
            ("date_col", TypeCode.DATE),
            ("ts_col", TypeCode.TIMESTAMP),
            ("num_col", TypeCode.NUMERIC),
        ])
        prs = self._make_partial_result_set(
            metadata=metadata,
            values=[
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
                Value(null_value=0),
            ],
            last=True,
        )
        streamed = StreamedResultSet(_MockIterator(prs))
        table = streamed.to_arrow()
        self.assertEqual(table.num_rows, 1)
        self.assertIsNone(table.column("id").to_pylist()[0])
        self.assertIsNone(table.column("name").to_pylist()[0])
        self.assertIsNone(table.column("date_col").to_pylist()[0])
        self.assertIsNone(table.column("ts_col").to_pylist()[0])
        self.assertIsNone(table.column("num_col").to_pylist()[0])

    def test_to_arrow_arrays_and_structs(self):
        metadata = ResultSetMetadata(
            row_type=StructType(
                fields=[
                    StructType.Field(
                        name="arr",
                        type_=Type(
                            code=TypeCode.ARRAY,
                            array_element_type=Type(code=TypeCode.STRING),
                        ),
                    ),
                    StructType.Field(
                        name="st",
                        type_=Type(
                            code=TypeCode.STRUCT,
                            struct_type=StructType(
                                fields=[
                                    StructType.Field(
                                        name="f_int",
                                        type_=Type(code=TypeCode.INT64),
                                    ),
                                    StructType.Field(
                                        name="f_str",
                                        type_=Type(code=TypeCode.STRING),
                                    ),
                                ]
                            ),
                        ),
                    ),
                ]
            )
        )

        arr_val = Value(
            list_value=ListValue(values=[Value(string_value="x"), Value(string_value="y")])
        )
        st_val = Value(
            struct_value=Struct(
                fields={"f_int": Value(string_value="10"), "f_str": Value(string_value="hello")}
            )
        )

        prs = self._make_partial_result_set(
            metadata=metadata,
            values=[arr_val, st_val],
            last=True,
        )

        streamed = StreamedResultSet(_MockIterator(prs))
        table = streamed.to_arrow()

        self.assertEqual(table.num_rows, 1)
        self.assertEqual(table.column("arr").to_pylist(), [["x", "y"]])

    def test_to_arrow_missing_pyarrow_raises(self):
        metadata = self._make_metadata([("id", TypeCode.INT64)])
        prs = self._make_partial_result_set(metadata=metadata, values=[Value(string_value="1")], last=True)
        streamed = StreamedResultSet(_MockIterator(prs))

        with mock.patch("google.cloud.spanner_v1._arrow._HAS_PYARROW", False):
            with self.assertRaises(ImportError):
                streamed.to_arrow()

            with self.assertRaises(ImportError):
                list(streamed.to_arrow_batches())

            with self.assertRaises(ImportError):
                streamed.to_dataframe()


if __name__ == "__main__":
    unittest.main()
