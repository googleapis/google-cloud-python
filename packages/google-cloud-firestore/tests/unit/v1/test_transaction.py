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

import mock
import pytest


def _make_transaction(*args, **kwargs):
    from google.cloud.firestore_v1.transaction import Transaction

    return Transaction(*args, **kwargs)


def test_transaction_constructor_defaults():
    from google.cloud.firestore_v1.transaction import MAX_ATTEMPTS

    transaction = _make_transaction(mock.sentinel.client)
    assert transaction._client is mock.sentinel.client
    assert transaction._write_pbs == []
    assert transaction._max_attempts == MAX_ATTEMPTS
    assert not transaction._read_only
    assert transaction._id is None


def test_transaction_constructor_explicit():
    transaction = _make_transaction(
        mock.sentinel.client, max_attempts=10, read_only=True
    )
    assert transaction._client is mock.sentinel.client
    assert transaction._write_pbs == []
    assert transaction._max_attempts == 10
    assert transaction._read_only
    assert transaction._id is None


def test_transaction__add_write_pbs_failure():
    from google.cloud.firestore_v1.base_transaction import _WRITE_READ_ONLY

    batch = _make_transaction(mock.sentinel.client, read_only=True)
    assert batch._write_pbs == []
    with pytest.raises(ValueError) as exc_info:
        batch._add_write_pbs([mock.sentinel.write])

    assert exc_info.value.args == (_WRITE_READ_ONLY,)
    assert batch._write_pbs == []


def test_transaction__add_write_pbs():
    batch = _make_transaction(mock.sentinel.client)
    assert batch._write_pbs == []
    batch._add_write_pbs([mock.sentinel.write])
    assert batch._write_pbs == [mock.sentinel.write]


def test_transaction__clean_up():
    transaction = _make_transaction(mock.sentinel.client)
    transaction._write_pbs.extend([mock.sentinel.write_pb1, mock.sentinel.write])
    transaction._id = b"not-this-time-my-friend"

    ret_val = transaction._clean_up()
    assert ret_val is None

    assert transaction._write_pbs == []
    assert transaction._id is None


def test_transaction__begin():
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.types import firestore

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )
    txn_id = b"to-begin"
    response = firestore.BeginTransactionResponse(transaction=txn_id)
    firestore_api.begin_transaction.return_value = response

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction and ``begin()`` it.
    transaction = _make_transaction(client)
    assert transaction._id is None

    ret_val = transaction._begin()
    assert ret_val is None
    assert transaction._id == txn_id

    # Verify the called mock.
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": client._database_string, "options": None},
        metadata=client._rpc_metadata,
    )


def test_transaction__begin_failure():
    from google.cloud.firestore_v1.base_transaction import _CANT_BEGIN

    client = _make_client()
    transaction = _make_transaction(client)
    transaction._id = b"not-none"

    with pytest.raises(ValueError) as exc_info:
        transaction._begin()

    err_msg = _CANT_BEGIN.format(transaction._id)
    assert exc_info.value.args == (err_msg,)


def test_transaction__rollback():
    from google.protobuf import empty_pb2
    from google.cloud.firestore_v1.services.firestore import client as firestore_client

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )
    firestore_api.rollback.return_value = empty_pb2.Empty()

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction and roll it back.
    transaction = _make_transaction(client)
    txn_id = b"to-be-r\x00lled"
    transaction._id = txn_id
    ret_val = transaction._rollback()
    assert ret_val is None
    assert transaction._id is None

    # Verify the called mock.
    firestore_api.rollback.assert_called_once_with(
        request={"database": client._database_string, "transaction": txn_id},
        metadata=client._rpc_metadata,
    )


def test_transaction__rollback_not_allowed():
    from google.cloud.firestore_v1.base_transaction import _CANT_ROLLBACK

    client = _make_client()
    transaction = _make_transaction(client)
    assert transaction._id is None

    with pytest.raises(ValueError) as exc_info:
        transaction._rollback()

    assert exc_info.value.args == (_CANT_ROLLBACK,)


def test_transaction__rollback_failure():
    from google.api_core import exceptions
    from google.cloud.firestore_v1.services.firestore import client as firestore_client

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
    transaction = _make_transaction(client)
    txn_id = b"roll-bad-server"
    transaction._id = txn_id

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        transaction._rollback()

    assert exc_info.value is exc
    assert transaction._id is None
    assert transaction._write_pbs == []

    # Verify the called mock.
    firestore_api.rollback.assert_called_once_with(
        request={"database": client._database_string, "transaction": txn_id},
        metadata=client._rpc_metadata,
    )


