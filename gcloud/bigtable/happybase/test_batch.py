# Copyright 2016 Google Inc. All rights reserved.
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


class _SendMixin(object):

    _send_called = False

    def send(self):
        self._send_called = True


class TestBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.batch import Batch
        return Batch

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        table = object()
        batch = self._makeOne(table)
        self.assertEqual(batch._table, table)
        self.assertEqual(batch._batch_size, None)
        self.assertEqual(batch._timestamp, None)
        self.assertEqual(batch._delete_range, None)
        self.assertEqual(batch._transaction, False)
        self.assertEqual(batch._row_map, {})
        self.assertEqual(batch._mutation_count, 0)

    def test_constructor_explicit(self):
        from gcloud._helpers import _datetime_from_microseconds
        from gcloud.bigtable.row import TimestampRange

        table = object()
        timestamp = 144185290431
        batch_size = 42
        transaction = False  # Must be False when batch_size is non-null

        batch = self._makeOne(table, timestamp=timestamp,
                              batch_size=batch_size, transaction=transaction)
        self.assertEqual(batch._table, table)
        self.assertEqual(batch._batch_size, batch_size)
        self.assertEqual(batch._timestamp,
                         _datetime_from_microseconds(1000 * timestamp))

        next_timestamp = _datetime_from_microseconds(1000 * (timestamp + 1))
        time_range = TimestampRange(end=next_timestamp)
        self.assertEqual(batch._delete_range, time_range)
        self.assertEqual(batch._transaction, transaction)
        self.assertEqual(batch._row_map, {})
        self.assertEqual(batch._mutation_count, 0)

    def test_constructor_with_non_default_wal(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import batch as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        table = object()
        wal = object()
        with _Monkey(MUT, _WARN=mock_warn):
            self._makeOne(table, wal=wal)

        self.assertEqual(warned, [MUT._WAL_WARNING])

    def test_constructor_with_non_positive_batch_size(self):
        table = object()
        batch_size = -10
        with self.assertRaises(ValueError):
            self._makeOne(table, batch_size=batch_size)
        batch_size = 0
        with self.assertRaises(ValueError):
            self._makeOne(table, batch_size=batch_size)

    def test_constructor_with_batch_size_and_transactional(self):
        table = object()
        batch_size = 1
        transaction = True
        with self.assertRaises(TypeError):
            self._makeOne(table, batch_size=batch_size,
                          transaction=transaction)

    def test_send(self):
        table = object()
        batch = self._makeOne(table)

        batch._row_map = row_map = _MockRowMap()
        row_map['row-key1'] = row1 = _MockRow()
        row_map['row-key2'] = row2 = _MockRow()
        batch._mutation_count = 1337

        self.assertEqual(row_map.clear_count, 0)
        self.assertEqual(row1.commits, 0)
        self.assertEqual(row2.commits, 0)
        self.assertNotEqual(batch._mutation_count, 0)
        self.assertNotEqual(row_map, {})

        batch.send()
        self.assertEqual(row_map.clear_count, 1)
        self.assertEqual(row1.commits, 1)
        self.assertEqual(row2.commits, 1)
        self.assertEqual(batch._mutation_count, 0)
        self.assertEqual(row_map, {})

    def test_context_manager(self):
        klass = self._getTargetClass()

        class BatchWithSend(_SendMixin, klass):
            pass

        table = object()
        batch = BatchWithSend(table)
        self.assertFalse(batch._send_called)

        with batch:
            pass

        self.assertTrue(batch._send_called)

    def test_context_manager_with_exception_non_transactional(self):
        klass = self._getTargetClass()

        class BatchWithSend(_SendMixin, klass):
            pass

        table = object()
        batch = BatchWithSend(table)
        self.assertFalse(batch._send_called)

        with self.assertRaises(ValueError):
            with batch:
                raise ValueError('Something bad happened')

        self.assertTrue(batch._send_called)

    def test_context_manager_with_exception_transactional(self):
        klass = self._getTargetClass()

        class BatchWithSend(_SendMixin, klass):
            pass

        table = object()
        batch = BatchWithSend(table, transaction=True)
        self.assertFalse(batch._send_called)

        with self.assertRaises(ValueError):
            with batch:
                raise ValueError('Something bad happened')

        self.assertFalse(batch._send_called)

        # Just to make sure send() actually works (and to make cover happy).
        batch.send()
        self.assertTrue(batch._send_called)


class _MockRowMap(dict):

    clear_count = 0

    def clear(self):
        self.clear_count += 1
        super(_MockRowMap, self).clear()


class _MockRow(object):

    def __init__(self):
        self.commits = 0

    def commit(self):
        self.commits += 1
