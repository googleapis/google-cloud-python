# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/parquet.py
""" parquet compat """
from __future__ import annotations


class ParquetIOMixin:
    def read_parquet(
        self,
        path: str,
    ):
        r"""Load a Parquet object from the file path (local or Cloud Storage), returning a DataFrame.

        .. note::
            This method will not guarantee the same ordering as the file.
            Instead, set a serialized index column as the index and sort by
            that in the resulting DataFrame.

        Args:
            path (str):
                Local or Cloud Storage path to Parquet file.

        Returns:
            bigframes.dataframe.DataFrame: A BigQuery DataFrames.
        """
        raise NotImplementedError("abstract method")
