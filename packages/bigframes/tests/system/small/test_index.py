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

import re

import numpy
import pandas as pd
import pytest

from bigframes import dtypes
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_pandas_index_equal_ignore_index_type


def test_index_construct_from_list():
    bf_result = bpd.Index(
        [3, 14, 159], dtype=pd.Int64Dtype(), name="my_index"
    ).to_pandas()

    pd_result: pd.Index = pd.Index([3, 14, 159], dtype=pd.Int64Dtype(), name="my_index")
    pd.testing.assert_index_equal(bf_result, pd_result)


@pytest.mark.parametrize("key, expected_loc", [("a", 0), ("b", 1), ("c", 2)])
def test_get_loc_should_return_int_for_unique_index(key, expected_loc):
    """Behavior: get_loc on a unique index returns an integer position."""
    # The pandas result is used as the known-correct value.
    # We assert our implementation matches it and the expected type.
    bf_index = bpd.Index(["a", "b", "c"])

    result = bf_index.get_loc(key)

    assert result == expected_loc
    assert isinstance(result, int)


def test_get_loc_should_return_slice_for_monotonic_duplicates():
    """Behavior: get_loc on a monotonic string index with duplicates returns a slice."""
    bf_index = bpd.Index(["a", "b", "b", "c"])
    pd_index = pd.Index(["a", "b", "b", "c"])

    bf_result = bf_index.get_loc("b")
    pd_result = pd_index.get_loc("b")

    assert isinstance(bf_result, slice)
    assert bf_result == pd_result  # Should be slice(1, 3, None)


def test_get_loc_should_return_slice_for_monotonic_numeric_duplicates():
    """Behavior: get_loc on a monotonic numeric index with duplicates returns a slice."""
    bf_index = bpd.Index([1, 2, 2, 3])
    pd_index = pd.Index([1, 2, 2, 3])

    bf_result = bf_index.get_loc(2)
    pd_result = pd_index.get_loc(2)

    assert isinstance(bf_result, slice)
    assert bf_result == pd_result  # Should be slice(1, 3, None)


def test_get_loc_should_return_mask_for_non_monotonic_duplicates():
    """Behavior: get_loc on a non-monotonic string index returns a boolean array."""
    bf_index = bpd.Index(["a", "b", "c", "b"])
    pd_index = pd.Index(["a", "b", "c", "b"])

    pd_result = pd_index.get_loc("b")
    bf_result = bf_index.get_loc("b")

    assert not isinstance(bf_result, (int, slice))

    if hasattr(bf_result, "to_numpy"):
        bf_array = bf_result.to_numpy()
    else:
        bf_array = bf_result.to_pandas().to_numpy()
    numpy.testing.assert_array_equal(bf_array, pd_result)


def test_get_loc_should_return_mask_for_non_monotonic_numeric_duplicates():
    """Behavior: get_loc on a non-monotonic numeric index returns a boolean array."""
    bf_index = bpd.Index([1, 2, 3, 2])
    pd_index = pd.Index([1, 2, 3, 2])

    pd_result = pd_index.get_loc(2)
    bf_result = bf_index.get_loc(2)

    assert not isinstance(bf_result, (int, slice))

    if hasattr(bf_result, "to_numpy"):
        bf_array = bf_result.to_numpy()
    else:
        bf_array = bf_result.to_pandas().to_numpy()
    numpy.testing.assert_array_equal(bf_array, pd_result)


def test_get_loc_should_raise_error_for_missing_key():
    """Behavior: get_loc raises KeyError when a string key is not found."""
    bf_index = bpd.Index(["a", "b", "c"])

    with pytest.raises(KeyError):
        bf_index.get_loc("d")


def test_get_loc_should_raise_error_for_missing_numeric_key():
    """Behavior: get_loc raises KeyError when a numeric key is not found."""
    bf_index = bpd.Index([1, 2, 3])

    with pytest.raises(KeyError):
        bf_index.get_loc(4)


def test_get_loc_should_work_for_single_element_index():
    """Behavior: get_loc on a single-element index returns 0."""
    assert bpd.Index(["a"]).get_loc("a") == pd.Index(["a"]).get_loc("a")


def test_get_loc_should_return_slice_when_all_elements_are_duplicates():
    """Behavior: get_loc returns a full slice if all elements match the key."""
    bf_index = bpd.Index(["a", "a", "a"])
    pd_index = pd.Index(["a", "a", "a"])

    bf_result = bf_index.get_loc("a")
    pd_result = pd_index.get_loc("a")

    assert isinstance(bf_result, slice)
    assert bf_result == pd_result  # Should be slice(0, 3, None)


