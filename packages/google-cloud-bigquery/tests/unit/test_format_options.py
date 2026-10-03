# Copyright 2021 Google LLC
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


class TestAvroOptions:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.format_options import AvroOptions

        return AvroOptions

    def test_ctor(self):
        config = self._get_target_class()()
        assert config.use_avro_logical_types is None

    def test_from_api_repr(self):
        config = self._get_target_class().from_api_repr({"useAvroLogicalTypes": True})
        assert config.use_avro_logical_types

    def test_to_api_repr(self):
        config = self._get_target_class()()
        config.use_avro_logical_types = False

        result = config.to_api_repr()
        assert result == {"useAvroLogicalTypes": False}


class TestParquetOptions:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.format_options import ParquetOptions

        return ParquetOptions

    def test_ctor(self):
        config = self._get_target_class()()
        assert config.enum_as_string is None
        assert config.enable_list_inference is None

    def test_from_api_repr(self):
        config = self._get_target_class().from_api_repr(
            {"enumAsString": False, "enableListInference": True}
        )
        assert not config.enum_as_string
        assert config.enable_list_inference
        assert config.map_target_type is None

    def test_to_api_repr(self):
        config = self._get_target_class()()
        config.enum_as_string = True
        config.enable_list_inference = False
        config.map_target_type = "ARRAY_OF_STRUCT"

        result = config.to_api_repr()
        assert result == {
            "enumAsString": True,
            "enableListInference": False,
            "mapTargetType": "ARRAY_OF_STRUCT",
        }


class TestQueryResultsFormat:
    def test_values(self):
        from google.cloud.bigquery.format_options import QueryResultsFormat

        assert QueryResultsFormat.STRUCT_ENCODING == "STRUCT_ENCODING"
        assert QueryResultsFormat.ARROW == "ARROW"


class TestArrowSerializationOptions:
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.format_options import ArrowSerializationOptions

        return ArrowSerializationOptions

    def test_ctor_and_properties(self):
        opts = self._get_target_class()(buffer_byte_limit=1048576, use_int64_timestamp=True)
        assert opts.buffer_byte_limit == 1048576
        assert opts.use_int64_timestamp is True

    def test_setters(self):
        opts = self._get_target_class()()
        opts.buffer_byte_limit = 2048576
        opts.use_int64_timestamp = False
        assert opts.buffer_byte_limit == 2048576
        assert opts.use_int64_timestamp is False

    def test_from_api_repr(self):
        opts = self._get_target_class().from_api_repr(
            {"bufferByteLimit": "1048576", "useInt64Timestamp": True}
        )
        assert opts.buffer_byte_limit == 1048576
        assert opts.use_int64_timestamp is True

    def test_to_api_repr(self):
        opts = self._get_target_class()(buffer_byte_limit=1048576, use_int64_timestamp=True)
        assert opts.to_api_repr() == {
            "bufferByteLimit": "1048576",
            "useInt64Timestamp": True,
        }


class TestArrowQueryResult:
    def test_properties(self):
        from google.cloud.bigquery.table import ArrowQueryResult
        import unittest.mock

        mock_table = unittest.mock.MagicMock()
        mock_table.__len__.return_value = 100

        result = ArrowQueryResult(
            table=mock_table,
            query_id="query_123",
            job_id="job_abc",
            job_creation_reason="JOB_CREATION_OPTIONAL",
            total_rows=100,
        )

        assert result.table == mock_table
        assert result.query_id == "query_123"
        assert result.job_id == "job_abc"
        assert result.job_creation_reason == "JOB_CREATION_OPTIONAL"
        assert result.total_rows == 100
        assert len(result) == 100


