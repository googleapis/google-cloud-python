# Copyright 2020 Google LLC All rights reserved.
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

from tests.unit.v1.test__helpers import AsyncMock


def _make_async_transaction(*args, **kwargs):
    from google.cloud.firestore_v1.async_transaction import AsyncTransaction

    return AsyncTransaction(*args, **kwargs)


def test_asynctransaction_constructor_defaults():
    from google.cloud.firestore_v1.async_transaction import MAX_ATTEMPTS

    transaction = _make_async_transaction(mock.sentinel.client)
    assert transaction._client is mock.sentinel.client
    assert transaction._write_pbs == []
    assert transaction._max_attempts == MAX_ATTEMPTS
    assert not transaction._read_only
    assert transaction._id is None


def test_asynctransaction_constructor_explicit():
    transaction = _make_async_transaction(
        mock.sentinel.client, max_attempts=10, read_only=True
    )
    assert transaction._client is mock.sentinel.client
    assert transaction._write_pbs == []
    assert transaction._max_attempts == 10
    assert transaction._read_only
    assert transaction._id is None


def test_asynctransaction__add_write_pbs_failure():
    from google.cloud.firestore_v1.base_transaction import _WRITE_READ_ONLY

    batch = _make_async_transaction(mock.sentinel.client, read_only=True)
    assert batch._write_pbs == []
    with pytest.raises(ValueError) as exc_info:
        batch._add_write_pbs([mock.sentinel.write])

    assert exc_info.value.args == (_WRITE_READ_ONLY,)
    assert batch._write_pbs == []


def test_asynctransaction__add_write_pbs():
    batch = _make_async_transaction(mock.sentinel.client)
    assert batch._write_pbs == []
    batch._add_write_pbs([mock.sentinel.write])
    assert batch._write_pbs == [mock.sentinel.write]


def test_asynctransaction__clean_up():
    transaction = _make_async_transaction(mock.sentinel.client)
    transaction._write_pbs.extend([mock.sentinel.write_pb1, mock.sentinel.write_pb2])
    transaction._id = b"not-this-time-my-friend"

    ret_val = transaction._clean_up()
    assert ret_val is None

    assert transaction._write_pbs == []
    assert transaction._id is None


@pytest.mark.asyncio
async def test_asynctransaction__begin():
    from google.cloud.firestore_v1.types import firestore

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = AsyncMock()
    txn_id = b"to-begin"
    response = firestore.BeginTransactionResponse(transaction=txn_id)
    firestore_api.begin_transaction.return_value = response

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction and ``begin()`` it.
    transaction = _make_async_transaction(client)
    assert transaction._id is None

    ret_val = await transaction._begin()
    assert ret_val is None
    assert transaction._id == txn_id

    # Verify the called mock.
    firestore_api.begin_transaction.assert_called_once_with(
        request={"database": client._database_string, "options": None},
        metadata=client._rpc_metadata,
    )


@pytest.mark.asyncio
async def test_asynctransaction__begin_failure():
    from google.cloud.firestore_v1.base_transaction import _CANT_BEGIN

    client = _make_client()
    transaction = _make_async_transaction(client)
    transaction._id = b"not-none"

    with pytest.raises(ValueError) as exc_info:
        await transaction._begin()

    err_msg = _CANT_BEGIN.format(transaction._id)
    assert exc_info.value.args == (err_msg,)


@pytest.mark.asyncio
async def test_asynctransaction__rollback():
    from google.protobuf import empty_pb2

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = AsyncMock()
    firestore_api.rollback.return_value = empty_pb2.Empty()

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction and roll it back.
    transaction = _make_async_transaction(client)
    txn_id = b"to-be-r\x00lled"
    transaction._id = txn_id
    ret_val = await transaction._rollback()
    assert ret_val is None
    assert transaction._id is None

    # Verify the called mock.
    firestore_api.rollback.assert_called_once_with(
        request={"database": client._database_string, "transaction": txn_id},
        metadata=client._rpc_metadata,
    )


@pytest.mark.asyncio
async def test_asynctransaction__rollback_not_allowed():
    from google.cloud.firestore_v1.base_transaction import _CANT_ROLLBACK

    client = _make_client()
    transaction = _make_async_transaction(client)
    assert transaction._id is None

    with pytest.raises(ValueError) as exc_info:
        await transaction._rollback()
    assert exc_info.value.args == (_CANT_ROLLBACK,)


