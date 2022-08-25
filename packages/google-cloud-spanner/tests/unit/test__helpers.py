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

    def test_w_timestamp_w_nanos(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.api_core import datetime_helpers

        when = datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=datetime.timezone.utc
        )
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, when.rfc3339())

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
        from google.api_core import datetime_helpers

        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        value_pb = self._callFUT(now)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, datetime_helpers.to_rfc3339(now))

    def test_w_timestamp_w_tz(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        zone = datetime.timezone(datetime.timedelta(hours=+1), name="CET")
        when = datetime.datetime(2021, 2, 8, 0, 0, 0, tzinfo=zone)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, "2021-02-07T23:00:00.000000Z")

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
        value_pb = Value(null_value=NULL_VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), None)

    def test_w_string(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = "Value"
        field_type = Type(code=TypeCode.STRING)
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_bytes(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = b"Value"
        field_type = Type(code=TypeCode.BYTES)
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_bool(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = True
        field_type = Type(code=TypeCode.BOOL)
        value_pb = Value(bool_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_int(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = 12345
        field_type = Type(code=TypeCode.INT64)
        value_pb = Value(string_value=str(VALUE))

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_float(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = 3.14159
        field_type = Type(code=TypeCode.FLOAT64)
        value_pb = Value(number_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_float_str(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = "3.14159"
        field_type = Type(code=TypeCode.FLOAT64)
        value_pb = Value(string_value=VALUE)
        expected_value = 3.14159

        self.assertEqual(self._callFUT(value_pb, field_type), expected_value)

    def test_w_date(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = datetime.date.today()
        field_type = Type(code=TypeCode.DATE)
        value_pb = Value(string_value=VALUE.isoformat())

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

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
        value_pb = Value(string_value=datetime_helpers.to_rfc3339(value))

        parsed = self._callFUT(value_pb, field_type)
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
        value_pb = Value(string_value=datetime_helpers.to_rfc3339(value))

        parsed = self._callFUT(value_pb, field_type)
        self.assertIsInstance(parsed, datetime_helpers.DatetimeWithNanoseconds)
        self.assertEqual(parsed, value)

    def test_w_array_empty(self):
        from google.protobuf.struct_pb2 import Value, ListValue
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(
            code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64)
        )
        value_pb = Value(list_value=ListValue(values=[]))

        self.assertEqual(self._callFUT(value_pb, field_type), [])

    def test_w_array_non_empty(self):
        from google.protobuf.struct_pb2 import Value, ListValue
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(
            code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64)
        )
        VALUES = [32, 19, 5]
        values_pb = ListValue(
            values=[Value(string_value=str(value)) for value in VALUES]
        )
        value_pb = Value(list_value=values_pb)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUES)

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
        value_pb = Value(list_value=_make_list_value_pb(VALUES))

        self.assertEqual(self._callFUT(value_pb, field_type), VALUES)

    def test_w_numeric(self):
        import decimal
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = decimal.Decimal("99999999999999999999999999999.999999999")
        field_type = Type(code=TypeCode.NUMERIC)
        value_pb = Value(string_value=str(VALUE))

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_json(self):
        import json
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        VALUE = {"id": 27863, "Name": "Anamika"}
        str_repr = json.dumps(VALUE, sort_keys=True, separators=(",", ":"))

        field_type = Type(code=TypeCode.JSON)
        value_pb = Value(string_value=str_repr)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

        VALUE = None
        str_repr = json.dumps(VALUE, sort_keys=True, separators=(",", ":"))

        field_type = Type(code=TypeCode.JSON)
        value_pb = Value(string_value=str_repr)

        self.assertEqual(self._callFUT(value_pb, field_type), {})

    def test_w_unknown_type(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode

        field_type = Type(code=TypeCode.TYPE_CODE_UNSPECIFIED)
        value_pb = Value(string_value="Borked")

        with self.assertRaises(ValueError):
            self._callFUT(value_pb, field_type)


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