def test_transaction__commit():
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.types import firestore
    from google.cloud.firestore_v1.types import write

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )
    commit_response = firestore.CommitResponse(write_results=[write.WriteResult()])
    firestore_api.commit.return_value = commit_response

    # Attach the fake GAPIC to a real client.
    client = _make_client("phone-joe")
    client._firestore_api_internal = firestore_api

    # Actually make a transaction with some mutations and call _commit().
    transaction = _make_transaction(client)
    txn_id = b"under-over-thru-woods"
    transaction._id = txn_id
    document = client.document("zap", "galaxy", "ship", "space")
    transaction.set(document, {"apple": 4.5})
    write_pbs = transaction._write_pbs[::]

    write_results = transaction._commit()
    assert write_results == list(commit_response.write_results)
    # Make sure transaction has no more "changes".
    assert transaction._id is None
    assert transaction._write_pbs == []

    # Verify the mocks.
    firestore_api.commit.assert_called_once_with(
        request={
            "database": client._database_string,
            "writes": write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )


def test_transaction__commit_not_allowed():
    from google.cloud.firestore_v1.base_transaction import _CANT_COMMIT

    transaction = _make_transaction(mock.sentinel.client)
    assert transaction._id is None
    with pytest.raises(ValueError) as exc_info:
        transaction._commit()

    assert exc_info.value.args == (_CANT_COMMIT,)


def test_transaction__commit_failure():
    from google.api_core import exceptions
    from google.cloud.firestore_v1.services.firestore import client as firestore_client

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
    transaction = _make_transaction(client)
    txn_id = b"beep-fail-commit"
    transaction._id = txn_id
    transaction.create(client.document("up", "down"), {"water": 1.0})
    transaction.delete(client.document("up", "left"))
    write_pbs = transaction._write_pbs[::]

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        transaction._commit()

    assert exc_info.value is exc
    assert transaction._id == txn_id
    assert transaction._write_pbs == write_pbs

    # Verify the called mock.
    firestore_api.commit.assert_called_once_with(
        request={
            "database": client._database_string,
            "writes": write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )


def _transaction_get_all_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers

    client = mock.Mock(spec=["get_all"])
    transaction = _make_transaction(client)
    ref1, ref2 = mock.Mock(), mock.Mock()
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = transaction.get_all([ref1, ref2], **kwargs)

    client.get_all.assert_called_once_with(
        [ref1, ref2],
        transaction=transaction,
        **kwargs,
    )
    assert result is client.get_all.return_value


def test_transaction_get_all():
    _transaction_get_all_helper()


def test_transaction_get_all_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _transaction_get_all_helper(retry=retry, timeout=timeout)


def _transaction_get_w_document_ref_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1.document import DocumentReference
    from google.cloud.firestore_v1 import _helpers

    client = mock.Mock(spec=["get_all"])
    transaction = _make_transaction(client)
    ref = DocumentReference("documents", "doc-id")
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = transaction.get(ref, **kwargs)

    assert result is client.get_all.return_value
    client.get_all.assert_called_once_with([ref], transaction=transaction, **kwargs)


def test_transaction_get_w_document_ref():
    _transaction_get_w_document_ref_helper()


def test_transaction_get_w_document_ref_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _transaction_get_w_document_ref_helper(retry=retry, timeout=timeout)


def _transaction_get_w_query_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.query import Query

    client = mock.Mock(spec=[])
    transaction = _make_transaction(client)
    query = Query(parent=mock.Mock(spec=[]))
    query.stream = mock.MagicMock()
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = transaction.get(query, **kwargs)

    assert result is query.stream.return_value
    query.stream.assert_called_once_with(transaction=transaction, **kwargs)


def test_transaction_get_w_query():
    _transaction_get_w_query_helper()


def test_transaction_get_w_query_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    _transaction_get_w_query_helper(retry=retry, timeout=timeout)


def test_transaction_get_failure():
    client = _make_client()
    transaction = _make_transaction(client)
    ref_or_query = object()
    with pytest.raises(ValueError):
        transaction.get(ref_or_query)


def _make__transactional(*args, **kwargs):
    from google.cloud.firestore_v1.transaction import _Transactional

    return _Transactional(*args, **kwargs)


def test__transactional_constructor():
    wrapped = _make__transactional(mock.sentinel.callable_)
    assert wrapped.to_wrap is mock.sentinel.callable_
    assert wrapped.current_id is None
    assert wrapped.retry_id is None


def test__transactional__pre_commit_success():
    to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"totes-began"
    transaction = _make_transaction_pb(txn_id)
    result = wrapped._pre_commit(transaction, "pos", key="word")
    assert result is mock.sentinel.result

    assert transaction._id == txn_id
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "pos", key="word")
    firestore_api = transaction._client._firestore_api
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": transaction._client._database_string, "options": None},
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_not_called()


def test__transactional__pre_commit_retry_id_already_set_success():
    from google.cloud.firestore_v1.types import common

    to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make__transactional(to_wrap)
    txn_id1 = b"already-set"
    wrapped.retry_id = txn_id1

    txn_id2 = b"ok-here-too"
    transaction = _make_transaction_pb(txn_id2)
    result = wrapped._pre_commit(transaction)
    assert result is mock.sentinel.result

    assert transaction._id == txn_id2
    assert wrapped.current_id == txn_id2
    assert wrapped.retry_id == txn_id1

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction)
    firestore_api = transaction._client._firestore_api
    options_ = common.TransactionOptions(
        read_write=common.TransactionOptions.ReadWrite(retry_transaction=txn_id1)
    )
    firestore_api.begin_transaction.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "options": options_,
        },
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_not_called()


