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

import google.api_core.exceptions
import pandas as pd
import pytest

import bigframes.exceptions
from bigframes.functions import _function_session as bff_session
from bigframes.functions import function as bff
from bigframes.functions._utils import get_python_version
from bigframes.pandas import udf
import bigframes.pandas as bpd
import bigframes.series
from tests.system.utils import assert_pandas_df_equal, get_function_name

pytestmark = pytest.mark.skipif(
    get_python_version() not in bff_session._MANAGED_FUNC_PYTHON_VERSIONS,
    reason=f"Supported version: {bff_session._MANAGED_FUNC_PYTHON_VERSIONS}",
)


bpd.options.experiments.udf = True


@pytest.mark.parametrize(
    ("typ",),
    [
        pytest.param(int),
        pytest.param(float),
        pytest.param(bool),
        pytest.param(str),
        pytest.param(bytes),
    ],
)
def test_managed_function_series_apply(
    session,
    typ,
    scalars_dfs,
    dataset_id_permanent,
):
    def foo(x):
        # The bytes() constructor expects a non-negative interger as its arg.
        return typ(abs(x))

    foo = udf(
        input_types=int,
        output_type=typ,
        dataset=dataset_id_permanent,
        name=get_function_name(foo),
    )(foo)

    # Function should still work normally.
    assert foo(-2) == typ(2)

    assert hasattr(foo, "bigframes_bigquery_function")
    assert hasattr(foo, "ibis_node")
    assert hasattr(foo, "input_dtypes")
    assert hasattr(foo, "output_dtype")
    assert hasattr(foo, "bigframes_bigquery_function_output_dtype")

    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result_col = scalars_df["int64_too"].apply(foo)
    bf_result = (
        scalars_df["int64_too"].to_frame().assign(result=bf_result_col).to_pandas()
    )

    pd_result_col = scalars_pandas_df["int64_too"].apply(foo)
    pd_result = scalars_pandas_df["int64_too"].to_frame().assign(result=pd_result_col)

    assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)

    # Make sure the read_gbq_function path works for this function.
    foo_ref = bff.read_gbq_function(
        function_name=foo.bigframes_bigquery_function,  # type: ignore
        session=session,
    )
    assert hasattr(foo_ref, "bigframes_bigquery_function")
    assert not hasattr(foo_ref, "bigframes_remote_function")
    assert foo.bigframes_bigquery_function == foo_ref.bigframes_bigquery_function  # type: ignore

    bf_result_col_gbq = scalars_df["int64_too"].apply(foo_ref)
    bf_result_gbq = (
        scalars_df["int64_too"].to_frame().assign(result=bf_result_col_gbq).to_pandas()
    )

    assert_pandas_df_equal(bf_result_gbq, pd_result, check_dtype=False)


def test_managed_function_series_combine(dataset_id_permanent, scalars_dfs):
    # This function is deliberately written to not work with NA input.
    def add(x: int, y: int) -> int:
        return x + y

    scalars_df, scalars_pandas_df = scalars_dfs
    int_col_name_with_nulls = "int64_col"
    int_col_name_no_nulls = "int64_too"
    bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
    pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

    # make sure there are NA values in the test column.
    assert any([pd.isna(val) for val in bf_df[int_col_name_with_nulls]])

    add_managed_func = udf(
        dataset=dataset_id_permanent,
        name=get_function_name(add),
    )(add)

    # with nulls in the series the managed function application would fail.
    with pytest.raises(
        google.api_core.exceptions.BadRequest, match="unsupported operand"
    ):
        bf_df[int_col_name_with_nulls].combine(
            bf_df[int_col_name_no_nulls], add_managed_func
        ).to_pandas()

    # after filtering out nulls the managed function application should work
    # similar to pandas.
    pd_filter = pd_df[int_col_name_with_nulls].notnull()
    pd_result = pd_df[pd_filter][int_col_name_with_nulls].combine(
        pd_df[pd_filter][int_col_name_no_nulls], add
    )
    bf_filter = bf_df[int_col_name_with_nulls].notnull()
    bf_result = (
        bf_df[bf_filter][int_col_name_with_nulls]
        .combine(bf_df[bf_filter][int_col_name_no_nulls], add_managed_func)
        .to_pandas()
    )

    # ignore any dtype difference.
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("typ",),
    [
        pytest.param(int),
        pytest.param(float),
        pytest.param(bool),
        pytest.param(str),
    ],
)
def test_managed_function_series_apply_list_output(
    typ,
    scalars_dfs,
    dataset_id_permanent,
):
    def foo_list(x):
        # The bytes() constructor expects a non-negative interger as its arg.
        return [typ(abs(x)), typ(abs(x) + 1)]

    foo_list = udf(
        input_types=int,
        output_type=list[typ],  # type: ignore
        dataset=dataset_id_permanent,
        name=get_function_name(foo_list),
    )(foo_list)

    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result_col = scalars_df["int64_too"].apply(foo_list)
    bf_result = (
        scalars_df["int64_too"].to_frame().assign(result=bf_result_col).to_pandas()
    )

    pd_result_col = scalars_pandas_df["int64_too"].apply(foo_list)
    pd_result = scalars_pandas_df["int64_too"].to_frame().assign(result=pd_result_col)

    # Ignore any dtype difference.
    assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)


