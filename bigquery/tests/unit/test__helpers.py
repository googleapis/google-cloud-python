# Copyright 2015 Google Inc.
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
import datetime
import unittest

import mock


class Test_not_null(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _not_null

        return _not_null(value, field)

    def test_w_none_nullable(self):
        self.assertFalse(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        self.assertTrue(self._call_fut(None, _Field('REQUIRED')))

    def test_w_value(self):
        self.assertTrue(self._call_fut(object(), object()))


class Test_int_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _int_from_json

        return _int_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('42', object())
        self.assertEqual(coerced, 42)

    def test_w_float_value(self):
        coerced = self._call_fut(42, object())
        self.assertEqual(coerced, 42)


class Test_float_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _float_from_json

        return _float_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('3.1415', object())
        self.assertEqual(coerced, 3.1415)

    def test_w_float_value(self):
        coerced = self._call_fut(3.1415, object())
        self.assertEqual(coerced, 3.1415)


class Test_bool_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _bool_from_json

        return _bool_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(AttributeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_value_t(self):
        coerced = self._call_fut('T', object())
        self.assertTrue(coerced)

    def test_w_value_true(self):
        coerced = self._call_fut('True', object())
        self.assertTrue(coerced)

    def test_w_value_1(self):
        coerced = self._call_fut('1', object())
        self.assertTrue(coerced)

    def test_w_value_other(self):
        coerced = self._call_fut('f', object())
        self.assertFalse(coerced)


class Test_string_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _string_from_json

        return _string_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        self.assertIsNone(self._call_fut(None, _Field('REQUIRED')))

    def test_w_string_value(self):
        coerced = self._call_fut('Wonderful!', object())
        self.assertEqual(coerced, 'Wonderful!')


class Test_bytes_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _bytes_from_json

        return _bytes_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_base64_encoded_bytes(self):
        expected = b'Wonderful!'
        encoded = base64.standard_b64encode(expected)
        coerced = self._call_fut(encoded, object())
        self.assertEqual(coerced, expected)

    def test_w_base64_encoded_text(self):
        expected = b'Wonderful!'
        encoded = base64.standard_b64encode(expected).decode('ascii')
        coerced = self._call_fut(encoded, object())
        self.assertEqual(coerced, expected)


class Test_timestamp_query_param_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery import _helpers

        return _helpers._timestamp_query_param_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_timestamp_valid(self):
        from google.cloud._helpers import UTC

        samples = [
            (
                '2016-12-20 15:58:27.339328+00:00',
                datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
            ),
            (
                '2016-12-20 15:58:27+00:00',
                datetime.datetime(2016, 12, 20, 15, 58, 27, tzinfo=UTC)
            ),
            (
                '2016-12-20T15:58:27.339328+00:00',
                datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
            ),
            (
                '2016-12-20T15:58:27+00:00',
                datetime.datetime(2016, 12, 20, 15, 58, 27, tzinfo=UTC)
            ),
            (
                '2016-12-20 15:58:27.339328Z',
                datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
            ),
            (
                '2016-12-20 15:58:27Z',
                datetime.datetime(2016, 12, 20, 15, 58, 27, tzinfo=UTC)
            ),
            (
                '2016-12-20T15:58:27.339328Z',
                datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
            ),
            (
                '2016-12-20T15:58:27Z',
                datetime.datetime(2016, 12, 20, 15, 58, 27, tzinfo=UTC)
            ),
        ]
        for timestamp_str, expected_result in samples:
            self.assertEqual(
                self._call_fut(timestamp_str, _Field('NULLABLE')),
                expected_result)

    def test_w_timestamp_invalid(self):
        with self.assertRaises(ValueError):
            self._call_fut('definitely-not-a-timestamp', _Field('NULLABLE'))


class Test_timestamp_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _timestamp_from_json

        return _timestamp_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        from google.cloud._helpers import _EPOCH

        coerced = self._call_fut('1.234567', object())
        self.assertEqual(
            coerced,
            _EPOCH + datetime.timedelta(seconds=1, microseconds=234567))

    def test_w_float_value(self):
        from google.cloud._helpers import _EPOCH

        coerced = self._call_fut(1.234567, object())
        self.assertEqual(
            coerced,
            _EPOCH + datetime.timedelta(seconds=1, microseconds=234567))


class Test_datetime_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _datetime_from_json

        return _datetime_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('2016-12-02T18:51:33', object())
        self.assertEqual(
            coerced,
            datetime.datetime(2016, 12, 2, 18, 51, 33))

    def test_w_microseconds(self):
        coerced = self._call_fut('2015-05-22T10:11:12.987654', object())
        self.assertEqual(
            coerced,
            datetime.datetime(2015, 5, 22, 10, 11, 12, 987654))


class Test_date_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _date_from_json

        return _date_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('1987-09-22', object())
        self.assertEqual(
            coerced,
            datetime.date(1987, 9, 22))


class Test_time_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _time_from_json

        return _time_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('12:12:27', object())
        self.assertEqual(
            coerced,
            datetime.time(12, 12, 27))


class Test_record_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _record_from_json

        return _record_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_nullable_subfield_none(self):
        subfield = _Field('NULLABLE', 'age', 'INTEGER')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': None}]}
        coerced = self._call_fut(value, field)
        self.assertEqual(coerced, {'age': None})

    def test_w_scalar_subfield(self):
        subfield = _Field('REQUIRED', 'age', 'INTEGER')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': 42}]}
        coerced = self._call_fut(value, field)
        self.assertEqual(coerced, {'age': 42})

    def test_w_repeated_subfield(self):
        subfield = _Field('REPEATED', 'color', 'STRING')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': [{'v': 'red'}, {'v': 'yellow'}, {'v': 'blue'}]}]}
        coerced = self._call_fut(value, field)
        self.assertEqual(coerced, {'color': ['red', 'yellow', 'blue']})

    def test_w_record_subfield(self):
        full_name = _Field('REQUIRED', 'full_name', 'STRING')
        area_code = _Field('REQUIRED', 'area_code', 'STRING')
        local_number = _Field('REQUIRED', 'local_number', 'STRING')
        rank = _Field('REQUIRED', 'rank', 'INTEGER')
        phone = _Field('NULLABLE', 'phone', 'RECORD',
                       fields=[area_code, local_number, rank])
        person = _Field('REQUIRED', 'person', 'RECORD',
                        fields=[full_name, phone])
        value = {
            'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': {'f': [{'v': '800'}, {'v': '555-1212'}, {'v': 1}]}},
            ],
        }
        expected = {
            'full_name': 'Phred Phlyntstone',
            'phone': {
                'area_code': '800',
                'local_number': '555-1212',
                'rank': 1,
            }
        }
        coerced = self._call_fut(value, person)
        self.assertEqual(coerced, expected)


class Test_row_tuple_from_json(unittest.TestCase):

    def _call_fut(self, row, schema):
        from google.cloud.bigquery._helpers import _row_tuple_from_json

        return _row_tuple_from_json(row, schema)

    def test_w_single_scalar_column(self):
        # SELECT 1 AS col
        col = _Field('REQUIRED', 'col', 'INTEGER')
        row = {u'f': [{u'v': u'1'}]}
        self.assertEqual(self._call_fut(row, schema=[col]), (1,))

    def test_w_single_struct_column(self):
        # SELECT (1, 2) AS col
        sub_1 = _Field('REQUIRED', 'sub_1', 'INTEGER')
        sub_2 = _Field('REQUIRED', 'sub_2', 'INTEGER')
        col = _Field('REQUIRED', 'col', 'RECORD', fields=[sub_1, sub_2])
        row = {u'f': [{u'v': {u'f': [{u'v': u'1'}, {u'v': u'2'}]}}]}
        self.assertEqual(self._call_fut(row, schema=[col]),
                         ({'sub_1': 1, 'sub_2': 2},))

    def test_w_single_array_column(self):
        # SELECT [1, 2, 3] as col
        col = _Field('REPEATED', 'col', 'INTEGER')
        row = {u'f': [{u'v': [{u'v': u'1'}, {u'v': u'2'}, {u'v': u'3'}]}]}
        self.assertEqual(self._call_fut(row, schema=[col]),
                         ([1, 2, 3],))

    def test_w_struct_w_nested_array_column(self):
        # SELECT ([1, 2], 3, [4, 5]) as col
        first = _Field('REPEATED', 'first', 'INTEGER')
        second = _Field('REQUIRED', 'second', 'INTEGER')
        third = _Field('REPEATED', 'third', 'INTEGER')
        col = _Field('REQUIRED', 'col', 'RECORD',
                     fields=[first, second, third])
        row = {
            u'f': [
                {u'v': {
                    u'f': [
                        {u'v': [{u'v': u'1'}, {u'v': u'2'}]},
                        {u'v': u'3'},
                        {u'v': [{u'v': u'4'}, {u'v': u'5'}]}
                    ]
                }},
            ]
        }
        self.assertEqual(
            self._call_fut(row, schema=[col]),
            ({u'first': [1, 2], u'second': 3, u'third': [4, 5]},))

    def test_w_array_of_struct(self):
        # SELECT [(1, 2, 3), (4, 5, 6)] as col
        first = _Field('REQUIRED', 'first', 'INTEGER')
        second = _Field('REQUIRED', 'second', 'INTEGER')
        third = _Field('REQUIRED', 'third', 'INTEGER')
        col = _Field('REPEATED', 'col', 'RECORD',
                     fields=[first, second, third])
        row = {u'f': [{u'v': [
            {u'v': {u'f': [{u'v': u'1'}, {u'v': u'2'}, {u'v': u'3'}]}},
            {u'v': {u'f': [{u'v': u'4'}, {u'v': u'5'}, {u'v': u'6'}]}},
        ]}]}
        self.assertEqual(
            self._call_fut(row, schema=[col]),
            ([
                {u'first': 1, u'second': 2, u'third': 3},
                {u'first': 4, u'second': 5, u'third': 6},
            ],))

    def test_w_array_of_struct_w_array(self):
        # SELECT [([1, 2, 3], 4), ([5, 6], 7)]
        first = _Field('REPEATED', 'first', 'INTEGER')
        second = _Field('REQUIRED', 'second', 'INTEGER')
        col = _Field('REPEATED', 'col', 'RECORD', fields=[first, second])
        row = {u'f': [{u'v': [
            {u'v': {u'f': [
                {u'v': [{u'v': u'1'}, {u'v': u'2'}, {u'v': u'3'}]},
                {u'v': u'4'}
            ]}},
            {u'v': {u'f': [
                {u'v': [{u'v': u'5'}, {u'v': u'6'}]},
                {u'v': u'7'}
            ]}}
        ]}]}
        self.assertEqual(
            self._call_fut(row, schema=[col]),
            ([
                {u'first': [1, 2, 3], u'second': 4},
                {u'first': [5, 6], u'second': 7},
            ],))

    def test_row(self):
        from google.cloud.bigquery._helpers import Row

        VALUES = (1, 2, 3)
        r = Row(VALUES, {'a': 0, 'b': 1, 'c': 2})
        self.assertEqual(r.a, 1)
        self.assertEqual(r[1], 2)
        self.assertEqual(r['c'], 3)
        self.assertEqual(len(r), 3)
        self.assertEqual(r.values(), VALUES)
        self.assertEqual(repr(r),
                         "Row((1, 2, 3), {'a': 0, 'b': 1, 'c': 2})")
        self.assertFalse(r != r)
        self.assertFalse(r == 3)
        with self.assertRaises(AttributeError):
            r.z
        with self.assertRaises(KeyError):
            r['z']


class Test_rows_from_json(unittest.TestCase):

    def _call_fut(self, rows, schema):
        from google.cloud.bigquery._helpers import _rows_from_json

        return _rows_from_json(rows, schema)

    def test_w_record_subfield(self):
        from google.cloud.bigquery._helpers import Row

        full_name = _Field('REQUIRED', 'full_name', 'STRING')
        area_code = _Field('REQUIRED', 'area_code', 'STRING')
        local_number = _Field('REQUIRED', 'local_number', 'STRING')
        rank = _Field('REQUIRED', 'rank', 'INTEGER')
        phone = _Field('NULLABLE', 'phone', 'RECORD',
                       fields=[area_code, local_number, rank])
        color = _Field('REPEATED', 'color', 'STRING')
        schema = [full_name, phone, color]
        rows = [
            {'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': {'f': [{'v': '800'}, {'v': '555-1212'}, {'v': 1}]}},
                {'v': [{'v': 'orange'}, {'v': 'black'}]},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': {'f': [{'v': '877'}, {'v': '768-5309'}, {'v': 2}]}},
                {'v': [{'v': 'brown'}]},
            ]},
            {'f': [
                {'v': 'Wylma Phlyntstone'},
                {'v': None},
                {'v': []},
            ]},
        ]
        phred_phone = {
            'area_code': '800',
            'local_number': '555-1212',
            'rank': 1,
        }
        bharney_phone = {
            'area_code': '877',
            'local_number': '768-5309',
            'rank': 2,
        }
        f2i = {'full_name': 0, 'phone': 1, 'color': 2}
        expected = [
            Row(('Phred Phlyntstone', phred_phone, ['orange', 'black']), f2i),
            Row(('Bharney Rhubble', bharney_phone, ['brown']), f2i),
            Row(('Wylma Phlyntstone', None, []), f2i),
        ]
        coerced = self._call_fut(rows, schema)
        self.assertEqual(coerced, expected)

    def test_w_int64_float64_bool(self):
        from google.cloud.bigquery._helpers import Row

        # "Standard" SQL dialect uses 'INT64', 'FLOAT64', 'BOOL'.
        candidate = _Field('REQUIRED', 'candidate', 'STRING')
        votes = _Field('REQUIRED', 'votes', 'INT64')
        percentage = _Field('REQUIRED', 'percentage', 'FLOAT64')
        incumbent = _Field('REQUIRED', 'incumbent', 'BOOL')
        schema = [candidate, votes, percentage, incumbent]
        rows = [
            {'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': 8},
                {'v': 0.25},
                {'v': 'true'},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': 4},
                {'v': 0.125},
                {'v': 'false'},
            ]},
            {'f': [
                {'v': 'Wylma Phlyntstone'},
                {'v': 20},
                {'v': 0.625},
                {'v': 'false'},
            ]},
        ]
        f2i = {'candidate': 0, 'votes': 1, 'percentage': 2, 'incumbent': 3}
        expected = [
            Row(('Phred Phlyntstone', 8, 0.25, True), f2i),
            Row(('Bharney Rhubble', 4, 0.125, False), f2i),
            Row(('Wylma Phlyntstone', 20, 0.625, False), f2i),
        ]
        coerced = self._call_fut(rows, schema)
        self.assertEqual(coerced, expected)


