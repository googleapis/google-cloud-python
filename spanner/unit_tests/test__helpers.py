# Copyright 2016 Google Inc. All rights reserved.
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


class TestTimestampWithNanoseconds(unittest.TestCase):

    def _get_target_class(self):
        from google.cloud.spanner._helpers import TimestampWithNanoseconds

        return TimestampWithNanoseconds

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_wo_nanos(self):
        stamp = self._make_one(2016, 12, 20, 21, 13, 47, 123456)
        self.assertEqual(stamp.year, 2016)
        self.assertEqual(stamp.month, 12)
        self.assertEqual(stamp.day, 20)
        self.assertEqual(stamp.hour, 21)
        self.assertEqual(stamp.minute, 13)
        self.assertEqual(stamp.second, 47)
        self.assertEqual(stamp.microsecond, 123456)
        self.assertEqual(stamp.nanosecond, 0)

    def test_ctor_w_nanos(self):
        stamp = self._make_one(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789)
        self.assertEqual(stamp.year, 2016)
        self.assertEqual(stamp.month, 12)
        self.assertEqual(stamp.day, 20)
        self.assertEqual(stamp.hour, 21)
        self.assertEqual(stamp.minute, 13)
        self.assertEqual(stamp.second, 47)
        self.assertEqual(stamp.microsecond, 123456)
        self.assertEqual(stamp.nanosecond, 123456789)

    def test_ctor_w_micros_positional_and_nanos(self):
        with self.assertRaises(TypeError):
            self._make_one(
                2016, 12, 20, 21, 13, 47, 123456, nanosecond=123456789)

    def test_ctor_w_micros_keyword_and_nanos(self):
        with self.assertRaises(TypeError):
            self._make_one(
                2016, 12, 20, 21, 13, 47,
                microsecond=123456, nanosecond=123456789)

    def test_rfc339_wo_nanos(self):
        stamp = self._make_one(2016, 12, 20, 21, 13, 47, 123456)
        self.assertEqual(stamp.rfc3339(),
                         '2016-12-20T21:13:47.123456Z')

    def test_rfc339_w_nanos(self):
        stamp = self._make_one(2016, 12, 20, 21, 13, 47, nanosecond=123456789)
        self.assertEqual(stamp.rfc3339(),
                         '2016-12-20T21:13:47.123456789Z')

    def test_rfc339_w_nanos_no_trailing_zeroes(self):
        stamp = self._make_one(2016, 12, 20, 21, 13, 47, nanosecond=100000000)
        self.assertEqual(stamp.rfc3339(),
                         '2016-12-20T21:13:47.1Z')

    def test_from_rfc3339_w_invalid(self):
        klass = self._get_target_class()
        STAMP = '2016-12-20T21:13:47'
        with self.assertRaises(ValueError):
            klass.from_rfc3339(STAMP)

    def test_from_rfc3339_wo_fraction(self):
        from google.cloud._helpers import UTC

        klass = self._get_target_class()
        STAMP = '2016-12-20T21:13:47Z'
        expected = self._make_one(2016, 12, 20, 21, 13, 47, tzinfo=UTC)
        stamp = klass.from_rfc3339(STAMP)
        self.assertEqual(stamp, expected)

    def test_from_rfc3339_w_partial_precision(self):
        from google.cloud._helpers import UTC

        klass = self._get_target_class()
        STAMP = '2016-12-20T21:13:47.1Z'
        expected = self._make_one(2016, 12, 20, 21, 13, 47,
                                  microsecond=100000, tzinfo=UTC)
        stamp = klass.from_rfc3339(STAMP)
        self.assertEqual(stamp, expected)

    def test_from_rfc3339_w_full_precision(self):
        from google.cloud._helpers import UTC

        klass = self._get_target_class()
        STAMP = '2016-12-20T21:13:47.123456789Z'
        expected = self._make_one(2016, 12, 20, 21, 13, 47,
                                  nanosecond=123456789, tzinfo=UTC)
        stamp = klass.from_rfc3339(STAMP)
        self.assertEqual(stamp, expected)


