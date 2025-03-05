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

import pandas
import pytest

from bigframes.functions import _function_session as bff_session
from bigframes.functions._utils import get_python_version
import bigframes.pandas as bpd
from tests.system.utils import cleanup_function_assets

bpd.options.experiments.udf = True


@pytest.mark.skipif(
    get_python_version() not in bff_session._MANAGED_FUNC_PYTHON_VERSIONS,
    reason=f"Supported version: {bff_session._MANAGED_FUNC_PYTHON_VERSIONS}",
)
def test_managed_function_multiply_with_ibis(
    session,
    scalars_table_id,
    bigquery_client,
    ibis_client,
    dataset_id,
):

    try:

        @session.udf(
            input_types=[int, int],
            output_type=int,
            dataset=dataset_id,
        )
        def multiply(x, y):
            return x * y

        _, dataset_name, table_name = scalars_table_id.split(".")
        if not ibis_client.dataset:
            ibis_client.dataset = dataset_name

        col_name = "int64_col"
        table = ibis_client.tables[table_name]
        table = table.filter(table[col_name].notnull()).order_by("rowindex").head(10)
        sql = table.compile()
        pandas_df_orig = bigquery_client.query(sql).to_dataframe()

        col = table[col_name]
        col_2x = multiply(col, 2).name("int64_col_2x")
        col_square = multiply(col, col).name("int64_col_square")
        table = table.mutate([col_2x, col_square])
        sql = table.compile()
        pandas_df_new = bigquery_client.query(sql).to_dataframe()

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name] * 2,
            pandas_df_new["int64_col_2x"],
            check_names=False,
        )

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name] * pandas_df_orig[col_name],
            pandas_df_new["int64_col_square"],
            check_names=False,
        )
    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(multiply, bigquery_client)


@pytest.mark.skipif(
    get_python_version() not in bff_session._MANAGED_FUNC_PYTHON_VERSIONS,
    reason=f"Supported version: {bff_session._MANAGED_FUNC_PYTHON_VERSIONS}",
)
def test_managed_function_stringify_with_ibis(
    session,
    scalars_table_id,
    bigquery_client,
    ibis_client,
    dataset_id,
):
    try:

        @session.udf(
            input_types=[int],
            output_type=str,
            dataset=dataset_id,
        )
        def stringify(x):
            return f"I got {x}"

        # Function should work locally.
        assert stringify(8912) == "I got 8912"

        _, dataset_name, table_name = scalars_table_id.split(".")
        if not ibis_client.dataset:
            ibis_client.dataset = dataset_name

        col_name = "int64_col"
        table = ibis_client.tables[table_name]
        table = table.filter(table[col_name].notnull()).order_by("rowindex").head(10)
        sql = table.compile()
        pandas_df_orig = bigquery_client.query(sql).to_dataframe()

        col = table[col_name]
        col_2x = stringify.ibis_node(col).name("int64_str_col")
        table = table.mutate([col_2x])
        sql = table.compile()
        pandas_df_new = bigquery_client.query(sql).to_dataframe()

        pandas.testing.assert_series_equal(
            pandas_df_orig[col_name].apply(lambda x: f"I got {x}"),
            pandas_df_new["int64_str_col"],
            check_names=False,
        )
    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            bigquery_client, session.cloudfunctionsclient, stringify
        )


@pytest.mark.skipif(
    get_python_version() not in bff_session._MANAGED_FUNC_PYTHON_VERSIONS,
    reason=f"Supported version: {bff_session._MANAGED_FUNC_PYTHON_VERSIONS}",
)
def test_managed_function_binop(session, scalars_dfs, dataset_id):
    try:

        def func(x, y):
            return x * abs(y % 4)

        managed_func = session.udf(
            input_types=[str, int],
            output_type=str,
            dataset=dataset_id,
        )(func)

        scalars_df, scalars_pandas_df = scalars_dfs

        scalars_df = scalars_df.dropna()
        scalars_pandas_df = scalars_pandas_df.dropna()
        pd_result = scalars_pandas_df["string_col"].combine(
            scalars_pandas_df["int64_col"], func
        )
        bf_result = (
            scalars_df["string_col"]
            .combine(scalars_df["int64_col"], managed_func)
            .to_pandas()
        )
        pandas.testing.assert_series_equal(bf_result, pd_result)
    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            session.bqclient, session.cloudfunctionsclient, managed_func
        )
