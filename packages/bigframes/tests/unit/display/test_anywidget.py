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

import signal
import unittest.mock as mock

import pandas as pd
import pytest

import bigframes

# Skip if anywidget/traitlets not installed, though they should be in the dev env
pytest.importorskip("anywidget")
pytest.importorskip("traitlets")

from bigframes.core.blocks import Block
from bigframes.dataframe import DataFrame
from bigframes.display.anywidget import TableWidget
from bigframes.dtypes import JSON_DTYPE, STRING_DTYPE, struct_type
from bigframes.operations import SqlScalarOp


def test_navigation_to_invalid_page_resets_to_valid_page_without_deadlock():
    """
    Given a widget on a page beyond available data, when navigating,
    then it should reset to the last valid page without deadlock.
    """
    mock_df = mock.create_autospec(bigframes.dataframe.DataFrame, instance=True)
    mock_df.columns = ["col1"]
    mock_df.dtypes = {"col1": "object"}

    mock_block = mock.Mock()
    mock_block.has_index = False
    mock_df._block = mock_block

    # We mock _initial_load to avoid complex setup
    with mock.patch.object(TableWidget, "_initial_load"):
        with bigframes.option_context(
            "display.render_mode", "anywidget", "display.max_rows", 10
        ):
            widget = TableWidget(mock_df)

    # Simulate "loaded data but unknown total rows" state
    widget.page_size = 10
    widget.row_count = None
    widget._all_data_loaded = True

    # Populate cache with 1 page of data (10 rows). Page 0 is valid, page 1+ are invalid.
    widget._cached_batches = [pd.DataFrame({"col1": range(10)})]

    # Mark initial load as complete so observers fire
    widget._initial_load_complete = True

    # Setup timeout to fail fast if deadlock occurs
    # signal.SIGALRM is not available on Windows
    has_sigalrm = hasattr(signal, "SIGALRM")
    if has_sigalrm:

        def handler(signum, frame):
            raise TimeoutError("Deadlock detected!")

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(2)  # 2 seconds timeout

    try:
        # Trigger navigation to page 5 (invalid), which should reset to page 0
        widget.page = 5

        assert widget.page == 0

    finally:
        if has_sigalrm:
            signal.alarm(0)


def test_css_contains_dark_mode_selectors():
    """Test that the CSS for dark mode is loaded with all required selectors."""
    mock_df = mock.create_autospec(bigframes.dataframe.DataFrame, instance=True)
    # mock_df.columns and mock_df.dtypes are needed for __init__
    mock_df.columns = ["col1"]
    mock_df.dtypes = {"col1": "object"}

    # Mock _block to avoid AttributeError during _set_table_html
    mock_block = mock.Mock()
    mock_block.has_index = False
    mock_df._block = mock_block

    with mock.patch.object(TableWidget, "_initial_load"):
        widget = TableWidget(mock_df)
        css = widget._css
        assert "@media (prefers-color-scheme: dark)" in css
        assert 'html[theme="dark"]' in css
        assert 'body[data-theme="dark"]' in css


@pytest.fixture
def mock_df():
    """A mock DataFrame that can be used in multiple tests."""
    df = mock.create_autospec(bigframes.dataframe.DataFrame, instance=True)
    df.columns = ["col1", "col2"]
    df.dtypes = {"col1": "int64", "col2": "int64"}

    mock_block = mock.Mock()
    mock_block.has_index = False
    df._block = mock_block

    # Mock to_pandas_batches to return empty iterator or simple data
    batch_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    batches = mock.MagicMock()
    batches.__iter__.return_value = iter([batch_df])
    batches.total_rows = 2
    df.to_pandas_batches.return_value = batches

    # Mock sort_values to return self (for chaining)
    df.sort_values.return_value = df

    return df


def test_sorting_single_column(mock_df):
    """Test that the widget can be sorted by a single column."""
    with bigframes.option_context("display.render_mode", "anywidget"):
        widget = TableWidget(mock_df)

    # Verify initial state
    assert widget.sort_context == []

    # Apply sort
    widget.sort_context = [{"column": "col1", "ascending": True}]

    # This should trigger _sort_changed -> _set_table_html
    # which calls df.sort_values

    mock_df.sort_values.assert_called_with(by=["col1"], ascending=[True])


