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


class Test__timedelta_to_duration_pb(unittest2.TestCase):

    def _callFUT(self, *args, **kwargs):
        from gcloud.bigtable.column_family import _timedelta_to_duration_pb
        return _timedelta_to_duration_pb(*args, **kwargs)

    def test_it(self):
        import datetime
        from gcloud.bigtable._generated import duration_pb2

        seconds = microseconds = 1
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds)
        self.assertEqual(result.nanos, 1000 * microseconds)

    def test_with_negative_microseconds(self):
        import datetime
        from gcloud.bigtable._generated import duration_pb2

        seconds = 1
        microseconds = -5
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds - 1)
        self.assertEqual(result.nanos, 10**9 + 1000 * microseconds)

    def test_with_negative_seconds(self):
        import datetime
        from gcloud.bigtable._generated import duration_pb2

        seconds = -1
        microseconds = 5
        timedelta_val = datetime.timedelta(seconds=seconds,
                                           microseconds=microseconds)
        result = self._callFUT(timedelta_val)
        self.assertTrue(isinstance(result, duration_pb2.Duration))
        self.assertEqual(result.seconds, seconds + 1)
        self.assertEqual(result.nanos, -(10**9 - 1000 * microseconds))


class TestMaxVersionsGCRule(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule
        return MaxVersionsGCRule

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test___eq__type_differ(self):
        gc_rule1 = self._makeOne(10)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___eq__same_value(self):
        gc_rule1 = self._makeOne(2)
        gc_rule2 = self._makeOne(2)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        gc_rule1 = self._makeOne(99)
        gc_rule2 = self._makeOne(99)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        max_num_versions = 1337
        gc_rule = self._makeOne(max_num_versions=max_num_versions)
        pb_val = gc_rule.to_pb()
        self.assertEqual(pb_val,
                         data_pb2.GcRule(max_num_versions=max_num_versions))


class TestMaxAgeGCRule(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import MaxAgeGCRule
        return MaxAgeGCRule

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test___eq__type_differ(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = object()
        self.assertNotEqual(gc_rule1, gc_rule2)

    def test___eq__same_value(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = self._makeOne(max_age=max_age)
        self.assertEqual(gc_rule1, gc_rule2)

    def test___ne__same_value(self):
        max_age = object()
        gc_rule1 = self._makeOne(max_age=max_age)
        gc_rule2 = self._makeOne(max_age=max_age)
        comparison_val = (gc_rule1 != gc_rule2)
        self.assertFalse(comparison_val)

    def test_to_pb(self):
        import datetime
        from gcloud.bigtable._generated import (
            bigtable_table_data_pb2 as data_pb2)
        from gcloud.bigtable._generated import duration_pb2

        max_age = datetime.timedelta(seconds=1)
        duration = duration_pb2.Duration(seconds=1)
        gc_rule = self._makeOne(max_age=max_age)
        pb_val = gc_rule.to_pb()
        self.assertEqual(pb_val, data_pb2.GcRule(max_age=duration))


class TestColumnFamily(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.column_family import ColumnFamily
        return ColumnFamily

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor(self):
        column_family_id = u'column-family-id'
        table = object()
        column_family = self._makeOne(column_family_id, table)

        self.assertEqual(column_family.column_family_id, column_family_id)
        self.assertTrue(column_family._table is table)
