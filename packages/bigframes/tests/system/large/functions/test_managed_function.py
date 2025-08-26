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

import warnings

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

        with warnings.catch_warnings(record=True) as record:

            @session.udf(
                dataset=dataset_id,
                name=prefixer.create_prefix(),
            )
            def featurize(x: int) -> list[float]:
                return [float(i) for i in [x, x + 1, x + 2]]

        # No following conflict warning when there is no redundant type hints.
        input_type_warning = "Conflicting input types detected"
        return_type_warning = "Conflicting return type detected"
        assert not any(input_type_warning in str(warning.message) for warning in record)
        assert not any(
            return_type_warning in str(warning.message) for warning in record
        )

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

        # The type hints in this function's signature has conflicts. The
        # `input_types` and `output_type` arguments from udf decorator take
        # precedence and will be used instead.
        def add_list(x, y: bool) -> list[bool]:
            return [x, y]

        scalars_df, scalars_pandas_df = scalars_dfs
        int_col_name_with_nulls = "int64_col"
        int_col_name_no_nulls = "int64_too"
        bf_df = scalars_df[[int_col_name_with_nulls, int_col_name_no_nulls]]
        pd_df = scalars_pandas_df[[int_col_name_with_nulls, int_col_name_no_nulls]]

        # Make sure there are NA values in the test column.
        assert any([pandas.isna(val) for val in bf_df[int_col_name_with_nulls]])

        with warnings.catch_warnings(record=True) as record:
            add_list_managed_func = session.udf(
                input_types=[int, int],
                output_type=list[int],
                dataset=dataset_id,
                name=prefixer.create_prefix(),
            )(add_list)

        input_type_warning = "Conflicting input types detected"
        assert any(input_type_warning in str(warning.message) for warning in record)
        return_type_warning = "Conflicting return type detected"
        assert any(return_type_warning in str(warning.message) for warning in record)

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


def test_managed_function_options(session, dataset_id, scalars_dfs):
    try:

        def multiply_five(x: int) -> int:
            return x * 5

        mf_multiply_five = session.udf(
            dataset=dataset_id,
            name=prefixer.create_prefix(),
            max_batching_rows=100,
            container_cpu=2,
            container_memory="2Gi",
        )(multiply_five)

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_int64_df = scalars_df["int64_col"]
        bf_int64_df_filtered = bf_int64_df.dropna()
        bf_result = bf_int64_df_filtered.apply(mf_multiply_five).to_pandas()

        pd_int64_df = scalars_pandas_df["int64_col"]
        pd_int64_df_filtered = pd_int64_df.dropna()
        pd_result = pd_int64_df_filtered.apply(multiply_five)

        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

        # Make sure the read_gbq_function path works for this function.
        multiply_five_ref = session.read_gbq_function(
            function_name=mf_multiply_five.bigframes_bigquery_function,  # type: ignore
        )
        assert mf_multiply_five.bigframes_bigquery_function == multiply_five_ref.bigframes_bigquery_function  # type: ignore

        bf_result = bf_int64_df_filtered.apply(multiply_five_ref).to_pandas()
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

        # Retrieve the routine and validate its runtime configuration.
        routine = session.bqclient.get_routine(
            mf_multiply_five.bigframes_bigquery_function
        )

        # TODO(jialuo): Use the newly exposed class properties instead of
        # accessing the hidden _properties after resolve of this issue:
        # https://github.com/googleapis/python-bigquery/issues/2240.
        assert routine._properties["externalRuntimeOptions"]["maxBatchingRows"] == "100"
        assert routine._properties["externalRuntimeOptions"]["containerCpu"] == 2
        assert routine._properties["externalRuntimeOptions"]["containerMemory"] == "2Gi"

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            mf_multiply_five, session.bqclient, ignore_failures=False
        )


