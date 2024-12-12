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
from google.cloud.bigtable.data.execute_query._parameters_formatting import (
    _format_execute_query_params,
)
from google.cloud.bigtable.data.execute_query.metadata import SqlType
from google.cloud.bigtable.data.execute_query.values import Struct
import datetime

from google.type import date_pb2
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


timestamp = int(
    datetime.datetime(2024, 5, 12, 17, 44, 12, tzinfo=datetime.timezone.utc).timestamp()
)
dt_micros_non_zero = DatetimeWithNanoseconds(
    2024, 5, 12, 17, 44, 12, 123, nanosecond=0, tzinfo=datetime.timezone.utc
).timestamp_pb()
dt_nanos_zero = DatetimeWithNanoseconds(
    2024, 5, 12, 17, 44, 12, nanosecond=0, tzinfo=datetime.timezone.utc
).timestamp_pb()
dt_nanos_non_zero = DatetimeWithNanoseconds(
    2024, 5, 12, 17, 44, 12, nanosecond=12, tzinfo=datetime.timezone.utc
).timestamp_pb()
pb_date = date_pb2.Date(year=2024, month=5, day=15)


@pytest.mark.parametrize(
    "input_value,value_field,type_field,expected_value",
    [
        (1, "int_value", "int64_type", 1),
        ("2", "string_value", "string_type", "2"),
        (b"3", "bytes_value", "bytes_type", b"3"),
        (True, "bool_value", "bool_type", True),
        (
            datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc),
            "timestamp_value",
            "timestamp_type",
            dt_nanos_zero,
        ),
        (
            datetime.datetime(
                2024, 5, 12, 17, 44, 12, 123, tzinfo=datetime.timezone.utc
            ),
            "timestamp_value",
            "timestamp_type",
            dt_micros_non_zero,
        ),
        (datetime.date(2024, 5, 15), "date_value", "date_type", pb_date),
        (
            DatetimeWithNanoseconds(
                2024, 5, 12, 17, 44, 12, nanosecond=12, tzinfo=datetime.timezone.utc
            ),
            "timestamp_value",
            "timestamp_type",
            dt_nanos_non_zero,
        ),
    ],
)
def test_instance_execute_query_parameters_simple_types_parsing(
    input_value, value_field, type_field, expected_value
):
    result = _format_execute_query_params(
        {
            "test": input_value,
        },
        None,
    )
    assert result["test"][value_field] == expected_value
    assert type_field in result["test"]["type_"]


def test_instance_execute_query_parameters_not_supported_types():
    with pytest.raises(ValueError):
        _format_execute_query_params({"test1": 1.1}, None)

    with pytest.raises(ValueError):
        _format_execute_query_params({"test1": {"a": 1}}, None)

    with pytest.raises(ValueError):
        _format_execute_query_params({"test1": [1]}, None)

    with pytest.raises(ValueError):
        _format_execute_query_params({"test1": Struct([("field1", 1)])}, None)

    with pytest.raises(NotImplementedError, match="not supported"):
        _format_execute_query_params(
            {"test1": {"a": 1}},
            {
                "test1": SqlType.Map(SqlType.String(), SqlType.Int64()),
            },
        )

    with pytest.raises(NotImplementedError, match="not supported"):
        _format_execute_query_params(
            {"test1": [1]},
            {
                "test1": SqlType.Array(SqlType.Int64()),
            },
        )

    with pytest.raises(NotImplementedError, match="not supported"):
        _format_execute_query_params(
            {"test1": Struct([("field1", 1)])},
            {"test1": SqlType.Struct([("field1", SqlType.Int64())])},
        )


def test_instance_execute_query_parameters_not_match():
    with pytest.raises(ValueError, match="test2"):
        _format_execute_query_params(
            {
                "test1": 1,
                "test2": 1,
            },
            {
                "test1": SqlType.Int64(),
                "test2": SqlType.String(),
            },
        )