class Test_int_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _int_to_json

        return _int_to_json(value)

    def test_w_int(self):
        self.assertEqual(self._call_fut(123), '123')

    def test_w_string(self):
        self.assertEqual(self._call_fut('123'), '123')


class Test_float_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _float_to_json

        return _float_to_json(value)

    def test_w_float(self):
        self.assertEqual(self._call_fut(1.23), 1.23)


class Test_bool_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _bool_to_json

        return _bool_to_json(value)

    def test_w_true(self):
        self.assertEqual(self._call_fut(True), 'true')

    def test_w_false(self):
        self.assertEqual(self._call_fut(False), 'false')

    def test_w_string(self):
        self.assertEqual(self._call_fut('false'), 'false')


class Test_bytes_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _bytes_to_json

        return _bytes_to_json(value)

    def test_w_non_bytes(self):
        non_bytes = object()
        self.assertIs(self._call_fut(non_bytes), non_bytes)

    def test_w_bytes(self):
        source = b'source'
        expected = u'c291cmNl'
        converted = self._call_fut(source)
        self.assertEqual(converted, expected)


class Test_timestamp_to_json_parameter(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _timestamp_to_json_parameter

        return _timestamp_to_json_parameter(value)

    def test_w_float(self):
        self.assertEqual(self._call_fut(1.234567), 1.234567)

    def test_w_string(self):
        ZULU = '2016-12-20 15:58:27.339328+00:00'
        self.assertEqual(self._call_fut(ZULU), ZULU)

    def test_w_datetime_wo_zone(self):
        ZULU = '2016-12-20 15:58:27.339328+00:00'
        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328)
        self.assertEqual(self._call_fut(when), ZULU)

    def test_w_datetime_w_non_utc_zone(self):
        class _Zone(datetime.tzinfo):

            def utcoffset(self, _):
                return datetime.timedelta(minutes=-240)

        ZULU = '2016-12-20 19:58:27.339328+00:00'
        when = datetime.datetime(
            2016, 12, 20, 15, 58, 27, 339328, tzinfo=_Zone())
        self.assertEqual(self._call_fut(when), ZULU)

    def test_w_datetime_w_utc_zone(self):
        from google.cloud._helpers import UTC

        ZULU = '2016-12-20 15:58:27.339328+00:00'
        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
        self.assertEqual(self._call_fut(when), ZULU)


