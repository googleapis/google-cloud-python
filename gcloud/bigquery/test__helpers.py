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

import unittest2


class Test_ConfigurationProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery._helpers import _ConfigurationProperty
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
        self.assertEqual(wrapper.attr, None)

        value = object()
        wrapper.attr = value
        self.assertTrue(wrapper.attr is value)
        self.assertTrue(wrapper._configuration._attr is value)

        del wrapper.attr
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)


class Test_TypedProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery._helpers import _TypedProperty
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
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)


class Test_EnumProperty(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery._helpers import _EnumProperty
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
        self.assertEqual(wrapper.attr, None)
        self.assertEqual(wrapper._configuration._attr, None)
