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

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _not_null
        return _not_null(value, field)

    def test_w_none_nullable(self):
        self.assertFalse(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        self.assertTrue(self._callFUT(None, _Field('REQUIRED')))

    def test_w_value(self):
        self.assertTrue(self._callFUT(object(), object()))


class Test_int_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _int_from_json
        return _int_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._callFUT('42', object())
        self.assertEqual(coerced, 42)

    def test_w_float_value(self):
        coerced = self._callFUT(42, object())
        self.assertEqual(coerced, 42)


class Test_float_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _float_from_json
        return _float_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        coerced = self._callFUT('3.1415', object())
        self.assertEqual(coerced, 3.1415)

    def test_w_float_value(self):
        coerced = self._callFUT(3.1415, object())
        self.assertEqual(coerced, 3.1415)


class Test_bool_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _bool_from_json
        return _bool_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(AttributeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_value_t(self):
        coerced = self._callFUT('T', object())
        self.assertTrue(coerced)

    def test_w_value_true(self):
        coerced = self._callFUT('True', object())
        self.assertTrue(coerced)

    def test_w_value_1(self):
        coerced = self._callFUT('1', object())
        self.assertTrue(coerced)

    def test_w_value_other(self):
        coerced = self._callFUT('f', object())
        self.assertFalse(coerced)


class Test_datetime_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _datetime_from_json
        return _datetime_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        import datetime
        from google.cloud._helpers import _EPOCH
        coerced = self._callFUT('1.234567', object())
        self.assertEqual(
            coerced,
            _EPOCH + datetime.timedelta(seconds=1, microseconds=234567))

    def test_w_float_value(self):
        import datetime
        from google.cloud._helpers import _EPOCH
        coerced = self._callFUT(1.234567, object())
        self.assertEqual(
            coerced,
            _EPOCH + datetime.timedelta(seconds=1, microseconds=234567))


class Test_date_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _date_from_json
        return _date_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_string_value(self):
        import datetime
        coerced = self._callFUT('1987-09-22', object())
        self.assertEqual(
            coerced,
            datetime.date(1987, 9, 22))


class Test_record_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _record_from_json
        return _record_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        with self.assertRaises(TypeError):
            self._callFUT(None, _Field('REQUIRED'))

    def test_w_nullable_subfield_none(self):
        subfield = _Field('NULLABLE', 'age', 'INTEGER')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': None}]}
        coerced = self._callFUT(value, field)
        self.assertEqual(coerced, {'age': None})

    def test_w_scalar_subfield(self):
        subfield = _Field('REQUIRED', 'age', 'INTEGER')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': 42}]}
        coerced = self._callFUT(value, field)
        self.assertEqual(coerced, {'age': 42})

    def test_w_repeated_subfield(self):
        subfield = _Field('REPEATED', 'color', 'STRING')
        field = _Field('REQUIRED', fields=[subfield])
        value = {'f': [{'v': ['red', 'yellow', 'blue']}]}
        coerced = self._callFUT(value, field)
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
        coerced = self._callFUT(value, person)
        self.assertEqual(coerced, expected)


class Test_string_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
        from google.cloud.bigquery._helpers import _string_from_json
        return _string_from_json(value, field)

    def test_w_none_nullable(self):
        self.assertIsNone(self._callFUT(None, _Field('NULLABLE')))

    def test_w_none_required(self):
        self.assertIsNone(self._callFUT(None, _Field('RECORD')))

    def test_w_string_value(self):
        coerced = self._callFUT('Wonderful!', object())
        self.assertEqual(coerced, 'Wonderful!')


class Test_rows_from_json(unittest.TestCase):

    def _callFUT(self, value, field):
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
                {'v': ['orange', 'black']},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': {'f': [{'v': '877'}, {'v': '768-5309'}, {'v': 2}]}},
                {'v': ['brown']},
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
        coerced = self._callFUT(rows, schema)
        self.assertEqual(coerced, expected)

    def test_w_int64_float64(self):
        # "Standard" SQL dialect uses 'INT64', 'FLOAT64'.
        candidate = _Field('REQUIRED', 'candidate', 'STRING')
        votes = _Field('REQUIRED', 'votes', 'INT64')
        percentage = _Field('REQUIRED', 'percentage', 'FLOAT64')
        schema = [candidate, votes, percentage]
        rows = [
            {'f': [
                {'v': 'Phred Phlyntstone'},
                {'v': 8},
                {'v': 0.25},
            ]},
            {'f': [
                {'v': 'Bharney Rhubble'},
                {'v': 4},
                {'v': 0.125},
            ]},
            {'f': [
                {'v': 'Wylma Phlyntstone'},
                {'v': 20},
                {'v': 0.625},
            ]},
        ]
        expected = [
            ('Phred Phlyntstone', 8, 0.25),
            ('Bharney Rhubble', 4, 0.125),
            ('Wylma Phlyntstone', 20, 0.625),
        ]
        coerced = self._callFUT(rows, schema)
        self.assertEqual(coerced, expected)


class Test_ConfigurationProperty(unittest.TestCase):

    def _getTargetClass(self):
        from google.cloud.bigquery._helpers import _ConfigurationProperty
        return _ConfigurationProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._makeOne('attr')

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

    def _getTargetClass(self):
        from google.cloud.bigquery._helpers import _TypedProperty
        return _TypedProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_it(self):

        class Configuration(object):
            _attr = None

        class Wrapper(object):
            attr = self._makeOne('attr', int)

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

    def _getTargetClass(self):
        from google.cloud.bigquery._helpers import _EnumProperty
        return _EnumProperty

    def test_it(self):

        class Sub(self._getTargetClass()):
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

    def _getTargetClass(self):
        from google.cloud.bigquery._helpers import UDFResourcesProperty
        return UDFResourcesProperty

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _descriptor_and_klass(self):
        descriptor = self._makeOne()

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


class _Field(object):

    def __init__(self, mode, name='unknown', field_type='UNKNOWN', fields=()):
        self.mode = mode
        self.name = name
        self.field_type = field_type
        self.fields = fields
