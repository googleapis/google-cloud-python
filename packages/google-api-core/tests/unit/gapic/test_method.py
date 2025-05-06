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

import datetime
from unittest import mock

import pytest

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)


from google.api_core import exceptions
from google.api_core import retry
from google.api_core import timeout
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.method
import google.api_core.page_iterator


def _utcnow_monotonic():
    curr_value = datetime.datetime.min
    delta = datetime.timedelta(seconds=0.5)
    while True:
        yield curr_value
        curr_value += delta


def test_wrap_method_basic():
    method = mock.Mock(spec=["__call__"], return_value=42)

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(method)

    result = wrapped_method(1, 2, meep="moop")

    assert result == 42
    method.assert_called_once_with(1, 2, meep="moop", metadata=mock.ANY)

    # Check that the default client info was specified in the metadata.
    metadata = method.call_args[1]["metadata"]
    assert len(metadata) == 1
    client_info = google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO
    user_agent_metadata = client_info.to_grpc_metadata()
    assert user_agent_metadata in metadata


def test_wrap_method_with_no_client_info():
    method = mock.Mock(spec=["__call__"])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, client_info=None
    )

    wrapped_method(1, 2, meep="moop")

    method.assert_called_once_with(1, 2, meep="moop")


def test_wrap_method_with_custom_client_info():
    client_info = google.api_core.gapic_v1.client_info.ClientInfo(
        python_version=1,
        grpc_version=2,
        api_core_version=3,
        gapic_version=4,
        client_library_version=5,
        protobuf_runtime_version=6,
    )
    method = mock.Mock(spec=["__call__"])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, client_info=client_info
    )

    wrapped_method(1, 2, meep="moop")

    method.assert_called_once_with(1, 2, meep="moop", metadata=mock.ANY)

    # Check that the custom client info was specified in the metadata.
    metadata = method.call_args[1]["metadata"]
    assert client_info.to_grpc_metadata() in metadata


def test_invoke_wrapped_method_with_metadata():
    method = mock.Mock(spec=["__call__"])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(method)

    wrapped_method(mock.sentinel.request, metadata=[("a", "b")])

    method.assert_called_once_with(mock.sentinel.request, metadata=mock.ANY)
    metadata = method.call_args[1]["metadata"]
    # Metadata should have two items: the client info metadata and our custom
    # metadata.
    assert len(metadata) == 2
    assert ("a", "b") in metadata


def test_invoke_wrapped_method_with_metadata_as_none():
    method = mock.Mock(spec=["__call__"])

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(method)

    wrapped_method(mock.sentinel.request, metadata=None)

    method.assert_called_once_with(mock.sentinel.request, metadata=mock.ANY)
    metadata = method.call_args[1]["metadata"]
    # Metadata should have just one items: the client info metadata.
    assert len(metadata) == 1


@mock.patch("time.sleep")
def test_wrap_method_with_default_retry_and_timeout_and_compression(unused_sleep):
    method = mock.Mock(
        spec=["__call__"], side_effect=[exceptions.InternalServerError(None), 42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = grpc.Compression.Gzip
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = wrapped_method()

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=60, compression=default_compression, metadata=mock.ANY
    )


@mock.patch("time.sleep")
def test_wrap_method_with_default_retry_and_timeout_using_sentinel(unused_sleep):
    method = mock.Mock(
        spec=["__call__"], side_effect=[exceptions.InternalServerError(None), 42]
    )
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = grpc.Compression.Gzip
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = wrapped_method(
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        compression=google.api_core.gapic_v1.method.DEFAULT,
    )

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=60, compression=default_compression, metadata=mock.ANY
    )


@mock.patch("time.sleep")
def test_wrap_method_with_overriding_retry_timeout_compression(unused_sleep):
    method = mock.Mock(spec=["__call__"], side_effect=[exceptions.NotFound(None), 42])
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    default_compression = grpc.Compression.Gzip
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout, default_compression
    )

    result = wrapped_method(
        retry=retry.Retry(retry.if_exception_type(exceptions.NotFound)),
        timeout=timeout.ConstantTimeout(22),
        compression=grpc.Compression.Deflate,
    )

    assert result == 42
    assert method.call_count == 2
    method.assert_called_with(
        timeout=22, compression=grpc.Compression.Deflate, metadata=mock.ANY
    )


def test_wrap_method_with_overriding_timeout_as_a_number():
    method = mock.Mock(spec=["__call__"], return_value=42)
    default_retry = retry.Retry()
    default_timeout = timeout.ConstantTimeout(60)
    wrapped_method = google.api_core.gapic_v1.method.wrap_method(
        method, default_retry, default_timeout
    )

    result = wrapped_method(timeout=22)

    assert result == 42
    method.assert_called_once_with(timeout=22, metadata=mock.ANY)


def test_wrap_method_with_call():
    method = mock.Mock()
    mock_call = mock.Mock()
    method.with_call.return_value = 42, mock_call

    wrapped_method = google.api_core.gapic_v1.method.wrap_method(method, with_call=True)
    result = wrapped_method()
    assert len(result) == 2
    assert result[0] == 42
    assert result[1] == mock_call


def test_wrap_method_with_call_not_supported():
    """Raises an error if wrapped callable doesn't have with_call method."""
    method = lambda: None  # noqa: E731

    with pytest.raises(ValueError) as exc_info:
        google.api_core.gapic_v1.method.wrap_method(method, with_call=True)
    assert "with_call=True is only supported for unary calls" in str(exc_info.value)
