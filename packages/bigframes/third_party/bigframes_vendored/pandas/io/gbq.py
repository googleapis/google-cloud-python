# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/gbq.py
""" Google BigQuery support """

from __future__ import annotations

from typing import Any, Dict, Iterable, Literal, Optional, Tuple, Union

from bigframes import constants

FilterOps = Literal["in", "not in", "<", "<=", "==", "!=", ">=", ">", "LIKE"]
FilterType = Tuple[str, FilterOps, Any]
FiltersType = Union[Iterable[FilterType], Iterable[Iterable[FilterType]]]


class GBQIOMixin:
    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        filters: FiltersType = (),
        use_cache: Optional[bool] = None,
        col_order: Iterable[str] = (),
    ):
        """Loads a DataFrame from BigQuery.

        BigQuery tables are an unordered, unindexed data source. By default,
        the DataFrame will have an arbitrary index and ordering.

        Set the `index_col` argument to one or more columns to choose an
        index. The resulting DataFrame is sorted by the index columns. For the
        best performance, ensure the index columns don't contain duplicate
        values.

        .. note::
            By default, even SQL query inputs with an ORDER BY clause create a
            DataFrame with an arbitrary ordering. Use ``row_number() OVER
            (ORDER BY ...) AS rowindex`` in your SQL query and set
            ``index_col='rowindex'`` to preserve the desired ordering.

            If your query doesn't have an ordering, select ``GENERATE_UUID() AS
            rowindex`` in your SQL and set ``index_col='rowindex'`` for the
            best performance.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        If the input is a table ID:

            >>> df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

        Read table path with wildcard suffix and filters:
            >>> df = bpd.read_gbq_table("bigquery-public-data.noaa_gsod.gsod19*", filters=[("_table_suffix", ">=", "30"), ("_table_suffix", "<=", "39")])

        Preserve ordering in a query input.

            >>> df = bpd.read_gbq('''
            ...    SELECT
            ...       -- Instead of an ORDER BY clause on the query, use
            ...       -- ROW_NUMBER() to create an ordered DataFrame.
            ...       ROW_NUMBER() OVER (ORDER BY AVG(pitchSpeed) DESC)
            ...         AS rowindex,
            ...
            ...       pitcherFirstName,
            ...       pitcherLastName,
            ...       AVG(pitchSpeed) AS averagePitchSpeed
            ...     FROM `bigquery-public-data.baseball.games_wide`
            ...     WHERE year = 2016
            ...     GROUP BY pitcherFirstName, pitcherLastName
            ... ''', index_col="rowindex")
            >>> df.head(2)
                     pitcherFirstName pitcherLastName  averagePitchSpeed
            rowindex
            1                Albertin         Chapman          96.514113
            2                 Zachary         Britton          94.591039
            <BLANKLINE>
            [2 rows x 3 columns]

        Reading data with `columns` and `filters` parameters:

            >>> columns = ['pitcherFirstName', 'pitcherLastName', 'year', 'pitchSpeed']
            >>> filters = [('year', '==', 2016), ('pitcherFirstName', 'in', ['John', 'Doe']), ('pitcherLastName', 'in', ['Gant'])]
            >>> df = bpd.read_gbq(
            ...             "bigquery-public-data.baseball.games_wide",
            ...             columns=columns,
            ...             filters=filters,
            ...         )
            >>> df.head(1)
                     pitcherFirstName	pitcherLastName     year	pitchSpeed
            0	                 John	           Gant	    2016            82
            <BLANKLINE>
            [1 rows x 4 columns]

        Args:
            query_or_table (str):
                A SQL string to be executed or a BigQuery table to be read. The
                table must be specified in the format of
                `project.dataset.tablename` or `dataset.tablename`.
                Can also take wildcard table name, such as `project.dataset.table_prefix*`.
                In tha case, will read all the matched table as one DataFrame.
            index_col (Iterable[str] or str):
                Name of result column(s) to use for index in results DataFrame.
            columns (Iterable[str]):
                List of BigQuery column names in the desired order for results
                DataFrame.
            configuration (dict, optional):
                Query config parameters for job processing.
                For example: configuration = {'query': {'useQueryCache': False}}.
                For more information see `BigQuery REST API Reference
                <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__.
            max_results (Optional[int], default None):
                If set, limit the maximum number of rows to fetch from the
                query results.
            filters (Union[Iterable[FilterType], Iterable[Iterable[FilterType]]], default ()): To
                filter out data. Filter syntax: [[(column, op, val), …],…] where
                op is [==, >, >=, <, <=, !=, in, not in, LIKE]. The innermost tuples
                are transposed into a set of filters applied through an AND
                operation. The outer Iterable combines these sets of filters
                through an OR operation. A single Iterable of tuples can also
                be used, meaning that no OR operation between set of filters
                is to be conducted.
                If using wildcard table suffix in query_or_table, can specify
                '_table_suffix' pseudo column to filter the tables to be read
                into the DataFrame.
            use_cache (Optional[bool], default None):
                Caches query results if set to `True`. When `None`, it behaves
                as `True`, but should not be combined with `useQueryCache` in
                `configuration` to avoid conflicts.
            col_order (Iterable[str]):
                Alias for columns, retained for backwards compatibility.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame representing results of the query or table.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
