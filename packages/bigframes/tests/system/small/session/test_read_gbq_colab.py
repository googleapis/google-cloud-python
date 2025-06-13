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

"""System tests for read_gbq_colab helper functions."""

import numpy
import pandas
import pandas.testing
import pytest


def test_read_gbq_colab_to_pandas_batches_preserves_order_by(maybe_ordered_session):
    # This query should return enough results to be too big to fit in a single
    # page from jobs.query.
    executions_before_sql = maybe_ordered_session._metrics.execution_count
    df = maybe_ordered_session._read_gbq_colab(
        """
        SELECT
            name,
            state,
            gender,
            year,
            SUM(number) AS total
        FROM
            `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state LIKE 'W%'
        GROUP BY name, state, gender, year
        ORDER BY total DESC
        """
    )
    executions_before_python = maybe_ordered_session._metrics.execution_count
    batches = df.to_pandas_batches(
        page_size=100,
    )
    executions_after = maybe_ordered_session._metrics.execution_count

    num_batches = 0
    for batch in batches:
        assert batch["total"].is_monotonic_decreasing
        assert len(batch.index) == 100
        num_batches += 1

        # Only test the first few pages to avoid downloading unnecessary data
        # and so we can confirm we have full pages in each batch.
        if num_batches >= 3:
            break

    assert executions_after == executions_before_python == executions_before_sql + 1


def test_read_gbq_colab_peek_avoids_requery(maybe_ordered_session):
    executions_before_sql = maybe_ordered_session._metrics.execution_count
    df = maybe_ordered_session._read_gbq_colab(
        """
        SELECT
            name,
            SUM(number) AS total
        FROM
            `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state LIKE 'W%'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 300
        """
    )
    executions_before_python = maybe_ordered_session._metrics.execution_count
    result = df.peek(100)
    executions_after = maybe_ordered_session._metrics.execution_count

    # Ok, this isn't guaranteed by peek, but should happen with read api based impl
    # if starts failing, maybe stopped using read api?
    assert result["total"].is_monotonic_decreasing

    assert len(result) == 100
    assert executions_after == executions_before_python == executions_before_sql + 1


def test_read_gbq_colab_repr_avoids_requery(maybe_ordered_session):
    executions_before_sql = maybe_ordered_session._metrics.execution_count
    df = maybe_ordered_session._read_gbq_colab(
        """
        SELECT
            name,
            SUM(number) AS total
        FROM
            `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state LIKE 'W%'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 300
        """
    )
    executions_before_python = maybe_ordered_session._metrics.execution_count
    _ = repr(df)
    executions_after = maybe_ordered_session._metrics.execution_count
    assert executions_after == executions_before_python == executions_before_sql + 1


def test_read_gbq_colab_includes_formatted_scalars(session):
    pyformat_args = {
        "some_integer": 123,
        "some_string": "This could be dangerous, but we escape it",
        # This is not a supported type, but ignored if not referenced.
        "some_object": object(),
    }

    # This query should return few enough results to be small enough to fit in a
    # single page from jobs.query.
    df = session._read_gbq_colab(
        """
        SELECT {some_integer} as some_integer,
        {some_string} as some_string,
        '{{escaped}}' as escaped
        """,
        pyformat_args=pyformat_args,
    )
    result = df.to_pandas()
    pandas.testing.assert_frame_equal(
        result,
        pandas.DataFrame(
            {
                "some_integer": pandas.Series([123], dtype=pandas.Int64Dtype()),
                "some_string": pandas.Series(
                    ["This could be dangerous, but we escape it"],
                    dtype="string[pyarrow]",
                ),
                "escaped": pandas.Series(["{escaped}"], dtype="string[pyarrow]"),
            }
        ),
        check_index_type=False,  # int64 vs Int64
    )


