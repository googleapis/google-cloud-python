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


"""
JSON functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions
"""


from __future__ import annotations

from typing import Any, Sequence, Tuple

import bigframes.operations as ops
import bigframes.series as series


def json_set(
    series: series.Series,
    json_path_value_pairs: Sequence[Tuple[str, Any]],
) -> series.Series:
    """Produces a new JSON value within a Series by inserting or replacing values at
    specified paths.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.read_gbq("SELECT JSON '{\\\"a\\\": 1}' AS data")["data"]
        >>> bbq.json_set(s, json_path_value_pairs=[("$.a", 100), ("$.b", "hi")])
            0    {"a":100,"b":"hi"}
            Name: data, dtype: string

    Args:
        series (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path_value_pairs (Sequence[Tuple[str, Any]]):
            Pairs of JSON path and the new value to insert/replace.

    Returns:
        bigframes.series.Series: A new Series with the transformed JSON data.

    """
    # SQLGlot parser does not support the "create_if_missing => true" syntax, so
    # create_if_missing is not currently implemented.

    for json_path_value_pair in json_path_value_pairs:
        if len(json_path_value_pair) != 2:
            raise ValueError(
                "Incorrect format: Expected (<json_path>, <json_value>), but found: "
                + f"{json_path_value_pair}"
            )

        json_path, json_value = json_path_value_pair
        series = series._apply_binary_op(
            json_value, ops.JSONSet(json_path=json_path), alignment="left"
        )
    return series


def json_extract(
    series: series.Series,
    json_path: str,
) -> series.Series:
    """Extracts a JSON value and converts it to a SQL JSON-formatted `STRING` or `JSON`
    value. This function uses single quotes and brackets to escape invalid JSONPath
    characters in JSON keys.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['{"class": {"students": [{"id": 5}, {"id": 12}]}}'])
        >>> bbq.json_extract(s, json_path="$.class")
        0    {"students":[{"id":5},{"id":12}]}
        dtype: string

    Args:
        series (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the JSON or JSON-formatted STRING.
    """
    return series._apply_unary_op(ops.JSONExtract(json_path=json_path))


def json_extract_array(
    series: series.Series,
    json_path: str = "$",
) -> series.Series:
    """Extracts a JSON array and converts it to a SQL array of JSON-formatted `STRING` or `JSON`
    values. This function uses single quotes and brackets to escape invalid JSONPath
    characters in JSON keys.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['[1, 2, 3]', '[4, 5]'])
        >>> bbq.json_extract_array(s)
        0    ['1' '2' '3']
        1        ['4' '5']
        dtype: list<item: string>[pyarrow]

    Args:
        series (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the JSON or JSON-formatted STRING.
    """
    return series._apply_unary_op(ops.JSONExtractArray(json_path=json_path))
