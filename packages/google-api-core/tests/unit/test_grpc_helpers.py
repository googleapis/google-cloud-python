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

import copy
import gc
import inspect
import threading
import time
import weakref
from concurrent import futures
from unittest import mock

import pytest

from ..helpers import warn_deprecated_credentials_file

try:
    import grpc
except ImportError:  # pragma: NO COVER
    pytest.skip("No GRPC", allow_module_level=True)

import google.auth.credentials
from google.longrunning import operations_pb2

from google.api_core import exceptions, grpc_helpers


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

    def trailing_metadata(self):
        return None


def test_wrap_unary_errors():
    grpc_error = RpcErrorImpl(grpc.StatusCode.INVALID_ARGUMENT)
    callable_ = mock.Mock(spec=["__call__"], side_effect=grpc_error)

    wrapped_callable = grpc_helpers._wrap_unary_errors(callable_)

    with pytest.raises(exceptions.InvalidArgument) as exc_info:
        wrapped_callable(1, 2, three="four")

    callable_.assert_called_once_with(1, 2, three="four")
    assert exc_info.value.response == grpc_error


class Test_StreamingResponseIterator:
    @staticmethod
    def _make_wrapped(*items):
        return iter(items)

    @staticmethod
    def _make_one(wrapped, **kw):
        return grpc_helpers._StreamingResponseIterator(wrapped, **kw)

    def test_ctor_defaults(self):
        wrapped = self._make_wrapped("a", "b", "c")
        iterator = self._make_one(wrapped)
        assert iterator._stored_first_result == "a"
        assert list(wrapped) == ["b", "c"]

    def test_ctor_explicit(self):
        wrapped = self._make_wrapped("a", "b", "c")
        iterator = self._make_one(wrapped, prefetch_first_result=False)
        assert getattr(iterator, "_stored_first_result", self) is self
        assert list(wrapped) == ["a", "b", "c"]

    def test_ctor_w_rpc_error_on_prefetch(self):
        wrapped = mock.MagicMock()
        wrapped.__next__.side_effect = grpc.RpcError()

        with pytest.raises(grpc.RpcError):
            self._make_one(wrapped)

    def test___iter__(self):
        wrapped = self._make_wrapped("a", "b", "c")
        iterator = self._make_one(wrapped)
        assert iter(iterator) is iterator

    def test___next___w_cached_first_result(self):
        wrapped = self._make_wrapped("a", "b", "c")
        iterator = self._make_one(wrapped)
        assert next(iterator) == "a"
        iterator = self._make_one(wrapped, prefetch_first_result=False)
        assert next(iterator) == "b"
        assert next(iterator) == "c"

    def test___next___wo_cached_first_result(self):
        wrapped = self._make_wrapped("a", "b", "c")
        iterator = self._make_one(wrapped, prefetch_first_result=False)
        assert next(iterator) == "a"
        assert next(iterator) == "b"
        assert next(iterator) == "c"

    def test___next___w_rpc_error(self):
        wrapped = mock.MagicMock()
        wrapped.__next__.side_effect = grpc.RpcError()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        with pytest.raises(exceptions.GoogleAPICallError):
            next(iterator)

    def test_add_callback(self):
        wrapped = mock.MagicMock()
        callback = mock.Mock(spec={})
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.add_callback(callback) is wrapped.add_callback.return_value

        wrapped.add_callback.assert_called_once_with(callback)

    def test_cancel(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.cancel() is wrapped.cancel.return_value

        wrapped.cancel.assert_called_once_with()

    def test_code(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.code() is wrapped.code.return_value

        wrapped.code.assert_called_once_with()

    def test_details(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.details() is wrapped.details.return_value

        wrapped.details.assert_called_once_with()

    def test_initial_metadata(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.initial_metadata() is wrapped.initial_metadata.return_value

        wrapped.initial_metadata.assert_called_once_with()

    def test_is_active(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.is_active() is wrapped.is_active.return_value

        wrapped.is_active.assert_called_once_with()

    def test_time_remaining(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.time_remaining() is wrapped.time_remaining.return_value

        wrapped.time_remaining.assert_called_once_with()

    def test_trailing_metadata(self):
        wrapped = mock.MagicMock()
        iterator = self._make_one(wrapped, prefetch_first_result=False)

        assert iterator.trailing_metadata() is wrapped.trailing_metadata.return_value

        wrapped.trailing_metadata.assert_called_once_with()


class TestGrpcStream(Test_StreamingResponseIterator):
    @staticmethod
    def _make_one(wrapped, **kw):
        return grpc_helpers.GrpcStream(wrapped, **kw)

    def test_grpc_stream_attributes(self):
        """
        Should be both a grpc.Call and an iterable
        """
        call = self._make_one(None)
        assert isinstance(call, grpc.Call)
        # should implement __iter__
        assert hasattr(call, "__iter__")
        it = call.__iter__()
        assert hasattr(it, "__next__")


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


def test_wrap_stream_iterable_interface():
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


@pytest.mark.parametrize(
    "attempt_direct_path,target,expected_target",
    [
        (None, "example.com:443", "example.com:443"),
        (False, "example.com:443", "example.com:443"),
        (True, "example.com:443", "google-c2p:///example.com"),
        (True, "dns:///example.com", "google-c2p:///example.com"),
        (True, "another-c2p:///example.com", "another-c2p:///example.com"),
    ],
)
@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
    attempt_direct_path,
    target,
    expected_target,
):
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        target,
        compression=grpc.Compression.Gzip,
        attempt_direct_path=attempt_direct_path,
    )

    assert channel is grpc_secure_channel.return_value

    google_auth_default.assert_called_once_with(scopes=None, default_scopes=None)

    grpc_secure_channel.assert_called_once_with(
        expected_target, composite_creds, compression=grpc.Compression.Gzip
    )


@pytest.mark.parametrize(
    "attempt_direct_path,target, expected_target",
    [
        (None, "example.com:443", "example.com:443"),
        (False, "example.com:443", "example.com:443"),
        (True, "example.com:443", "google-c2p:///example.com"),
        (True, "dns:///example.com", "google-c2p:///example.com"),
        (True, "another-c2p:///example.com", "another-c2p:///example.com"),
    ],
)
@mock.patch("google.auth.transport.grpc.AuthMetadataPlugin", autospec=True)
@mock.patch(
    "google.auth.transport.requests.Request",
    autospec=True,
    return_value=mock.sentinel.Request,
)
@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_default_host(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
    request,
    auth_metadata_plugin,
    attempt_direct_path,
    target,
    expected_target,
):
    default_host = "example.com"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        target, default_host=default_host, attempt_direct_path=attempt_direct_path
    )

    assert channel is grpc_secure_channel.return_value

    google_auth_default.assert_called_once_with(scopes=None, default_scopes=None)
    assert auth_metadata_plugin.call_count == 1
    assert auth_metadata_plugin.call_args.args == (
        mock.sentinel.credentials,
        mock.sentinel.Request,
    )
    assert auth_metadata_plugin.call_args.kwargs["default_host"] == default_host
    # google-auth >= 2.56.3 supports suppress_metrics_header; older versions omit it during fallback
    if "suppress_metrics_header" in auth_metadata_plugin.call_args.kwargs:
        assert auth_metadata_plugin.call_args.kwargs["suppress_metrics_header"] is True

    grpc_secure_channel.assert_called_once_with(
        expected_target, composite_creds, compression=None
    )


@pytest.mark.parametrize(
    "attempt_direct_path",
    [
        None,
        False,
    ],
)
@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_ssl_creds(
    grpc_secure_channel, default, composite_creds_call, attempt_direct_path
):
    target = "example.com:443"

    ssl_creds = grpc.ssl_channel_credentials()

    grpc_helpers.create_channel(
        target, ssl_credentials=ssl_creds, attempt_direct_path=attempt_direct_path
    )

    default.assert_called_once_with(scopes=None, default_scopes=None)

    composite_creds_call.assert_called_once_with(ssl_creds, mock.ANY)
    composite_creds = composite_creds_call.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


def test_create_channel_implicit_with_ssl_creds_attempt_direct_path_true():
    target = "example.com:443"
    ssl_creds = grpc.ssl_channel_credentials()
    with pytest.raises(
        ValueError, match="Using ssl_credentials with Direct Path is not supported"
    ):
        grpc_helpers.create_channel(
            target, ssl_credentials=ssl_creds, attempt_direct_path=True
        )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_scopes(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target, scopes=["one", "two"])

    assert channel is grpc_secure_channel.return_value

    default.assert_called_once_with(scopes=["one", "two"], default_scopes=None)

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_implicit_with_default_scopes(
    grpc_secure_channel, default, composite_creds_call
):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target, default_scopes=["three", "four"])

    assert channel is grpc_secure_channel.return_value

    default.assert_called_once_with(scopes=None, default_scopes=["three", "four"])

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


def test_create_channel_explicit_with_duplicate_credentials():
    target = "example.com:443"

    with pytest.raises(exceptions.DuplicateCredentialArgs):
        with warn_deprecated_credentials_file():
            grpc_helpers.create_channel(
                target,
                credentials_file="credentials.json",
                credentials=mock.sentinel.credentials,
            )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("google.auth.credentials.with_scopes_if_required", autospec=True)
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit(grpc_secure_channel, auth_creds, composite_creds_call):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(target, credentials=mock.sentinel.credentials)

    auth_creds.assert_called_once_with(
        mock.sentinel.credentials, scopes=None, default_scopes=None
    )

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
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

    credentials.with_scopes.assert_called_once_with(scopes, default_scopes=None)

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit_default_scopes(
    grpc_secure_channel, composite_creds_call
):
    target = "example.com:443"
    default_scopes = ["3", "4"]
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    channel = grpc_helpers.create_channel(
        target, credentials=credentials, default_scopes=default_scopes
    )

    credentials.with_scopes.assert_called_once_with(
        scopes=None, default_scopes=default_scopes
    )

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("grpc.secure_channel")
def test_create_channel_explicit_with_quota_project(
    grpc_secure_channel, composite_creds_call
):
    target = "example.com:443"
    composite_creds = composite_creds_call.return_value

    credentials = mock.create_autospec(
        google.auth.credentials.CredentialsWithQuotaProject, instance=True
    )

    channel = grpc_helpers.create_channel(
        target, credentials=credentials, quota_project_id="project-foo"
    )

    credentials.with_quota_project.assert_called_once_with("project-foo")

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("grpc.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
def test_create_channel_with_credentials_file(
    load_credentials_from_file, grpc_secure_channel, composite_creds_call
):
    target = "example.com:443"

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    with warn_deprecated_credentials_file():
        channel = grpc_helpers.create_channel(target, credentials_file=credentials_file)

    google.auth.load_credentials_from_file.assert_called_once_with(
        credentials_file, scopes=None, default_scopes=None
    )

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("grpc.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
def test_create_channel_with_credentials_file_and_scopes(
    load_credentials_from_file, grpc_secure_channel, composite_creds_call
):
    target = "example.com:443"
    scopes = ["1", "2"]

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    with warn_deprecated_credentials_file():
        channel = grpc_helpers.create_channel(
            target, credentials_file=credentials_file, scopes=scopes
        )

    google.auth.load_credentials_from_file.assert_called_once_with(
        credentials_file, scopes=scopes, default_scopes=None
    )

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch("grpc.secure_channel")
@mock.patch(
    "google.auth.load_credentials_from_file",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
def test_create_channel_with_credentials_file_and_default_scopes(
    load_credentials_from_file, grpc_secure_channel, composite_creds_call
):
    target = "example.com:443"
    default_scopes = ["3", "4"]

    credentials_file = "/path/to/credentials/file.json"
    composite_creds = composite_creds_call.return_value

    with warn_deprecated_credentials_file():
        channel = grpc_helpers.create_channel(
            target, credentials_file=credentials_file, default_scopes=default_scopes
        )

    load_credentials_from_file.assert_called_once_with(
        credentials_file, scopes=None, default_scopes=default_scopes
    )

    assert channel is grpc_secure_channel.return_value

    grpc_secure_channel.assert_called_once_with(
        target, composite_creds, compression=None
    )


@mock.patch("grpc.secure_channel")
def test_create_channel_without_grpc_gcp(grpc_secure_channel):
    target = "example.com:443"
    scopes = ["test_scope"]

    credentials = mock.create_autospec(google.auth.credentials.Scoped, instance=True)
    credentials.requires_scopes = True

    grpc_helpers.create_channel(target, credentials=credentials, scopes=scopes)
    grpc_secure_channel.assert_called()

    credentials.with_scopes.assert_called_once_with(scopes, default_scopes=None)


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
        expected_compression = grpc.Compression.NoCompression
        expected_metadata = [("red", "blue"), ("two", "shoe")]
        expected_credentials = mock.sentinel.credentials
        channel.GetOperation.response = expected_response

        response = stub.GetOperation(
            expected_request,
            timeout=42,
            compression=expected_compression,
            metadata=expected_metadata,
            credentials=expected_credentials,
        )

        assert response == expected_response
        assert channel.requests == [("GetOperation", expected_request)]
        assert channel.GetOperation.calls == [
            (
                expected_request,
                42,
                expected_metadata,
                expected_credentials,
                expected_compression,
            )
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


@pytest.mark.parametrize("falsy_interceptors", [None, [], ()])
def test_apply_channel_interceptors_passthrough(falsy_interceptors):
    """Verify that falsy or empty interceptor sequences return the channel unmodified."""
    mock_base_channel = mock.Mock(name="base_channel")
    result = grpc_helpers.apply_channel_interceptors(
        mock_base_channel, falsy_interceptors
    )
    assert result is mock_base_channel


def test_apply_channel_interceptors_grpc_client_interceptors():
    """Verify that standard gRPC ClientInterceptor instances are applied via grpc.intercept_channel."""

    class DummyUnaryInterceptor(grpc.UnaryUnaryClientInterceptor):
        def intercept_unary_unary(self, continuation, client_call_details, request):
            return continuation(client_call_details, request)

    class DummyStreamInterceptor(grpc.StreamStreamClientInterceptor):
        def intercept_stream_stream(
            self, continuation, client_call_details, request_iterator
        ):
            return continuation(client_call_details, request_iterator)

    interceptor1 = DummyUnaryInterceptor()
    interceptor2 = DummyStreamInterceptor()

    mock_base_channel = mock.Mock(name="base_channel")
    mock_chan_after_i2 = mock.Mock(name="chan_after_i2")
    mock_chan_after_i1 = mock.Mock(name="chan_after_i1")

    with mock.patch(
        "grpc.intercept_channel",
        side_effect=[mock_chan_after_i2, mock_chan_after_i1],
    ) as mock_intercept:
        result = grpc_helpers.apply_channel_interceptors(
            mock_base_channel, [interceptor1, interceptor2]
        )

    assert result is mock_chan_after_i1
    assert mock_intercept.call_count == 2
    # Executed in reverse order so interceptor1 is outermost
    mock_intercept.assert_has_calls(
        [
            mock.call(mock_base_channel, interceptor2),
            mock.call(mock_chan_after_i2, interceptor1),
        ]
    )


def test_apply_channel_interceptors_callables():
    """Verify that channel-intercepting callables Callable[[Channel], Channel] are invoked in sequence."""
    mock_base_channel = mock.Mock(name="base_channel")
    mock_chan_1 = mock.Mock(name="chan_1")
    mock_chan_2 = mock.Mock(name="chan_2")

    interceptor1 = mock.Mock(side_effect=lambda ch: mock_chan_2)
    interceptor2 = mock.Mock(side_effect=lambda ch: mock_chan_1)

    result = grpc_helpers.apply_channel_interceptors(
        mock_base_channel, [interceptor1, interceptor2]
    )

    assert result is mock_chan_2
    # Executed in reverse order: interceptor2 runs first on base channel, then interceptor1
    interceptor2.assert_called_once_with(mock_base_channel)
    interceptor1.assert_called_once_with(mock_chan_1)


def test_apply_channel_interceptors_interspersed():
    """Verify that a mixed sequence of gRPC interceptors and interceptor callables are applied."""

    class DummyUnaryInterceptor(grpc.UnaryUnaryClientInterceptor):
        def intercept_unary_unary(self, continuation, client_call_details, request):
            return continuation(client_call_details, request)

    interceptor = DummyUnaryInterceptor()
    mock_base_channel = mock.Mock(name="base_channel")
    mock_chan_after_callable = mock.Mock(name="chan_after_callable")
    mock_chan_after_interceptor = mock.Mock(name="chan_after_interceptor")

    interceptor_callable = mock.Mock(return_value=mock_chan_after_callable)

    with mock.patch(
        "grpc.intercept_channel", return_value=mock_chan_after_interceptor
    ) as mock_intercept:
        result = grpc_helpers.apply_channel_interceptors(
            mock_base_channel, [interceptor, interceptor_callable]
        )

    assert result is mock_chan_after_interceptor
    interceptor_callable.assert_called_once_with(mock_base_channel)
    mock_intercept.assert_called_once_with(mock_chan_after_callable, interceptor)


def test_apply_channel_interceptors_invalid_type_raises():
    """Verify that passing an invalid object that is neither an interceptor nor callable raises TypeError."""
    mock_base_channel = mock.Mock(name="base_channel")
    with pytest.raises(TypeError, match="Expected ClientInterceptor or Callable"):
        grpc_helpers.apply_channel_interceptors(mock_base_channel, [12345])


@pytest.mark.parametrize(
    "env_value,attempt_interconnect,expected_result",
    [
        ("false", True, True),
        ("FALSE", True, True),
        ("0", True, True),
        ("true", False, False),
        ("TRUE", False, False),
        ("1", False, False),
        ("true", None, True),
        ("TRUE", None, True),
        (" True ", None, True),
        ("1", None, True),
        ("yes", None, True),
        ("on", None, True),
        ("false", None, False),
        ("FALSE", None, False),
        (" False ", None, False),
        ("0", None, False),
        ("no", None, False),
        ("off", None, False),
        (None, True, True),
        (None, False, False),
        (None, None, False),
    ],
)
def test__resolve_direct_path_interconnect(
    monkeypatch, env_value, attempt_interconnect, expected_result
):
    if env_value is None:
        monkeypatch.delenv(grpc_helpers._DIRECT_PATH_INTERCONNECT_ENV, raising=False)
    else:
        monkeypatch.setenv(grpc_helpers._DIRECT_PATH_INTERCONNECT_ENV, env_value)
    assert (
        grpc_helpers._resolve_direct_path_interconnect(attempt_interconnect)
        is expected_result
    )


@pytest.mark.parametrize("invalid_env_value", ["invalid", "   ", ""])
def test__resolve_direct_path_interconnect_invalid_raises(
    monkeypatch, invalid_env_value
):
    monkeypatch.setenv(grpc_helpers._DIRECT_PATH_INTERCONNECT_ENV, invalid_env_value)
    with pytest.raises(
        ValueError,
        match=f"Invalid value for {grpc_helpers._DIRECT_PATH_INTERCONNECT_ENV}",
    ):
        grpc_helpers._resolve_direct_path_interconnect(None)


@pytest.mark.parametrize(
    "target,expected_host",
    [
        ("storage-direct.googleapis.com:443", "storage-direct.googleapis.com"),
        ("dns:///storage-direct.googleapis.com:443", "storage-direct.googleapis.com"),
        (
            "https://storage-direct.googleapis.com:443/v1",
            "storage-direct.googleapis.com",
        ),
        (
            "http://storage-direct.googleapis.com:443/v1",
            "storage-direct.googleapis.com",
        ),
        (
            "google-c2p:///storage-direct.googleapis.com?force-xds",
            "storage-direct.googleapis.com",
        ),
        ("[::1]:8080", "::1"),
        ("[invalid_ipv6", "[invalid_ipv6"),
        ("", ""),
    ],
)
def test__extract_target_host(target, expected_host):
    assert grpc_helpers._extract_target_host(target) == expected_host


@pytest.mark.parametrize(
    "target,attempt_interconnect,expected_target",
    [
        (
            "storage-direct.googleapis.com:443",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "dns:///storage-direct.googleapis.com:443",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "https://storage-direct.googleapis.com:443",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "http://storage-direct.googleapis.com:443/v1",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "google-c2p:///storage-direct.googleapis.com",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "google-c2p:///storage-direct.googleapis.com?force-xds",
            True,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "google-c2p:///storage-direct.googleapis.com?force-xds",
            False,
            "google-c2p:///storage-direct.googleapis.com?force-xds",
        ),
        (
            "storage-direct.googleapis.com:443?foo=bar",
            True,
            "google-c2p:///storage-direct.googleapis.com?foo=bar&force-xds",
        ),
    ],
)
def test__modify_target_for_direct_path_interconnect(
    target, attempt_interconnect, expected_target
):
    actual = grpc_helpers._modify_target_for_direct_path(
        target,
        attempt_direct_path_xds_over_interconnect=attempt_interconnect,
    )
    assert actual == expected_target


@mock.patch("grpc.ssl_channel_credentials")
@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_attempt_direct_path_xds_over_interconnect_default_ssl(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
    ssl_creds_call,
):
    composite_creds = composite_creds_call.return_value
    default_ssl_creds = ssl_creds_call.return_value

    channel = grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path=True,
        attempt_direct_path_xds_over_interconnect=True,
    )

    assert channel is grpc_secure_channel.return_value
    ssl_creds_call.assert_called_once_with()
    assert composite_creds_call.call_args.args[0] is default_ssl_creds
    grpc_secure_channel.assert_called_once_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=(("grpc.default_authority", "storage.googleapis.com"),),
    )


@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_attempt_direct_path_xds_over_interconnect_custom_ssl(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
):
    composite_creds = composite_creds_call.return_value
    custom_ssl_creds = mock.sentinel.custom_ssl_creds

    channel = grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        ssl_credentials=custom_ssl_creds,
        attempt_direct_path=True,
        attempt_direct_path_xds_over_interconnect=True,
    )

    assert channel is grpc_secure_channel.return_value
    assert composite_creds_call.call_args.args[0] is custom_ssl_creds
    grpc_secure_channel.assert_called_once_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=(("grpc.default_authority", "storage.googleapis.com"),),
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_interconnect_fallback_rewrites_direct_host(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
):
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path=False,
        attempt_direct_path_xds_over_interconnect=False,
    )

    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(
        "storage.googleapis.com:443",
        composite_creds,
        compression=None,
    )


@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_interconnect_fallback_preserves_non_google_direct_host(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
):
    composite_creds = composite_creds_call.return_value

    channel = grpc_helpers.create_channel(
        "my-direct.example.com:443",
        attempt_direct_path=False,
        attempt_direct_path_xds_over_interconnect=False,
    )

    assert channel is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_once_with(
        "my-direct.example.com:443",
        composite_creds,
        compression=None,
    )

    channel2 = grpc_helpers.create_channel(
        "storage-direct.googleapis.com.example.com:443",
        attempt_direct_path=False,
        attempt_direct_path_xds_over_interconnect=False,
    )
    assert channel2 is grpc_secure_channel.return_value
    grpc_secure_channel.assert_called_with(
        "storage-direct.googleapis.com.example.com:443",
        composite_creds,
        compression=None,
    )


@pytest.mark.parametrize(
    "target,expected_authority",
    [
        ("storage-direct.googleapis.com:443", "storage.googleapis.com"),
        ("dns:///storage-direct.googleapis.com:443", "storage.googleapis.com"),
        (
            "google-c2p:///storage-direct.googleapis.com?force-xds",
            "storage.googleapis.com",
        ),
        ("storage.googleapis.com:443", None),
        ("my-direct.example.com:443", None),
        ("storage-direct.googleapis.com.example.com:443", None),
        ("-direct.googleapis.com:443", None),
    ],
)
def test__extract_direct_path_authority(target, expected_authority):
    assert grpc_helpers._extract_direct_path_authority(target) == expected_authority


@mock.patch("grpc.ssl_channel_credentials")
@mock.patch("grpc.composite_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_interconnect_authority_branches(
    grpc_secure_channel,
    google_auth_default,
    composite_creds_call,
    ssl_creds_call,
):
    composite_creds = composite_creds_call.return_value

    # Authority is None (target does not contain -direct.googleapis.com)
    grpc_helpers.create_channel(
        "storage.googleapis.com:443",
        attempt_direct_path_xds_over_interconnect=True,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage.googleapis.com?force-xds",
        composite_creds,
        compression=None,
    )

    # Authority exists, but grpc.default_authority is already provided
    custom_options_default = (("grpc.default_authority", "custom.googleapis.com"),)
    grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path_xds_over_interconnect=True,
        options=custom_options_default,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=custom_options_default,
    )

    # Authority exists, but grpc.ssl_target_name_override is already provided
    custom_options_ssl = (("grpc.ssl_target_name_override", "custom.googleapis.com"),)
    grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path_xds_over_interconnect=True,
        options=custom_options_ssl,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=custom_options_ssl,
    )