class Test_timestamp_to_json_row(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _timestamp_to_json_row

        return _timestamp_to_json_row(value)

    def test_w_float(self):
        self.assertEqual(self._call_fut(1.234567), 1.234567)

    def test_w_string(self):
        ZULU = '2016-12-20 15:58:27.339328+00:00'
        self.assertEqual(self._call_fut(ZULU), ZULU)

    def test_w_datetime(self):
        from google.cloud._helpers import _microseconds_from_datetime

        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328)
        self.assertEqual(
            self._call_fut(when), _microseconds_from_datetime(when) / 1e6)


class Test_datetime_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _datetime_to_json

        return _datetime_to_json(value)

    def test_w_string(self):
        RFC3339 = '2016-12-03T14:14:51Z'
        self.assertEqual(self._call_fut(RFC3339), RFC3339)

    def test_w_datetime(self):
        from google.cloud._helpers import UTC

        when = datetime.datetime(2016, 12, 3, 14, 11, 27, 123456, tzinfo=UTC)
        self.assertEqual(self._call_fut(when), '2016-12-03T14:11:27.123456')


class Test_date_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _date_to_json

        return _date_to_json(value)

    def test_w_string(self):
        RFC3339 = '2016-12-03'
        self.assertEqual(self._call_fut(RFC3339), RFC3339)

    def test_w_datetime(self):
        when = datetime.date(2016, 12, 3)
        self.assertEqual(self._call_fut(when), '2016-12-03')


