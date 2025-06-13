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
import pandas
import pyarrow
import pytest
import test_utils.prefixer

import bigframes
import bigframes.dataframe
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.pandas as bpd
from bigframes.testing.utils import cleanup_function_assets

prefixer = test_utils.prefixer.Prefixer("bigframes", "")


def test_managed_function_array_output(session, scalars_dfs, dataset_id):
    try:

        @session.udf(
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )
        def featurize(x: int) -> list[float]:
            return [float(i) for i in [x, x + 1, x + 2]]

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_col = scalars_df["int64_too"]
        bf_result = bf_int64_col.apply(featurize).to_pandas()

        pd_int64_col = scalars_pandas_df["int64_too"]
        pd_result = pd_int64_col.apply(featurize)

        # Ignore any dtype disparity.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        featurize_ref = session.read_gbq_function(featurize.bigframes_bigquery_function)

        assert hasattr(featurize_ref, "bigframes_bigquery_function")
        assert featurize_ref.bigframes_remote_function is None
        assert (
            featurize_ref.bigframes_bigquery_function
            == featurize.bigframes_bigquery_function
        )

        # Test on the function from read_gbq_function.
        got = featurize_ref(10)
        assert got == [10.0, 11.0, 12.0]

        bf_result_gbq = bf_int64_col.apply(featurize_ref).to_pandas()
        pandas.testing.assert_series_equal(bf_result_gbq, pd_result, check_dtype=False)

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(featurize, session.bqclient, ignore_failures=False)


