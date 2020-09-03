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
import mock
import pytest

from google.api_core import exceptions
from google.api_core import grpc_helpers
import google.auth.credentials
from google.longrunning import operations_pb2


def test__patch_callable_name():
    callable = mock.Mock(spec=["__class__"])
    callable.__class__ = mock.Mock(spec=["__name__"])
    callable.__class__.__name__ = "TestCallable"

    grpc_helpers._patch_callable_name(callable)

    assert callable.__name__ == "TestCallable"


def test__patch_callable_name_no_op():
    callable = mock.Mock(spec=["__name__"])
    callable.__name__ = "test_callable"

    grpc_helpers._patch_callable_name(callable)

    assert callable.__name__ == "test_callable"


class RpcErrorImpl(grpc.RpcError, grpc.Call):
    def __init__(self, code):
        super(RpcErrorImpl, self).__init__()
        self._code = code

    def code(self):
        return self._code

    def details(self):
        return None


def test_wrap_unary_errors():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)
    callable_ = mock.Mock(spec=["__call__"], side_effect=grpc_error)

    wrapped_callable = grpc_helpers._wrap_unary_errors(callable_)

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        wrapped_callable(1, 2, three="four")

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


def test_wrap_stream_okay():
    expected_responses = [1, 2, 3]
    callable_ = mock.Mock(spec=["__call__"], return_value=iter(expected_responses))

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)

    got_iterator = wrapped_callable(1, 2, three="four")

    responses = list(got_iterator)

    callable_.assert_called_once_with(1, 2, three="four")
    assert responses == expected_responses


def test_wrap_stream_prefetch_disabled():
    responses = [1, 2, 3]
    iter_responses = iter(responses)
    callable_ = mock.Mock(spec=["__call__"], return_value=iter_responses)
    callable_._prefetch_first_result_ = False

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)
    wrapped_callable(1, 2, three="four")

    assert list(iter_responses) == responses  # no items should have been pre-fetched
    callable_.assert_called_once_with(1, 2, three="four")


def test_wrap_stream_iterable_iterface():
    response_iter = mock.create_autospec(grpc.Call, instance=True)
    callable_ = mock.Mock(spec=["__call__"], return_value=response_iter)

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)

    got_iterator = wrapped_callable()

    callable_.assert_called_once_with()

    # Check each aliased method in the grpc.Call interface
    got_iterator.add_callback(mock.sentinel.callback)
    response_iter.add_callback.assert_called_once_with(mock.sentinel.callback)

    got_iterator.cancel()
    response_iter.cancel.assert_called_once_with()

    got_iterator.code()
    response_iter.code.assert_called_once_with()

    got_iterator.details()
    response_iter.details.assert_called_once_with()

    got_iterator.initial_metadata()
    response_iter.initial_metadata.assert_called_once_with()

    got_iterator.is_active()
    response_iter.is_active.assert_called_once_with()

    got_iterator.time_remaining()
    response_iter.time_remaining.assert_called_once_with()

    got_iterator.trailing_metadata()
    response_iter.trailing_metadata.assert_called_once_with()


def test_wrap_stream_errors_invocation():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)
    callable_ = mock.Mock(spec=["__call__"], side_effect=grpc_error)

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        wrapped_callable(1, 2, three="four")

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


def test_wrap_stream_empty_iterator():
    expected_responses = []
    callable_ = mock.Mock(spec=["__call__"], return_value=iter(expected_responses))

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)

    got_iterator = wrapped_callable()

    responses = list(got_iterator)

    callable_.assert_called_once_with()
    assert responses == expected_responses


class RpcResponseIteratorImpl(object):
    def __init__(self, iterable):
        self._iterable = iter(iterable)

    def next(self):
        next_item = next(self._iterable)
        if isinstance(next_item, RpcErrorImpl):
            raise next_item
        return next_item

    __next__ = next


def test_wrap_stream_errors_iterator_initialization():
    grpc_error = RpcErrorImpl(grpc.StatusCode.UNAVAILABLE)
    response_iter = RpcResponseIteratorImpl([grpc_error])
    callable_ = mock.Mock(spec=["__call__"], return_value=response_iter)

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)

    with pytest.raises(exceptions.ServiceUnavailable) as exc_info:
        wrapped_callable(1, 2, three="four")

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


def test_wrap_stream_errors_during_iteration():
    grpc_error = RpcErrorImpl(grpc.StatusCode.UNAVAILABLE)
    response_iter = RpcResponseIteratorImpl([1, grpc_error])
    callable_ = mock.Mock(spec=["__call__"], return_value=response_iter)

    wrapped_callable = grpc_helpers._wrap_stream_errors(callable_)
    got_iterator = wrapped_callable(1, 2, three="four")
    next(got_iterator)

    with pytest.raises(exceptions.ServiceUnavailable) as exc_info:
        next(got_iterator)

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


