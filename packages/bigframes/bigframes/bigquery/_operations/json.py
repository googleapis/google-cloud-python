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

from typing import Any, cast, Optional, Sequence, Tuple, Union
import warnings

import bigframes.core.utils as utils
import bigframes.dtypes
import bigframes.exceptions as bfe
import bigframes.operations as ops
import bigframes.series as series

from . import array


@utils.preview(name="The JSON-related API `json_set`")
def json_set(
    input: series.Series,
    json_path_value_pairs: Sequence[Tuple[str, Any]],
) -> series.Series:
    """Produces a new JSON value within a Series by inserting or replacing values at
    specified paths.

    .. warning::
        The JSON-related API `parse_json` is in preview. Its behavior may change in
        future versions.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.read_gbq("SELECT JSON '{\\\"a\\\": 1}' AS data")["data"]
        >>> bbq.json_set(s, json_path_value_pairs=[("$.a", 100), ("$.b", "hi")])
            0    {"a":100,"b":"hi"}
            Name: data, dtype: extension<dbjson<JSONArrowType>>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path_value_pairs (Sequence[Tuple[str, Any]]):
            Pairs of JSON path and the new value to insert/replace.

    Returns:
        bigframes.series.Series: A new Series with the transformed JSON data.

    """
    # SQLGlot parser does not support the "create_if_missing => true" syntax, so
    # create_if_missing is not currently implemented.

    result = input
    for json_path_value_pair in json_path_value_pairs:
        if len(json_path_value_pair) != 2:
            raise ValueError(
                "Incorrect format: Expected (<json_path>, <json_value>), but found: "
                + f"{json_path_value_pair}"
            )

        json_path, json_value = json_path_value_pair
        result = result._apply_binary_op(
            json_value, ops.JSONSet(json_path=json_path), alignment="left"
        )
    return result


def json_extract(
    input: series.Series,
    json_path: str,
) -> series.Series:
    """Extracts a JSON value and converts it to a SQL JSON-formatted ``STRING`` or
    ``JSON`` value. This function uses single quotes and brackets to escape invalid
    JSONPath characters in JSON keys.

    .. deprecated:: 2.5.0
        The ``json_extract`` is deprecated and will be removed in a future version.
        Use ``json_query`` instead.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['{"class": {"students": [{"id": 5}, {"id": 12}]}}'])
        >>> bbq.json_extract(s, json_path="$.class")
        0    {"students":[{"id":5},{"id":12}]}
        dtype: string

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the JSON or JSON-formatted STRING.
    """
    msg = (
        "The `json_extract` is deprecated and will be removed in a future version. "
        "Use `json_query` instead."
    )
    warnings.warn(bfe.format_message(msg), category=UserWarning)
    return input._apply_unary_op(ops.JSONExtract(json_path=json_path))


def json_extract_array(
    input: series.Series,
    json_path: str = "$",
) -> series.Series:
    """Extracts a JSON array and converts it to a SQL array of JSON-formatted
    `STRING` or `JSON` values. This function uses single quotes and brackets to
    escape invalid JSONPath characters in JSON keys.

    .. deprecated:: 2.5.0
        The ``json_extract_array`` is deprecated and will be removed in a future version.
        Use ``json_query_array`` instead.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['[1, 2, 3]', '[4, 5]'])
        >>> bbq.json_extract_array(s)
        0    ['1' '2' '3']
        1        ['4' '5']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": [{"name": "apple"}, {"name": "cherry"}]}',
        ...   '{"fruits": [{"name": "guava"}, {"name": "grapes"}]}'
        ... ])
        >>> bbq.json_extract_array(s, "$.fruits")
        0    ['{"name":"apple"}' '{"name":"cherry"}']
        1    ['{"name":"guava"}' '{"name":"grapes"}']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": {"color": "red",   "names": ["apple","cherry"]}}',
        ...   '{"fruits": {"color": "green", "names": ["guava", "grapes"]}}'
        ... ])
        >>> bbq.json_extract_array(s, "$.fruits.names")
        0    ['"apple"' '"cherry"']
        1    ['"guava"' '"grapes"']
        dtype: list<item: string>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the parsed arrays from the input.
    """
    msg = (
        "The `json_extract_array` is deprecated and will be removed in a future version. "
        "Use `json_query_array` instead."
    )
    warnings.warn(bfe.format_message(msg), category=UserWarning)
    return input._apply_unary_op(ops.JSONExtractArray(json_path=json_path))


