# Copyright 2024 Google LLC
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

import os
from unittest import mock
from .test_execute_query_utils import (
    ChannelMockAsync,
    response_with_metadata,
    response_with_result,
)
from google.api_core import exceptions as core_exceptions
from google.cloud.bigtable.data import BigtableDataClientAsync
import google.cloud.bigtable.data._async.client

TABLE_NAME = "TABLE_NAME"
INSTANCE_NAME = "INSTANCE_NAME"


class TestAsyncExecuteQuery:
    @pytest.fixture()
    def async_channel_mock(self):
        with mock.patch.dict(os.environ, {"BIGTABLE_EMULATOR_HOST": "localhost"}):
            yield ChannelMockAsync()

    @pytest.fixture()
    def async_client(self, async_channel_mock):
        with mock.patch.dict(
            os.environ, {"BIGTABLE_EMULATOR_HOST": "localhost"}
        ), mock.patch.object(
            google.cloud.bigtable.data._async.client,
            "PooledChannel",
            return_value=async_channel_mock,
        ):
            yield BigtableDataClientAsync()

    @pytest.mark.asyncio
    async def test_execute_query(self, async_client, async_channel_mock):
        values = [
            response_with_metadata(),
            response_with_result("test"),
            response_with_result(8, resume_token=b"r1"),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
            response_with_result("test3"),
            response_with_result(None, resume_token=b"r3"),
        ]
        async_channel_mock.set_values(values)
        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert results[0]["a"] == "test"
        assert results[0]["b"] == 8
        assert results[1]["a"] == "test2"
        assert results[1]["b"] == 9
        assert results[2]["a"] == "test3"
        assert results[2]["b"] is None
        assert len(async_channel_mock.execute_query_calls) == 1

    @pytest.mark.asyncio
    async def test_execute_query_with_params(self, async_client, async_channel_mock):
        values = [
            response_with_metadata(),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME} WHERE b=@b",
            INSTANCE_NAME,
            parameters={"b": 9},
        )
        results = [r async for r in result]
        assert len(results) == 1
        assert results[0]["a"] == "test2"
        assert results[0]["b"] == 9
        assert len(async_channel_mock.execute_query_calls) == 1

    @pytest.mark.asyncio
    async def test_execute_query_error_before_metadata(
        self, async_client, async_channel_mock
    ):
        from google.api_core.exceptions import DeadlineExceeded

        values = [
            DeadlineExceeded(""),
            response_with_metadata(),
            response_with_result("test"),
            response_with_result(8, resume_token=b"r1"),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
            response_with_result("test3"),
            response_with_result(None, resume_token=b"r3"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert len(results) == 3
        assert len(async_channel_mock.execute_query_calls) == 2

    @pytest.mark.asyncio
    async def test_execute_query_error_after_metadata(
        self, async_client, async_channel_mock
    ):
        from google.api_core.exceptions import DeadlineExceeded

        values = [
            response_with_metadata(),
            DeadlineExceeded(""),
            response_with_metadata(),
            response_with_result("test"),
            response_with_result(8, resume_token=b"r1"),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
            response_with_result("test3"),
            response_with_result(None, resume_token=b"r3"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert len(results) == 3
        assert len(async_channel_mock.execute_query_calls) == 2
        assert async_channel_mock.resume_tokens == []

    @pytest.mark.asyncio
    async def test_execute_query_with_retries(self, async_client, async_channel_mock):
        from google.api_core.exceptions import DeadlineExceeded

        values = [
            response_with_metadata(),
            response_with_result("test"),
            response_with_result(8, resume_token=b"r1"),
            DeadlineExceeded(""),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
            response_with_result("test3"),
            DeadlineExceeded(""),
            response_with_result("test3"),
            response_with_result(None, resume_token=b"r3"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert results[0]["a"] == "test"
        assert results[0]["b"] == 8
        assert results[1]["a"] == "test2"
        assert results[1]["b"] == 9
        assert results[2]["a"] == "test3"
        assert results[2]["b"] is None
        assert len(async_channel_mock.execute_query_calls) == 3
        assert async_channel_mock.resume_tokens == [b"r1", b"r2"]

    @pytest.mark.parametrize(
        "exception",
        [
            (core_exceptions.DeadlineExceeded("")),
            (core_exceptions.Aborted("")),
            (core_exceptions.ServiceUnavailable("")),
        ],
    )
    @pytest.mark.asyncio
    async def test_execute_query_retryable_error(
        self, async_client, async_channel_mock, exception
    ):
        values = [
            response_with_metadata(),
            response_with_result("test", resume_token=b"t1"),
            exception,
            response_with_result(8, resume_token=b"t2"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert len(results) == 1
        assert len(async_channel_mock.execute_query_calls) == 2
        assert async_channel_mock.resume_tokens == [b"t1"]

    @pytest.mark.asyncio
    async def test_execute_query_retry_partial_row(
        self, async_client, async_channel_mock
    ):
        values = [
            response_with_metadata(),
            response_with_result("test", resume_token=b"t1"),
            core_exceptions.DeadlineExceeded(""),
            response_with_result(8, resume_token=b"t2"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        results = [r async for r in result]
        assert results[0]["a"] == "test"
        assert results[0]["b"] == 8
        assert len(async_channel_mock.execute_query_calls) == 2
        assert async_channel_mock.resume_tokens == [b"t1"]

    @pytest.mark.parametrize(
        "ExceptionType",
        [
            (core_exceptions.InvalidArgument),
            (core_exceptions.FailedPrecondition),
            (core_exceptions.PermissionDenied),
            (core_exceptions.MethodNotImplemented),
            (core_exceptions.Cancelled),
            (core_exceptions.AlreadyExists),
            (core_exceptions.OutOfRange),
            (core_exceptions.DataLoss),
            (core_exceptions.Unauthenticated),
            (core_exceptions.NotFound),
            (core_exceptions.ResourceExhausted),
            (core_exceptions.Unknown),
            (core_exceptions.InternalServerError),
        ],
    )
    @pytest.mark.asyncio
    async def test_execute_query_non_retryable(
        self, async_client, async_channel_mock, ExceptionType
    ):
        values = [
            response_with_metadata(),
            response_with_result("test"),
            response_with_result(8, resume_token=b"r1"),
            ExceptionType(""),
            response_with_result("test2"),
            response_with_result(9, resume_token=b"r2"),
            response_with_result("test3"),
            response_with_result(None, resume_token=b"r3"),
        ]
        async_channel_mock.set_values(values)

        result = await async_client.execute_query(
            f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
        )
        r = await result.__anext__()
        assert r["a"] == "test"
        assert r["b"] == 8

        with pytest.raises(ExceptionType):
            r = await result.__anext__()

        assert len(async_channel_mock.execute_query_calls) == 1
        assert async_channel_mock.resume_tokens == []

    @pytest.mark.asyncio
    async def test_execute_query_metadata_received_multiple_times_detected(
        self, async_client, async_channel_mock
    ):
        values = [
            response_with_metadata(),
            response_with_metadata(),
        ]
        async_channel_mock.set_values(values)

        with pytest.raises(Exception, match="Invalid ExecuteQuery response received"):
            [
                r
                async for r in await async_client.execute_query(
                    f"SELECT a, b FROM {TABLE_NAME}", INSTANCE_NAME
                )
            ]
