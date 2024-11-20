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

import pytest
import concurrent.futures
from google.cloud.bigtable_v2.types.bigtable import ExecuteQueryResponse
from .._testing import TYPE_INT, split_bytes_into_chunks, proto_rows_bytes

from google.cloud.bigtable.data._cross_sync import CrossSync

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock  # type: ignore


__CROSS_SYNC_OUTPUT__ = (
    "tests.unit.data.execute_query._sync_autogen.test_query_iterator"
)


@CrossSync.convert_class(sync_name="MockIterator")
class MockIterator:
    def __init__(self, values, delay=None):
        self._values = values
        self.idx = 0
        self._delay = delay

    @CrossSync.convert(sync_name="__iter__")
    def __aiter__(self):
        return self

    @CrossSync.convert(sync_name="__next__")
    async def __anext__(self):
        if self.idx >= len(self._values):
            raise CrossSync.StopIteration
        if self._delay is not None:
            await CrossSync.sleep(self._delay)
        value = self._values[self.idx]
        self.idx += 1
        return value


@CrossSync.convert_class(sync_name="TestQueryIterator")
class TestQueryIteratorAsync:
    @staticmethod
    def _target_class():
        return CrossSync.ExecuteQueryIterator

    def _make_one(self, *args, **kwargs):
        return self._target_class()(*args, **kwargs)

    @pytest.fixture
    def proto_byte_stream(self):
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
            ExecuteQueryResponse(
                results={"proto_rows_batch": {"batch_data": messages[0]}}
            ),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": messages[1]},
                    "resume_token": b"token1",
                }
            ),
            ExecuteQueryResponse(
                results={"proto_rows_batch": {"batch_data": messages[2]}}
            ),
            ExecuteQueryResponse(
                results={"proto_rows_batch": {"batch_data": messages[3]}}
            ),
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

    @CrossSync.pytest
    async def test_iterator(self, proto_byte_stream):
        client_mock = mock.Mock()

        client_mock._register_instance = CrossSync.Mock()
        client_mock._remove_instance_registration = CrossSync.Mock()
        client_mock._executor = concurrent.futures.ThreadPoolExecutor()
        mock_async_iterator = MockIterator(proto_byte_stream)
        iterator = None

        with mock.patch.object(
            CrossSync,
            "retry_target_stream",
            return_value=mock_async_iterator,
        ):
            iterator = self._make_one(
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

    @CrossSync.pytest
    async def test_iterator_awaits_metadata(self, proto_byte_stream):
        client_mock = mock.Mock()

        client_mock._register_instance = CrossSync.Mock()
        client_mock._remove_instance_registration = CrossSync.Mock()
        mock_async_iterator = MockIterator(proto_byte_stream)
        iterator = None
        with mock.patch.object(
            CrossSync,
            "retry_target_stream",
            return_value=mock_async_iterator,
        ):
            iterator = self._make_one(
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
