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
from unittest import mock
from google.cloud.bigtable_v2.types.bigtable import ExecuteQueryResponse
from google.cloud.bigtable_v2.types.data import Value as PBValue
from google.cloud.bigtable.data.execute_query._reader import _QueryResultRowReader

from google.cloud.bigtable.data.execute_query.metadata import ProtoMetadata, SqlType

import google.cloud.bigtable.data.execute_query._reader
from ._testing import TYPE_INT, proto_rows_bytes


class TestQueryResultRowReader:
    def test__single_values_received(self):
        byte_cursor = mock.Mock(
            metadata=ProtoMetadata(
                [("test1", SqlType.Int64()), ("test2", SqlType.Int64())]
            )
        )
        values = [
            proto_rows_bytes({"int_value": 1}),
            proto_rows_bytes({"int_value": 2}),
            proto_rows_bytes({"int_value": 3}),
        ]

        reader = _QueryResultRowReader(byte_cursor)

        assert reader.consume(values[0]) is None
        result = reader.consume(values[1])
        assert len(result) == 1
        assert len(result[0]) == 2
        assert reader.consume(values[2]) is None

    def test__multiple_rows_received(self):
        values = [
            proto_rows_bytes(
                {"int_value": 1},
                {"int_value": 2},
                {"int_value": 3},
                {"int_value": 4},
            ),
            proto_rows_bytes({"int_value": 5}, {"int_value": 6}),
            proto_rows_bytes({"int_value": 7}, {"int_value": 8}),
        ]

        byte_cursor = mock.Mock(
            metadata=ProtoMetadata(
                [("test1", SqlType.Int64()), ("test2", SqlType.Int64())]
            )
        )

        reader = _QueryResultRowReader(byte_cursor)

        result = reader.consume(values[0])
        assert len(result) == 2
        assert len(result[0]) == 2
        assert result[0][0] == result[0]["test1"] == 1
        assert result[0][1] == result[0]["test2"] == 2

        assert len(result[1]) == 2
        assert result[1][0] == result[1]["test1"] == 3
        assert result[1][1] == result[1]["test2"] == 4

        result = reader.consume(values[1])
        assert len(result) == 1
        assert len(result[0]) == 2
        assert result[0][0] == result[0]["test1"] == 5
        assert result[0][1] == result[0]["test2"] == 6

        result = reader.consume(values[2])
        assert len(result) == 1
        assert len(result[0]) == 2
        assert result[0][0] == result[0]["test1"] == 7
        assert result[0][1] == result[0]["test2"] == 8

    def test__received_values_are_passed_to_parser_in_batches(self):
        byte_cursor = mock.Mock(
            metadata=ProtoMetadata(
                [("test1", SqlType.Int64()), ("test2", SqlType.Int64())]
            )
        )

        assert SqlType.Struct([("a", SqlType.Int64())]) == SqlType.Struct(
            [("a", SqlType.Int64())]
        )
        assert SqlType.Struct([("a", SqlType.String())]) != SqlType.Struct(
            [("a", SqlType.Int64())]
        )
        assert SqlType.Struct([("a", SqlType.Int64())]) != SqlType.Struct(
            [("b", SqlType.Int64())]
        )

        assert SqlType.Array(SqlType.Int64()) == SqlType.Array(SqlType.Int64())
        assert SqlType.Array(SqlType.Int64()) != SqlType.Array(SqlType.String())

        assert SqlType.Map(SqlType.Int64(), SqlType.String()) == SqlType.Map(
            SqlType.Int64(), SqlType.String()
        )
        assert SqlType.Map(SqlType.Int64(), SqlType.String()) != SqlType.Map(
            SqlType.String(), SqlType.String()
        )

        values = [
            {"int_value": 1},
            {"int_value": 2},
        ]

        reader = _QueryResultRowReader(byte_cursor)
        with mock.patch.object(
            google.cloud.bigtable.data.execute_query._reader,
            "_parse_pb_value_to_python_value",
        ) as parse_mock:
            reader.consume(proto_rows_bytes(values[0]))
            parse_mock.assert_not_called()
            reader.consume(proto_rows_bytes(values[1]))
            parse_mock.assert_has_calls(
                [
                    mock.call(PBValue(values[0]), SqlType.Int64()),
                    mock.call(PBValue(values[1]), SqlType.Int64()),
                ]
            )

    def test__parser_errors_are_forwarded(self):
        byte_cursor = mock.Mock(metadata=ProtoMetadata([("test1", SqlType.Int64())]))

        values = [
            {"string_value": "test"},
        ]

        reader = _QueryResultRowReader(byte_cursor)
        with mock.patch.object(
            google.cloud.bigtable.data.execute_query._reader,
            "_parse_pb_value_to_python_value",
            side_effect=ValueError("test"),
        ) as parse_mock:
            with pytest.raises(ValueError, match="test"):
                reader.consume(proto_rows_bytes(values[0]))

            parse_mock.assert_has_calls(
                [
                    mock.call(PBValue(values[0]), SqlType.Int64()),
                ]
            )

    def test__multiple_proto_rows_received_with_one_resume_token(self):
        from google.cloud.bigtable.data.execute_query._byte_cursor import _ByteCursor

        def split_bytes_into_chunks(bytes_to_split, num_chunks):
            from google.cloud.bigtable.helpers import batched

            assert num_chunks <= len(bytes_to_split)
            bytes_per_part = (len(bytes_to_split) - 1) // num_chunks + 1
            result = list(map(bytes, batched(bytes_to_split, bytes_per_part)))
            assert len(result) == num_chunks
            return result

        def pass_values_to_byte_cursor(byte_cursor, iterable):
            for value in iterable:
                result = byte_cursor.consume(value)
                if result is not None:
                    yield result

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
                results={"proto_rows_batch": {"batch_data": messages[1]}}
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
                    "resume_token": b"token1",
                }
            ),
            ExecuteQueryResponse(
                results={
                    "proto_rows_batch": {"batch_data": messages[5]},
                    "resume_token": b"token2",
                }
            ),
        ]

        byte_cursor = _ByteCursor()

        reader = _QueryResultRowReader(byte_cursor)

        byte_cursor_iter = pass_values_to_byte_cursor(byte_cursor, stream)

        returned_values = []

        def intercept_return_values(func):
            nonlocal intercept_return_values

            def wrapped(*args, **kwargs):
                value = func(*args, **kwargs)
                returned_values.append(value)
                return value

            return wrapped

        with mock.patch.object(
            reader,
            "_parse_proto_rows",
            wraps=intercept_return_values(reader._parse_proto_rows),
        ):
            result = reader.consume(next(byte_cursor_iter))

        # Despite the fact that two ProtoRows were received, a single resume_token after the second ProtoRows object forces us to parse them together.
        # We will interpret them as one larger ProtoRows object.
        assert len(returned_values) == 1
        assert len(returned_values[0]) == 4
        assert returned_values[0][0].int_value == 1
        assert returned_values[0][1].int_value == 2
        assert returned_values[0][2].int_value == 3
        assert returned_values[0][3].int_value == 4

        assert len(result) == 2
        assert len(result[0]) == 2
        assert result[0][0] == 1
        assert result[0]["test1"] == 1
        assert result[0][1] == 2
        assert result[0]["test2"] == 2
        assert len(result[1]) == 2
        assert result[1][0] == 3
        assert result[1]["test1"] == 3
        assert result[1][1] == 4
        assert result[1]["test2"] == 4
        assert byte_cursor._resume_token == b"token1"

        returned_values = []
        with mock.patch.object(
            reader,
            "_parse_proto_rows",
            wraps=intercept_return_values(reader._parse_proto_rows),
        ):
            result = reader.consume(next(byte_cursor_iter))

        assert len(result) == 1
        assert len(result[0]) == 2
        assert result[0][0] == 5
        assert result[0]["test1"] == 5
        assert result[0][1] == 6
        assert result[0]["test2"] == 6
        assert byte_cursor._resume_token == b"token2"


class TestProtoMetadata:
    def test__duplicate_column_names(self):
        metadata = ProtoMetadata(
            [
                ("test1", SqlType.Int64()),
                ("test2", SqlType.Bytes()),
                ("test2", SqlType.String()),
            ]
        )
        assert metadata[0].column_name == "test1"
        assert metadata["test1"].column_type == SqlType.Int64()

        # duplicate columns not accesible by name
        with pytest.raises(KeyError, match="Ambigious column name"):
            metadata["test2"]

        # duplicate columns accessible by index
        assert metadata[1].column_type == SqlType.Bytes()
        assert metadata[1].column_name == "test2"
        assert metadata[2].column_type == SqlType.String()
        assert metadata[2].column_name == "test2"