def test__transactional__pre_commit_failure():
    exc = RuntimeError("Nope not today.")
    to_wrap = mock.Mock(side_effect=exc, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"gotta-fail"
    transaction = _make_transaction_pb(txn_id)
    with pytest.raises(RuntimeError) as exc_info:
        wrapped._pre_commit(transaction, 10, 20)
    assert exc_info.value is exc

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, 10, 20)
    firestore_api = transaction._client._firestore_api
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": transaction._client._database_string, "options": None},
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.commit.assert_not_called()


def test__transactional__pre_commit_failure_with_rollback_failure():
    from google.api_core import exceptions

    exc1 = ValueError("I will not be only failure.")
    to_wrap = mock.Mock(side_effect=exc1, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"both-will-fail"
    transaction = _make_transaction_pb(txn_id)
    # Actually force the ``rollback`` to fail as well.
    exc2 = exceptions.InternalServerError("Rollback blues.")
    firestore_api = transaction._client._firestore_api
    firestore_api.rollback.side_effect = exc2

    # Try to ``_pre_commit``
    with pytest.raises(exceptions.InternalServerError) as exc_info:
        wrapped._pre_commit(transaction, a="b", c="zebra")
    assert exc_info.value is exc2

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, a="b", c="zebra")
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": transaction._client._database_string, "options": None},
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.commit.assert_not_called()


