# Copyright 2025 Google LLC
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

import pytest
from grpc import RpcError

from google.cloud.bigtable.data._cross_sync import CrossSync

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock  # type: ignore

if CrossSync.is_async:
    from google.cloud.bigtable.data._async.metrics_interceptor import (
        AsyncBigtableMetricsInterceptor,
    )
else:
    from google.cloud.bigtable.data._sync_autogen.metrics_interceptor import (  # noqa: F401
        BigtableMetricsInterceptor,
    )


__CROSS_SYNC_OUTPUT__ = "tests.unit.data._sync_autogen.test_metrics_interceptor"


@CrossSync.convert(replace_symbols={"__aiter__": "__iter__"})
def _make_mock_stream_call(values, exc=None):
    """
    Create a mock call object that can be used for streaming calls
    """
    call = CrossSync.Mock()

    async def gen():
        for val in values:
            yield val
        if exc:
            raise exc

    call.__aiter__ = mock.Mock(return_value=gen())
    return call


@CrossSync.convert_class(sync_name="TestMetricsInterceptor")
class TestMetricsInterceptorAsync:
    @staticmethod
    @CrossSync.convert(
        replace_symbols={
            "AsyncBigtableMetricsInterceptor": "BigtableMetricsInterceptor"
        }
    )
    def _get_target_class():
        return AsyncBigtableMetricsInterceptor

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    @CrossSync.pytest
    async def test_unary_unary_interceptor_success(self):
        """Test that interceptor handles successful unary-unary calls"""
        instance = self._make_one()
        continuation = CrossSync.Mock()
        call = continuation.return_value
        details = mock.Mock()
        request = mock.Mock()
        result = await instance.intercept_unary_unary(continuation, details, request)
        assert result == call
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_unary_interceptor_failure(self):
        """Test a failed RpcError with metadata"""

        instance = self._make_one()
        exc = RpcError("test")
        continuation = CrossSync.Mock(side_effect=exc)
        details = mock.Mock()
        request = mock.Mock()
        with pytest.raises(RpcError) as e:
            await instance.intercept_unary_unary(continuation, details, request)
        assert e.value == exc
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_unary_interceptor_failure_generic(self):
        """Test generic exception"""

        instance = self._make_one()
        exc = ValueError("test")
        continuation = CrossSync.Mock(side_effect=exc)
        details = mock.Mock()
        request = mock.Mock()
        with pytest.raises(ValueError) as e:
            await instance.intercept_unary_unary(continuation, details, request)
        assert e.value == exc
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_stream_interceptor_success(self):
        """Test that interceptor handles successful unary-stream calls"""

        instance = self._make_one()

        continuation = CrossSync.Mock(return_value=_make_mock_stream_call([1, 2]))
        details = mock.Mock()
        request = mock.Mock()
        wrapper = await instance.intercept_unary_stream(continuation, details, request)
        results = [val async for val in wrapper]
        assert results == [1, 2]
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_stream_interceptor_failure_mid_stream(self):
        """Test that interceptor handles failures mid-stream"""
        instance = self._make_one()
        exc = ValueError("test")
        continuation = CrossSync.Mock(return_value=_make_mock_stream_call([1], exc=exc))
        details = mock.Mock()
        request = mock.Mock()
        wrapper = await instance.intercept_unary_stream(continuation, details, request)
        with pytest.raises(ValueError) as e:
            [val async for val in wrapper]
        assert e.value == exc
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_stream_interceptor_failure_start_stream(self):
        """Test that interceptor handles failures at start of stream with RpcError with metadata"""

        instance = self._make_one()
        exc = RpcError("test")

        continuation = CrossSync.Mock()
        continuation.side_effect = exc
        details = mock.Mock()
        request = mock.Mock()
        with pytest.raises(RpcError) as e:
            await instance.intercept_unary_stream(continuation, details, request)
        assert e.value == exc
        continuation.assert_called_once_with(details, request)

    @CrossSync.pytest
    async def test_unary_stream_interceptor_failure_start_stream_generic(self):
        """Test that interceptor handles failures at start of stream with generic exception"""

        instance = self._make_one()
        exc = ValueError("test")

        continuation = CrossSync.Mock()
        continuation.side_effect = exc
        details = mock.Mock()
        request = mock.Mock()
        with pytest.raises(ValueError) as e:
            await instance.intercept_unary_stream(continuation, details, request)
        assert e.value == exc
        continuation.assert_called_once_with(details, request)
