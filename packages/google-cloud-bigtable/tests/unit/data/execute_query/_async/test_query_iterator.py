# -*- coding: utf-8 -*-
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

import asyncio
from unittest.mock import Mock
from mock import patch
import pytest
from google.cloud.bigtable.data.execute_query._async.execute_query_iterator import (
    ExecuteQueryIteratorAsync,
)
from google.cloud.bigtable_v2.types.bigtable import ExecuteQueryResponse
from ._testing import TYPE_INT, proto_rows_bytes, split_bytes_into_chunks, async_mock


class MockIteratorAsync:
    def __init__(self, values, delay=None):
        self._values = values
        self.idx = 0
        self._delay = delay

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.idx >= len(self._values):
            raise StopAsyncIteration
        if self._delay is not None:
            await asyncio.sleep(self._delay)
        value = self._values[self.idx]
        self.idx += 1
        return value


@pytest.fixture
def proto_byte_stream():
    proto_rows = [
        proto_rows_bytes({"int_value": 1}, {"int_value": 2}),
        proto_rows_bytes({"int_value": 3}, {"int_value": 4}),
        proto_rows_bytes({"int_value": 5}, {"int_value": 6}),
    ]

    messages = [
        *split_bytes_into_chunks(proto_rows[0], num_chunks=2),
        *split_bytes_into_chunks(proto_rows[1], num_chunks=3),
        proto_rows[2],
    ]

    stream = [
        ExecuteQueryResponse(
            metadata={
                "proto_schema": {
                    "columns": [
                        {"name": "test1", "type_": TYPE_INT},
                        {"name": "test2", "type_": TYPE_INT},
                    ]
                }
            }
        ),
        ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": messages[0]}}),
        ExecuteQueryResponse(
            results={
                "proto_rows_batch": {"batch_data": messages[1]},
                "resume_token": b"token1",
            }
        ),
        ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": messages[2]}}),
        ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": messages[3]}}),
        ExecuteQueryResponse(
            results={
                "proto_rows_batch": {"batch_data": messages[4]},
                "resume_token": b"token2",
            }
        ),
        ExecuteQueryResponse(
            results={
                "proto_rows_batch": {"batch_data": messages[5]},
                "resume_token": b"token3",
            }
        ),
    ]
    return stream


@pytest.mark.asyncio
async def test_iterator(proto_byte_stream):
    client_mock = Mock()

    client_mock._register_instance = async_mock()
    client_mock._remove_instance_registration = async_mock()
    mock_async_iterator = MockIteratorAsync(proto_byte_stream)
    iterator = None

    with patch(
        "google.api_core.retry.retry_target_stream_async",
        return_value=mock_async_iterator,
    ):
        iterator = ExecuteQueryIteratorAsync(
            client=client_mock,
            instance_id="test-instance",
            app_profile_id="test_profile",
            request_body={},
            attempt_timeout=10,
            operation_timeout=10,
            req_metadata=(),
            retryable_excs=[],
        )
    result = []
    async for value in iterator:
        result.append(tuple(value))
    assert result == [(1, 2), (3, 4), (5, 6)]

    assert iterator.is_closed
    client_mock._register_instance.assert_called_once()
    client_mock._remove_instance_registration.assert_called_once()

    assert mock_async_iterator.idx == len(proto_byte_stream)


@pytest.mark.asyncio
async def test_iterator_awaits_metadata(proto_byte_stream):
    client_mock = Mock()

    client_mock._register_instance = async_mock()
    client_mock._remove_instance_registration = async_mock()
    mock_async_iterator = MockIteratorAsync(proto_byte_stream)
    iterator = None
    with patch(
        "google.api_core.retry.retry_target_stream_async",
        return_value=mock_async_iterator,
    ):
        iterator = ExecuteQueryIteratorAsync(
            client=client_mock,
            instance_id="test-instance",
            app_profile_id="test_profile",
            request_body={},
            attempt_timeout=10,
            operation_timeout=10,
            req_metadata=(),
            retryable_excs=[],
        )

    await iterator.metadata()

    assert mock_async_iterator.idx == 1