@pytest.mark.asyncio
async def test_asynctransaction__rollback_failure():
    from google.api_core import exceptions

    # Create a minimal fake GAPIC with a dummy failure.
    firestore_api = AsyncMock()
    exc = exceptions.InternalServerError("Fire during rollback.")
    firestore_api.rollback.side_effect = exc

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction and roll it back.
    transaction = _make_async_transaction(client)
    txn_id = b"roll-bad-server"
    transaction._id = txn_id

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        await transaction._rollback()

    assert exc_info.value is exc
    assert transaction._id is None
    assert transaction._write_pbs == []

    # Verify the called mock.
    firestore_api.rollback.assert_called_once_with(
        request={"database": client._database_string, "transaction": txn_id},
        metadata=client._rpc_metadata,
    )


@pytest.mark.asyncio
async def test_asynctransaction__commit():
    from google.cloud.firestore_v1.types import firestore, write

    # Create a minimal fake GAPIC with a dummy result.
    firestore_api = AsyncMock()
    commit_response = firestore.CommitResponse(write_results=[write.WriteResult()])
    firestore_api.commit.return_value = commit_response

    # Attach the fake GAPIC to a real client.
    client = _make_client("phone-joe")
    client._firestore_api_internal = firestore_api

    # Actually make a transaction with some mutations and call _commit().
    transaction = _make_async_transaction(client)
    txn_id = b"under-over-thru-woods"
    transaction._id = txn_id
    document = client.document("zap", "galaxy", "ship", "space")
    transaction.set(document, {"apple": 4.5})
    write_pbs = transaction._write_pbs[::]

    write_results = await transaction._commit()
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


@pytest.mark.asyncio
async def test_asynctransaction__commit_not_allowed():
    from google.cloud.firestore_v1.base_transaction import _CANT_COMMIT

    transaction = _make_async_transaction(mock.sentinel.client)
    assert transaction._id is None
    with pytest.raises(ValueError) as exc_info:
        await transaction._commit()

    assert exc_info.value.args == (_CANT_COMMIT,)


@pytest.mark.asyncio
async def test_asynctransaction__commit_failure():
    from google.api_core import exceptions

    # Create a minimal fake GAPIC with a dummy failure.
    firestore_api = AsyncMock()
    exc = exceptions.InternalServerError("Fire during commit.")
    firestore_api.commit.side_effect = exc

    # Attach the fake GAPIC to a real client.
    client = _make_client()
    client._firestore_api_internal = firestore_api

    # Actually make a transaction with some mutations and call _commit().
    transaction = _make_async_transaction(client)
    txn_id = b"beep-fail-commit"
    transaction._id = txn_id
    transaction.create(client.document("up", "down"), {"water": 1.0})
    transaction.delete(client.document("up", "left"))
    write_pbs = transaction._write_pbs[::]

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        await transaction._commit()

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


async def _get_all_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers

    client = AsyncMock(spec=["get_all"])
    transaction = _make_async_transaction(client)
    ref1, ref2 = mock.Mock(), mock.Mock()
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = await transaction.get_all([ref1, ref2], **kwargs)

    client.get_all.assert_called_once_with(
        [ref1, ref2],
        transaction=transaction,
        **kwargs,
    )
    assert result is client.get_all.return_value


@pytest.mark.asyncio
async def test_asynctransaction_get_all():
    await _get_all_helper()


@pytest.mark.asyncio
async def test_asynctransaction_get_all_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    await _get_all_helper(retry=retry, timeout=timeout)


async def _get_w_document_ref_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.async_document import AsyncDocumentReference

    client = AsyncMock(spec=["get_all"])
    transaction = _make_async_transaction(client)
    ref = AsyncDocumentReference("documents", "doc-id")
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = await transaction.get(ref, **kwargs)

    client.get_all.assert_called_once_with([ref], transaction=transaction, **kwargs)
    assert result is client.get_all.return_value


@pytest.mark.asyncio
async def test_asynctransaction_get_w_document_ref():
    await _get_w_document_ref_helper()


@pytest.mark.asyncio
async def test_asynctransaction_get_w_document_ref_w_retry_timeout():
    from google.api_core.retry import Retry

    retry = Retry(predicate=object())
    timeout = 123.0
    await _get_w_document_ref_helper(retry=retry, timeout=timeout)