def test_managed_function_options_errors(session, dataset_id):
    def foo(x: int) -> int:
        return 0

    with pytest.raises(
        google.api_core.exceptions.BadRequest,
        # For CPU Value >= 1.0, the value must be one of [1, 2, ...].
        match="Invalid container_cpu function OPTIONS value",
    ):
        session.udf(
            dataset=dataset_id,
            name=prefixer.create_prefix(),
            max_batching_rows=100,
            container_cpu=2.5,
            container_memory="2Gi",
        )(foo)

    with pytest.raises(
        google.api_core.exceptions.BadRequest,
        # For less than 1.0 CPU, the value must be no less than 0.33.
        match="Invalid container_cpu function OPTIONS value",
    ):
        session.udf(
            dataset=dataset_id,
            name=prefixer.create_prefix(),
            max_batching_rows=100,
            container_cpu=0.10,
            container_memory="512Mi",
        )(foo)

    with pytest.raises(
        google.api_core.exceptions.BadRequest,
        # For 2.00 CPU, the memory must be in the range of [256Mi, 8Gi].
        match="Invalid container_memory function OPTIONS value",
    ):
        session.udf(
            dataset=dataset_id,
            name=prefixer.create_prefix(),
            max_batching_rows=100,
            container_cpu=2,
            container_memory="64Mi",
        )(foo)


