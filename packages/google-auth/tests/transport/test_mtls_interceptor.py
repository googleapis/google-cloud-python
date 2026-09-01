# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from unittest import mock
import grpc
import pytest
import google.auth.transport.grpc as transport_grpc
def test_interceptor_uses_factory_if_callable(mock_replayable):
    import google.auth.transport.grpc as transport_grpc
    interceptor = transport_grpc.CertRotationInterceptor()
    call_no_factory = transport_grpc._RetryableStreamResponseIterator(
        continuation=mock.Mock(),
        client_call_details=mock.Mock(),
        request_or_iterator=[b"1", b"2"],
        interceptor=interceptor,
        is_client_stream=True,
    )
    assert call_no_factory._uses_factory is False
    assert call_no_factory._payload is not None
    def generator_factory():
        return (x for x in [b"1", b"2"])
    call_factory = transport_grpc._RetryableStreamResponseIterator(
        continuation=mock.Mock(),
        client_call_details=mock.Mock(),
        request_or_iterator=generator_factory,
        interceptor=interceptor,
        is_client_stream=True,
    )
    assert call_factory._uses_factory is True
    assert call_factory._payload is None
@mock.patch("google.auth.transport.grpc.CertRotationInterceptor._should_retry")
def test_factory_infinite_replay_on_error(mock_should_retry):
    import google.auth.transport.grpc as transport_grpc
    interceptor = transport_grpc.CertRotationInterceptor()
    interceptor._wrapper = mock.Mock()
    interceptor._wrapper._cached_cert = "cert"
    mock_should_retry.side_effect = [
        (True, b"cert", b"key", None),
        (False, None, None, None),
    ]
    mock_inner_call1 = mock.Mock()
    mock_err = transport_grpc.grpc.RpcError()
    mock_err.code = lambda: transport_grpc.grpc.StatusCode.UNAUTHENTICATED
    mock_inner_call1.__next__ = mock.Mock(side_effect=mock_err)
    mock_inner_call2 = mock.Mock()
    mock_inner_call2.__next__ = mock.Mock(side_effect=[b"SUCCESS", StopIteration])
    continuation = mock.Mock(side_effect=[mock_inner_call1, mock_inner_call2])
