# Copyright 2017 Google LLC
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

import grpc
from grpc.experimental import aio
import mock
import pytest

from google.api_core import exceptions
from google.api_core import grpc_helpers_async
import google.auth.credentials


class RpcErrorImpl(grpc.RpcError, grpc.Call):
    def __init__(self, code):
        super(RpcErrorImpl, self).__init__()
        self._code = code

    def code(self):
        return self._code

    def details(self):
        return None


@pytest.mark.asyncio
async def test_wrap_unary_errors():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)
    callable_ = mock.AsyncMock(spec=["__call__"], side_effect=grpc_error)

    wrapped_callable = grpc_helpers_async._wrap_unary_errors(callable_)

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        await wrapped_callable(1, 2, three="four")

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


@pytest.mark.asyncio
async def test_common_methods_in_wrapped_call():
    mock_call = mock.Mock(aio.UnaryUnaryCall, autospec=True)
    wrapped_call = grpc_helpers_async._WrappedUnaryUnaryCall().with_call(mock_call)

    await wrapped_call.initial_metadata()
    assert mock_call.initial_metadata.call_count == 1

    await wrapped_call.trailing_metadata()
    assert mock_call.trailing_metadata.call_count == 1

    await wrapped_call.code()
    assert mock_call.code.call_count == 1

    await wrapped_call.details()
    assert mock_call.details.call_count == 1

    wrapped_call.cancelled()
    assert mock_call.cancelled.call_count == 1

    wrapped_call.done()
    assert mock_call.done.call_count == 1

    wrapped_call.time_remaining()
    assert mock_call.time_remaining.call_count == 1

    wrapped_call.cancel()
    assert mock_call.cancel.call_count == 1

    callback = mock.sentinel.callback
    wrapped_call.add_done_callback(callback)
    mock_call.add_done_callback.assert_called_once_with(callback)

    await wrapped_call.wait_for_connection()
    assert mock_call.wait_for_connection.call_count == 1


@pytest.mark.asyncio
async def test_wrap_stream_errors_unary_stream():
    mock_call = mock.Mock(aio.UnaryStreamCall, autospec=True)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    await wrapped_callable(1, 2, three="four")
    multicallable.assert_called_once_with(1, 2, three="four")
    assert mock_call.wait_for_connection.call_count == 1


@pytest.mark.asyncio
async def test_wrap_stream_errors_stream_unary():
    mock_call = mock.Mock(aio.StreamUnaryCall, autospec=True)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    await wrapped_callable(1, 2, three="four")
    multicallable.assert_called_once_with(1, 2, three="four")
    assert mock_call.wait_for_connection.call_count == 1


@pytest.mark.asyncio
async def test_wrap_stream_errors_stream_stream():
    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    await wrapped_callable(1, 2, three="four")
    multicallable.assert_called_once_with(1, 2, three="four")
    assert mock_call.wait_for_connection.call_count == 1


@pytest.mark.asyncio
async def test_wrap_stream_errors_type_error():
    mock_call = mock.Mock()
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    with pytest.raises(TypeError):
        await wrapped_callable()


@pytest.mark.asyncio
async def test_wrap_stream_errors_raised():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)
    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    mock_call.wait_for_connection = mock.AsyncMock(side_effect=[grpc_error])
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    with pytest.raises(exceptions.InvalidArgument):
        await wrapped_callable()
    assert mock_call.wait_for_connection.call_count == 1


@pytest.mark.asyncio
async def test_wrap_stream_errors_read():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)

    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    mock_call.read = mock.AsyncMock(side_effect=grpc_error)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    wrapped_call = await wrapped_callable(1, 2, three="four")
    multicallable.assert_called_once_with(1, 2, three="four")
    assert mock_call.wait_for_connection.call_count == 1

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        await wrapped_call.read()
    assert exc_info.value.response == grpc_error


@pytest.mark.asyncio
async def test_wrap_stream_errors_aiter():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)

    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    mocked_aiter = mock.Mock(spec=['__anext__'])
    mocked_aiter.__anext__ = mock.AsyncMock(side_effect=[mock.sentinel.response, grpc_error])
    mock_call.__aiter__ = mock.Mock(return_value=mocked_aiter)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)
    wrapped_call = await wrapped_callable()

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        async for response in wrapped_call:
            assert response == mock.sentinel.response
    assert exc_info.value.response == grpc_error


@pytest.mark.asyncio
async def test_wrap_stream_errors_aiter_non_rpc_error():
    non_grpc_error = TypeError('Not a gRPC error')

    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    mocked_aiter = mock.Mock(spec=['__anext__'])
    mocked_aiter.__anext__ = mock.AsyncMock(side_effect=[mock.sentinel.response, non_grpc_error])
    mock_call.__aiter__ = mock.Mock(return_value=mocked_aiter)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)
    wrapped_call = await wrapped_callable()

    with pytest.raises(TypeError) as exc_info:
        async for response in wrapped_call:
            assert response == mock.sentinel.response
    assert exc_info.value == non_grpc_error


@pytest.mark.asyncio
async def test_wrap_stream_errors_aiter_called_multiple_times():
    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)
    wrapped_call = await wrapped_callable()

    assert wrapped_call.__aiter__() == wrapped_call.__aiter__()


