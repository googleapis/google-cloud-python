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
        import base64

        expected = b'Wonderful!'
        encoded = base64.encodestring(expected)
        coerced = self._call_fut(encoded, object())
        self.assertEqual(coerced, expected)

    def test_w_base64_encoded_text(self):
        import base64

        expected = b'Wonderful!'
        encoded = base64.encodestring(expected).decode('ascii')
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
        import datetime
        from google.cloud._helpers import _EPOCH

        coerced = self._call_fut('1.234567', object())
        self.assertEqual(
            coerced,
            _EPOCH + datetime.timedelta(seconds=1, microseconds=234567))

    def test_w_float_value(self):
        import datetime
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
        import datetime

        coerced = self._call_fut('2016-12-02T18:51:33', object())
        self.assertEqual(
            coerced,
            datetime.datetime(2016, 12, 2, 18, 51, 33))


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
        import datetime

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
        import datetime

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


class Test_row_from_json(unittest.TestCase):

    def _call_fut(self, row, schema):
        from google.cloud.bigquery._helpers import _row_from_json

        return _row_from_json(row, schema)

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

    def _call_fut(self, value, field):
        from google.cloud.bigquery._helpers import _rows_from_json

        return _rows_from_json(value, field)

    def test_w_record_subfield(self):
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
        expected = [
            ('Phred Phlyntstone', phred_phone, ['orange', 'black']),
            ('Bharney Rhubble', bharney_phone, ['brown']),
            ('Wylma Phlyntstone', None, []),
        ]
        coerced = self._call_fut(rows, schema)
        self.assertEqual(coerced, expected)

    def test_w_int64_float64_bool(self):
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
        expected = [
            ('Phred Phlyntstone', 8, 0.25, True),
            ('Bharney Rhubble', 4, 0.125, False),
            ('Wylma Phlyntstone', 20, 0.625, False),
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
        import base64

        source = b'source'
        expected = base64.encodestring(source)
        self.assertEqual(self._call_fut(source), expected)


class Test_timestamp_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _timestamp_to_json

        return _timestamp_to_json(value)

    def test_w_float(self):
        self.assertEqual(self._call_fut(1.234567), 1.234567)

    def test_w_string(self):
        ZULU = '2016-12-20 15:58:27.339328+00:00'
        self.assertEqual(self._call_fut(ZULU), ZULU)

    def test_w_datetime_wo_zone(self):
        import datetime

        ZULU = '2016-12-20 15:58:27.339328+00:00'
        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328)
        self.assertEqual(self._call_fut(when), ZULU)

    def test_w_datetime_w_non_utc_zone(self):
        import datetime

        class _Zone(datetime.tzinfo):

            def utcoffset(self, _):
                return datetime.timedelta(minutes=-240)

        ZULU = '2016-12-20 19:58:27.339328+00:00'
        when = datetime.datetime(
            2016, 12, 20, 15, 58, 27, 339328, tzinfo=_Zone())
        self.assertEqual(self._call_fut(when), ZULU)

    def test_w_datetime_w_utc_zone(self):
        import datetime
        from google.cloud._helpers import UTC

        ZULU = '2016-12-20 15:58:27.339328+00:00'
        when = datetime.datetime(2016, 12, 20, 15, 58, 27, 339328, tzinfo=UTC)
        self.assertEqual(self._call_fut(when), ZULU)


class Test_datetime_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _datetime_to_json

        return _datetime_to_json(value)

    def test_w_string(self):
        RFC3339 = '2016-12-03T14:14:51Z'
        self.assertEqual(self._call_fut(RFC3339), RFC3339)

    def test_w_datetime(self):
        import datetime
        from google.cloud._helpers import UTC

        when = datetime.datetime(2016, 12, 3, 14, 11, 27, 123456, tzinfo=UTC)
        self.assertEqual(self._call_fut(when), '2016-12-03T14:11:27.123456Z')


class Test_date_to_json(unittest.TestCase):

    def _call_fut(self, value):
        from google.cloud.bigquery._helpers import _date_to_json

        return _date_to_json(value)

    def test_w_string(self):
        RFC3339 = '2016-12-03'
        self.assertEqual(self._call_fut(RFC3339), RFC3339)

    def test_w_datetime(self):
        import datetime

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
        import datetime

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
            ALLOWED = ('FOO', 'BAR', 'BAZ')

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = Sub('attr')

            def __init__(self):
                self._configuration = Configuration()

        wrapper = Wrapper()
        with self.assertRaises(ValueError):
            wrapper.attr = 'BOGUS'

        wrapper.attr = 'FOO'
        self.assertEqual(wrapper.attr, 'FOO')
        self.assertEqual(wrapper._configuration._attr, 'FOO')

        del wrapper.attr
        self.assertIsNone(wrapper.attr)
        self.assertIsNone(wrapper._configuration._attr)


