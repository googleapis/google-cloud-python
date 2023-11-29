# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/gbq.py
""" Google BigQuery support """

from __future__ import annotations

from typing import Iterable, Optional

from bigframes import constants


class GBQIOMixin:
    def read_gbq(
        self,
        query_or_table: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
        use_cache: bool = True,
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

        Args:
            query_or_table (str):
                A SQL string to be executed or a BigQuery table to be read. The
                table must be specified in the format of
                `project.dataset.tablename` or `dataset.tablename`.
            index_col (Iterable[str] or str):
                Name of result column(s) to use for index in results DataFrame.
            col_order (Iterable[str]):
                List of BigQuery column names in the desired order for results
                DataFrame.
            max_results (Optional[int], default None):
                If set, limit the maximum number of rows to fetch from the
                query results.
            use_cache (bool, default True):
                Whether to cache the query inputs. Default to True.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame representing results of the query or table.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
