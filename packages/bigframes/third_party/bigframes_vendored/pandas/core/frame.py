# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/frame.py
"""
DataFrame
---------
An efficient 2D container for potentially mixed-type time series or other
labeled data series.

Similar to its R counterpart, data.frame, except providing automatic data
alignment and a host of useful data manipulation methods having to do with the
labeling information
"""
from __future__ import annotations

from typing import Literal, Mapping, Optional, Sequence, Union

import numpy as np

from bigframes import constants
from third_party.bigframes_vendored.pandas.core.generic import NDFrame

# -----------------------------------------------------------------------
# DataFrame class


class DataFrame(NDFrame):
    """Two-dimensional, size-mutable, potentially heterogeneous tabular data.

    Data structure also contains labeled axes (rows and columns).
    Arithmetic operations align on both row and column labels. Can be
    thought of as a dict-like container for Series objects. The primary
    pandas data structure.
    """

    @property
    def shape(self) -> tuple[int, int]:
        """
        Return a tuple representing the dimensionality of the DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2, 3],
            ...                     'col2': [4, 5, 6]})
            >>> df.shape
            (3, 2)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def axes(self) -> list:
        """
        Return a list representing the axes of the DataFrame.

        It has the row axis labels and column axis labels as the only members.
        They are returned in that order.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.axes[1:]
            [Index(['col1', 'col2'], dtype='object')]
        """
        return [self.index, self.columns]

    @property
    def values(self) -> np.ndarray:
        """Return the values of DataFrame in the form of a NumPy array.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.values
            array([[1, 3],
                   [2, 4]], dtype=object)

        Args:
            dytype (default None):
                The dtype to pass to `numpy.asarray()`.
            copy (bool, default False):
                Whether to ensure that the returned value is not a view
                on another array.
            na_value (default None):
                The value to use for missing values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def info(
        self,
        verbose: bool | None = None,
        buf=None,
        max_cols: int | None = None,
        memory_usage: bool | None = None,
        show_counts: bool | None = None,
    ) -> None:
        """
        Print a concise summary of a DataFrame.

        This method prints information about a DataFrame including
        the index dtypeand columns, non-null values and memory usage.

        Args:
            verbose (bool, optional):
                Whether to print the full summary. By default, the setting in
                ``pandas.options.display.max_info_columns`` is followed.
            buf (writable buffer, defaults to sys.stdout):
                Where to send the output. By default, the output is printed to
                sys.stdout. Pass a writable buffer if you need to further process
                the output.
            max_cols (int, optional):
                When to switch from the verbose to the truncated output. If the
                DataFrame has more than `max_cols` columns, the truncated output
                is used. By default, the setting in
                ``pandas.options.display.max_info_columns`` is used.
            memory_usage (bool, optional):
                Specifies whether total memory usage of the DataFrame
                elements (including the index) should be displayed. By default,
                this follows the ``pandas.options.display.memory_usage`` setting.
                True always show memory usage. False never shows memory usage.
                Memory estimation is made based in column dtype and number of rows
                assuming values consume the same memory amount for corresponding dtypes.
            show_counts (bool, optional):
                Whether to show the non-null counts. By default, this is shown
                only if the DataFrame is smaller than
                ``pandas.options.display.max_info_rows`` and
                ``pandas.options.display.max_info_columns``. A value of True always
                shows the counts, and False never shows the counts.

        Returns:
            None: This method prints a summary of a DataFrame and returns None."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def memory_usage(self, index: bool = True):
        """
        Return the memory usage of each column in bytes.

        The memory usage can optionally include the contribution of
        the index and elements of `object` dtype.

        This value is displayed in `DataFrame.info` by default. This can be
        suppressed by setting ``pandas.options.display.memory_usage`` to False.

        Args:
            index (bool, default True):
                Specifies whether to include the memory usage of the DataFrame's
                index in returned Series. If ``index=True``, the memory usage of
                the index is the first item in the output.

        Returns:
            Series: A Series whose index is the original column names and whose values is the memory usage of each column in bytes.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # IO methods (to / from other formats)
    def to_numpy(self, dtype=None, copy=False, na_value=None, **kwargs) -> np.ndarray:
        """
        Convert the DataFrame to a NumPy array.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.to_numpy()
            array([[1, 3],
                   [2, 4]], dtype=object)

        Args:
            dtype (None):
                The dtype to pass to `numpy.asarray()`.
            copy (bool, default None):
                Whether to ensure that the returned value is not a view
                on another array.
            na_value (Any, default None):
                The value to use for missing values. The default value
                depends on dtype and the dtypes of the DataFrame columns.

        Returns:
            numpy.ndarray: The converted NumPy array.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_gbq(
        self,
        destination_table: Optional[str],
        *,
        if_exists: Optional[Literal["fail", "replace", "append"]] = None,
        index: bool = True,
        ordering_id: Optional[str] = None,
    ) -> str:
        """Write a DataFrame to a BigQuery table.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Write a DataFrame to a BigQuery table.

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> # destination_table = PROJECT_ID + "." + DATASET_ID + "." + TABLE_NAME
            >>> df.to_gbq("bigframes-dev.birds.test-numbers", if_exists="replace")
            'bigframes-dev.birds.test-numbers'

        Write a DataFrame to a temporary BigQuery table in the anonymous dataset.

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> destination = df.to_gbq(ordering_id="ordering_id")
            >>> # The table created can be read outside of the current session.
            >>> bpd.close_session()  # For demonstration, only.
            >>> bpd.read_gbq(destination, index_col="ordering_id")
                         col1  col2
            ordering_id
            0               1     3
            1               2     4
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            destination_table (Optional[str]):
                Name of table to be written, in the form ``dataset.tablename``
                or ``project.dataset.tablename``.

                If no ``destination_table`` is set, a new temporary table is
                created in the BigQuery anonymous dataset.

            if_exists (Optional[str]):
                Behavior when the destination table exists. When
                ``destination_table`` is set, this defaults to ``'fail'``. When
                ``destination_table`` is not set, this field is not applicable.
                A new table is always created. Value can be one of:

                ``'fail'``
                    If table exists raise pandas_gbq.gbq.TableCreationError.
                ``'replace'``
                    If table exists, drop it, recreate it, and insert data.
                ``'append'``
                    If table exists, insert data. Create if does not exist.

            index (bool. default True):
                whether write row names (index) or not.

            ordering_id (Optional[str], default None):
                If set, write the ordering of the DataFrame as a column in the
                result table with this name.

        Returns:
            str:
                The fully-qualified ID for the written table, in the form
                ``project.dataset.tablename``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_parquet(
        self,
        path: str,
        *,
        compression: Optional[Literal["snappy", "gzip"]] = "snappy",
        index: bool = True,
    ) -> None:
        """Write a DataFrame to the binary Parquet format.

        This function writes the dataframe as a `parquet file
        <https://parquet.apache.org/>`_ to Cloud Storage.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> gcs_bucket = "gs://bigframes-dev-testing/sample_parquet*.parquet"
            >>> df.to_parquet(path=gcs_bucket)

        Args:
            path (str):
                Destination URI(s) of Cloud Storage files(s) to store the extracted dataframe
                in format of ``gs://<bucket_name>/<object_name_or_glob>``.
                If the data size is more than 1GB, you must use a wildcard to export
                the data into multiple files and the size of the files varies.

            compression (str, default 'snappy'):
                Name of the compression to use. Use ``None`` for no compression.
                Supported options: ``'gzip'``, ``'snappy'``.

            index (bool, default True):
                If ``True``, include the dataframe's index(es) in the file output.
                If ``False``, they will not be written to the file.

        Returns:
            None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_dict(
        self,
        orient: Literal[
            "dict", "list", "series", "split", "tight", "records", "index"
        ] = "dict",
        into: type[dict] = dict,
        **kwargs,
    ) -> dict | list[dict]:
        """
        Convert the DataFrame to a dictionary.

        The type of the key-value pairs can be customized with the parameters
        (see below).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.to_dict()
            {'col1': {0: 1, 1: 2}, 'col2': {0: 3, 1: 4}}

        You can specify the return orientation.

            >>> df.to_dict('series')
            {'col1': 0    1
            1    2
            Name: col1, dtype: Int64,
            'col2': 0    3
            1    4
            Name: col2, dtype: Int64}

            >>> df.to_dict('split')
            {'index': [0, 1], 'columns': ['col1', 'col2'], 'data': [[1, 3], [2, 4]]}

            >>> df.to_dict("tight")
            {'index': [0, 1],
            'columns': ['col1', 'col2'],
            'data': [[1, 3], [2, 4]],
            'index_names': [None],
            'column_names': [None]}

        Args:
            orient (str {'dict', 'list', 'series', 'split', 'tight', 'records', 'index'}):
                Determines the type of the values of the dictionary.
                'dict' (default) : dict like {column -> {index -> value}}.
                'list' : dict like {column -> [values]}.
                'series' : dict like {column -> Series(values)}.
                split' : dict like {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}.
                'tight' : dict like {'index' -> [index], 'columns' -> [columns], 'data' -> [values],
                'index_names' -> [index.names], 'column_names' -> [column.names]}.
                'records' : list like [{column -> value}, ... , {column -> value}].
                'index' : dict like {index -> {column -> value}}.
            into (class, default dict):
                The collections.abc.Mapping subclass used for all Mappings
                in the return value.  Can be the actual class or an empty
                instance of the mapping type you want.  If you want a
                collections.defaultdict, you must pass it initialized.

            index (bool, default True):
                Whether to include the index item (and index_names item if `orient`
                is 'tight') in the returned dictionary. Can only be ``False``
                when `orient` is 'split' or 'tight'.

        Returns:
            dict or list of dict: Return a collections.abc.Mapping object representing the DataFrame.
            The resulting transformation depends on the `orient` parameter.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_excel(self, excel_writer, sheet_name: str = "Sheet1", **kwargs) -> None:
        """
        Write DataFrame to an Excel sheet.

        To write a single DataFrame to an Excel .xlsx file it is only necessary to
        specify a target file name. To write to multiple sheets it is necessary to
        create an `ExcelWriter` object with a target file name, and specify a sheet
        in the file to write to.

        Multiple sheets may be written to by specifying unique `sheet_name`.
        With all data written to the file it is necessary to save the changes.
        Note that creating an `ExcelWriter` object with a file name that already
        exists will result in the contents of the existing file being erased.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import tempfile
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.to_excel(tempfile.TemporaryFile())

        Args:
            excel_writer (path-like, file-like, or ExcelWriter object):
                File path or existing ExcelWriter.
            sheet_name (str, default 'Sheet1'):
                Name of sheet which will contain DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_latex(
        self, buf=None, columns=None, header=True, index=True, **kwargs
    ) -> str | None:
        r"""
        Render object to a LaTeX tabular, longtable, or nested table.

        Requires ``\usepackage{{booktabs}}``.  The output can be copy/pasted
        into a main LaTeX document or read from an external file
        with ``\input{{table.tex}}``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> print(df.to_latex())
            \begin{tabular}{lrr}
            \toprule
            & col1 & col2 \\
            \midrule
            0 & 1 & 3 \\
            1 & 2 & 4 \\
            \bottomrule
            \end{tabular}
            <BLANKLINE>

        Args:
            buf (str, Path or StringIO-like, optional, default None):
                Buffer to write to. If None, the output is returned as a string.
            columns (list of label, optional):
                The subset of columns to write. Writes all columns by default.
            header (bool or list of str, default True):
                Write out the column names. If a list of strings is given,
                it is assumed to be aliases for the column names.
            index (bool, default True):
                Write row names (index).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_records(
        self, index: bool = True, column_dtypes=None, index_dtypes=None
    ) -> np.recarray:
        """
        Convert DataFrame to a NumPy record array.

        Index will be included as the first field of the record array if
        requested.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.to_records()
            rec.array([(0, 1, 3), (1, 2, 4)],
                      dtype=[('index', 'O'), ('col1', 'O'), ('col2', 'O')])

        Args:
            index (bool, default True):
                Include index in resulting record array, stored in 'index'
                field or using the index label, if set.
            column_dtypes (str, type, dict, default None):
                If a string or type, the data type to store all columns. If
                a dictionary, a mapping of column names and indices (zero-indexed)
                to specific data types.
            index_dtypes (str, type, dict, default None):
                If a string or type, the data type to store all index levels. If
                a dictionary, a mapping of index level names and indices
                (zero-indexed) to specific data types.

                This mapping is applied only if `index=True`.

        Returns:
            np.recarray: NumPy ndarray with the DataFrame labels as fields and each row
            of the DataFrame as entries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_string(
        self,
        buf=None,
        columns: Sequence[str] | None = None,
        col_space=None,
        header: bool | Sequence[str] = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters=None,
        float_format=None,
        sparsify: bool | None = None,
        index_names: bool = True,
        justify: str | None = None,
        max_rows: int | None = None,
        max_cols: int | None = None,
        show_dimensions: bool = False,
        decimal: str = ".",
        line_width: int | None = None,
        min_rows: int | None = None,
        max_colwidth: int | None = None,
        encoding: str | None = None,
    ):
        """Render a DataFrame to a console-friendly tabular output.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> print(df.to_string())
               col1  col2
            0     1     3
            1     2     4

        Args:
            buf (str, Path or StringIO-like, optional, default None):
                Buffer to write to. If None, the output is returned as a string.
            columns (sequence, optional, default None):
                The subset of columns to write. Writes all columns by default.
            col_space (int, list or dict of int, optional):
                The minimum width of each column.
            header (bool or sequence, optional):
                Write out the column names. If a list of strings is given, it is assumed to be aliases for the column names.
            index (bool, optional, default True):
                Whether to print index (row) labels.
            na_rep (str, optional, default 'NaN'):
                String representation of NAN to use.
            formatters (list, tuple or dict of one-param. functions, optional):
                Formatter functions to apply to columns' elements by position or
                name.
                The result of each function must be a unicode string.
                List/tuple must be of length equal to the number of columns.
            float_format (one-parameter function, optional, default None):
                Formatter function to apply to columns' elements if they are
                floats. The result of this function must be a unicode string.
            sparsify (bool, optional, default True):
                Set to False for a DataFrame with a hierarchical index to print
                every multiindex key at each row.
            index_names (bool, optional, default True):
                Prints the names of the indexes.
            justify (str, default None):
                How to justify the column labels. If None uses the option from
                the print configuration (controlled by set_option), 'right' out
                of the box. Valid values are, 'left', 'right', 'center', 'justify',
                'justify-all', 'start', 'end', 'inherit', 'match-parent', 'initial',
                'unset'.
            max_rows (int, optional):
                Maximum number of rows to display in the console.
            min_rows (int, optional):
                The number of rows to display in the console in a truncated repr
                (when number of rows is above `max_rows`).
            max_cols (int, optional):
                Maximum number of columns to display in the console.
            show_dimensions (bool, default False):
                Display DataFrame dimensions (number of rows by number of columns).
            decimal (str, default '.'):
                Character recognized as decimal separator, e.g. ',' in Europe.
            line_width (int, optional):
                Width to wrap a line in characters.
            max_colwidth (int, optional):
                Max width to truncate each column in characters. By default, no limit.
            encoding (str, default "utf-8"):
                Set character encoding.

        Returns:
            str or None: If buf is None, returns the result as a string. Otherwise returns
            None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_markdown(
        self,
        buf=None,
        mode: str = "wt",
        index: bool = True,
        **kwargs,
    ):
        """Print DataFrame in Markdown-friendly format.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> print(df.to_markdown())
            |    |   col1 |   col2 |
            |---:|-------:|-------:|
            |  0 |      1 |      3 |
            |  1 |      2 |      4 |

        Args:
            buf (str, Path or StringIO-like, optional, default None):
                Buffer to write to. If None, the output is returned as a string.
            mode (str, optional):
                Mode in which file is opened.
            index (bool, optional, default True):
                Add index (row) labels.
            **kwargs
                These parameters will be passed to `tabulate <https://pypi.org/project/tabulate>`_.

        Returns:
            DataFrame in Markdown-friendly format.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_pickle(self, path, **kwargs) -> None:
        """Pickle (serialize) object to file.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> gcs_bucket = "gs://bigframes-dev-testing/sample_pickle_gcs.pkl"
            >>> df.to_pickle(path=gcs_bucket)

        Args:
            path (str):
                File path where the pickled object will be stored.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_orc(self, path=None, **kwargs) -> bytes | None:
        """
        Write a DataFrame to the ORC format.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> import tempfile
            >>> df.to_orc(tempfile.TemporaryFile())

        Args:
            path (str, file-like object or None, default None):
                If a string, it will be used as Root Directory path
                when writing a partitioned dataset. By file-like object,
                we refer to objects with a write() method, such as a file handle
                (e.g. via builtin open function). If path is None,
                a bytes object is returned.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Unsorted

    def equals(self, other) -> bool:
        """
        Test whether two objects contain the same elements.

        This function allows two Series or DataFrames to be compared against
        each other to see if they have the same shape and elements. NaNs in
        the same location are considered equal.

        The row/column index do not need to have the same type, as long
        as the values are considered equal. Corresponding columns must be of
        the same dtype.

        Args:
            other (Series or DataFrame):
                The other Series or DataFrame to be compared with the first.

        Returns:
            bool: True if all elements are the same in both objects, False
            otherwise.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def assign(self, **kwargs) -> DataFrame:
        r"""
        Assign new columns to a DataFrame.

        Returns a new object with all original columns in addition to new ones.
        Existing columns that are re-assigned will be overwritten.

        .. note::
            Assigning multiple columns within the same ``assign`` is possible.
            Later items in '\*\*kwargs' may refer to newly created or modified
            columns in 'df'; items are computed and assigned into 'df' in
            order.

        Args:
            kwargs:
                A dictionary of ``{str: values}``. The column names are
                keywords. If the values (e.g. a Series, scalar, or array), they
                are simply assigned to the column.

        Returns:
            bigframes.dataframe.DataFrame: A new DataFrame with the new columns
                in addition to all the existing columns.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Reindexing and alignment

    def reindex(
        self,
        labels=None,
        *,
        index=None,
        columns=None,
        axis=None,
    ):
        """Conform DataFrame to new index with optional filling logic.

        Places NA in locations having no value in the previous index. A new object
        is produced.

        Args:
            labels (array-like, optional):
                New labels / index to conform the axis specified by 'axis' to.
            index (array-like, optional):
                New labels for the index. Preferably an Index object to avoid
                duplicating data.
            columns (array-like, optional):
                New labels for the columns. Preferably an Index object to avoid
                duplicating data.
            axis (int or str, optional):
                Axis to target. Can be either the axis name ('index', 'columns')
                or number (0, 1).
        Returns:
            DataFrame: DataFrame with changed index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reindex_like(self, other):
        """Return an object with matching indices as other object.

        Conform the object to the same index on all axes. Optional
        filling logic, placing Null in locations having no value
        in the previous index.

        Args:
            other (Object of the same data type):
                Its row and column indices are used to define the new indices
                of this object.

        Returns:
            Series or DataFrame: Same type as caller, but with changed indices on each axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop(
        self, labels=None, *, axis=0, index=None, columns=None, level=None
    ) -> DataFrame | None:
        """Drop specified labels from columns.

        Remove columns by directly specifying column names.

        Args:
            labels:
                Index or column labels to drop.
            axis:
                Whether to drop labels from the index (0 or 'index') or
                columns (1 or 'columns').
            index:
                Alternative to specifying axis (``labels, axis=0``
                is equivalent to ``index=labels``).
            columns:
                Alternative to specifying axis (``labels, axis=1``
                is equivalent to ``columns=labels``).
            level:
                For MultiIndex, level from which the labels will be removed.
        Returns:
            bigframes.dataframe.DataFrame: DataFrame without the removed column labels.

        Raises:
            KeyError: If any of the labels is not found in the selected axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def align(
        self,
        other,
        join="outer",
        axis=None,
    ) -> tuple:
        """
        Align two objects on their axes with the specified join method.

        Join method is specified for each axis Index.


        Args:
            other (DataFrame or Series):
            join ({{'outer', 'inner', 'left', 'right'}}, default 'outer'):
                Type of alignment to be performed.
                left: use only keys from left frame, preserve key order.
                right: use only keys from right frame, preserve key order.
                outer: use union of keys from both frames, sort keys lexicographically.
                inner: use intersection of keys from both frames,
                preserve the order of the left keys.

            axis (allowed axis of the other object, default None):
                Align on index (0), columns (1), or both (None).

        Returns:
            tuple of (DataFrame, type of other): Aligned objects.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename(
        self,
        *,
        columns: Mapping,
    ) -> DataFrame:
        """Rename columns.

        Dict values must be unique (1-to-1). Labels not contained in a dict
        will be left as-is. Extra labels listed don't throw an error.

        Args:
            columns (Mapping):
                Dict-like from old column labels to new column labels.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame with the renamed axis labels.

        Raises:
            KeyError: If any of the labels is not found.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename_axis(self, mapper: Optional[str], **kwargs) -> DataFrame:
        """
        Set the name of the axis for the index.

        .. note::

            Currently only accepts a single string parameter (the new name of the index).

        Args:
            mapper str:
                Value to set the axis name attribute.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame with the new index name
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def set_index(
        self,
        keys,
        *,
        drop: bool = True,
    ) -> DataFrame | None:
        """
        Set the DataFrame index using existing columns.

        Set the DataFrame index (row labels) using one existing column. The
        index can replace the existing index.

        Args:
            keys:
                A label. This parameter can be a single column key.
            drop :
                Delete columns to be used as the new index.

        Returns:
            DataFrame: Changed row labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reorder_levels(
        self, order: Sequence[int | str], axis: str | int = 0
    ) -> DataFrame:
        """
        Rearrange index levels using input order. May not drop or duplicate levels.

        Args:
            order (list of int or list of str):
                List representing new level order. Reference level by number
                (position) or by key (label).
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                Where to reorder levels.

        Returns:
            DataFrame: DataFrame of rearranged index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def swaplevel(self, i, j, axis: str | int = 0) -> DataFrame:
        """
        Swap levels i and j in a :class:`MultiIndex`.

        Default is to swap the two innermost levels of the index.

        Args:
            i, j (int or str):
                Levels of the indices to be swapped. Can pass level name as string.
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                The axis to swap levels on. 0 or 'index' for row-wise, 1 or
                'columns' for column-wise.

        Returns:
            DataFrame: DataFrame with levels swapped in MultiIndex.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def droplevel(self, level, axis: str | int = 0):
        """
        Return DataFrame with requested index / column level(s) removed.

        Args:
            level (int, str, or list-like):
                If a string is given, must be the name of a level
                If list-like, elements must be names or positional indexes
                of levels.
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                Axis along which the level(s) is removed:

                * 0 or 'index': remove level(s) in column.
                * 1 or 'columns': remove level(s) in row.
        Returns:
            DataFrame: DataFrame with requested index / column level(s) removed.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reset_index(
        self,
        *,
        drop: bool = False,
    ) -> DataFrame | None:
        """Reset the index.

        Reset the index of the DataFrame, and use the default one instead.

        Args:
            drop (bool, default False):
                Do not try to insert index into dataframe columns. This resets
                the index to the default integer index.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame with the new index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop_duplicates(
        self,
        *,
        keep="first",
    ) -> DataFrame:
        """
        Return DataFrame with duplicate rows removed.

        Considering certain columns is optional. Indexes, including time indexes
        are ignored.

        Args:
            subset (column label or sequence of labels, optional):
                Only consider certain columns for identifying duplicates, by
                default use all of the columns.
            keep ({'first', 'last', ``False``}, default 'first'):
                Determines which duplicates (if any) to keep.

                - 'first' : Drop duplicates except for the first occurrence.
                - 'last' : Drop duplicates except for the last occurrence.
                - ``False`` : Drop all duplicates.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame with duplicates removed
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def duplicated(self, subset=None, keep="first"):
        """
        Return boolean Series denoting duplicate rows.

        Considering certain columns is optional.

        Args:
            subset (column label or sequence of labels, optional):
                Only consider certain columns for identifying duplicates, by
                default use all of the columns.
            keep ({'first', 'last', False}, default 'first'):
                Determines which duplicates (if any) to mark.

                - ``first`` : Mark duplicates as ``True`` except for the first occurrence.
                - ``last`` : Mark duplicates as ``True`` except for the last occurrence.
                - False : Mark all duplicates as ``True``.

        Returns:
            bigframes.series.Series: Boolean series for each duplicated rows.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Reindex-based selection methods

    def dropna(
        self,
    ) -> DataFrame:
        """Remove missing values.

        Args:
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Determine if rows or columns which contain missing values are
                removed.

                * 0, or 'index' : Drop rows which contain missing values.
                * 1, or 'columns' : Drop columns which contain missing value.
            how ({'any', 'all'}, default 'any'):
                Determine if row or column is removed from DataFrame, when we have
                at least one NA or all NA.

                * 'any' : If any NA values are present, drop that row or column.
                * 'all' : If all values are NA, drop that row or column.
            ignore_index (bool, default ``False``):
                If ``True``, the resulting axis will be labeled 0, 1, …, n - 1.


        Returns:
            bigframes.dataframe.DataFrame: DataFrame with NA entries dropped from it.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isin(self, values):
        """
        Whether each element in the DataFrame is contained in values.

        Args:
            values (iterable, or dict):
                The result will only be true at a location if all the
                labels match. If `values` is a dict, the keys must be
                the column names, which must match.

        Returns:
            DataFrame: DataFrame of booleans showing whether each element
            in the DataFrame is contained in values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def keys(self):
        """
        Get the 'info axis'.

        This is index for Series, columns for DataFrame.

        Returns:
            Index: Info axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df.keys()
            Index(['A', 'B'], dtype='object')
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def iterrows(self):
        """
        Iterate over DataFrame rows as (index, Series) pairs.

        Yields:
            a tuple (index, data) where data contains row values as a Series

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> index, row = next(df.iterrows())
            >>> index
            0
            >>> row
            A    1
            B    4
            Name: 0, dtype: object
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def itertuples(self, index: bool = True, name: str | None = "Pandas"):
        """
        Iterate over DataFrame rows as namedtuples.

        Args:
            index (bool, default True):
                If True, return the index as the first element of the tuple.
            name (str or None, default "Pandas"):
                The name of the returned namedtuples or None to return regular
                tuples.

        Returns:
            iterator:
                An object to iterate over namedtuples for each row in the
                DataFrame with the first field possibly being the index and
                following fields being the column values.


        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> next(df.itertuples(name="Pair"))
            Pair(Index=0, A=1, B=4)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def items(self):
        """
        Iterate over (column name, Series) pairs.

        Iterates over the DataFrame columns, returning a tuple with
        the column name and the content as a Series.

        Returns:
            Iterator: Iterator of label, Series for each column.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Sorting

    def sort_values(
        self,
        by: str | Sequence[str],
        *,
        ascending: bool | Sequence[bool] = True,
        kind: str = "quicksort",
        na_position="last",
    ) -> DataFrame:
        """Sort by the values along row axis.

        Args:
            by (str or Sequence[str]):
                Name or list of names to sort by.
            ascending (bool or Sequence[bool], default True):
                Sort ascending vs. descending. Specify list for multiple sort
                orders.  If this is a list of bools, must match the length of
                the by.
            kind (str, default 'quicksort'):
                Choice of sorting algorithm. Accepts 'quicksort', 'mergesort',
                'heapsort', 'stable'. Ignored except when determining whether to
                sort stably. 'mergesort' or 'stable' will result in stable reorder.
            na_position ({'first', 'last'}, default `last`):
             ``{'first', 'last'}``, default 'last' Puts NaNs at the beginning
             if `first`; `last` puts NaNs at the end.

        Returns:
            DataFrame with sorted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sort_index(
        self,
    ) -> DataFrame:
        """Sort object by labels (along an axis).

        Returns:
            The original DataFrame sorted by the labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Arithmetic Methods

    def eq(self, other, axis: str | int = "columns") -> DataFrame:
        """
        Get equal to of DataFrame and other, element-wise (binary operator `eq`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can use method name:

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].eq(360)
            circle        True
            triangle     False
            rectangle     True
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``==``:
            >>> df["degrees"] == 360
            circle        True
            triangle     False
            rectangle     True
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            Result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ne(self, other, axis: str | int = "columns") -> DataFrame:
        """
        Get not equal to of DataFrame and other, element-wise (binary operator `ne`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can use method name:

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].ne(360)
            circle       False
            triangle      True
            rectangle    False
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``!=``:

            >>> df["degrees"] != 360
            circle       False
            triangle      True
            rectangle    False
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').
        Returns:
            DataFrame: Result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def le(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'less than or equal to' of dataframe and other, element-wise (binary operator `<=`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        .. note::
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can use method name:

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].le(180)
            circle       False
            triangle      True
            rectangle    False
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``<=``:

            >>> df["degrees"] <= 180
            circle       False
            triangle      True
            rectangle    False
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame: DataFrame of bool. The result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lt(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'less than' of DataFrame and other, element-wise (binary operator `<`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        .. note::
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can use method name:

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].lt(180)
            circle       False
            triangle     False
            rectangle    False
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``<``:

            >>> df["degrees"] < 180
            circle       False
            triangle     False
            rectangle    False
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame: DataFrame of bool. The result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ge(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'greater than or equal to' of DataFrame and other, element-wise (binary operator `>=`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        .. note::
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can use method name:

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].ge(360)
            circle        True
            triangle     False
            rectangle     True
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``>=``:

            >>> df["degrees"] >= 360
            circle        True
            triangle     False
            rectangle     True
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame: DataFrame of bool. The result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def gt(self, other, axis: str | int = "columns") -> DataFrame:
        """Get 'greater than' of DataFrame and other, element-wise (binary operator `>`).

        Among flexible wrappers (`eq`, `ne`, `le`, `lt`, `ge`, `gt`) to comparison
        operators.

        Equivalent to `==`, `!=`, `<=`, `<`, `>=`, `>` with support to choose axis
        (rows or columns) and level for comparison.

        .. note::
            Mismatched indices will be unioned together. `NaN` values in
            floating point columns are considered different
            (i.e. `NaN` != `NaN`).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'angles': [0, 3, 4],
            ...        'degrees': [360, 180, 360]},
            ...       index=['circle', 'triangle', 'rectangle'])
            >>> df["degrees"].gt(360)
            circle       False
            triangle     False
            rectangle    False
            Name: degrees, dtype: boolean

        You can also use arithmetic operator ``>``:

            >>> df["degrees"] > 360
            circle       False
            triangle     False
            rectangle    False
            Name: degrees, dtype: boolean

        Args:
            other (scalar, sequence, Series, or DataFrame):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}, default 'columns'):
                Whether to compare by the index (0 or 'index') or columns
                (1 or 'columns').

        Returns:
            DataFrame: DataFrame of bool: The result of the comparison.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def add(self, other, axis: str | int = "columns") -> DataFrame:
        """Get addition of DataFrame and other, element-wise (binary operator `+`).

        Equivalent to ``dataframe + other``. With reverse version, `radd`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].add(df['B'])
            0    5
            1    7
            2    9
            dtype: Int64

        You can also use arithmetic operator ``+``:

            >>> df['A'] + (df['B'])
            0    5
            1    7
            2    9
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sub(self, other, axis: str | int = "columns") -> DataFrame:
        """Get subtraction of DataFrame and other, element-wise (binary operator `-`).

        Equivalent to ``dataframe - other``. With reverse version, `rsub`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].sub(df['B'])
            0    -3
            1    -3
            2    -3
            dtype: Int64

        You can also use arithmetic operator ``-``:

            >>> df['A'] - (df['B'])
            0    -3
            1    -3
            2    -3
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rsub(self, other, axis: str | int = "columns") -> DataFrame:
        """Get subtraction of DataFrame and other, element-wise (binary operator `-`).

        Equivalent to ``other - dataframe``. With reverse version, `sub`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df['A'].rsub(df['B'])
            0    3
            1    3
            2    3
            dtype: Int64

        It's equivalent to using arithmetic operator: ``-``:

            >>> df['B'] - (df['A'])
            0    3
            1    3
            2    3
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mul(self, other, axis: str | int = "columns") -> DataFrame:
        """Get multiplication of DataFrame and other, element-wise (binary operator `*`).

        Equivalent to ``dataframe * other``. With reverse version, `rmul`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].mul(df['B'])
            0     4
            1    10
            2    18
            dtype: Int64

        You can also use arithmetic operator ``*``:

            >>> df['A'] * (df['B'])
            0     4
            1    10
            2    18
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def truediv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get floating division of DataFrame and other, element-wise (binary operator `/`).

        Equivalent to ``dataframe / other``. With reverse version, `rtruediv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].truediv(df['B'])
            0    0.25
            1     0.4
            2     0.5
            dtype: Float64

        You can also use arithmetic operator ``/``:

            >>> df['A'] / (df['B'])
            0    0.25
            1     0.4
            2     0.5
            dtype: Float64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rtruediv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get floating division of DataFrame and other, element-wise (binary operator `/`).

        Equivalent to ``other / dataframe``. With reverse version, `truediv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df['A'].rtruediv(df['B'])
            0    4.0
            1    2.5
            2    2.0
            dtype: Float64

        It's equivalent to using arithmetic operator: ``/``:

            >>> df['B'] / (df['A'])
            0    4.0
            1    2.5
            2    2.0
            dtype: Float64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def floordiv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get integer division of DataFrame and other, element-wise (binary operator `//`).

        Equivalent to ``dataframe // other``. With reverse version, `rfloordiv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].floordiv(df['B'])
            0    0
            1    0
            2    0
            dtype: Int64

        You can also use arithmetic operator ``//``:

            >>> df['A'] // (df['B'])
            0    0
            1    0
            2    0
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rfloordiv(self, other, axis: str | int = "columns") -> DataFrame:
        """Get integer division of DataFrame and other, element-wise (binary operator `//`).

        Equivalent to ``other // dataframe``. With reverse version, `rfloordiv`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df['A'].rfloordiv(df['B'])
            0    4
            1    2
            2    2
            dtype: Int64

        It's equivalent to using arithmetic operator: ``//``:

            >>> df['B'] // (df['A'])
            0    4
            1    2
            2    2
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mod(self, other, axis: str | int = "columns") -> DataFrame:
        """Get modulo of DataFrame and other, element-wise (binary operator `%`).

        Equivalent to ``dataframe % other``. With reverse version, `rmod`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].mod(df['B'])
            0    1
            1    2
            2    3
            dtype: Int64

        You can also use arithmetic operator ``%``:

            >>> df['A'] % (df['B'])
            0    1
            1    2
            2    3
            dtype: Int64

        Args:
            other:
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rmod(self, other, axis: str | int = "columns") -> DataFrame:
        """Get modulo of DataFrame and other, element-wise (binary operator `%`).

        Equivalent to ``other % dataframe``. With reverse version, `mod`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df['A'].rmod(df['B'])
            0    0
            1    1
            2    0
            dtype: Int64

        It's equivalent to using arithmetic operator: ``%``:

            >>> df['B'] % (df['A'])
            0    0
            1    1
            2    0
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pow(self, other, axis: str | int = "columns") -> DataFrame:
        """Get Exponential power of dataframe and other, element-wise (binary operator `**`).

        Equivalent to ``dataframe ** other``, but with support to substitute a fill_value
        for missing data in one of the inputs. With reverse version, `rpow`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })

        You can use method name:

            >>> df['A'].pow(df['B'])
            0      1
            1     32
            2    729
            dtype: Int64

        You can also use arithmetic operator ``**``:

            >>> df['A'] ** (df['B'])
            0      1
            1     32
            2    729
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rpow(self, other, axis: str | int = "columns") -> DataFrame:
        """Get Exponential power of dataframe and other, element-wise (binary operator `rpow`).

        Equivalent to ``other ** dataframe``, but with support to substitute a fill_value
        for missing data in one of the inputs. With reverse version, `pow`.

        Among flexible wrappers (`add`, `sub`, `mul`, `div`, `mod`, `pow`) to
        arithmetic operators: `+`, `-`, `*`, `/`, `//`, `%`, `**`.

        .. note::
            Mismatched indices will be unioned together.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     })
            >>> df['A'].rpow(df['B'])
            0      4
            1     25
            2    216
            dtype: Int64

        It's equivalent to using arithmetic operator: ``**``:

            >>> df['B'] ** (df['A'])
            0      4
            1     25
            2    216
            dtype: Int64

        Args:
            other (float, int, or Series):
                Any single or multiple element data structure, or list-like object.
            axis ({0 or 'index', 1 or 'columns'}):
                Whether to compare by the index (0 or 'index') or columns.
                (1 or 'columns'). For Series input, axis to match Series index on.

        Returns:
            DataFrame: DataFrame result of the arithmetic operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def combine(
        self, other, func, fill_value=None, overwrite: bool = True
    ) -> DataFrame:
        """Perform column-wise combine with another DataFrame.

        Combines a DataFrame with `other` DataFrame using `func`
        to element-wise combine columns. The row and column indexes of the
        resulting DataFrame will be the union of the two.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df1 = bpd.DataFrame({'A': [0, 0], 'B': [4, 4]})
            >>> df2 = bpd.DataFrame({'A': [1, 1], 'B': [3, 3]})
            >>> take_smaller = lambda s1, s2: s1 if s1.sum() < s2.sum() else s2
            >>> df1.combine(df2, take_smaller)
               A  B
            0  0  3
            1  0  3
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            other (DataFrame):
                The DataFrame to merge column-wise.
            func (function):
                Function that takes two series as inputs and return a Series or a
                scalar. Used to merge the two dataframes column by columns.
            fill_value (scalar value, default None):
                The value to fill NaNs with prior to passing any column to the
                merge func.
            overwrite (bool, default True):
                If True, columns in `self` that do not exist in `other` will be
                overwritten with NaNs.

        Returns:
            DataFrame: Combination of the provided DataFrames.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def combine_first(self, other) -> DataFrame:
        """
        Update null elements with value in the same location in `other`.

        Combine two DataFrame objects by filling null values in one DataFrame
        with non-null values from other DataFrame. The row and column indexes
        of the resulting DataFrame will be the union of the two. The resulting
        dataframe contains the 'first' dataframe values and overrides the
        second one values where both first.loc[index, col] and
        second.loc[index, col] are not missing values, upon calling
        first.combine_first(second).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df1 = bpd.DataFrame({'A': [None, 0], 'B': [None, 4]})
            >>> df2 = bpd.DataFrame({'A': [1, 1], 'B': [3, 3]})
            >>> df1.combine_first(df2)
                 A    B
            0  1.0  3.0
            1  0.0  4.0
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            other (DataFrame):
                Provided DataFrame to use to fill null values.

        Returns:
            DataFrame: The result of combining the provided DataFrame with the other object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def update(
        self, other, join: str = "left", overwrite: bool = True, filter_func=None
    ) -> DataFrame:
        """
        Modify in place using non-NA values from another DataFrame.

        Aligns on indices. There is no return value.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'A': [1, 2, 3],
            ...                    'B': [400, 500, 600]})
            >>> new_df = bpd.DataFrame({'B': [4, 5, 6],
            ...                        'C': [7, 8, 9]})
            >>> df.update(new_df)
            >>> df
               A  B
            0  1  4
            1  2  5
            2  3  6
            <BLANKLINE>
            [3 rows x 2 columns]

        Args:
            other (DataFrame, or object coercible into a DataFrame):
                Should have at least one matching index/column label
                with the original DataFrame. If a Series is passed,
                its name attribute must be set, and that will be
                used as the column name to align with the original DataFrame.
            join ({'left'}, default 'left'):
                Only left join is implemented, keeping the index and columns of the
                original object.
            overwrite (bool, default True):
                How to handle non-NA values for overlapping keys:
                True: overwrite original DataFrame's values
                with values from `other`.
                False: only update values that are NA in
                the original DataFrame.

            filter_func (callable(1d-array) -> bool 1d-array, optional):
                Can choose to replace values other than NA. Return True for values
                that should be updated.

        Returns:
            None: This method directly changes calling object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Data reshaping

    def groupby(
        self,
        by: Union[str, Sequence[str]],
        *,
        level=None,
        as_index: bool = True,
        dropna: bool = True,
    ):
        """Group DataFrame by columns.

        A groupby operation involves some combination of splitting the
        object, applying a function, and combining the results. This can be
        used to group large amounts of data and compute operations on these
        groups.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'Animal': ['Falcon', 'Falcon',
            ...                                'Parrot', 'Parrot'],
            ...                     'Max Speed': [380., 370., 24., 26.]})
            >>> df
               Animal  Max Speed
            0  Falcon      380.0
            1  Falcon      370.0
            2  Parrot       24.0
            3  Parrot       26.0
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> df.groupby(['Animal'])['Max Speed'].mean()
            Animal
            Falcon    375.0
            Parrot     25.0
            Name: Max Speed, dtype: Float64

        We can also choose to include NA in group keys or not by setting `dropna`:

            >>> df = bpd.DataFrame([[1, 2, 3],[1, None, 4], [2, 1, 3], [1, 2, 2]],
            ...                    columns=["a", "b", "c"])
            >>> df.groupby(by=["b"]).sum()
                 a  c
            b
            1.0  2  3
            2.0  2  5
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df.groupby(by=["b"], dropna=False).sum()
                  a  c
            b
            1.0   2  3
            2.0   2  5
            <NA>  1  4
            <BLANKLINE>
            [3 rows x 2 columns]

        We can also choose to return object with group labels or not by setting `as_index`:

            >>> df.groupby(by=["b"], as_index=False).sum()
                 b  a  c
            0  1.0  2  3
            1  2.0  2  5
            <BLANKLINE>
            [2 rows x 3 columns]

        Args:
            by (str, Sequence[str]):
                A label or list of labels may be passed to group by the columns
                in ``self``. Notice that a tuple is interpreted as a (single)
                key.
            level (int, level name, or sequence of such, default None):
                If the axis is a MultiIndex (hierarchical), group by a particular
                level or levels. Do not specify both ``by`` and ``level``.
            as_index (bool, default True):
                Default True. Return object with group labels as the index.
                Only relevant for DataFrame input. ``as_index=False`` is
                effectively "SQL-style" grouped output. This argument has no
                effect on filtrations such as ``head()``, ``tail()``, ``nth()``
                and in transformations.
            dropna (bool, default True):
                Default True. If True, and if group keys contain NA values, NA
                values together with row/column will be dropped. If False, NA
                values will also be treated as the key in groups.

        Returns:
            bigframes.core.groupby.SeriesGroupBy: A groupby object that contains information about the groups.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Function application

    def map(self, func, na_action: Optional[str] = None) -> DataFrame:
        """Apply a function to a Dataframe elementwise.

        This method applies a function that accepts and returns a scalar
        to every element of a DataFrame.

        .. note::

           In pandas 2.1.0, DataFrame.applymap is deprecated and renamed to
           DataFrame.map.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Let's use ``reuse=False`` flag to make sure a new ``remote_function``
        is created every time we run the following code, but you can skip it
        to potentially reuse a previously deployed ``remote_function`` from
        the same user defined function.

            >>> @bpd.remote_function([int], float, reuse=False)
            ... def minutes_to_hours(x):
            ...     return x/60

            >>> df_minutes = bpd.DataFrame(
            ...     {"system_minutes" : [0, 30, 60, 90, 120],
            ...      "user_minutes" : [0, 15, 75, 90, 6]})
            >>> df_minutes
            system_minutes  user_minutes
            0               0             0
            1              30            15
            2              60            75
            3              90            90
            4             120             6
            <BLANKLINE>
            [5 rows x 2 columns]

            >>> df_hours = df_minutes.map(minutes_to_hours)
            >>> df_hours
            system_minutes  user_minutes
            0             0.0           0.0
            1             0.5          0.25
            2             1.0          1.25
            3             1.5           1.5
            4             2.0           0.1
            <BLANKLINE>
            [5 rows x 2 columns]

        If there are ``NA``/``None`` values in the data, you can ignore
        applying the remote function on such values by specifying
        ``na_action='ignore'``.

            >>> df_minutes = bpd.DataFrame(
            ...     {
            ...         "system_minutes" : [0, 30, 60, None, 90, 120, bpd.NA],
            ...         "user_minutes" : [0, 15, 75, 90, 6, None, bpd.NA]
            ...     }, dtype="Int64")
            >>> df_hours = df_minutes.map(minutes_to_hours, na_action='ignore')
            >>> df_hours
            system_minutes  user_minutes
            0             0.0           0.0
            1             0.5          0.25
            2             1.0          1.25
            3            <NA>           1.5
            4             1.5           0.1
            5             2.0          <NA>
            6            <NA>          <NA>
            <BLANKLINE>
            [7 rows x 2 columns]

        Args:
            func (function):
                Python function wrapped by ``remote_function`` decorator,
                returns a single value from a single value.
            na_action (Optional[str], default None):
                ``{None, 'ignore'}``, default None. If `ignore`, propagate NaN
                values, without passing them to func.

        Returns:
            bigframes.dataframe.DataFrame: Transformed DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Merging / joining methods

    def join(self, other, *, on: Optional[str] = None, how: str) -> DataFrame:
        """Join columns of another DataFrame.

        Join columns with `other` DataFrame on index

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Join two DataFrames by specifying how to handle the operation:

            >>> df1 = bpd.DataFrame({'col1': ['foo', 'bar'], 'col2': [1, 2]}, index=[10, 11])
            >>> df1
               col1  col2
            10  foo     1
            11  bar     2
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df2 = bpd.DataFrame({'col3': ['foo', 'baz'], 'col4': [3, 4]}, index=[11, 22])
            >>> df2
               col3  col4
            11  foo     3
            22  baz     4
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df1.join(df2)
               col1  col2  col3  col4
            10  foo     1  <NA>  <NA>
            11  bar     2   foo     3
            <BLANKLINE>
            [2 rows x 4 columns]

            >>> df1.join(df2, how="left")
               col1  col2  col3  col4
            10  foo     1  <NA>  <NA>
            11  bar     2   foo     3
            <BLANKLINE>
            [2 rows x 4 columns]

            >>> df1.join(df2, how="right")
                col1  col2 col3  col4
            11  bar      2  foo     3
            22  <NA>  <NA>  baz     4
            <BLANKLINE>
            [2 rows x 4 columns]

            >>> df1.join(df2, how="outer")
                col1  col2  col3  col4
            10   foo     1  <NA>  <NA>
            11   bar     2   foo     3
            22  <NA>  <NA>   baz     4
            <BLANKLINE>
            [3 rows x 4 columns]

            >>> df1.join(df2, how="inner")
               col1  col2 col3  col4
            11  bar     2  foo     3
            <BLANKLINE>
            [1 rows x 4 columns]


        Another option to join using the key columns is to use the on parameter:

            >>> df1.join(df2, on="col1", how="right")
                  col1  col2 col3  col4
            <NA>    11  <NA>  foo     3
            <NA>    22  <NA>  baz     4
            <BLANKLINE>
            [2 rows x 4 columns]

        Args:
            other:
                DataFrame with an Index similar to the Index of this one.
            on:
                Column in the caller to join on the index in other, otherwise
                joins index-on-index. Like an Excel VLOOKUP operation.
            how ({'left', 'right', 'outer', 'inner'}, default 'left'`):
                How to handle the operation of the two objects.
                ``left``: use calling frame's index (or column if on is specified)
                ``right``: use `other`'s index. ``outer``: form union of calling
                frame's index (or column if on is specified) with `other`'s index,
                and sort it lexicographically. ``inner``: form intersection of
                calling frame's index (or column if on is specified) with `other`'s
                index, preserving the order of the calling's one.
                ``cross``: creates the cartesian product from both frames, preserves
                the order of the left keys.

        Returns:
            bigframes.dataframe.DataFrame: A dataframe containing columns from both the caller and `other`.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def merge(
        self,
        right,
        how: Literal[
            "inner",
            "left",
            "outer",
            "right",
            "cross",
        ] = "inner",
        on: Optional[str] = None,
        *,
        left_on: Optional[str] = None,
        right_on: Optional[str] = None,
        sort: bool = False,
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> DataFrame:
        """Merge DataFrame objects with a database-style join.

        The join is done on columns or indexes. If joining columns on
        columns, the DataFrame indexes *will be ignored*. Otherwise if joining indexes
        on indexes or indexes on a column or columns, the index will be passed on.
        When performing a cross merge, no column specifications to merge on are
        allowed.

        .. warning::
            If both key columns contain rows where the key is a null value, those
            rows will be matched against each other. This is different from usual SQL
            join behaviour and can lead to unexpected results.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Merge DataFrames df1 and df2 by specifiying type of merge:

            >>> df1 = bpd.DataFrame({'a': ['foo', 'bar'], 'b': [1, 2]})
            >>> df1
                 a  b
            0  foo  1
            1  bar  2
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df2 = bpd.DataFrame({'a': ['foo', 'baz'], 'c': [3, 4]})
            >>> df2
                 a  c
            0  foo  3
            1  baz  4
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df1.merge(df2, how="inner", on="a")
                 a  b  c
            0  foo  1  3
            <BLANKLINE>
            [1 rows x 3 columns]

            >>> df1.merge(df2, how='left', on='a')
                 a  b     c
            0  foo  1     3
            1  bar  2  <NA>
            <BLANKLINE>
            [2 rows x 3 columns]

        Merge df1 and df2 on the lkey and rkey columns. The value columns have
        the default suffixes, _x and _y, appended.

            >>> df1 = bpd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
            ...                     'value': [1, 2, 3, 5]})
            >>> df1
              lkey  value
            0  foo      1
            1  bar      2
            2  baz      3
            3  foo      5
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> df2 = bpd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
            ...                     'value': [5, 6, 7, 8]})
            >>> df2
              rkey  value
            0  foo      5
            1  bar      6
            2  baz      7
            3  foo      8
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> df1.merge(df2, left_on='lkey', right_on='rkey')
              lkey  value_x rkey  value_y
            0  foo        1  foo        5
            1  foo        1  foo        8
            2  bar        2  bar        6
            3  baz        3  baz        7
            4  foo        5  foo        5
            5  foo        5  foo        8
            <BLANKLINE>
            [6 rows x 4 columns]

        Args:
            right:
                Object to merge with.
            how:
                ``{'left', 'right', 'outer', 'inner'}, default 'inner'``
                Type of merge to be performed.
                ``left``: use only keys from left frame, similar to a SQL left outer join;
                preserve key order.
                ``right``: use only keys from right frame, similar to a SQL right outer join;
                preserve key order.
                ``outer``: use union of keys from both frames, similar to a SQL full outer
                join; sort keys lexicographically.
                ``inner``: use intersection of keys from both frames, similar to a SQL inner
                join; preserve the order of the left keys.
                ``cross``: creates the cartesian product from both frames, preserves the order
                of the left keys.

            on (label or list of labels):
                Columns to join on. It must be found in both DataFrames. Either on or left_on + right_on
                must be passed in.
            left_on (label or list of labels):
                Columns to join on in the left DataFrame. Either on or left_on + right_on
                must be passed in.
            right_on (label or list of labels):
                Columns to join on in the right DataFrame. Either on or left_on + right_on
                must be passed in.
            sort:
                Default False. Sort the join keys lexicographically in the
                result DataFrame. If False, the order of the join keys depends
                on the join type (how keyword).
            suffixes:
                Default ``("_x", "_y")``. A length-2 sequence where each
                element is optionally a string indicating the suffix to add to
                overlapping column names in `left` and `right` respectively.
                Pass a value of `None` instead of a string to indicate that the
                column name from `left` or `right` should be left as-is, with
                no suffix. At least one of the values must not be None.

        Returns:
            bigframes.dataframe.DataFrame: A DataFrame of the two merged objects.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def apply(self, func, *, args=(), **kwargs):
        """Apply a function along an axis of the DataFrame.

        Objects passed to the function are Series objects whose index is
        the DataFrame's index (``axis=0``) the final return type
        is inferred from the return type of the applied function.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df
            col1	col2
            0	1	3
            1	2	4
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> def sqaure(x):
            ...     return x * x
            >>> df1 = df.apply(sqaure)
            >>> df
               col1  col2
            0     1     3
            1     2     4
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            func (function):
                Function to apply to each column or row.
            args (tuple):
                Positional arguments to pass to `func` in addition to the
                array/series.
            **kwargs:
                Additional keyword arguments to pass as keywords arguments to
                `func`.

        Returns:
            pandas.Series or bigframes.DataFrame: Result of applying ``func`` along the given axis of the DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # ndarray-like stats methods

    def any(self, *, axis=0, bool_only: bool = False):
        """
        Return whether any element is True, potentially over an axis.

        Returns False unless there is at least one element within a series or
        along a Dataframe axis that is True or equivalent (e.g. non-zero or
        non-empty).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [True, True], "B": [False, False]})
            >>> df
                    A        B
            0    True    False
            1    True    False
            <BLANKLINE>
            [2 rows x 2 columns]

        Checking if each column contains at least one True element(the default behavior without an explicit axis parameter):

            >>> df.any()
            A     True
            B    False
            dtype: boolean

        Checking if each row contains at least one True element:

            >>> df.any(axis=1)
            0    True
            1    True
            dtype: boolean

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            bool_only (bool. default False):
                Include only boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def all(self, axis=0, *, bool_only: bool = False):
        """
        Return whether all elements are True, potentially over an axis.

        Returns True unless there at least one element within a Series or
        along a DataFrame axis that is False or equivalent (e.g. zero or
        empty).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [True, True], "B": [False, False]})
            >>> df
                    A        B
            0    True    False
            1    True    False
            <BLANKLINE>
            [2 rows x 2 columns]

        Checking if all values in each column are True(the default behavior without an explicit axis parameter):

            >>> df.all()
            A     True
            B    False
            dtype: boolean

        Checking across rows to see if all values are True:

            >>> df.all(axis=1)
            0    False
            1    False
            dtype: boolean

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            bool_only (bool. default False):
                Include only boolean columns.

        Returns:
            bigframes.series.Series: Series if all elements are True.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def prod(self, axis=0, *, numeric_only: bool = False):
        """
        Return the product of the values over the requested axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 2, 3], "B": [4.5, 5.5, 6.5]})
            >>> df
                A    B
            0   1  4.5
            1   2  5.5
            2   3  6.5
            <BLANKLINE>
            [3 rows x 2 columns]

        Calculating the product of each column(the default behavior without an explicit axis parameter):

            >>> df.prod()
            A        6.0
            B    160.875
            dtype: Float64

        Calculating the product of each row:

            >>> df.prod(axis=1)
            0     4.5
            1    11.0
            2    19.5
            dtype: Float64

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool. default False):
                Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with the product of the values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(self, axis=0, *, numeric_only: bool = False):
        """Return the minimum of the values over the requested axis.

        If you want the *index* of the minimum, use ``idxmin``. This is the
        equivalent of the ``numpy.ndarray`` method ``argmin``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Finding the minimum value in each column (the default behavior without an explicit axis parameter).

            >>> df.min()
            A    1.0
            B    2.0
            dtype: Float64

        Finding the minimum value in each row.

            >>> df.min(axis=1)
            0    1.0
            1    3.0
            dtype: Float64

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool, default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with the minimum of the values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(self, axis=0, *, numeric_only: bool = False):
        """Return the maximum of the values over the requested axis.

        If you want the *index* of the maximum, use ``idxmax``. This is
        the equivalent of the ``numpy.ndarray`` method ``argmax``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Finding the maximum value in each column (the default behavior without an explicit axis parameter).

            >>> df.max()
            A    3.0
            B    4.0
            dtype: Float64

        Finding the maximum value in each row.

            >>> df.max(axis=1)
            0    2.0
            1    4.0
            dtype: Float64

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series after the maximum of values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(self, axis=0, *, numeric_only: bool = False):
        """Return the sum of the values over the requested axis.

        This is equivalent to the method ``numpy.sum``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Calculating the sum of each column (the default behavior without an explicit axis parameter).

            >>> df.sum()
            A    4.0
            B    6.0
            dtype: Float64

        Calculating the sum of each row.

            >>> df.sum(axis=1)
            0    3.0
            1    7.0
            dtype: Float64

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with the sum of values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(self, axis=0, *, numeric_only: bool = False):
        """Return the mean of the values over the requested axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Calculating the mean of each column (the default behavior without an explicit axis parameter).

            >>> df.mean()
            A    2.0
            B    3.0
            dtype: Float64

        Calculating the mean of each row.

            >>> df.mean(axis=1)
            0    1.5
            1    3.5
            dtype: Float64

        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with the mean of values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def median(self, *, numeric_only: bool = False, exact: bool = False):
        """Return the median of the values over colunms.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Finding the median value of each column.

            >>> df.median()
            A    1.0
            B    2.0
            dtype: Float64

        Args:
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.
            exact (bool. default False):
                Default False. Get the exact median instead of an approximate
                one. Note: ``exact=True`` not yet supported.

        Returns:
            bigframes.series.Series: Series with the median of values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(self, axis=0, *, numeric_only: bool = False):
        """Return unbiased variance over requested axis.

        Normalized by N-1 by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 3], "B": [2, 4]})
            >>> df
                A	B
            0	1	2
            1	3	4
            <BLANKLINE>
            [2 rows x 2 columns]

        Calculating the variance of each column (the default behavior without an explicit axis parameter).

            >>> df.var()
            A    2.0
            B    2.0
            dtype: Float64

        Calculating the variance of each row.

            >>> df.var(axis=1)
            0    0.5
            1    0.5
            dtype: Float64


        Args:
            axis ({index (0), columns (1)}):
                Axis for the function to be applied on.
                For Series this parameter is unused and defaults to 0.
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with unbiased variance over requested axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def skew(self, *, numeric_only: bool = False):
        """Return unbiased skew over columns.

        Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'A': [1, 2, 3, 4, 5],
            ...                    'B': [5, 4, 3, 2, 1],
            ...                    'C': [2, 2, 3, 2, 2]})
            >>> df
                A	B	C
            0	1	5	2
            1	2	4	2
            2	3	3	3
            3	4	2	2
            4	5	1	2
            <BLANKLINE>
            [5 rows x 3 columns]

        Calculating the skewness of each column.

            >>> df.skew()
            A         0.0
            B         0.0
            C    2.236068
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def kurt(self, *, numeric_only: bool = False):
        """Return unbiased kurtosis over columns.

        Kurtosis obtained using Fisher's definition of
        kurtosis (kurtosis of normal == 0.0). Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 2, 3, 4, 5],
            ...                     "B": [3, 4, 3, 2, 1],
            ...                     "C": [2, 2, 3, 2, 2]})
            >>> df
                A	B	C
            0	1	3	2
            1	2	4	2
            2	3	3	3
            3	4	2	2
            4	5	1	2
            <BLANKLINE>
            [5 rows x 3 columns]

        Calculating the kurtosis value of each column:

            >>> df.kurt()
            A        -1.2
            B   -0.177515
            C         5.0
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.

        Returns:
            Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(self, *, numeric_only: bool = False):
        """Return sample standard deviation over columns.

        Normalized by N-1 by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, 2, 3, 4, 5],
            ...                     "B": [3, 4, 3, 2, 1],
            ...                     "C": [2, 2, 3, 2, 2]})
            >>> df
                A	B	C
            0	1	3	2
            1	2	4	2
            2	3	3	3
            3	4	2	2
            4	5	1	2
            <BLANKLINE>
            [5 rows x 3 columns]

        Calculating the standard deviation of each column:

            >>> df.std()
            A    1.581139
            B    1.140175
            C    0.447214
            dtype: Float64

        Args:
            numeric_only (bool. default False):
                Default False. Include only float, int, boolean columns.

        Returns:
            bigframes.series.Series: Series with sample standard deviation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def count(self, *, numeric_only: bool = False):
        """
        Count non-NA cells for each column.

        The values `None`, `NaN`, `NaT`, and optionally `numpy.inf` (depending
        on `pandas.options.mode.use_inf_as_na`) are considered NA.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({"A": [1, None, 3, 4, 5],
            ...                     "B": [1, 2, 3, 4, 5],
            ...                     "C": [None, 3.5, None, 4.5, 5.0]})
            >>> df
                   A	B	   C
            0	 1.0	1	<NA>
            1	<NA>	2	 3.5
            2	 3.0	3	<NA>
            3	 4.0	4	 4.5
            4	 5.0	5	 5.0
            <BLANKLINE>
            [5 rows x 3 columns]

        Counting non-NA values for each column:

            >>> df.count()
            A    4.0
            B    5.0
            C    3.0
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.series.Series: For each column/row the number of
                non-NA/null entries. If `level` is specified returns a `DataFrame`.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nlargest(self, n: int, columns, keep: str = "first"):
        """
        Return the first `n` rows ordered by `columns` in descending order.

        Return the first `n` rows with the largest values in `columns`, in
        descending order. The columns that are not specified are returned as
        well, but not used for ordering.

        This method is equivalent to
        ``df.sort_values(columns, ascending=False).head(n)``, but more
        performant.

        Args:
            n (int):
                Number of rows to return.
            columns (label or list of labels):
                Column label(s) to order by.
            keep ({'first', 'last', 'all'}, default 'first'):
                Where there are duplicate values:

                - ``first`` : prioritize the first occurrence(s)
                - ``last`` : prioritize the last occurrence(s)
                - ``all`` : do not drop any duplicates, even it means
                  selecting more than `n` items.

        Returns:
            DataFrame: The first `n` rows ordered by the given columns in descending order.

        .. note::
            This function cannot be used with all column types. For example, when
            specifying columns with `object` or `category` dtypes, ``TypeError`` is
            raised.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nsmallest(self, n: int, columns, keep: str = "first"):
        """
        Return the first `n` rows ordered by `columns` in ascending order.

        Return the first `n` rows with the smallest values in `columns`, in
        ascending order. The columns that are not specified are returned as
        well, but not used for ordering.

        This method is equivalent to
        ``df.sort_values(columns, ascending=True).head(n)``, but more
        performant.

        Args:
            n (int):
                Number of rows to return.
            columns (label or list of labels):
                Column label(s) to order by.
            keep ({'first', 'last', 'all'}, default 'first'):
                Where there are duplicate values:

                - ``first`` : prioritize the first occurrence(s)
                - ``last`` : prioritize the last occurrence(s)
                - ``all`` : do not drop any duplicates, even it means
                  selecting more than `n` items.

        Returns:
            DataFrame: The first `n` rows ordered by the given columns in ascending order.

        .. note::
            This function cannot be used with all column types. For example, when
            specifying columns with `object` or `category` dtypes, ``TypeError`` is
            raised.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmin(self):
        """
        Return index of first occurrence of minimum over requested axis.

        NA/null values are excluded.

        Returns:
            Series: Indexes of minima along the specified axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmax(self):
        """
        Return index of first occurrence of maximum over requested axis.

        NA/null values are excluded.

        Returns:
            Series: Indexes of maxima along the specified axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def melt(self, id_vars, value_vars, var_name, value_name):
        """
        Unpivot a DataFrame from wide to long format, optionally leaving identifiers set.

        This function is useful to massage a DataFrame into a format where one
        or more columns are identifier variables (`id_vars`), while all other
        columns, considered measured variables (`value_vars`), are "unpivoted" to
        the row axis, leaving just two non-identifier columns, 'variable' and
        'value'.

        Parameters
        ----------
        id_vars (tuple, list, or ndarray, optional):
            Column(s) to use as identifier variables.
        value_vars (tuple, list, or ndarray, optional):
            Column(s) to unpivot. If not specified, uses all columns that
            are not set as `id_vars`.
        var_name (scalar):
            Name to use for the 'variable' column. If None it uses
            ``frame.columns.name`` or 'variable'.
        value_name (scalar, default 'value'):
            Name to use for the 'value' column.

        Returns:
            DataFrame: Unpivoted DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self):
        """
        Count number of distinct elements in specified axis.

        Returns:
            bigframes.series.Series: Series with number of distinct elements.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummin(self) -> DataFrame:
        """Return cumulative minimum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative minimum.

        Returns:
            bigframes.dataframe.DataFrame: Return cumulative minimum of DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummax(self) -> DataFrame:
        """Return cumulative maximum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative maximum.

        Returns:
            bigframes.dataframe.DataFrame: Return cumulative maximum of DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumsum(self) -> DataFrame:
        """Return cumulative sum over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative sum.

        Returns:
            bigframes.dataframe.DataFrame: Return cumulative sum of DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumprod(self) -> DataFrame:
        """Return cumulative product over a DataFrame axis.

        Returns a DataFrame of the same size containing the cumulative product.

        Returns:
            bigframes.dataframe.DataFrame: Return cumulative product of DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def diff(
        self,
        periods: int = 1,
    ) -> NDFrame:
        """First discrete difference of element.

        Calculates the difference of a DataFrame element compared with another
        element in the DataFrame (default is element in previous row).

        Args:
            periods (int, default 1):
                Periods to shift for calculating difference, accepts negative
                values.

        Returns:
            bigframes.dataframe.DataFrame: First differences of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def agg(self, func):
        """
        Aggregate using one or more operations over the specified axis.

        Args:
            func (function):
                Function to use for aggregating the data.
                Accepted combinations are: string function name, list of
                function names, e.g. ``['sum', 'mean']``.

        Returns:
            DataFrame or bigframes.series.Series: Aggregated results.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def describe(self):
        """
        Generate descriptive statistics.

        Descriptive statistics include those that summarize the central
        tendency, dispersion and shape of a
        dataset's distribution, excluding ``NaN`` values.

        Only supports numeric columns.

        .. note::
            Percentile values are approximates only.

        .. note::
            For numeric data, the result's index will include ``count``,
            ``mean``, ``std``, ``min``, ``max`` as well as lower, ``50`` and
            upper percentiles. By default the lower percentile is ``25`` and the
            upper percentile is ``75``. The ``50`` percentile is the
            same as the median.

        Returns:
            bigframes.dataframe.DataFrame: Summary statistics of the Series or Dataframe provided.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pivot(self, *, columns, index=None, values=None):
        """
        Return reshaped DataFrame organized by given index / column values.

        Reshape data (produce a "pivot" table) based on column values. Uses
        unique values from specified `index` / `columns` to form axes of the
        resulting DataFrame. This function does not support data
        aggregation, multiple values will result in a MultiIndex in the
        columns.

        .. note::
            BigQuery supports up to 10000 columns. Pivot operations on columns
            with too many unique values will fail if they would exceed this limit.

        .. note::
            The validity of the pivot operation is not checked. If columns and index
            do not together uniquely identify input rows, the output will be
            silently non-deterministic.

        Args:
            columns (str or object or a list of str):
                Column to use to make new frame's columns.

            index (str or object or a list of str, optional):
                Column to use to make new frame's index. If not given, uses existing index.

            values (str, object or a list of the previous, optional):
                Column(s) to use for populating new frame's values. If not
                specified, all remaining columns will be used and the result will
                have hierarchically indexed columns.

        Returns:
            Returns reshaped DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def stack(self):
        """
        Stack the prescribed level(s) from columns to index.

        Return a reshaped DataFrame or Series having a multi-level
        index with one or more new inner-most levels compared to the current
        DataFrame. The new inner-most levels are created by pivoting the
        columns of the current dataframe:

        - if the columns have a single level, the output is a Series;
        - if the columns have multiple levels, the new index
            level(s) is (are) taken from the prescribed level(s) and
            the output is a DataFrame.

        .. note::
            BigQuery DataFrames does not support stack operations that would
            combine columns of different dtypes.

        Returns:
            DataFrame or Series: Stacked dataframe or series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def unstack(self):
        """
        Pivot a level of the (necessarily hierarchical) index labels.

        Returns a DataFrame having a new level of column labels whose inner-most level
        consists of the pivoted index labels.

        If the index is not a MultiIndex, the output will be a Series
        (the analogue of stack when the columns are not a MultiIndex).

        Returns:
            DataFrame or Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Add index and columns

    @property
    def index(self):
        """The index (row labels) of the DataFrame.

        The index of a DataFrame is a series of labels that identify each row.
        The labels can be integers, strings, or any other hashable type. The
        index is used for label-based access and alignment, and can be accessed
        or modified using this attribute.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can access the index of a DataFrame via ``index`` property.

            >>> df = bpd.DataFrame({'Name': ['Alice', 'Bob', 'Aritra'],
            ...                     'Age': [25, 30, 35],
            ...                     'Location': ['Seattle', 'New York', 'Kona']},
            ...                    index=([10, 20, 30]))
            >>> df
                Name  Age  Location
            10   Alice   25   Seattle
            20     Bob   30  New York
            30  Aritra   35      Kona
            <BLANKLINE>
            [3 rows x 3 columns]
            >>> df.index # doctest: +ELLIPSIS
            <bigframes.core.indexes.index.Index object at ...>
            >>> df.index.values
            array([10, 20, 30], dtype=object)

        Let's try setting a new index for the dataframe and see that reflect via
        ``index`` property.

            >>> df1 = df.set_index(["Name", "Location"])
            >>> df1
                            Age
            Name   Location
            Alice  Seattle    25
            Bob    New York   30
            Aritra Kona       35
            <BLANKLINE>
            [3 rows x 1 columns]
            >>> df1.index # doctest: +ELLIPSIS
            <bigframes.core.indexes.index.Index object at ...>
            >>> df1.index.values
            array([('Alice', 'Seattle'), ('Bob', 'New York'), ('Aritra', 'Kona')],
                dtype=object)

        Returns:
            The index labels of the DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def columns(self):
        """The column labels of the DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can access the column labels of a DataFrame via ``columns`` property.

            >>> df = bpd.DataFrame({'Name': ['Alice', 'Bob', 'Aritra'],
            ...                     'Age': [25, 30, 35],
            ...                     'Location': ['Seattle', 'New York', 'Kona']},
            ...                    index=([10, 20, 30]))
            >>> df
                  Name  Age  Location
            10   Alice   25   Seattle
            20     Bob   30  New York
            30  Aritra   35      Kona
            <BLANKLINE>
            [3 rows x 3 columns]
            >>> df.columns
            Index(['Name', 'Age', 'Location'], dtype='object')

        You can also set new labels for columns.

            >>> df.columns = ["NewName", "NewAge", "NewLocation"]
            >>> df
               NewName  NewAge NewLocation
            10   Alice      25     Seattle
            20     Bob      30    New York
            30  Aritra      35        Kona
            <BLANKLINE>
            [3 rows x 3 columns]
            >>> df.columns
            Index(['NewName', 'NewAge', 'NewLocation'], dtype='object')

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def value_counts(
        self,
        subset=None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ):
        """
        Return a Series containing counts of unique rows in the DataFrame.

        Args:
            subset (label or list of labels, optional):
                Columns to use when counting unique combinations.
            normalize (bool, default False):
                Return proportions rather than frequencies.
            sort (bool, default True):
                Sort by frequencies.
            ascending (bool, default False):
                Sort in ascending order.
            dropna (bool, default True):
                Don’t include counts of rows that contain NA values.

        Returns:
            Series: Series containing counts of unique rows in the DataFrame
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def interpolate(self, method: str = "linear"):
        """
        Fill NaN values using an interpolation method.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3, None, None, 6],
            ...     'B': [None, 6, None, 2, None, 3],
            ...     }, index=[0, 0.1, 0.3, 0.7, 0.9, 1.0])
            >>> df.interpolate()
                   A     B
            0.0  1.0  <NA>
            0.1  2.0   6.0
            0.3  3.0   4.0
            0.7  4.0   2.0
            0.9  5.0   2.5
            1.0  6.0   3.0
            <BLANKLINE>
            [6 rows x 2 columns]
            >>> df.interpolate(method="values")
                        A         B
            0.0       1.0      <NA>
            0.1       2.0       6.0
            0.3       3.0  4.666667
            0.7  4.714286       2.0
            0.9  5.571429  2.666667
            1.0       6.0       3.0
            <BLANKLINE>
            [6 rows x 2 columns]

        Args:
            method (str, default 'linear'):
                Interpolation technique to use. Only 'linear' supported.
                'linear': Ignore the index and treat the values as equally spaced.
                This is the only method supported on MultiIndexes.
                'index', 'values': use the actual numerical values of the index.
                'pad': Fill in NaNs using existing values.
                'nearest', 'zero', 'slinear': Emulates `scipy.interpolate.interp1d`

        Returns:
            DataFrame:
                Returns the same object type as the caller, interpolated at
                some or all ``NaN`` values
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fillna(self, value):
        """
        Fill NA/NaN values using the specified method.

        Args:
            value (scalar, Series):
                Value to use to fill holes (e.g. 0), alternately a
                Series of values specifying which value to use for
                each index (for a Series) or column (for a DataFrame).  Values not
                in the Series will not be filled. This value cannot
                be a list.

        Returns:
            DataFrame: Object with missing values filled
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def iloc(self):
        """Purely integer-location based indexing for selection by position."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def iat(self):
        """Access a single value for a row/column pair by integer position."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def at(self):
        """Access a single value for a row/column label pair."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def dot(self, other):
        """
        Compute the matrix multiplication between the DataFrame and other.

        This method computes the matrix product between the DataFrame and the
        values of an other Series or DataFrame.

        It can also be called using `self @ other`.

        .. note::
            The dimensions of DataFrame and other must be compatible in order to
            compute the matrix multiplication. In addition, the column names of
            DataFrame and the index of other must contain the same values, as they
            will be aligned prior to the multiplication.

            The dot method for Series computes the inner product, instead of the
            matrix product here.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> left = bpd.DataFrame([[0, 1, -2, -1], [1, 1, 1, 1]])
            >>> left
               0  1   2   3
            0  0  1  -2  -1
            1  1  1   1   1
            <BLANKLINE>
            [2 rows x 4 columns]
            >>> right = bpd.DataFrame([[0, 1], [1, 2], [-1, -1], [2, 0]])
            >>> right
                0   1
            0   0   1
            1   1   2
            2  -1  -1
            3   2   0
            <BLANKLINE>
            [4 rows x 2 columns]
            >>> left.dot(right)
               0  1
            0  1  4
            1  2  2
            <BLANKLINE>
            [2 rows x 2 columns]

        You can also use the operator ``@`` for the dot product:

            >>> left @ right
               0  1
            0  1  4
            1  2  2
            <BLANKLINE>
            [2 rows x 2 columns]

        The right input can be a Series, in which case the result will also be a
        Series:

            >>> right = bpd.Series([1, 2, -1,0])
            >>> left @ right
            0    4
            1    2
            dtype: Int64

        Any user defined index of the left matrix and columns of the right
        matrix will reflect in the result.

            >>> left = bpd.DataFrame([[1, 2, 3], [2, 5, 7]], index=["alpha", "beta"])
            >>> left
                   0  1  2
            alpha  1  2  3
            beta   2  5  7
            <BLANKLINE>
            [2 rows x 3 columns]
            >>> right = bpd.DataFrame([[2, 4, 8], [1, 5, 10], [3, 6, 9]], columns=["red", "green", "blue"])
            >>> right
               red  green  blue
            0    2      4     8
            1    1      5    10
            2    3      6     9
            <BLANKLINE>
            [3 rows x 3 columns]
            >>> left.dot(right)
                   red  green  blue
            alpha   13     32    55
            beta    30     75   129
            <BLANKLINE>
            [2 rows x 3 columns]

        Args:
            other (Series or DataFrame):
                The other object to compute the matrix product with.

        Returns:
            Series or DataFrame
                If `other` is a Series, return the matrix product between self and
                other as a Series. If other is a DataFrame, return
                the matrix product of self and other in a DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