def test_index_construct_from_series():
    bf_result = bpd.Index(
        bpd.Series([3, 14, 159], dtype=pd.Float64Dtype(), name="series_name"),
        name="index_name",
        dtype=pd.Int64Dtype(),
    ).to_pandas()
    pd_result: pd.Index = pd.Index(
        pd.Series([3, 14, 159], dtype=pd.Float64Dtype(), name="series_name"),
        name="index_name",
        dtype=pd.Int64Dtype(),
    )
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_construct_from_index():
    bf_index_input = bpd.Index(
        [3, 14, 159], dtype=pd.Float64Dtype(), name="series_name"
    )
    bf_result = bpd.Index(
        bf_index_input, dtype=pd.Int64Dtype(), name="index_name"
    ).to_pandas()
    pd_index_input: pd.Index = pd.Index(
        [3, 14, 159], dtype=pd.Float64Dtype(), name="series_name"
    )
    pd_result: pd.Index = pd.Index(
        pd_index_input, dtype=pd.Int64Dtype(), name="index_name"
    )
    pd.testing.assert_index_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("json_type"),
    [
        pytest.param(dtypes.JSON_DTYPE),
        pytest.param("json"),
    ],
)
def test_index_construct_w_json_dtype(json_type):
    data = [
        "1",
        "false",
        '["a", {"b": 1}, null]',
        None,
    ]
    index = bpd.Index(data, dtype=json_type)

    assert index.dtype == dtypes.JSON_DTYPE
    assert index[1] == "false"


def test_get_index(scalars_df_index, scalars_pandas_df_index):
    index = scalars_df_index.index
    bf_result = index.to_pandas()
    pd_result = scalars_pandas_df_index.index

    assert_pandas_index_equal_ignore_index_type(bf_result, pd_result)


