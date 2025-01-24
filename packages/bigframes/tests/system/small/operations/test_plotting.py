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

from matplotlib.collections import PathCollection
import numpy as np
import pandas as pd
import pandas._testing as tm
import pytest

import bigframes.operations._matplotlib.core as bf_mpl
import bigframes.pandas as bpd


def _check_legend_labels(ax, labels):
    """
    Check the ax has expected legend label
    """
    assert ax.get_legend() is not None
    texts = ax.get_legend().get_texts()
    actual_labels = [t.get_text() for t in texts]
    assert len(actual_labels) == len(labels)
    for label, e in zip(actual_labels, labels):
        assert label == e


@pytest.mark.parametrize(
    ("alias"),
    [
        pytest.param(True),
        pytest.param(False),
    ],
)
def test_series_hist_bins(scalars_dfs, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    bins = 5
    if alias:
        ax = scalars_df["int64_col"].hist(bins=bins)
    else:
        ax = scalars_df["int64_col"].plot.hist(bins=bins)
    pd_ax = scalars_pandas_df["int64_col"].plot.hist(bins=bins)

    # Compares axis values and height between bigframes and pandas histograms.
    # Note: Due to potential float rounding by matplotlib, this test may not
    # be applied to all cases.
    assert len(ax.patches) == len(pd_ax.patches)
    for i in range(len(ax.patches)):
        assert ax.patches[i].xy == pd_ax.patches[i].xy
        assert ax.patches[i]._height == pd_ax.patches[i]._height


@pytest.mark.parametrize(
    ("alias"),
    [
        pytest.param(True),
        pytest.param(False),
    ],
)
def test_dataframes_hist_bins(scalars_dfs, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    bins = 7
    columns = ["int64_col", "int64_too", "float64_col"]
    if alias:
        ax = scalars_df[columns].hist(bins=bins)
    else:
        ax = scalars_df[columns].plot.hist(bins=bins)
    pd_ax = scalars_pandas_df[columns].plot.hist(bins=bins)

    # Compares axis values and height between bigframes and pandas histograms.
    # Note: Due to potential float rounding by matplotlib, this test may not
    # be applied to all cases.
    assert len(ax.patches) == len(pd_ax.patches)
    for i in range(len(ax.patches)):
        assert ax.patches[i]._height == pd_ax.patches[i]._height


@pytest.mark.parametrize(
    ("col_names"),
    [
        pytest.param(["int64_col"]),
        pytest.param(["float64_col"]),
        pytest.param(["int64_too", "bool_col"]),
        pytest.param(["bool_col"], marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(["date_col"], marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(["datetime_col"], marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(["time_col"], marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(["timestamp_col"], marks=pytest.mark.xfail(raises=TypeError)),
    ],
)
def test_hist_include_types(scalars_dfs, col_names):
    scalars_df, _ = scalars_dfs
    ax = scalars_df[col_names].plot.hist()
    assert len(ax.patches) == 10


@pytest.mark.parametrize(
    ("arg_name", "arg_value"),
    [
        pytest.param(
            "by", ["int64_col"], marks=pytest.mark.xfail(raises=NotImplementedError)
        ),
        pytest.param(
            "bins", [1, 3, 5], marks=pytest.mark.xfail(raises=NotImplementedError)
        ),
        pytest.param(
            "weight", [2, 3], marks=pytest.mark.xfail(raises=NotImplementedError)
        ),
        pytest.param(
            "backend",
            "backend.module",
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
    ],
)
def test_hist_not_implemented_error(scalars_dfs, arg_name, arg_value):
    scalars_df, _ = scalars_dfs
    kwargs = {arg_name: arg_value}
    scalars_df.plot.hist(**kwargs)


def test_hist_kwargs_true_subplots(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["int64_col", "int64_too", "float64_col"]
    axes = scalars_df[columns].plot.hist(subplots=True)
    pd_axes = scalars_pandas_df[columns].plot.hist(subplots=True)
    assert len(axes) == len(pd_axes)

    expected_labels = (["int64_col"], ["int64_too"], ["float64_col"])
    for ax, labels in zip(axes, expected_labels):
        _check_legend_labels(ax, labels)


def test_hist_kwargs_list_subplots(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["int64_col", "int64_too", "float64_col"]
    subplots = [["int64_col", "int64_too"]]
    axes = scalars_df[columns].plot.hist(subplots=subplots)
    pd_axes = scalars_pandas_df[columns].plot.hist(subplots=subplots)
    assert len(axes) == len(pd_axes)

    expected_labels = (["int64_col", "int64_too"], ["float64_col"])
    for ax, labels in zip(axes, expected_labels):
        _check_legend_labels(ax, labels=labels)


@pytest.mark.parametrize(
    ("orientation"),
    [
        pytest.param("horizontal"),
        pytest.param("vertical"),
    ],
)
def test_hist_kwargs_orientation(scalars_dfs, orientation):
    scalars_df, scalars_pandas_df = scalars_dfs
    ax = scalars_df["int64_col"].plot.hist(orientation=orientation)
    pd_ax = scalars_pandas_df["int64_col"].plot.hist(orientation=orientation)
    assert ax.xaxis.get_label().get_text() == pd_ax.xaxis.get_label().get_text()
    assert ax.yaxis.get_label().get_text() == pd_ax.yaxis.get_label().get_text()


def test_hist_kwargs_ticks_props(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    xticks = [20, 18]
    yticks = [30, 40]

    ax = scalars_df["float64_col"].plot.hist(xticks=xticks, yticks=yticks)
    pd_ax = scalars_pandas_df["float64_col"].plot.hist(xticks=xticks, yticks=yticks)
    xlabels = ax.get_xticklabels()
    pd_xlables = pd_ax.get_xticklabels()
    assert len(xlabels) == len(pd_xlables)
    for i in range(len(pd_xlables)):
        tm.assert_almost_equal(xlabels[i].get_fontsize(), pd_xlables[i].get_fontsize())
        tm.assert_almost_equal(xlabels[i].get_rotation(), pd_xlables[i].get_rotation())

    ylabels = ax.get_yticklabels()
    pd_ylables = pd_ax.get_yticklabels()
    assert len(xlabels) == len(pd_xlables)
    for i in range(len(pd_xlables)):
        tm.assert_almost_equal(ylabels[i].get_fontsize(), pd_ylables[i].get_fontsize())
        tm.assert_almost_equal(ylabels[i].get_rotation(), pd_ylables[i].get_rotation())


@pytest.mark.parametrize(
    ("col_names", "alias"),
    [
        pytest.param(
            ["int64_col", "float64_col", "int64_too", "bool_col"], True, id="df_alias"
        ),
        pytest.param(
            ["int64_col", "float64_col", "int64_too", "bool_col"], False, id="df"
        ),
        pytest.param(["int64_col"], True, id="series_alias"),
        pytest.param(["int64_col"], False, id="series"),
    ],
)
def test_line(scalars_dfs, col_names, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    if alias:
        ax = scalars_df[col_names].line()
    else:
        ax = scalars_df[col_names].plot.line()
    pd_ax = scalars_pandas_df[col_names].plot.line()
    tm.assert_almost_equal(ax.get_xticks(), pd_ax.get_xticks())
    tm.assert_almost_equal(ax.get_yticks(), pd_ax.get_yticks())
    for line, pd_line in zip(ax.lines, pd_ax.lines):
        # Compare y coordinates between the lines
        tm.assert_almost_equal(line.get_data()[1], pd_line.get_data()[1])


@pytest.mark.parametrize(
    ("col_names", "alias"),
    [
        pytest.param(["int64_col", "float64_col", "int64_too"], True, id="df_alias"),
        pytest.param(["int64_col", "float64_col", "int64_too"], False, id="df"),
        pytest.param(["int64_col"], True, id="series_alias"),
        pytest.param(["int64_col"], False, id="series"),
    ],
)
def test_area(scalars_dfs, col_names, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    if alias:
        ax = scalars_df[col_names].area(stacked=False)
    else:
        ax = scalars_df[col_names].plot.area(stacked=False)
    pd_ax = scalars_pandas_df[col_names].plot.area(stacked=False)
    tm.assert_almost_equal(ax.get_xticks(), pd_ax.get_xticks())
    tm.assert_almost_equal(ax.get_yticks(), pd_ax.get_yticks())
    for line, pd_line in zip(ax.lines, pd_ax.lines):
        # Compare y coordinates between the lines
        tm.assert_almost_equal(line.get_data()[1], pd_line.get_data()[1])


@pytest.mark.parametrize(
    ("col_names", "alias"),
    [
        pytest.param(["int64_col", "float64_col", "int64_too"], True, id="df_alias"),
        pytest.param(["int64_col", "float64_col", "int64_too"], False, id="df"),
        pytest.param(["int64_col"], True, id="series_alias"),
        pytest.param(["int64_col"], False, id="series"),
    ],
)
def test_bar(scalars_dfs, col_names, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    if alias:
        ax = scalars_df[col_names].bar()
    else:
        ax = scalars_df[col_names].plot.bar()
    pd_ax = scalars_pandas_df[col_names].plot.bar()
    tm.assert_almost_equal(ax.get_xticks(), pd_ax.get_xticks())
    tm.assert_almost_equal(ax.get_yticks(), pd_ax.get_yticks())
    for line, pd_line in zip(ax.lines, pd_ax.lines):
        # Compare y coordinates between the lines
        tm.assert_almost_equal(line.get_data()[1], pd_line.get_data()[1])


@pytest.mark.parametrize(
    ("col_names", "alias"),
    [
        pytest.param(
            ["int64_col", "float64_col", "int64_too", "bool_col"], True, id="df_alias"
        ),
        pytest.param(
            ["int64_col", "float64_col", "int64_too", "bool_col"], False, id="df"
        ),
    ],
)
def test_scatter(scalars_dfs, col_names, alias):
    scalars_df, scalars_pandas_df = scalars_dfs
    if alias:
        ax = scalars_df[col_names].scatter(x="int64_col", y="float64_col")
    else:
        ax = scalars_df[col_names].plot.scatter(x="int64_col", y="float64_col")
    pd_ax = scalars_pandas_df[col_names].plot.scatter(x="int64_col", y="float64_col")
    tm.assert_almost_equal(ax.get_xticks(), pd_ax.get_xticks())
    tm.assert_almost_equal(ax.get_yticks(), pd_ax.get_yticks())
    tm.assert_almost_equal(
        ax.collections[0].get_sizes(), pd_ax.collections[0].get_sizes()
    )


@pytest.mark.parametrize(
    ("c"),
    [
        pytest.param("red", id="red"),
        pytest.param("c", id="int_column"),
        pytest.param("species", id="color_column"),
        pytest.param(3, id="column_index"),
    ],
)
def test_scatter_args_c(c):
    data = {
        "a": [1, 2, 3],
        "b": [1, 2, 3],
        "c": [1, 2, 3],
        "species": ["r", "g", "b"],
    }
    df = bpd.DataFrame(data)
    pd_df = pd.DataFrame(data)

    ax = df.plot.scatter(x="a", y="b", c=c)
    pd_ax = pd_df.plot.scatter(x="a", y="b", c=c)
    assert len(ax.collections[0].get_facecolor()) == len(
        pd_ax.collections[0].get_facecolor()
    )
    for idx in range(len(ax.collections[0].get_facecolor())):
        tm.assert_numpy_array_equal(
            ax.collections[0].get_facecolor()[idx],
            pd_ax.collections[0].get_facecolor()[idx],
        )


@pytest.mark.parametrize(
    ("s"),
    [
        pytest.param([10, 34, 50], id="int"),
        pytest.param([1.0, 3.4, 5.0], id="float"),
        pytest.param(
            [True, True, False], id="bool", marks=pytest.mark.xfail(raises=ValueError)
        ),
    ],
)
def test_scatter_args_s(s):
    data = {
        "a": [1, 2, 3],
        "b": [1, 2, 3],
    }
    data["s"] = s
    df = bpd.DataFrame(data)
    pd_df = pd.DataFrame(data)

    ax = df.plot.scatter(x="a", y="b", s="s")
    pd_ax = pd_df.plot.scatter(x="a", y="b", s="s")

    assert isinstance(pd_ax.collections[0], PathCollection)
    tm.assert_numpy_array_equal(
        ax.collections[0].get_sizes(), pd_ax.collections[0].get_sizes()
    )


@pytest.mark.parametrize(
    ("arg_name"),
    [
        pytest.param("c", marks=pytest.mark.xfail(raises=NotImplementedError)),
        pytest.param("s", marks=pytest.mark.xfail(raises=NotImplementedError)),
    ],
)
def test_scatter_sequence_arg(arg_name):
    data = {
        "a": [1, 2, 3],
        "b": [1, 2, 3],
    }
    arg_value = [3, 3, 1]
    bpd.DataFrame(data).plot.scatter(x="a", y="b", **{arg_name: arg_value})


def test_sampling_plot_args_n():
    df = bpd.DataFrame(np.arange(bf_mpl.DEFAULT_SAMPLING_N * 10), columns=["one"])
    ax = df.plot.line()
    assert len(ax.lines) == 1
    assert len(ax.lines[0].get_data()[1]) == bf_mpl.DEFAULT_SAMPLING_N

    ax = df.plot.line(sampling_n=2)
    assert len(ax.lines) == 1
    assert len(ax.lines[0].get_data()[1]) == 2


def test_sampling_plot_args_random_state():
    df = bpd.DataFrame(np.arange(bf_mpl.DEFAULT_SAMPLING_N * 10), columns=["one"])
    ax_0 = df.plot.line()
    ax_1 = df.plot.line()
    ax_2 = df.plot.line(sampling_random_state=100)
    ax_3 = df.plot.line(sampling_random_state=100)

    # Setting a fixed sampling_random_state guarantees reproducible plotted sampling.
    tm.assert_almost_equal(ax_0.lines[0].get_data()[1], ax_1.lines[0].get_data()[1])
    tm.assert_almost_equal(ax_2.lines[0].get_data()[1], ax_3.lines[0].get_data()[1])

    msg = "numpy array are different"
    with pytest.raises(AssertionError, match=msg):
        tm.assert_almost_equal(ax_0.lines[0].get_data()[1], ax_2.lines[0].get_data()[1])


def test_sampling_preserve_ordering():
    df = bpd.DataFrame([0.0, 1.0, 2.0, 3.0, 4.0], index=[1, 3, 4, 2, 0])
    pd_df = pd.DataFrame([0.0, 1.0, 2.0, 3.0, 4.0], index=[1, 3, 4, 2, 0])
    ax = df.plot.line()
    pd_ax = pd_df.plot.line()
    tm.assert_almost_equal(ax.get_xticks(), pd_ax.get_xticks())
    tm.assert_almost_equal(ax.get_yticks(), pd_ax.get_yticks())
    for line, pd_line in zip(ax.lines, pd_ax.lines):
        # Compare y coordinates between the lines
        tm.assert_almost_equal(line.get_data()[1], pd_line.get_data()[1])


@pytest.mark.parametrize(
    ("kind", "col_names", "kwargs"),
    [
        pytest.param("hist", ["int64_col", "int64_too"], {}),
        pytest.param("line", ["int64_col", "int64_too"], {}),
        pytest.param("area", ["int64_col", "int64_too"], {"stacked": False}),
        pytest.param(
            "scatter", ["int64_col", "int64_too"], {"x": "int64_col", "y": "int64_too"}
        ),
        pytest.param(
            "scatter",
            ["int64_col"],
            {},
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            "bar",
            ["int64_col", "int64_too"],
            {},
            marks=pytest.mark.xfail(raises=NotImplementedError),
        ),
    ],
)
def test_plot_call(scalars_dfs, kind, col_names, kwargs):
    scalars_df, _ = scalars_dfs
    scalars_df[col_names].plot(kind=kind, **kwargs)