def test__transactional__maybe_commit_success():
    wrapped = _make__transactional(mock.sentinel.callable_)

    txn_id = b"nyet"
    transaction = _make_transaction_pb(txn_id)
    transaction._id = txn_id  # We won't call ``begin()``.
    succeeded = wrapped._maybe_commit(transaction)
    assert succeeded

    # On success, _id is reset.
    assert transaction._id is None

    # Verify mocks.
    firestore_api = transaction._client._firestore_api
    firestore_api.begin_transaction.assert_not_called()
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test__transactional__maybe_commit_failure_read_only():
    from google.api_core import exceptions

    wrapped = _make__transactional(mock.sentinel.callable_)

    txn_id = b"failed"
    transaction = _make_transaction_pb(txn_id, read_only=True)
    transaction._id = txn_id  # We won't call ``begin()``.
    wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
    wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

    # Actually force the ``commit`` to fail (use ABORTED, but cannot
    # retry since read-only).
    exc = exceptions.Aborted("Read-only did a bad.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    with pytest.raises(exceptions.Aborted) as exc_info:
        wrapped._maybe_commit(transaction)
    assert exc_info.value is exc

    assert transaction._id == txn_id
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    firestore_api.begin_transaction.assert_not_called()
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test__transactional__maybe_commit_failure_can_retry():
    from google.api_core import exceptions

    wrapped = _make__transactional(mock.sentinel.callable_)

    txn_id = b"failed-but-retry"
    transaction = _make_transaction_pb(txn_id)
    transaction._id = txn_id  # We won't call ``begin()``.
    wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
    wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

    # Actually force the ``commit`` to fail.
    exc = exceptions.Aborted("Read-write did a bad.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    succeeded = wrapped._maybe_commit(transaction)
    assert not succeeded

    assert transaction._id == txn_id
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    firestore_api.begin_transaction.assert_not_called()
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test__transactional__maybe_commit_failure_cannot_retry():
    from google.api_core import exceptions

    wrapped = _make__transactional(mock.sentinel.callable_)

    txn_id = b"failed-but-not-retryable"
    transaction = _make_transaction_pb(txn_id)
    transaction._id = txn_id  # We won't call ``begin()``.
    wrapped.current_id = txn_id  # We won't call ``_pre_commit()``.
    wrapped.retry_id = txn_id  # We won't call ``_pre_commit()``.

    # Actually force the ``commit`` to fail.
    exc = exceptions.InternalServerError("Real bad thing")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        wrapped._maybe_commit(transaction)
    assert exc_info.value is exc

    assert transaction._id == txn_id
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    firestore_api.begin_transaction.assert_not_called()
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test__transactional___call__success_first_attempt():
    to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"whole-enchilada"
    transaction = _make_transaction_pb(txn_id)
    result = wrapped(transaction, "a", b="c")
    assert result is mock.sentinel.result

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "a", b="c")
    firestore_api = transaction._client._firestore_api
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": transaction._client._database_string, "options": None},
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test__transactional___call__success_second_attempt():
    from google.api_core import exceptions
    from google.cloud.firestore_v1.types import common
    from google.cloud.firestore_v1.types import firestore
    from google.cloud.firestore_v1.types import write

    to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"whole-enchilada"
    transaction = _make_transaction_pb(txn_id)

    # Actually force the ``commit`` to fail on first / succeed on second.
    exc = exceptions.Aborted("Contention junction.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = [
        exc,
        firestore.CommitResponse(write_results=[write.WriteResult()]),
    ]

    # Call the __call__-able ``wrapped``.
    result = wrapped(transaction, "a", b="c")
    assert result is mock.sentinel.result

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    wrapped_call = mock.call(transaction, "a", b="c")
    assert to_wrap.mock_calls, [wrapped_call == wrapped_call]
    firestore_api = transaction._client._firestore_api
    db_str = transaction._client._database_string
    options_ = common.TransactionOptions(
        read_write=common.TransactionOptions.ReadWrite(retry_transaction=txn_id)
    )
    expected_calls = [
        mock.call(
            request={"database": db_str, "options": None},
            metadata=transaction._client._rpc_metadata,
        ),
        mock.call(
            request={"database": db_str, "options": options_},
            metadata=transaction._client._rpc_metadata,
        ),
    ]
    assert firestore_api.begin_transaction.mock_calls == expected_calls
    firestore_api.rollback.assert_not_called()
    commit_call = mock.call(
        request={"database": db_str, "writes": [], "transaction": txn_id},
        metadata=transaction._client._rpc_metadata,
    )
    assert firestore_api.commit.mock_calls == [commit_call, commit_call]


def test__transactional___call__failure():
    from google.api_core import exceptions
    from google.cloud.firestore_v1.base_transaction import _EXCEED_ATTEMPTS_TEMPLATE

    to_wrap = mock.Mock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make__transactional(to_wrap)

    txn_id = b"only-one-shot"
    transaction = _make_transaction_pb(txn_id, max_attempts=1)

    # Actually force the ``commit`` to fail.
    exc = exceptions.Aborted("Contention just once.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    # Call the __call__-able ``wrapped``.
    with pytest.raises(ValueError) as exc_info:
        wrapped(transaction, "here", there=1.5)

    err_msg = _EXCEED_ATTEMPTS_TEMPLATE.format(transaction._max_attempts)
    assert exc_info.value.args == (err_msg,)

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "here", there=1.5)
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": transaction._client._database_string, "options": None},
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.commit.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


def test_transactional_factory():
    from google.cloud.firestore_v1.transaction import _Transactional
    from google.cloud.firestore_v1.transaction import transactional

    wrapped = transactional(mock.sentinel.callable_)
    assert isinstance(wrapped, _Transactional)
    assert wrapped.to_wrap is mock.sentinel.callable_


@mock.patch("google.cloud.firestore_v1.transaction._sleep")
def test__commit_with_retry_success_first_attempt(_sleep):
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.transaction import _commit_with_retry

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )

    # Attach the fake GAPIC to a real client.
    client = _make_client("summer")
    client._firestore_api_internal = firestore_api

    # Call function and check result.
    txn_id = b"cheeeeeez"
    commit_response = _commit_with_retry(client, mock.sentinel.write_pbs, txn_id)
    assert commit_response is firestore_api.commit.return_value

    # Verify mocks used.
    _sleep.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": client._database_string,
            "writes": mock.sentinel.write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )


@mock.patch("google.cloud.firestore_v1.transaction._sleep", side_effect=[2.0, 4.0])
def test__commit_with_retry_success_third_attempt(_sleep):
    from google.api_core import exceptions
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.transaction import _commit_with_retry

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
    commit_response = _commit_with_retry(client, mock.sentinel.write_pbs, txn_id)
    assert commit_response is mock.sentinel.commit_response

    # Verify mocks used.
    # Ensure _sleep is called after commit failures, with intervals of 1 and 2 seconds
    assert _sleep.call_count == 2
    _sleep.assert_any_call(1.0)
    _sleep.assert_any_call(2.0)
    # commit() called same way 3 times.
    commit_call = mock.call(
        request={
            "database": client._database_string,
            "writes": mock.sentinel.write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )
    assert firestore_api.commit.mock_calls == [commit_call, commit_call, commit_call]


@mock.patch("google.cloud.firestore_v1.transaction._sleep")
def test__commit_with_retry_failure_first_attempt(_sleep):
    from google.api_core import exceptions
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.transaction import _commit_with_retry

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
    with pytest.raises(exceptions.ResourceExhausted) as exc_info:
        _commit_with_retry(client, mock.sentinel.write_pbs, txn_id)

    assert exc_info.value is exc

    # Verify mocks used.
    _sleep.assert_not_called()
    firestore_api.commit.assert_called_once_with(
        request={
            "database": client._database_string,
            "writes": mock.sentinel.write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )


@mock.patch("google.cloud.firestore_v1.transaction._sleep", return_value=2.0)
def test__commit_with_retry_failure_second_attempt(_sleep):
    from google.api_core import exceptions
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.transaction import _commit_with_retry

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
    with pytest.raises(exceptions.InternalServerError) as exc_info:
        _commit_with_retry(client, mock.sentinel.write_pbs, txn_id)

    assert exc_info.value is exc2

    # Verify mocks used.
    _sleep.assert_called_once_with(1.0)
    # commit() called same way 2 times.
    commit_call = mock.call(
        request={
            "database": client._database_string,
            "writes": mock.sentinel.write_pbs,
            "transaction": txn_id,
        },
        metadata=client._rpc_metadata,
    )
    assert firestore_api.commit.mock_calls == [commit_call, commit_call]


@mock.patch("random.uniform", return_value=5.5)
@mock.patch("time.sleep", return_value=None)
def test_defaults(sleep, uniform):
    from google.cloud.firestore_v1.transaction import _sleep

    curr_sleep = 10.0
    assert uniform.return_value <= curr_sleep

    new_sleep = _sleep(curr_sleep)
    assert new_sleep == 2.0 * curr_sleep

    uniform.assert_called_once_with(0.0, curr_sleep)
    sleep.assert_called_once_with(uniform.return_value)


@mock.patch("random.uniform", return_value=10.5)
@mock.patch("time.sleep", return_value=None)
def test_explicit(sleep, uniform):
    from google.cloud.firestore_v1.transaction import _sleep

    curr_sleep = 12.25
    assert uniform.return_value <= curr_sleep

    multiplier = 1.5
    new_sleep = _sleep(curr_sleep, max_sleep=100.0, multiplier=multiplier)
    assert new_sleep == multiplier * curr_sleep

    uniform.assert_called_once_with(0.0, curr_sleep)
    sleep.assert_called_once_with(uniform.return_value)


@mock.patch("random.uniform", return_value=6.75)
@mock.patch("time.sleep", return_value=None)
def test_exceeds_max(sleep, uniform):
    from google.cloud.firestore_v1.transaction import _sleep

    curr_sleep = 20.0
    assert uniform.return_value <= curr_sleep

    max_sleep = 38.5
    new_sleep = _sleep(curr_sleep, max_sleep=max_sleep, multiplier=2.0)
    assert new_sleep == max_sleep

    uniform.assert_called_once_with(0.0, curr_sleep)
    sleep.assert_called_once_with(uniform.return_value)


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="feral-tom-cat"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)


def _make_transaction_pb(txn_id, **txn_kwargs):
    from google.protobuf import empty_pb2
    from google.cloud.firestore_v1.services.firestore import client as firestore_client
    from google.cloud.firestore_v1.types import firestore
    from google.cloud.firestore_v1.types import write
    from google.cloud.firestore_v1.transaction import Transaction

    # Create a fake GAPIC ...
    firestore_api = mock.create_autospec(
        firestore_client.FirestoreClient, instance=True
    )
    # ... with a dummy ``BeginTransactionResponse`` result ...
    begin_response = firestore.BeginTransactionResponse(transaction=txn_id)
    firestore_api.begin_transaction.return_value = begin_response
    # ... and a dummy ``Rollback`` result ...
    firestore_api.rollback.return_value = empty_pb2.Empty()
    # ... and a dummy ``Commit`` result.
    commit_response = firestore.CommitResponse(write_results=[write.WriteResult()])
    firestore_api.commit.return_value = commit_response

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    return Transaction(client, **txn_kwargs)