class Test_time_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _time_to_json

        return _time_to_json(value)

    def test_w_string(self):
        RFC3339 = '12:13:41'
        self.assertEqual(self._call_fut(RFC3339), RFC3339)

    def test_w_datetime(self):
        when = datetime.time(12, 13, 41)
        self.assertEqual(self._call_fut(when), '12:13:41')


class Test_ConfigurationProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import _ConfigurationProperty

        return _ConfigurationProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._make_one('attr')

            def __init__(self):
                self._configuration = Configuration()

        self.assertEqual(Wrapper.attr.name, 'attr')

        wrapper = Wrapper()
        self.assertIsNone(wrapper.attr)

        value = object()
        wrapper.attr = value
        self.assertIs(wrapper.attr, value)
        self.assertIs(wrapper._configuration._attr, value)

        del wrapper.attr
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._configuration._attr)


class Test_TypedApiResourceProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import _TypedApiResourceProperty

        return _TypedApiResourceProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_it(self):

        class Wrapper(object):
            attr = self._make_one('attr', 'back', int)

            def __init__(self):
                self._properties = {}

        self.assertIsNotNone(Wrapper.attr)

        wrapper = Wrapper()
        with self.assertRaises(ValueError):
            wrapper.attr = 'BOGUS'

        wrapper.attr = 42
        self.assertEqual(wrapper.attr, 42)
        self.assertEqual(wrapper._properties['back'], 42)

        wrapper.attr = None
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._properties['back'])

        wrapper.attr = 23
        self.assertEqual(wrapper.attr, 23)
        self.assertEqual(wrapper._properties['back'], 23)

        del wrapper.attr
        self.assertIsNone(wrapper.attr)
        with self.assertRaises(KeyError):
            wrapper._properties['back']


class Test_TypedProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import _TypedProperty

        return _TypedProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._make_one('attr', int)

            def __init__(self):
                self._configuration = Configuration()

        wrapper = Wrapper()
        with self.assertRaises(ValueError):
            wrapper.attr = 'BOGUS'

        wrapper.attr = 42
        self.assertEqual(wrapper.attr, 42)
        self.assertEqual(wrapper._configuration._attr, 42)

        wrapper.attr = None
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._configuration._attr)

        wrapper.attr = 23
        self.assertEqual(wrapper.attr, 23)
        self.assertEqual(wrapper._configuration._attr, 23)

        del wrapper.attr
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._configuration._attr)


class Test_EnumProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import _EnumProperty

        return _EnumProperty

    def test_it(self):

        class Sub(self._get_target_class()):
            pass

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = Sub('attr')

            def __init__(self):
                self._configuration = Configuration()

        wrapper = Wrapper()
        wrapper.attr = 'FOO'
        self.assertEqual(wrapper.attr, 'FOO')
        self.assertEqual(wrapper._configuration._attr, 'FOO')

        del wrapper.attr
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._configuration._attr)


class Test_AbstractQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import AbstractQueryParameter

        return AbstractQueryParameter

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_from_api_virtual(self):
        klass = self._get_target_class()
        with self.assertRaises(NotImplementedError):
            klass.from_api_repr({})

    def test_to_api_virtual(self):
        param = self._make_one()
        with self.assertRaises(NotImplementedError):
            param.to_api_repr()


