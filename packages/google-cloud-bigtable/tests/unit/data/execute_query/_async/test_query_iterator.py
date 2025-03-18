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

from google.cloud.bigtable.data import exceptions
from google.cloud.bigtable.data.execute_query.metadata import (
    _pb_metadata_to_metadata_types,
)
import pytest
import concurrent.futures
from ..sql_helpers import (
    chunked_responses,
    int_val,
    column,
    metadata,
    int64_type,
)

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
        stream = [
            *chunked_responses(2, int_val(1), int_val(2), token=b"token1"),
            *chunked_responses(3, int_val(3), int_val(4), token=b"token2"),
            *chunked_responses(1, int_val(5), int_val(6), token=b"token3"),
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
                prepare_metadata=_pb_metadata_to_metadata_types(
                    metadata(
                        column("test1", int64_type()), column("test2", int64_type())
                    )
                ),
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
    async def test_iterator_returns_metadata_after_data(self, proto_byte_stream):
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
                prepare_metadata=_pb_metadata_to_metadata_types(
                    metadata(
                        column("test1", int64_type()), column("test2", int64_type())
                    )
                ),
                attempt_timeout=10,
                operation_timeout=10,
                req_metadata=(),
                retryable_excs=[],
            )

        await CrossSync.next(iterator)
        assert len(iterator.metadata) == 2

        assert mock_async_iterator.idx == 2

    @CrossSync.pytest
    async def test_iterator_throws_error_on_close_w_bufferred_data(self):
        client_mock = mock.Mock()

        client_mock._register_instance = CrossSync.Mock()
        client_mock._remove_instance_registration = CrossSync.Mock()
        stream = [
            *chunked_responses(2, int_val(1), int_val(2), token=b"token1"),
            *chunked_responses(3, int_val(3), int_val(4), token=b"token2"),
            # Remove the last response, which has the token. We expect this
            # to cause the call to close within _next_impl_ to fail
            chunked_responses(2, int_val(5), int_val(6), token=b"token3")[0],
        ]
        mock_async_iterator = MockIterator(stream)
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
                prepare_metadata=_pb_metadata_to_metadata_types(
                    metadata(
                        column("test1", int64_type()), column("test2", int64_type())
                    )
                ),
                attempt_timeout=10,
                operation_timeout=10,
                req_metadata=(),
                retryable_excs=[],
            )
        i = 0
        async for row in iterator:
            i += 1
            if i == 2:
                break
        with pytest.raises(
            ValueError,
            match="Unexpected buffered data at end of executeQuery reqest",
        ):
            await CrossSync.next(iterator)

    @CrossSync.pytest
    async def test_iterator_handles_reset(self):
        client_mock = mock.Mock()

        client_mock._register_instance = CrossSync.Mock()
        client_mock._remove_instance_registration = CrossSync.Mock()
        stream = [
            # Expect this to be dropped by reset
            *chunked_responses(2, int_val(1), int_val(2)),
            *chunked_responses(3, int_val(3), int_val(4), reset=True),
            *chunked_responses(2, int_val(5), int_val(6), reset=False, token=b"token1"),
            # Only send first of two responses so that there is no checksum
            # expect to be reset
            chunked_responses(2, int_val(10), int_val(12))[0],
            *chunked_responses(2, int_val(7), int_val(8), token=b"token2"),
        ]
        mock_async_iterator = MockIterator(stream)
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
                prepare_metadata=_pb_metadata_to_metadata_types(
                    metadata(
                        column("test1", int64_type()), column("test2", int64_type())
                    )
                ),
                attempt_timeout=10,
                operation_timeout=10,
                req_metadata=(),
                retryable_excs=[],
            )
        results = []
        async for value in iterator:
            results.append(value)
        assert len(results) == 3
        [row1, row2, row3] = results
        assert row1["test1"] == 3
        assert row1["test2"] == 4
        assert row2["test1"] == 5
        assert row2["test2"] == 6
        assert row3["test1"] == 7
        assert row3["test2"] == 8

    @CrossSync.pytest
    async def test_iterator_returns_error_if_metadata_requested_too_early(
        self, proto_byte_stream
    ):
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
                prepare_metadata=_pb_metadata_to_metadata_types(
                    metadata(
                        column("test1", int64_type()), column("test2", int64_type())
                    )
                ),
                attempt_timeout=10,
                operation_timeout=10,
                req_metadata=(),
                retryable_excs=[],
            )

        with pytest.raises(exceptions.EarlyMetadataCallError):
            iterator.metadata
