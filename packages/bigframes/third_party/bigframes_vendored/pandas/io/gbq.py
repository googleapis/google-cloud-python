# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/gbq.py
""" Google BigQuery support """

from __future__ import annotations

from typing import Any, Dict, Iterable, Literal, Optional, Tuple, Union

from bigframes import constants
import bigframes.enums

FilterOps = Literal["in", "not in", "<", "<=", "==", "!=", ">=", ">", "LIKE"]
FilterType = Tuple[str, FilterOps, Any]
FiltersType = Union[Iterable[FilterType], Iterable[Iterable[FilterType]]]


class GBQIOMixin:
    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Union[Iterable[str], str, bigframes.enums.DefaultIndexKind] = (),
        columns: Iterable[str] = (),
        configuration: Optional[Dict] = None,
        max_results: Optional[int] = None,
        filters: FiltersType = (),
        use_cache: Optional[bool] = None,
        col_order: Iterable[str] = (),
    ):
        """Loads a DataFrame from BigQuery.

        BigQuery tables are an unordered, unindexed data source. To add support
        pandas-compatibility, the following indexing options are supported via
        the ``index_col`` parameter:

        * (Empty iterable, default) A default index. **Behavior may change.**
          Explicitly set ``index_col`` if your application makes use of
          specific index values.

          If a table has primary key(s), those are used as the index,
          otherwise a sequential index is generated.
        * (:attr:`bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64`) Add an
          arbitrary sequential index and ordering. **Warning** This uses an
          analytic windowed operation that prevents filtering push down. Avoid
          using on large clustered or partitioned tables.
        * (Recommended) Set the ``index_col`` argument to one or more columns.
          Unique values for the row labels are recommended. Duplicate labels
          are possible, but note that joins on a non-unique index can duplicate
          rows via pandas-compatible outer join behavior.

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
            >>> filters = [('year', '==', 2016), ('pitcherFirstName', 'in', ['John', 'Doe']), ('pitcherLastName', 'in', ['Gant']), ('pitchSpeed', '>', 94)]
            >>> df = bpd.read_gbq(
            ...             "bigquery-public-data.baseball.games_wide",
            ...             columns=columns,
            ...             filters=filters,
            ...         )
            >>> df.head(1)
              pitcherFirstName pitcherLastName  year  pitchSpeed
            0             John            Gant  2016          95
            <BLANKLINE>
            [1 rows x 4 columns]

        Args:
            query_or_table (str):
                A SQL string to be executed or a BigQuery table to be read. The
                table must be specified in the format of
                `project.dataset.tablename` or `dataset.tablename`.
                Can also take wildcard table name, such as `project.dataset.table_prefix*`.
                In tha case, will read all the matched table as one DataFrame.
            index_col (Iterable[str], str, bigframes.enums.DefaultIndexKind):
                Name of result column(s) to use for index in results DataFrame.

                If an empty iterable, such as ``()``, a default index is
                generated. Do not depend on specific index values in this case.

                **New in bigframes version 1.3.0**: If ``index_cols`` is not
                set, the primary key(s) of the table are used as the index.

                **New in bigframes version 1.4.0**: Support
                :class:`bigframes.enums.DefaultIndexKind` to override default index
                behavior.
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

        Raises:
            bigframes.exceptions.DefaultIndexWarning:
                Using the default index is discouraged, such as with clustered
                or partitioned tables without primary keys.
            ValueError:
                When both ``columns`` and ``col_order`` are specified.
            ValueError:
                If ``configuration`` is specified when directly reading
                from a table.

        Returns:
            bigframes.pandas.DataFrame:
                A DataFrame representing results of the query or table.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