class Test_ScalarQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        return ScalarQueryParameter

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        param = self._make_one(name='foo', type_='INT64', value=123)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.type_, 'INT64')
        self.assertEqual(param.value, 123)

    def test___eq__(self):
        param = self._make_one(name='foo', type_='INT64', value=123)
        self.assertEqual(param, param)
        self.assertNotEqual(param, object())
        alias = self._make_one(name='bar', type_='INT64', value=123)
        self.assertNotEqual(param, alias)
        wrong_type = self._make_one(name='foo', type_='FLOAT64', value=123.0)
        self.assertNotEqual(param, wrong_type)
        wrong_val = self._make_one(name='foo', type_='INT64', value=234)
        self.assertNotEqual(param, wrong_val)

    def test_positional(self):
        klass = self._get_target_class()
        param = klass.positional(type_='INT64', value=123)
        self.assertEqual(param.name, None)
        self.assertEqual(param.type_, 'INT64')
        self.assertEqual(param.value, 123)

    def test_from_api_repr_w_name(self):
        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'INT64',
            },
            'parameterValue': {
                'value': 123,
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.type_, 'INT64')
        self.assertEqual(param.value, 123)

    def test_from_api_repr_wo_name(self):
        RESOURCE = {
            'parameterType': {
                'type': 'INT64',
            },
            'parameterValue': {
                'value': '123',
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, None)
        self.assertEqual(param.type_, 'INT64')
        self.assertEqual(param.value, 123)

    def test_to_api_repr_w_name(self):
        EXPECTED = {
            'name': 'foo',
            'parameterType': {
                'type': 'INT64',
            },
            'parameterValue': {
                'value': '123',
            },
        }
        param = self._make_one(name='foo', type_='INT64', value=123)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_wo_name(self):
        EXPECTED = {
            'parameterType': {
                'type': 'INT64',
            },
            'parameterValue': {
                'value': '123',
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='INT64', value=123)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_float(self):
        EXPECTED = {
            'parameterType': {
                'type': 'FLOAT64',
            },
            'parameterValue': {
                'value': 12.345,
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='FLOAT64', value=12.345)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_bool(self):
        EXPECTED = {
            'parameterType': {
                'type': 'BOOL',
            },
            'parameterValue': {
                'value': 'false',
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='BOOL', value=False)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_timestamp_datetime(self):
        from google.cloud._helpers import UTC

        STAMP = '2016-12-20 15:58:27.339328+00:00'
        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
        EXPECTED = {
            'parameterType': {
                'type': 'TIMESTAMP',
            },
            'parameterValue': {
                'value': STAMP,
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='TIMESTAMP', value=when)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_timestamp_micros(self):
        from google.cloud._helpers import _microseconds_from_datetime

        now = datetime.datetime.utcnow()
        seconds = _microseconds_from_datetime(now) / 1.0e6
        EXPECTED = {
            'parameterType': {
                'type': 'TIMESTAMP',
            },
            'parameterValue': {
                'value': seconds,
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='TIMESTAMP', value=seconds)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_datetime_datetime(self):
        from google.cloud._helpers import _datetime_to_rfc3339

        now = datetime.datetime.utcnow()
        EXPECTED = {
            'parameterType': {
                'type': 'DATETIME',
            },
            'parameterValue': {
                'value': _datetime_to_rfc3339(now)[:-1],  # strip trailing 'Z'
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='DATETIME', value=now)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_datetime_string(self):
        from google.cloud._helpers import _datetime_to_rfc3339

        now = datetime.datetime.utcnow()
        now_str = _datetime_to_rfc3339(now)
        EXPECTED = {
            'parameterType': {
                'type': 'DATETIME',
            },
            'parameterValue': {
                'value': now_str,
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='DATETIME', value=now_str)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_date_date(self):
        today = datetime.date.today()
        EXPECTED = {
            'parameterType': {
                'type': 'DATE',
            },
            'parameterValue': {
                'value': today.isoformat(),
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='DATE', value=today)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_date_string(self):
        today = datetime.date.today()
        today_str = today.isoformat(),
        EXPECTED = {
            'parameterType': {
                'type': 'DATE',
            },
            'parameterValue': {
                'value': today_str,
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='DATE', value=today_str)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_unknown_type(self):
        EXPECTED = {
            'parameterType': {
                'type': 'UNKNOWN',
            },
            'parameterValue': {
                'value': 'unknown',
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='UNKNOWN', value='unknown')
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test___eq___wrong_type(self):
        field = self._make_one('test', 'STRING', 'value')
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one('test', 'STRING', 'value')
        other = self._make_one('other', 'STRING', 'value')
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one('test', 'STRING', None)
        other = self._make_one('test', 'INT64', None)
        self.assertNotEqual(field, other)

    def test___eq___value_mismatch(self):
        field = self._make_one('test', 'STRING', 'hello')
        other = self._make_one('test', 'STRING', 'world')
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one('test', 'STRING', 'gotcha')
        other = self._make_one('test', 'STRING', 'gotcha')
        self.assertEqual(field, other)

    def test___ne___wrong_type(self):
        field = self._make_one('toast', 'INT64', 13)
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one('test', 'INT64', 12)
        field2 = self._make_one('test', 'INT64', 12)
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = (field1 != field2)
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one('test', 'INT64', 11)
        field2 = self._make_one('test', 'INT64', 12)
        self.assertNotEqual(field1, field2)

    def test___repr__(self):
        field1 = self._make_one('field1', 'STRING', 'value')
        expected = "ScalarQueryParameter('field1', 'STRING', 'value')"
        self.assertEqual(repr(field1), expected)


def _make_subparam(name, type_, value):
    from google.cloud.bigquery._helpers import ScalarQueryParameter

    return ScalarQueryParameter(name, type_, value)


class Test_ArrayQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import ArrayQueryParameter

        return ArrayQueryParameter

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        param = self._make_one(name='foo', array_type='INT64', values=[1, 2])
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.array_type, 'INT64')
        self.assertEqual(param.values, [1, 2])

    def test___eq__(self):
        param = self._make_one(name='foo', array_type='INT64', values=[123])
        self.assertEqual(param, param)
        self.assertNotEqual(param, object())
        alias = self._make_one(name='bar', array_type='INT64', values=[123])
        self.assertNotEqual(param, alias)
        wrong_type = self._make_one(
            name='foo', array_type='FLOAT64', values=[123.0])
        self.assertNotEqual(param, wrong_type)
        wrong_val = self._make_one(
            name='foo', array_type='INT64', values=[234])
        self.assertNotEqual(param, wrong_val)

    def test_positional(self):
        klass = self._get_target_class()
        param = klass.positional(array_type='INT64', values=[1, 2])
        self.assertEqual(param.name, None)
        self.assertEqual(param.array_type, 'INT64')
        self.assertEqual(param.values, [1, 2])

    def test_from_api_repr_w_name(self):
        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'value': '1',
                    },
                    {
                        'value': '2'
                    },
                ],
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.array_type, 'INT64')
        self.assertEqual(param.values, [1, 2])

    def test_from_api_repr_wo_name(self):
        RESOURCE = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'value': '1',
                    },
                    {
                        'value': '2'
                    },
                ],
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, None)
        self.assertEqual(param.array_type, 'INT64')
        self.assertEqual(param.values, [1, 2])

    def test_from_api_repr_w_struct_type(self):
        from google.cloud.bigquery._helpers import StructQueryParameter

        RESOURCE = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'STRUCT',
                    'structTypes': [
                        {
                            'name': 'name',
                            'type': {'type': 'STRING'},
                        },
                        {
                            'name': 'age',
                            'type': {'type': 'INT64'},
                        },
                    ],
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'structValues': {
                            'name': {'value': 'Phred Phlyntstone'},
                            'age': {'value': '32'},
                        },
                    },
                    {
                        'structValues': {
                            'name': {
                                'value': 'Bharney Rhubbyl',
                            },
                            'age': {'value': '31'},
                        },
                    },
                ],
            },
        }

        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)

        phred = StructQueryParameter.positional(
            _make_subparam('name', 'STRING', 'Phred Phlyntstone'),
            _make_subparam('age', 'INT64', 32))
        bharney = StructQueryParameter.positional(
            _make_subparam('name', 'STRING', 'Bharney Rhubbyl'),
            _make_subparam('age', 'INT64', 31))
        self.assertEqual(param.array_type, 'STRUCT')
        self.assertEqual(param.values, [phred, bharney])

    def test_to_api_repr_w_name(self):
        EXPECTED = {
            'name': 'foo',
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'value': '1',
                    },
                    {
                        'value': '2'
                    },
                ],
            },
        }
        param = self._make_one(name='foo', array_type='INT64', values=[1, 2])
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_wo_name(self):
        EXPECTED = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'INT64',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'value': '1',
                    },
                    {
                        'value': '2'
                    },
                ],
            },
        }
        klass = self._get_target_class()
        param = klass.positional(array_type='INT64', values=[1, 2])
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_unknown_type(self):
        EXPECTED = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'UNKNOWN',
                },
            },
            'parameterValue': {
                'arrayValues': [
                    {
                        'value': 'unknown',
                    }
                ],
            },
        }
        klass = self._get_target_class()
        param = klass.positional(array_type='UNKNOWN', values=['unknown'])
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_record_type(self):
        from google.cloud.bigquery._helpers import StructQueryParameter

        EXPECTED = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {
                    'type': 'STRUCT',
                    'structTypes': [
                        {'name': 'foo', 'type': {'type': 'STRING'}},
                        {'name': 'bar', 'type': {'type': 'INT64'}},
                    ],
                },
            },
            'parameterValue': {
                'arrayValues': [{
                    'structValues': {
                        'foo': {'value': 'Foo'},
                        'bar': {'value': '123'},
                    }
                }]
            },
        }
        one = _make_subparam('foo', 'STRING', 'Foo')
        another = _make_subparam('bar', 'INT64', 123)
        struct = StructQueryParameter.positional(one, another)
        klass = self._get_target_class()
        param = klass.positional(array_type='RECORD', values=[struct])
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test___eq___wrong_type(self):
        field = self._make_one('test', 'STRING', ['value'])
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one('field', 'STRING', ['value'])
        other = self._make_one('other', 'STRING', ['value'])
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one('test', 'STRING', [])
        other = self._make_one('test', 'INT64', [])
        self.assertNotEqual(field, other)

    def test___eq___value_mismatch(self):
        field = self._make_one('test', 'STRING', ['hello'])
        other = self._make_one('test', 'STRING', ['hello', 'world'])
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one('test', 'STRING', ['gotcha'])
        other = self._make_one('test', 'STRING', ['gotcha'])
        self.assertEqual(field, other)

    def test___ne___wrong_type(self):
        field = self._make_one('toast', 'INT64', [13])
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one('test', 'INT64', [12])
        field2 = self._make_one('test', 'INT64', [12])
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = (field1 != field2)
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one('test', 'INT64', [11])
        field2 = self._make_one('test', 'INT64', [12])
        self.assertNotEqual(field1, field2)

    def test___repr__(self):
        field1 = self._make_one('field1', 'STRING', ['value'])
        expected = "ArrayQueryParameter('field1', 'STRING', ['value'])"
        self.assertEqual(repr(field1), expected)