def test_sorting_multi_column(mock_df):
    """Test that the widget can be sorted by multiple columns."""
    with bigframes.option_context("display.render_mode", "anywidget"):
        widget = TableWidget(mock_df)

    # Apply multi-column sort
    widget.sort_context = [
        {"column": "col1", "ascending": True},
        {"column": "col2", "ascending": False},
    ]

    mock_df.sort_values.assert_called_with(by=["col1", "col2"], ascending=[True, False])


def test_page_size_change_resets_sort(mock_df):
    """Test that changing the page size resets the sorting."""
    with bigframes.option_context("display.render_mode", "anywidget"):
        widget = TableWidget(mock_df)

    # Set sort state
    widget.sort_context = [{"column": "col1", "ascending": True}]

    # Change page size
    widget.page_size = 50

    # Sort should be reset
    assert widget.sort_context == []

    # to_pandas_batches called again (reset)
    assert mock_df.to_pandas_batches.call_count >= 2


def test_cell_execution_count_propagation(mock_df):
    """Test that the captured cell_execution_count is propagated to to_pandas_batches."""
    with mock.patch(
        "bigframes.core.utils.get_ipython_execution_count", return_value=42
    ):
        with bigframes.option_context("display.render_mode", "anywidget"):
            widget = TableWidget(mock_df)

    assert widget._cell_execution_count == 42

    mock_df.to_pandas_batches.assert_called_with(
        page_size=widget.page_size,
        cell_execution_count=42,
    )


def test_json_column_converted_to_string_for_display():
    mock_block = mock.Mock(spec=Block)
    mock_block.column_labels = pd.Index(["col_json"])
    mock_block.value_columns = ["col_json"]

    df = DataFrame(mock_block)
    df._block = mock_block

    mock_series = mock.Mock()
    mock_series.dtype = JSON_DTYPE

    with mock.patch.object(DataFrame, "__getitem__", return_value=mock_series):
        with mock.patch.object(DataFrame, "assign") as mock_assign:
            df._prepare_display_df()

            mock_assign.assert_called_once()
            _, kwargs = mock_assign.call_args
            assert "col_json" in kwargs

            mock_series._apply_unary_op.assert_called_once()
            call_arg = mock_series._apply_unary_op.call_args[0][0]
            assert isinstance(call_arg, SqlScalarOp)
            assert call_arg._output_type == STRING_DTYPE
            assert call_arg.sql_template == "TO_JSON_STRING({0})"


def test_struct_column_with_nested_json_converted_to_string_for_display():
    nested_struct_dtype = struct_type(
        [("field1", STRING_DTYPE), ("field2", JSON_DTYPE)]
    )

    mock_block = mock.Mock(spec=Block)
    mock_block.column_labels = pd.Index(["col_struct"])
    mock_block.value_columns = ["col_struct"]

    df = DataFrame(mock_block)
    df._block = mock_block

    mock_series = mock.Mock()
    mock_series.dtype = nested_struct_dtype

    with mock.patch.object(DataFrame, "__getitem__", return_value=mock_series):
        with mock.patch.object(DataFrame, "assign") as mock_assign:
            df._prepare_display_df()

            mock_assign.assert_called_once()
            _, kwargs = mock_assign.call_args
            assert "col_struct" in kwargs

            mock_series._apply_unary_op.assert_called_once()
            call_arg = mock_series._apply_unary_op.call_args[0][0]
            assert isinstance(call_arg, SqlScalarOp)
            assert call_arg._output_type == STRING_DTYPE
            assert call_arg.sql_template == "TO_JSON_STRING({0})"


@pytest.fixture
def mock_df_deferred():
    with mock.patch("bigframes.display.anywidget._ANYWIDGET_INSTALLED", True):
        df = mock.Mock(spec=bigframes.dataframe.DataFrame)
        df.shape = (100, 4)
        df.columns = ["A", "B", "C", "D"]
        df.dtypes = {
            "A": bigframes.dtypes.INT_DTYPE,
            "B": bigframes.dtypes.STRING_DTYPE,
            "C": bigframes.dtypes.FLOAT_DTYPE,
            "D": bigframes.dtypes.BOOL_DTYPE,
        }

        df.to_pandas_batches.return_value = iter(
            [pd.DataFrame({"A": [1], "B": ["a"], "C": [1.0], "D": [True]})]
        )

        df.sort_values.return_value = df

        df._block = mock.Mock()
        df._block.has_index = False
        df._prepare_display_df.return_value = df

        yield df


