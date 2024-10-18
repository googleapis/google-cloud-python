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

from __future__ import annotations

import bigframes.operations.aggregations as agg_ops
import bigframes.series as series

"""
Approximate functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions
"""


def approx_top_count(
    series: series.Series,
    number: int,
) -> series.Series:
    """Returns the approximate top elements of `expression` as an array of STRUCTs.
    The number parameter specifies the number of elements returned.

    Each `STRUCT` contains two fields. The first field (named `value`) contains an input
    value. The second field (named `count`) contains an `INT64` specifying the number
    of times the value was returned.

    Returns `NULL` if there are zero input rows.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None
        >>> s = bpd.Series(["apple", "apple", "pear", "pear", "pear", "banana"])
        >>> bbq.approx_top_count(s, number=2)
        [{'value': 'pear', 'count': 3}, {'value': 'apple', 'count': 2}]

    Args:
        series (bigframes.series.Series):
            The Series with any data type that the `GROUP BY` clause supports.
        number (int):
            An integer specifying the number of times the value was returned.

    Returns:
        bigframes.series.Series: A new Series with the result data.
    """
    if number < 1:
        raise ValueError("The number of approx_top_count must be at least 1")
    return series._apply_aggregation(agg_ops.ApproxTopCountOp(number=number))
