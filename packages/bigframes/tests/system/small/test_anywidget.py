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

"""System tests for the anywidget-based table widget."""

from typing import Any
from unittest import mock

import pandas as pd
import pytest

import bigframes as bf
import bigframes.core.blocks
import bigframes.dataframe
import bigframes.display

pytest.importorskip("anywidget")

# Test constants to avoid change detector tests
EXPECTED_ROW_COUNT = 6
EXPECTED_PAGE_SIZE = 2
EXPECTED_TOTAL_PAGES = 3


@pytest.fixture(scope="module")
def paginated_pandas_df() -> pd.DataFrame:
    """Create a minimal test DataFrame with exactly 3 pages of 2 rows each."""
    test_data = pd.DataFrame(
        {
            "id": [5, 4, 3, 2, 1, 0],
            "page_indicator": [
                "page_3_row_2",
                "page_3_row_1",
                "page_2_row_2",
                "page_2_row_1",
                "page_1_row_2",
                "page_1_row_1",
            ],
            "value": [5, 4, 3, 2, 1, 0],
        }
    )
    return test_data


@pytest.fixture(scope="module")
def paginated_bf_df(
    session: bf.Session, paginated_pandas_df: pd.DataFrame
) -> bigframes.dataframe.DataFrame:
    return session.read_pandas(paginated_pandas_df)


@pytest.fixture
def table_widget(paginated_bf_df: bigframes.dataframe.DataFrame):
    """
    Helper fixture to create a TableWidget instance with a fixed page size.
    This reduces duplication across tests that use the same widget configuration.
    """

    from bigframes.display import TableWidget

    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        # Delay context manager cleanup of `max_rows` until after tests finish.
        yield TableWidget(paginated_bf_df)


@pytest.fixture(scope="module")
def small_pandas_df() -> pd.DataFrame:
    """Create a DataFrame smaller than the page size for edge case testing."""
    return pd.DataFrame(
        {
            "id": [0, 1],
            "page_indicator": ["small_row_1", "small_row_2"],
            "value": [0, 1],
        }
    )


@pytest.fixture(scope="module")
def small_bf_df(
    session: bf.Session, small_pandas_df: pd.DataFrame
) -> bf.dataframe.DataFrame:
    return session.read_pandas(small_pandas_df)


@pytest.fixture
def small_widget(small_bf_df):
    """Helper fixture for tests using a DataFrame smaller than the page size."""
    from bigframes.display import TableWidget

    with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 5):
        yield TableWidget(small_bf_df)


@pytest.fixture
def unknown_row_count_widget(session):
    """Fixture to create a TableWidget with an unknown row count."""
    from bigframes.core import blocks
    from bigframes.display import TableWidget

    # Create a small DataFrame with known content
    test_data = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4],
            "value": ["row_0", "row_1", "row_2", "row_3", "row_4"],
        }
    )
    bf_df = session.read_pandas(test_data)

    # Simulate a scenario where total_rows is not available from the iterator
    with mock.patch.object(bf_df, "_to_pandas_batches") as mock_batches:
        # We need to provide an iterator of DataFrames, not Series
        batches_iterator = iter([test_data])
        mock_batches.return_value = blocks.PandasBatches(
            batches_iterator, total_rows=None
        )
        with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 2):
            widget = TableWidget(bf_df)
            yield widget


@pytest.fixture(scope="module")
def empty_pandas_df() -> pd.DataFrame:
    """Create an empty DataFrame for edge case testing."""
    return pd.DataFrame(columns=["id", "page_indicator", "value"])


@pytest.fixture(scope="module")
def empty_bf_df(
    session: bf.Session, empty_pandas_df: pd.DataFrame
) -> bf.dataframe.DataFrame:
    return session.read_pandas(empty_pandas_df)


def mock_execute_result_with_params(
    self, schema, total_rows_val, arrow_batches_val, *args, **kwargs
):
    """
    Mocks an execution result with configurable total_rows and arrow_batches.
    """
    from bigframes.session.executor import (
        ExecuteResult,
        ExecutionMetadata,
        ResultsIterator,
    )

    class MockExecuteResult(ExecuteResult):
        @property
        def execution_metadata(self) -> ExecutionMetadata:
            return ExecutionMetadata()

        @property
        def schema(self) -> Any:
            return schema

        def batches(self) -> ResultsIterator:
            return ResultsIterator(
                arrow_batches_val,
                self.schema,
                total_rows_val,
                None,
            )

    return MockExecuteResult()