@mock.patch("grpc.ssl_channel_credentials")
@mock.patch("grpc.composite_channel_credentials")
@mock.patch("grpc.compute_engine_channel_credentials")
@mock.patch(
    "google.auth.default",
    autospec=True,
    return_value=(mock.sentinel.credentials, mock.sentinel.project),
)
@mock.patch("grpc.secure_channel")
def test_create_channel_interconnect_gated_by_attempt_direct_path(
    grpc_secure_channel,
    google_auth_default,
    compute_engine_creds_call,
    composite_creds_call,
    ssl_creds_call,
    monkeypatch,
):
    monkeypatch.setenv(grpc_helpers._DIRECT_PATH_INTERCONNECT_ENV, "true")
    composite_creds = composite_creds_call.return_value
    compute_creds = compute_engine_creds_call.return_value

    # When attempt_direct_path is False (default), env var override is ignored
    grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path=False,
    )
    # Target rewrites to standard fallback host instead of C2P
    grpc_secure_channel.assert_called_with(
        "storage.googleapis.com:443",
        compute_creds,
        compression=None,
    )

    # When attempt_direct_path is True, env var override activates DirectPath Interconnect
    grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path=True,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=(("grpc.default_authority", "storage.googleapis.com"),),
    )

    # When attempt_direct_path_xds_over_interconnect is True explicitly, Interconnect activates
    grpc_helpers.create_channel(
        "storage-direct.googleapis.com:443",
        attempt_direct_path=False,
        attempt_direct_path_xds_over_interconnect=True,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage-direct.googleapis.com?force-xds",
        composite_creds,
        compression=None,
        options=(("grpc.default_authority", "storage.googleapis.com"),),
    )

    # When target already starts with google-c2p:/// and attempt_direct_path=False, preserve target
    grpc_helpers.create_channel(
        "google-c2p:///storage-direct.googleapis.com",
        attempt_direct_path=False,
    )
    grpc_secure_channel.assert_called_with(
        "google-c2p:///storage-direct.googleapis.com",
        compute_creds,
        compression=None,
    )


