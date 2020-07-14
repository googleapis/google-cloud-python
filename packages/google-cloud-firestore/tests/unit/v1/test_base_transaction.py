# Copyright 2017 Google LLC All rights reserved.
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


class TestBaseTransaction(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.base_transaction import BaseTransaction

        return BaseTransaction

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.firestore_v1.transaction import MAX_ATTEMPTS

        transaction = self._make_one()
        self.assertEqual(transaction._max_attempts, MAX_ATTEMPTS)
        self.assertFalse(transaction._read_only)
        self.assertIsNone(transaction._id)

    def test_constructor_explicit(self):
        transaction = self._make_one(max_attempts=10, read_only=True)
        self.assertEqual(transaction._max_attempts, 10)
        self.assertTrue(transaction._read_only)
        self.assertIsNone(transaction._id)

    def test__options_protobuf_read_only(self):
        from google.cloud.firestore_v1.types import common

        transaction = self._make_one(read_only=True)
        options_pb = transaction._options_protobuf(None)
        expected_pb = common.TransactionOptions(
            read_only=common.TransactionOptions.ReadOnly()
        )
        self.assertEqual(options_pb, expected_pb)

    def test__options_protobuf_read_only_retry(self):
        from google.cloud.firestore_v1.base_transaction import _CANT_RETRY_READ_ONLY

        transaction = self._make_one(read_only=True)
        retry_id = b"illuminate"

        with self.assertRaises(ValueError) as exc_info:
            transaction._options_protobuf(retry_id)

        self.assertEqual(exc_info.exception.args, (_CANT_RETRY_READ_ONLY,))

    def test__options_protobuf_read_write(self):
        transaction = self._make_one()
        options_pb = transaction._options_protobuf(None)
        self.assertIsNone(options_pb)

    def test__options_protobuf_on_retry(self):
        from google.cloud.firestore_v1.types import common

        transaction = self._make_one()
        retry_id = b"hocus-pocus"
        options_pb = transaction._options_protobuf(retry_id)
        expected_pb = common.TransactionOptions(
            read_write=common.TransactionOptions.ReadWrite(retry_transaction=retry_id)
        )
        self.assertEqual(options_pb, expected_pb)

    def test_in_progress_property(self):
        transaction = self._make_one()
        self.assertFalse(transaction.in_progress)
        transaction._id = b"not-none-bites"
        self.assertTrue(transaction.in_progress)

    def test_id_property(self):
        transaction = self._make_one()
        transaction._id = mock.sentinel.eye_dee
        self.assertIs(transaction.id, mock.sentinel.eye_dee)


class Test_Transactional(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1.base_transaction import _BaseTransactional

        return _BaseTransactional

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor(self):
        wrapped = self._make_one(mock.sentinel.callable_)
        self.assertIs(wrapped.to_wrap, mock.sentinel.callable_)
        self.assertIsNone(wrapped.current_id)
        self.assertIsNone(wrapped.retry_id)

    def test__reset(self):
        wrapped = self._make_one(mock.sentinel.callable_)
        wrapped.current_id = b"not-none"
        wrapped.retry_id = b"also-not"

        ret_val = wrapped._reset()
        self.assertIsNone(ret_val)

        self.assertIsNone(wrapped.current_id)
        self.assertIsNone(wrapped.retry_id)