@pytest.fixture
def mock_deferred_df():
    from bigframes.session.deferred import DeferredBigQueryDataFrame

    with mock.patch("bigframes.display.anywidget._ANYWIDGET_INSTALLED", True):
        # We create a mock that subclasses DeferredBigQueryDataFrame so isinstance passes
        class MockDeferredBigQueryDataFrame(DeferredBigQueryDataFrame):
            def __init__(self):
                pass

        df = mock.MagicMock(spec=MockDeferredBigQueryDataFrame)
        df.__class__ = DeferredBigQueryDataFrame  # type: ignore[assignment]
        yield df


def test_init_raises_if_anywidget_not_installed():
    with mock.patch("bigframes.display.anywidget._ANYWIDGET_INSTALLED", False):
        with pytest.raises(ImportError):
            from bigframes.display.anywidget import TableWidget

            TableWidget(mock.Mock())


def test_init_initializes_attributes(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with bigframes.option_context("display.render_mode", "anywidget"):
        with mock.patch.object(TableWidget, "_initial_load"):
            widget = TableWidget(mock_df_deferred)

    assert widget._dataframe is mock_df_deferred
    assert widget.page == 0
    assert widget.page_size > 0
    assert widget.orderable_columns == [
        "A",
        "B",
        "C",
        "D",
    ]


def test_init_calls_initial_load(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with mock.patch.object(TableWidget, "_initial_load") as mock_load:
        TableWidget(mock_df_deferred)
        mock_load.assert_called_once()


def test_validate_page_clamping(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with mock.patch.object(TableWidget, "_initial_load"):
        widget = TableWidget(mock_df_deferred)
        widget.row_count = 100
        widget.page_size = 10

        widget.page = 5
        assert widget.page == 5

        with pytest.raises(ValueError):
            widget.page = -1

        widget.page = 100
        assert widget.page == 9


def test_validate_page_size(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with bigframes.option_context("display.render_mode", "anywidget"):
        with mock.patch.object(TableWidget, "_initial_load"):
            widget = TableWidget(mock_df_deferred)

            widget.page_size = 50
            assert widget.page_size == 50

            original_size = widget.page_size
            widget.page_size = -5
            assert widget.page_size == original_size

            widget.page_size = 10000
            assert widget.page_size == 1000


def test_page_size_change_resets_page_and_sort(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with mock.patch.object(TableWidget, "_initial_load"):
        widget = TableWidget(mock_df_deferred)
        widget._initial_load_complete = True
        widget.page = 5
        widget.sort_context = [{"column": "A", "ascending": True}]

        widget.page_size = 20

        assert widget.page == 0
        assert widget.sort_context == []


def test_page_size_change_resets_batches(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with mock.patch.object(TableWidget, "_initial_load"):
        widget = TableWidget(mock_df_deferred)
        widget._initial_load_complete = True

        widget.page_size = 50

    mock_df_deferred.to_pandas_batches.assert_called()


def test_sort_change_resets_batches(mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    with bigframes.option_context("display.render_mode", "anywidget"):
        with mock.patch.object(TableWidget, "_initial_load"):
            widget = TableWidget(mock_df_deferred)
            widget._initial_load_complete = True

            mock_df_deferred.to_pandas_batches.reset_mock()

            widget.sort_context = [{"column": "B", "ascending": False}]

    assert mock_df_deferred.to_pandas_batches.call_count >= 1


def test_deferred_mode_initialization(mock_deferred_df):
    from bigframes.display.anywidget import TableWidget

    with mock.patch.object(TableWidget, "_initial_load") as mock_load:
        widget = TableWidget(mock_deferred_df)

        assert widget.is_deferred_mode is True
        mock_load.assert_not_called()


def test_deferred_mode_execution(mock_deferred_df, mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    mock_deferred_df.execute.return_value = mock_df_deferred

    widget = TableWidget(mock_deferred_df)

    assert widget.is_deferred_mode is True

    import bigframes

    with bigframes.option_context(
        "display.render_mode", bigframes.options.display.render_mode
    ):
        widget.start_execution = True

    thread = getattr(widget, "_execution_thread", None)
    if thread is not None:
        thread.join(timeout=5)

    mock_deferred_df.execute.assert_called_once()
    mock_df_deferred.to_pandas_batches.assert_called_once()
    assert widget.is_deferred_mode is False


def test_deferred_mode_execution_updates_table_html(mock_deferred_df, mock_df_deferred):
    from bigframes.display.anywidget import TableWidget

    mock_deferred_df.execute.return_value = mock_df_deferred

    batches = mock.MagicMock()
    batch_df = pd.DataFrame({"A": [1], "B": ["a"], "C": [1.0], "D": [True]})
    batches.__iter__.return_value = iter([batch_df])
    batches.total_rows = 1
    mock_df_deferred.to_pandas_batches.return_value = batches

    with bigframes.option_context("display.render_mode", "anywidget"):
        widget = TableWidget(mock_deferred_df)
        widget.is_deferred_mode = True
        widget._deferred_dataframe = mock_deferred_df
        assert widget.table_html == ""

        widget.start_execution = True
        thread = getattr(widget, "_execution_thread", None)
        if thread is not None:
            thread.join(timeout=5)

        assert widget.is_deferred_mode is False
        assert widget.table_html != ""
        assert "table" in widget.table_html


def test_deferred_mode_execution_error(mock_deferred_df):
    from bigframes.display.anywidget import TableWidget

    mock_deferred_df.execute.side_effect = RuntimeError("Query Failed")

    with mock.patch.object(TableWidget, "_initial_load"):
        widget = TableWidget(mock_deferred_df)

        import bigframes

        with bigframes.option_context(
            "display.render_mode", bigframes.options.display.render_mode
        ):
            widget.start_execution = True

        thread = getattr(widget, "_execution_thread", None)
        if thread is not None:
            thread.join(timeout=5)

        assert widget.is_deferred_mode is True
        assert widget._error_message == "Query Failed"


def test_deferred_mode_execution_does_not_reset_page_on_navigation(
    mock_deferred_df, mock_df_deferred
):
    from bigframes.display.anywidget import TableWidget

    mock_deferred_df.execute.return_value = mock_df_deferred

    batches = mock.MagicMock()
    batch_df = pd.DataFrame({"A": [1], "B": ["a"], "C": [1.0], "D": [True]})
    batches.__iter__.return_value = iter([batch_df])
    batches.total_rows = 50
    mock_df_deferred.to_pandas_batches.return_value = batches

    with bigframes.option_context("display.render_mode", "anywidget"):
        widget = TableWidget(mock_deferred_df)
        widget.page_size = 10
        widget.start_execution = True

        thread = getattr(widget, "_execution_thread", None)
        if thread is not None:
            thread.join(timeout=5)

        assert widget.page == 0
        widget.page = 1
        assert widget.page == 1


def test_deferred_mode_execution_in_colab(mock_deferred_df, mock_df_deferred):
    import sys

    from bigframes.display.anywidget import TableWidget

    mock_deferred_df.execute.return_value = mock_df_deferred

    batches = mock.MagicMock()
    batch_df = pd.DataFrame({"A": [1], "B": ["a"], "C": [1.0], "D": [True]})
    batches.__iter__.return_value = iter([batch_df])
    batches.total_rows = 1
    mock_df_deferred.to_pandas_batches.return_value = batches

    with mock.patch.dict(sys.modules, {"google.colab": mock.MagicMock()}):
        with bigframes.option_context("display.render_mode", "anywidget"):
            widget = TableWidget(mock_deferred_df)
            widget.is_deferred_mode = True

            widget.start_execution = True

            thread = getattr(widget, "_execution_thread", None)
            if thread is not None:
                thread.join(timeout=5)

            assert widget.is_deferred_mode is True
            assert widget.table_html == ""

            # Simulate frontend ping callback
            widget.ping = 1

            assert widget.is_deferred_mode is False
            assert widget.table_html != ""