class Test_StructQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import StructQueryParameter

        return StructQueryParameter

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        sub_1 = _make_subparam('bar', 'INT64', 123)
        sub_2 = _make_subparam('baz', 'STRING', 'abc')
        param = self._make_one('foo', sub_1, sub_2)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.struct_types, {'bar': 'INT64', 'baz': 'STRING'})
        self.assertEqual(param.struct_values, {'bar': 123, 'baz': 'abc'})

    def test___eq__(self):
        sub_1 = _make_subparam('bar', 'INT64', 123)
        sub_2 = _make_subparam('baz', 'STRING', 'abc')
        sub_3 = _make_subparam('baz', 'STRING', 'def')
        sub_1_float = _make_subparam('bar', 'FLOAT64', 123.0)
        param = self._make_one('foo', sub_1, sub_2)
        self.assertEqual(param, param)
        self.assertNotEqual(param, object())
        alias = self._make_one('bar', sub_1, sub_2)
        self.assertNotEqual(param, alias)
        wrong_type = self._make_one('foo', sub_1_float, sub_2)
        self.assertNotEqual(param, wrong_type)
        wrong_val = self._make_one('foo', sub_2, sub_3)
        self.assertNotEqual(param, wrong_val)

    def test_positional(self):
        sub_1 = _make_subparam('bar', 'INT64', 123)
        sub_2 = _make_subparam('baz', 'STRING', 'abc')
        klass = self._get_target_class()
        param = klass.positional(sub_1, sub_2)
        self.assertEqual(param.name, None)
        self.assertEqual(param.struct_types, {'bar': 'INT64', 'baz': 'STRING'})
        self.assertEqual(param.struct_values, {'bar': 123, 'baz': 'abc'})

    def test_from_api_repr_w_name(self):
        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'INT64'}},
                    {'name': 'baz', 'type': {'type': 'STRING'}},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 123},
                    'baz': {'value': 'abc'},
                },
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.struct_types, {'bar': 'INT64', 'baz': 'STRING'})
        self.assertEqual(param.struct_values, {'bar': 123, 'baz': 'abc'})

    def test_from_api_repr_wo_name(self):
        RESOURCE = {
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'INT64'}},
                    {'name': 'baz', 'type': {'type': 'STRING'}},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 123},
                    'baz': {'value': 'abc'},
                },
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(param.name, None)
        self.assertEqual(param.struct_types, {'bar': 'INT64', 'baz': 'STRING'})
        self.assertEqual(param.struct_values, {'bar': 123, 'baz': 'abc'})

    def test_from_api_repr_w_nested_array(self):
        from google.cloud.bigquery._helpers import ArrayQueryParameter

        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'STRING'}},
                    {'name': 'baz', 'type': {
                        'type': 'ARRAY',
                        'arrayType': {'type': 'INT64'},
                    }},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 'abc'},
                    'baz': {'arrayValues': [
                        {'value': '123'},
                        {'value': '456'},
                    ]},
                },
            },
        }
        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)
        self.assertEqual(
            param,
            self._make_one(
                'foo',
                _make_subparam('bar', 'STRING', 'abc'),
                ArrayQueryParameter('baz', 'INT64', [123, 456])))

    def test_from_api_repr_w_nested_struct(self):
        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'STRING'}},
                    {'name': 'baz', 'type': {
                        'type': 'STRUCT',
                        'structTypes': [
                            {'name': 'qux', 'type': {'type': 'INT64'}},
                            {'name': 'spam', 'type': {'type': 'BOOL'}},
                        ],
                    }},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 'abc'},
                    'baz': {'structValues': {
                        'qux': {'value': '123'},
                        'spam': {'value': 'true'},
                    }},
                },
            },
        }

        klass = self._get_target_class()
        param = klass.from_api_repr(RESOURCE)

        expected = self._make_one(
            'foo',
            _make_subparam('bar', 'STRING', 'abc'),
            self._make_one(
                'baz',
                _make_subparam('qux', 'INT64', 123),
                _make_subparam('spam', 'BOOL', True)))
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.struct_types, expected.struct_types)
        self.assertEqual(param.struct_values, expected.struct_values)

    def test_to_api_repr_w_name(self):
        EXPECTED = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'INT64'}},
                    {'name': 'baz', 'type': {'type': 'STRING'}},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': '123'},
                    'baz': {'value': 'abc'},
                },
            },
        }
        sub_1 = _make_subparam('bar', 'INT64', 123)
        sub_2 = _make_subparam('baz', 'STRING', 'abc')
        param = self._make_one('foo', sub_1, sub_2)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_wo_name(self):
        EXPECTED = {
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'INT64'}},
                    {'name': 'baz', 'type': {'type': 'STRING'}},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': '123'},
                    'baz': {'value': 'abc'},
                },
            },
        }
        sub_1 = _make_subparam('bar', 'INT64', 123)
        sub_2 = _make_subparam('baz', 'STRING', 'abc')
        klass = self._get_target_class()
        param = klass.positional(sub_1, sub_2)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_nested_array(self):
        from google.cloud.bigquery._helpers import ArrayQueryParameter

        EXPECTED = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'STRING'}},
                    {'name': 'baz', 'type': {
                        'type': 'ARRAY',
                        'arrayType': {'type': 'INT64'},
                    }},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 'abc'},
                    'baz': {'arrayValues': [
                        {'value': '123'},
                        {'value': '456'},
                    ]},
                },
            },
        }
        scalar = _make_subparam('bar', 'STRING', 'abc')
        array = ArrayQueryParameter('baz', 'INT64', [123, 456])
        param = self._make_one('foo', scalar, array)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_nested_struct(self):
        EXPECTED = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'bar', 'type': {'type': 'STRING'}},
                    {'name': 'baz', 'type': {
                        'type': 'STRUCT',
                        'structTypes': [
                            {'name': 'qux', 'type': {'type': 'INT64'}},
                            {'name': 'spam', 'type': {'type': 'BOOL'}},
                        ],
                    }},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'bar': {'value': 'abc'},
                    'baz': {'structValues': {
                        'qux': {'value': '123'},
                        'spam': {'value': 'true'},
                    }},
                },
            },
        }
        scalar_1 = _make_subparam('bar', 'STRING', 'abc')
        scalar_2 = _make_subparam('qux', 'INT64', 123)
        scalar_3 = _make_subparam('spam', 'BOOL', True)
        sub = self._make_one('baz', scalar_2, scalar_3)
        param = self._make_one('foo', scalar_1, sub)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test___eq___wrong_type(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'abc'))
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'abc'))
        other = self._make_one(
            'other ', _make_subparam('bar', 'STRING', 'abc'))
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', None))
        other = self._make_one(
            'test', _make_subparam('bar', 'INT64', None))
        self.assertNotEqual(field, other)

    def test___eq___value_mismatch(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'hello'))
        other = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'world'))
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'gotcha'))
        other = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'gotcha'))
        self.assertEqual(field, other)

    def test___ne___wrong_type(self):
        field = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'hello'))
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'hello'))
        field2 = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'hello'))
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = (field1 != field2)
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'hello'))
        field2 = self._make_one(
            'test', _make_subparam('bar', 'STRING', 'world'))
        self.assertNotEqual(field1, field2)

    def test___repr__(self):
        field1 = self._make_one(
            'test', _make_subparam('field1', 'STRING', 'hello'))
        got = repr(field1)
        self.assertIn('StructQueryParameter', got)
        self.assertIn("'field1', 'STRING'", got)
        self.assertIn("'field1': 'hello'", got)


