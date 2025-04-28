# Copyright 2016 Google LLC All rights reserved.
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
from google.cloud.spanner_v1 import TransactionOptions


class Test_merge_query_options(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _merge_query_options

        return _merge_query_options(*args, **kw)

    def test_base_none_and_merge_none(self):
        base = merge = None
        result = self._callFUT(base, merge)
        self.assertIsNone(result)

    def test_base_dict_and_merge_none(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        base = {
            "optimizer_version": "2",
            "optimizer_statistics_package": "auto_20191128_14_47_22UTC",
        }
        merge = None
        expected = ExecuteSqlRequest.QueryOptions(
            optimizer_version="2",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        result = self._callFUT(base, merge)
        self.assertEqual(result, expected)

    def test_base_empty_and_merge_empty(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        base = ExecuteSqlRequest.QueryOptions()
        merge = ExecuteSqlRequest.QueryOptions()
        result = self._callFUT(base, merge)
        self.assertIsNone(result)

    def test_base_none_merge_object(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        base = None
        merge = ExecuteSqlRequest.QueryOptions(
            optimizer_version="3",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        result = self._callFUT(base, merge)
        self.assertEqual(result, merge)

    def test_base_none_merge_dict(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        base = None
        merge = {"optimizer_version": "3"}
        expected = ExecuteSqlRequest.QueryOptions(optimizer_version="3")
        result = self._callFUT(base, merge)
        self.assertEqual(result, expected)

    def test_base_object_merge_dict(self):
        from google.cloud.spanner_v1 import ExecuteSqlRequest

        base = ExecuteSqlRequest.QueryOptions(
            optimizer_version="1",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        merge = {"optimizer_version": "3"}
        expected = ExecuteSqlRequest.QueryOptions(
            optimizer_version="3",
            optimizer_statistics_package="auto_20191128_14_47_22UTC",
        )
        result = self._callFUT(base, merge)
        self.assertEqual(result, expected)


class Test_make_value_pb(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _make_value_pb

        return _make_value_pb(*args, **kw)

    def test_w_None(self):
        value_pb = self._callFUT(None)
        self.assertTrue(value_pb.HasField("null_value"))

    def test_w_bytes(self):
        from google.protobuf.struct_pb2 import Value

        BYTES = b"BYTES"
        expected = Value(string_value=BYTES)
        value_pb = self._callFUT(BYTES)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb, expected)

    def test_w_invalid_bytes(self):
        BYTES = b"\xff\xfe\x03&"
        with self.assertRaises(ValueError):
            self._callFUT(BYTES)

    def test_w_explicit_unicode(self):
        from google.protobuf.struct_pb2 import Value

        TEXT = "TEXT"
        value_pb = self._callFUT(TEXT)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, TEXT)

    def test_w_list(self):
        from google.protobuf.struct_pb2 import Value
        from google.protobuf.struct_pb2 import ListValue

        value_pb = self._callFUT(["a", "b", "c"])
        self.assertIsInstance(value_pb, Value)
        self.assertIsInstance(value_pb.list_value, ListValue)
        values = value_pb.list_value.values
        self.assertEqual([value.string_value for value in values], ["a", "b", "c"])

    def test_w_tuple(self):
        from google.protobuf.struct_pb2 import Value
        from google.protobuf.struct_pb2 import ListValue

        value_pb = self._callFUT(("a", "b", "c"))
        self.assertIsInstance(value_pb, Value)
        self.assertIsInstance(value_pb.list_value, ListValue)
        values = value_pb.list_value.values
        self.assertEqual([value.string_value for value in values], ["a", "b", "c"])

    def test_w_bool(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(True)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.bool_value, True)

    def test_w_int(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(42)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "42")

    def test_w_float(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(3.14159)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.number_value, 3.14159)

    def test_w_float_nan(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float("nan"))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "NaN")

    def test_w_float_neg_inf(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float("-inf"))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "-Infinity")

    def test_w_float_pos_inf(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float("inf"))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "Infinity")

    def test_w_date(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        today = datetime.date.today()
        value_pb = self._callFUT(today)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, today.isoformat())

    def test_w_date_pre1000ad(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        when = datetime.date(800, 2, 25)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "0800-02-25")

    def test_w_timestamp_w_nanos(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.api_core import datetime_helpers

        when = datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=datetime.timezone.utc
        )
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "2016-12-20T21:13:47.123456789Z")

    def test_w_timestamp_w_nanos_pre1000ad(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.api_core import datetime_helpers

        when = datetime_helpers.DatetimeWithNanoseconds(
            850, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=datetime.timezone.utc
        )
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "0850-12-20T21:13:47.123456789Z")

    def test_w_listvalue(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1._helpers import _make_list_value_pb

        list_value = _make_list_value_pb([1, 2, 3])
        value_pb = self._callFUT(list_value)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.list_value, list_value)

    def test_w_datetime(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        when = datetime.datetime(2021, 2, 8, 0, 0, 0, tzinfo=datetime.timezone.utc)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "2021-02-08T00:00:00.000000Z")

    def test_w_datetime_pre1000ad(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        when = datetime.datetime(916, 2, 8, 0, 0, 0, tzinfo=datetime.timezone.utc)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "0916-02-08T00:00:00.000000Z")

    def test_w_timestamp_w_tz(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        zone = datetime.timezone(datetime.timedelta(hours=+1), name="CET")
        when = datetime.datetime(2021, 2, 8, 0, 0, 0, tzinfo=zone)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "2021-02-07T23:00:00.000000Z")

    def test_w_timestamp_w_tz_pre1000ad(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        zone = datetime.timezone(datetime.timedelta(hours=+1), name="CET")
        when = datetime.datetime(721, 2, 8, 0, 0, 0, tzinfo=zone)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "0721-02-07T23:00:00.000000Z")

    def test_w_unknown_type(self):
        with self.assertRaises(ValueError):
            self._callFUT(object())

    def test_w_numeric_precision_and_scale_valid(self):
        import decimal
        from google.protobuf.struct_pb2 import Value

        cases = [
            decimal.Decimal("42"),
            decimal.Decimal("9.9999999999999999999999999999999999999E+28"),
            decimal.Decimal("-9.9999999999999999999999999999999999999E+28"),
            decimal.Decimal("99999999999999999999999999999.999999999"),
            decimal.Decimal("1E+28"),
            decimal.Decimal("1E-9"),
        ]
        for value in cases:
            with self.subTest(value=value):
                value_pb = self._callFUT(value)
                self.assertIsInstance(value_pb, Value)
                self.assertEqual(value_pb.string_value, str(value))

    def test_w_numeric_precision_and_scale_invalid(self):
        import decimal
        from google.cloud.spanner_v1._helpers import (
            NUMERIC_MAX_SCALE_ERR_MSG,
            NUMERIC_MAX_PRECISION_ERR_MSG,
        )

        max_precision_error_msg = NUMERIC_MAX_PRECISION_ERR_MSG.format("30")
        max_scale_error_msg = NUMERIC_MAX_SCALE_ERR_MSG.format("10")

        cases = [
            (
                decimal.Decimal("9.9999999999999999999999999999999999999E+29"),
                max_precision_error_msg,
            ),
            (
                decimal.Decimal("-9.9999999999999999999999999999999999999E+29"),
                max_precision_error_msg,
            ),
            (
                decimal.Decimal("999999999999999999999999999999.99999999"),
                max_precision_error_msg,
            ),
            (
                decimal.Decimal("-999999999999999999999999999999.99999999"),
                max_precision_error_msg,
            ),
            (
                decimal.Decimal("999999999999999999999999999999"),
                max_precision_error_msg,
            ),
            (decimal.Decimal("1E+29"), max_precision_error_msg),
            (decimal.Decimal("1E-10"), max_scale_error_msg),
        ]

        for value, err_msg in cases:
            with self.subTest(value=value, err_msg=err_msg):
                self.assertRaisesRegex(
                    ValueError,
                    err_msg,
                    lambda: self._callFUT(value),
                )

    def test_w_json(self):
        import json
        from google.protobuf.struct_pb2 import Value

        value = json.dumps(
            {"id": 27863, "Name": "Anamika"}, sort_keys=True, separators=(",", ":")
        )
        value_pb = self._callFUT(value)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, value)

    def test_w_json_None(self):
        from google.cloud.spanner_v1 import JsonObject

        value = JsonObject(None)
        value_pb = self._callFUT(value)
        self.assertTrue(value_pb.HasField("null_value"))

    def test_w_proto_message(self):
        from google.protobuf.struct_pb2 import Value
        import base64
        from .testdata import singer_pb2

        singer_info = singer_pb2.SingerInfo()
        expected = Value(string_value=base64.b64encode(singer_info.SerializeToString()))
        value_pb = self._callFUT(singer_info)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb, expected)

    def test_w_proto_enum(self):
        from google.protobuf.struct_pb2 import Value
        from .testdata import singer_pb2

        value_pb = self._callFUT(singer_pb2.Genre.ROCK)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "3")