def _assert_html_matches_pandas_slice(
    table_html: str,
    expected_pd_slice: pd.DataFrame,
    full_pd_df: pd.DataFrame,
):
    """
    Assertion helper to verify that the rendered HTML contains exactly the
    rows from the expected pandas DataFrame slice and no others. This is
    inspired by the pattern of comparing BigFrames output to pandas output.
    """
    # Check that the unique indicator from each expected row is present.
    for _, row in expected_pd_slice.iterrows():
        assert row["page_indicator"] in table_html

    # Create a DataFrame of all rows that should NOT be present.
    unexpected_pd_df = full_pd_df.drop(expected_pd_slice.index)

    # Check that no unique indicators from unexpected rows are present.
    for _, row in unexpected_pd_df.iterrows():
        assert row["page_indicator"] not in table_html


def test_widget_initialization_should_calculate_total_row_count(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """A TableWidget should correctly calculate the total row count on creation."""
    from bigframes.display import TableWidget

    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(paginated_bf_df)

    assert widget.row_count == EXPECTED_ROW_COUNT


def test_widget_initialization_should_default_to_page_zero(
    table_widget,
):
    """
    Given a new TableWidget, when it is initialized,
    then its page number should default to 0.
    """
    # The `table_widget` fixture already creates the widget.
    # Assert its state.
    assert table_widget.page == 0
    assert table_widget.page_size == EXPECTED_PAGE_SIZE


def test_widget_display_should_show_first_page_on_load(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget, when it is first loaded, then it should display
    the first page of data.
    """
    expected_slice = paginated_pandas_df.iloc[0:2]

    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


@pytest.mark.parametrize(
    "page_number, start_row, end_row",
    [
        (1, 2, 4),  # Second page
        (2, 4, 6),  # Last page
    ],
    ids=["second_page", "last_page"],
)
def test_widget_navigation_should_display_correct_page(
    table_widget,
    paginated_pandas_df: pd.DataFrame,
    page_number: int,
    start_row: int,
    end_row: int,
):
    """
    Given a widget, when the page is set, then it should display the correct
    slice of data.
    """
    expected_slice = paginated_pandas_df.iloc[start_row:end_row]

    table_widget.page = page_number
    html = table_widget.table_html

    assert table_widget.page == page_number
    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_setting_negative_page_should_raise_error(
    table_widget,
):
    """
    Given a widget, when a negative page number is set,
    then a ValueError should be raised.
    """
    with pytest.raises(ValueError, match="Page number cannot be negative."):
        table_widget.page = -1


def test_setting_page_beyond_max_should_clamp_to_last_page(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget,
    when a page number greater than the max is set,
    then the page number should be clamped to the last valid page.
    """
    expected_slice = paginated_pandas_df.iloc[4:6]  # Last page data

    table_widget.page = 100  # Set page far beyond the total of 3 pages
    html = table_widget.table_html

    assert table_widget.page == 2  # Page is clamped to the last valid page (0-indexed)
    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


@pytest.mark.parametrize(
    "page, start_row, end_row",
    [
        (0, 0, 3),  # Page 0: rows 0-2
        (1, 3, 6),  # Page 1: rows 3-5
    ],
    ids=[
        "Page 0 (Rows 0-2)",
        "Page 1 (Rows 3-5)",
    ],
)
def test_widget_pagination_should_work_with_custom_page_size(
    paginated_bf_df: bf.dataframe.DataFrame,
    paginated_pandas_df: pd.DataFrame,
    page: int,
    start_row: int,
    end_row: int,
):
    """
    A widget should paginate correctly with a custom page size of 3.
    """
    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 3
    ):
        from bigframes.display import TableWidget

        widget = TableWidget(paginated_bf_df)
        assert widget.page_size == 3

        expected_slice = paginated_pandas_df.iloc[start_row:end_row]

        widget.page = page
        html = widget.table_html

        assert widget.page == page
        _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_widget_with_few_rows_should_display_all_rows(small_widget, small_pandas_df):
    """
    Given a DataFrame smaller than the page size, the widget should
    display all rows on the first page.
    """
    html = small_widget.table_html

    _assert_html_matches_pandas_slice(html, small_pandas_df, small_pandas_df)


def test_navigation_beyond_last_page_should_be_clamped(small_widget):
    """
    Given a DataFrame smaller than the page size,
    when navigating beyond the last page,
    then the page should be clamped to the last valid page (page 0).
    """
    # For a DataFrame with 2 rows and page_size 5 (from small_widget fixture),
    # the frontend should calculate 1 total page.
    assert small_widget.row_count == 2

    # The widget should always be on page 0 for a single-page dataset.
    assert small_widget.page == 0

    # Attempting to navigate to page 1 should be clamped back to page 0,
    # confirming that only one page is recognized by the backend.
    small_widget.page = 1
    assert small_widget.page == 0


def test_global_options_change_should_not_affect_existing_widget_page_size(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Given an existing widget,
    when global display options are changed,
    then the widget's page size should remain unchanged.
    """
    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        from bigframes.display import TableWidget

        widget = TableWidget(paginated_bf_df)
        initial_page_size = widget.page_size
        assert initial_page_size == 2
        widget.page = 1  # a non-default state
        assert widget.page == 1

    bf.options.display.max_rows = 10  # Change global setting

    assert widget.page_size == initial_page_size  # Should remain unchanged
    assert widget.page == 1  # Page should not be reset


def test_widget_with_empty_dataframe_should_have_zero_row_count(
    empty_bf_df: bf.dataframe.DataFrame,
):
    """
    Given an empty DataFrame,
    when a widget is created from it,
    then its row_count should be 0.
    """

    with bigframes.option_context("display.repr_mode", "anywidget"):
        from bigframes.display import TableWidget

        widget = TableWidget(empty_bf_df)

    assert widget.row_count == 0


def test_widget_with_empty_dataframe_should_render_table_headers(
    empty_bf_df: bf.dataframe.DataFrame,
):

    """


    Given an empty DataFrame,


    when a widget is created from it,


    then its HTML representation should still render the table headers.


    """

    with bigframes.option_context("display.repr_mode", "anywidget"):

        from bigframes.display import TableWidget

        widget = TableWidget(empty_bf_df)

        html = widget.table_html

        assert "<table" in html

        assert "id" in html  # Check for a column header


def test_page_size_change_should_reset_current_page_to_zero(table_widget):
    """
    Given a widget on a non-default page, When the page_size is changed,
    Then the current page attribute should reset to 0.
    """
    # Start on page 1 with an initial page size of 2.
    table_widget.page = 1
    assert table_widget.page == 1

    # Change the page size.
    table_widget.page_size = 3

    # The page number is reset to 0.
    assert table_widget.page == 0


def test_page_size_change_should_render_html_with_new_size(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget, when the page_size is changed,
    the rendered HTML should immediately reflect the new page size.
    """
    # The widget is in its initial state with page_size=2.
    # We expect the first 3 rows after the change.
    expected_slice = paginated_pandas_df.iloc[0:3]

    # Change the page size.
    table_widget.page_size = 3

    # The HTML now contains the first 3 rows.
    html = table_widget.table_html
    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_navigation_after_page_size_change_should_use_new_size(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget whose page size has been changed, When we navigate to the
    next page, Then the pagination should use the new page size.
    """
    # Change the page size to 3.
    table_widget.page_size = 3
    # We expect the second page to contain rows 4-6 (indices 3-6).
    expected_slice = paginated_pandas_df.iloc[3:6]

    # Navigate to the next page.
    table_widget.page = 1

    # The second page's HTML correctly reflects the new page size.
    html = table_widget.table_html
    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


@pytest.mark.parametrize("invalid_size", [0, -5], ids=["zero", "negative"])
def test_setting_invalid_page_size_should_be_ignored(table_widget, invalid_size: int):
    """
    When the page size is set to an invalid number (<=0), the change should
    be ignored.
    """
    # Set the initial page to 2.
    initial_size = table_widget.page_size
    assert initial_size == 2

    # Attempt to set the page size to a invlaid size.
    table_widget.page_size = invalid_size

    # The page size remains unchanged.
    assert table_widget.page_size == initial_size


def test_setting_page_size_above_max_should_be_clamped(table_widget):
    """
    Given a widget, when the page size is set to a value greater than the
    allowed maximum, the page size should be clamped to the maximum value.
    """
    # The maximum is hardcoded to 1000 in the implementation.
    expected_clamped_size = 1000

    # Attempt to set a very large page size.
    table_widget.page_size = 9001

    # The page size is clamped to the maximum.
    assert table_widget.page_size == expected_clamped_size


def test_widget_creation_should_load_css_for_rendering(table_widget):
    """
    Given a TableWidget is created, when its resources are accessed,
    it should contain the CSS content required for styling.
    """
    # The table_widget fixture creates the widget.
    # No additional setup is needed.

    # Access the CSS content.
    css_content = table_widget._css

    # The content is a non-empty string containing a known selector.
    assert isinstance(css_content, str)
    assert len(css_content) > 0
    assert ".bigframes-widget .footer" in css_content


def test_widget_row_count_should_be_immutable_after_creation(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Given a widget created with a specific configuration when global display
    options are changed later, the widget's original row_count should remain
    unchanged.
    """
    from bigframes.display import TableWidget

    # Use a context manager to ensure the option is reset
    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(paginated_bf_df)
        initial_row_count = widget.row_count

    # Change a global option that could influence row count
    bf.options.display.max_rows = 10

    # Verify the row count remains immutable.
    assert widget.row_count == initial_row_count


class FaultyIterator:
    def __iter__(self):
        return self

    def __next__(self):
        raise ValueError("Simulated read error")


def test_widget_should_show_error_on_batch_failure(
    paginated_bf_df: bf.dataframe.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
):
    """
    Given that the internal call to `_to_pandas_batches` fails and returns None,
    when the TableWidget is created, its `error_message` should be set and displayed.
    """
    # Patch the DataFrame's batch creation method to simulate a failure.
    monkeypatch.setattr(
        "bigframes.dataframe.DataFrame._to_pandas_batches",
        lambda self, *args, **kwargs: None,
    )

    # Create the TableWidget under the error condition.
    with bigframes.option_context("display.repr_mode", "anywidget"):
        from bigframes.display import TableWidget

        # The widget should handle the faulty data from the mock without crashing.
        widget = TableWidget(paginated_bf_df)

    # The widget should have an error message and display it in the HTML.
    assert widget.row_count is None
    assert widget._error_message is not None
    assert "Could not retrieve data batches" in widget._error_message
    assert widget._error_message in widget.table_html


def test_widget_row_count_reflects_actual_data_available(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Test that widget row_count reflects the actual data available,
    regardless of theoretical limits.
    """
    from bigframes.display import TableWidget

    # Set up display options that define a page size.
    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(paginated_bf_df)

    # The widget should report the total rows in the DataFrame,
    # not limited by page_size (which only affects pagination)
    assert widget.row_count == EXPECTED_ROW_COUNT
    assert widget.page_size == 2  # Respects the display option


def test_widget_with_unknown_row_count_should_auto_navigate_to_last_page(
    session: bf.Session,
):
    """
    Given a widget with unknown row count (row_count=None), when a user
    navigates beyond the available data and all data is loaded, then the
    widget should automatically navigate back to the last valid page.
    """
    from bigframes.display import TableWidget

    # Create a small DataFrame with known content
    test_data = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4],
            "value": ["row_0", "row_1", "row_2", "row_3", "row_4"],
        }
    )
    bf_df = session.read_pandas(test_data)

    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(bf_df)

        # Manually set row_count to None to simulate unknown total
        widget.row_count = None

        # Navigate to a page beyond available data (page 10)
        # With page_size=2 and 5 rows, valid pages are 0, 1, 2
        widget.page = 10

        # Force data loading by accessing table_html
        _ = widget.table_html

        # After all data is loaded, widget should auto-navigate to last valid page
        # Last valid page = ceil(5 / 2) - 1 = 2
        assert widget.page == 2

        # Verify the displayed content is the last page
        html = widget.table_html
        assert "row_4" in html  # Last row should be visible
        assert "row_0" not in html  # First row should not be visible


def test_widget_with_unknown_row_count_should_set_none_state_for_frontend(
    session: bf.Session,
):
    """
    Given a widget with unknown row count, its `row_count` traitlet should be
    `None`, which signals the frontend to display 'Page X of many'.
    """
    from bigframes.display import TableWidget

    test_data = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "value": ["a", "b", "c"],
        }
    )
    bf_df = session.read_pandas(test_data)

    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(bf_df)

        # Set row_count to None
        widget.row_count = None

        # Verify row_count is None (not 0)
        assert widget.row_count is None

        # The widget should still function normally
        assert widget.page == 0
        assert widget.page_size == 2

        # Force data loading by accessing table_html. This also ensures that
        # rendering does not raise an exception.
        _ = widget.table_html


def test_widget_with_unknown_row_count_should_allow_forward_navigation(
    session: bf.Session,
):
    """
    Given a widget with unknown row count, users should be able to navigate
    forward until they reach the end of available data.
    """
    from bigframes.display import TableWidget

    test_data = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4, 5],
            "value": ["p0_r0", "p0_r1", "p1_r0", "p1_r1", "p2_r0", "p2_r1"],
        }
    )
    bf_df = session.read_pandas(test_data)

    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        widget = TableWidget(bf_df)
        widget.row_count = None

        # Navigate to page 1
        widget.page = 1
        html = widget.table_html
        assert "p1_r0" in html
        assert "p1_r1" in html

        # Navigate to page 2
        widget.page = 2
        html = widget.table_html
        assert "p2_r0" in html
        assert "p2_r1" in html

        # Navigate beyond available data (page 5)
        widget.page = 5
        _ = widget.table_html

        # Should auto-navigate back to last valid page (page 2)
        assert widget.page == 2


def test_widget_with_unknown_row_count_empty_dataframe(
    session: bf.Session,
):
    """
    Given an empty DataFrame with unknown row count, the widget should
    stay on page 0 and display empty content.
    """
    from bigframes.display import TableWidget

    empty_data = pd.DataFrame(columns=["id", "value"])
    bf_df = session.read_pandas(empty_data)

    with bigframes.option_context("display.repr_mode", "anywidget"):
        widget = TableWidget(bf_df)
        widget.row_count = None

        # Attempt to navigate to page 5
        widget.page = 5
        _ = widget.table_html

        # Should stay on page 0 for empty DataFrame
        assert widget.page == 0


def test_widget_sort_should_sort_ascending_on_first_click(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget, when a column header is clicked for the first time,
    then the data should be sorted by that column in ascending order.
    """
    table_widget.sort_column = "id"
    table_widget.sort_ascending = True

    expected_slice = paginated_pandas_df.sort_values("id", ascending=True).iloc[0:2]
    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_widget_sort_should_sort_descending_on_second_click(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget sorted by a column, when the same column header is clicked again,
    then the data should be sorted by that column in descending order.
    """
    table_widget.sort_column = "id"
    table_widget.sort_ascending = True

    # Second click
    table_widget.sort_ascending = False

    expected_slice = paginated_pandas_df.sort_values("id", ascending=False).iloc[0:2]
    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_widget_sort_should_switch_column_and_sort_ascending(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a widget sorted by a column, when a different column header is clicked,
    then the data should be sorted by the new column in ascending order.
    """
    table_widget.sort_column = "id"
    table_widget.sort_ascending = True

    # Click on a different column
    table_widget.sort_column = "value"
    table_widget.sort_ascending = True

    expected_slice = paginated_pandas_df.sort_values("value", ascending=True).iloc[0:2]
    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_widget_sort_should_be_maintained_after_pagination(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a sorted widget, when the user navigates to the next page,
    then the sorting should be maintained.
    """
    table_widget.sort_column = "id"
    table_widget.sort_ascending = True

    # Go to the second page
    table_widget.page = 1

    expected_slice = paginated_pandas_df.sort_values("id", ascending=True).iloc[2:4]
    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


def test_widget_sort_should_reset_on_page_size_change(
    table_widget, paginated_pandas_df: pd.DataFrame
):
    """
    Given a sorted widget, when the page size is changed,
    then the sorting should be reset.
    """
    table_widget.sort_column = "id"
    table_widget.sort_ascending = True

    table_widget.page_size = 3

    # Sorting is not reset in the backend, but the view should be of the unsorted df
    expected_slice = paginated_pandas_df.iloc[0:3]
    html = table_widget.table_html

    _assert_html_matches_pandas_slice(html, expected_slice, paginated_pandas_df)


@pytest.fixture(scope="module")
def integer_column_df(session):
    """Create a DataFrame with integer column labels."""
    pandas_df = pd.DataFrame([[0, 1], [2, 3]], columns=pd.Index([1, 2]))
    return session.read_pandas(pandas_df)


@pytest.fixture(scope="module")
def multiindex_column_df(session):
    """Create a DataFrame with MultiIndex column labels."""
    pandas_df = pd.DataFrame(
        {
            "foo": ["one", "one", "one", "two", "two", "two"],
            "bar": ["A", "B", "C", "A", "B", "C"],
            "baz": [1, 2, 3, 4, 5, 6],
            "zoo": ["x", "y", "z", "q", "w", "t"],
        }
    )
    df = session.read_pandas(pandas_df)
    # The session is attached to `df` through the constructor.
    # We can pass it to the pivoted DataFrame.
    pdf = df.pivot(index="foo", columns="bar", values=["baz", "zoo"])
    return pdf


def test_table_widget_integer_columns_disables_sorting(integer_column_df):
    """
    Given a DataFrame with integer column labels, the widget should
    disable sorting.
    """
    from bigframes.display import TableWidget

    widget = TableWidget(integer_column_df)
    assert widget.orderable_columns == []


def test_table_widget_multiindex_columns_disables_sorting(multiindex_column_df):
    """
    Given a DataFrame with a MultiIndex for columns, the widget should
    disable sorting.
    """
    from bigframes.display import TableWidget

    widget = TableWidget(multiindex_column_df)
    assert widget.orderable_columns == []


def test_repr_mimebundle_should_fallback_to_html_if_anywidget_is_unavailable(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Test that _repr_mimebundle_ falls back to static html when anywidget is not available.
    """
    with bigframes.option_context(
        "display.repr_mode", "anywidget", "display.max_rows", 2
    ):
        # Mock the ANYWIDGET_INSTALLED flag to simulate absence of anywidget
        with mock.patch("bigframes.display.anywidget.ANYWIDGET_INSTALLED", False):
            bundle = paginated_bf_df._repr_mimebundle_()
            assert "application/vnd.jupyter.widget-view+json" not in bundle
            assert "text/html" in bundle
            html = bundle["text/html"]
            assert "page_3_row_2" in html
            assert "page_3_row_1" in html
            assert "page_1_row_1" not in html


def test_repr_mimebundle_should_return_widget_view_if_anywidget_is_available(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Test that _repr_mimebundle_ returns a widget view when anywidget is available.
    """
    with bigframes.option_context("display.repr_mode", "anywidget"):
        bundle = paginated_bf_df._repr_mimebundle_()
        assert isinstance(bundle, tuple)
        data, metadata = bundle
        assert "application/vnd.jupyter.widget-view+json" in data
        assert "text/html" in data
        assert "text/plain" in data


def test_repr_in_anywidget_mode_should_not_be_deferred(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Test that repr(df) is not deferred in anywidget mode.
    This is to ensure that print(df) works as expected.
    """
    with bigframes.option_context("display.repr_mode", "anywidget"):
        representation = repr(paginated_bf_df)
        assert "Computation deferred" not in representation
        assert "page_1_row_1" in representation


def test_dataframe_repr_mimebundle_anywidget_with_metadata(
    monkeypatch: pytest.MonkeyPatch,
    session: bigframes.Session,  # Add session as a fixture
):
    with bigframes.option_context("display.repr_mode", "anywidget"):
        # Create a real DataFrame object (or a mock that behaves like one minimally)
        # for _repr_mimebundle_ to operate on.
        test_df = bigframes.dataframe.DataFrame(
            pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}), session=session
        )

        mock_get_anywidget_bundle_return_value: tuple[
            dict[str, Any], dict[str, Any]
        ] = (
            {
                "application/vnd.jupyter.widget-view+json": {"model_id": "123"},
                "text/html": "<div>My Table HTML</div>",
                "text/plain": "My Table Plain Text",
            },
            {
                "application/vnd.jupyter.widget-view+json": {
                    "colab": {"custom_widget_manager": {}}
                }
            },
        )

        # Patch the class method directly
        with mock.patch(
            "bigframes.dataframe.DataFrame._get_anywidget_bundle",
            return_value=mock_get_anywidget_bundle_return_value,
        ):
            result = test_df._repr_mimebundle_()

        assert isinstance(result, tuple)
        data, metadata = result
        assert "application/vnd.jupyter.widget-view+json" in data
        assert "text/html" in data
        assert "text/plain" in data
        assert "application/vnd.jupyter.widget-view+json" in metadata
        assert "colab" in metadata["application/vnd.jupyter.widget-view+json"]


@pytest.fixture(scope="module")
def custom_index_pandas_df() -> pd.DataFrame:
    """Create a DataFrame with a custom named index for testing."""
    test_data = pd.DataFrame(
        {
            "value_a": [10, 20, 30, 40, 50, 60],
            "value_b": ["a", "b", "c", "d", "e", "f"],
        }
    )
    test_data.index = pd.Index(
        ["row_1", "row_2", "row_3", "row_4", "row_5", "row_6"], name="custom_idx"
    )
    return test_data


@pytest.fixture(scope="module")
def custom_index_bf_df(
    session: bf.Session, custom_index_pandas_df: pd.DataFrame
) -> bf.dataframe.DataFrame:
    return session.read_pandas(custom_index_pandas_df)


@pytest.fixture(scope="module")
def multiindex_pandas_df() -> pd.DataFrame:
    """Create a DataFrame with MultiIndex for testing."""
    test_data = pd.DataFrame(
        {
            "value": [100, 200, 300, 400, 500, 600],
            "category": ["X", "Y", "Z", "X", "Y", "Z"],
        }
    )
    test_data.index = pd.MultiIndex.from_arrays(
        [
            ["group_A", "group_A", "group_A", "group_B", "group_B", "group_B"],
            [1, 2, 3, 1, 2, 3],
        ],
        names=["group", "item"],
    )
    return test_data


@pytest.fixture(scope="module")
def multiindex_bf_df(
    session: bf.Session, multiindex_pandas_df: pd.DataFrame
) -> bf.dataframe.DataFrame:
    return session.read_pandas(multiindex_pandas_df)


def test_widget_with_default_index_should_display_index_column_with_empty_header(
    paginated_bf_df: bf.dataframe.DataFrame,
):
    """
    Given a DataFrame with a default index, when the TableWidget is rendered,
    then an index column should be visible with an empty header.
    """
    import re

    from bigframes.display.anywidget import TableWidget

    with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 2):
        widget = TableWidget(paginated_bf_df)
        html = widget.table_html

    # The header for the index should be present but empty, matching the
    # internal rendering logic.
    thead = html.split("<thead>")[1].split("</thead>")[0]
    # Find the first header cell and check that its content div is empty.
    match = re.search(r"<th[^>]*><div[^>]*>([^<]*)</div></th>", thead)
    assert match is not None, "Could not find table header cell in output."
    assert (
        match.group(1) == ""
    ), f"Expected empty index header, but found: {match.group(1)}"


def test_widget_with_custom_index_should_display_index_column(
    custom_index_bf_df: bf.dataframe.DataFrame,
):
    """
    Given a DataFrame with a custom named index, when rendered,
    then the index column and first page of rows should be visible.
    """
    from bigframes.display.anywidget import TableWidget

    with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 2):
        widget = TableWidget(custom_index_bf_df)
        html = widget.table_html

    assert "custom_idx" in html
    assert "row_1" in html
    assert "row_2" in html
    assert "row_3" not in html  # Verify pagination is working
    assert "row_4" not in html


def test_widget_with_custom_index_pagination_preserves_index(
    custom_index_bf_df: bf.dataframe.DataFrame,
):
    """
    Given a DataFrame with a custom index, when navigating to the second page,
    then the second page's index values should be visible.
    """
    from bigframes.display.anywidget import TableWidget

    with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 2):
        widget = TableWidget(custom_index_bf_df)

        widget.page = 1  # Navigate to page 2
        html = widget.table_html

    assert "row_3" in html
    assert "row_4" in html
    assert "row_1" not in html  # Verify page 1 content is gone
    assert "row_2" not in html


def test_widget_with_custom_index_matches_pandas_output(
    custom_index_bf_df: bf.dataframe.DataFrame,
):
    """
    Given a DataFrame with a custom index and max_rows=3, the widget's HTML
    output should contain the first three index values.
    """
    from bigframes.display.anywidget import TableWidget

    with bf.option_context("display.repr_mode", "anywidget", "display.max_rows", 3):
        widget = TableWidget(custom_index_bf_df)
        html = widget.table_html

    assert "row_1" in html
    assert "row_2" in html
    assert "row_3" in html
    assert "row_4" not in html  # Verify it respects max_rows


# TODO(b/438181139): Add tests for custom multiindex
# This may not be necessary for the SQL Cell use case but should be
# considered for completeness.
