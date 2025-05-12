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

"""System tests for read_gbq_colab helper functions."""

import pandas
import pandas.testing


def test_read_gbq_colab_to_pandas_batches_preserves_order_by(maybe_ordered_session):
    df = maybe_ordered_session._read_gbq_colab(
        """
        SELECT
            name,
            SUM(number) AS total
        FROM
            `bigquery-public-data.usa_names.usa_1910_2013`
        WHERE state LIKE 'W%'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 300
        """
    )
    batches = df.to_pandas_batches(
        page_size=100,
    )

    total_rows = 0
    for batch in batches:
        assert batch["total"].is_monotonic_decreasing
        total_rows += len(batch.index)

    assert total_rows > 0


def test_read_gbq_colab_includes_formatted_scalars(session):
    pyformat_args = {
        "some_integer": 123,
        "some_string": "This could be dangerous, but we escape it",
        # This is not a supported type, but ignored if not referenced.
        "some_object": object(),
    }
    df = session._read_gbq_colab(
        """
        SELECT {some_integer} as some_integer,
        {some_string} as some_string,
        '{{escaped}}' as escaped
        """,
        pyformat_args=pyformat_args,
    )
    result = df.to_pandas()
    pandas.testing.assert_frame_equal(
        result,
        pandas.DataFrame(
            {
                "some_integer": pandas.Series([123], dtype=pandas.Int64Dtype()),
                "some_string": pandas.Series(
                    ["This could be dangerous, but we escape it"],
                    dtype="string[pyarrow]",
                ),
                "escaped": pandas.Series(["{escaped}"], dtype="string[pyarrow]"),
            }
        ),
    )
