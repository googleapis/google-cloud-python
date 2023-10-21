# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/io/parsers/readers.py
"""
Module contains tools for processing files into DataFrames or other objects

GH#48849 provides a convenient way of deprecating keyword arguments
"""
from __future__ import annotations

from typing import (
    Any,
    Dict,
    IO,
    Literal,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np

from bigframes import constants


class ReaderIOMixin:
    def read_csv(
        self,
        filepath_or_buffer: str,
        *,
        sep: Optional[str] = ",",
        header: Optional[int] = 0,
        names: Optional[
            Union[MutableSequence[Any], np.ndarray[Any, Any], Tuple[Any, ...], range]
        ] = None,
        index_col: Optional[
            Union[int, str, Sequence[Union[str, int]], Literal[False]]
        ] = None,
        usecols=None,
        dtype: Optional[Dict] = None,
        engine: Optional[
            Literal["c", "python", "pyarrow", "python-fwf", "bigquery"]
        ] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ):
        """Loads DataFrame from comma-separated values (csv) file locally or from
        Cloud Storage.

        The CSV file data will be persisted as a temporary BigQuery table, which can be
        automatically recycled after the Session is closed.

        .. note::
            using `engine="bigquery"` will not guarantee the same ordering as the
            file. Instead, set a serialized index column as the index and sort by
            that in the resulting DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> gcs_path = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
            >>> df = bpd.read_csv(filepath_or_buffer=gcs_path)
            >>> df.head(2)
                  name post_abbr
            0  Alabama        AL
            1   Alaska        AK
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            filepath_or_buffer (str):
                A local or Google Cloud Storage (`gs://`) path with `engine="bigquery"`
                otherwise passed to pandas.read_csv.
            sep (Optional[str], default ","):
                the separator for fields in a CSV file. For the BigQuery engine, the separator
                can be any ISO-8859-1 single-byte character. To use a character in the range
                128-255, you must encode the character as UTF-8. Both engines support
                `sep="\t"` to specify tab character as separator. Default engine supports
                having any number of spaces as separator by specifying `sep="\\s+"`. Separators
                longer than 1 character are interpreted as regular expressions by the default
                engine. BigQuery engine only supports single character separators.
            header (Optional[int], default 0):
                row number to use as the column names.
                - ``None``: Instructs autodetect that there are no headers and data should be
                read starting from the first row.
                - ``0``: If using `engine="bigquery"`, Autodetect tries to detect headers in the
                first row. If they are not detected, the row is read as data. Otherwise data
                is read starting from the second row. When using default engine, pandas assumes
                the first row contains column names unless the `names` argument is specified.
                If `names` is provided, then the first row is ignored, second row is read as
                data, and column names are inferred from `names`.
                - ``N > 0``: If using `engine="bigquery"`, Autodetect skips N rows and tries
                to detect headers in row N+1. If headers are not detected, row N+1 is just
                skipped. Otherwise row N+1 is used to extract column names for the detected
                schema. When using default engine, pandas will skip N rows and assumes row N+1
                contains column names unless the `names` argument is specified. If `names` is
                provided, row N+1 will be ignored, row N+2 will be read as data, and column
                names are inferred from `names`.
            names (default None):
                a list of column names to use. If the file contains a header row and you
                want to pass this parameter, then `header=0` should be passed as well so the
                first (header) row is ignored. Only to be used with default engine.
            index_col (default None):
                column(s) to use as the row labels of the DataFrame, either given as
                string name or column index. `index_col=False` can be used with the default
                engine only to enforce that the first column is not used as the index. Using
                column index instead of column name is only supported with the default engine.
                The BigQuery engine only supports having a single column name as the `index_col`.
                Neither engine supports having a multi-column index.
            usecols (default None):
                List of column names to use): The BigQuery engine only supports having a list
                of string column names. Column indices and callable functions are only supported
                with the default engine. Using the default engine, the column names in `usecols`
                can be defined to correspond to column names provided with the `names` parameter
                (ignoring the document's header row of column names). The order of the column
                indices/names in `usecols` is ignored with the default engine. The order of the
                column names provided with the BigQuery engine will be consistent in the resulting
                dataframe. If using a callable function with the default engine, only column names
                that evaluate to True by the callable function will be in the resulting dataframe.
            dtype (data type for data or columns):
                Data type for data or columns. Only to be used with default engine.
            engine (Optional[Dict], default None):
                Type of engine to use. If `engine="bigquery"` is specified, then BigQuery's load API will be used.
                Otherwise, the engine will be passed to `pandas.read_csv`.
            encoding (Optional[str], default to None):
                encoding the character encoding of the data. The default encoding is `UTF-8` for both
                engines. The default engine acceps a wide range of encodings. Refer to Python
                documentation for a comprehensive list,
                https://docs.python.org/3/library/codecs.html#standard-encodings
                The BigQuery engine only supports `UTF-8` and `ISO-8859-1`.
            **kwargs:
                keyword arguments for `pandas.read_csv` when not using the BigQuery engine.


        Returns:
            bigframes.dataframe.DataFrame: A BigQuery DataFrames.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def read_json(
        self,
        path_or_buf: str | IO["bytes"],
        *,
        orient: Literal[
            "split", "records", "index", "columns", "values", "table"
        ] = "columns",
        dtype: Optional[Dict] = None,
        encoding: Optional[str] = None,
        lines: bool = False,
        engine: Literal["ujson", "pyarrow", "bigquery"] = "ujson",
        **kwargs,
    ):
        """
        Convert a JSON string to DataFrame object.

        .. note::
            using `engine="bigquery"` will not guarantee the same ordering as the
            file. Instead, set a serialized index column as the index and sort by
            that in the resulting DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> gcs_path = "gs://bigframes-dev-testing/sample1.json"
            >>> df = bpd.read_json(path_or_buf=gcs_path, lines=True, orient="records")
            >>> df.head(2)
               id   name
            0   1  Alice
            1   2    Bob
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            path_or_buf (a valid JSON str, path object or file-like object):
                A local or Google Cloud Storage (`gs://`) path with `engine="bigquery"`
                otherwise passed to pandas.read_json.
            orient (str, optional):
                If `engine="bigquery"` orient only supports "records".
                Indication of expected JSON string format.
                Compatible JSON strings can be produced by ``to_json()`` with a
                corresponding orient value.
                The set of possible orients is:

                - ``'split'`` : dict like
                    ``{{index -> [index], columns -> [columns], data -> [values]}}``
                - ``'records'`` : list like
                    ``[{{column -> value}}, ... , {{column -> value}}]``
                - ``'index'`` : dict like ``{{index -> {{column -> value}}}}``
                - ``'columns'`` : dict like ``{{column -> {{index -> value}}}}``
                - ``'values'`` : just the values array

            dtype (bool or dict, default None):
                If True, infer dtypes; if a dict of column to dtype, then use those;
                if False, then don't infer dtypes at all, applies only to the data.

                For all ``orient`` values except ``'table'``, default is True.
            encoding (str, default is 'utf-8'):
                The encoding to use to decode py3 bytes.
            lines (bool, default False):
                Read the file as a json object per line. If using `engine="bigquery"` lines only supports True.
            engine ({{"ujson", "pyarrow", "bigquery"}}, default "ujson"):
                Type of engine to use. If `engine="bigquery"` is specified, then BigQuery's load API will be used.
                Otherwise, the engine will be passed to `pandas.read_json`.
            **kwargs:
                keyword arguments for `pandas.read_json` when not using the BigQuery engine.

        Returns:
            bigframes.dataframe.DataFrame:
                The DataFrame representing JSON contents.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
