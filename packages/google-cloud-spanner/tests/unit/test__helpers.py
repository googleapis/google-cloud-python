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
