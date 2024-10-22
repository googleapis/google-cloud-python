# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/parquet.py
""" parquet compat """
from __future__ import annotations

from bigframes import constants


class ParquetIOMixin:
    def read_parquet(
        self,
        path: str,
        *,
        engine: str = "auto",
    ):
        r"""Load a Parquet object from the file path (local or Cloud Storage), returning a DataFrame.

        .. note::
            This method will not guarantee the same ordering as the file.
            Instead, set a serialized index column as the index and sort by
            that in the resulting DataFrame.

        .. note::
            For non-"bigquery" engine, data is inlined in the query SQL if it is
            small enough (roughly 5MB or less in memory). Larger size data is
            loaded to a BigQuery table instead.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> gcs_path = "gs://cloud-samples-data/bigquery/us-states/us-states.parquet"
            >>> df = bpd.read_parquet(path=gcs_path, engine="bigquery")

        Args:
            path (str):
                Local or Cloud Storage path to Parquet file.
            engine (str):
                One of ``'auto', 'pyarrow', 'fastparquet'``, or ``'bigquery'``.
                Parquet library to parse the file. If set to ``'bigquery'``,
                order is not preserved. Default, ``'auto'``.

        Returns:
            bigframes.pandas.DataFrame: A BigQuery DataFrames.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
