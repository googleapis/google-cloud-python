# Copyright 2025 Google LLC
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

import pathlib
import typing

from google.cloud import bigquery
import pandas as pd
import pyarrow as pa
import pytest

from bigframes import dtypes
import bigframes.testing.mocks as mocks
import bigframes.testing.utils

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent.parent.parent.parent / "data"


@pytest.fixture(scope="session")
def compiler_session(basic_types_table_schema):
    from bigframes.testing import compiler_session

    # TODO: Check if ordering mode is needed for the tests.
    session = mocks.create_bigquery_session(table_schema=basic_types_table_schema)
    session._executor = compiler_session.SQLCompilerExecutor()
    return session


@pytest.fixture(scope="session")
def basic_types_table_schema() -> typing.Sequence[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("rowindex", "INTEGER"),
        bigquery.SchemaField("int64_col", "INTEGER"),
        bigquery.SchemaField("string_col", "STRING"),
        bigquery.SchemaField("float64_col", "FLOAT"),
        bigquery.SchemaField("bool_col", "BOOLEAN"),
    ]


@pytest.fixture(scope="session")
def scalars_types_pandas_df() -> pd.DataFrame:
    """Returns a pandas DataFrame containing all scalar types and using the `rowindex`
    column as the index."""
    # TODO: add tests for empty dataframes
    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    bigframes.testing.utils.convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    return df


@pytest.fixture(scope="session")
def nested_structs_pandas_df() -> pd.DataFrame:
    """Returns a pandas DataFrame containing STRUCT types and using the `id`
    column as the index."""

    df = pd.read_json(
        DATA_DIR / "nested_structs.jsonl",
        lines=True,
    )
    df = df.set_index("id")

    address_struct_schema = pa.struct(
        [pa.field("city", pa.string()), pa.field("country", pa.string())]
    )
    person_struct_schema = pa.struct(
        [
            pa.field("name", pa.string()),
            pa.field("age", pa.int64()),
            pa.field("address", address_struct_schema),
        ]
    )
    df["person"] = df["person"].astype(pd.ArrowDtype(person_struct_schema))
    return df


@pytest.fixture(scope="session")
def repeated_pandas_df() -> pd.DataFrame:
    """Returns a pandas DataFrame containing LIST types and using the `rowindex`
    column as the index."""

    df = pd.read_json(
        DATA_DIR / "repeated.jsonl",
        lines=True,
    )
    df = df.set_index("rowindex")
    return df


@pytest.fixture(scope="session")
def json_pandas_df() -> pd.DataFrame:
    """Returns a pandas DataFrame containing JSON types and using the `rowindex`
    column as the index."""
    json_data = [
        "null",
        "true",
        "100",
        "0.98",
        '"a string"',
        "[]",
        "[1, 2, 3]",
        '[{"a": 1}, {"a": 2}, {"a": null}, {}]',
        '"100"',
        '{"date": "2024-07-16"}',
        '{"int_value": 2, "null_filed": null}',
        '{"list_data": [10, 20, 30]}',
    ]
    df = pd.DataFrame(
        {
            "json_col": pd.Series(json_data, dtype=dtypes.JSON_DTYPE),
        },
        index=pd.Series(range(len(json_data)), dtype=dtypes.INT_DTYPE),
    )
    return df