_GRPC_SUPPORTS_REGISTERED_METHOD = (
    "_registered_method" in inspect.signature(grpc.Channel.unary_unary).parameters
)


class _FakeCertManager:
    """In-memory duck-typed certificate manager for _RotatingGrpcChannel tests."""

    def __init__(self, generation_id=1, advance_on_refresh=False):
        self.generation_id = generation_id
        self.advance_on_refresh = advance_on_refresh
        self.refresh_calls = []
        self._lock = threading.Lock()

    def refresh(self, expected_generation):
        with self._lock:
            self.refresh_calls.append(expected_generation)
            # Like the real manager, skip the reload if another caller already
            # moved past the caller's generation.
            if self.generation_id > expected_generation:
                return True
            if self.advance_on_refresh:
                self.generation_id += 1
                self.advance_on_refresh = False
                return True
            return False


class _UnaryUnaryPassthroughInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Matches generated GAPIC _LoggingClientInterceptor (UnaryUnary only)."""

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return continuation(client_call_details, request)


def _make_mock_channel(name="channel"):
    ch = mock.create_autospec(grpc.Channel, instance=True, name=name)
    ch.custom_attr = f"attr_{name}"
    return ch


def _make_real_channel():
    # Creating a channel opens no socket; tests never send an RPC on it.
    return grpc.insecure_channel("127.0.0.1:9")


class Test_RotatingGrpcChannel:
    def test_wrap_errors_recognizes_rotating_multicallables(self):
        ch1 = _make_mock_channel("ch1")
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: ch1)
        intercepted = grpc.intercept_channel(
            rotating, _UnaryUnaryPassthroughInterceptor()
        )

        assert isinstance(
            rotating.unary_unary("/svc/Unary"), grpc.UnaryUnaryMultiCallable
        )
        assert isinstance(
            intercepted.unary_stream("/svc/ServerStream"),
            grpc.UnaryStreamMultiCallable,
        )
        assert isinstance(
            intercepted.stream_unary("/svc/ClientStream"),
            grpc.StreamUnaryMultiCallable,
        )
        assert isinstance(
            intercepted.stream_stream("/svc/BidiStream"),
            grpc.StreamStreamMultiCallable,
        )

    @pytest.mark.parametrize(
        "registered_method",
        [
            False,
            pytest.param(
                True,
                marks=pytest.mark.skipif(
                    not _GRPC_SUPPORTS_REGISTERED_METHOD,
                    reason="grpcio < 1.63 has no _registered_method",
                ),
            ),
        ],
    )
    def test_registered_method_and_fresh_multicallable_across_swap(
        self, registered_method
    ):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: next(channels))
        intercepted = grpc.intercept_channel(
            rotating, _UnaryUnaryPassthroughInterceptor()
        )

        serializer = mock.sentinel.serializer
        deserializer = mock.sentinel.deserializer
        # The 4th positional argument only exists on grpcio 1.63+. The inner
        # channel must only see it when it is True.
        extra_args = (True,) if registered_method else ()
        extra_kwargs = {"_registered_method": True} if registered_method else {}

        uu_stub = intercepted.unary_unary(
            "/svc/UU", serializer, deserializer, *extra_args
        )
        us_stub = intercepted.unary_stream(
            "/svc/US", serializer, deserializer, *extra_args
        )
        su_stub = intercepted.stream_unary(
            "/svc/SU", serializer, deserializer, *extra_args
        )
        ss_stub = intercepted.stream_stream(
            "/svc/SS", serializer, deserializer, *extra_args
        )

        # Factory creation is side-effect free on the inner channels
        ch1.unary_unary.assert_not_called()
        ch1.unary_stream.assert_not_called()
        ch1.stream_unary.assert_not_called()
        ch1.stream_stream.assert_not_called()

        for ch, suffix in ((ch1, "1"), (ch2, "2")):
            ch.unary_unary.return_value.with_call.return_value = (
                f"uu_{suffix}",
                None,
            )
            uu_fut = mock.MagicMock()
            uu_fut.result.return_value = f"uu_fut_{suffix}"
            ch.unary_unary.return_value.future.return_value = uu_fut
            ch.unary_stream.return_value.return_value = iter([f"us_{suffix}"])
            ch.stream_unary.return_value.with_call.return_value = (
                f"su_{suffix}",
                None,
            )
            su_fut = mock.MagicMock()
            su_fut.result.return_value = f"su_fut_{suffix}"
            ch.stream_unary.return_value.future.return_value = su_fut
            ch.stream_stream.return_value.return_value = iter([f"ss_{suffix}"])

        assert uu_stub("req") == "uu_1"
        assert uu_stub.future("req").result() == "uu_fut_1"
        assert list(us_stub("req")) == ["us_1"]
        assert su_stub(iter(["req"])) == "su_1"
        assert su_stub.future(iter(["req"])).result() == "su_fut_1"
        assert list(ss_stub(iter(["req"]))) == ["ss_1"]

        # Swap channel (generic timer/Bigtable pattern with cert_manager=None)
        prewarmed = rotating.create_channel()
        assert prewarmed is ch2
        old = rotating.swap_channel(prewarmed)
        assert old is ch1
        assert rotating.channel is ch2
        ch1.close.assert_not_called()

        # Same cached stubs now dispatch on ch2
        assert uu_stub("req") == "uu_2"
        assert uu_stub.future("req").result() == "uu_fut_2"
        assert list(us_stub("req")) == ["us_2"]
        assert su_stub(iter(["req"])) == "su_2"
        assert su_stub.future(iter(["req"])).result() == "su_fut_2"
        assert list(ss_stub(iter(["req"]))) == ["ss_2"]

        for ch in (ch1, ch2):
            assert ch.unary_unary.call_args_list == [
                mock.call("/svc/UU", serializer, deserializer, **extra_kwargs),
                mock.call("/svc/UU", serializer, deserializer, **extra_kwargs),
            ]
            ch.unary_stream.assert_called_once_with(
                "/svc/US", serializer, deserializer, **extra_kwargs
            )
            assert ch.stream_unary.call_args_list == [
                mock.call("/svc/SU", serializer, deserializer, **extra_kwargs),
                mock.call("/svc/SU", serializer, deserializer, **extra_kwargs),
            ]
            ch.stream_stream.assert_called_once_with(
                "/svc/SS", serializer, deserializer, **extra_kwargs
            )

    def test_proxy_call_kwargs_and_with_call_passthrough(self):
        ch1 = _make_mock_channel("ch1")
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: ch1)
        call_kwargs = dict(
            timeout=12.5,
            metadata=(("x-test", "1"),),
            credentials=mock.sentinel.call_creds,
            wait_for_ready=True,
            compression=grpc.Compression.Gzip,
        )

        ch1.unary_unary.return_value.with_call.return_value = (
            "uu_resp",
            mock.sentinel.uu_call,
        )
        ch1.stream_unary.return_value.with_call.return_value = (
            "su_resp",
            mock.sentinel.su_call,
        )

        uu_stub = rotating.unary_unary("/svc/UU")
        su_stub = rotating.stream_unary("/svc/SU")

        assert uu_stub("req", **call_kwargs) == "uu_resp"
        assert uu_stub.with_call("req", **call_kwargs) == (
            "uu_resp",
            mock.sentinel.uu_call,
        )
        uu_stub.future("req", **call_kwargs)
        rotating.unary_stream("/svc/US")("req", **call_kwargs)
        assert su_stub(iter(["req"]), **call_kwargs) == "su_resp"
        assert su_stub.with_call(iter(["req"]), **call_kwargs) == (
            "su_resp",
            mock.sentinel.su_call,
        )
        su_stub.future(iter(["req"]), **call_kwargs)
        rotating.stream_stream("/svc/SS")(iter(["req"]), **call_kwargs)

        assert ch1.unary_unary.return_value.with_call.call_args_list == [
            mock.call("req", **call_kwargs),
            mock.call("req", **call_kwargs),
        ]
        ch1.unary_unary.return_value.future.assert_called_once_with(
            "req", **call_kwargs
        )
        ch1.unary_stream.return_value.assert_called_once_with("req", **call_kwargs)
        assert ch1.stream_unary.return_value.with_call.call_args_list == [
            mock.call(mock.ANY, **call_kwargs),
            mock.call(mock.ANY, **call_kwargs),
        ]
        ch1.stream_unary.return_value.future.assert_called_once_with(
            mock.ANY, **call_kwargs
        )
        ch1.stream_stream.return_value.assert_called_once_with(mock.ANY, **call_kwargs)

    def test_pre_rpc_generation_advance_swaps_before_call(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )

        stub = rotating.unary_unary("/svc/UU")
        ch2.unary_unary.return_value.with_call.return_value = (
            "ok_from_ch2",
            mock.sentinel.call,
        )

        # Simulate AuthMetadataPlugin advancing generation_id before next RPC
        cert_manager.generation_id = 2

        assert stub("req") == "ok_from_ch2"
        ch1.unary_unary.assert_not_called()
        assert rotating.channel is ch2

    def test_concurrent_pre_rpc_checks_build_one_channel(self):
        num_threads = 8
        cert_manager = _FakeCertManager(generation_id=1)
        built = []

        def factory():
            if built:
                # Hold the channel lock long enough for the other threads to
                # pass the lock-free generation check and queue on the lock.
                time.sleep(0.05)
            ch = _make_mock_channel(f"ch{len(built) + 1}")
            ch.unary_unary.return_value.with_call.return_value = ("ok", None)
            built.append(ch)
            return ch

        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        stub = rotating.unary_unary("/svc/UU")
        cert_manager.generation_id = 2
        barrier = threading.Barrier(num_threads)

        def call_after_barrier():
            barrier.wait()
            return stub("req")

        with futures.ThreadPoolExecutor(num_threads) as executor:
            results = [executor.submit(call_after_barrier) for _ in range(num_threads)]
            assert [f.result() for f in results] == ["ok"] * num_threads

        assert len(built) == 2
        assert rotating.channel is built[1]
        built[0].unary_unary.assert_not_called()

    @pytest.mark.parametrize(
        "timeout,expected_retry_timeout",
        [(5.0, 3.75), (None, None)],
    )
    def test_unary_unary_reactive_retry_and_arg_passthrough(
        self, timeout, expected_retry_timeout
    ):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        intercepted = grpc.intercept_channel(
            rotating, _UnaryUnaryPassthroughInterceptor()
        )
        stub = intercepted.unary_unary("/svc/UU")

        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)
        ch1.unary_unary.return_value.with_call.side_effect = unauth_err
        ch2.unary_unary.return_value.with_call.return_value = (
            "retried_ok",
            mock.sentinel.call2,
        )

        metadata = [("x-test", "1")]
        credentials = mock.sentinel.call_creds
        compression = grpc.Compression.Gzip

        with mock.patch(
            "google.api_core.grpc_helpers.time.monotonic",
            side_effect=[100.0, 101.25],
        ):
            resp, _ = stub.with_call(
                "req",
                timeout=timeout,
                metadata=metadata,
                credentials=credentials,
                wait_for_ready=True,
                compression=compression,
            )

        assert resp == "retried_ok"
        assert cert_manager.refresh_calls == [1]
        assert rotating.channel is ch2
        ch1.unary_unary.return_value.with_call.assert_called_once_with(
            "req",
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=True,
            compression=compression,
        )
        ch2.unary_unary.return_value.with_call.assert_called_once_with(
            "req",
            timeout=expected_retry_timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=True,
            compression=compression,
        )

    @pytest.mark.parametrize(
        "cert_manager,status_code",
        [
            (
                _FakeCertManager(generation_id=1, advance_on_refresh=False),
                grpc.StatusCode.UNAUTHENTICATED,
            ),
            (None, grpc.StatusCode.UNAUTHENTICATED),
            (
                _FakeCertManager(generation_id=1, advance_on_refresh=True),
                grpc.StatusCode.PERMISSION_DENIED,
            ),
        ],
    )
    def test_unary_unary_no_retry_when_not_rotated_or_non_unauthenticated(
        self, cert_manager, status_code
    ):
        ch1 = _make_mock_channel("ch1")
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: ch1, cert_manager=cert_manager
        )
        stub = rotating.unary_unary("/svc/UU")

        rpc_err = RpcErrorImpl(status_code)
        ch1.unary_unary.return_value.with_call.side_effect = rpc_err

        with pytest.raises(grpc.RpcError) as exc_info:
            stub("req")

        assert exc_info.value is rpc_err
        assert rotating.channel is ch1
        assert ch1.unary_unary.return_value.with_call.call_count == 1

    def test_concurrent_unauthenticated_failures_build_one_channel(self):
        num_threads = 8
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        factory = mock.Mock(side_effect=[ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        stub = rotating.unary_unary("/svc/UU")
        barrier = threading.Barrier(num_threads)

        def fail_together(*args, **kwargs):
            barrier.wait()
            raise RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)

        ch1.unary_unary.return_value.with_call.side_effect = fail_together
        ch2.unary_unary.return_value.with_call.return_value = ("ok", None)

        with futures.ThreadPoolExecutor(num_threads) as executor:
            results = [executor.submit(stub, "req") for _ in range(num_threads)]
            assert [f.result() for f in results] == ["ok"] * num_threads

        assert factory.call_count == 2
        assert cert_manager.generation_id == 2
        assert rotating.channel is ch2

    def test_rotate_on_unauthenticated_coalesces_when_generation_already_advanced(
        self,
    ):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        factory = mock.Mock(side_effect=[ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        unauthenticated = grpc.StatusCode.UNAUTHENTICATED

        # Generation already advanced in AuthMetadataPlugin during in-flight call
        cert_manager.generation_id = 2

        # First call from attempt_gen=1 swaps to ch2 without calling cert_manager.refresh
        assert rotating._rotate_on_unauthenticated(unauthenticated, 1) is True
        assert cert_manager.refresh_calls == []
        assert rotating.channel is ch2
        assert factory.call_count == 2

        # Second concurrent call from attempt_gen=1 sees channel already at gen 2;
        # returns True so caller retries on ch2 without rebuilding a third channel
        assert rotating._rotate_on_unauthenticated(unauthenticated, 1) is True
        assert cert_manager.refresh_calls == []
        assert rotating.channel is ch2
        assert factory.call_count == 2

    def test_rotating_call_forwards_call_and_future_methods(self):
        ch1 = _make_mock_channel("ch1")
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: ch1, cert_manager=cert_manager
        )

        raw_future = mock.MagicMock()
        raw_future.result.return_value = "future_ok"
        raw_future.exception.return_value = None
        raw_future.code.return_value = grpc.StatusCode.OK
        ch1.unary_unary.return_value.future.return_value = raw_future

        fut = rotating.unary_unary("/svc/UU").future("req", timeout=2.0)
        assert iter(fut) is fut
        assert fut.result(timeout=1.0) == "future_ok"
        assert fut.exception(timeout=1.0) is None
        assert fut.cancel() is raw_future.cancel.return_value
        assert fut.cancelled() is raw_future.cancelled.return_value
        assert fut.running() is raw_future.running.return_value
        assert fut.done() is raw_future.done.return_value
        assert fut.traceback(timeout=1.0) is raw_future.traceback.return_value
        assert (
            fut.add_callback(mock.sentinel.cb) is raw_future.add_callback.return_value
        )
        assert fut.is_active() is raw_future.is_active.return_value
        assert fut.time_remaining() is raw_future.time_remaining.return_value
        assert fut.code() == grpc.StatusCode.OK
        assert fut.details() is raw_future.details.return_value
        assert fut.debug_error_string() is raw_future.debug_error_string.return_value
        assert fut.initial_metadata() is raw_future.initial_metadata.return_value
        assert fut.trailing_metadata() is raw_future.trailing_metadata.return_value

        done_seen = []
        raw_future.add_done_callback.side_effect = lambda cb: cb(raw_future)
        fut.add_done_callback(lambda f: done_seen.append(f))
        assert done_seen == [raw_future]
        assert rotating.channel is ch1

    @pytest.mark.parametrize(
        "trigger", ["result", "exception", "code", "add_done_callback"]
    )
    def test_rotating_call_swaps_channel_on_unauthenticated(self, trigger):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)

        raw_future = mock.MagicMock()
        raw_future.result.side_effect = unauth_err
        raw_future.exception.return_value = unauth_err
        raw_future.code.return_value = grpc.StatusCode.UNAUTHENTICATED
        raw_future.add_done_callback.side_effect = lambda cb: cb(raw_future)
        ch1.unary_unary.return_value.future.return_value = raw_future

        fut = rotating.unary_unary("/svc/UU").future("req")
        if trigger == "result":
            with pytest.raises(grpc.RpcError) as exc_info:
                fut.result()
            assert exc_info.value is unauth_err
        elif trigger == "exception":
            assert fut.exception() is unauth_err
        elif trigger == "code":
            assert fut.code() == grpc.StatusCode.UNAUTHENTICATED
        else:
            seen = []
            fut.add_done_callback(lambda f: seen.append((f, rotating.channel)))
            assert seen == [(raw_future, ch2)]

        assert rotating.channel is ch2

    def test_failed_call_runs_rotation_check_once(self):
        ch1 = _make_mock_channel("ch1")
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: ch1, cert_manager=cert_manager
        )

        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)
        raw_future = mock.MagicMock()
        raw_future.code.return_value = grpc.StatusCode.UNAUTHENTICATED
        raw_future.exception.return_value = unauth_err
        raw_future.result.side_effect = unauth_err
        raw_future.add_done_callback.side_effect = lambda cb: cb(raw_future)
        raw_future.add_callback.side_effect = lambda cb: cb()
        ch1.unary_unary.return_value.future.return_value = raw_future

        fut = rotating.unary_unary("/svc/UU").future("req")
        assert fut.exception() is unauth_err
        for _ in range(3):
            assert fut.code() == grpc.StatusCode.UNAUTHENTICATED
        with pytest.raises(grpc.RpcError):
            fut.result()
        fut.add_done_callback(lambda f: None)
        fut.add_callback(lambda: None)

        # The certificate did not change, so it was reloaded only once.
        assert cert_manager.refresh_calls == [1]
        assert rotating.channel is ch1

    def test_add_callback_runs_rotation_check(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )

        raw_call = mock.MagicMock()
        raw_call.code.return_value = grpc.StatusCode.UNAUTHENTICATED
        raw_call.add_callback.side_effect = lambda cb: cb()
        ch1.stream_stream.return_value.return_value = raw_call
        callback = mock.Mock()

        call = rotating.stream_stream("/svc/BidiStream")(iter(["r1"]))
        call.add_callback(callback)

        # grpcio logs a raising callback through its .func attribute.
        registered = raw_call.add_callback.call_args[0][0]
        assert hasattr(registered, "func")
        callback.assert_called_once_with()
        assert rotating.channel is ch2

    def test_unary_unary_skips_retry_when_timeout_exhausted(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        stub = rotating.unary_unary("/svc/UU")
        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)
        ch1.unary_unary.return_value.with_call.side_effect = unauth_err

        with mock.patch(
            "google.api_core.grpc_helpers.time.monotonic",
            side_effect=[100.0, 106.0],
        ):
            with pytest.raises(grpc.RpcError) as exc_info:
                stub("req", timeout=5.0)

        assert exc_info.value is unauth_err
        assert rotating.channel is ch2
        ch2.unary_unary.assert_not_called()

    def test_bare_rpc_error_without_code_propagates(self):
        ch1 = _make_mock_channel("ch1")
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: ch1)
        bare_err = grpc.RpcError()

        ch1.unary_unary.return_value.with_call.side_effect = bare_err
        with pytest.raises(grpc.RpcError) as exc_info:
            rotating.unary_unary("/svc/UU")("req")
        assert exc_info.value is bare_err

    def test_rotation_failure_does_not_mask_rpc_error(self):
        def _make_failing_rotating():
            ch1 = _make_mock_channel("ch1")
            factory = mock.Mock(side_effect=[ch1, RuntimeError("factory failed")])
            cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
            rotating = grpc_helpers._RotatingGrpcChannel(
                factory, cert_manager=cert_manager
            )
            return ch1, rotating

        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)

        ch1, rotating = _make_failing_rotating()
        ch1.unary_unary.return_value.with_call.side_effect = unauth_err
        with pytest.raises(grpc.RpcError) as exc_info:
            rotating.unary_unary("/svc/UU")("req")
        assert exc_info.value is unauth_err
        assert rotating.channel is ch1

        ch1, rotating = _make_failing_rotating()
        raw_future = mock.MagicMock()
        raw_future.exception.return_value = unauth_err
        raw_future.code.return_value = grpc.StatusCode.UNAUTHENTICATED
        ch1.unary_unary.return_value.future.return_value = raw_future
        fut = rotating.unary_unary("/svc/UU").future("req")
        assert fut.exception() is unauth_err
        assert fut.code() == grpc.StatusCode.UNAUTHENTICATED
        assert rotating.channel is ch1

    def test_unary_stream_swaps_without_replay(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        intercepted = grpc.intercept_channel(
            rotating, _UnaryUnaryPassthroughInterceptor()
        )
        stub = grpc_helpers.wrap_errors(intercepted.unary_stream("/svc/ServerStream"))
        ch1.unary_stream.return_value.return_value = RpcResponseIteratorImpl(
            [RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)]
        )

        with pytest.raises(exceptions.Unauthenticated):
            stub("req")
        assert rotating.channel is ch2
        ch2.unary_stream.assert_not_called()

    def test_stream_unary_swaps_without_replay(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        ch3 = _make_mock_channel("ch3")
        channels = iter([ch1, ch2, ch3])
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        stub = rotating.stream_unary("/svc/ClientStream")
        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)

        ch1.stream_unary.return_value.with_call.side_effect = unauth_err
        cert_manager.advance_on_refresh = True
        with pytest.raises(grpc.RpcError) as exc_info:
            stub.with_call(iter(["r1"]))
        assert exc_info.value is unauth_err
        assert rotating.channel is ch2
        ch2.stream_unary.assert_not_called()

        raw_future = mock.MagicMock()
        raw_future.result.side_effect = unauth_err
        ch2.stream_unary.return_value.future.return_value = raw_future
        cert_manager.advance_on_refresh = True
        fut = stub.future(iter(["r1"]))
        with pytest.raises(grpc.RpcError) as exc_info:
            fut.result()
        assert exc_info.value is unauth_err
        assert rotating.channel is ch3

    def test_stream_stream_swaps_without_replay(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(
            lambda: next(channels), cert_manager=cert_manager
        )
        stub = grpc_helpers.wrap_errors(rotating.stream_stream("/svc/BidiStream"))

        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)
        ch1.stream_stream.return_value.return_value = RpcResponseIteratorImpl(
            [unauth_err]
        )

        with pytest.raises(exceptions.Unauthenticated):
            stub(iter(["r1"]))

        assert rotating.channel is ch2
        ch2.stream_stream.assert_not_called()

    def test_swap_in_channel_created_before_rotation(self):
        ch1 = _make_mock_channel("ch1")
        prewarmed = _make_mock_channel("prewarmed")
        ch3 = _make_mock_channel("ch3")
        factory = mock.Mock(side_effect=[ch1, prewarmed, ch3])
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        ch3.unary_unary.return_value.with_call.return_value = ("ok", None)

        assert rotating.create_channel() is prewarmed
        # The certificate rotates while the caller warms the channel.
        cert_manager.generation_id = 2

        # The old-certificate channel is closed and not installed; a new one is built.
        assert rotating.swap_channel(prewarmed) is ch1
        assert rotating.channel is ch3
        assert rotating.unary_unary("/svc/UU")("req") == "ok"
        prewarmed.unary_unary.assert_not_called()
        prewarmed.close.assert_called_once_with()
        assert factory.call_count == 3

    def test_swap_in_current_or_external_channel_is_kept(self):
        ch1 = _make_mock_channel("ch1")
        prewarmed = _make_mock_channel("prewarmed")
        external = _make_mock_channel("external")
        factory = mock.Mock(side_effect=[ch1, prewarmed])
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        stub = rotating.unary_unary("/svc/UU")
        prewarmed.unary_unary.return_value.with_call.return_value = ("prewarmed", None)
        external.unary_unary.return_value.with_call.return_value = ("external", None)

        rotating.swap_channel(rotating.create_channel())
        assert stub("req") == "prewarmed"

        # A channel that did not come from create_channel() is assumed current.
        cert_manager.generation_id = 2
        rotating.swap_channel(external)
        assert stub("req") == "external"
        assert factory.call_count == 2

    def test_subscriber_migration_across_swap(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: next(channels))

        cb1 = mock.Mock(name="cb1")
        cb2 = mock.Mock(name="cb2")

        rotating.subscribe(cb1, try_to_connect=False)
        rotating.subscribe(cb1, try_to_connect=True)
        rotating.subscribe(cb2, try_to_connect=False)

        # Unsubscribing cb2 removes it; unsubscribing cb1 once leaves the second entry;
        # unsubscribing an unregistered callback forwards cleanly without error.
        rotating.unsubscribe(cb2)
        rotating.unsubscribe(cb1)
        rotating.unsubscribe(mock.Mock(name="unknown"))
        ch1.unsubscribe.reset_mock()

        old = rotating.swap_channel()
        assert old is ch1
        assert rotating.channel is ch2
        ch1.unsubscribe.assert_called_once_with(cb1)
        ch2.subscribe.assert_called_once_with(cb1, try_to_connect=True)
        ch1.close.assert_not_called()

    def test_getattr_and_context_manager(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        channels = iter([ch1, ch2])
        rotating = grpc_helpers._RotatingGrpcChannel(lambda: next(channels))

        rotating.swap_channel()
        assert rotating.custom_attr == "attr_ch2"

        with rotating as ctx_ch:
            assert ctx_ch is rotating
        ch2.close.assert_called_once_with()
        ch1.close.assert_not_called()

    def test_call_keeps_its_channel_alive_after_swap(self):
        rotating = grpc_helpers._RotatingGrpcChannel(_make_real_channel)
        old_channel = rotating.channel
        # Replace the multicallable factory so no RPC is sent.
        old_channel.unary_stream = mock.Mock()
        call = rotating.unary_stream("/svc/ServerStream")("req")
        old_channel_ref = weakref.ref(old_channel)
        del old_channel

        rotating.swap_channel()
        gc.collect()
        assert old_channel_ref() is not None

        del call
        gc.collect()
        assert old_channel_ref() is None
        rotating.close()

    def test_close_stops_building_channels(self):
        factory = mock.Mock(side_effect=_make_real_channel)
        cert_manager = _FakeCertManager(generation_id=1)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        stub = rotating.unary_unary("/svc/UU")
        registered_stub = rotating.unary_unary("/svc/UU", _registered_method=True)

        rotating.close()
        cert_manager.generation_id = 2

        # Unregistered RPC stays on the closed channel; registered RPC raises
        # before touching grpcio's _get_registered_call_handle().
        with pytest.raises(ValueError):
            stub(b"req")
        with pytest.raises(ValueError):
            registered_stub(b"req")
        with pytest.raises(ValueError):
            rotating.swap_channel()
        with pytest.raises(ValueError):
            rotating.create_channel()
        # Post-close subscribe is a no-op and does not start a polling thread.
        rotating.subscribe(lambda _: None, try_to_connect=True)
        assert rotating._subscribers == []
        assert factory.call_count == 1

    def test_create_channel_closes_channel_when_closed_concurrently(self):
        ch1 = _make_mock_channel("ch1")
        ch2 = _make_mock_channel("ch2")
        rotating = None

        def factory():
            if rotating is None:
                return ch1
            rotating.close()
            return ch2

        rotating = grpc_helpers._RotatingGrpcChannel(factory)
        with pytest.raises(ValueError):
            rotating.create_channel()

        ch1.close.assert_called_once_with()
        ch2.close.assert_called_once_with()

    def test_unauthenticated_after_close_does_not_rebuild(self):
        ch1 = _make_mock_channel("ch1")
        factory = mock.Mock(return_value=ch1)
        cert_manager = _FakeCertManager(generation_id=1, advance_on_refresh=True)
        rotating = grpc_helpers._RotatingGrpcChannel(factory, cert_manager=cert_manager)
        unauth_err = RpcErrorImpl(grpc.StatusCode.UNAUTHENTICATED)
        raw_future = mock.MagicMock()
        raw_future.result.side_effect = unauth_err
        ch1.unary_unary.return_value.future.return_value = raw_future

        fut = rotating.unary_unary("/svc/UU").future("req")
        rotating.close()

        with pytest.raises(grpc.RpcError) as exc_info:
            fut.result()
        assert exc_info.value is unauth_err
        assert cert_manager.refresh_calls == []
        assert factory.call_count == 1
        ch1.close.assert_called_once_with()

    def test_getattr_without_init_raises_attribute_error(self):
        rotating = grpc_helpers._RotatingGrpcChannel(_make_mock_channel)
        assert copy.copy(rotating).channel is rotating.channel

        uninitialized = grpc_helpers._RotatingGrpcChannel.__new__(
            grpc_helpers._RotatingGrpcChannel
        )
        with pytest.raises(AttributeError):
            uninitialized.custom_attr