async def _get_w_query_helper(retry=None, timeout=None):
    from google.cloud.firestore_v1 import _helpers
    from google.cloud.firestore_v1.async_query import AsyncQuery

    client = AsyncMock(spec=[])
    transaction = _make_async_transaction(client)
    query = AsyncQuery(parent=AsyncMock(spec=[]))
    query.stream = AsyncMock()
    kwargs = _helpers.make_retry_timeout_kwargs(retry, timeout)

    result = await transaction.get(
        query,
        **kwargs,
    )

    query.stream.assert_called_once_with(
        transaction=transaction,
        **kwargs,
    )
    assert result is query.stream.return_value


@pytest.mark.asyncio
async def test_asynctransaction_get_w_query():
    await _get_w_query_helper()


@pytest.mark.asyncio
async def test_asynctransaction_get_w_query_w_retry_timeout():
    await _get_w_query_helper()


@pytest.mark.asyncio
async def test_asynctransaction_get_failure():
    client = _make_client()
    transaction = _make_async_transaction(client)
    ref_or_query = object()
    with pytest.raises(ValueError):
        await transaction.get(ref_or_query)


def _make_async_transactional(*args, **kwargs):
    from google.cloud.firestore_v1.async_transaction import _AsyncTransactional

    return _AsyncTransactional(*args, **kwargs)


def test_asynctransactional_constructor():
    wrapped = _make_async_transactional(mock.sentinel.callable_)
    assert wrapped.to_wrap is mock.sentinel.callable_
    assert wrapped.current_id is None
    assert wrapped.retry_id is None


@pytest.mark.asyncio
async def test_asynctransactional__pre_commit_success():
    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"totes-began"
    transaction = _make_transaction(txn_id)
    result = await wrapped._pre_commit(transaction, "pos", key="word")
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


@pytest.mark.asyncio
async def test_asynctransactional__pre_commit_retry_id_already_set_success():
    from google.cloud.firestore_v1.types import common

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)
    txn_id1 = b"already-set"
    wrapped.retry_id = txn_id1

    txn_id2 = b"ok-here-too"
    transaction = _make_transaction(txn_id2)
    result = await wrapped._pre_commit(transaction)
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


@pytest.mark.asyncio
async def test_asynctransactional___call__success_first_attempt():
    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"whole-enchilada"
    transaction = _make_transaction(txn_id)
    result = await wrapped(transaction, "a", b="c")
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


@pytest.mark.asyncio
async def test_asynctransactional___call__success_second_attempt():
    from google.api_core import exceptions

    from google.cloud.firestore_v1.types import common, firestore, write

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"whole-enchilada"
    transaction = _make_transaction(txn_id)

    # Actually force the ``commit`` to fail on first / succeed on second.
    exc = exceptions.Aborted("Contention junction.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = [
        exc,
        firestore.CommitResponse(write_results=[write.WriteResult()]),
    ]

    # Call the __call__-able ``wrapped``.
    result = await wrapped(transaction, "a", b="c")
    assert result is mock.sentinel.result

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    wrapped_call = mock.call(transaction, "a", b="c")
    assert to_wrap.mock_calls == [wrapped_call, wrapped_call]
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


@pytest.mark.parametrize("max_attempts", [1, 5])
@pytest.mark.asyncio
async def test_asynctransactional___call__failure_max_attempts(max_attempts):
    """
    rasie retryable error and exhause max_attempts
    """
    from google.api_core import exceptions

    from google.cloud.firestore_v1.async_transaction import _EXCEED_ATTEMPTS_TEMPLATE
    from google.cloud.firestore_v1.types import common

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"attempt_exhaustion"
    transaction = _make_transaction(txn_id, max_attempts=max_attempts)

    # Actually force the ``commit`` to fail.
    exc = exceptions.Aborted("Contention just once.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    # Call the __call__-able ``wrapped``.
    with pytest.raises(ValueError) as exc_info:
        await wrapped(transaction, "here", there=1.5)

    err_msg = _EXCEED_ATTEMPTS_TEMPLATE.format(transaction._max_attempts)
    assert exc_info.value.args == (err_msg,)
    # should retain cause exception
    assert exc_info.value.__cause__ == exc

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    assert to_wrap.call_count == max_attempts
    to_wrap.assert_called_with(transaction, "here", there=1.5)
    assert firestore_api.begin_transaction.call_count == max_attempts
    options_ = common.TransactionOptions(
        read_write=common.TransactionOptions.ReadWrite(retry_transaction=txn_id)
    )
    expected_calls = [
        mock.call(
            request={
                "database": transaction._client._database_string,
                "options": None if i == 0 else options_,
            },
            metadata=transaction._client._rpc_metadata,
        )
        for i in range(max_attempts)
    ]
    assert firestore_api.begin_transaction.call_args_list == expected_calls
    assert firestore_api.commit.call_count == max_attempts
    firestore_api.commit.assert_called_with(
        request={
            "database": transaction._client._database_string,
            "writes": [],
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )
    firestore_api.rollback.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "transaction": txn_id,
        },
        metadata=transaction._client._rpc_metadata,
    )


