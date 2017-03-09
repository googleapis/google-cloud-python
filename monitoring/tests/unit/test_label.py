# Copyright 2016 Google Inc.
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


class TestLabelValueType(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.label import LabelValueType

        return LabelValueType

    def test_one(self):
        self.assertTrue(hasattr(self._get_target_class(), 'STRING'))

    def test_names(self):
        for name in self._get_target_class().__dict__:
            if not name.startswith('_'):
                self.assertEqual(getattr(self._get_target_class(), name), name)


class TestLabelDescriptor(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.monitoring.label import LabelDescriptor

        return LabelDescriptor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_constructor(self):
        KEY = 'response_code'
        VALUE_TYPE = 'INT64'
        DESCRIPTION = 'HTTP status code for the request.'
        descriptor = self._make_one(key=KEY, value_type=VALUE_TYPE,
                                    description=DESCRIPTION)
        self.assertEqual(descriptor.key, KEY)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)
        self.assertEqual(descriptor.description, DESCRIPTION)

    def test_constructor_defaults(self):
        KEY = 'response_code'
        descriptor = self._make_one(key=KEY)
        self.assertEqual(descriptor.key, KEY)
        self.assertEqual(descriptor.value_type, 'STRING')
        self.assertEqual(descriptor.description, '')

    def test_from_dict(self):
        KEY = 'response_code'
        VALUE_TYPE = 'INT64'
        DESCRIPTION = 'HTTP status code for the request.'
        info = {
            'key': KEY,
            'valueType': VALUE_TYPE,
            'description': DESCRIPTION,
        }
        descriptor = self._get_target_class()._from_dict(info)
        self.assertEqual(descriptor.key, KEY)
        self.assertEqual(descriptor.value_type, VALUE_TYPE)
        self.assertEqual(descriptor.description, DESCRIPTION)

    def test_from_dict_defaults(self):
        KEY = 'response_code'
        info = {'key': KEY}
        descriptor = self._get_target_class()._from_dict(info)
        self.assertEqual(descriptor.key, KEY)
        self.assertEqual(descriptor.value_type, 'STRING')
        self.assertEqual(descriptor.description, '')

    def test_to_dict(self):
        KEY = 'response_code'
        VALUE_TYPE = 'INT64'
        DESCRIPTION = 'HTTP status code for the request.'
        descriptor = self._make_one(key=KEY, value_type=VALUE_TYPE,
                                    description=DESCRIPTION)
        expected = {
            'key': KEY,
            'valueType': VALUE_TYPE,
            'description': DESCRIPTION,
        }
        self.assertEqual(descriptor._to_dict(), expected)

    def test_to_dict_defaults(self):
        KEY = 'response_code'
        descriptor = self._make_one(key=KEY)
        expected = {
            'key': KEY,
            'valueType': 'STRING',
        }
        self.assertEqual(descriptor._to_dict(), expected)

    def test_equality(self):
        KEY = 'response_code'
        VALUE_TYPE = 'INT64'
        DESCRIPTION = 'HTTP status code for the request.'
        descriptor1 = self._make_one(key=KEY, value_type=VALUE_TYPE,
                                     description=DESCRIPTION)
        descriptor2 = self._make_one(key=KEY, value_type=VALUE_TYPE,
                                     description=DESCRIPTION)
        self.assertTrue(descriptor1 == descriptor2)
        self.assertFalse(descriptor1 != descriptor2)
