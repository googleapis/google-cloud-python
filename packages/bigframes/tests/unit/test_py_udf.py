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

import pathlib
from typing import Generator

import numpy as np
import pandas as pd
import pandas.testing
import pytest

import bigframes
import bigframes.pandas as bpd
from bigframes.testing.utils import (
    assert_frame_equal,
    assert_series_equal,
    convert_pandas_dtypes,
)

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.0.0")

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    with bpd.option_context("experiments.enable_python_transpiler", True):
        session = polars_session.TestSession()
        with bigframes.core.global_session._GlobalSessionContext(session):
            yield session


@pytest.fixture(scope="module")
def scalars_pandas_df_index() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    df.index.name = None
    return df.set_index("rowindex").sort_index()


@pytest.fixture(scope="module")
def scalars_df_index(
    session: bigframes.Session, scalars_pandas_df_index
) -> bpd.DataFrame:
    return session.read_pandas(scalars_pandas_df_index)


@pytest.fixture(scope="module")
def scalars_dfs(
    scalars_df_index,
    scalars_pandas_df_index,
):
    return scalars_df_index, scalars_pandas_df_index


def test_dataframe_map_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input):
        return input * 3 + 12

    bf_result = scalars_df_index[columns].map(foo, na_action="ignore").to_pandas()

    pd_result = (
        scalars_pandas_df_index[columns].map(foo, na_action="ignore").astype("Int64")
    )

    assert_frame_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input):
        return input.int64_too + input.int64_col

    bf_result = scalars_df_index[columns].apply(foo, axis=1).to_pandas()

    pd_result = scalars_pandas_df_index[columns].apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)


def test_series_combine_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    def which_smaller(left, right):
        return (left * right) + 3

    bf_result = (
        scalars_df_index["int64_too"]
        .combine(scalars_df_index["int64_col"], which_smaller)
        .to_pandas()
    )

    pd_result = scalars_pandas_df_index["int64_too"].combine(
        scalars_pandas_df_index["int64_col"], which_smaller
    )

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_with_defaults(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x=10, y=5):
        return input.int64_too + input.int64_col + x + y

    bf_result = scalars_df_index[columns].apply(foo, axis=1).to_pandas()
    pd_result = scalars_pandas_df_index[columns].apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_with_args(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x, y=5):
        return input.int64_too + input.int64_col + x + y

    bf_result = (
        scalars_df_index[columns].apply(foo, axis=1, args=(12,), y=20).to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index[columns]
        .apply(foo, axis=1, args=(12,), y=20)
        .astype("Int64")
    )

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_invalid_bindings(
    scalars_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x, y=5):
        return input.int64_too + input.int64_col + x + y

    # 1. Unexpected keyword argument
    with pytest.raises(TypeError, match="unexpected keyword argument 'z'"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10,), z=20)

    # 2. Multiple values for keyword argument 'x'
    with pytest.raises(TypeError, match="multiple values for argument 'x'"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10,), x=20)

    # 3. Too many positional arguments
    with pytest.raises(TypeError, match="too many positional arguments"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10, 20, 30))

    # 4. Missing required argument 'x'
    with pytest.raises(TypeError, match="missing a required argument: 'x'"):
        scalars_df_index[columns].apply(foo, axis=1)


def test_series_apply_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    def foo(x, y=10):
        return x * 2 + y

    bf_result = scalars_df_index["int64_col"].apply(foo, args=(5,)).to_pandas()
    pd_result = (
        scalars_pandas_df_index["int64_col"].apply(foo, args=(5,)).astype("Int64")
    )

    assert_series_equal(bf_result, pd_result)


def test_series_apply_transpile_invalid_bindings(
    scalars_df_index,
):
    def foo(x, y):
        return x + y

    # Too many positional args: foo takes 2 args (x, y), we pass self and 2 more args (total 3 positional)
    with pytest.raises(
        TypeError, match="too many positional arguments: expected 2, got 3"
    ):
        scalars_df_index["int64_col"].apply(foo, args=(10, 20))

    # Missing required argument: foo takes 2 args, we only pass self (so y is missing)
    with pytest.raises(TypeError, match="missing required argument: 'y'"):
        scalars_df_index["int64_col"].apply(foo)


