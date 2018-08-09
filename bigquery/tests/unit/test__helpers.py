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

import base64
import datetime
import decimal
import unittest


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


class Test_decimal_from_json(unittest.TestCase):

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _decimal_from_json

        return _decimal_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._call_fut(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._call_fut(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._call_fut('3.1415', object())
        self.assertEqual(coerced, decimal.Decimal('3.1415'))

    def test_w_float_value(self):
        coerced = self._call_fut(3.1415, object())
        # There is no exact float representation of 3.1415.
        self.assertEqual(coerced, decimal.Decimal(3.1415))


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

    def test_w_subsecond_string_value(self):
        coerced = self._call_fut('12:12:27.123456', object())
        self.assertEqual(
            coerced,
            datetime.time(12, 12, 27, 123456))

    def test_w_bogus_string_value(self):
        with self.assertRaises(ValueError):
            self._call_fut('12:12:27.123', object())


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


class Test_field_to_index_mapping(unittest.TestCase):

    def _call_fut(self, schema):
        from google.cloud.bigquery._helpers import _field_to_index_mapping

        return _field_to_index_mapping(schema)

    def test_w_empty_schema(self):
        self.assertEqual(self._call_fut([]), {})

    def test_w_non_empty_schema(self):
        schema = [
            _Field('REPEATED', 'first', 'INTEGER'),
            _Field('REQUIRED', 'second', 'INTEGER'),
            _Field('REPEATED', 'third', 'INTEGER'),
        ]
        self.assertEqual(
            self._call_fut(schema),
            {'first': 0, 'second': 1, 'third': 2})


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


class Test_rows_from_json(unittest.TestCase):

    def _call_fut(self, rows, schema):
        from google.cloud.bigquery._helpers import _rows_from_json

        return _rows_from_json(rows, schema)

    def test_w_record_subfield(self):
        from google.cloud.bigquery.table import Row

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
        from google.cloud.bigquery.table import Row

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


class Test_decimal_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _decimal_to_json

        return _decimal_to_json(value)

    def test_w_float(self):
        self.assertEqual(self._call_fut(1.23), 1.23)

    def test_w_string(self):
        self.assertEqual(self._call_fut('1.23'), '1.23')

    def test_w_decimal(self):
        self.assertEqual(self._call_fut(decimal.Decimal('1.23')), '1.23')


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


class Test_snake_to_camel_case(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _snake_to_camel_case

        return _snake_to_camel_case(value)

    def test_w_snake_case_string(self):
        self.assertEqual(self._call_fut('friendly_name'), 'friendlyName')

    def test_w_camel_case_string(self):
        self.assertEqual(self._call_fut('friendlyName'), 'friendlyName')


class Test__get_sub_prop(unittest.TestCase):

    def _call_fut(self, container, keys, **kw):
        from google.cloud.bigquery._helpers import _get_sub_prop

        return _get_sub_prop(container, keys, **kw)

    def test_w_empty_container_default_default(self):
        self.assertIsNone(self._call_fut({}, ['key1']))

    def test_w_missing_key_explicit_default(self):
        self.assertEqual(self._call_fut({'key2': 2}, ['key1'], default=1), 1)

    def test_w_matching_single_key(self):
        self.assertEqual(self._call_fut({'key1': 1}, ['key1']), 1)

    def test_w_matching_first_key_missing_second_key(self):
        self.assertIsNone(
            self._call_fut({'key1': {'key3': 3}}, ['key1', 'key2']))

    def test_w_matching_first_key_matching_second_key(self):
        self.assertEqual(
            self._call_fut({'key1': {'key2': 2}}, ['key1', 'key2']), 2)


class Test__set_sub_prop(unittest.TestCase):

    def _call_fut(self, container, keys, value):
        from google.cloud.bigquery._helpers import _set_sub_prop

        return _set_sub_prop(container, keys, value)

    def test_w_empty_container_single_key(self):
        container = {}
        self._call_fut(container, ['key1'], 'value')
        self.assertEqual(container, {'key1': 'value'})

    def test_w_empty_container_nested_keys(self):
        container = {}
        self._call_fut(container, ['key1', 'key2', 'key3'], 'value')
        self.assertEqual(container, {'key1': {'key2': {'key3': 'value'}}})

    def test_w_existing_value(self):
        container = {'key1': 'before'}
        self._call_fut(container, ['key1'], 'after')
        self.assertEqual(container, {'key1': 'after'})

    def test_w_nested_keys_existing_value(self):
        container = {'key1': {'key2': {'key3': 'before'}}}
        self._call_fut(container, ['key1', 'key2', 'key3'], 'after')
        self.assertEqual(container, {'key1': {'key2': {'key3': 'after'}}})


class Test__del_sub_prop(unittest.TestCase):

    def _call_fut(self, container, keys):
        from google.cloud.bigquery._helpers import _del_sub_prop

        return _del_sub_prop(container, keys)

    def test_w_single_key(self):
        container = {'key1': 'value'}
        self._call_fut(container, ['key1'])
        self.assertEqual(container, {})

    def test_w_empty_container_nested_keys(self):
        container = {}
        self._call_fut(container, ['key1', 'key2', 'key3'])
        self.assertEqual(container, {'key1': {'key2': {}}})

    def test_w_existing_value_nested_keys(self):
        container = {'key1': {'key2': {'key3': 'value'}}}
        self._call_fut(container, ['key1', 'key2', 'key3'])
        self.assertEqual(container, {'key1': {'key2': {}}})


class Test__int_or_none(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _int_or_none

        return _int_or_none(value)

    def test_w_num_string(self):
        self.assertEqual(self._call_fut('123'), 123)

    def test_w_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_w_int(self):
        self.assertEqual(self._call_fut(123), 123)

    def test_w_non_num_string(self):
        with self.assertRaises(ValueError):
            self._call_fut('ham')


class Test__str_or_none(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _str_or_none

        return _str_or_none(value)

    def test_w_int(self):
        self.assertEqual(self._call_fut(123), '123')

    def test_w_none(self):
        self.assertIsNone(self._call_fut(None))

    def test_w_str(self):
        self.assertEqual(self._call_fut('ham'), 'ham')


class _Field(object):

    def __init__(self, mode, name='unknown', field_type='UNKNOWN', fields=()):
        self.mode = mode
        self.name = name
        self.field_type = field_type
        self.fields = fields