def test_managed_function_df_apply_axis_1(session, dataset_id, scalars_dfs):
    columns = ["bool_col", "int64_col", "int64_too", "float64_col", "string_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    try:

        def serialize_row(row):
            # TODO(b/435021126): Remove explicit type conversion of the field
            # "name" after the issue has been addressed. It is added only to
            # accept partial pandas parity for the time being.
            custom = {
                "name": int(row.name),
                "index": [idx for idx in row.index],
                "values": [
                    val.item() if hasattr(val, "item") else val for val in row.values
                ],
            }

            return str(
                {
                    "default": row.to_json(),
                    "split": row.to_json(orient="split"),
                    "records": row.to_json(orient="records"),
                    "index": row.to_json(orient="index"),
                    "table": row.to_json(orient="table"),
                    "custom": custom,
                }
            )

        serialize_row_mf = session.udf(
            input_types=bigframes.series.Series,
            output_type=str,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(serialize_row)

        assert getattr(serialize_row_mf, "is_row_processor")

        bf_result = scalars_df[columns].apply(serialize_row_mf, axis=1).to_pandas()
        pd_result = scalars_pandas_df[columns].apply(serialize_row, axis=1)

        # bf_result.dtype is 'string[pyarrow]' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's make sure the read_gbq_function path works for this function.
        serialize_row_reuse = session.read_gbq_function(
            serialize_row_mf.bigframes_bigquery_function, is_row_processor=True
        )
        bf_result = scalars_df[columns].apply(serialize_row_reuse, axis=1).to_pandas()
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            serialize_row_mf, session.bqclient, ignore_failures=False
        )


def test_managed_function_df_apply_axis_1_aggregates(session, dataset_id, scalars_dfs):
    columns = ["int64_col", "int64_too", "float64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs

    try:

        def analyze(row):
            # TODO(b/435021126): Remove explicit type conversion of the fields
            # after the issue has been addressed. It is added only to accept
            # partial pandas parity for the time being.
            return str(
                {
                    "dtype": row.dtype,
                    "count": int(row.count()),
                    "min": int(row.min()),
                    "max": int(row.max()),
                    "mean": float(row.mean()),
                    "std": float(row.std()),
                    "var": float(row.var()),
                }
            )

        with pytest.warns(
            bfe.FunctionPackageVersionWarning,
            match=(
                "numpy, pandas, and pyarrow versions in the function execution"
                "\nenvironment may not precisely match your local environment."
            ),
        ):

            analyze_mf = session.udf(
                input_types=bigframes.series.Series,
                output_type=str,
                dataset=dataset_id,
                name=prefixer.create_prefix(),
            )(analyze)

        assert getattr(analyze_mf, "is_row_processor")

        bf_result = scalars_df[columns].dropna().apply(analyze_mf, axis=1).to_pandas()
        pd_result = scalars_pandas_df[columns].dropna().apply(analyze, axis=1)

        # bf_result.dtype is 'string[pyarrow]' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(analyze_mf, session.bqclient, ignore_failures=False)


@pytest.mark.parametrize(
    ("pd_df",),
    [
        pytest.param(
            pandas.DataFrame(
                {
                    "2": [1, 2, 3],
                    2: [1.5, 3.75, 5],
                    "name, [with. special'- chars\")/\\": [10, 20, 30],
                    (3, 4): ["pq", "rs", "tu"],
                    (5.0, "six", 7): [8, 9, 10],
                    'raise Exception("hacked!")': [11, 12, 13],
                },
                # Default pandas index has non-numpy type, whereas bigframes is
                # always numpy-based type, so let's use the index compatible
                # with bigframes. See more details in b/369689696.
                index=pandas.Index([0, 1, 2], dtype=pandas.Int64Dtype()),
            ),
            id="all-kinds-of-column-names",
        ),
        pytest.param(
            pandas.DataFrame(
                {
                    "x": [1, 2, 3],
                    "y": [1.5, 3.75, 5],
                    "z": ["pq", "rs", "tu"],
                },
                index=pandas.MultiIndex.from_frame(
                    pandas.DataFrame(
                        {
                            "idx0": pandas.Series(
                                ["a", "a", "b"], dtype=pandas.StringDtype()
                            ),
                            "idx1": pandas.Series(
                                [100, 200, 300], dtype=pandas.Int64Dtype()
                            ),
                        }
                    )
                ),
            ),
            id="multiindex",
            marks=pytest.mark.skip(
                reason="TODO: revert this skip after this pandas bug is fixed: https://github.com/pandas-dev/pandas/issues/59908"
            ),
        ),
        pytest.param(
            pandas.DataFrame(
                [
                    [10, 1.5, "pq"],
                    [20, 3.75, "rs"],
                    [30, 8.0, "tu"],
                ],
                # Default pandas index has non-numpy type, whereas bigframes is
                # always numpy-based type, so let's use the index compatible
                # with bigframes. See more details in b/369689696.
                index=pandas.Index([0, 1, 2], dtype=pandas.Int64Dtype()),
                columns=pandas.MultiIndex.from_arrays(
                    [
                        ["first", "last_two", "last_two"],
                        [1, 2, 3],
                    ]
                ),
            ),
            id="column-multiindex",
        ),
    ],
)
def test_managed_function_df_apply_axis_1_complex(session, dataset_id, pd_df):
    bf_df = session.read_pandas(pd_df)

    try:

        def serialize_row(row):
            # TODO(b/435021126): Remove explicit type conversion of the field
            # "name" after the issue has been addressed. It is added only to
            # accept partial pandas parity for the time being.
            custom = {
                "name": int(row.name),
                "index": [idx for idx in row.index],
                "values": [
                    val.item() if hasattr(val, "item") else val for val in row.values
                ],
            }
            return str(
                {
                    "default": row.to_json(),
                    "split": row.to_json(orient="split"),
                    "records": row.to_json(orient="records"),
                    "index": row.to_json(orient="index"),
                    "custom": custom,
                }
            )

        serialize_row_mf = session.udf(
            input_types=bigframes.series.Series,
            output_type=str,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(serialize_row)

        assert getattr(serialize_row_mf, "is_row_processor")

        bf_result = bf_df.apply(serialize_row_mf, axis=1).to_pandas()
        pd_result = pd_df.apply(serialize_row, axis=1)

        # ignore known dtype difference between pandas and bigframes.
        pandas.testing.assert_series_equal(
            pd_result, bf_result, check_dtype=False, check_index_type=False
        )

    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            serialize_row_mf, session.bqclient, ignore_failures=False
        )


@pytest.mark.skip(reason="Revert after this bug b/435018880 is fixed.")
def test_managed_function_df_apply_axis_1_na_nan_inf(dataset_id, session):
    """This test is for special cases of float values, to make sure any (nan,
    inf, -inf) produced by user code is honored.
    """
    bf_df = session.read_gbq(
        """\
SELECT "1" AS text, 1 AS num
UNION ALL
SELECT "2.5" AS text, 2.5 AS num
UNION ALL
SELECT "nan" AS text, IEEE_DIVIDE(0, 0) AS num
UNION ALL
SELECT "inf" AS text, IEEE_DIVIDE(1, 0) AS num
UNION ALL
SELECT "-inf" AS text, IEEE_DIVIDE(-1, 0) AS num
UNION ALL
SELECT "numpy nan" AS text, IEEE_DIVIDE(0, 0) AS num
UNION ALL
SELECT "pandas na" AS text, NULL AS num
                             """
    )

    pd_df = bf_df.to_pandas()

    try:

        def float_parser(row):
            import numpy as mynp
            import pandas as mypd

            if row["text"] == "pandas na":
                return mypd.NA
            if row["text"] == "numpy nan":
                return mynp.nan
            return float(row["text"])

        float_parser_mf = session.udf(
            input_types=bigframes.series.Series,
            output_type=float,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(float_parser)

        assert getattr(float_parser_mf, "is_row_processor")

        pd_result = pd_df.apply(float_parser, axis=1)
        bf_result = bf_df.apply(float_parser_mf, axis=1).to_pandas()

        # bf_result.dtype is 'Float64' while pd_result.dtype is 'object'
        # , ignore this mismatch by using check_dtype=False.
        pandas.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)

        # Let's also assert that the data is consistent in this round trip
        # (BQ -> BigFrames -> BQ -> GCF -> BQ -> BigFrames) w.r.t. their
        # expected values in BQ.
        bq_result = bf_df["num"].to_pandas()
        bq_result.name = None
        pandas.testing.assert_series_equal(bq_result, bf_result)
    finally:
        # clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            float_parser_mf, session.bqclient, ignore_failures=False
        )


def test_managed_function_df_where_mask(session, dataset_id, scalars_dfs):
    try:

        # The return type has to be bool type for callable where condition.
        def is_sum_positive(a, b):
            return a + b > 0

        is_sum_positive_mf = session.udf(
            input_types=[int, int],
            output_type=bool,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(is_sum_positive)

        scalars_df, scalars_pandas_df = scalars_dfs
        int64_cols = ["int64_col", "int64_too"]

        bf_int64_df = scalars_df[int64_cols]
        bf_int64_df_filtered = bf_int64_df.dropna()
        pd_int64_df = scalars_pandas_df[int64_cols]
        pd_int64_df_filtered = pd_int64_df.dropna()

        # Test callable condition in dataframe.where method.
        bf_result = bf_int64_df_filtered.where(is_sum_positive_mf).to_pandas()
        # Pandas doesn't support such case, use following as workaround.
        pd_result = pd_int64_df_filtered.where(pd_int64_df_filtered.sum(axis=1) > 0)

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)

        # Make sure the read_gbq_function path works for dataframe.where method.
        is_sum_positive_ref = session.read_gbq_function(
            function_name=is_sum_positive_mf.bigframes_bigquery_function
        )

        bf_result_gbq = bf_int64_df_filtered.where(
            is_sum_positive_ref, -bf_int64_df_filtered
        ).to_pandas()
        pd_result_gbq = pd_int64_df_filtered.where(
            pd_int64_df_filtered.sum(axis=1) > 0, -pd_int64_df_filtered
        )

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(
            bf_result_gbq, pd_result_gbq, check_dtype=False
        )

        # Test callable condition in dataframe.mask method.
        bf_result_gbq = bf_int64_df_filtered.mask(
            is_sum_positive_ref, -bf_int64_df_filtered
        ).to_pandas()
        pd_result_gbq = pd_int64_df_filtered.mask(
            pd_int64_df_filtered.sum(axis=1) > 0, -pd_int64_df_filtered
        )

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(
            bf_result_gbq, pd_result_gbq, check_dtype=False
        )

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            is_sum_positive_mf, session.bqclient, ignore_failures=False
        )