def test_transpilation_unsupported_ops_raise(
    scalars_df_index,
):
    def foo_with_loop(x):
        total = 0
        for i in range(x):
            total += i
        return total

    with pytest.raises(ValueError):
        scalars_df_index["int64_col"].apply(foo_with_loop)


def my_foo(x: int):
    return x + 1


def test_local_series_apply_simple(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].apply(my_foo).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(my_foo)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def my_numpy_foo(x: int):
    return np.add(x, x) * (np.cos(x) - np.sin(3))


def test_local_series_apply_w_numpy(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].apply(my_numpy_foo).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(my_numpy_foo)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_simple_lamdba(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].apply(lambda x: x + 3).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(lambda x: x + 3)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_ternary_lamdba(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"]
        .apply(lambda x: "positive" if x > 0 else "negative")
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].apply(
        lambda x: "positive" if x > 0 else "negative"
    )

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_nested_fizzbuzz(session):
    # challenging: closure, multiple exits, mutating variables
    foo_div = 3
    buzz_div = 5
    pd_series = pd.Series(
        range(20),
        dtype="Int64",
        index=pd.Index(range(20), dtype="Int64"),
        name="integers",
    )
    bf_series = bpd.Series(pd_series, session=session)

    def fizzbuzz(x):
        if (x % 3) and (x % 5):
            return str(x)
        val = ""
        if (x % foo_div) == 0:
            val += "fizz"
        if (x % buzz_div) == 0:
            val += "buzz"
        return val

    bf_result = bf_series.apply(fizzbuzz).to_pandas()
    pd_result = pd_series.apply(fizzbuzz).astype(pd.StringDtype(storage="pyarrow"))

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_dataframe_apply_w_ternary_lamdba(
    scalars_df_index, scalars_pandas_df_index
):
    bf_result = scalars_df_index.apply(
        lambda x: x.int64_col if x.rowindex_2 > 5 else x.float64_col, axis=1
    ).to_pandas()
    pd_result = scalars_pandas_df_index.apply(
        lambda x: x.int64_col if x.rowindex_2 > 5 else x.float64_col, axis=1
    ).astype("Float64")

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_nested_ifs(scalars_df_index, scalars_pandas_df_index):
    def nested_ifs(x):
        if x > 0:
            if x > 100:
                return x * 10
            else:
                return x * 2
        else:
            if x < -100:
                return x * 20
            return x * -1

    bf_result = scalars_df_index["int64_col"].apply(nested_ifs).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(nested_ifs)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_elif(scalars_df_index, scalars_pandas_df_index):
    def elif_fn(x):
        if x > 100:
            return 1
        elif x > 50:
            return 2
        elif x > 0:
            return 3
        else:
            return 4

    bf_result = scalars_df_index["int64_col"].apply(elif_fn).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(elif_fn)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_logical_not(scalars_df_index, scalars_pandas_df_index):
    def logical_not_fn(x):
        if not (x > 0):
            return -x
        return x

    bf_result = scalars_df_index["int64_col"].apply(logical_not_fn).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(logical_not_fn)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_short_circuit(scalars_df_index, scalars_pandas_df_index):
    def short_circuit(x):
        if (x > 0 and x < 100) or x == 55555:
            return 1
        return 0

    bf_result = scalars_df_index["int64_col"].apply(short_circuit).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(short_circuit)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_var_assignments(
    scalars_df_index, scalars_pandas_df_index
):
    def var_assign(x):
        val = x
        if x > 0:
            val = val + 10
            if val > 100:
                val = val * 2
        else:
            val = val - 10
        return val

    bf_result = scalars_df_index["int64_col"].apply(var_assign).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].apply(var_assign)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_logical_and_val(
    scalars_df_index, scalars_pandas_df_index
):
    def logical_and_val(x):
        return (x % 3) and 100

    bf_result = (
        scalars_df_index["int64_col"].dropna().apply(logical_and_val).to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].dropna().apply(logical_and_val)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_logical_or_val(scalars_df_index, scalars_pandas_df_index):
    def logical_or_val(x):
        return (x % 3) or 200

    bf_result = scalars_df_index["int64_col"].dropna().apply(logical_or_val).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].dropna().apply(logical_or_val)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_logical_and_mixed(
    scalars_df_index,
):
    def logical_and_mixed(x):
        return (x % 3) and "hello"

    with pytest.raises(TypeError, match="Cannot coerce"):
        scalars_df_index["int64_col"].apply(logical_and_mixed)