class Test_make_list_value_pb(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _make_list_value_pb

        return _make_list_value_pb(*args, **kw)

    def test_empty(self):
        from google.protobuf.struct_pb2 import ListValue

        result = self._callFUT(values=[])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 0)

    def test_w_single_value(self):
        from google.protobuf.struct_pb2 import ListValue

        VALUE = "value"
        result = self._callFUT(values=[VALUE])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 1)
        self.assertEqual(result.values[0].string_value, VALUE)

    def test_w_multiple_values(self):
        from google.protobuf.struct_pb2 import ListValue

        VALUE_1 = "value"
        VALUE_2 = 42
        result = self._callFUT(values=[VALUE_1, VALUE_2])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 2)
        self.assertEqual(result.values[0].string_value, VALUE_1)
        self.assertEqual(result.values[1].string_value, str(VALUE_2))


class Test_make_list_value_pbs(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _make_list_value_pbs

        return _make_list_value_pbs(*args, **kw)

    def test_empty(self):
        result = self._callFUT(values=[])
        self.assertEqual(result, [])

    def test_w_single_values(self):
        from google.protobuf.struct_pb2 import ListValue

        values = [[0], [1]]
        result = self._callFUT(values=values)
        self.assertEqual(len(result), len(values))
        for found, expected in zip(result, values):
            self.assertIsInstance(found, ListValue)
            self.assertEqual(len(found.values), 1)
            self.assertEqual(found.values[0].string_value, str(expected[0]))

    def test_w_multiple_values(self):
        from google.protobuf.struct_pb2 import ListValue

        values = [[0, "A"], [1, "B"]]
        result = self._callFUT(values=values)
        self.assertEqual(len(result), len(values))
        for found, expected in zip(result, values):
            self.assertIsInstance(found, ListValue)
            self.assertEqual(len(found.values), 2)
            self.assertEqual(found.values[0].string_value, str(expected[0]))
            self.assertEqual(found.values[1].string_value, expected[1])


class Test_parse_value_pb(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _parse_value_pb

        return _parse_value_pb(*args, **kw)

    def test_w_null(self):
        from google.protobuf.struct_pb2 import Value, NULL_VALUE
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(code=TypeCode.STRING)
        field_name = "null_column"
        value_pb = Value(null_value=NULL_VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), None)

    def test_w_string(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = "Value"
        field_type = Type(code=TypeCode.STRING)
        field_name = "string_column"
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_bytes(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = b"Value"
        field_type = Type(code=TypeCode.BYTES)
        field_name = "bytes_column"
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_bool(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = True
        field_type = Type(code=TypeCode.BOOL)
        field_name = "bool_column"
        value_pb = Value(bool_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_int(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = 12345
        field_type = Type(code=TypeCode.INT64)
        field_name = "int_column"
        value_pb = Value(string_value=str(VALUE))

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_float(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = 3.14159
        field_type = Type(code=TypeCode.FLOAT64)
        field_name = "float_column"
        value_pb = Value(number_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_float_str(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = "3.14159"
        field_type = Type(code=TypeCode.FLOAT64)
        field_name = "float_str_column"
        value_pb = Value(string_value=VALUE)
        expected_value = 3.14159

        self.assertEqual(
            self._callFUT(value_pb, field_type, field_name), expected_value
        )

    def test_w_float32(self):
        from google.cloud.spanner_v1 import Type, TypeCode
        from google.protobuf.struct_pb2 import Value

        VALUE = 3.14159
        field_type = Type(code=TypeCode.FLOAT32)
        field_name = "float32_column"
        value_pb = Value(number_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_float32_str(self):
        from google.cloud.spanner_v1 import Type, TypeCode
        from google.protobuf.struct_pb2 import Value

        VALUE = "3.14159"
        field_type = Type(code=TypeCode.FLOAT32)
        field_name = "float32_str_column"
        value_pb = Value(string_value=VALUE)
        expected_value = 3.14159

        self.assertEqual(
            self._callFUT(value_pb, field_type, field_name), expected_value
        )

    def test_w_date(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = datetime.date.today()
        field_type = Type(code=TypeCode.DATE)
        field_name = "date_column"
        value_pb = Value(string_value=VALUE.isoformat())

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_timestamp_wo_nanos(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.api_core import datetime_helpers
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        value = datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47, microsecond=123456, tzinfo=datetime.timezone.utc
        )
        field_type = Type(code=TypeCode.TIMESTAMP)
        field_name = "nanos_column"
        value_pb = Value(string_value=datetime_helpers.to_rfc3339(value))

        parsed = self._callFUT(value_pb, field_type, field_name)
        self.assertIsInstance(parsed, datetime_helpers.DatetimeWithNanoseconds)
        self.assertEqual(parsed, value)

    def test_w_timestamp_w_nanos(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.api_core import datetime_helpers
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        value = datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=datetime.timezone.utc
        )
        field_type = Type(code=TypeCode.TIMESTAMP)
        field_name = "timestamp_column"
        value_pb = Value(string_value=datetime_helpers.to_rfc3339(value))

        parsed = self._callFUT(value_pb, field_type, field_name)
        self.assertIsInstance(parsed, datetime_helpers.DatetimeWithNanoseconds)
        self.assertEqual(parsed, value)

    def test_w_array_empty(self):
        from google.protobuf.struct_pb2 import Value, ListValue
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(
            code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64)
        )
        field_name = "array_empty_column"
        value_pb = Value(list_value=ListValue(values=[]))

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), [])

    def test_w_array_non_empty(self):
        from google.protobuf.struct_pb2 import Value, ListValue
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(
            code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64)
        )
        field_name = "array_non_empty_column"
        VALUES = [32, 19, 5]
        values_pb = ListValue(
            values=[Value(string_value=str(value)) for value in VALUES]
        )
        value_pb = Value(list_value=values_pb)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUES)

    def test_w_struct(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1._helpers import _make_list_value_pb

        VALUES = ["phred", 32]
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )
        field_type = Type(code=TypeCode.STRUCT, struct_type=struct_type_pb)
        field_name = "struct_column"
        value_pb = Value(list_value=_make_list_value_pb(VALUES))

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUES)

    def test_w_numeric(self):
        import decimal
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = decimal.Decimal("99999999999999999999999999999.999999999")
        field_type = Type(code=TypeCode.NUMERIC)
        field_name = "numeric_column"
        value_pb = Value(string_value=str(VALUE))

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

    def test_w_json(self):
        import json
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = {"id": 27863, "Name": "Anamika"}
        str_repr = json.dumps(VALUE, sort_keys=True, separators=(",", ":"))

        field_type = Type(code=TypeCode.JSON)
        field_name = "json_column"
        value_pb = Value(string_value=str_repr)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), VALUE)

        VALUE = None
        str_repr = json.dumps(VALUE, sort_keys=True, separators=(",", ":"))

        field_type = Type(code=TypeCode.JSON)
        value_pb = Value(string_value=str_repr)

        self.assertEqual(self._callFUT(value_pb, field_type, field_name), {})

    def test_w_unknown_type(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(code=TypeCode.TYPE_CODE_UNSPECIFIED)
        field_name = "unknown_column"
        value_pb = Value(string_value="Borked")

        with self.assertRaises(ValueError):
            self._callFUT(value_pb, field_type, field_name)

    def test_w_proto_message(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode
        import base64
        from .testdata import singer_pb2

        VALUE = singer_pb2.SingerInfo()
        field_type = Type(code=TypeCode.PROTO)
        field_name = "proto_message_column"
        value_pb = Value(string_value=base64.b64encode(VALUE.SerializeToString()))
        column_info = {"proto_message_column": singer_pb2.SingerInfo()}

        self.assertEqual(
            self._callFUT(value_pb, field_type, field_name, column_info), VALUE
        )

    def test_w_proto_enum(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode
        from .testdata import singer_pb2

        VALUE = "ROCK"
        field_type = Type(code=TypeCode.ENUM)
        field_name = "proto_enum_column"
        value_pb = Value(string_value=str(singer_pb2.Genre.ROCK))
        column_info = {"proto_enum_column": singer_pb2.Genre}

        self.assertEqual(
            self._callFUT(value_pb, field_type, field_name, column_info), VALUE
        )


class Test_parse_list_value_pbs(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _parse_list_value_pbs

        return _parse_list_value_pbs(*args, **kw)

    def test_empty(self):
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import StructType
        from google.cloud.spanner_v1 import TypeCode

        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )

        self.assertEqual(self._callFUT(rows=[], row_type=struct_type_pb), [])

    def test_non_empty(self):
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import StructType
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1._helpers import _make_list_value_pbs

        VALUES = [["phred", 32], ["bharney", 31]]
        struct_type_pb = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="age", type_=Type(code=TypeCode.INT64)),
            ]
        )
        values_pbs = _make_list_value_pbs(VALUES)

        self.assertEqual(
            self._callFUT(rows=values_pbs, row_type=struct_type_pb), VALUES
        )


class Test_SessionWrapper(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.spanner_v1._helpers import _SessionWrapper

        return _SessionWrapper

    def _make_one(self, session):
        return self._getTargetClass()(session)

    def test_ctor(self):
        session = object()
        base = self._make_one(session)
        self.assertIs(base._session, session)


class Test_metadata_with_prefix(unittest.TestCase):
    def _call_fut(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _metadata_with_prefix

        return _metadata_with_prefix(*args, **kw)

    def test(self):
        prefix = "prefix"
        metadata = self._call_fut(prefix)
        self.assertEqual(metadata, [("google-cloud-resource-prefix", prefix)])


class Test_retry(unittest.TestCase):
    class test_class:
        def test_fxn(self):
            return True

    def test_retry_on_error(self):
        from google.api_core.exceptions import InternalServerError, NotFound
        from google.cloud.spanner_v1._helpers import _retry
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            InternalServerError("testing"),
            NotFound("testing"),
            True,
        ]

        _retry(functools.partial(test_api.test_fxn))

        self.assertEqual(test_api.test_fxn.call_count, 3)

    def test_retry_allowed_exceptions(self):
        from google.api_core.exceptions import InternalServerError, NotFound
        from google.cloud.spanner_v1._helpers import _retry
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            NotFound("testing"),
            InternalServerError("testing"),
            True,
        ]

        with self.assertRaises(InternalServerError):
            _retry(
                functools.partial(test_api.test_fxn),
                allowed_exceptions={NotFound: None},
            )

        self.assertEqual(test_api.test_fxn.call_count, 2)

    def test_retry_count(self):
        from google.api_core.exceptions import InternalServerError
        from google.cloud.spanner_v1._helpers import _retry
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            InternalServerError("testing"),
            InternalServerError("testing"),
        ]

        with self.assertRaises(InternalServerError):
            _retry(functools.partial(test_api.test_fxn), retry_count=1)

        self.assertEqual(test_api.test_fxn.call_count, 2)

    def test_check_rst_stream_error(self):
        from google.api_core.exceptions import InternalServerError
        from google.cloud.spanner_v1._helpers import _retry, _check_rst_stream_error
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            InternalServerError("Received unexpected EOS on DATA frame from server"),
            InternalServerError("RST_STREAM"),
            True,
        ]

        _retry(
            functools.partial(test_api.test_fxn),
            allowed_exceptions={InternalServerError: _check_rst_stream_error},
        )

        self.assertEqual(test_api.test_fxn.call_count, 3)

    def test_retry_on_aborted_exception_with_success_after_first_aborted_retry(self):
        from google.api_core.exceptions import Aborted
        import time
        from google.cloud.spanner_v1._helpers import _retry_on_aborted_exception
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            Aborted("aborted exception", errors=("Aborted error")),
            "true",
        ]
        deadline = time.time() + 30
        result_after_retry = _retry_on_aborted_exception(
            functools.partial(test_api.test_fxn), deadline
        )

        self.assertEqual(test_api.test_fxn.call_count, 2)
        self.assertTrue(result_after_retry)

    def test_retry_on_aborted_exception_with_success_after_three_retries(self):
        from google.api_core.exceptions import Aborted
        import time
        from google.cloud.spanner_v1._helpers import _retry_on_aborted_exception
        import functools

        test_api = mock.create_autospec(self.test_class)
        # Case where aborted exception is thrown after other generic exceptions
        test_api.test_fxn.side_effect = [
            Aborted("aborted exception", errors=("Aborted error")),
            Aborted("aborted exception", errors=("Aborted error")),
            Aborted("aborted exception", errors=("Aborted error")),
            "true",
        ]
        deadline = time.time() + 30
        _retry_on_aborted_exception(
            functools.partial(test_api.test_fxn),
            deadline=deadline,
        )

        self.assertEqual(test_api.test_fxn.call_count, 4)

    def test_retry_on_aborted_exception_raises_aborted_if_deadline_expires(self):
        from google.api_core.exceptions import Aborted
        import time
        from google.cloud.spanner_v1._helpers import _retry_on_aborted_exception
        import functools

        test_api = mock.create_autospec(self.test_class)
        test_api.test_fxn.side_effect = [
            Aborted("aborted exception", errors=("Aborted error")),
            "true",
        ]
        deadline = time.time() + 0.1
        with self.assertRaises(Aborted):
            _retry_on_aborted_exception(
                functools.partial(test_api.test_fxn), deadline=deadline
            )

        self.assertEqual(test_api.test_fxn.call_count, 1)