def test_managed_function_series_apply(session, dataset_id, scalars_dfs):
    try:

        # An explicit name with "def" in it is used to test the robustness of
        # the user code extraction logic, which depends on that term.
        bq_name = f"{prefixer.create_prefix()}_def_to_test_code_extraction"
        assert "def" in bq_name, "The substring 'def' was not found in 'bq_name'"

        @session.udf(dataset=dataset_id, name=bq_name)
        def foo(x: int) -> bytes:
            return bytes(abs(x))

        # Function should still work normally.
        assert foo(-2) == bytes(2)

        assert hasattr(foo, "bigframes_bigquery_function")
        assert hasattr(foo, "input_dtypes")
        assert hasattr(foo, "output_dtype")
        assert hasattr(foo, "bigframes_bigquery_function_output_dtype")

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result_col = scalars_df["int64_too"].apply(foo)
        bf_result = (
            scalars_df["int64_too"].to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_result_col = scalars_pandas_df["int64_too"].apply(foo)
        pd_result = (
            scalars_pandas_df["int64_too"].to_frame().assign(result=pd_result_col)
        )

        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        foo_ref = session.read_gbq_function(
            function_name=foo.bigframes_bigquery_function,  # type: ignore
        )
        assert hasattr(foo_ref, "bigframes_bigquery_function")
        assert foo_ref.bigframes_remote_function is None
        assert foo.bigframes_bigquery_function == foo_ref.bigframes_bigquery_function  # type: ignore

        bf_result_col_gbq = scalars_df["int64_too"].apply(foo_ref)
        bf_result_gbq = (
            scalars_df["int64_too"]
            .to_frame()
            .assign(result=bf_result_col_gbq)
            .to_pandas()
        )

        pandas.testing.assert_frame_equal(bf_result_gbq, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(foo, session.bqclient, ignore_failures=False)


def test_managed_function_series_apply_array_output(
    session,
    dataset_id,
    scalars_dfs,
):
    try:

        with pytest.warns(bfe.PreviewWarning, match="udf is in preview."):

            @session.udf(dataset=dataset_id, name=prefixer.create_prefix())
            def foo_list(x: int) -> list[float]:
                return [float(abs(x)), float(abs(x) + 1)]

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result_col = scalars_df["int64_too"].apply(foo_list)
        bf_result = (
            scalars_df["int64_too"].to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_result_col = scalars_pandas_df["int64_too"].apply(foo_list)
        pd_result = (
            scalars_pandas_df["int64_too"].to_frame().assign(result=pd_result_col)
        )

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(foo_list, session.bqclient, ignore_failures=False)


def test_managed_function_series_combine(session, dataset_id, scalars_dfs):
    try:
        # This function is deliberately written to not work with NA input.
        def add(x: int, y: int) -> int:
            return x + y

        scalars_df, scalars_pandas_df = scalars_dfs
        int_col_name_with_nulls = "int64_col"
        int_col_name_no_nulls = "int64_too"
        bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
        pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

        # make sure there are NA values in the test column.
        assert any([pandas.isna(val) for val in bf_df[int_col_name_with_nulls]])

        add_managed_func = session.udf(
            dataset=dataset_id, name=prefixer.create_prefix()
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
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        add_managed_func_ref = session.read_gbq_function(
            add_managed_func.bigframes_bigquery_function
        )
        bf_result = (
            bf_df[bf_filter][int_col_name_with_nulls]
            .combine(bf_df[bf_filter][int_col_name_no_nulls], add_managed_func_ref)
            .to_pandas()
        )
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            add_managed_func, session.bqclient, ignore_failures=False
        )


def test_managed_function_series_combine_array_output(session, dataset_id, scalars_dfs):
    try:

        def add_list(x: int, y: int) -> list[int]:
            return [x, y]

        scalars_df, scalars_pandas_df = scalars_dfs
        int_col_name_with_nulls = "int64_col"
        int_col_name_no_nulls = "int64_too"
        bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
        pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

        # Make sure there are NA values in the test column.
        assert any([pandas.isna(val) for val in bf_df[int_col_name_with_nulls]])

        add_list_managed_func = session.udf(
            dataset=dataset_id, name=prefixer.create_prefix()
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
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        add_list_managed_func_ref = session.read_gbq_function(
            function_name=add_list_managed_func.bigframes_bigquery_function,  # type: ignore
        )

        assert hasattr(add_list_managed_func_ref, "bigframes_bigquery_function")
        assert add_list_managed_func_ref.bigframes_remote_function is None
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

        pandas.testing.assert_series_equal(bf_result_gbq, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            add_list_managed_func, session.bqclient, ignore_failures=False
        )


def test_managed_function_dataframe_map(session, dataset_id, scalars_dfs):
    try:

        def add_one(x):
            return x + 1

        mf_add_one = session.udf(
            input_types=[int],
            output_type=int,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
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

        pandas.testing.assert_frame_equal(bf_result, pd_result)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(mf_add_one, session.bqclient, ignore_failures=False)


def test_managed_function_dataframe_map_array_output(session, scalars_dfs, dataset_id):
    try:

        def add_one_list(x):
            return [x + 1] * 3

        mf_add_one_list = session.udf(
            input_types=[int],
            output_type=list[int],
            dataset=dataset_id,
            name=prefixer.create_prefix(),
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
        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        mf_add_one_list_ref = session.read_gbq_function(
            function_name=mf_add_one_list.bigframes_bigquery_function,  # type: ignore
        )

        bf_result_gbq = bf_int64_df_filtered.map(mf_add_one_list_ref).to_pandas()
        pandas.testing.assert_frame_equal(bf_result_gbq, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            mf_add_one_list, session.bqclient, ignore_failures=False
        )


def test_managed_function_dataframe_apply_axis_1(session, dataset_id, scalars_dfs):
    try:
        scalars_df, scalars_pandas_df = scalars_dfs
        series = scalars_df["int64_too"]
        series_pandas = scalars_pandas_df["int64_too"]

        def add_ints(x, y):
            return x + y

        add_ints_mf = session.udf(
            input_types=[int, int],
            output_type=int,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
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

        pd_result = pandas.DataFrame({"x": series_pandas, "y": series_pandas}).apply(
            lambda row: add_ints(row["x"], row["y"]), axis=1
        )

        pandas.testing.assert_series_equal(
            pd_result, bf_result, check_dtype=False, check_exact=True
        )
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(add_ints_mf, session.bqclient, ignore_failures=False)


def test_managed_function_dataframe_apply_axis_1_array_output(session, dataset_id):
    bf_df = bigframes.dataframe.DataFrame(
        {
            "Id": [1, 2, 3],
            "Age": [22.5, 23, 23.5],
            "Name": ["alpha", "beta", "gamma"],
        }
    )

    expected_dtypes = (
        bigframes.dtypes.INT_DTYPE,
        bigframes.dtypes.FLOAT_DTYPE,
        bigframes.dtypes.STRING_DTYPE,
    )

    # Assert the dataframe dtypes.
    assert tuple(bf_df.dtypes) == expected_dtypes

    @session.udf(
        input_types=[int, float, str],
        output_type=list[str],
        dataset=dataset_id,
        name=prefixer.create_prefix(),
    )
    def foo(x, y, z):
        return [str(x), str(y), z]

    try:

        assert getattr(foo, "is_row_processor") is False
        assert getattr(foo, "input_dtypes") == expected_dtypes
        assert getattr(foo, "output_dtype") == pandas.ArrowDtype(
            pyarrow.list_(
                bigframes.dtypes.bigframes_dtype_to_arrow_dtype(
                    bigframes.dtypes.STRING_DTYPE
                )
            )
        )
        assert getattr(foo, "output_dtype") == getattr(
            foo, "bigframes_bigquery_function_output_dtype"
        )

        # Fails to apply on dataframe with incompatible number of columns.
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 2 columns\\.$",
        ):
            bf_df[["Id", "Age"]].apply(foo, axis=1)

        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes 3 arguments but DataFrame has 4 columns\\.$",
        ):
            bf_df.assign(Country="lalaland").apply(foo, axis=1)

        # Fails to apply on dataframe with incompatible column datatypes.
        with pytest.raises(
            ValueError,
            match="^BigFrames BigQuery function takes arguments of types .* but DataFrame dtypes are .*",
        ):
            bf_df.assign(Age=bf_df["Age"].astype("Int64")).apply(foo, axis=1)

        # Successfully applies to dataframe with matching number of columns.
        # and their datatypes.
        with pytest.warns(
            bigframes.exceptions.PreviewWarning,
            match="axis=1 scenario is in preview.",
        ):
            bf_result = bf_df.apply(foo, axis=1).to_pandas()

        # Since this scenario is not pandas-like, let's handcraft the
        # expected result.
        expected_result = pandas.Series(
            [
                ["1", "22.5", "alpha"],
                ["2", "23.0", "beta"],
                ["3", "23.5", "gamma"],
            ]
        )

        pandas.testing.assert_series_equal(
            expected_result, bf_result, check_dtype=False, check_index_type=False
        )

        # Make sure the read_gbq_function path works for this function.
        foo_ref = session.read_gbq_function(foo.bigframes_bigquery_function)

        assert hasattr(foo_ref, "bigframes_bigquery_function")
        assert foo_ref.bigframes_remote_function is None
        assert foo_ref.bigframes_bigquery_function == foo.bigframes_bigquery_function

        # Test on the function from read_gbq_function.
        got = foo_ref(10, 38, "hello")
        assert got == ["10", "38.0", "hello"]

        with pytest.warns(
            bigframes.exceptions.PreviewWarning,
            match="axis=1 scenario is in preview.",
        ):
            bf_result_gbq = bf_df.apply(foo_ref, axis=1).to_pandas()

        pandas.testing.assert_series_equal(
            bf_result_gbq, expected_result, check_dtype=False, check_index_type=False
        )

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(foo, session.bqclient, ignore_failures=False)


@pytest.mark.parametrize(
    "connection_fixture",
    [
        "bq_connection_name",
        "bq_connection",
    ],
)
def test_managed_function_with_connection(
    session, scalars_dfs, dataset_id, request, connection_fixture
):
    try:
        bigquery_connection = request.getfixturevalue(connection_fixture)

        @session.udf(
            bigquery_connection=bigquery_connection,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )
        def foo(x: int) -> int:
            return x + 10

        # Function should still work normally.
        assert foo(-2) == 8

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result_col = scalars_df["int64_too"].apply(foo)
        bf_result = (
            scalars_df["int64_too"].to_frame().assign(result=bf_result_col).to_pandas()
        )

        pd_result_col = scalars_pandas_df["int64_too"].apply(foo)
        pd_result = (
            scalars_pandas_df["int64_too"].to_frame().assign(result=pd_result_col)
        )

        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)
    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(foo, session.bqclient, ignore_failures=False)
