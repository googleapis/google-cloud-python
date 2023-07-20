# Copyright 2023 Google LLC
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

import math
from typing import Callable, Optional, Tuple, Union
from unittest import mock

import google.api_core.exceptions
import google.auth
import google.cloud.bigquery as bigquery
import google.cloud.bigquery.table
import google.oauth2.credentials  # type: ignore
import ibis.expr.types as ibis_types
import pandas
import pytest

import bigframes
import bigframes.core
import bigframes.dataframe

SCALARS_TABLE_ID = "project.dataset.scalars_table"


@pytest.fixture
def scalars_pandas_df_default_index() -> pandas.DataFrame:
    # Note: as of 2023-02-07, using nullable dtypes with the ibis pandas
    # backend requires running ibis at HEAD. See:
    # https://github.com/ibis-project/ibis/pull/5345
    return pandas.DataFrame(
        {
            "rowindex": pandas.Series(
                [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                ],
                dtype="Int64",
            ),
            "bool_col": pandas.Series(
                [
                    True,
                    None,
                    False,
                    True,
                    None,
                    False,
                    True,
                    None,
                    False,
                    True,
                ],
                dtype="boolean",
            ),
            "int64_col": pandas.Series(
                [
                    1,
                    2,
                    3,
                    None,
                    0,
                    -1,
                    -2,
                    2**63 - 1,
                    -(2**63),
                    None,
                ],
                dtype="Int64",
            ),
            "float64_col": pandas.Series(
                [
                    None,
                    1,
                    math.pi,
                    math.e * 1e10,
                    0,
                    float("nan"),
                    float("inf"),
                    float("-inf"),
                    -2.23e-308,
                    1.8e308,
                ],
                dtype="Float64",
            ),
            "string_col": pandas.Series(
                [
                    "abc",
                    "XYZ",
                    "aBcDeFgHiJkLmNoPqRsTuVwXyZ",
                    "1_2-3+4=5~6*7/8&9%10#11@12$" "",
                    None,
                    "こんにちは",
                    "你好",
                    "வணக்கம்",
                    "שלום",
                ],
                dtype="string[pyarrow]",
            ),
        }
    )


# We parameterize the fixtures at this point with the real pandas
# dataframes and deferred bigframes dataframes as we have the following
# chain of dependencies:
# -> index/default_index parameterization
# -> pandas dataframe
# -> bqclient mock
# -> session
# -> bigframes dataframe
@pytest.fixture
def scalars_testdata_setup(
    scalars_pandas_df_default_index,
) -> Tuple[
    pandas.DataFrame, Callable[[bigframes.Session], bigframes.dataframe.DataFrame]
]:
    return (
        scalars_pandas_df_default_index.set_index("rowindex"),
        lambda session: session.read_gbq(SCALARS_TABLE_ID, index_col=["rowindex"]),
    )


@pytest.fixture(autouse=True)
def mock_bigquery_client(monkeypatch, scalars_testdata_setup) -> bigquery.Client:
    scalars_pandas_df, _ = scalars_testdata_setup
    mock_client = mock.create_autospec(bigquery.Client)
    # Constructor returns the mock itself, so this mock can be treated as the
    # constructor or the instance.
    mock_client.return_value = mock_client
    mock_client.project = "default-project"
    most_recent_table = None

    def mock_bigquery_client_get_table(
        table_ref: Union[google.cloud.bigquery.table.TableReference, str]
    ):
        global most_recent_table

        if isinstance(table_ref, google.cloud.bigquery.table.TableReference):
            table_name = table_ref.__str__()
        else:
            table_name = table_ref

        schema = [
            {"mode": "NULLABLE", "name": "rowindex", "type": "INTEGER"},
            {
                "mode": "NULLABLE",
                "name": "bigframes_ordering_id",
                "type": "INTEGER",
            },
        ]

        if table_name == SCALARS_TABLE_ID:
            schema += [
                {"mode": "NULLABLE", "name": "bool_col", "type": "BOOL"},
                {"mode": "NULLABLE", "name": "int64_col", "type": "INTEGER"},
                {"mode": "NULLABLE", "name": "float64_col", "type": "FLOAT"},
                {"mode": "NULLABLE", "name": "string_col", "type": "STRING"},
            ]
        else:
            raise google.api_core.exceptions.NotFound("Not Found Table")

        most_recent_table = bigquery.Table(table_name, schema)  # type: ignore
        return most_recent_table  # type: ignore

    def mock_query(
        sql: str,
        job_config: Optional[bigquery.QueryJobConfig] = None,
        location: str = "US",
    ) -> bigquery.QueryJob:
        global most_recent_table

        def mock_result(max_results=None):
            mock_rows = mock.create_autospec(google.cloud.bigquery.table.RowIterator)
            mock_rows.total_rows = len(scalars_pandas_df.index)
            mock_rows.schema = [
                bigquery.SchemaField(name=name, field_type="INT64")
                for name in scalars_pandas_df.columns
            ]
            # Use scalars_pandas_df instead of ibis_expr.execute() to preserve dtypes.
            mock_rows.to_dataframe.return_value = scalars_pandas_df.head(n=max_results)
            return mock_rows

        mock_job = mock.create_autospec(bigquery.QueryJob)
        mock_job.result = mock_result
        return mock_job

    mock_client.get_table = mock_bigquery_client_get_table
    mock_client.query.side_effect = mock_query
    monkeypatch.setattr(bigquery, "Client", mock_client)
    mock_client.reset_mock()
    return mock_client


@pytest.fixture
def session() -> bigframes.Session:
    return bigframes.Session(
        context=bigframes.BigQueryOptions(
            credentials=mock.create_autospec(google.oauth2.credentials.Credentials),
            project="unit-test-project",
        )
    )


@pytest.fixture
def scalars_ibis_table(session) -> ibis_types.Table:
    return session.ibis_client.table(SCALARS_TABLE_ID)
