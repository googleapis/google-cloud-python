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

from google.cloud.bigtable_v2.types.bigtable import ExecuteQueryResponse
from google.cloud.bigtable.data.execute_query._byte_cursor import _ByteCursor

from ._testing import TYPE_INT


def pass_values_to_byte_cursor(byte_cursor, iterable):
    for value in iterable:
        result = byte_cursor.consume(value)
        if result is not None:
            yield result


class TestByteCursor:
    def test__proto_rows_batch__complete_data(self):
        byte_cursor = _ByteCursor()
        stream = [
            ExecuteQueryResponse(
                metadata={
                    "proto_schema": {"columns": [{"name": "test1", "type_": TYPE_INT}]}
                }
            ),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"123"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"456"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"789"}}),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"0"},
                    "resume_token": b"token1",
                }
            ),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"abc"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"def"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"ghi"}}),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"j"},
                    "resume_token": b"token2",
                }
            ),
        ]
        assert byte_cursor.metadata is None
        byte_cursor_iter = pass_values_to_byte_cursor(byte_cursor, stream)
        value = next(byte_cursor_iter)
        assert value == b"1234567890"
        assert byte_cursor._resume_token == b"token1"
        assert byte_cursor.metadata.columns[0].column_name == "test1"

        value = next(byte_cursor_iter)
        assert value == b"abcdefghij"
        assert byte_cursor._resume_token == b"token2"

    def test__proto_rows_batch__empty_proto_rows_batch(self):
        byte_cursor = _ByteCursor()
        stream = [
            ExecuteQueryResponse(
                metadata={
                    "proto_schema": {"columns": [{"name": "test1", "type_": TYPE_INT}]}
                }
            ),
            ExecuteQueryResponse(
                results={"proto_rows_batch": {}, "resume_token": b"token1"}
            ),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"123"}}),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"0"},
                    "resume_token": b"token2",
                }
            ),
        ]

        byte_cursor_iter = pass_values_to_byte_cursor(byte_cursor, stream)
        value = next(byte_cursor_iter)
        assert value == b"1230"
        assert byte_cursor._resume_token == b"token2"

    def test__proto_rows_batch__no_proto_rows_batch(self):
        byte_cursor = _ByteCursor()
        stream = [
            ExecuteQueryResponse(
                metadata={
                    "proto_schema": {"columns": [{"name": "test1", "type_": TYPE_INT}]}
                }
            ),
            ExecuteQueryResponse(results={"resume_token": b"token1"}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"123"}}),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"0"},
                    "resume_token": b"token2",
                }
            ),
        ]

        byte_cursor_iter = pass_values_to_byte_cursor(byte_cursor, stream)
        value = next(byte_cursor_iter)
        assert value == b"1230"
        assert byte_cursor._resume_token == b"token2"

    def test__proto_rows_batch__no_resume_token_at_the_end_of_stream(self):
        byte_cursor = _ByteCursor()
        stream = [
            ExecuteQueryResponse(
                metadata={
                    "proto_schema": {"columns": [{"name": "test1", "type_": TYPE_INT}]}
                }
            ),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"0"},
                    "resume_token": b"token1",
                }
            ),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"abc"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"def"}}),
            ExecuteQueryResponse(results={"proto_rows_batch": {"batch_data": b"ghi"}}),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": b"j"},
                }
            ),
        ]
        assert byte_cursor.metadata is None
        assert byte_cursor.consume(stream[0]) is None
        value = byte_cursor.consume(stream[1])
        assert value == b"0"
        assert byte_cursor._resume_token == b"token1"
        assert byte_cursor.metadata.columns[0].column_name == "test1"

        assert byte_cursor.consume(stream[2]) is None
        assert byte_cursor.consume(stream[3]) is None
        assert byte_cursor.consume(stream[3]) is None
        assert byte_cursor.consume(stream[4]) is None
        assert byte_cursor.consume(stream[5]) is None