@mock.patch("google.api_core.grpc_helpers._wrap_unary_errors")
def test_wrap_errors_non_streaming(wrap_unary_errors):
    callable_ = mock.create_autospec(grpc.UnaryUnaryMultiCallable)

    result = grpc_helpers.wrap_errors(callable_)

    assert result == wrap_unary_errors.return_value
    wrap_unary_errors.assert_called_once_with(callable_)


@mock.patch("google.api_core.grpc_helpers._wrap_stream_errors")
def test_wrap_errors_streaming(wrap_stream_errors):
    callable_ = mock.create_autospec(grpc.UnaryStreamMultiCallable)

    result = grpc_helpers.wrap_errors(callable_)

    assert result == wrap_stream_errors.return_value
    wrap_stream_errors.assert_called_once_with(callable_)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit(grpc_secure_channel, default, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target)

    assert channel is grpc_secure_channel.return_value
    default.assert_called_once_with(scopes=None)
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_ssl_creds(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"

    ssl_creds = grpc.ssl_channel_credentials()

    grpc_helpers.create_channel(target, ssl_credentials=ssl_creds)

    default.assert_called_once_with(scopes=None)
    composite_creds_call.assert_called_once_with(ssl_creds, mock.ANY)
    composite_creds = composite_creds_call.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    return_value=(mock.sentinel.credentials, mock.sentinel.projet),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_scopes(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target, scopes=["one", "two"])

    assert channel is grpc_secure_channel.return_value
    default.assert_called_once_with(scopes=["one", "two"])
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


def test_create_channel_explicit_with_duplicate_credentials():
    target = "example.com:443"

    with pytest.raises(exceptions.DuplicateCredentialArgs):
        grpc_helpers.create_channel(
            target,
            credentials_file="credentials.json",
            credentials=mock.sentinel.credentials
        )


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("google.auth.credentials.with_scopes_if_required")
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit(grpc_secure_channel, auth_creds, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target, credentials=mock.sentinel.credentials)

    auth_creds.assert_called_once_with(mock.sentinel.credentials, None)
    assert channel is grpc_secure_channel.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit_scoped(grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    scopes = ["1", "2"]
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    channel = grpc_helpers.create_channel(
        target, credentials=credentials, scopes=scopes
    )

    credentials.with_scopes.assert_called_once_with(scopes)
    assert channel is grpc_secure_channel.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit_with_quota_project(grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(google.auth.credentials.CredentialsWithQuotaProject, instance=True)

    channel = grpc_helpers.create_channel(
        target,
        credentials=credentials,
        quota_project_id="project-foo"
    )

    credentials.with_quota_project.assert_called_once_with("project-foo")

    assert channel is grpc_secure_channel.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    return_value=(mock.sentinel.credentials, mock.sentinel.project)
)
def test_create_channel_with_credentials_file(load_credentials_from_file, grpc_secure_channel, composite_creds_call):
    target = "example.com:443"

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        target, credentials_file=credentials_file
    )

    google.auth.load_credentials_from_file.assert_called_once_with(credentials_file, scopes=None)

    assert channel is grpc_secure_channel.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    return_value=(mock.sentinel.credentials, mock.sentinel.project)
)
def test_create_channel_with_credentials_file_and_scopes(load_credentials_from_file, grpc_secure_channel, composite_creds_call):
    target = "example.com:443"
    scopes = ["1", "2"]

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        target, credentials_file=credentials_file, scopes=scopes
    )

    google.auth.load_credentials_from_file.assert_called_once_with(credentials_file, scopes=scopes)
    assert channel is grpc_secure_channel.return_value
    if grpc_helpers.HAS_GRPC_GCP:
        grpc_secure_channel.assert_called_once_with(target, composite_creds, None)
    else:
        grpc_secure_channel.assert_called_once_with(target, composite_creds)


@pytest.mark.skipif(
    not grpc_helpers.HAS_GRPC_GCP, reason="grpc_gcp module not available"
)
@mock.patch("grpc_gcp.secure_channel")
def test_create_channel_with_grpc_gcp(grpc_gcp_secure_channel):
    target = "example.com:443"
    scopes = ["test_scope"]

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    grpc_helpers.create_channel(target, credentials=credentials, scopes=scopes)
    grpc_gcp_secure_channel.assert_called()
    credentials.with_scopes.assert_called_once_with(scopes)