@pytest.mark.skipif(
    pandas.__version__.startswith("1."), reason="bad left join in pandas 1.x"
)
def test_read_gbq_colab_includes_formatted_dataframes(
    session, scalars_df_index, scalars_pandas_df_index
):
    pd_df = pandas.DataFrame(
        {
            "rowindex": [0, 1, 2, 3, 4, 5],
            "value": [0, 100, 200, 300, 400, 500],
        }
    )

    # Make sure we test with some data that is too large to inline as SQL.
    pd_df_large = pandas.DataFrame(
        {
            "rowindex": numpy.arange(100_000),
            "large_value": numpy.arange(100_000),
        }
    )

    pyformat_args = {
        # Apply some operations to make sure the columns aren't renamed.
        "bf_df": scalars_df_index[scalars_df_index["int64_col"] > 0].assign(
            int64_col=scalars_df_index["int64_too"]
        ),
        "pd_df": pd_df,
        "pd_df_large": pd_df_large,
        # This is not a supported type, but ignored if not referenced.
        "some_object": object(),
    }
    sql = """
    SELECT bf_df.int64_col + pd_df.value + pd_df_large.large_value AS int64_col,
    COALESCE(bf_df.rowindex, pd_df.rowindex, pd_df_large.rowindex) AS rowindex
    FROM {bf_df} AS bf_df
    FULL OUTER JOIN {pd_df} AS pd_df
    ON bf_df.rowindex = pd_df.rowindex
    LEFT JOIN {pd_df_large} AS pd_df_large
    ON bf_df.rowindex = pd_df_large.rowindex
    ORDER BY rowindex ASC
    """

    # Do the dry run first so that we don't re-use the uploaded data from the
    # real query.
    dry_run_output = session._read_gbq_colab(
        sql,
        pyformat_args=pyformat_args,
        dry_run=True,
    )

    df = session._read_gbq_colab(
        sql,
        pyformat_args=pyformat_args,
    )

    # Confirm that dry_run was accurate.
    pandas.testing.assert_series_equal(
        pandas.Series(dry_run_output["columnDtypes"]),
        df.dtypes,
    )

    result = df.to_pandas()
    expected = (
        scalars_pandas_df_index[scalars_pandas_df_index["int64_col"] > 0]
        .assign(int64_col=scalars_pandas_df_index["int64_too"])
        .reset_index(drop=False)[["int64_col", "rowindex"]]
        .merge(
            pd_df,
            on="rowindex",
            how="outer",
        )
        .merge(
            pd_df_large,
            on="rowindex",
            how="left",
        )
        .assign(
            int64_col=lambda df: (
                df["int64_col"] + df["value"] + df["large_value"]
            ).astype("Int64")
        )
        .drop(columns=["value", "large_value"])
        .sort_values(by="rowindex")
        .reset_index(drop=True)
    )
    pandas.testing.assert_frame_equal(
        result,
        expected,
        check_index_type=False,  # int64 vs Int64
    )


@pytest.mark.parametrize(
    ("pd_df",),
    (
        pytest.param(
            pandas.DataFrame(
                {
                    "rowindex": [0, 1, 2, 3, 4, 5],
                    "value": [0, 100, 200, 300, 400, 500],
                    "value2": [-1, -2, -3, -4, -5, -6],
                }
            ),
            id="inline-df",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    # Make sure we test with some data that is too large to
                    # inline as SQL.
                    "rowindex": numpy.arange(100_000),
                    "value": numpy.arange(100_000),
                    "value2": numpy.arange(100_000),
                }
            ),
            id="large-df",
        ),
    ),
)
def test_read_gbq_colab_with_formatted_dataframe_deduplicates_column_names_just_like_to_gbq(
    session,
    pd_df,
):
    # Create duplicate column names.
    pd_df.columns = ["rowindex", "value", "value"]

    pyformat_args = {
        "pd_df": pd_df,
    }
    sql = """
    SELECT rowindex, value, value_1
    FROM {pd_df}
    """

    # Do the dry run first so that we don't re-use the uploaded data from the
    # real query.
    dry_run_output = session._read_gbq_colab(
        sql,
        pyformat_args=pyformat_args,
        dry_run=True,
    )

    df = session._read_gbq_colab(
        sql,
        pyformat_args=pyformat_args,
    )

    # Confirm that dry_run was accurate.
    pandas.testing.assert_series_equal(
        pandas.Series(dry_run_output["columnDtypes"]),
        df.dtypes,
    )

    # Make sure the query doesn't fail.
    df.to_pandas_batches()

    # Make sure the
    table_id = session.read_pandas(pd_df).to_gbq()
    table = session.bqclient.get_table(table_id)
    assert [field.name for field in table.schema] == ["rowindex", "value", "value_1"]