@pytest.mark.parametrize("max_attempts", [1, 5])
@pytest.mark.asyncio
async def test_asynctransactional___call__failure_readonly(max_attempts):
    """
    readonly transaction should never retry
    """
    from google.api_core import exceptions

    from google.cloud.firestore_v1.types import common

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"read_only_fail"
    transaction = _make_transaction(txn_id, max_attempts=max_attempts, read_only=True)

    # Actually force the ``commit`` to fail.
    exc = exceptions.Aborted("Contention just once.")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    # Call the __call__-able ``wrapped``.
    with pytest.raises(exceptions.Aborted) as exc_info:
        await wrapped(transaction, "here", there=1.5)

    assert exc_info.value == exc

    assert transaction._id is None
    assert wrapped.current_id == txn_id
    assert wrapped.retry_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "here", there=1.5)
    firestore_api.begin_transaction.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "options": common.TransactionOptions(
                read_only=common.TransactionOptions.ReadOnly()
            ),
        },
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


@pytest.mark.parametrize("max_attempts", [1, 5])
@pytest.mark.asyncio
async def test_asynctransactional___call__failure_with_non_retryable(max_attempts):
    """
    call fails due to an exception that is not retryable.
    Should rollback raise immediately
    """
    from google.api_core import exceptions

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"non_retryable"
    transaction = _make_transaction(txn_id, max_attempts=max_attempts)

    # Actually force the ``commit`` to fail.
    exc = exceptions.InvalidArgument("non retryable")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc

    # Call the __call__-able ``wrapped``.
    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        await wrapped(transaction, "here", there=1.5)

    assert exc_info.value == exc

    assert transaction._id is None
    assert wrapped.current_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "here", there=1.5)
    firestore_api.begin_transaction.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "options": None,
        },
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


@pytest.mark.asyncio
async def test_asynctransactional___call__failure_with_rollback_failure():
    """
    Test second failure as part of rollback
    should maintain first failure as __context__
    """
    from google.api_core import exceptions

    to_wrap = AsyncMock(return_value=mock.sentinel.result, spec=[])
    wrapped = _make_async_transactional(to_wrap)

    txn_id = b"non_retryable"
    transaction = _make_transaction(txn_id, max_attempts=1)

    # Actually force the ``commit`` to fail.
    exc = exceptions.InvalidArgument("first error")
    firestore_api = transaction._client._firestore_api
    firestore_api.commit.side_effect = exc
    # also force a second error on rollback
    rb_exc = exceptions.InternalServerError("second error")
    firestore_api.rollback.side_effect = rb_exc

    # Call the __call__-able ``wrapped``.
    # should raise second error with first error as __context__
    with pytest.raises(exceptions.InternalServerError) as exc_info:
        await wrapped(transaction, "here", there=1.5)

    assert exc_info.value == rb_exc
    assert exc_info.value.__context__ == exc

    assert transaction._id is None
    assert wrapped.current_id == txn_id

    # Verify mocks.
    to_wrap.assert_called_once_with(transaction, "here", there=1.5)
    firestore_api.begin_transaction.assert_called_once_with(
        request={
            "database": transaction._client._database_string,
            "options": None,
        },
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


def test_async_transactional_factory():
    from google.cloud.firestore_v1.async_transaction import (
        _AsyncTransactional,
        async_transactional,
    )

    wrapped = async_transactional(mock.sentinel.callable_)
    assert isinstance(wrapped, _AsyncTransactional)
    assert wrapped.to_wrap is mock.sentinel.callable_


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_client(project="feral-tom-cat"):
    from google.cloud.firestore_v1.client import Client

    credentials = _make_credentials()
    return Client(project=project, credentials=credentials)


def _make_transaction(txn_id, **txn_kwargs):
    from google.protobuf import empty_pb2

    from google.cloud.firestore_v1.async_transaction import AsyncTransaction
    from google.cloud.firestore_v1.types import firestore, write

    # Create a fake GAPIC ...
    firestore_api = AsyncMock()
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

    return AsyncTransaction(client, **txn_kwargs)