def test_index_has_duplicates(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.has_duplicates
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.has_duplicates
    assert bf_result == pd_result


def test_index_empty_has_duplicates():
    assert not bpd.Index([]).has_duplicates


def test_index_values(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.values
    pd_result = scalars_pandas_df_index.index.values

    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    pd.testing.assert_series_equal(
        pd.Series(bf_result), pd.Series(pd_result), check_dtype=False
    )


def test_index_ndim(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.ndim
    pd_result = scalars_pandas_df_index.index.ndim

    assert pd_result == bf_result


def test_index_dtype(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.dtype
    pd_result = scalars_pandas_df_index.index.dtype

    assert pd_result == bf_result


def test_index_dtypes(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index(["string_col", "int64_too"]).index.dtypes
    pd_result = scalars_pandas_df_index.set_index(
        ["string_col", "int64_too"]
    ).index.dtypes
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_index_shape(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.shape
    pd_result = scalars_pandas_df_index.index.shape

    assert bf_result == pd_result


def test_index_astype(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.set_index("int64_col").index.astype("Float64").to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.astype("Float64")
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_astype_python(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.astype(float).to_pandas()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.astype("Float64")
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_astype_error_error(session):
    input = pd.Index(["hello", "world", "3.11", "4000"])
    with pytest.raises(ValueError):
        session.read_pandas(input).astype("Float64", errors="bad_value")


def test_index_any(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.any()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.any()
    assert bf_result == pd_result


def test_index_all(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.all()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.all()
    assert bf_result == pd_result


def test_index_max(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.max()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.max()
    assert bf_result == pd_result


def test_index_min(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.min()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.min()
    assert bf_result == pd_result


def test_index_nunique(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.nunique()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.nunique()
    assert bf_result == pd_result


def test_index_fillna(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.fillna(42).to_pandas()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.fillna(42)

    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_drop(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.set_index("int64_col").index.drop([2, 314159]).to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.drop([2, 314159])
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_rename(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index("int64_col").index.rename("name").to_pandas()
    pd_result = scalars_pandas_df_index.set_index("int64_col").index.rename("name")
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_multi_rename(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.set_index(["int64_col", "int64_too"])
        .index.rename(["new", "names"])
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_col", "int64_too"]
    ).index.rename(["new", "names"])
    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_len(scalars_df_index, scalars_pandas_df_index):
    bf_result = len(scalars_df_index.index)
    pd_result = len(scalars_pandas_df_index.index)

    assert bf_result == pd_result


def test_index_array(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.__array__()
    pd_result = scalars_pandas_df_index.index.__array__()

    numpy.array_equal(bf_result, pd_result)


def test_index_getitem_int(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index[-2]
    pd_result = scalars_pandas_df_index.index[-2]
    assert bf_result == pd_result


def test_is_monotonic_increasing(scalars_df_index, scalars_pandas_df_index):
    assert (
        scalars_df_index.index.is_monotonic_increasing
        == scalars_pandas_df_index.index.is_monotonic_increasing
    )


def test_is_monotonic_decreasing(scalars_df_index, scalars_pandas_df_index):
    assert (
        scalars_df_index.index.is_monotonic_increasing
        == scalars_pandas_df_index.index.is_monotonic_increasing
    )


def test_index_argmin(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("1."):
        pytest.skip("doesn't work in pandas 1.x.")
    bf_result = scalars_df_index.set_index(["int64_too", "rowindex_2"]).index.argmin()
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_too", "rowindex_2"]
    ).index.argmin()
    assert bf_result == pd_result


def test_index_argmax(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("1."):
        pytest.skip("doesn't work in pandas 1.x.")
    bf_result = scalars_df_index.set_index(["int64_too", "rowindex_2"]).index.argmax()
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_too", "rowindex_2"]
    ).index.argmax()
    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("ascending", "na_position"),
    [
        (True, "first"),
        (True, "last"),
        (False, "first"),
        (False, "last"),
    ],
)
def test_index_sort_values(
    scalars_df_index, scalars_pandas_df_index, ascending, na_position
):
    # Test needs values to be unique
    bf_result = (
        scalars_df_index.set_index(["int64_too", "rowindex_2"])
        .index.sort_values(ascending=ascending, na_position=na_position)
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_too", "rowindex_2"]
    ).index.sort_values(ascending=ascending, na_position=na_position)

    pd.testing.assert_index_equal(
        bf_result,
        pd_result,
    )


def test_index_value_counts(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("1."):
        pytest.skip("value_counts results different in pandas 1.x.")
    bf_result = (
        scalars_df_index.set_index(["int64_too", "rowindex_2"])
        .index.value_counts()
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_too", "rowindex_2"]
    ).index.value_counts()

    pd.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("level",),
    [
        ("int64_too",),
        ("rowindex_2",),
        (1,),
    ],
)
def test_index_get_level_values(scalars_df_index, scalars_pandas_df_index, level):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "rowindex_2"])
        .index.get_level_values(level)
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_too", "rowindex_2"]
    ).index.get_level_values(level)

    pd.testing.assert_index_equal(bf_result, pd_result)


def test_index_to_series(
    scalars_df_index,
    scalars_pandas_df_index,
):
    bf_result = (
        scalars_df_index.set_index(["int64_too"])
        .index.to_series(index=scalars_df_index["float64_col"], name="new_name")
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(["int64_too"]).index.to_series(
        index=scalars_pandas_df_index["float64_col"], name="new_name"
    )

    pd.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("how",),
    [
        ("any",),
        ("all",),
    ],
)
def test_index_dropna(scalars_df_index, scalars_pandas_df_index, how):
    bf_result = (
        scalars_df_index.set_index(["int64_col", "float64_col"])
        .index.dropna(how=how)
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["int64_col", "float64_col"]
    ).index.dropna(how=how)
    pd.testing.assert_index_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        (False,),
    ],
)
def test_index_drop_duplicates(scalars_df_index, scalars_pandas_df_index, keep):
    bf_series = (
        scalars_df_index.set_index("int64_col")
        .index.drop_duplicates(keep=keep)
        .to_pandas()
    )
    pd_series = scalars_pandas_df_index.set_index("int64_col").index.drop_duplicates(
        keep=keep
    )
    pd.testing.assert_index_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("key",),
    [("hello",), (2,), (123123321,), (2.0,), (False,), ((2,),), (pd.NA,)],
)
def test_index_contains(scalars_df_index, scalars_pandas_df_index, key):
    col_name = "int64_col"
    bf_result = key in scalars_df_index.set_index(col_name).index
    pd_result = key in scalars_pandas_df_index.set_index(col_name).index

    assert bf_result == pd_result


def test_index_isin_list(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_series = (
        scalars_df_index.set_index(col_name).index.isin([2, 55555, 4]).to_pandas()
    )
    pd_result_array = scalars_pandas_df_index.set_index(col_name).index.isin(
        [2, 55555, 4]
    )
    pd.testing.assert_index_equal(
        pd.Index(pd_result_array).set_names(col_name),
        bf_series,
    )


def test_index_isin_bf_series(scalars_df_index, scalars_pandas_df_index, session):
    col_name = "int64_col"
    bf_series = (
        scalars_df_index.set_index(col_name)
        .index.isin(bpd.Series([2, 55555, 4], session=session))
        .to_pandas()
    )
    pd_result_array = scalars_pandas_df_index.set_index(col_name).index.isin(
        [2, 55555, 4]
    )
    pd.testing.assert_index_equal(
        pd.Index(pd_result_array).set_names(col_name),
        bf_series,
    )


def test_index_isin_bf_index(scalars_df_index, scalars_pandas_df_index, session):
    col_name = "int64_col"
    bf_series = (
        scalars_df_index.set_index(col_name)
        .index.isin(bpd.Index([2, 55555, 4], session=session))
        .to_pandas()
    )
    pd_result_array = scalars_pandas_df_index.set_index(col_name).index.isin(
        [2, 55555, 4]
    )
    pd.testing.assert_index_equal(
        pd.Index(pd_result_array).set_names(col_name),
        bf_series,
    )


def test_multiindex_name_is_none(session):
    df = pd.DataFrame(
        {
            "A": [0, 0, 0, 1, 1, 1],
            "B": ["x", "y", "z", "x", "y", "z"],
            "C": [123, 345, 789, -123, -345, -789],
            "D": ["a", "b", "c", "d", "e", "f"],
        },
    )
    index = session.read_pandas(df).set_index(["A", "B"]).index
    assert index.name is None


def test_multiindex_names_not_none(session):
    df = pd.DataFrame(
        {
            "A": [0, 0, 0, 1, 1, 1],
            "B": ["x", "y", "z", "x", "y", "z"],
            "C": [123, 345, 789, -123, -345, -789],
            "D": ["a", "b", "c", "d", "e", "f"],
        },
    )
    index = session.read_pandas(df).set_index(["A", "B"]).index
    assert tuple(index.names) == ("A", "B")


def test_multiindex_repr_includes_all_names(session):
    df = pd.DataFrame(
        {
            "A": [0, 0, 0, 1, 1, 1],
            "B": ["x", "y", "z", "x", "y", "z"],
            "C": [123, 345, 789, -123, -345, -789],
            "D": ["a", "b", "c", "d", "e", "f"],
        },
    )
    index = session.read_pandas(df).set_index(["A", "B"]).index
    assert "names=['A', 'B']" in repr(index)


def test_index_item(session):
    # Test with a single item
    bf_idx_single = bpd.Index([42], session=session)
    pd_idx_single = pd.Index([42])
    assert bf_idx_single.item() == pd_idx_single.item()


def test_index_item_with_multiple(session):
    # Test with multiple items
    bf_idx_multiple = bpd.Index([1, 2, 3], session=session)
    pd_idx_multiple = pd.Index([1, 2, 3])

    try:
        pd_idx_multiple.item()
    except ValueError as e:
        expected_message = str(e)
    else:
        raise AssertionError("Expected ValueError from pandas, but didn't get one")

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        bf_idx_multiple.item()


def test_index_item_with_empty(session):
    # Test with an empty Index
    bf_idx_empty = bpd.Index([], dtype="Int64", session=session)
    pd_idx_empty: pd.Index = pd.Index([], dtype="Int64")

    try:
        pd_idx_empty.item()
    except ValueError as e:
        expected_message = str(e)
    else:
        raise AssertionError("Expected ValueError from pandas, but didn't get one")

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        bf_idx_empty.item()


def test_index_to_list(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.index.to_list()
    pd_result = scalars_pandas_df_index.index.to_list()
    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("key", "value"),
    [
        (0, "string_value"),
        (1, 42),
        ("label", None),
        (-1, 3.14),
    ],
)
def test_index_setitem_different_types(scalars_dfs, key, value):
    """Tests that custom Index setitem raises TypeError."""
    scalars_df, _ = scalars_dfs
    index = scalars_df.index

    with pytest.raises(TypeError, match="Index does not support mutable operations"):
        index[key] = value


def test_custom_index_setitem_error():
    """Tests that custom Index setitem raises TypeError."""
    custom_index = bpd.Index([1, 2, 3, 4, 5], name="custom")

    with pytest.raises(TypeError, match="Index does not support mutable operations"):
        custom_index[2] = 999


def test_index_eq_const(scalars_df_index, scalars_pandas_df_index):
    bf_result = (scalars_df_index.index == 3).to_pandas()
    pd_result = scalars_pandas_df_index.index == 3
    assert bf_result == pd.Index(pd_result)


def test_index_eq_aligned_index(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        bpd.Index(scalars_df_index.int64_col)
        == bpd.Index(scalars_df_index.int64_col.abs())
    ).to_pandas()
    pd_result = pd.Index(scalars_pandas_df_index.int64_col) == pd.Index(
        scalars_pandas_df_index.int64_col.abs()
    )
    assert bf_result == pd.Index(pd_result)