class Test_metadata_with_leader_aware_routing(unittest.TestCase):
    def _call_fut(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _metadata_with_leader_aware_routing

        return _metadata_with_leader_aware_routing(*args, **kw)

    def test(self):
        value = True
        metadata = self._call_fut(True)
        self.assertEqual(
            metadata, ("x-goog-spanner-route-to-leader", str(value).lower())
        )


class Test_merge_transaction_options(unittest.TestCase):
    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _merge_Transaction_Options

        return _merge_Transaction_Options(*args, **kw)

    def test_default_none_and_merge_none(self):
        default = merge = None
        result = self._callFUT(default, merge)
        self.assertIsNone(result)

    def test_default_options_and_merge_none(self):
        default = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.REPEATABLE_READ
        )
        merge = None
        result = self._callFUT(default, merge)
        expected = default
        self.assertEqual(result, expected)

    def test_default_none_and_merge_options(self):
        default = None
        merge = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE
        )
        expected = merge
        result = self._callFUT(default, merge)
        self.assertEqual(result, expected)

    def test_default_and_merge_isolation_options(self):
        default = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE,
            read_write=TransactionOptions.ReadWrite(),
        )
        merge = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.REPEATABLE_READ,
            exclude_txn_from_change_streams=True,
        )
        expected = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.REPEATABLE_READ,
            read_write=TransactionOptions.ReadWrite(),
            exclude_txn_from_change_streams=True,
        )
        result = self._callFUT(default, merge)
        self.assertEqual(result, expected)

    def test_default_isolation_and_merge_options(self):
        default = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE
        )
        merge = TransactionOptions(
            read_write=TransactionOptions.ReadWrite(),
            exclude_txn_from_change_streams=True,
        )
        expected = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE,
            read_write=TransactionOptions.ReadWrite(),
            exclude_txn_from_change_streams=True,
        )
        result = self._callFUT(default, merge)
        self.assertEqual(result, expected)

    def test_default_isolation_and_merge_options_isolation_unspecified(self):
        default = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE
        )
        merge = TransactionOptions(
            read_write=TransactionOptions.ReadWrite(),
            exclude_txn_from_change_streams=True,
            isolation_level=TransactionOptions.IsolationLevel.ISOLATION_LEVEL_UNSPECIFIED,
        )
        expected = TransactionOptions(
            isolation_level=TransactionOptions.IsolationLevel.SERIALIZABLE,
            read_write=TransactionOptions.ReadWrite(),
            exclude_txn_from_change_streams=True,
        )
        result = self._callFUT(default, merge)
        self.assertEqual(result, expected)