class Test_make_value_pb(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner._helpers import _make_value_pb

        return _make_value_pb(*args, **kw)

    def test_w_None(self):
        value_pb = self._callFUT(None)
        self.assertTrue(value_pb.HasField('null_value'))

    def test_w_bytes(self):
        from google.protobuf.struct_pb2 import Value

        BYTES = b'BYTES'
        expected = Value(string_value=BYTES)
        value_pb = self._callFUT(BYTES)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb, expected)

    def test_w_invalid_bytes(self):
        BYTES = b'\xff\xfe\x03&'
        with self.assertRaises(ValueError):
            self._callFUT(BYTES)

    def test_w_explicit_unicode(self):
        from google.protobuf.struct_pb2 import Value

        TEXT = u'TEXT'
        value_pb = self._callFUT(TEXT)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, TEXT)

    def test_w_list(self):
        from google.protobuf.struct_pb2 import Value
        from google.protobuf.struct_pb2 import ListValue

        value_pb = self._callFUT([u'a', u'b', u'c'])
        self.assertIsInstance(value_pb, Value)
        self.assertIsInstance(value_pb.list_value, ListValue)
        values = value_pb.list_value.values
        self.assertEqual([value.string_value for value in values],
                         [u'a', u'b', u'c'])

    def test_w_bool(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(True)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.bool_value, True)

    def test_w_int(self):
        import six
        from google.protobuf.struct_pb2 import Value

        for int_type in six.integer_types:  # include 'long' on Python 2
            value_pb = self._callFUT(int_type(42))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, '42')

    def test_w_float(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(3.14159)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.number_value, 3.14159)

    def test_w_float_nan(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float('nan'))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, 'NaN')

    def test_w_float_neg_inf(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float('-inf'))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, '-inf')

    def test_w_float_pos_inf(self):
        from google.protobuf.struct_pb2 import Value

        value_pb = self._callFUT(float('inf'))
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, 'inf')

    def test_w_date(self):
        import datetime
        from google.protobuf.struct_pb2 import Value

        today = datetime.date.today()
        value_pb = self._callFUT(today)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, today.isoformat())

    def test_w_timestamp_w_nanos(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud._helpers import UTC
        from google.cloud.spanner._helpers import TimestampWithNanoseconds

        when = TimestampWithNanoseconds(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=UTC)
        value_pb = self._callFUT(when)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, when.rfc3339())

    def test_w_datetime(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.cloud._helpers import UTC, _datetime_to_rfc3339

        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        value_pb = self._callFUT(now)
        self.assertIsInstance(value_pb, Value)
        self.assertEqual(value_pb.string_value, _datetime_to_rfc3339(now))

    def test_w_unknown_type(self):
        with self.assertRaises(ValueError):
            self._callFUT(object())


class Test_make_list_value_pb(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner._helpers import _make_list_value_pb

        return _make_list_value_pb(*args, **kw)

    def test_empty(self):
        from google.protobuf.struct_pb2 import ListValue

        result = self._callFUT(values=[])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 0)

    def test_w_single_value(self):
        from google.protobuf.struct_pb2 import ListValue

        VALUE = u'value'
        result = self._callFUT(values=[VALUE])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 1)
        self.assertEqual(result.values[0].string_value, VALUE)

    def test_w_multiple_values(self):
        from google.protobuf.struct_pb2 import ListValue

        VALUE_1 = u'value'
        VALUE_2 = 42
        result = self._callFUT(values=[VALUE_1, VALUE_2])
        self.assertIsInstance(result, ListValue)
        self.assertEqual(len(result.values), 2)
        self.assertEqual(result.values[0].string_value, VALUE_1)
        self.assertEqual(result.values[1].string_value, str(VALUE_2))


