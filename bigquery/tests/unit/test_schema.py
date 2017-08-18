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

import mock


class TestSchemaField(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import SchemaField

        return SchemaField

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        field = self._make_one('test', 'STRING')
        self.assertEqual(field._name, 'test')
        self.assertEqual(field._field_type, 'STRING')
        self.assertEqual(field._mode, 'NULLABLE')
        self.assertIsNone(field._description)
        self.assertEqual(field._fields, ())

    def test_constructor_explicit(self):
        field = self._make_one('test', 'STRING', mode='REQUIRED',
                               description='Testing')
        self.assertEqual(field._name, 'test')
        self.assertEqual(field._field_type, 'STRING')
        self.assertEqual(field._mode, 'REQUIRED')
        self.assertEqual(field._description, 'Testing')
        self.assertEqual(field._fields, ())

    def test_constructor_subfields(self):
        sub_field1 = self._make_one('area_code', 'STRING')
        sub_field2 = self._make_one('local_number', 'STRING')
        field = self._make_one(
            'phone_number',
            'RECORD',
            fields=[sub_field1, sub_field2],
        )
        self.assertEqual(field._name, 'phone_number')
        self.assertEqual(field._field_type, 'RECORD')
        self.assertEqual(field._mode, 'NULLABLE')
        self.assertIsNone(field._description)
        self.assertEqual(len(field._fields), 2)
        self.assertIs(field._fields[0], sub_field1)
        self.assertIs(field._fields[1], sub_field2)

    def test_to_api_repr(self):
        field = self._make_one('foo', 'INTEGER', 'NULLABLE')
        self.assertEqual(field.to_api_repr(), {
            'mode': 'nullable',
            'name': 'foo',
            'type': 'integer',
        })

    def test_to_api_repr_with_subfield(self):
        subfield = self._make_one('bar', 'INTEGER', 'NULLABLE')
        field = self._make_one('foo', 'RECORD', 'REQUIRED', fields=(subfield,))
        self.assertEqual(field.to_api_repr(), {
            'fields': [{
                'mode': 'nullable',
                'name': 'bar',
                'type': 'integer',
            }],
            'mode': 'required',
            'name': 'foo',
            'type': 'record',
        })

    def test_from_api_repr(self):
        field = self._get_target_class().from_api_repr({
            'fields': [{
                'mode': 'nullable',
                'name': 'bar',
                'type': 'integer',
            }],
            'mode': 'required',
            'name': 'foo',
            'type': 'record',
        })
        self.assertEqual(field.name, 'foo')
        self.assertEqual(field.field_type, 'RECORD')
        self.assertEqual(field.mode, 'REQUIRED')
        self.assertEqual(len(field.fields), 1)
        self.assertEqual(field.fields[0].name, 'bar')
        self.assertEqual(field.fields[0].field_type, 'INTEGER')
        self.assertEqual(field.fields[0].mode, 'NULLABLE')

    def test_name_property(self):
        name = 'lemon-ness'
        schema_field = self._make_one(name, 'INTEGER')
        self.assertIs(schema_field.name, name)

    def test_field_type_property(self):
        field_type = 'BOOLEAN'
        schema_field = self._make_one('whether', field_type)
        self.assertIs(schema_field.field_type, field_type)

    def test_mode_property(self):
        mode = 'REPEATED'
        schema_field = self._make_one('again', 'FLOAT', mode=mode)
        self.assertIs(schema_field.mode, mode)

    def test_is_nullable(self):
        mode = 'NULLABLE'
        schema_field = self._make_one('test', 'FLOAT', mode=mode)
        self.assertTrue(schema_field.is_nullable)

    def test_is_not_nullable(self):
        mode = 'REPEATED'
        schema_field = self._make_one('test', 'FLOAT', mode=mode)
        self.assertFalse(schema_field.is_nullable)

    def test_description_property(self):
        description = 'It holds some data.'
        schema_field = self._make_one(
            'do', 'TIMESTAMP', description=description)
        self.assertIs(schema_field.description, description)

    def test_fields_property(self):
        sub_field1 = self._make_one('one', 'STRING')
        sub_field2 = self._make_one('fish', 'INTEGER')
        fields = (sub_field1, sub_field2)
        schema_field = self._make_one('boat', 'RECORD', fields=fields)
        self.assertIs(schema_field.fields, fields)

    def test___eq___wrong_type(self):
        field = self._make_one('test', 'STRING')
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one('test', 'STRING')
        other = self._make_one('other', 'STRING')
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one('test', 'STRING')
        other = self._make_one('test', 'INTEGER')
        self.assertNotEqual(field, other)

    def test___eq___mode_mismatch(self):
        field = self._make_one('test', 'STRING', mode='REQUIRED')
        other = self._make_one('test', 'STRING', mode='NULLABLE')
        self.assertNotEqual(field, other)

    def test___eq___description_mismatch(self):
        field = self._make_one('test', 'STRING', description='Testing')
        other = self._make_one('test', 'STRING', description='Other')
        self.assertNotEqual(field, other)

    def test___eq___fields_mismatch(self):
        sub1 = self._make_one('sub1', 'STRING')
        sub2 = self._make_one('sub2', 'STRING')
        field = self._make_one('test', 'RECORD', fields=[sub1])
        other = self._make_one('test', 'RECORD', fields=[sub2])
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one('test', 'STRING', mode='REQUIRED',
                               description='Testing')
        other = self._make_one('test', 'STRING', mode='REQUIRED',
                               description='Testing')
        self.assertEqual(field, other)

    def test___eq___hit_case_diff_on_type(self):
        field = self._make_one('test', 'STRING', mode='REQUIRED',
                               description='Testing')
        other = self._make_one('test', 'string', mode='REQUIRED',
                               description='Testing')
        self.assertEqual(field, other)

    def test___eq___hit_w_fields(self):
        sub1 = self._make_one('sub1', 'STRING')
        sub2 = self._make_one('sub2', 'STRING')
        field = self._make_one('test', 'RECORD', fields=[sub1, sub2])
        other = self._make_one('test', 'RECORD', fields=[sub1, sub2])
        self.assertEqual(field, other)

    def test___ne___wrong_type(self):
        field = self._make_one('toast', 'INTEGER')
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one('test', 'TIMESTAMP', mode='REPEATED')
        field2 = self._make_one('test', 'TIMESTAMP', mode='REPEATED')
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = (field1 != field2)
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one(
            'test1', 'FLOAT', mode='REPEATED', description='Not same')
        field2 = self._make_one(
            'test2', 'FLOAT', mode='NULLABLE', description='Knot saym')
        self.assertNotEqual(field1, field2)

    def test___hash__set_equality(self):
        sub1 = self._make_one('sub1', 'STRING')
        sub2 = self._make_one('sub2', 'STRING')
        field1 = self._make_one('test', 'RECORD', fields=[sub1])
        field2 = self._make_one('test', 'RECORD', fields=[sub2])
        set_one = {field1, field2}
        set_two = {field1, field2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        sub1 = self._make_one('sub1', 'STRING')
        sub2 = self._make_one('sub2', 'STRING')
        field1 = self._make_one('test', 'RECORD', fields=[sub1])
        field2 = self._make_one('test', 'RECORD', fields=[sub2])
        set_one = {field1}
        set_two = {field2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        field1 = self._make_one('field1', 'STRING')
        expected = "SchemaField('field1', 'string', 'NULLABLE', None, ())"
        self.assertEqual(repr(field1), expected)