class Test__query_param_from_api_repr(unittest.TestCase):

    @staticmethod
    def _call_fut(resource):
        from google.cloud.bigquery._helpers import _query_param_from_api_repr

        return _query_param_from_api_repr(resource)

    def test_w_scalar(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        RESOURCE = {
            'name': 'foo',
            'parameterType': {'type': 'INT64'},
            'parameterValue': {'value': '123'},
        }

        parameter = self._call_fut(RESOURCE)

        self.assertIsInstance(parameter, ScalarQueryParameter)
        self.assertEqual(parameter.name, 'foo')
        self.assertEqual(parameter.type_, 'INT64')
        self.assertEqual(parameter.value, 123)

    def test_w_scalar_timestamp(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter
        from google.cloud._helpers import UTC

        RESOURCE = {
            'name': 'zoned',
            'parameterType': {'type': 'TIMESTAMP'},
            'parameterValue': {'value': '2012-03-04 05:06:07+00:00'},
        }

        parameter = self._call_fut(RESOURCE)

        self.assertIsInstance(parameter, ScalarQueryParameter)
        self.assertEqual(parameter.name, 'zoned')
        self.assertEqual(parameter.type_, 'TIMESTAMP')
        self.assertEqual(
            parameter.value,
            datetime.datetime(2012, 3, 4, 5, 6, 7, tzinfo=UTC))

    def test_w_scalar_timestamp_micros(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter
        from google.cloud._helpers import UTC

        RESOURCE = {
            'name': 'zoned',
            'parameterType': {'type': 'TIMESTAMP'},
            'parameterValue': {'value': '2012-03-04 05:06:07.250000+00:00'},
        }

        parameter = self._call_fut(RESOURCE)

        self.assertIsInstance(parameter, ScalarQueryParameter)
        self.assertEqual(parameter.name, 'zoned')
        self.assertEqual(parameter.type_, 'TIMESTAMP')
        self.assertEqual(
            parameter.value,
            datetime.datetime(2012, 3, 4, 5, 6, 7, 250000, tzinfo=UTC))

    def test_w_array(self):
        from google.cloud.bigquery._helpers import ArrayQueryParameter

        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': {'type': 'INT64'},
            },
            'parameterValue': {
                'arrayValues': [
                    {'value': '123'},
                ]},
        }

        parameter = self._call_fut(RESOURCE)

        self.assertIsInstance(parameter, ArrayQueryParameter)
        self.assertEqual(parameter.name, 'foo')
        self.assertEqual(parameter.array_type, 'INT64')
        self.assertEqual(parameter.values, [123])

    def test_w_struct(self):
        from google.cloud.bigquery._helpers import StructQueryParameter

        RESOURCE = {
            'name': 'foo',
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [
                    {'name': 'foo', 'type': {'type': 'STRING'}},
                    {'name': 'bar', 'type': {'type': 'INT64'}},
                ],
            },
            'parameterValue': {
                'structValues': {
                    'foo': {'value': 'Foo'},
                    'bar': {'value': '123'},
                }
            },
        }

        parameter = self._call_fut(RESOURCE)

        self.assertIsInstance(parameter, StructQueryParameter)
        self.assertEqual(parameter.name, 'foo')
        self.assertEqual(
            parameter.struct_types, {'foo': 'STRING', 'bar': 'INT64'})
        self.assertEqual(parameter.struct_values, {'foo': 'Foo', 'bar': 123})


