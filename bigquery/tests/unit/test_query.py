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

import datetime
import unittest

import mock


class Test_UDFResource(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import UDFResource

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


class Test__AbstractQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import _AbstractQueryParameter

        return _AbstractQueryParameter

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
        from google.cloud.bigquery.query import ScalarQueryParameter

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

    def test_to_api_repr_w_numeric(self):
        EXPECTED = {
            'parameterType': {
                'type': 'NUMERIC',
            },
            'parameterValue': {
                'value': '123456789.123456789',
            },
        }
        klass = self._get_target_class()
        param = klass.positional(type_='NUMERIC',
                                 value='123456789.123456789')
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
    from google.cloud.bigquery.query import ScalarQueryParameter

    return ScalarQueryParameter(name, type_, value)


class Test_ArrayQueryParameter(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import ArrayQueryParameter

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
        from google.cloud.bigquery.query import StructQueryParameter

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
        from google.cloud.bigquery.query import StructQueryParameter

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
        from google.cloud.bigquery.query import StructQueryParameter

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
        from google.cloud.bigquery.query import ArrayQueryParameter

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
        from google.cloud.bigquery.query import ArrayQueryParameter

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


class Test_QueryResults(unittest.TestCase):
    PROJECT = 'project'
    JOB_ID = 'test-synchronous-query'
    TOKEN = 'TOKEN'

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.query import _QueryResults

        return _QueryResults

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_resource(self):
        return {
            'jobReference': {
                'projectId': self.PROJECT,
                'jobId': self.JOB_ID,
            },
        }

    def _verifySchema(self, query, resource):
        from google.cloud.bigquery.schema import SchemaField

        if 'schema' in resource:
            fields = resource['schema']['fields']
            self.assertEqual(len(query.schema), len(fields))
            for found, expected in zip(query.schema, fields):
                self.assertIsInstance(found, SchemaField)
                self.assertEqual(found.name, expected['name'])
                self.assertEqual(found.field_type, expected['type'])
                self.assertEqual(found.mode, expected['mode'])
                self.assertEqual(found.description,
                                 expected.get('description'))
                self.assertEqual(found.fields, expected.get('fields', ()))
        else:
            self.assertEqual(query.schema, ())

    def test_ctor_defaults(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.cache_hit)
        self.assertIsNone(query.complete)
        self.assertIsNone(query.errors)
        self.assertIsNone(query.page_token)
        self.assertEqual(query.project, self.PROJECT)
        self.assertEqual(query.rows, [])
        self.assertEqual(query.schema, ())
        self.assertIsNone(query.total_rows)
        self.assertIsNone(query.total_bytes_processed)

    def test_cache_hit_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.cache_hit)

    def test_cache_hit_present(self):
        resource = self._make_resource()
        resource['cacheHit'] = True
        query = self._make_one(resource)
        self.assertTrue(query.cache_hit)

    def test_complete_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.complete)

    def test_complete_present(self):
        resource = self._make_resource()
        resource['jobComplete'] = True
        query = self._make_one(resource)
        self.assertTrue(query.complete)

    def test_errors_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.errors)

    def test_errors_present(self):
        ERRORS = [
            {'reason': 'testing'},
        ]
        resource = self._make_resource()
        resource['errors'] = ERRORS
        query = self._make_one(resource)
        self.assertEqual(query.errors, ERRORS)

    def test_job_id_missing(self):
        with self.assertRaises(ValueError):
            self._make_one({})

    def test_job_id_broken_job_reference(self):
        resource = {'jobReference': {'bogus': 'BOGUS'}}
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_job_id_present(self):
        resource = self._make_resource()
        resource['jobReference']['jobId'] = 'custom-job'
        query = self._make_one(resource)
        self.assertEqual(query.job_id, 'custom-job')

    def test_page_token_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.page_token)

    def test_page_token_present(self):
        resource = self._make_resource()
        resource['pageToken'] = 'TOKEN'
        query = self._make_one(resource)
        self.assertEqual(query.page_token, 'TOKEN')

    def test_total_rows_present_integer(self):
        resource = self._make_resource()
        resource['totalRows'] = 42
        query = self._make_one(resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_rows_present_string(self):
        resource = self._make_resource()
        resource['totalRows'] = '42'
        query = self._make_one(resource)
        self.assertEqual(query.total_rows, 42)

    def test_total_bytes_processed_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.total_bytes_processed)

    def test_total_bytes_processed_present_integer(self):
        resource = self._make_resource()
        resource['totalBytesProcessed'] = 123456
        query = self._make_one(resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_total_bytes_processed_present_string(self):
        resource = self._make_resource()
        resource['totalBytesProcessed'] = '123456'
        query = self._make_one(resource)
        self.assertEqual(query.total_bytes_processed, 123456)

    def test_num_dml_affected_rows_missing(self):
        query = self._make_one(self._make_resource())
        self.assertIsNone(query.num_dml_affected_rows)

    def test_num_dml_affected_rows_present_integer(self):
        resource = self._make_resource()
        resource['numDmlAffectedRows'] = 123456
        query = self._make_one(resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_num_dml_affected_rows_present_string(self):
        resource = self._make_resource()
        resource['numDmlAffectedRows'] = '123456'
        query = self._make_one(resource)
        self.assertEqual(query.num_dml_affected_rows, 123456)

    def test_schema(self):
        query = self._make_one(self._make_resource())
        self._verifySchema(query, self._make_resource())
        resource = self._make_resource()
        resource['schema'] = {
            'fields': [
                {'name': 'full_name', 'type': 'STRING', 'mode': 'REQURED'},
                {'name': 'age', 'type': 'INTEGER', 'mode': 'REQURED'},
            ],
        }
        query._set_properties(resource)
        self._verifySchema(query, resource)


class Test__query_param_from_api_repr(unittest.TestCase):

    @staticmethod
    def _call_fut(resource):
        from google.cloud.bigquery.query import _query_param_from_api_repr

        return _query_param_from_api_repr(resource)

    def test_w_scalar(self):
        from google.cloud.bigquery.query import ScalarQueryParameter

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
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.query import ScalarQueryParameter

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
        from google.cloud._helpers import UTC
        from google.cloud.bigquery.query import ScalarQueryParameter

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
        from google.cloud.bigquery.query import ArrayQueryParameter

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
        from google.cloud.bigquery.query import StructQueryParameter

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
