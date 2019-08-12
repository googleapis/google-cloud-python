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
import pytest


class TestTransaction(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.transaction import Transaction

        return Transaction

    def _make_one(self, *args, **kwargs):
        klass = self._get_target_class()
        return klass(*args, **kwargs)

    def test_constructor_defaults(self):
        from google.cloud.firestore_v1beta1.transaction import MAX_ATTEMPTS

        transaction = self._make_one(mock.sentinel.client)
        self.assertIs(transaction._client, mock.sentinel.client)
        self.assertEqual(transaction._write_pbs, [])
        self.assertEqual(transaction._max_attempts, MAX_ATTEMPTS)
        self.assertFalse(transaction._read_only)
        self.assertIsNone(transaction._id)

    def test_constructor_explicit(self):
        transaction = self._make_one(
            mock.sentinel.client, max_attempts=10, read_only=True
        )
        self.assertIs(transaction._client, mock.sentinel.client)
        self.assertEqual(transaction._write_pbs, [])
        self.assertEqual(transaction._max_attempts, 10)
        self.assertTrue(transaction._read_only)
        self.assertIsNone(transaction._id)

    def test__add_write_pbs_failure(self):
        from google.cloud.firestore_v1beta1.transaction import _WRITE_READ_ONLY

        batch = self._make_one(mock.sentinel.client, read_only=True)
        self.assertEqual(batch._write_pbs, [])
        with self.assertRaises(ValueError) as exc_info:
            batch._add_write_pbs([mock.sentinel.write])

        self.assertEqual(exc_info.exception.args, (_WRITE_READ_ONLY,))
        self.assertEqual(batch._write_pbs, [])

    def test__add_write_pbs(self):
        batch = self._make_one(mock.sentinel.client)
        self.assertEqual(batch._write_pbs, [])
        batch._add_write_pbs([mock.sentinel.write])
        self.assertEqual(batch._write_pbs, [mock.sentinel.write])

    def test__options_protobuf_read_only(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2

        transaction = self._make_one(mock.sentinel.client, read_only=True)
        options_pb = transaction._options_protobuf(None)
        expected_pb = common_pb2.TransactionOptions(
            read_only=common_pb2.TransactionOptions.ReadOnly()
        )
        self.assertEqual(options_pb, expected_pb)

    def test__options_protobuf_read_only_retry(self):
        from google.cloud.firestore_v1beta1.transaction import _CANT_RETRY_READ_ONLY

        transaction = self._make_one(mock.sentinel.client, read_only=True)
        retry_id = b"illuminate"

        with self.assertRaises(ValueError) as exc_info:
            transaction._options_protobuf(retry_id)

        self.assertEqual(exc_info.exception.args, (_CANT_RETRY_READ_ONLY,))

    def test__options_protobuf_read_write(self):
        transaction = self._make_one(mock.sentinel.client)
        options_pb = transaction._options_protobuf(None)
        self.assertIsNone(options_pb)

    def test__options_protobuf_on_retry(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2

        transaction = self._make_one(mock.sentinel.client)
        retry_id = b"hocus-pocus"
        options_pb = transaction._options_protobuf(retry_id)
        expected_pb = common_pb2.TransactionOptions(
            read_write=common_pb2.TransactionOptions.ReadWrite(
                retry_transaction=retry_id
            )
        )
        self.assertEqual(options_pb, expected_pb)

    def test_in_progress_property(self):
        transaction = self._make_one(mock.sentinel.client)
        self.assertFalse(transaction.in_progress)
        transaction._id = b"not-none-bites"
        self.assertTrue(transaction.in_progress)

    def test_id_property(self):
        transaction = self._make_one(mock.sentinel.client)
        transaction._id = mock.sentinel.eye_dee
        self.assertIs(transaction.id, mock.sentinel.eye_dee)

    def test__begin(self):
        from google.cloud.firestore_v1beta1.gapic import firestore_client
        from google.cloud.firestore_v1beta1.proto import firestore_pb2

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        txn_id = b"to-begin"
        response = firestore_pb2.BeginTransactionResponse(transaction=txn_id)
        firestore_api.begin_transaction.return_value = response

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a transaction and ``begin()`` it.
        transaction = self._make_one(client)
        self.assertIsNone(transaction._id)

        ret_val = transaction._begin()
        self.assertIsNone(ret_val)
        self.assertEqual(transaction._id, txn_id)

        # Verify the called mock.
        firestore_api.begin_transaction.assert_called_once_with(
            client._database_string, options_=None, metadata=client._rpc_metadata
        )

    def test__begin_failure(self):
        from google.cloud.firestore_v1beta1.transaction import _CANT_BEGIN

        client = _make_client()
        transaction = self._make_one(client)
        transaction._id = b"not-none"

        with self.assertRaises(ValueError) as exc_info:
            transaction._begin()

        err_msg = _CANT_BEGIN.format(transaction._id)
        self.assertEqual(exc_info.exception.args, (err_msg,))

    def test__clean_up(self):
        transaction = self._make_one(mock.sentinel.client)
        transaction._write_pbs.extend(
            [mock.sentinel.write_pb1, mock.sentinel.write_pb2]
        )
        transaction._id = b"not-this-time-my-friend"

        ret_val = transaction._clean_up()
        self.assertIsNone(ret_val)

        self.assertEqual(transaction._write_pbs, [])
        self.assertIsNone(transaction._id)

    def test__rollback(self):
        from google.protobuf import empty_pb2
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        firestore_api.rollback.return_value = empty_pb2.Empty()

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a transaction and roll it back.
        transaction = self._make_one(client)
        txn_id = b"to-be-r\x00lled"
        transaction._id = txn_id
        ret_val = transaction._rollback()
        self.assertIsNone(ret_val)
        self.assertIsNone(transaction._id)

        # Verify the called mock.
        firestore_api.rollback.assert_called_once_with(
            client._database_string, txn_id, metadata=client._rpc_metadata
        )

    def test__rollback_not_allowed(self):
        from google.cloud.firestore_v1beta1.transaction import _CANT_ROLLBACK

        client = _make_client()
        transaction = self._make_one(client)
        self.assertIsNone(transaction._id)

        with self.assertRaises(ValueError) as exc_info:
            transaction._rollback()

        self.assertEqual(exc_info.exception.args, (_CANT_ROLLBACK,))

    def test__rollback_failure(self):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy failure.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        exc = exceptions.InternalServerError("Fire during rollback.")
        firestore_api.rollback.side_effect = exc

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a transaction and roll it back.
        transaction = self._make_one(client)
        txn_id = b"roll-bad-server"
        transaction._id = txn_id

        with self.assertRaises(exceptions.InternalServerError) as exc_info:
            transaction._rollback()

        self.assertIs(exc_info.exception, exc)
        self.assertIsNone(transaction._id)
        self.assertEqual(transaction._write_pbs, [])

        # Verify the called mock.
        firestore_api.rollback.assert_called_once_with(
            client._database_string, txn_id, metadata=client._rpc_metadata
        )

    def test__commit(self):
        from google.cloud.firestore_v1beta1.gapic import firestore_client
        from google.cloud.firestore_v1beta1.proto import firestore_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        commit_response = firestore_pb2.CommitResponse(
            write_results=[write_pb2.WriteResult()]
        )
        firestore_api.commit.return_value = commit_response

        # Attach the fake GAPIC to a real client.
        client = _make_client("phone-joe")
        client._firestore_api_internal = firestore_api

        # Actually make a transaction with some mutations and call _commit().
        transaction = self._make_one(client)
        txn_id = b"under-over-thru-woods"
        transaction._id = txn_id
        document = client.document("zap", "galaxy", "ship", "space")
        transaction.set(document, {"apple": 4.5})
        write_pbs = transaction._write_pbs[::]

        write_results = transaction._commit()
        self.assertEqual(write_results, list(commit_response.write_results))
        # Make sure transaction has no more "changes".
        self.assertIsNone(transaction._id)
        self.assertEqual(transaction._write_pbs, [])

        # Verify the mocks.
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )

    def test__commit_not_allowed(self):
        from google.cloud.firestore_v1beta1.transaction import _CANT_COMMIT

        transaction = self._make_one(mock.sentinel.client)
        self.assertIsNone(transaction._id)
        with self.assertRaises(ValueError) as exc_info:
            transaction._commit()

        self.assertEqual(exc_info.exception.args, (_CANT_COMMIT,))

    def test__commit_failure(self):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy failure.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        exc = exceptions.InternalServerError("Fire during commit.")
        firestore_api.commit.side_effect = exc

        # Attach the fake GAPIC to a real client.
        client = _make_client()
        client._firestore_api_internal = firestore_api

        # Actually make a transaction with some mutations and call _commit().
        transaction = self._make_one(client)
        txn_id = b"beep-fail-commit"
        transaction._id = txn_id
        transaction.create(client.document("up", "down"), {"water": 1.0})
        transaction.delete(client.document("up", "left"))
        write_pbs = transaction._write_pbs[::]

        with self.assertRaises(exceptions.InternalServerError) as exc_info:
            transaction._commit()

        self.assertIs(exc_info.exception, exc)
        self.assertEqual(transaction._id, txn_id)
        self.assertEqual(transaction._write_pbs, write_pbs)

        # Verify the called mock.
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )


class Test_Transactional(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.firestore_v1beta1.transaction import _Transactional

        return _Transactional

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

    def test__pre_commit_success(self):
        to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"totes-began"
        transaction = _make_transaction(txn_id)
        result = wrapped._pre_commit(transaction, "pos", key="word")
        self.assertIs(result, mock.sentinel.result)

        self.assertEqual(transaction._id, txn_id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction, "pos", key="word")
        firestore_api = transaction._client._firestore_api
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=None,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_not_called()

    def test__pre_commit_retry_id_already_set_success(self):
        from google.cloud.firestore_v1beta1.proto import common_pb2

        to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
        wrapped = self._make_one(to_wrap)
        txn_id1 = b"already-set"
        wrapped.retry_id = txn_id1

        txn_id2 = b"ok-here-too"
        transaction = _make_transaction(txn_id2)
        result = wrapped._pre_commit(transaction)
        self.assertIs(result, mock.sentinel.result)

        self.assertEqual(transaction._id, txn_id2)
        self.assertEqual(wrapped.current_id, txn_id2)
        self.assertEqual(wrapped.retry_id, txn_id1)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction)
        firestore_api = transaction._client._firestore_api
        options_ = common_pb2.TransactionOptions(
            read_write=common_pb2.TransactionOptions.ReadWrite(
                retry_transaction=txn_id1
            )
        )
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=options_,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_not_called()

    def test__pre_commit_failure(self):
        exc = RuntimeError("Nope not today.")
        to_wrap = mock.Mock(side_effect=exc, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"gotta-fail"
        transaction = _make_transaction(txn_id)
        with self.assertRaises(RuntimeError) as exc_info:
            wrapped._pre_commit(transaction, 10, 20)
        self.assertIs(exc_info.exception, exc)

        self.assertIsNone(transaction._id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction, 10, 20)
        firestore_api = transaction._client._firestore_api
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=None,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_called_once_with(
            transaction._client._database_string,
            txn_id,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.commit.assert_not_called()

    def test__pre_commit_failure_with_rollback_failure(self):
        from google.api_core import exceptions

        exc1 = ValueError("I will not be only failure.")
        to_wrap = mock.Mock(side_effect=exc1, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"both-will-fail"
        transaction = _make_transaction(txn_id)
        # Actually force the ``rollback`` to fail as well.
        exc2 = exceptions.InternalServerError("Rollback blues.")
        firestore_api = transaction._client._firestore_api
        firestore_api.rollback.side_effect = exc2

        # Try to ``_pre_commit``
        with self.assertRaises(exceptions.InternalServerError) as exc_info:
            wrapped._pre_commit(transaction, a="b", c="zebra")
        self.assertIs(exc_info.exception, exc2)

        self.assertIsNone(transaction._id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction, a="b", c="zebra")
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=None,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_called_once_with(
            transaction._client._database_string,
            txn_id,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.commit.assert_not_called()

    def test__maybe_commit_success(self):
        wrapped = self._make_one(mock.sentinel.callable_)

        txn_id = b"nyet"
        transaction = _make_transaction(txn_id)
        transaction._id = txn_id  # We won't call ``begin()``.
        succeeded = wrapped._maybe_commit(transaction)
        self.assertTrue(succeeded)

        # On success, _id is reset.
        self.assertIsNone(transaction._id)

        # Verify mocks.
        firestore_api = transaction._client._firestore_api
        firestore_api.begin_transaction.assert_not_called()
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )

    def test__maybe_commit_failure_read_only(self):
        from google.api_core import exceptions

        wrapped = self._make_one(mock.sentinel.callable_)

        txn_id = b"failed"
        transaction = _make_transaction(txn_id, read_only=True)
        transaction._id = txn_id  # We won't call ``begin()``.
        wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
        wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

        # Actually force the ``commit`` to fail (use ABORTED, but cannot
        # retry since read-only).
        exc = exceptions.Aborted("Read-only did a bad.")
        firestore_api = transaction._client._firestore_api
        firestore_api.commit.side_effect = exc

        with self.assertRaises(exceptions.Aborted) as exc_info:
            wrapped._maybe_commit(transaction)
        self.assertIs(exc_info.exception, exc)

        self.assertEqual(transaction._id, txn_id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        firestore_api.begin_transaction.assert_not_called()
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )

    def test__maybe_commit_failure_can_retry(self):
        from google.api_core import exceptions

        wrapped = self._make_one(mock.sentinel.callable_)

        txn_id = b"failed-but-retry"
        transaction = _make_transaction(txn_id)
        transaction._id = txn_id  # We won't call ``begin()``.
        wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
        wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

        # Actually force the ``commit`` to fail.
        exc = exceptions.Aborted("Read-write did a bad.")
        firestore_api = transaction._client._firestore_api
        firestore_api.commit.side_effect = exc

        succeeded = wrapped._maybe_commit(transaction)
        self.assertFalse(succeeded)

        self.assertEqual(transaction._id, txn_id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        firestore_api.begin_transaction.assert_not_called()
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )

    def test__maybe_commit_failure_cannot_retry(self):
        from google.api_core import exceptions

        wrapped = self._make_one(mock.sentinel.callable_)

        txn_id = b"failed-but-not-retryable"
        transaction = _make_transaction(txn_id)
        transaction._id = txn_id  # We won't call ``begin()``.
        wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
        wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

        # Actually force the ``commit`` to fail.
        exc = exceptions.InternalServerError("Real bad thing")
        firestore_api = transaction._client._firestore_api
        firestore_api.commit.side_effect = exc

        with self.assertRaises(exceptions.InternalServerError) as exc_info:
            wrapped._maybe_commit(transaction)
        self.assertIs(exc_info.exception, exc)

        self.assertEqual(transaction._id, txn_id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        firestore_api.begin_transaction.assert_not_called()
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )

    def test___call__success_first_attempt(self):
        to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"whole-enchilada"
        transaction = _make_transaction(txn_id)
        result = wrapped(transaction, "a", b="c")
        self.assertIs(result, mock.sentinel.result)

        self.assertIsNone(transaction._id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction, "a", b="c")
        firestore_api = transaction._client._firestore_api
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=None,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )

    def test___call__success_second_attempt(self):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.proto import common_pb2
        from google.cloud.firestore_v1beta1.proto import firestore_pb2
        from google.cloud.firestore_v1beta1.proto import write_pb2

        to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"whole-enchilada"
        transaction = _make_transaction(txn_id)

        # Actually force the ``commit`` to fail on first / succeed on second.
        exc = exceptions.Aborted("Contention junction.")
        firestore_api = transaction._client._firestore_api
        firestore_api.commit.side_effect = [
            exc,
            firestore_pb2.CommitResponse(write_results=[write_pb2.WriteResult()]),
        ]

        # Call the __call__-able ``wrapped``.
        result = wrapped(transaction, "a", b="c")
        self.assertIs(result, mock.sentinel.result)

        self.assertIsNone(transaction._id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        wrapped_call = mock.call(transaction, "a", b="c")
        self.assertEqual(to_wrap.mock_calls, [wrapped_call, wrapped_call])
        firestore_api = transaction._client._firestore_api
        db_str = transaction._client._database_string
        options_ = common_pb2.TransactionOptions(
            read_write=common_pb2.TransactionOptions.ReadWrite(retry_transaction=txn_id)
        )
        self.assertEqual(
            firestore_api.begin_transaction.mock_calls,
            [
                mock.call(
                    db_str, options_=None, metadata=transaction._client._rpc_metadata
                ),
                mock.call(
                    db_str,
                    options_=options_,
                    metadata=transaction._client._rpc_metadata,
                ),
            ],
        )
        firestore_api.rollback.assert_not_called()
        commit_call = mock.call(
            db_str, [], transaction=txn_id, metadata=transaction._client._rpc_metadata
        )
        self.assertEqual(firestore_api.commit.mock_calls, [commit_call, commit_call])

    def test___call__failure(self):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.transaction import _EXCEED_ATTEMPTS_TEMPLATE

        to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
        wrapped = self._make_one(to_wrap)

        txn_id = b"only-one-shot"
        transaction = _make_transaction(txn_id, max_attempts=1)

        # Actually force the ``commit`` to fail.
        exc = exceptions.Aborted("Contention just once.")
        firestore_api = transaction._client._firestore_api
        firestore_api.commit.side_effect = exc

        # Call the __call__-able ``wrapped``.
        with self.assertRaises(ValueError) as exc_info:
            wrapped(transaction, "here", there=1.5)

        err_msg = _EXCEED_ATTEMPTS_TEMPLATE.format(transaction._max_attempts)
        self.assertEqual(exc_info.exception.args, (err_msg,))

        self.assertIsNone(transaction._id)
        self.assertEqual(wrapped.current_id, txn_id)
        self.assertEqual(wrapped.retry_id, txn_id)

        # Verify mocks.
        to_wrap.assert_called_once_with(transaction, "here", there=1.5)
        firestore_api.begin_transaction.assert_called_once_with(
            transaction._client._database_string,
            options_=None,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.rollback.assert_called_once_with(
            transaction._client._database_string,
            txn_id,
            metadata=transaction._client._rpc_metadata,
        )
        firestore_api.commit.assert_called_once_with(
            transaction._client._database_string,
            [],
            transaction=txn_id,
            metadata=transaction._client._rpc_metadata,
        )


class Test_transactional(unittest.TestCase):
    @staticmethod
    def _call_fut(to_wrap):
        from google.cloud.firestore_v1beta1.transaction import transactional

        return transactional(to_wrap)

    def test_it(self):
        from google.cloud.firestore_v1beta1.transaction import _Transactional

        wrapped = self._call_fut(mock.sentinel.callable_)
        self.assertIsInstance(wrapped, _Transactional)
        self.assertIs(wrapped.to_wrap, mock.sentinel.callable_)


class Test__commit_with_retry(unittest.TestCase):
    @staticmethod
    def _call_fut(client, write_pbs, transaction_id):
        from google.cloud.firestore_v1beta1.transaction import _commit_with_retry

        return _commit_with_retry(client, write_pbs, transaction_id)

    @mock.patch("google.cloud.firestore_v1beta1.transaction._sleep")
    def test_success_first_attempt(self, _sleep):
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )

        # Attach the fake GAPIC to a real client.
        client = _make_client("summer")
        client._firestore_api_internal = firestore_api

        # Call function and check result.
        txn_id = b"cheeeeeez"
        commit_response = self._call_fut(client, mock.sentinel.write_pbs, txn_id)
        self.assertIs(commit_response, firestore_api.commit.return_value)

        # Verify mocks used.
        _sleep.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            mock.sentinel.write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )

    @mock.patch(
        "google.cloud.firestore_v1beta1.transaction._sleep", side_effect=[2.0, 4.0]
    )
    def test_success_third_attempt(self, _sleep):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        # Make sure the first two requests fail and the third succeeds.
        firestore_api.commit.side_effect = [
            exceptions.ServiceUnavailable("Server sleepy."),
            exceptions.ServiceUnavailable("Server groggy."),
            mock.sentinel.commit_response,
        ]

        # Attach the fake GAPIC to a real client.
        client = _make_client("outside")
        client._firestore_api_internal = firestore_api

        # Call function and check result.
        txn_id = b"the-world\x00"
        commit_response = self._call_fut(client, mock.sentinel.write_pbs, txn_id)
        self.assertIs(commit_response, mock.sentinel.commit_response)

        # Verify mocks used.
        self.assertEqual(_sleep.call_count, 2)
        _sleep.assert_any_call(1.0)
        _sleep.assert_any_call(2.0)
        # commit() called same way 3 times.
        commit_call = mock.call(
            client._database_string,
            mock.sentinel.write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )
        self.assertEqual(
            firestore_api.commit.mock_calls, [commit_call, commit_call, commit_call]
        )

    @mock.patch("google.cloud.firestore_v1beta1.transaction._sleep")
    def test_failure_first_attempt(self, _sleep):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        # Make sure the first request fails with an un-retryable error.
        exc = exceptions.ResourceExhausted("We ran out of fries.")
        firestore_api.commit.side_effect = exc

        # Attach the fake GAPIC to a real client.
        client = _make_client("peanut-butter")
        client._firestore_api_internal = firestore_api

        # Call function and check result.
        txn_id = b"\x08\x06\x07\x05\x03\x00\x09-jenny"
        with self.assertRaises(exceptions.ResourceExhausted) as exc_info:
            self._call_fut(client, mock.sentinel.write_pbs, txn_id)

        self.assertIs(exc_info.exception, exc)

        # Verify mocks used.
        _sleep.assert_not_called()
        firestore_api.commit.assert_called_once_with(
            client._database_string,
            mock.sentinel.write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )

    @mock.patch("google.cloud.firestore_v1beta1.transaction._sleep", return_value=2.0)
    def test_failure_second_attempt(self, _sleep):
        from google.api_core import exceptions
        from google.cloud.firestore_v1beta1.gapic import firestore_client

        # Create a minimal fake GAPIC with a dummy result.
        firestore_api = mock.create_autospec(
            firestore_client.FirestoreClient, instance=True
        )
        # Make sure the first request fails retry-able and second
        # fails non-retryable.
        exc1 = exceptions.ServiceUnavailable("Come back next time.")
        exc2 = exceptions.InternalServerError("Server on fritz.")
        firestore_api.commit.side_effect = [exc1, exc2]

        # Attach the fake GAPIC to a real client.
        client = _make_client("peanut-butter")
        client._firestore_api_internal = firestore_api

        # Call function and check result.
        txn_id = b"the-journey-when-and-where-well-go"
        with self.assertRaises(exceptions.InternalServerError) as exc_info:
            self._call_fut(client, mock.sentinel.write_pbs, txn_id)

        self.assertIs(exc_info.exception, exc2)

        # Verify mocks used.
        _sleep.assert_called_once_with(1.0)
        # commit() called same way 2 times.
        commit_call = mock.call(
            client._database_string,
            mock.sentinel.write_pbs,
            transaction=txn_id,
            metadata=client._rpc_metadata,
        )
        self.assertEqual(firestore_api.commit.mock_calls, [commit_call, commit_call])


class Test__sleep(unittest.TestCase):
    @staticmethod
    def _call_fut(current_sleep, **kwargs):
        from google.cloud.firestore_v1beta1.transaction import _sleep

        return _sleep(current_sleep, **kwargs)

    @mock.patch("random.uniform", return_value=5.5)
    @mock.patch("time.sleep", return_value=None)
    def test_defaults(self, sleep, uniform):
        curr_sleep = 10.0
        self.assertLessEqual(uniform.return_value, curr_sleep)

        new_sleep = self._call_fut(curr_sleep)
        self.assertEqual(new_sleep, 2.0 * curr_sleep)

        uniform.assert_called_once_with(0.0, curr_sleep)
        sleep.assert_called_once_with(uniform.return_value)

    @mock.patch("random.uniform", return_value=10.5)
    @mock.patch("time.sleep", return_value=None)
    def test_explicit(self, sleep, uniform):
        curr_sleep = 12.25
        self.assertLessEqual(uniform.return_value, curr_sleep)

        multiplier = 1.5
        new_sleep = self._call_fut(curr_sleep, max_sleep=100.0, multiplier=multiplier)
        self.assertEqual(new_sleep, multiplier * curr_sleep)

        uniform.assert_called_once_with(0.0, curr_sleep)
        sleep.assert_called_once_with(uniform.return_value)

    @mock.patch("random.uniform", return_value=6.75)
    @mock.patch("time.sleep", return_value=None)
    def test_exceeds_max(self, sleep, uniform):
        curr_sleep = 20.0
        self.assertLessEqual(uniform.return_value, curr_sleep)

        max_sleep = 38.5
        new_sleep = self._call_fut(curr_sleep, max_sleep=max_sleep, multiplier=2.0)
        self.assertEqual(new_sleep, max_sleep)

        uniform.assert_called_once_with(0.0, curr_sleep)
        sleep.assert_called_once_with(uniform.return_value)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="feral-tom-cat"):
    from google.cloud.firestore_v1beta1.client import Client

    credentials = _make_credentials()

    with pytest.deprecated_call():
        return Client(project=project, credentials=credentials)


def _make_transaction(txn_id, **txn_kwargs):
    from google.protobuf import empty_pb2
    from google.cloud.firestore_v1beta1.gapic import firestore_client
    from google.cloud.firestore_v1beta1.proto import firestore_pb2
    from google.cloud.firestore_v1beta1.proto import write_pb2
    from google.cloud.firestore_v1beta1.transaction import Transaction

    # Create a fake GAPIC ...
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )
    # ... with a dummy ``BeginTransactionResponse`` result ...
    begin_response = firestore_pb2.BeginTransactionResponse(transaction=txn_id)
    firestore_api.begin_transaction.return_value = begin_response
    # ... and a dummy ``Rollback`` result ...
    firestore_api.rollback.return_value = empty_pb2.Empty()
    # ... and a dummy ``Commit`` result.
    commit_response = firestore_pb2.CommitResponse(
        write_results=[write_pb2.WriteResult()]
    )
    firestore_api.commit.return_value = commit_response

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    return Transaction(client, **txn_kwargs)