def json_extract_string_array(
    input: series.Series,
    json_path: str = "$",
    value_dtype: Optional[
        Union[bigframes.dtypes.Dtype, bigframes.dtypes.DtypeString]
    ] = None,
) -> series.Series:
    """Extracts a JSON array and converts it to a SQL array of `STRING` values.
    A `value_dtype` can be provided to further coerce the data type of the
    values in the array. This function uses single quotes and brackets to escape
    invalid JSONPath characters in JSON keys.

    .. deprecated:: 2.6.0
        The ``json_extract_string_array`` is deprecated and will be removed in a future version.
        Use ``json_value_array`` instead.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['[1, 2, 3]', '[4, 5]'])
        >>> bbq.json_extract_string_array(s)
        0    ['1' '2' '3']
        1        ['4' '5']
        dtype: list<item: string>[pyarrow]

        >>> bbq.json_extract_string_array(s, value_dtype='Int64')
        0    [1 2 3]
        1      [4 5]
        dtype: list<item: int64>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": {"color": "red",   "names": ["apple","cherry"]}}',
        ...   '{"fruits": {"color": "green", "names": ["guava", "grapes"]}}'
        ... ])
        >>> bbq.json_extract_string_array(s, "$.fruits.names")
        0    ['apple' 'cherry']
        1    ['guava' 'grapes']
        dtype: list<item: string>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.
        value_dtype (dtype, Optional):
            The data type supported by BigFrames DataFrame.

    Returns:
        bigframes.series.Series: A new Series with the parsed arrays from the input.
    """
    msg = (
        "The `json_extract_string_array` is deprecated and will be removed in a future version. "
        "Use `json_value_array` instead."
    )
    warnings.warn(bfe.format_message(msg), category=UserWarning)
    array_series = input._apply_unary_op(
        ops.JSONExtractStringArray(json_path=json_path)
    )
    if value_dtype not in [None, bigframes.dtypes.STRING_DTYPE]:
        array_items_series = array_series.explode()
        if value_dtype == bigframes.dtypes.BOOL_DTYPE:
            array_items_series = array_items_series.str.lower() == "true"
        else:
            array_items_series = array_items_series.astype(value_dtype)
        array_series = cast(
            series.Series,
            array.array_agg(
                array_items_series.groupby(level=input.index.names, dropna=False)
            ),
        )
    return array_series


def json_query(
    input: series.Series,
    json_path: str,
) -> series.Series:
    """Extracts a JSON value and converts it to a SQL JSON-formatted ``STRING``
    or ``JSON`` value. This function uses double quotes to escape invalid JSONPath
    characters in JSON keys. For example: ``"a.b"``.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['{"class": {"students": [{"id": 5}, {"id": 12}]}}'])
        >>> bbq.json_query(s, json_path="$.class")
        0    {"students":[{"id":5},{"id":12}]}
        dtype: string

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the JSON or JSON-formatted STRING.
    """
    return input._apply_unary_op(ops.JSONQuery(json_path=json_path))