def test_managed_function_df_where_mask_series(session, dataset_id, scalars_dfs):
    try:

        # The return type has to be bool type for callable where condition.
        def is_sum_positive_series(s):
            return s["int64_col"] + s["int64_too"] > 0

        is_sum_positive_series_mf = session.udf(
            input_types=bigframes.series.Series,
            output_type=bool,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(is_sum_positive_series)

        scalars_df, scalars_pandas_df = scalars_dfs
        int64_cols = ["int64_col", "int64_too"]

        bf_int64_df = scalars_df[int64_cols]
        bf_int64_df_filtered = bf_int64_df.dropna()
        pd_int64_df = scalars_pandas_df[int64_cols]
        pd_int64_df_filtered = pd_int64_df.dropna()

        # Test callable condition in dataframe.where method.
        bf_result = bf_int64_df_filtered.where(is_sum_positive_series).to_pandas()
        pd_result = pd_int64_df_filtered.where(is_sum_positive_series)

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)

        # Make sure the read_gbq_function path works for dataframe.where method.
        is_sum_positive_series_ref = session.read_gbq_function(
            function_name=is_sum_positive_series_mf.bigframes_bigquery_function,
            is_row_processor=True,
        )

        # This is for callable `other` arg in dataframe.where method.
        def func_for_other(x):
            return -x

        bf_result_gbq = bf_int64_df_filtered.where(
            is_sum_positive_series_ref, func_for_other
        ).to_pandas()
        pd_result_gbq = pd_int64_df_filtered.where(
            is_sum_positive_series, func_for_other
        )

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(
            bf_result_gbq, pd_result_gbq, check_dtype=False
        )

        # Test callable condition in dataframe.mask method.
        bf_result_gbq = bf_int64_df_filtered.mask(
            is_sum_positive_series_ref, func_for_other
        ).to_pandas()
        pd_result_gbq = pd_int64_df_filtered.mask(
            is_sum_positive_series, func_for_other
        )

        # Ignore any dtype difference.
        pandas.testing.assert_frame_equal(
            bf_result_gbq, pd_result_gbq, check_dtype=False
        )

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(
            is_sum_positive_series_mf, session.bqclient, ignore_failures=False
        )


