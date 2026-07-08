# Copyright 2024 Google LLC
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

import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pyarrow as pa
import pytest

import bigframes as bf
import bigframes.display.html as bf_html


@pytest.mark.parametrize(
    ("data", "expected_alignments", "expected_strings"),
    [
        pytest.param(
            {
                "string_col": ["a", "b", "c"],
                "int_col": [1, 2, 3],
                "float_col": [1.1, 2.2, 3.3],
                "bool_col": [True, False, True],
            },
            {
                "string_col": "left",
                "int_col": "right",
                "float_col": "right",
                "bool_col": "left",
            },
            ["1.100000", "2.200000", "3.300000"],
            id="scalars",
        ),
        pytest.param(
            {
                "timestamp_col": pa.array(
                    [
                        datetime.datetime.fromisoformat(value)
                        for value in [
                            "2024-01-01 00:00:00",
                            "2024-01-01 00:00:01",
                            "2024-01-01 00:00:02",
                        ]
                    ],
                    pa.timestamp("us", tz="UTC"),
                ),
                "datetime_col": pa.array(
                    [
                        datetime.datetime.fromisoformat(value)
                        for value in [
                            "2027-06-05 04:03:02.001",
                            "2027-01-01 00:00:01",
                            "2027-01-01 00:00:02",
                        ]
                    ],
                    pa.timestamp("us"),
                ),
                "date_col": pa.array(
                    [
                        datetime.date(1999, 1, 1),
                        datetime.date(1999, 1, 2),
                        datetime.date(1999, 1, 3),
                    ],
                    pa.date32(),
                ),
                "time_col": pa.array(
                    [
                        datetime.time(11, 11, 0),
                        datetime.time(11, 11, 1),
                        datetime.time(11, 11, 2),
                    ],
                    pa.time64("us"),
                ),
            },
            {
                "timestamp_col": "left",
                "datetime_col": "left",
                "date_col": "left",
                "time_col": "left",
            },
            [
                "2024-01-01 00:00:00",
                "2027-06-05 04:03:02.001",
                "1999-01-01",
                "11:11:01",
            ],
            id="datetimes",
        ),
        pytest.param(
            {
                "array_col": pd.Series(
                    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                    dtype=pd.ArrowDtype(pa.list_(pa.int64())),
                ),
            },
            {
                "array_col": "left",
            },
            ["[1, 2, 3]", "[4, 5, 6]", "[7, 8, 9]"],
            id="array",
        ),
        pytest.param(
            {
                "struct_col": pd.Series(
                    [{"v": 1}, {"v": 2}, {"v": 3}],
                    dtype=pd.ArrowDtype(pa.struct([("v", pa.int64())])),
                ),
            },
            {
                "struct_col": "left",
            },
            ["{&#x27;v&#x27;: 1}", "{&#x27;v&#x27;: 2}", "{&#x27;v&#x27;: 3}"],
            id="struct",
        ),
    ],
)
def test_render_html_alignment_and_precision(
    data, expected_alignments, expected_strings
):
    df = pd.DataFrame(data)
    html = bf_html.render_html(dataframe=df, table_id="test-table")

    for align in expected_alignments.values():
        assert f'class="cell-align-{align}"' in html

    for expected_string in expected_strings:
        assert expected_string in html


def test_render_html_precision():
    data = {"float_col": [3.14159265]}
    df = pd.DataFrame(data)

    with bf.option_context("display.precision", 4):
        html = bf_html.render_html(dataframe=df, table_id="test-table")
        assert "3.1416" in html

    # Make sure we reset to default
    html = bf_html.render_html(dataframe=df, table_id="test-table")
    assert "3.141593" in html


def test_render_html_max_columns_truncation():
    # Create a DataFrame with 10 columns
    data = {f"col_{i}": [i] for i in range(10)}
    df = pd.DataFrame(data)

    # Test max_columns=4
    # max_columns=4 -> 2 left, 2 right. col_0, col_1 ... col_8, col_9
    html = bf_html.render_html(dataframe=df, table_id="test", max_columns=4)

    assert "col_0" in html
    assert "col_1" in html
    assert "col_2" not in html
    assert "col_7" not in html
    assert "col_8" in html
    assert "col_9" in html
    assert "..." in html

    # Test max_columns=3
    # 3 // 2 = 1. Left: col_0. Right: 3 - 1 = 2. col_8, col_9.
    # Total displayed: col_0, ..., col_8, col_9. (3 data cols + 1 ellipsis)
    html = bf_html.render_html(dataframe=df, table_id="test", max_columns=3)
    assert "col_0" in html
    assert "col_1" not in html
    assert "col_7" not in html
    assert "col_8" in html
    assert "col_9" in html

    # Test max_columns=1
    # 1 // 2 = 0. Left: []. Right: 1. col_9.
    # Total: ..., col_9.
    html = bf_html.render_html(dataframe=df, table_id="test", max_columns=1)
    assert "col_0" not in html
    assert "col_8" not in html
    assert "col_9" in html
    assert "..." in html


def test_repr_mimebundle_head():
    mock_df = Mock()
    mock_df.columns = ["col1"]

    mock_df._prepare_display_df.return_value = mock_df

    # Mock the call to retrieve_repr_request_results
    pandas_df = pd.DataFrame({"col1": [1, 2, 3]})
    mock_df._block.retrieve_repr_request_results.return_value = (
        pandas_df,
        3,
        Mock(),  # query_job
    )

    # Mock _get_obj_metadata
    with patch("bigframes.display.html._get_obj_metadata", return_value=(False, False)):
        # Mock create_html_representation and create_text_representation
        with patch(
            "bigframes.display.html.create_html_representation", return_value="<html>"
        ) as mock_create_html:
            with patch(
                "bigframes.display.plaintext.create_text_representation",
                return_value="text",
            ) as mock_create_text:
                bundle = bf_html.repr_mimebundle_head(mock_df)

                assert bundle == {"text/html": "<html>", "text/plain": "text"}
                mock_df._prepare_display_df.assert_called_once()
                mock_df._block.retrieve_repr_request_results.assert_called_once()
                mock_create_html.assert_called_once()
                mock_create_text.assert_called_once()