@pytest.mark.asyncio
async def test_wrap_stream_errors_write():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)

    mock_call = mock.Mock(aio.StreamStreamCall, autospec=True)
    mock_call.write = mock.AsyncMock(side_effect=[None, grpc_error])
    mock_call.done_writing = mock.AsyncMock(side_effect=[None, grpc_error])
    multicallable = mock.Mock(return_value=mock_call)

    wrapped_callable = grpc_helpers_async._wrap_stream_errors(multicallable)

    wrapped_call = await wrapped_callable()

    await wrapped_call.write(mock.sentinel.request)
    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        await wrapped_call.write(mock.sentinel.request)
    assert mock_call.write.call_count == 2
    assert exc_info.value.response == grpc_error

    await wrapped_call.done_writing()
    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        await wrapped_call.done_writing()
    assert mock_call.done_writing.call_count == 2
    assert exc_info.value.response == grpc_error


@mock.patch("google.api_core.grpc_helpers_async._wrap_unary_errors")
def test_wrap_errors_non_streaming(wrap_unary_errors):
    callable_ = mock.create_autospec(aio.UnaryUnaryMultiCallable)

    result = grpc_helpers_async.wrap_errors(callable_)

    assert result == wrap_unary_errors.return_value
    wrap_unary_errors.assert_called_once_with(callable_)


@mock.patch("google.api_core.grpc_helpers_async._wrap_stream_errors")
def test_wrap_errors_streaming(wrap_stream_errors):
    callable_ = mock.create_autospec(aio.UnaryStreamMultiCallable)

    result = grpc_helpers_async.wrap_errors(callable_)

    assert result == wrap_stream_errors.return_value
    wrap_stream_errors.assert_called_once_with(callable_)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_implicit(grpc_secure_channel, default, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers_async.create_channel(target)

    assert channel is grpc_secure_channel.return_value
    default.assert_called_once_with(scopes=None)
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_implicit_with_ssl_creds(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"

    ssl_creds = grpc.ssl_channel_credentials()

    grpc_helpers_async.create_channel(target, ssl_credentials=ssl_creds)

    default.assert_called_once_with(scopes=None)
    composite_creds_call.assert_called_once_with(ssl_creds, mock.ANY)
    composite_creds = composite_creds_call.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_implicit_with_scopes(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers_async.create_channel(target, scopes=["one", "two"])

    assert channel is grpc_secure_channel.return_value
    default.assert_called_once_with(scopes=["one", "two"])
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


def test_create_channel_explicit_with_duplicate_credentials():
    target = "example:443"

    with pytest.raises(exceptions.DuplicateCredentialArgs) as excinfo:
        grpc_helpers_async.create_channel(
            target,
            credentials_file="credentials.json",
            credentials=mock.sentinel.credentials
        )

    assert "mutually exclusive" in str(excinfo.value)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("google.auth.credentials.with_scopes_if_required")
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_explicit(grpc_secure_channel, auth_creds, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers_async.create_channel(target, credentials=mock.sentinel.credentials)

    auth_creds.assert_called_once_with(mock.sentinel.credentials, None)
    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_explicit_scoped(grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    scopes = ["1", "2"]
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    channel = grpc_helpers_async.create_channel(
        target, credentials=credentials, scopes=scopes
    )

    credentials.with_scopes.assert_called_once_with(scopes)
    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_explicit_with_quota_project(grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(google.auth.credentials.CredentialsWithQuotaProject, instance=True)

    channel = grpc_helpers_async.create_channel(
        target, credentials=credentials, quota_project_id="project-foo"
    )

    credentials.with_quota_project.assert_called_once_with("project-foo")
    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.experimental.aio.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    return_value=(mock.sentinel.credentials, mock.sentinel.project)
)
def test_create_channnel_with_credentials_file(load_credentials_from_file, grpc_secure_channel, composite_creds_call):
    target = "example.com:443"

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers_async.create_channel(
        target, credentials_file=credentials_file
    )

    google.auth.load_credentials_from_file.assert_called_once_with(credentials_file, scopes=None)
    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.experimental.aio.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    return_value=(mock.sentinel.credentials, mock.sentinel.project)
)
def test_create_channel_with_credentials_file_and_scopes(load_credentials_from_file, grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    scopes = ["1", "2"]

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers_async.create_channel(
        target, credentials_file=credentials_file, scopes=scopes
    )

    google.auth.load_credentials_from_file.assert_called_once_with(credentials_file, scopes=scopes)
    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(target, composite_creds)


@pytest.mark.skipif(grpc_helpers_async.HAS_GRPC_GCP, reason="grpc_gcp module not available")
@mock.patch("grpc.experimental.aio.secure_channel")
def test_create_channel_without_grpc_gcp(grpc_secure_channel):
    target = "example.com:443"
    scopes = ["test_scope"]

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    grpc_helpers_async.create_channel(target, credentials=credentials, scopes=scopes)
    grpc_secure_channel.assert_called()
    credentials.with_scopes.assert_called_once_with(scopes)


@pytest.mark.asyncio
async def test_fake_stream_unary_call():
    fake_call = grpc_helpers_async.FakeStreamUnaryCall()
    await fake_call.wait_for_connection()
    response = await fake_call
    assert fake_call.response == response
