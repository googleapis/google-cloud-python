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

import json
import typing
from typing import Collection, Literal, Mapping, Optional, Union

import google.cloud.bigquery as bigquery

import bigframes.core.sql
import bigframes.ml.utils as utils

if typing.TYPE_CHECKING:
    import bigframes.dataframe as dataframe
    import bigframes.series as series
    import bigframes.session

"""
Search functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/search_functions
"""


def create_vector_index(
    table_id: str,
    column_name: str,
    *,
    replace: bool = False,
    index_name: Optional[str] = None,
    distance_type="cosine",
    stored_column_names: Collection[str] = (),
    index_type: str = "ivf",
    ivf_options: Optional[Mapping] = None,
    tree_ah_options: Optional[Mapping] = None,
    session: Optional[bigframes.session.Session] = None,
) -> None:
    """
    Creates a new vector index on a column of a table.

    This method calls the `CREATE VECTOR INDEX DDL statement
    <https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_vector_index_statement>`_.

    """
    import bigframes.pandas

    if index_name is None:
        table_ref = bigquery.TableReference.from_string(table_id)
        index_name = table_ref.table_id

    options = {
        "index_type": index_type.upper(),
        "distance_type": distance_type.upper(),
    }

    if ivf_options is not None:
        options["ivf_options"] = json.dumps(ivf_options)

    if tree_ah_options is not None:
        options["tree_ah_options"] = json.dumps(tree_ah_options)

    sql = bigframes.core.sql.create_vector_index_ddl(
        replace=replace,
        index_name=index_name,
        table_name=table_id,
        column_name=column_name,
        stored_column_names=stored_column_names,
        options=options,
    )

    # Use global read_gbq to execute this for better location autodetection.
    if session is None:
        read_gbq_query = bigframes.pandas.read_gbq_query
    else:
        read_gbq_query = session.read_gbq_query

    read_gbq_query(sql)


def vector_search(
    base_table: str,
    column_to_search: str,
    query: Union[dataframe.DataFrame, series.Series],
    *,
    query_column_to_search: Optional[str] = None,
    top_k: Optional[int] = None,
    distance_type: Optional[Literal["euclidean", "cosine", "dot_product"]] = None,
    fraction_lists_to_search: Optional[float] = None,
    use_brute_force: Optional[bool] = None,
) -> dataframe.DataFrame:
    """
    Conduct vector search which searches embeddings to find semantically similar entities.

    This method calls the `VECTOR_SEARCH() SQL function
    <https://cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search>`_.

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
        ...             top_k=2).sort_values("id")
          query_id  embedding  id my_embedding  distance
        0      dog    [1. 2.]   1      [1. 2.]       0.0
        1      cat  [3.  5.2]   2      [2. 4.]   1.56205
        0      dog    [1. 2.]   4    [1.  3.2]       1.2
        1      cat  [3.  5.2]   5    [5.  5.4]  2.009975
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
        ...             top_k=2,
        ...             use_brute_force=True).sort_values("id")
             embedding  id my_embedding  distance
        dog    [1. 2.]   1      [1. 2.]       0.0
        cat  [3.  5.2]   2      [2. 4.]   1.56205
        dog    [1. 2.]   4    [1.  3.2]       1.2
        cat  [3.  5.2]   5    [5.  5.4]  2.009975
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
        top_k (int):
            Sepecifies the number of nearest neighbors to return. Default to 10.
        distance_type (str, defalt "euclidean"):
            Specifies the type of metric to use to compute the distance between two vectors.
            Possible values are "euclidean", "cosine" and "dot_product".
            Default to "euclidean".
        fraction_lists_to_search (float, range in [0.0, 1.0]):
            Specifies the percentage of lists to search. Specifying a higher percentage leads to
            higher recall and slower performance, and the converse is true when specifying a lower
            percentage. It is only used when a vector index is also used. You can only specify
            ``fraction_lists_to_search`` when ``use_brute_force`` is set to False.
        use_brute_force (bool):
            Determines whether to use brute force search by skipping the vector index if one is available.
            Default to False.

    Returns:
        bigframes.dataframe.DataFrame: A DataFrame containing vector search result.
    """
    import bigframes.series

    if (
        isinstance(query, bigframes.series.Series)
        and query_column_to_search is not None
    ):
        raise ValueError(
            "You can't specify query_column_to_search when query is a Series."
        )

    # Only populate options if not set to the default value.
    # This avoids accidentally setting options that are mutually exclusive.
    options = None
    if fraction_lists_to_search is not None:
        options = {} if options is None else options
        options["fraction_lists_to_search"] = fraction_lists_to_search
    if use_brute_force is not None:
        options = {} if options is None else options
        options["use_brute_force"] = use_brute_force

    (query,) = utils.batch_convert_to_dataframe(query)
    sql_string, index_col_ids, index_labels = query._to_sql_query(include_index=True)

    sql = bigframes.core.sql.create_vector_search_sql(
        sql_string=sql_string,
        base_table=base_table,
        column_to_search=column_to_search,
        query_column_to_search=query_column_to_search,
        top_k=top_k,
        distance_type=distance_type,
        options=options,
    )
    if index_col_ids is not None:
        df = query._session.read_gbq(sql, index_col=index_col_ids)
        df.index.names = index_labels
    else:
        df = query._session.read_gbq(sql)

    return df