def test_local_series_apply_w_logical_not_val(
    scalars_df_index, scalars_pandas_df_index
):
    def logical_not_val(x):
        return not x

    bf_result = scalars_df_index["bool_col"].dropna().apply(logical_not_val).to_pandas()
    pd_result = scalars_pandas_df_index["bool_col"].dropna().apply(logical_not_val)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_local_series_apply_w_compare_chain(scalars_df_index, scalars_pandas_df_index):
    def compare_chain(x):
        return 0 < x < 1000

    bf_result = scalars_df_index["int64_col"].dropna().apply(compare_chain).to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].dropna().apply(compare_chain)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_dataframe_transpile(scalars_df_index, scalars_pandas_df_index):
    def composite_metric(df):
        return (df.int64_col.sum() - df.int64_too.mean()) / df.float64_col.std()

    # Drop nulls to avoid NaN comparison differences
    bf_df = scalars_df_index.dropna(
        subset=["int64_col", "int64_too", "float64_col", "bool_col"]
    )
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "float64_col", "bool_col"]
    )

    bf_result = bf_df.groupby("bool_col").apply(composite_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(composite_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_series_transpile(scalars_df_index, scalars_pandas_df_index):
    def series_metric(s):
        return s.sum() - s.mean()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col", "bool_col"])

    bf_result = bf_df.groupby("bool_col")["int64_col"].apply(series_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col")["int64_col"].apply(series_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_with_subscript(scalars_df_index, scalars_pandas_df_index):
    def subscript_metric(df):
        return df["int64_col"].sum() - df["int64_too"].mean()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = bf_df.groupby("bool_col").apply(subscript_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(subscript_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_as_index_false(scalars_df_index, scalars_pandas_df_index):
    def composite_metric(df):
        return df.int64_col.sum() - df.int64_too.mean()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = (
        bf_df.groupby("bool_col", as_index=False).apply(composite_metric).to_pandas()
    )
    pd_result = pd_df.groupby("bool_col", as_index=False).apply(composite_metric)

    if isinstance(pd_result, pd.DataFrame):
        assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )
    else:
        assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_apply_agg_of_agg(scalars_df_index, scalars_pandas_df_index):
    # This is a variance-like metric: sum((x - mean(x)) ** 2) / count(x)
    def var_metric(df):
        return ((df.int64_col - df.int64_col.mean()) ** 2).sum() / df.int64_col.count()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col", "bool_col"])

    bf_result = bf_df.groupby("bool_col").apply(var_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(var_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_unsupported_method_raises(scalars_df_index):
    def unsupported_method(df):
        return df.int64_col.unsupported_method_xyz()

    with pytest.raises(
        NotImplementedError, match="No implementation available for call expression"
    ):
        scalars_df_index.groupby("bool_col").apply(unsupported_method)


def test_groupby_apply_series_unsupported_method_raises(scalars_df_index):
    def unsupported_method(s):
        return s.unsupported_method_xyz()

    with pytest.raises(
        NotImplementedError, match="No implementation available for call expression"
    ):
        scalars_df_index.groupby("bool_col")["int64_col"].apply(unsupported_method)


def test_groupby_apply_constant(scalars_df_index, scalars_pandas_df_index):
    def const_func(df):
        return 42

    bf_df = scalars_df_index.dropna(subset=["int64_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col"])

    bf_result = bf_df.groupby("int64_col").apply(const_func).to_pandas()
    pd_result = pd_df.groupby("int64_col").apply(const_func)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_conflicting_column_name(
    scalars_df_index, scalars_pandas_df_index
):
    bf_df = scalars_df_index.rename(columns={"int64_col": "sum"})
    pd_df = scalars_pandas_df_index.rename(columns={"int64_col": "sum"})

    def my_metric(df):
        return df["sum"].sum() - df.int64_too.mean()

    bf_result = bf_df.groupby("bool_col").apply(my_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(my_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_post_agg_scalar_op(scalars_df_index, scalars_pandas_df_index):
    import math

    def complex_metric(df):
        return math.sin(abs(df.int64_col.sum() - df.int64_too.mean()))

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = bf_df.groupby("bool_col").apply(complex_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(complex_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_groupby_apply_conditional_aggs(scalars_df_index, scalars_pandas_df_index):
    def conditional_metric(df):
        return df.int64_col.sum() if df.int64_too.mean() > 0 else df.float64_col.std()

    bf_df = scalars_df_index.dropna(
        subset=["int64_col", "int64_too", "float64_col", "bool_col"]
    )
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "float64_col", "bool_col"]
    )

    bf_result = bf_df.groupby("bool_col").apply(conditional_metric).to_pandas()
    pd_result = pd_df.groupby("bool_col").apply(conditional_metric)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_dataframe_apply_axis_1_with_integer_subscript(
    scalars_df_index, scalars_pandas_df_index
):
    columns = ["int64_too", "int64_col"]
    bf_df = scalars_df_index[columns].rename(columns={"int64_too": 0, "int64_col": 1})
    pd_df = scalars_pandas_df_index[columns].rename(
        columns={"int64_too": 0, "int64_col": 1}
    )

    def foo(input):
        return input[0] + input[1]

    bf_result = bf_df.apply(foo, axis=1).to_pandas()
    pd_result = pd_df.apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_with_invalid_subscript_raises(
    scalars_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo_invalid_label(input):
        return input["non_existent_column"]

    with pytest.raises(KeyError, match="non_existent_column"):
        scalars_df_index[columns].apply(foo_invalid_label, axis=1)


def test_series_groupby_apply_with_subscript_raises(
    scalars_df_index,
):
    # Columnar context: SeriesGroupBy.apply(func) where func subscripts Series
    def bad_metric(s):
        return s[0]

    with pytest.raises(
        NotImplementedError,
        match="Subscripting a Series/column is not supported in this UDF context.",
    ):
        scalars_df_index.groupby("bool_col")["int64_col"].apply(bad_metric)


def test_series_map_with_struct_and_array_subscript(session):
    import pyarrow as pa

    # Struct setup
    struct_pa_type = pa.struct([("str_field", pa.string()), ("int_field", pa.int64())])
    pd_struct_series = pd.Series(
        pa.array([{"str_field": "hello", "int_field": 1}], struct_pa_type),
        dtype=pd.ArrowDtype(struct_pa_type),
    )
    bf_struct_series = bpd.Series(pd_struct_series, session=session)

    # Array setup
    array_pa_type = pa.list_(pa.int64())
    pd_array_series = pd.Series(
        pa.array([[10, 20]], array_pa_type),
        dtype=pd.ArrowDtype(array_pa_type),
    )
    bf_array_series = bpd.Series(pd_array_series, session=session)

    # Struct subscripting in UDF
    def get_struct_val(x):
        return x["str_field"]

    bf_struct_res = bf_struct_series.map(get_struct_val).to_pandas()
    pd_struct_res = pd_struct_series.map(get_struct_val)
    assert_series_equal(bf_struct_res, pd_struct_res, check_dtype=False)

    # Array subscripting in UDF
    def get_array_val(x):
        return x[1]

    bf_array_res = bf_array_series.map(get_array_val).to_pandas()
    pd_array_res = pd_array_series.map(get_array_val)
    assert_series_equal(bf_array_res, pd_array_res, check_dtype=False)


def test_dataframe_apply_axis_1_with_dynamic_subscript_raises(
    scalars_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo_dynamic(input):
        return input[input[0]]

    with pytest.raises(
        NotImplementedError, match="Dynamic column lookup is not supported"
    ):
        scalars_df_index[columns].apply(foo_dynamic, axis=1)


def test_dataframe_apply_axis_1_with_dynamic_array_subscript(session):
    import pyarrow as pa

    array_pa_type = pa.list_(pa.int64())
    pd_df = pd.DataFrame(
        {
            "array_col": pd.Series(
                pa.array([[10, 20], [30, 40, 50], [60]], array_pa_type),
                dtype=pd.ArrowDtype(array_pa_type),
            ),
            "index_col": pd.Series([1, 2, 0], dtype="Int64"),
        }
    )
    bf_df = bpd.DataFrame(pd_df, session=session)

    def foo(row):
        return row["array_col"][row["index_col"]]

    bf_result = bf_df.apply(foo, axis=1).to_pandas()
    pd_result = pd_df.apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)
