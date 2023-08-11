# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/gbq.py
""" Google BigQuery support """

from __future__ import annotations

from typing import Iterable, Optional


class GBQIOMixin:
    def read_gbq(
        self,
        query: str,
        *,
        index_col: Iterable[str] | str = (),
        col_order: Iterable[str] = (),
        max_results: Optional[int] = None,
    ):
        """Loads DataFrame from BigQuery.

        Args:
            query (str):
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

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame representing results of the query or table.
        """
        raise NotImplementedError("abstract method")
