# Copyright 2019 Google LLC
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

import pyarrow.types
import pytest

from google.cloud.bigquery import schema


@pytest.fixture
def module_under_test():
    from google.cloud.bigquery import _pandas_helpers

    return _pandas_helpers


def is_none(value):
    return value is None


def is_numeric(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#numeric-type
    return all_(
        pyarrow.types.is_decimal,
        lambda type_: type_.precision == 38,
        lambda type_: type_.scale == 9,
    )


def is_timestamp(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#timestamp-type
    return all_(
        pyarrow.types.is_timestamp,
        lambda type_: type_.unit == "us",
        lambda type_: type_.tz == "UTC",
    )


def is_datetime(type_):
    # See: https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#datetime-type
    return all_(
        pyarrow.types.is_timestamp,
        lambda type_: type_.unit == "us",
        lambda type_: type_.tz is None,
    )


def all_(*functions):
    def do_all(value):
        return all((func(value) for func in functions))

    return do_all


@pytest.mark.parametrize(
    "bq_type,bq_mode,is_correct_type",
    [
        ("STRING", "NULLABLE", pyarrow.types.is_string),
        ("STRING", None, pyarrow.types.is_string),
        ("string", "NULLABLE", pyarrow.types.is_string),
        ("StRiNg", "NULLABLE", pyarrow.types.is_string),
        ("BYTES", "NULLABLE", pyarrow.types.is_binary),
        ("INTEGER", "NULLABLE", pyarrow.types.is_int64),
        ("INT64", "NULLABLE", pyarrow.types.is_int64),
        ("FLOAT", "NULLABLE", pyarrow.types.is_float64),
        ("FLOAT64", "NULLABLE", pyarrow.types.is_float64),
        ("NUMERIC", "NULLABLE", is_numeric),
        ("BOOLEAN", "NULLABLE", pyarrow.types.is_boolean),
        ("BOOL", "NULLABLE", pyarrow.types.is_boolean),
        ("TIMESTAMP", "NULLABLE", is_timestamp),
        ("DATE", "NULLABLE", pyarrow.types.is_date32),
        ("TIME", "NULLABLE", pyarrow.types.is_time64),
        ("DATETIME", "NULLABLE", is_datetime),
        ("GEOGRAPHY", "NULLABLE", pyarrow.types.is_string),
        # TODO: Use pyarrow.struct(fields) for record (struct) fields.
        ("RECORD", "NULLABLE", is_none),
        ("STRUCT", "NULLABLE", is_none),
        # TODO: Use pyarrow.list_(item_type) for repeated (array) fields.
        ("STRING", "REPEATED", is_none),
        ("STRING", "repeated", is_none),
        ("STRING", "RePeAtEd", is_none),
        ("BYTES", "REPEATED", is_none),
        ("INTEGER", "REPEATED", is_none),
        ("INT64", "REPEATED", is_none),
        ("FLOAT", "REPEATED", is_none),
        ("FLOAT64", "REPEATED", is_none),
        ("NUMERIC", "REPEATED", is_none),
        ("BOOLEAN", "REPEATED", is_none),
        ("BOOL", "REPEATED", is_none),
        ("TIMESTAMP", "REPEATED", is_none),
        ("DATE", "REPEATED", is_none),
        ("TIME", "REPEATED", is_none),
        ("DATETIME", "REPEATED", is_none),
        ("GEOGRAPHY", "REPEATED", is_none),
        ("RECORD", "REPEATED", is_none),
    ],
)
def test_bq_to_arrow_data_type(module_under_test, bq_type, bq_mode, is_correct_type):
    field = schema.SchemaField("ignored_name", bq_type, mode=bq_mode)
    got = module_under_test.bq_to_arrow_data_type(field)
    assert is_correct_type(got)