def test_managed_function_series_where_mask(session, dataset_id, scalars_dfs):
    try:

        # The return type has to be bool type for callable where condition.
        def _is_positive(s):
            return s + 1000 > 0

        is_positive_mf = session.udf(
            input_types=int,
            output_type=bool,
            dataset=dataset_id,
            name=prefixer.create_prefix(),
        )(_is_positive)

        scalars, scalars_pandas = scalars_dfs

        bf_int64 = scalars["int64_col"]
        bf_int64_filtered = bf_int64.dropna()
        pd_int64 = scalars_pandas["int64_col"]
        pd_int64_filtered = pd_int64.dropna()

        # Test series.where method: the cond is a callable (managed function)
        # and the other is not a callable.
        bf_result = bf_int64_filtered.where(
            cond=is_positive_mf, other=-bf_int64_filtered
        ).to_pandas()
        pd_result = pd_int64_filtered.where(cond=_is_positive, other=-pd_int64_filtered)

        # Ignore any dtype difference.
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

        # Test series.mask method: the cond is a callable (managed function)
        # and the other is not a callable.
        bf_result = bf_int64_filtered.mask(
            cond=is_positive_mf, other=-bf_int64_filtered
        ).to_pandas()
        pd_result = pd_int64_filtered.mask(cond=_is_positive, other=-pd_int64_filtered)

        # Ignore any dtype difference.
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(is_positive_mf, session.bqclient, ignore_failures=False)


def test_managed_function_series_apply_args(session, dataset_id, scalars_dfs):
    try:

        with pytest.warns(bfe.PreviewWarning, match="udf is in preview."):

            @session.udf(dataset=dataset_id, name=prefixer.create_prefix())
            def foo_list(x: int, y0: float, y1: bytes, y2: bool) -> list[str]:
                return [str(x), str(y0), str(y1), str(y2)]

        scalars_df, scalars_pandas_df = scalars_dfs

        bf_result = (
            scalars_df["int64_too"]
            .apply(foo_list, args=(12.34, b"hello world", False))
            .to_pandas()
        )
        pd_result = scalars_pandas_df["int64_too"].apply(
            foo_list, args=(12.34, b"hello world", False)
        )

        # Ignore any dtype difference.
        pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)

    finally:
        # Clean up the gcp assets created for the managed function.
        cleanup_function_assets(foo_list, session.bqclient, ignore_failures=False)