def test_managed_function_series_combine_list_output(
    session, dataset_id_permanent, scalars_dfs
):
    def add_list(x: int, y: int) -> list[int]:
        return [x, y]

    scalars_df, scalars_pandas_df = scalars_dfs
    int_col_name_with_nulls = "int64_col"
    int_col_name_no_nulls = "int64_too"
    bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
    pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

    # Make sure there are NA values in the test column.
    assert any([pd.isna(val) for val in bf_df[int_col_name_with_nulls]])

    add_list_managed_func = udf(
        dataset=dataset_id_permanent,
        name=get_function_name(add_list),
    )(add_list)

    # After filtering out nulls the managed function application should work
    # similar to pandas.
    pd_filter = pd_df[int_col_name_with_nulls].notnull()
    pd_result = pd_df[pd_filter][int_col_name_with_nulls].combine(
        pd_df[pd_filter][int_col_name_no_nulls], add_list
    )
    bf_filter = bf_df[int_col_name_with_nulls].notnull()
    bf_result = (
        bf_df[bf_filter][int_col_name_with_nulls]
        .combine(bf_df[bf_filter][int_col_name_no_nulls], add_list_managed_func)
        .to_pandas()
    )

    # Ignore any dtype difference.
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

    # Make sure the read_gbq_function path works for this function.
    add_list_managed_func_ref = bff.read_gbq_function(
        function_name=add_list_managed_func.bigframes_bigquery_function,  # type: ignore
        session=session,
    )

    assert hasattr(add_list_managed_func_ref, "bigframes_bigquery_function")
    assert not hasattr(add_list_managed_func_ref, "bigframes_remote_function")
    assert (
        add_list_managed_func_ref.bigframes_bigquery_function
        == add_list_managed_func.bigframes_bigquery_function
    )

    # Test on the function from read_gbq_function.
    got = add_list_managed_func_ref(10, 38)
    assert got == [10, 38]

    bf_result_gbq = (
        bf_df[bf_filter][int_col_name_with_nulls]
        .combine(bf_df[bf_filter][int_col_name_no_nulls], add_list_managed_func_ref)
        .to_pandas()
    )

    pd.testing.assert_series_equal(bf_result_gbq, pd_result, check_dtype=False)


def test_managed_function_dataframe_map(scalars_dfs, dataset_id_permanent):
    def add_one(x):
        return x + 1

    mf_add_one = udf(
        input_types=[int],
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_one),
    )(add_one)

    scalars_df, scalars_pandas_df = scalars_dfs
    int64_cols = ["int64_col", "int64_too"]

    bf_int64_df = scalars_df[int64_cols]
    bf_int64_df_filtered = bf_int64_df.dropna()
    bf_result = bf_int64_df_filtered.map(mf_add_one).to_pandas()

    pd_int64_df = scalars_pandas_df[int64_cols]
    pd_int64_df_filtered = pd_int64_df.dropna()
    pd_result = pd_int64_df_filtered.map(add_one)
    # TODO(shobs): Figure why pandas .map() changes the dtype, i.e.
    # pd_int64_df_filtered.dtype is Int64Dtype()
    # pd_int64_df_filtered.map(lambda x: x).dtype is int64.
    # For this test let's force the pandas dtype to be same as input.
    for col in pd_result:
        pd_result[col] = pd_result[col].astype(pd_int64_df_filtered[col].dtype)

    assert_pandas_df_equal(bf_result, pd_result)