@pytest.mark.skipif(grpc_helpers.HAS_GRPC_GCP, reason="grpc_gcp module not available")
@mock.patch("grpc.secure_channel")
def test_create_channel_without_grpc_gcp(grpc_secure_channel):
    target = "example.com:443"
    scopes = ["test_scope"]

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    grpc_helpers.create_channel(target, credentials=credentials, scopes=scopes)
    grpc_secure_channel.assert_called()
    credentials.with_scopes.assert_called_once_with(scopes)


class TestChannelStub(object):
    def test_single_response(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")
        expected_response = operations_pb2.Operation(name="moop")

        channel.GetOperation.response = expected_response

        response = stub.GetOperation(expected_request)

        assert response == expected_response
        assert channel.requests == [("GetOperation", expected_request)]
        assert channel.GetOperation.requests == [expected_request]

    def test_no_response(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")

        with pytest.raises(ValueError) as exc_info:
            stub.GetOperation(expected_request)

        assert exc_info.match("GetOperation")

    def test_missing_method(self):
        channel = grpc_helpers.ChannelStub()

        with pytest.raises(AttributeError):
            channel.DoesNotExist.response

    def test_exception_response(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")

        channel.GetOperation.response = RuntimeError()

        with pytest.raises(RuntimeError):
            stub.GetOperation(expected_request)

    def test_callable_response(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")
        expected_response = operations_pb2.Operation(name="moop")

        on_get_operation = mock.Mock(spec=("__call__",), return_value=expected_response)

        channel.GetOperation.response = on_get_operation

        response = stub.GetOperation(expected_request)

        assert response == expected_response
        on_get_operation.assert_called_once_with(expected_request)

    def test_multiple_responses(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")
        expected_responses = [
            operations_pb2.Operation(name="foo"),
            operations_pb2.Operation(name="bar"),
            operations_pb2.Operation(name="baz"),
        ]

        channel.GetOperation.responses = iter(expected_responses)

        response1 = stub.GetOperation(expected_request)
        response2 = stub.GetOperation(expected_request)
        response3 = stub.GetOperation(expected_request)

        assert response1 == expected_responses[0]
        assert response2 == expected_responses[1]
        assert response3 == expected_responses[2]
        assert channel.requests == [("GetOperation", expected_request)] * 3
        assert channel.GetOperation.requests == [expected_request] * 3

        with pytest.raises(StopIteration):
            stub.GetOperation(expected_request)

    def test_multiple_responses_and_single_response_error(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        channel.GetOperation.responses = []
        channel.GetOperation.response = mock.sentinel.response

        with pytest.raises(ValueError):
            stub.GetOperation(operations_pb2.GetOperationRequest())

    def test_call_info(self):
        channel = grpc_helpers.ChannelStub()
        stub = operations_pb2.OperationsStub(channel)
        expected_request = operations_pb2.GetOperationRequest(name="meep")
        expected_response = operations_pb2.Operation(name="moop")
        expected_metadata = [("red", "blue"), ("two", "shoe")]
        expected_credentials = mock.sentinel.credentials
        channel.GetOperation.response = expected_response

        response = stub.GetOperation(
            expected_request,
            timeout=42,
            metadata=expected_metadata,
            credentials=expected_credentials,
        )

        assert response == expected_response
        assert channel.requests == [("GetOperation", expected_request)]
        assert channel.GetOperation.calls == [
            (expected_request, 42, expected_metadata, expected_credentials)
        ]

    def test_unary_unary(self):
        channel = grpc_helpers.ChannelStub()
        method_name = "GetOperation"
        callable_stub = channel.unary_unary(method_name)
        assert callable_stub._method == method_name
        assert callable_stub._channel == channel

    def test_unary_stream(self):
        channel = grpc_helpers.ChannelStub()
        method_name = "GetOperation"
        callable_stub = channel.unary_stream(method_name)
        assert callable_stub._method == method_name
        assert callable_stub._channel == channel

    def test_stream_unary(self):
        channel = grpc_helpers.ChannelStub()
        method_name = "GetOperation"
        callable_stub = channel.stream_unary(method_name)
        assert callable_stub._method == method_name
        assert callable_stub._channel == channel

    def test_stream_stream(self):
        channel = grpc_helpers.ChannelStub()
        method_name = "GetOperation"
        callable_stub = channel.stream_stream(method_name)
        assert callable_stub._method == method_name
        assert callable_stub._channel == channel

    def test_subscribe_unsubscribe(self):
        channel = grpc_helpers.ChannelStub()
        assert channel.subscribe(None) is None
        assert channel.unsubscribe(None) is None

    def test_close(self):
        channel = grpc_helpers.ChannelStub()
        assert channel.close() is None
