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

import copy
import datetime
import os
import re
from unittest import mock
import warnings

import google.api_core.exceptions
import google.cloud.bigquery
import google.cloud.bigquery.table
import pytest

import bigframes
import bigframes.enums
import bigframes.exceptions

from .. import resources

TABLE_REFERENCE = {
    "projectId": "my-project",
    "datasetId": "my_dataset",
    "tableId": "my_table",
}
SCHEMA = {
    "fields": [
        {"name": "col1", "type": "INTEGER"},
        {"name": "col2", "type": "INTEGER"},
        {"name": "col3", "type": "INTEGER"},
        {"name": "col4", "type": "INTEGER"},
    ]
}
CLUSTERED_OR_PARTITIONED_TABLES = [
    pytest.param(
        google.cloud.bigquery.Table.from_api_repr(
            {
                "tableReference": TABLE_REFERENCE,
                "clustering": {
                    "fields": ["col1", "col2"],
                },
                "schema": SCHEMA,
            },
        ),
        id="clustered",
    ),
    pytest.param(
        google.cloud.bigquery.Table.from_api_repr(
            {
                "tableReference": TABLE_REFERENCE,
                "rangePartitioning": {
                    "field": "col1",
                    "range": {
                        "start": 1,
                        "end": 100,
                        "interval": 1,
                    },
                },
                "schema": SCHEMA,
            },
        ),
        id="range-partitioned",
    ),
    pytest.param(
        google.cloud.bigquery.Table.from_api_repr(
            {
                "tableReference": TABLE_REFERENCE,
                "timePartitioning": {
                    "type": "MONTH",
                    "field": "col1",
                },
                "schema": SCHEMA,
            },
        ),
        id="time-partitioned",
    ),
    pytest.param(
        google.cloud.bigquery.Table.from_api_repr(
            {
                "tableReference": TABLE_REFERENCE,
                "clustering": {
                    "fields": ["col1", "col2"],
                },
                "timePartitioning": {
                    "type": "MONTH",
                    "field": "col1",
                },
                "schema": SCHEMA,
            },
        ),
        id="time-partitioned-and-clustered",
    ),
]


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        pytest.param(
            {"engine": "bigquery", "names": []},
            "BigQuery engine does not support these arguments",
            id="with_names",
        ),
        pytest.param(
            {"engine": "bigquery", "dtype": {}},
            "BigQuery engine does not support these arguments",
            id="with_dtype",
        ),
        pytest.param(
            {"engine": "bigquery", "index_col": 5},
            "BigQuery engine only supports a single column name for `index_col`.",
            id="with_index_col_not_str",
        ),
        pytest.param(
            {"engine": "bigquery", "usecols": [1, 2]},
            "BigQuery engine only supports an iterable of strings for `usecols`.",
            id="with_usecols_invalid",
        ),
        pytest.param(
            {"engine": "bigquery", "encoding": "ASCII"},
            "BigQuery engine only supports the following encodings",
            id="with_encoding_invalid",
        ),
    ],
)
def test_read_csv_bq_engine_throws_not_implemented_error(kwargs, match):
    session = resources.create_bigquery_session()

    with pytest.raises(NotImplementedError, match=match):
        session.read_csv("", **kwargs)


@pytest.mark.parametrize(
    ("engine",),
    (
        ("c",),
        ("python",),
        ("pyarrow",),
    ),
)
def test_read_csv_pandas_engines_index_col_sequential_int64_not_supported(engine):
    session = resources.create_bigquery_session()

    with pytest.raises(NotImplementedError, match="index_col"):
        session.read_csv(
            "path/to/csv.csv",
            engine=engine,
            index_col=bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64,
        )


@pytest.mark.parametrize("missing_parts_table_id", [(""), ("table")])
def test_read_gbq_missing_parts(missing_parts_table_id):
    session = resources.create_bigquery_session()

    with pytest.raises(ValueError):
        session.read_gbq(missing_parts_table_id)


