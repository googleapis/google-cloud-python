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

import copy
from typing import Any, Dict, Optional, Union

from google.cloud.bigquery.enums import QueryResultsFormat



class AvroOptions:
    """Options if source format is set to AVRO."""

    _SOURCE_FORMAT = "AVRO"
    _RESOURCE_NAME = "avroOptions"

    def __init__(self):
        self._properties = {}

    @property
    def use_avro_logical_types(self) -> Optional[bool]:
        """[Optional] If sourceFormat is set to 'AVRO', indicates whether to
        interpret logical types as the corresponding BigQuery data type (for
        example, TIMESTAMP), instead of using the raw type (for example,
        INTEGER).

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#AvroOptions.FIELDS.use_avro_logical_types
        """
        return self._properties.get("useAvroLogicalTypes")

    @use_avro_logical_types.setter
    def use_avro_logical_types(self, value):
        self._properties["useAvroLogicalTypes"] = value

    @classmethod
    def from_api_repr(cls, resource: Dict[str, bool]) -> "AvroOptions":
        """Factory: construct an instance from a resource dict.

        Args:
            resource (Dict[str, bool]):
                Definition of a :class:`~.format_options.AvroOptions` instance in
                the same representation as is returned from the API.

        Returns:
            :class:`~.format_options.AvroOptions`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config

    def to_api_repr(self) -> dict:
        """Build an API representation of this object.

        Returns:
            Dict[str, bool]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)


class ParquetOptions:
    """Additional options if the PARQUET source format is used."""

    _SOURCE_FORMAT = "PARQUET"
    _RESOURCE_NAME = "parquetOptions"

    def __init__(self):
        self._properties = {}

    @property
    def enum_as_string(self) -> bool:
        """Indicates whether to infer Parquet ENUM logical type as STRING instead of
        BYTES by default.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#ParquetOptions.FIELDS.enum_as_string
        """
        return self._properties.get("enumAsString")

    @enum_as_string.setter
    def enum_as_string(self, value: bool) -> None:
        self._properties["enumAsString"] = value

    @property
    def enable_list_inference(self) -> bool:
        """Indicates whether to use schema inference specifically for Parquet LIST
        logical type.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#ParquetOptions.FIELDS.enable_list_inference
        """
        return self._properties.get("enableListInference")

    @enable_list_inference.setter
    def enable_list_inference(self, value: bool) -> None:
        self._properties["enableListInference"] = value

    @property
    def map_target_type(self) -> Optional[Union[bool, str]]:
        """Indicates whether to simplify the representation of parquet maps to only show keys and values."""

        return self._properties.get("mapTargetType")

    @map_target_type.setter
    def map_target_type(self, value: str) -> None:
        """Sets the map target type.

        Args:
          value: The map target type (eg ARRAY_OF_STRUCT).
        """
        self._properties["mapTargetType"] = value

    @classmethod
    def from_api_repr(cls, resource: Dict[str, bool]) -> "ParquetOptions":
        """Factory: construct an instance from a resource dict.

        Args:
            resource (Dict[str, bool]):
                Definition of a :class:`~.format_options.ParquetOptions` instance in
                the same representation as is returned from the API.

        Returns:
            :class:`~.format_options.ParquetOptions`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config

    def to_api_repr(self) -> dict:
        """Build an API representation of this object.

        Returns:
            Dict[str, bool]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)


class ArrowSerializationOptions:
    """Options for Arrow payload serialization in query result jobs.

    Args:

        buffer_byte_limit (Optional[int]): Target byte limit for returned Arrow IPC record batches.
        use_int64_timestamp (Optional[bool]): Use Int64 timestamp representation in Arrow schema.
    """

    def __init__(
        self,
        buffer_byte_limit: Optional[int] = None,
        use_int64_timestamp: Optional[bool] = None,
    ):
        self._properties: Dict[str, Any] = {}
        if buffer_byte_limit is not None:
            self.buffer_byte_limit = buffer_byte_limit
        if use_int64_timestamp is not None:
            self.use_int64_timestamp = use_int64_timestamp

    @property
    def buffer_byte_limit(self) -> Optional[int]:
        """Target maximum byte size for returned Arrow IPC record batch buffers."""
        val = self._properties.get("bufferByteLimit")
        return int(val) if val is not None else None

    @buffer_byte_limit.setter
    def buffer_byte_limit(self, value: Optional[int]) -> None:
        if value is not None and value <= 0:
            raise ValueError("buffer_byte_limit must be a positive integer.")
        self._properties["bufferByteLimit"] = str(value) if value is not None else None

    @property
    def use_int64_timestamp(self) -> Optional[bool]:
        """Whether timestamp columns are encoded as 64-bit microsecond integers."""
        return self._properties.get("useInt64Timestamp")

    @use_int64_timestamp.setter
    def use_int64_timestamp(self, value: Optional[bool]) -> None:
        self._properties["useInt64Timestamp"] = value

    @classmethod
    def from_api_repr(cls, resource: Dict[str, Any]) -> "ArrowSerializationOptions":
        """Factory: construct an instance from a resource dict."""
        opts = cls()
        opts._properties = copy.deepcopy(resource)
        return opts

    def to_api_repr(self) -> Dict[str, Any]:
        """Build an API representation of this object."""
        return copy.deepcopy(self._properties)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ArrowSerializationOptions):
            return False
        return self._properties == other._properties

    def __repr__(self) -> str:
        return f"ArrowSerializationOptions({self._properties})"



