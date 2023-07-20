# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/parquet.py
""" parquet compat """
from __future__ import annotations


class ParquetIOMixin:
    def read_parquet(
        self,
        path: str,
    ):
        r"""Load a parquet object from the file path (local or GCS), returning a DataFrame.

        Args:
            path:
                Local or GCS path to parquet file.

        Note:
            This method will not guarantee the same ordering as the file.
            Instead, set a serialized index column as the index and sort by
            that in the resulting DataFrame.
        """
        raise NotImplementedError("abstract method")
