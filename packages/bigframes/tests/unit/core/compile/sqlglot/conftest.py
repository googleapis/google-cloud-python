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
import bigframes.core as core
import bigframes.pandas as bpd
import bigframes.testing.mocks as mocks
import bigframes.testing.utils

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent.parent.parent.parent / "data"


def _create_compiler_session(table_name, table_schema):
    """Helper function to create a compiler session."""
    from bigframes.testing import compiler_session

    anonymous_dataset = bigquery.DatasetReference.from_string(
        "bigframes-dev.sqlglot_test"
    )
    session = mocks.create_bigquery_session(
        table_name=table_name,
        table_schema=table_schema,
        anonymous_dataset=anonymous_dataset,
    )
    session._executor = compiler_session.SQLCompilerExecutor()
    return session


@pytest.fixture(scope="session")
def compiler_session(scalar_types_table_schema):
    """Compiler session for scalar types."""
    return _create_compiler_session("scalar_types", scalar_types_table_schema)


@pytest.fixture(scope="session")
def compiler_session_w_repeated_types(repeated_types_table_schema):
    """Compiler session for repeated data types."""
    return _create_compiler_session("repeated_types", repeated_types_table_schema)


@pytest.fixture(scope="session")
def compiler_session_w_nested_structs_types(nested_structs_types_table_schema):
    """Compiler session for nested STRUCT data types."""
    return _create_compiler_session(
        "nested_structs_types", nested_structs_types_table_schema
    )


@pytest.fixture(scope="session")
def compiler_session_w_json_types(json_types_table_schema):
    """Compiler session for JSON data types."""
    return _create_compiler_session("json_types", json_types_table_schema)


@pytest.fixture(scope="session")
def scalar_types_table_schema() -> typing.Sequence[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("bool_col", "BOOLEAN"),
        bigquery.SchemaField("bytes_col", "BYTES"),
        bigquery.SchemaField("date_col", "DATE"),
        bigquery.SchemaField("datetime_col", "DATETIME"),
        bigquery.SchemaField("geography_col", "GEOGRAPHY"),
        bigquery.SchemaField("int64_col", "INTEGER"),
        bigquery.SchemaField("int64_too", "INTEGER"),
        bigquery.SchemaField("numeric_col", "NUMERIC"),
        bigquery.SchemaField("float64_col", "FLOAT"),
        bigquery.SchemaField("rowindex", "INTEGER"),
        bigquery.SchemaField("rowindex_2", "INTEGER"),
        bigquery.SchemaField("string_col", "STRING"),
        bigquery.SchemaField("time_col", "TIME"),
        bigquery.SchemaField("timestamp_col", "TIMESTAMP"),
    ]


@pytest.fixture(scope="session")
def scalar_types_df(compiler_session) -> bpd.DataFrame:
    """Returns a BigFrames DataFrame containing all scalar types and using the `rowindex`
    column as the index."""
    bf_df = compiler_session.read_gbq_table("bigframes-dev.sqlglot_test.scalar_types")
    bf_df = bf_df.set_index("rowindex", drop=False)
    return bf_df


@pytest.fixture(scope="session")
def scalar_types_pandas_df() -> pd.DataFrame:
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


@pytest.fixture(scope="module")
def scalar_types_array_value(
    scalar_types_pandas_df: pd.DataFrame, compiler_session: bigframes.Session
) -> core.ArrayValue:
    managed_data_source = core.local_data.ManagedArrowTable.from_pandas(
        scalar_types_pandas_df
    )
    return core.ArrayValue.from_managed(managed_data_source, compiler_session)


@pytest.fixture(scope="session")
def nested_structs_types_table_schema() -> typing.Sequence[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField(
            "people",
            "RECORD",
            fields=[
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("age", "INTEGER"),
                bigquery.SchemaField(
                    "address",
                    "RECORD",
                    fields=[
                        bigquery.SchemaField("city", "STRING"),
                        bigquery.SchemaField("country", "STRING"),
                    ],
                ),
            ],
        ),
    ]


@pytest.fixture(scope="session")
def nested_structs_types_df(compiler_session_w_nested_structs_types) -> bpd.DataFrame:
    """Returns a BigFrames DataFrame containing all scalar types and using the `rowindex`
    column as the index."""
    bf_df = compiler_session_w_nested_structs_types.read_gbq_table(
        "bigframes-dev.sqlglot_test.nested_structs_types"
    )
    bf_df = bf_df.set_index("id", drop=False)
    return bf_df


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
def repeated_types_table_schema() -> typing.Sequence[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("rowindex", "INTEGER"),
        bigquery.SchemaField("int_list_col", "INTEGER", "REPEATED"),
        bigquery.SchemaField("bool_list_col", "BOOLEAN", "REPEATED"),
        bigquery.SchemaField("float_list_col", "FLOAT", "REPEATED"),
        bigquery.SchemaField("date_list_col", "DATE", "REPEATED"),
        bigquery.SchemaField("date_time_list_col", "DATETIME", "REPEATED"),
        bigquery.SchemaField("numeric_list_col", "NUMERIC", "REPEATED"),
        bigquery.SchemaField("string_list_col", "STRING", "REPEATED"),
    ]


@pytest.fixture(scope="session")
def repeated_types_df(compiler_session_w_repeated_types) -> bpd.DataFrame:
    """Returns a BigFrames DataFrame containing all scalar types and using the `rowindex`
    column as the index."""
    bf_df = compiler_session_w_repeated_types.read_gbq_table(
        "bigframes-dev.sqlglot_test.repeated_types"
    )
    bf_df = bf_df.set_index("rowindex", drop=False)
    return bf_df


@pytest.fixture(scope="session")
def repeated_types_pandas_df() -> pd.DataFrame:
    """Returns a pandas DataFrame containing LIST types and using the `rowindex`
    column as the index."""

    df = pd.read_json(
        DATA_DIR / "repeated.jsonl",
        lines=True,
    )
    # TODO: add dtype conversion here if needed.
    df = df.set_index("rowindex")
    return df


@pytest.fixture(scope="session")
def json_types_table_schema() -> typing.Sequence[bigquery.SchemaField]:
    return [
        bigquery.SchemaField("rowindex", "INTEGER"),
        bigquery.SchemaField("json_col", "JSON"),
    ]


@pytest.fixture(scope="session")
def json_types_df(compiler_session_w_json_types) -> bpd.DataFrame:
    """Returns a BigFrames DataFrame containing JSON types and using the `rowindex`
    column as the index."""
    bf_df = compiler_session_w_json_types.read_gbq_table(
        "bigframes-dev.sqlglot_test.json_types"
    )
    # TODO(b/427305807): Why `drop=False` will produce two "rowindex" columns?
    bf_df = bf_df.set_index("rowindex", drop=True)
    return bf_df


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
            "rowindex": pd.Series(range(len(json_data)), dtype=dtypes.INT_DTYPE),
            "json_col": pd.Series(json_data, dtype=dtypes.JSON_DTYPE),
        },
    )
    # TODO(b/427305807): Why `drop=False` will produce two "rowindex" columns?
    df = df.set_index("rowindex", drop=True)
    return df
