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


"""This module integrates BigQuery built-in functions for use with DataFrame objects,
such as array functions:
https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions. """


from __future__ import annotations

import typing
from typing import Literal, Optional, Union

import bigframes.constants as constants
import bigframes.core.groupby as groupby
import bigframes.core.sql
import bigframes.ml.utils as utils
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops
import bigframes.series

if typing.TYPE_CHECKING:
    import bigframes.dataframe as dataframe
    import bigframes.series as series


# Array functions defined from
# https://cloud.google.com/bigquery/docs/reference/standard-sql/array_functions


def array_length(series: series.Series) -> series.Series:
    """Compute the length of each array element in the Series.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([[1, 2, 8, 3], [], [3, 4]])
        >>> bbq.array_length(s)
        0    4
        1    0
        2    2
        dtype: Int64

    You can also apply this function directly to Series.

        >>> s.apply(bbq.array_length, by_row=False)
        0    4
        1    0
        2    2
        dtype: Int64

    Args:
        series (bigframes.series.Series): A Series with array columns.

    Returns:
        bigframes.series.Series: A Series of integer values indicating
            the length of each element in the Series.

    """
    return series._apply_unary_op(ops.len_op)


def array_agg(
    obj: groupby.SeriesGroupBy | groupby.DataFrameGroupBy,
) -> series.Series | dataframe.DataFrame:
    """Group data and create arrays from selected columns, omitting NULLs to avoid
    BigQuery errors (NULLs not allowed in arrays).

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

    For a SeriesGroupBy object:

        >>> lst = ['a', 'a', 'b', 'b', 'a']
        >>> s = bpd.Series([1, 2, 3, 4, np.nan], index=lst)
        >>> bbq.array_agg(s.groupby(level=0))
        a    [1. 2.]
        b    [3. 4.]
        dtype: list<item: double>[pyarrow]

    For a DataFrameGroupBy object:

        >>> l = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]
        >>> df = bpd.DataFrame(l, columns=["a", "b", "c"])
        >>> bbq.array_agg(df.groupby(by=["b"]))
                 a      c
        b
        1.0    [2]    [3]
        2.0  [1 1]  [3 2]
        <BLANKLINE>
        [2 rows x 2 columns]

    Args:
        obj (groupby.SeriesGroupBy | groupby.DataFrameGroupBy):
            A GroupBy object to be applied the function.

    Returns:
        bigframes.series.Series | bigframes.dataframe.DataFrame: A Series or
            DataFrame containing aggregated array columns, and indexed by the
            original group columns.
    """
    if isinstance(obj, groupby.SeriesGroupBy):
        return obj._aggregate(agg_ops.ArrayAggOp())
    elif isinstance(obj, groupby.DataFrameGroupBy):
        return obj._aggregate_all(agg_ops.ArrayAggOp(), numeric_only=False)
    else:
        raise ValueError(
            f"Unsupported type {type(obj)} to apply `array_agg` function. {constants.FEEDBACK_LINK}"
        )


def array_to_string(series: series.Series, delimiter: str) -> series.Series:
    """Converts array elements within a Series into delimited strings.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import numpy as np
        >>> bpd.options.display.progress_bar = None

        >>> s = bpd.Series([["H", "i", "!"], ["Hello", "World"], np.nan, [], ["Hi"]])
        >>> bbq.array_to_string(s, delimiter=", ")
            0         H, i, !
            1    Hello, World
            2
            3
            4              Hi
            dtype: string

    Args:
        series (bigframes.series.Series): A Series containing arrays.
        delimiter (str): The string used to separate array elements.

    Returns:
        bigframes.series.Series: A Series containing delimited strings.

    """
    return series._apply_unary_op(ops.ArrayToStringOp(delimiter=delimiter))


# JSON functions defined from
# https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions


def json_set(
    series: series.Series,
    json_path_value_pairs: typing.Sequence[typing.Tuple[str, typing.Any]],
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
        json_path_value_pairs (Sequence[Tuple[str, typing.Any]]):
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


def struct(value: dataframe.DataFrame) -> series.Series:
    """Takes a DataFrame and converts it into a Series of structs with each
    struct entry corresponding to a DataFrame row and each struct field
    corresponding to a DataFrame column

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> import bigframes.series as series
        >>> bpd.options.display.progress_bar = None

        >>> srs = series.Series([{"version": 1, "project": "pandas"}, {"version": 2, "project": "numpy"},])
        >>> df = srs.struct.explode()
        >>> bbq.struct(df)
        0    {'project': 'pandas', 'version': 1}
        1     {'project': 'numpy', 'version': 2}
        dtype: struct<project: string, version: int64>[pyarrow]

        Args:
            value (bigframes.dataframe.DataFrame):
                The DataFrame to be converted to a Series of structs

        Returns:
            bigframes.series.Series: A new Series with struct entries representing rows of the original DataFrame
    """
    block = value._block
    block, result_id = block.apply_nary_op(
        block.value_columns, ops.StructOp(column_names=tuple(block.column_labels))
    )
    block = block.select_column(result_id)
    return bigframes.series.Series(block)


# Search functions defined from
# https://cloud.google.com/bigquery/docs/reference/standard-sql/search_functions


def vector_search(
    base_table: str,
    column_to_search: str,
    query: Union[dataframe.DataFrame, series.Series],
    *,
    query_column_to_search: Optional[str] = None,
    top_k: Optional[int] = 10,
    distance_type: Literal["euclidean", "cosine"] = "euclidean",
    fraction_lists_to_search: Optional[float] = None,
    use_brute_force: bool = False,
) -> dataframe.DataFrame:
    """
    Conduct vector search which searches embeddings to find semantically similar entities.

    **Examples:**


        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> bpd.options.display.progress_bar = None

    DataFrame embeddings for which to find nearest neighbors. The ``ARRAY<FLOAT64>`` column
    is used as the search query:

        >>> search_query = bpd.DataFrame({"query_id": ["dog", "cat"],
        ...                               "embedding": [[1.0, 2.0], [3.0, 5.2]]})
        >>> bbq.vector_search(
        ...             base_table="bigframes-dev.bigframes_tests_sys.base_table",
        ...             column_to_search="my_embedding",
        ...             query=search_query,
        ...             top_k=2)
          query_id  embedding  id my_embedding  distance
        1      cat  [3.  5.2]   5    [5.  5.4]  2.009975
        0      dog    [1. 2.]   1      [1. 2.]       0.0
        0      dog    [1. 2.]   4    [1.  3.2]       1.2
        1      cat  [3.  5.2]   2      [2. 4.]   1.56205
        <BLANKLINE>
        [4 rows x 5 columns]

    Series embeddings for which to find nearest neighbors:

        >>> search_query = bpd.Series([[1.0, 2.0], [3.0, 5.2]],
        ...                            index=["dog", "cat"],
        ...                            name="embedding")
        >>> bbq.vector_search(
        ...             base_table="bigframes-dev.bigframes_tests_sys.base_table",
        ...             column_to_search="my_embedding",
        ...             query=search_query,
        ...             top_k=2)
             embedding  id my_embedding  distance
        dog    [1. 2.]   1      [1. 2.]       0.0
        cat  [3.  5.2]   5    [5.  5.4]  2.009975
        dog    [1. 2.]   4    [1.  3.2]       1.2
        cat  [3.  5.2]   2      [2. 4.]   1.56205
        <BLANKLINE>
        [4 rows x 4 columns]

    You can specify the name of the column in the query DataFrame embeddings and distance type.
    If you specify query_column_to_search_value, it will use the provided column which contains
    the embeddings for which to find nearest neighbors. Otherwiese, it uses the column_to_search value.

        >>> search_query = bpd.DataFrame({"query_id": ["dog", "cat"],
        ...                               "embedding": [[1.0, 2.0], [3.0, 5.2]],
        ...                               "another_embedding": [[0.7, 2.2], [3.3, 5.2]]})
        >>> bbq.vector_search(
        ...             base_table="bigframes-dev.bigframes_tests_sys.base_table",
        ...             column_to_search="my_embedding",
        ...             query=search_query,
        ...             distance_type="cosine",
        ...             query_column_to_search="another_embedding",
        ...             top_k=2)
          query_id  embedding another_embedding  id my_embedding  distance
        1      cat  [3.  5.2]         [3.3 5.2]   2      [2. 4.]  0.005181
        0      dog    [1. 2.]         [0.7 2.2]   4    [1.  3.2]  0.000013
        1      cat  [3.  5.2]         [3.3 5.2]   1      [1. 2.]  0.005181
        0      dog    [1. 2.]         [0.7 2.2]   3    [1.5 7. ]  0.004697
        <BLANKLINE>
        [4 rows x 6 columns]

    Args:
        base_table (str):
            The table to search for nearest neighbor embeddings.
        column_to_search (str):
            The name of the base table column to search for nearest neighbor embeddings.
            The column must have a type of ``ARRAY<FLOAT64>``. All elements in the array must be non-NULL.
        query (bigframes.dataframe.DataFrame | bigframes.dataframe.Series):
            A Series or DataFrame that provides the embeddings for which to find nearest neighbors.
        query_column_to_search (str):
            Specifies the name of the column in the query that contains the embeddings for which to
            find nearest neighbors. The column must have a type of ``ARRAY<FLOAT64>``. All elements in
            the array must be non-NULL and all values in the column must have the same array dimensions
            as the values in the ``column_to_search`` column. Can only be set when query is a DataFrame.
        top_k (int, default 10):
            Sepecifies the number of nearest neighbors to return. Default to 10.
        distance_type (str, defalt "euclidean"):
            Specifies the type of metric to use to compute the distance between two vectors.
            Possible values are "euclidean" and "cosine". Default to "euclidean".
        fraction_lists_to_search (float, range in [0.0, 1.0]):
            Specifies the percentage of lists to search. Specifying a higher percentage leads to
            higher recall and slower performance, and the converse is true when specifying a lower
            percentage. It is only used when a vector index is also used. You can only specify
            ``fraction_lists_to_search`` when ``use_brute_force`` is set to False.
        use_brute_force (bool, default False):
            Determines whether to use brute force search by skipping the vector index if one is available.
            Default to False.

    Returns:
        bigframes.dataframe.DataFrame: A DataFrame containing vector search result.
    """
    if not fraction_lists_to_search and use_brute_force is True:
        raise ValueError(
            "You can't specify fraction_lists_to_search when use_brute_force is set to True."
        )
    if (
        isinstance(query, bigframes.series.Series)
        and query_column_to_search is not None
    ):
        raise ValueError(
            "You can't specify query_column_to_search when query is a Series."
        )
    # TODO(ashleyxu): Support options in vector search. b/344019989
    if fraction_lists_to_search is not None or use_brute_force is True:
        raise NotImplementedError(
            f"fraction_lists_to_search and use_brute_force is not supported. {constants.FEEDBACK_LINK}"
        )
    options = {
        "base_table": base_table,
        "column_to_search": column_to_search,
        "query_column_to_search": query_column_to_search,
        "distance_type": distance_type,
        "top_k": top_k,
        "fraction_lists_to_search": fraction_lists_to_search,
        "use_brute_force": use_brute_force,
    }

    (query,) = utils.convert_to_dataframe(query)
    sql_string, index_col_ids, index_labels = query._to_sql_query(include_index=True)

    sql = bigframes.core.sql.create_vector_search_sql(
        sql_string=sql_string, options=options  # type: ignore
    )
    if index_col_ids is not None:
        df = query._session.read_gbq(sql, index_col=index_col_ids)
    else:
        df = query._session.read_gbq(sql)
    df.index.names = index_labels

    return df