class Test_UDFResourcesProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import UDFResourcesProperty

        return UDFResourcesProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _descriptor_and_klass(self):
        descriptor = self._make_one()

        class _Test(object):
            _udf_resources = ()
            udf_resources = descriptor

        return descriptor, _Test

    def test_class_getter(self):
        descriptor, klass = self._descriptor_and_klass()
        self.assertIs(klass.udf_resources, descriptor)

    def test_instance_getter_empty(self):
        _, klass = self._descriptor_and_klass()
        instance = klass()
        self.assertEqual(instance.udf_resources, [])

    def test_instance_getter_w_non_empty_list(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._udf_resources = tuple(udf_resources)

        self.assertEqual(instance.udf_resources, udf_resources)

    def test_instance_setter_w_empty_list(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._udf_resources = udf_resources

        instance.udf_resources = []

        self.assertEqual(instance.udf_resources, [])

    def test_instance_setter_w_valid_udf(self):
        from google.cloud.bigquery._helpers import UDFResource

        RESOURCE_URI = 'gs://some-bucket/js/lib.js'
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        _, klass = self._descriptor_and_klass()
        instance = klass()

        instance.udf_resources = udf_resources

        self.assertEqual(instance.udf_resources, udf_resources)

    def test_instance_setter_w_bad_udfs(self):
        _, klass = self._descriptor_and_klass()
        instance = klass()

        with self.assertRaises(ValueError):
            instance.udf_resources = ["foo"]

        self.assertEqual(instance.udf_resources, [])


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
        import datetime

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
        import datetime
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
        import datetime
        from google.cloud._helpers import _datetime_to_rfc3339

        now = datetime.datetime.utcnow()
        EXPECTED = {
            'parameterType': {
                'type': 'DATETIME',
            },
            'parameterValue': {
                'value': _datetime_to_rfc3339(now),
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='DATETIME', value=now)
        self.assertEqual(param.to_api_repr(), EXPECTED)

    def test_to_api_repr_w_datetime_string(self):
        import datetime
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
        import datetime

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
        import datetime

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


class Test_StructQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import StructQueryParameter

        return StructQueryParameter

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    @staticmethod
    def _make_subparam(name, type_, value):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        return ScalarQueryParameter(name, type_, value)

    def test_ctor(self):
        sub_1 = self._make_subparam('bar', 'INT64', 123)
        sub_2 = self._make_subparam('baz', 'STRING', 'abc')
        param = self._make_one('foo', sub_1, sub_2)
        self.assertEqual(param.name, 'foo')
        self.assertEqual(param.struct_types, {'bar': 'INT64', 'baz': 'STRING'})
        self.assertEqual(param.struct_values, {'bar': 123, 'baz': 'abc'})

    def test_positional(self):
        sub_1 = self._make_subparam('bar', 'INT64', 123)
        sub_2 = self._make_subparam('baz', 'STRING', 'abc')
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
        sub_1 = self._make_subparam('bar', 'INT64', 123)
        sub_2 = self._make_subparam('baz', 'STRING', 'abc')
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
        sub_1 = self._make_subparam('bar', 'INT64', 123)
        sub_2 = self._make_subparam('baz', 'STRING', 'abc')
        klass = self._get_target_class()
        param = klass.positional(sub_1, sub_2)
        self.assertEqual(param.to_api_repr(), EXPECTED)


class Test_QueryParametersProperty(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery._helpers import QueryParametersProperty

        return QueryParametersProperty

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _descriptor_and_klass(self):
        descriptor = self._make_one()

        class _Test(object):
            _query_parameters = ()
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
        instance._query_parameters = tuple(query_parameters)

        self.assertEqual(instance.query_parameters, query_parameters)

    def test_instance_setter_w_empty_list(self):
        from google.cloud.bigquery._helpers import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", 'INT64', 123)]
        _, klass = self._descriptor_and_klass()
        instance = klass()
        instance._query_parameters = query_parameters

        instance.query_parameters = []

        self.assertEqual(instance.query_parameters, [])

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