def test_read_gbq_cached_table():
    session = resources.create_bigquery_session()
    table_ref = google.cloud.bigquery.TableReference(
        google.cloud.bigquery.DatasetReference("my-project", "my_dataset"),
        "my_table",
    )
    table = google.cloud.bigquery.Table(
        table_ref, (google.cloud.bigquery.SchemaField("col", "INTEGER"),)
    )
    table._properties["location"] = session._location
    table._properties["numRows"] = "1000000000"
    table._properties["location"] = session._location
    session._loader._df_snapshot[table_ref] = (
        datetime.datetime(1999, 1, 2, 3, 4, 5, 678901, tzinfo=datetime.timezone.utc),
        table,
    )

    session.bqclient.get_table.return_value = table
    session.bqclient.query_and_wait.return_value = (
        {"total_count": 3, "distinct_count": 2},
    )

    with pytest.warns(UserWarning, match=re.escape("use_cache=False")):
        df = session.read_gbq("my-project.my_dataset.my_table")

    assert "1999-01-02T03:04:05.678901" in df.sql


@pytest.mark.parametrize("table", CLUSTERED_OR_PARTITIONED_TABLES)
def test_default_index_warning_raised_by_read_gbq(table):
    """Because of the windowing operation to create a default index, row
    filters can't push down to the clustering column.

    Raise an exception in this case so that the user is directed to supply a
    unique index column or filter if possible.

    See internal issue 335727141.
    """
    table = copy.deepcopy(table)
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.return_value = table
    bqclient.query_and_wait.return_value = ({"total_count": 3, "distinct_count": 2},)
    session = resources.create_bigquery_session(bqclient=bqclient)
    table._properties["location"] = session._location

    with pytest.warns(bigframes.exceptions.DefaultIndexWarning):
        session.read_gbq("my-project.my_dataset.my_table")


@pytest.mark.parametrize("table", CLUSTERED_OR_PARTITIONED_TABLES)
def test_default_index_warning_not_raised_by_read_gbq_index_col_sequential_int64(
    table,
):
    """Because of the windowing operation to create a default index, row
    filters can't push down to the clustering column.

    Allow people to use the default index only if they explicitly request it.

    See internal issue 335727141.
    """
    table = copy.deepcopy(table)
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.return_value = table
    bqclient.query_and_wait.return_value = ({"total_count": 4, "distinct_count": 3},)
    session = resources.create_bigquery_session(bqclient=bqclient)
    table._properties["location"] = session._location

    # No warnings raised because we set the option allowing the default indexes.
    with warnings.catch_warnings():
        warnings.simplefilter("error", bigframes.exceptions.DefaultIndexWarning)
        df = session.read_gbq(
            "my-project.my_dataset.my_table",
            index_col=bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64,
        )

    # We expect a window operation because we specificaly requested a sequential index and named it.
    df.index.name = "named_index"
    generated_sql = df.sql.casefold()
    assert "OVER".casefold() in generated_sql
    assert "ROW_NUMBER()".casefold() in generated_sql


@pytest.mark.parametrize(
    ("total_count", "distinct_count"),
    (
        (0, 0),
        (123, 123),
        # Should still have a positive effect, even if the index is not unique.
        (123, 111),
    ),
)
@pytest.mark.parametrize("table", CLUSTERED_OR_PARTITIONED_TABLES)
def test_default_index_warning_not_raised_by_read_gbq_index_col_columns(
    total_count,
    distinct_count,
    table,
):
    table = copy.deepcopy(table)
    table.schema = (
        google.cloud.bigquery.SchemaField("idx_1", "INT64"),
        google.cloud.bigquery.SchemaField("idx_2", "INT64"),
        google.cloud.bigquery.SchemaField("col_1", "INT64"),
        google.cloud.bigquery.SchemaField("col_2", "INT64"),
    )

    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.return_value = table
    bqclient.query_and_wait.return_value = (
        {"total_count": total_count, "distinct_count": distinct_count},
    )
    session = resources.create_bigquery_session(
        bqclient=bqclient, table_schema=table.schema
    )
    table._properties["location"] = session._location

    # No warning raised because there are columns to use as the index.
    with warnings.catch_warnings():
        warnings.simplefilter("error", bigframes.exceptions.DefaultIndexWarning)
        df = session.read_gbq(
            "my-project.my_dataset.my_table", index_col=("idx_1", "idx_2")
        )

    # There should be no analytic operators to prevent row filtering pushdown.
    assert "OVER" not in df.sql
    assert tuple(df.index.names) == ("idx_1", "idx_2")