class Test_interval(unittest.TestCase):
    from google.protobuf.struct_pb2 import Value
    from google.cloud.spanner_v1 import Interval
    from google.cloud.spanner_v1 import Type
    from google.cloud.spanner_v1 import TypeCode

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _make_value_pb

        return _make_value_pb(*args, **kw)

    def test_interval_cases(self):
        test_cases = [
            {
                "name": "Basic interval",
                "interval": self.Interval(months=14, days=3, nanos=43926789000123),
                "expected": "P1Y2M3DT12H12M6.789000123S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Months only",
                "interval": self.Interval(months=10, days=0, nanos=0),
                "expected": "P10M",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Days only",
                "interval": self.Interval(months=0, days=10, nanos=0),
                "expected": "P10D",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Seconds only",
                "interval": self.Interval(months=0, days=0, nanos=10000000000),
                "expected": "PT10S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Milliseconds only",
                "interval": self.Interval(months=0, days=0, nanos=10000000),
                "expected": "PT0.010S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Microseconds only",
                "interval": self.Interval(months=0, days=0, nanos=10000),
                "expected": "PT0.000010S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Nanoseconds only",
                "interval": self.Interval(months=0, days=0, nanos=10),
                "expected": "PT0.000000010S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Mixed components",
                "interval": self.Interval(months=10, days=20, nanos=1030),
                "expected": "P10M20DT0.000001030S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Mixed components with negative nanos",
                "interval": self.Interval(months=10, days=20, nanos=-1030),
                "expected": "P10M20DT-0.000001030S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Negative interval",
                "interval": self.Interval(months=-14, days=-3, nanos=-43926789000123),
                "expected": "P-1Y-2M-3DT-12H-12M-6.789000123S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Mixed signs",
                "interval": self.Interval(months=10, days=3, nanos=-41401234000000),
                "expected": "P10M3DT-11H-30M-1.234S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Large values",
                "interval": self.Interval(
                    months=25, days=15, nanos=316223999999999999999
                ),
                "expected": "P2Y1M15DT87839999H59M59.999999999S",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
            {
                "name": "Zero interval",
                "interval": self.Interval(months=0, days=0, nanos=0),
                "expected": "P0Y",
                "expected_type": self.Type(code=self.TypeCode.INTERVAL),
            },
        ]

        for case in test_cases:
            with self.subTest(name=case["name"]):
                value_pb = self._callFUT(case["interval"])
                self.assertIsInstance(value_pb, self.Value)
                self.assertEqual(value_pb.string_value, case["expected"])
                # TODO: Add type checking once we have access to the type information


class Test_parse_interval(unittest.TestCase):
    from google.protobuf.struct_pb2 import Value

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner_v1._helpers import _parse_interval

        return _parse_interval(*args, **kw)

    def test_parse_interval_cases(self):
        test_cases = [
            {
                "name": "full interval with all components",
                "input": "P1Y2M3DT12H12M6.789000123S",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 43926789000123,
                "want_err": False,
            },
            {
                "name": "interval with negative minutes",
                "input": "P1Y2M3DT13H-48M6S",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 43926000000000,
                "want_err": False,
            },
            {
                "name": "date only interval",
                "input": "P1Y2M3D",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "years and months only",
                "input": "P1Y2M",
                "expected_months": 14,
                "expected_days": 0,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "years only",
                "input": "P1Y",
                "expected_months": 12,
                "expected_days": 0,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "months only",
                "input": "P2M",
                "expected_months": 2,
                "expected_days": 0,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "days only",
                "input": "P3D",
                "expected_months": 0,
                "expected_days": 3,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "time components with fractional seconds",
                "input": "PT4H25M6.7890001S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 15906789000100,
                "want_err": False,
            },
            {
                "name": "time components without fractional seconds",
                "input": "PT4H25M6S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 15906000000000,
                "want_err": False,
            },
            {
                "name": "hours and seconds only",
                "input": "PT4H30S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 14430000000000,
                "want_err": False,
            },
            {
                "name": "hours and minutes only",
                "input": "PT4H1M",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 14460000000000,
                "want_err": False,
            },
            {
                "name": "minutes only",
                "input": "PT5M",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 300000000000,
                "want_err": False,
            },
            {
                "name": "fractional seconds only",
                "input": "PT6.789S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 6789000000,
                "want_err": False,
            },
            {
                "name": "small fractional seconds",
                "input": "PT0.123S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 123000000,
                "want_err": False,
            },
            {
                "name": "very small fractional seconds",
                "input": "PT.000000123S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 123,
                "want_err": False,
            },
            {
                "name": "zero years",
                "input": "P0Y",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 0,
                "want_err": False,
            },
            {
                "name": "all negative components",
                "input": "P-1Y-2M-3DT-12H-12M-6.789000123S",
                "expected_months": -14,
                "expected_days": -3,
                "expected_nanos": -43926789000123,
                "want_err": False,
            },
            {
                "name": "mixed signs in components",
                "input": "P1Y-2M3DT13H-51M6.789S",
                "expected_months": 10,
                "expected_days": 3,
                "expected_nanos": 43746789000000,
                "want_err": False,
            },
            {
                "name": "negative years with mixed signs",
                "input": "P-1Y2M-3DT-13H49M-6.789S",
                "expected_months": -10,
                "expected_days": -3,
                "expected_nanos": -43866789000000,
                "want_err": False,
            },
            {
                "name": "negative time components",
                "input": "P1Y2M3DT-4H25M-6.7890001S",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": -12906789000100,
                "want_err": False,
            },
            {
                "name": "large time values",
                "input": "PT100H100M100.5S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 366100500000000,
                "want_err": False,
            },
            {
                "name": "only time components with seconds",
                "input": "PT12H30M1S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 45001000000000,
                "want_err": False,
            },
            {
                "name": "date and time no seconds",
                "input": "P1Y2M3DT12H30M",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 45000000000000,
                "want_err": False,
            },
            {
                "name": "fractional seconds with max digits",
                "input": "PT0.123456789S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 123456789,
                "want_err": False,
            },
            {
                "name": "hours and fractional seconds",
                "input": "PT1H0.5S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 3600500000000,
                "want_err": False,
            },
            {
                "name": "years and months to months with fractional seconds",
                "input": "P1Y2M3DT12H30M1.23456789S",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 45001234567890,
                "want_err": False,
            },
            {
                "name": "comma as decimal point",
                "input": "P1Y2M3DT12H30M1,23456789S",
                "expected_months": 14,
                "expected_days": 3,
                "expected_nanos": 45001234567890,
                "want_err": False,
            },
            {
                "name": "fractional seconds without 0 before decimal",
                "input": "PT.5S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 500000000,
                "want_err": False,
            },
            {
                "name": "mixed signs",
                "input": "P-1Y2M3DT12H-30M1.234S",
                "expected_months": -10,
                "expected_days": 3,
                "expected_nanos": 41401234000000,
                "want_err": False,
            },
            {
                "name": "more mixed signs",
                "input": "P1Y-2M3DT-12H30M-1.234S",
                "expected_months": 10,
                "expected_days": 3,
                "expected_nanos": -41401234000000,
                "want_err": False,
            },
            {
                "name": "trailing zeros after decimal",
                "input": "PT1.234000S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 1234000000,
                "want_err": False,
            },
            {
                "name": "all zeros after decimal",
                "input": "PT1.000S",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 1000000000,
                "want_err": False,
            },
            # Invalid cases
            {"name": "invalid format", "input": "invalid", "want_err": True},
            {"name": "missing duration specifier", "input": "P", "want_err": True},
            {"name": "missing time components", "input": "PT", "want_err": True},
            {"name": "missing unit specifier", "input": "P1YM", "want_err": True},
            {"name": "missing T separator", "input": "P1Y2M3D4H5M6S", "want_err": True},
            {
                "name": "missing decimal value",
                "input": "P1Y2M3DT4H5M6.S",
                "want_err": True,
            },
            {
                "name": "extra unit specifier",
                "input": "P1Y2M3DT4H5M6.789SS",
                "want_err": True,
            },
            {
                "name": "missing value after decimal",
                "input": "P1Y2M3DT4H5M6.",
                "want_err": True,
            },
            {
                "name": "non-digit after decimal",
                "input": "P1Y2M3DT4H5M6.ABC",
                "want_err": True,
            },
            {"name": "missing unit", "input": "P1Y2M3", "want_err": True},
            {"name": "missing time value", "input": "P1Y2M3DT", "want_err": True},
            {
                "name": "invalid negative sign position",
                "input": "P-T1H",
                "want_err": True,
            },
            {"name": "trailing negative sign", "input": "PT1H-", "want_err": True},
            {
                "name": "too many decimal places",
                "input": "P1Y2M3DT4H5M6.789123456789S",
                "want_err": True,
            },
            {
                "name": "multiple decimal points",
                "input": "P1Y2M3DT4H5M6.123.456S",
                "want_err": True,
            },
            {
                "name": "both dot and comma decimals",
                "input": "P1Y2M3DT4H5M6.,789S",
                "want_err": True,
            },
        ]

        for case in test_cases:
            with self.subTest(name=case["name"]):
                value_pb = self.Value(string_value=case["input"])
                if case.get("want_err", False):
                    with self.assertRaises(ValueError):
                        self._callFUT(value_pb)
                else:
                    result = self._callFUT(value_pb)
                    self.assertEqual(result.months, case["expected_months"])
                    self.assertEqual(result.days, case["expected_days"])
                    self.assertEqual(result.nanos, case["expected_nanos"])

    def test_large_values(self):
        large_test_cases = [
            {
                "name": "large positive hours",
                "input": "PT87840000H",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": 316224000000000000000,
                "want_err": False,
            },
            {
                "name": "large negative hours",
                "input": "PT-87840000H",
                "expected_months": 0,
                "expected_days": 0,
                "expected_nanos": -316224000000000000000,
                "want_err": False,
            },
            {
                "name": "large mixed values with max precision",
                "input": "P2Y1M15DT87839999H59M59.999999999S",
                "expected_months": 25,
                "expected_days": 15,
                "expected_nanos": 316223999999999999999,
                "want_err": False,
            },
            {
                "name": "large mixed negative values with max precision",
                "input": "P2Y1M15DT-87839999H-59M-59.999999999S",
                "expected_months": 25,
                "expected_days": 15,
                "expected_nanos": -316223999999999999999,
                "want_err": False,
            },
        ]

        for case in large_test_cases:
            with self.subTest(name=case["name"]):
                value_pb = self.Value(string_value=case["input"])
                if case.get("want_err", False):
                    with self.assertRaises(ValueError):
                        self._callFUT(value_pb)
                else:
                    result = self._callFUT(value_pb)
                    self.assertEqual(result.months, case["expected_months"])
                    self.assertEqual(result.days, case["expected_days"])
                    self.assertEqual(result.nanos, case["expected_nanos"])