class Test_UDFResource(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import UDFResource

        return UDFResource

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        udf = self._make_one('resourceUri', 'gs://some_bucket/some_file')
        self.assertEqual(udf.udf_type, 'resourceUri')
        self.assertEqual(udf.value, 'gs://some_bucket/some_file')

    def test___eq__(self):
        udf = self._make_one('resourceUri', 'gs://some_bucket/some_file')
        self.assertEqual(udf, udf)
        self.assertNotEqual(udf, object())
        wrong_val = self._make_one(
            'resourceUri', 'gs://some_bucket/other_file')
        self.assertNotEqual(udf, wrong_val)
        wrong_type = self._make_one('inlineCode', udf.value)
        self.assertNotEqual(udf, wrong_type)


class Test_ListApiResourceProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import _ListApiResourceProperty

        return _ListApiResourceProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _descriptor_and_klass(self):
        from google.cloud.bigquery._helpers import AbstractQueryParameter

        descriptor = self._make_one(
            'query_parameters', 'queryParameters', AbstractQueryParameter)

        class _Test(object):
            def __init__(self):
                self._properties = {}

            query_parameters = descriptor

        return descriptor, _Test

    def test_class_getter(self):
        descriptor, klass = self._descriptor_and_klass()
        self.assertIs(klass.query_parameters, descriptor)

    def test_instance_getter_empty(self):
        _, klass = self._descriptor_and_klass()
        instance = klass()
        self.assertEqual(instance.query_parameters, [])

    def test_instance_getter_w_non_empty_list(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._properties['queryParameters'] = query_parameters

        self.assertEqual(instance.query_parameters, query_parameters)

    def test_instance_setter_w_empty_list(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._query_parameters = query_parameters

        instance.query_parameters = []

        self.assertEqual(instance.query_parameters, [])

    def test_instance_setter_w_none(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._query_parameters = query_parameters

        with self.assertRaises(ValueError):
            instance.query_parameters = None

    def test_instance_setter_w_valid_udf(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        _, klass = self._descriptor_and_klass()
        instance = klass()

        instance.query_parameters = query_parameters

        self.assertEqual(instance.query_parameters, query_parameters)

    def test_instance_setter_w_bad_udfs(self):
        _, klass = self._descriptor_and_klass()
        instance = klass()

        with self.assertRaises(ValueError):
            instance.query_parameters = ["foo"]

        self.assertEqual(instance.query_parameters, [])


class _Field(object):

    def __init__(self, mode, name='unknown', field_type='UNKNOWN', fields=()):
        self.mode = mode
        self.name = name
        self.field_type = field_type
        self.fields = fields