@pytest.mark.parametrize("table", CLUSTERED_OR_PARTITIONED_TABLES)
def test_default_index_warning_not_raised_by_read_gbq_primary_key(table):
    """If a primary key is set on the table, we use that as the index column
    by default, no error should be raised in this case.

    See internal issue 335727141.
    """
    table = copy.deepcopy(table)
    table.schema = (
        google.cloud.bigquery.SchemaField("pk_1", "INT64"),
        google.cloud.bigquery.SchemaField("pk_2", "INT64"),
        google.cloud.bigquery.SchemaField("col_1", "INT64"),
        google.cloud.bigquery.SchemaField("col_2", "INT64"),
    )

    # TODO(b/305264153): use setter for table_constraints in client library
    # when available.
    table._properties["tableConstraints"] = {
        "primaryKey": {
            "columns": ["pk_1", "pk_2"],
        },
    }
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.return_value = table
    session = resources.create_bigquery_session(
        bqclient=bqclient, table_schema=table.schema
    )
    table._properties["location"] = session._location

    # No warning raised because there is a primary key to use as the index.
    with warnings.catch_warnings():
        warnings.simplefilter("error", bigframes.exceptions.DefaultIndexWarning)
        df = session.read_gbq("my-project.my_dataset.my_table")

    # There should be no analytic operators to prevent row filtering pushdown.
    assert "OVER" not in df.sql
    assert tuple(df.index.names) == ("pk_1", "pk_2")


@pytest.mark.parametrize(
    "not_found_table_id",
    [("unknown.dataset.table"), ("project.unknown.table"), ("project.dataset.unknown")],
)
def test_read_gbq_not_found_tables(not_found_table_id):
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.side_effect = google.api_core.exceptions.NotFound(
        "table not found"
    )
    session = resources.create_bigquery_session(bqclient=bqclient)

    with pytest.raises(google.api_core.exceptions.NotFound):
        session.read_gbq(not_found_table_id)


@pytest.mark.parametrize(
    ("api_name", "query_or_table"),
    [
        ("read_gbq", "project.dataset.table"),
        ("read_gbq_table", "project.dataset.table"),
        ("read_gbq", "SELECT * FROM project.dataset.table"),
        ("read_gbq_query", "SELECT * FROM project.dataset.table"),
    ],
    ids=[
        "read_gbq_on_table",
        "read_gbq_table",
        "read_gbq_on_query",
        "read_gbq_query",
    ],
)
def test_read_gbq_external_table_no_drive_access(api_name, query_or_table):
    session = resources.create_bigquery_session()
    session_query_mock = session.bqclient.query

    def query_mock(query, *args, **kwargs):
        if query.lstrip().startswith("SELECT *"):
            raise google.api_core.exceptions.Forbidden(
                "Access Denied: BigQuery BigQuery: Permission denied while getting Drive credentials."
            )

        return session_query_mock(query, *args, **kwargs)

    session.bqclient.query_and_wait = query_mock

    def get_table_mock(table_ref):
        table = google.cloud.bigquery.Table(
            table_ref, (google.cloud.bigquery.SchemaField("col", "INTEGER"),)
        )
        table._properties["numRows"] = 1000000000
        table._properties["location"] = session._location
        return table

    session.bqclient.get_table = get_table_mock

    api = getattr(session, api_name)
    with pytest.raises(
        google.api_core.exceptions.Forbidden,
        match="Check https://cloud.google.com/bigquery/docs/query-drive-data#Google_Drive_permissions.",
    ):
        api(query_or_table)


@mock.patch.dict(os.environ, {}, clear=True)
def test_session_init_fails_with_no_project():
    with pytest.raises(
        ValueError, match="Project must be set to initialize BigQuery client."
    ):
        bigframes.Session(
            bigframes.BigQueryOptions(
                credentials=mock.Mock(spec=google.auth.credentials.Credentials)
            )
        )