def test_managed_function_dataframe_apply_axis_1(
    session, scalars_dfs, dataset_id_permanent
):
    scalars_df, scalars_pandas_df = scalars_dfs
    series = scalars_df["int64_too"]
    series_pandas = scalars_pandas_df["int64_too"]

    def add_ints(x, y):
        return x + y

    add_ints_mf = session.udf(
        input_types=[int, int],
        output_type=int,
        dataset=dataset_id_permanent,
        name=get_function_name(add_ints, is_row_processor=True),
    )(add_ints)
    assert add_ints_mf.bigframes_bigquery_function  # type: ignore

    with pytest.warns(
        bigframes.exceptions.PreviewWarning, match="axis=1 scenario is in preview."
    ):
        bf_result = (
            bpd.DataFrame({"x": series, "y": series})
            .apply(add_ints_mf, axis=1)
            .to_pandas()
        )

    pd_result = pd.DataFrame({"x": series_pandas, "y": series_pandas}).apply(
        lambda row: add_ints(row["x"], row["y"]), axis=1
    )

    pd.testing.assert_series_equal(
        pd_result, bf_result, check_dtype=False, check_exact=True
    )


def test_managed_function_dataframe_map_list_output(
    session, scalars_dfs, dataset_id_permanent
):
    def add_one_list(x):
        return [x + 1] * 3

    mf_add_one_list = udf(
        input_types=[int],
        output_type=list[int],
        dataset=dataset_id_permanent,
        name=get_function_name(add_one_list),
    )(add_one_list)

    scalars_df, scalars_pandas_df = scalars_dfs
    int64_cols = ["int64_col", "int64_too"]

    bf_int64_df = scalars_df[int64_cols]
    bf_int64_df_filtered = bf_int64_df.dropna()
    bf_result = bf_int64_df_filtered.map(mf_add_one_list).to_pandas()

    pd_int64_df = scalars_pandas_df[int64_cols]
    pd_int64_df_filtered = pd_int64_df.dropna()
    pd_result = pd_int64_df_filtered.map(add_one_list)

    # Ignore any dtype difference.
    assert_pandas_df_equal(bf_result, pd_result, check_dtype=False)

    # Make sure the read_gbq_function path works for this function.
    mf_add_one_list_ref = bff.read_gbq_function(
        function_name=mf_add_one_list.bigframes_bigquery_function,  # type: ignore
        session=session,
    )

    bf_result_gbq = bf_int64_df_filtered.map(mf_add_one_list_ref).to_pandas()
    assert_pandas_df_equal(bf_result_gbq, pd_result, check_dtype=False)


def test_managed_function_dataframe_apply_axis_1_list_output(
    session, scalars_dfs, dataset_id_permanent
):
    scalars_df, scalars_pandas_df = scalars_dfs
    series = scalars_df["int64_too"]
    series_pandas = scalars_pandas_df["int64_too"]

    def add_ints_list(x, y):
        return [x + y] * 2

    add_ints_list_mf = session.udf(
        input_types=[int, int],
        output_type=list[int],
        dataset=dataset_id_permanent,
        name=get_function_name(add_ints_list, is_row_processor=True),
    )(add_ints_list)
    assert add_ints_list_mf.bigframes_bigquery_function  # type: ignore

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match="axis=1 scenario is in preview.",
    ):
        bf_result = (
            bpd.DataFrame({"x": series, "y": series})
            .apply(add_ints_list_mf, axis=1)
            .to_pandas()
        )

    pd_result = pd.DataFrame({"x": series_pandas, "y": series_pandas}).apply(
        lambda row: add_ints_list(row["x"], row["y"]), axis=1
    )

    # Ignore any dtype difference.
    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

    # Make sure the read_gbq_function path works for this function.
    add_ints_list_mf_ref = bff.read_gbq_function(
        function_name=add_ints_list_mf.bigframes_bigquery_function,  # type: ignore
        session=session,
    )
    assert hasattr(add_ints_list_mf_ref, "bigframes_bigquery_function")
    assert not hasattr(add_ints_list_mf_ref, "bigframes_remote_function")
    assert (
        add_ints_list_mf_ref.bigframes_bigquery_function
        == add_ints_list_mf.bigframes_bigquery_function
    )

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match="axis=1 scenario is in preview.",
    ):
        bf_result_gbq = (
            bpd.DataFrame({"x": series, "y": series})
            .apply(add_ints_list_mf_ref, axis=1)
            .to_pandas()
        )

    pd.testing.assert_series_equal(bf_result_gbq, pd_result, check_dtype=False)