def json_query_array(
    input: series.Series,
    json_path: str = "$",
) -> series.Series:
    """Extracts a JSON array and converts it to a SQL array of JSON-formatted
    `STRING` or `JSON` values. This function uses double quotes to escape invalid
    JSONPath characters in JSON keys. For example: `"a.b"`.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['[1, 2, 3]', '[4, 5]'])
        >>> bbq.json_query_array(s)
        0    ['1' '2' '3']
        1        ['4' '5']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": [{"name": "apple"}, {"name": "cherry"}]}',
        ...   '{"fruits": [{"name": "guava"}, {"name": "grapes"}]}'
        ... ])
        >>> bbq.json_query_array(s, "$.fruits")
        0    ['{"name":"apple"}' '{"name":"cherry"}']
        1    ['{"name":"guava"}' '{"name":"grapes"}']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": {"color": "red",   "names": ["apple","cherry"]}}',
        ...   '{"fruits": {"color": "green", "names": ["guava", "grapes"]}}'
        ... ])
        >>> bbq.json_query_array(s, "$.fruits.names")
        0    ['"apple"' '"cherry"']
        1    ['"guava"' '"grapes"']
        dtype: list<item: string>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the parsed arrays from the input.
    """
    return input._apply_unary_op(ops.JSONQueryArray(json_path=json_path))


def json_value(
    input: series.Series,
    json_path: str = "$",
) -> series.Series:
    """Extracts a JSON scalar value and converts it to a SQL ``STRING`` value. In
    addtion, this function:
    - Removes the outermost quotes and unescapes the values.
    - Returns a SQL ``NULL`` if a non-scalar value is selected.
    - Uses double quotes to escape invalid ``JSON_PATH`` characters in JSON keys.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['{"name": "Jakob", "age": "6"}', '{"name": "Jakob", "age": []}'])
        >>> bbq.json_value(s, json_path="$.age")
        0    6
        1  <NA>
        dtype: string

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the JSON-formatted STRING.
    """
    return input._apply_unary_op(ops.JSONValue(json_path=json_path))


def json_value_array(
    input: series.Series,
    json_path: str = "$",
) -> series.Series:
    """
    Extracts a JSON array of scalar values and converts it to a SQL ``ARRAY<STRING>``
    value. In addition, this function:

    - Removes the outermost quotes and unescapes the values.
    - Returns a SQL ``NULL`` if the selected value isn't an array or not an array
      containing only scalar values.
    - Uses double quotes to escape invalid ``JSON_PATH`` characters in JSON keys.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['[1, 2, 3]', '[4, 5]'])
        >>> bbq.json_value_array(s)
        0    ['1' '2' '3']
        1        ['4' '5']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": ["apples", "oranges", "grapes"]',
        ...   '{"fruits": ["guava", "grapes"]}'
        ... ])
        >>> bbq.json_value_array(s, "$.fruits")
        0    ['apples' 'oranges' 'grapes']
        1               ['guava' 'grapes']
        dtype: list<item: string>[pyarrow]

        >>> s = bpd.Series([
        ...   '{"fruits": {"color": "red",   "names": ["apple","cherry"]}}',
        ...   '{"fruits": {"color": "green", "names": ["guava", "grapes"]}}'
        ... ])
        >>> bbq.json_value_array(s, "$.fruits.names")
        0    ['apple' 'cherry']
        1    ['guava' 'grapes']
        dtype: list<item: string>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON data (as native JSON objects or JSON-formatted strings).
        json_path (str):
            The JSON path identifying the data that you want to obtain from the input.

    Returns:
        bigframes.series.Series: A new Series with the parsed arrays from the input.
    """
    return input._apply_unary_op(ops.JSONValueArray(json_path=json_path))


@utils.preview(name="The JSON-related API `parse_json`")
def parse_json(
    input: series.Series,
) -> series.Series:
    """Converts a series with a JSON-formatted STRING value to a JSON value.

    .. warning::
        The JSON-related API `parse_json` is in preview. Its behavior may change in
        future versions.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series(['{"class": {"students": [{"id": 5}, {"id": 12}]}}'])
        >>> s
        0    {"class": {"students": [{"id": 5}, {"id": 12}]}}
        dtype: string
        >>> bbq.parse_json(s)
        0    {"class":{"students":[{"id":5},{"id":12}]}}
        dtype: extension<dbjson<JSONArrowType>>[pyarrow]

    Args:
        input (bigframes.series.Series):
            The Series containing JSON-formatted strings).

    Returns:
        bigframes.series.Series: A new Series with the JSON value.
    """
    return input._apply_unary_op(ops.ParseJSON())
