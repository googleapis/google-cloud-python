# Copyright 2015 Google Inc. All rights reserved.
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


class TestSchemaField(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.schema import SchemaField
        return SchemaField

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        field = self._makeOne('test', 'STRING')
        self.assertEqual(field.name, 'test')
        self.assertEqual(field.field_type, 'STRING')
        self.assertEqual(field.mode, 'NULLABLE')
        self.assertEqual(field.description, None)
        self.assertEqual(field.fields, None)

    def test_ctor_explicit(self):
        field = self._makeOne('test', 'STRING', mode='REQUIRED',
                              description='Testing')
        self.assertEqual(field.name, 'test')
        self.assertEqual(field.field_type, 'STRING')
        self.assertEqual(field.mode, 'REQUIRED')
        self.assertEqual(field.description, 'Testing')
        self.assertEqual(field.fields, None)

    def test_ctor_subfields(self):
        field = self._makeOne('phone_number', 'RECORD',
                              fields=[self._makeOne('area_code', 'STRING'),
                                      self._makeOne('local_number', 'STRING')])
        self.assertEqual(field.name, 'phone_number')
        self.assertEqual(field.field_type, 'RECORD')
        self.assertEqual(field.mode, 'NULLABLE')
        self.assertEqual(field.description, None)
        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0].name, 'area_code')
        self.assertEqual(field.fields[0].field_type, 'STRING')
        self.assertEqual(field.fields[0].mode, 'NULLABLE')
        self.assertEqual(field.fields[0].description, None)
        self.assertEqual(field.fields[0].fields, None)
        self.assertEqual(field.fields[1].name, 'local_number')
        self.assertEqual(field.fields[1].field_type, 'STRING')
        self.assertEqual(field.fields[1].mode, 'NULLABLE')
        self.assertEqual(field.fields[1].description, None)
        self.assertEqual(field.fields[1].fields, None)

    def test___eq___name_mismatch(self):
        field = self._makeOne('test', 'STRING')
        other = self._makeOne('other', 'STRING')
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._makeOne('test', 'STRING')
        other = self._makeOne('test', 'INTEGER')
        self.assertNotEqual(field, other)

    def test___eq___mode_mismatch(self):
        field = self._makeOne('test', 'STRING', mode='REQUIRED')
        other = self._makeOne('test', 'STRING', mode='NULLABLE')
        self.assertNotEqual(field, other)

    def test___eq___description_mismatch(self):
        field = self._makeOne('test', 'STRING', description='Testing')
        other = self._makeOne('test', 'STRING', description='Other')
        self.assertNotEqual(field, other)

    def test___eq___fields_mismatch(self):
        sub1 = self._makeOne('sub1', 'STRING')
        sub2 = self._makeOne('sub2', 'STRING')
        field = self._makeOne('test', 'RECORD', fields=[sub1])
        other = self._makeOne('test', 'RECORD', fields=[sub2])
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._makeOne('test', 'STRING', mode='REQUIRED',
                              description='Testing')
        other = self._makeOne('test', 'STRING', mode='REQUIRED',
                              description='Testing')
        self.assertEqual(field, other)

    def test___eq___hit_case_diff_on_type(self):
        field = self._makeOne('test', 'STRING', mode='REQUIRED',
                              description='Testing')
        other = self._makeOne('test', 'string', mode='REQUIRED',
                              description='Testing')
        self.assertEqual(field, other)

    def test___eq___hit_w_fields(self):
        sub1 = self._makeOne('sub1', 'STRING')
        sub2 = self._makeOne('sub2', 'STRING')
        field = self._makeOne('test', 'RECORD', fields=[sub1, sub2])
        other = self._makeOne('test', 'RECORD', fields=[sub1, sub2])
        self.assertEqual(field, other)
