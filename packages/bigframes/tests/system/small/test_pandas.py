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

from datetime import datetime

import pandas as pd
import pytest
import pytz

import bigframes.pandas as bpd
from tests.system.utils import assert_pandas_df_equal


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_concat_dataframe(scalars_dfs, ordered):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = bpd.concat(11 * [scalars_df])
    bf_result = bf_result.to_pandas(ordered=ordered)
    pd_result = pd.concat(11 * [scalars_pandas_df])

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=not ordered)


def test_concat_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = bpd.concat(
        [scalars_df.int64_col, scalars_df.int64_too, scalars_df.int64_col]
    )
    bf_result = bf_result.to_pandas()
    pd_result = pd.concat(
        [
            scalars_pandas_df.int64_col,
            scalars_pandas_df.int64_too,
            scalars_pandas_df.int64_col,
        ]
    )

    pd.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("kwargs"),
    [
        {
            "prefix": ["prefix1", "prefix2"],
            "prefix_sep": "_",
            "dummy_na": None,
            "columns": ["bool_col", "int64_col"],
            "drop_first": False,
        },
        {
            "prefix": "prefix",
            "prefix_sep": ["_", ","],
            "dummy_na": False,
            "columns": ["int64_too", "string_col"],
            "drop_first": False,
        },
        {
            "prefix": None,
            "prefix_sep": ".",
            "dummy_na": True,
            "columns": ["time_col", "float64_col"],
            "drop_first": True,
        },
    ],
)
def test_get_dummies_dataframe(scalars_dfs, kwargs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = bpd.get_dummies(scalars_df, **kwargs, dtype=bool)
    pd_result = pd.get_dummies(scalars_pandas_df, **kwargs, dtype=bool)
    # dtype argument above is needed for pandas v1 only

    # adjust for expected dtype differences
    for (column_name, type_name) in zip(pd_result.columns, pd_result.dtypes):
        if type_name == "bool":
            pd_result[column_name] = pd_result[column_name].astype("boolean")

    pd.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


def test_get_dummies_dataframe_duplicate_labels(scalars_dfs):
    if pd.__version__.startswith("1."):
        pytest.skip("pandas has different behavior in 1.x")

    scalars_df, scalars_pandas_df = scalars_dfs

    scalars_renamed_df = scalars_df.rename(
        columns={"int64_too": "int64_col", "float64_col": None, "string_col": None}
    )
    scalars_renamed_pandas_df = scalars_pandas_df.rename(
        columns={"int64_too": "int64_col", "float64_col": None, "string_col": None}
    )

    bf_result = bpd.get_dummies(
        scalars_renamed_df, columns=["int64_col", None], dtype=bool
    )
    pd_result = pd.get_dummies(
        scalars_renamed_pandas_df, columns=["int64_col", None], dtype=bool
    )
    # dtype argument above is needed for pandas v1 only

    # adjust for expected dtype differences
    for (column_name, type_name) in zip(pd_result.columns, pd_result.dtypes):
        if type_name == "bool":
            pd_result[column_name] = pd_result[column_name].astype("boolean")

    pd.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


def test_get_dummies_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df.date_col
    pd_series = scalars_pandas_df.date_col

    bf_result = bpd.get_dummies(bf_series, dtype=bool)
    pd_result = pd.get_dummies(pd_series, dtype=bool)
    # dtype argument above is needed for pandas v1 only

    # adjust for expected dtype differences
    for (column_name, type_name) in zip(pd_result.columns, pd_result.dtypes):
        if type_name == "bool":
            pd_result[column_name] = pd_result[column_name].astype("boolean")
    pd_result.columns = pd_result.columns.astype(object)

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_get_dummies_series_nameless(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df.date_col.rename(None)
    pd_series = scalars_pandas_df.date_col.rename(None)

    bf_result = bpd.get_dummies(bf_series, dtype=bool)
    pd_result = pd.get_dummies(pd_series, dtype=bool)
    # dtype argument above is needed for pandas v1 only

    # adjust for expected dtype differences
    for (column_name, type_name) in zip(pd_result.columns, pd_result.dtypes):
        if type_name == "bool":
            pd_result[column_name] = pd_result[column_name].astype("boolean")
    pd_result.columns = pd_result.columns.astype(object)

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


@pytest.mark.parametrize(
    ("how"),
    [
        ("inner"),
        ("outer"),
    ],
)
def test_concat_dataframe_mismatched_columns(scalars_dfs, how):
    cols1 = ["int64_too", "int64_col", "float64_col"]
    cols2 = ["int64_col", "string_col", "int64_too"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = bpd.concat([scalars_df[cols1], scalars_df[cols2]], join=how)
    bf_result = bf_result.to_pandas()
    pd_result = pd.concat(
        [scalars_pandas_df[cols1], scalars_pandas_df[cols2]],
        join=how,
    )

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_concat_dataframe_upcasting(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_input1 = scalars_df[["int64_col", "float64_col", "int64_too"]].set_index(
        "int64_col", drop=True
    )
    bf_input1.columns = ["a", "b"]
    bf_input2 = scalars_df[["int64_too", "int64_col", "float64_col"]].set_index(
        "float64_col", drop=True
    )
    bf_input2.columns = ["a", "b"]
    bf_result = bpd.concat([bf_input1, bf_input2], join="outer")
    bf_result = bf_result.to_pandas()

    bf_input1 = (
        scalars_pandas_df[["int64_col", "float64_col", "int64_too"]]
        .set_index("int64_col", drop=True)
        .set_axis(["a", "b"], axis=1)
    )
    bf_input2 = (
        scalars_pandas_df[["int64_too", "int64_col", "float64_col"]]
        .set_index("float64_col", drop=True)
        .set_axis(["a", "b"], axis=1)
    )
    pd_result = pd.concat(
        [bf_input1, bf_input2],
        join="outer",
    )

    pd.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("how",),
    [
        ("inner",),
        ("outer",),
    ],
)
def test_concat_axis_1(scalars_dfs, how):
    if pd.__version__.startswith("1."):
        pytest.skip("pandas has different behavior in 1.x")
    scalars_df, scalars_pandas_df = scalars_dfs
    cols1 = ["int64_col", "float64_col", "rowindex_2"]
    cols2 = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    part1 = scalars_df[cols1]
    part1.index.name = "newindexname"
    # Offset the rows somewhat so that outer join can have an effect.
    part2 = (
        scalars_df[cols2]
        .assign(rowindex_2=scalars_df["rowindex_2"] + 2)
        .sort_values(["string_col"], kind="stable")
    )
    part3 = scalars_df["int64_too"].cumsum().iloc[2:]

    bf_result = bpd.concat([part1, part2, part3], join=how, axis=1)

    # Copy since modifying index
    pd_part1 = scalars_pandas_df.copy()[cols1]
    pd_part1.index.name = "newindexname"
    # Offset the rows somewhat so that outer join can have an effect.
    pd_part2 = (
        scalars_pandas_df[cols2]
        .assign(rowindex_2=scalars_pandas_df["rowindex_2"] + 2)
        .sort_values(["string_col"], kind="stable")
    )
    pd_part3 = scalars_pandas_df["int64_too"].cumsum().iloc[2:]

    pd_result = pd.concat([pd_part1, pd_part2, pd_part3], join=how, axis=1)

    pd.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    on = "rowindex_2"
    left_columns = ["int64_col", "float64_col", "rowindex_2"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    # Offset the rows somewhat so that outer join can have an effect.
    right = scalars_df[right_columns].assign(rowindex_2=scalars_df["rowindex_2"] + 2)

    df = bpd.merge(left, right, merge_how, on, sort=True)
    bf_result = df.to_pandas()

    pd_result = pd.merge(
        scalars_pandas_df[left_columns],
        scalars_pandas_df[right_columns].assign(
            rowindex_2=scalars_pandas_df["rowindex_2"] + 2
        ),
        merge_how,
        on,
        sort=True,
    )

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge_left_on_right_on(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col", "int64_too"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    right = scalars_df[right_columns]

    df = bpd.merge(
        left, right, merge_how, left_on="int64_too", right_on="rowindex_2", sort=True
    )
    bf_result = df.to_pandas()

    pd_result = pd.merge(
        scalars_pandas_df[left_columns],
        scalars_pandas_df[right_columns],
        merge_how,
        left_on="int64_too",
        right_on="rowindex_2",
        sort=True,
    )

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


def test_pd_merge_cross(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col", "int64_too"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    right = scalars_df[right_columns]

    df = bpd.merge(left, right, "cross", sort=True)
    bf_result = df.to_pandas()

    pd_result = pd.merge(
        scalars_pandas_df[left_columns],
        scalars_pandas_df[right_columns],
        "cross",
        sort=True,
    )

    pd.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge_series(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_column = "int64_too"
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_column]
    right = scalars_df[right_columns]

    df = bpd.merge(
        left, right, merge_how, left_on="int64_too", right_on="rowindex_2", sort=True
    )
    bf_result = df.to_pandas()

    pd_result = pd.merge(
        scalars_pandas_df[left_column],
        scalars_pandas_df[right_columns],
        merge_how,
        left_on="int64_too",
        right_on="rowindex_2",
        sort=True,
    )

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


def test_cut(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = pd.cut(scalars_pandas_df["float64_col"], 5, labels=False)
    bf_result = bpd.cut(scalars_df["float64_col"], 5, labels=False)

    # make sure the result is a supported dtype
    assert bf_result.dtype == bpd.Int64Dtype()

    bf_result = bf_result.to_pandas()
    pd_result = pd_result.astype("Int64")
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_cut_default_labels(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = pd.cut(scalars_pandas_df["float64_col"], 5)
    bf_result = bpd.cut(scalars_df["float64_col"], 5).to_pandas()

    # Convert to match data format
    pd_result_converted = pd.Series(
        [
            {"left_exclusive": interval.left, "right_inclusive": interval.right}
            if pd.notna(val)
            else pd.NA
            for val, interval in zip(
                pd_result, pd_result.cat.categories[pd_result.cat.codes]
            )
        ],
        name=pd_result.name,
    )

    pd.testing.assert_series_equal(
        bf_result, pd_result_converted, check_index=False, check_dtype=False
    )


@pytest.mark.parametrize(
    ("bins",),
    [
        ([(-5, 2), (2, 3), (-3000, -10)],),
        (pd.IntervalIndex.from_tuples([(1, 2), (2, 3), (4, 5)]),),
    ],
)
def test_cut_with_interval(scalars_dfs, bins):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = bpd.cut(scalars_df["int64_too"], bins, labels=False).to_pandas()

    if isinstance(bins, list):
        bins = pd.IntervalIndex.from_tuples(bins)
    pd_result = pd.cut(scalars_pandas_df["int64_too"], bins, labels=False)

    # Convert to match data format
    pd_result_converted = pd.Series(
        [
            {"left_exclusive": interval.left, "right_inclusive": interval.right}
            if pd.notna(val)
            else pd.NA
            for val, interval in zip(
                pd_result, pd_result.cat.categories[pd_result.cat.codes]
            )
        ],
        name=pd_result.name,
    )

    pd.testing.assert_series_equal(
        bf_result, pd_result_converted, check_index=False, check_dtype=False
    )


@pytest.mark.parametrize(
    ("q",),
    [
        (1,),
        (2,),
        (7,),
        (32,),
        ([0, 0.1, 0.3, 0.4, 0.9, 1.0],),
        ([0.5, 0.9],),
    ],
)
def test_qcut(scalars_dfs, q):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = pd.qcut(
        scalars_pandas_df["float64_col"], q, labels=False, duplicates="drop"
    )
    bf_result = bpd.qcut(scalars_df["float64_col"], q, labels=False, duplicates="drop")

    bf_result = bf_result.to_pandas()
    pd_result = pd_result.astype("Int64")

    pd.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("arg", "utc", "unit", "format"),
    [
        (173872738, False, None, None),
        (32787983.23, True, "s", None),
        ("2023-01-01", False, None, "%Y-%m-%d"),
        (datetime(2023, 1, 1, 12, 0), False, None, None),
    ],
)
def test_to_datetime_scalar(arg, utc, unit, format):
    bf_result = bpd.to_datetime(arg, utc=utc, unit=unit, format=format)
    pd_result = pd.to_datetime(arg, utc=utc, unit=unit, format=format)

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("arg", "utc", "unit", "format"),
    [
        ([173872738], False, None, None),
        ([32787983.23], True, "s", None),
        (
            [datetime(2023, 1, 1, 12, 0, tzinfo=pytz.timezone("America/New_York"))],
            True,
            None,
            None,
        ),
        (["2023-01-01"], True, None, "%Y-%m-%d"),
        (["2023-02-01T15:00:00+07:22"], True, None, None),
        (["01-31-2023 14:30 -0800"], True, None, "%m-%d-%Y %H:%M %z"),
        (["01-31-2023 14:00", "02-01-2023 15:00"], True, None, "%m-%d-%Y %H:%M"),
    ],
)
def test_to_datetime_iterable(arg, utc, unit, format):
    bf_result = (
        bpd.to_datetime(arg, utc=utc, unit=unit, format=format)
        .to_pandas()
        .astype("datetime64[ns, UTC]" if utc else "datetime64[ns]")
    )
    pd_result = pd.Series(
        pd.to_datetime(arg, utc=utc, unit=unit, format=format)
    ).dt.floor("us")
    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_names=False
    )


def test_to_datetime_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col = "int64_too"
    bf_result = (
        bpd.to_datetime(scalars_df[col], unit="s").to_pandas().astype("datetime64[s]")
    )
    pd_result = pd.Series(pd.to_datetime(scalars_pandas_df[col], unit="s"))
    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_names=False
    )


@pytest.mark.parametrize(
    ("arg", "unit"),
    [
        ([1, 2, 3], "W"),
        ([1, 2, 3], "d"),
        ([1, 2, 3], "D"),
        ([1, 2, 3], "h"),
        ([1, 2, 3], "m"),
        ([20242330, 25244685, 34324234], "s"),
        ([20242330000, 25244685000, 34324234000], "ms"),
        ([20242330000000, 25244685000000, 34324234000000], "us"),
        ([20242330000000000, 25244685000000000, 34324234000000000], "ns"),
    ],
)
def test_to_datetime_unit_param(arg, unit):
    bf_result = bpd.to_datetime(arg, unit=unit).to_pandas().astype("datetime64[ns]")
    pd_result = pd.Series(pd.to_datetime(arg, unit=unit)).dt.floor("us")
    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_names=False
    )


@pytest.mark.parametrize(
    ("arg", "utc", "format"),
    [
        ([20230110, 20230101, 20230101], False, "%Y%m%d"),
        ([201301.01], False, "%Y%m.%d"),
        (["2023-01-10", "2023-01-20", "2023-01-01"], True, "%Y-%m-%d"),
        (["2014-08-15 07:19"], True, "%Y-%m-%d %H:%M"),
    ],
)
def test_to_datetime_format_param(arg, utc, format):
    bf_result = (
        bpd.to_datetime(arg, utc=utc, format=format)
        .to_pandas()
        .astype("datetime64[ns, UTC]" if utc else "datetime64[ns]")
    )
    pd_result = pd.Series(pd.to_datetime(arg, utc=utc, format=format)).dt.floor("us")
    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_names=False
    )