class Test_make_list_value_pbs(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner._helpers import _make_list_value_pbs

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

        values = [[0, u'A'], [1, u'B']]
        result = self._callFUT(values=values)
        self.assertEqual(len(result), len(values))
        for found, expected in zip(result, values):
            self.assertIsInstance(found, ListValue)
            self.assertEqual(len(found.values), 2)
            self.assertEqual(found.values[0].string_value, str(expected[0]))
            self.assertEqual(found.values[1].string_value, expected[1])


class Test_parse_value_pb(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner._helpers import _parse_value_pb

        return _parse_value_pb(*args, **kw)

    def test_w_null(self):
        from google.protobuf.struct_pb2 import Value, NULL_VALUE
        from google.cloud.proto.spanner.v1.type_pb2 import Type, STRING

        field_type = Type(code=STRING)
        value_pb = Value(null_value=NULL_VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), None)

    def test_w_string(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, STRING

        VALUE = u'Value'
        field_type = Type(code=STRING)
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_bytes(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, BYTES

        VALUE = b'Value'
        field_type = Type(code=BYTES)
        value_pb = Value(string_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_bool(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, BOOL

        VALUE = True
        field_type = Type(code=BOOL)
        value_pb = Value(bool_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_int(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, INT64

        VALUE = 12345
        field_type = Type(code=INT64)
        value_pb = Value(string_value=str(VALUE))

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_float(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, FLOAT64

        VALUE = 3.14159
        field_type = Type(code=FLOAT64)
        value_pb = Value(number_value=VALUE)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_date(self):
        import datetime
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, DATE

        VALUE = datetime.date.today()
        field_type = Type(code=DATE)
        value_pb = Value(string_value=VALUE.isoformat())

        self.assertEqual(self._callFUT(value_pb, field_type), VALUE)

    def test_w_timestamp_wo_nanos(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, TIMESTAMP
        from google.cloud._helpers import UTC, _datetime_to_rfc3339
        from google.cloud.spanner._helpers import TimestampWithNanoseconds

        VALUE = TimestampWithNanoseconds(
            2016, 12, 20, 21, 13, 47, microsecond=123456, tzinfo=UTC)
        field_type = Type(code=TIMESTAMP)
        value_pb = Value(string_value=_datetime_to_rfc3339(VALUE))

        parsed = self._callFUT(value_pb, field_type)
        self.assertIsInstance(parsed, TimestampWithNanoseconds)
        self.assertEqual(parsed, VALUE)

    def test_w_timestamp_w_nanos(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, TIMESTAMP
        from google.cloud._helpers import UTC, _datetime_to_rfc3339
        from google.cloud.spanner._helpers import TimestampWithNanoseconds

        VALUE = TimestampWithNanoseconds(
            2016, 12, 20, 21, 13, 47, nanosecond=123456789, tzinfo=UTC)
        field_type = Type(code=TIMESTAMP)
        value_pb = Value(string_value=_datetime_to_rfc3339(VALUE))

        parsed = self._callFUT(value_pb, field_type)
        self.assertIsInstance(parsed, TimestampWithNanoseconds)
        self.assertEqual(parsed, VALUE)

    def test_w_array_empty(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, ARRAY, INT64

        field_type = Type(code=ARRAY, array_element_type=Type(code=INT64))
        value_pb = Value()

        self.assertEqual(self._callFUT(value_pb, field_type), [])

    def test_w_array_non_empty(self):
        from google.protobuf.struct_pb2 import Value, ListValue
        from google.cloud.proto.spanner.v1.type_pb2 import Type, ARRAY, INT64

        field_type = Type(code=ARRAY, array_element_type=Type(code=INT64))
        VALUES = [32, 19, 5]
        values_pb = ListValue(
            values=[Value(string_value=str(value)) for value in VALUES])
        value_pb = Value(list_value=values_pb)

        self.assertEqual(self._callFUT(value_pb, field_type), VALUES)

    def test_w_struct(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type, StructType
        from google.cloud.proto.spanner.v1.type_pb2 import (
            STRUCT, STRING, INT64)
        from google.cloud.spanner._helpers import _make_list_value_pb

        VALUES = [u'phred', 32]
        struct_type_pb = StructType(fields=[
            StructType.Field(name='name', type=Type(code=STRING)),
            StructType.Field(name='age', type=Type(code=INT64)),
        ])
        field_type = Type(code=STRUCT, struct_type=struct_type_pb)
        value_pb = Value(list_value=_make_list_value_pb(VALUES))

        self.assertEqual(self._callFUT(value_pb, field_type), VALUES)

    def test_w_unknown_type(self):
        from google.protobuf.struct_pb2 import Value
        from google.cloud.proto.spanner.v1.type_pb2 import Type
        from google.cloud.proto.spanner.v1.type_pb2 import (
            TYPE_CODE_UNSPECIFIED)

        field_type = Type(code=TYPE_CODE_UNSPECIFIED)
        value_pb = Value(string_value='Borked')

        with self.assertRaises(ValueError):
            self._callFUT(value_pb, field_type)


class Test_parse_list_value_pbs(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from google.cloud.spanner._helpers import _parse_list_value_pbs

        return _parse_list_value_pbs(*args, **kw)

    def test_empty(self):
        from google.cloud.proto.spanner.v1.type_pb2 import Type, StructType
        from google.cloud.proto.spanner.v1.type_pb2 import STRING, INT64

        struct_type_pb = StructType(fields=[
            StructType.Field(name='name', type=Type(code=STRING)),
            StructType.Field(name='age', type=Type(code=INT64)),
        ])

        self.assertEqual(self._callFUT(rows=[], row_type=struct_type_pb), [])

    def test_non_empty(self):
        from google.cloud.proto.spanner.v1.type_pb2 import Type, StructType
        from google.cloud.proto.spanner.v1.type_pb2 import STRING, INT64
        from google.cloud.spanner._helpers import _make_list_value_pbs

        VALUES = [
            [u'phred', 32],
            [u'bharney', 31],
        ]
        struct_type_pb = StructType(fields=[
            StructType.Field(name='name', type=Type(code=STRING)),
            StructType.Field(name='age', type=Type(code=INT64)),
        ])
        values_pbs = _make_list_value_pbs(VALUES)

        self.assertEqual(
            self._callFUT(rows=values_pbs, row_type=struct_type_pb), VALUES)


class Test_SessionWrapper(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.spanner._helpers import _SessionWrapper

        return _SessionWrapper

    def _make_one(self, session):
        return self._getTargetClass()(session)

    def test_ctor(self):
        session = object()
        base = self._make_one(session)
        self.assertTrue(base._session is session)


class Test_options_with_prefix(unittest.TestCase):

    def _call_fut(self, *args, **kw):
        from google.cloud.spanner._helpers import _options_with_prefix

        return _options_with_prefix(*args, **kw)

    def test_wo_kwargs(self):
        from google.gax import CallOptions

        PREFIX = 'prefix'
        options = self._call_fut(PREFIX)
        self.assertIsInstance(options, CallOptions)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', PREFIX)])

    def test_w_kwargs(self):
        from google.gax import CallOptions

        PREFIX = 'prefix'
        TOKEN = 'token'
        options = self._call_fut('prefix', page_token=TOKEN)
        self.assertIsInstance(options, CallOptions)
        self.assertEqual(options.kwargs['metadata'],
                         [('google-cloud-resource-prefix', PREFIX)])
        self.assertEqual(options.page_token, TOKEN)
