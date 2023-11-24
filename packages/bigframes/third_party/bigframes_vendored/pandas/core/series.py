"""
Data structure for 1-dimensional cross-sectional and time series data
"""
from __future__ import annotations

from typing import Hashable, IO, Literal, Mapping, Sequence, TYPE_CHECKING

import numpy as np
from pandas._libs import lib
from pandas._typing import Axis, FilePath, NaPosition, WriteBuffer

from bigframes import constants
from third_party.bigframes_vendored.pandas.core.generic import NDFrame

if TYPE_CHECKING:
    from third_party.bigframes_vendored.pandas.core.frame import DataFrame
    from third_party.bigframes_vendored.pandas.core.groupby import SeriesGroupBy


class Series(NDFrame):  # type: ignore[misc]
    @property
    def dt(self):
        """
        Accessor object for datetime-like properties of the Series values.

        Returns:
            bigframes.operations.datetimes.DatetimeMethods:
                An accessor containing datetime methods.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def struct(self):
        """
        Accessor object for struct properties of the Series values.

        Returns:
            bigframes.operations.structs.StructAccessor:
                An accessor containing struct methods.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def index(self):
        """The index (axis labels) of the Series.

        The index of a Series is used to label and identify each element of the
        underlying data. The index can be thought of as an immutable ordered set
        (technically a multi-set, as it may contain duplicate labels), and is
        used to index and align data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can access the index of a Series via ``index`` property.

            >>> df = bpd.DataFrame({'Name': ['Alice', 'Bob', 'Aritra'],
            ...                     'Age': [25, 30, 35],
            ...                     'Location': ['Seattle', 'New York', 'Kona']},
            ...                    index=([10, 20, 30]))
            >>> s = df["Age"]
            >>> s
            10    25
            20    30
            30    35
            Name: Age, dtype: Int64
            >>> s.index # doctest: +ELLIPSIS
            <bigframes.core.indexes.index.Index object at ...>
            >>> s.index.values
            array([10, 20, 30], dtype=object)

        Let's try setting a multi-index case reflect via ``index`` property.

            >>> df1 = df.set_index(["Name", "Location"])
            >>> s1 = df1["Age"]
            >>> s1
            Name    Location
            Alice   Seattle     25
            Bob     New York    30
            Aritra  Kona        35
            Name: Age, dtype: Int64
            >>> s1.index # doctest: +ELLIPSIS
            <bigframes.core.indexes.index.Index object at ...>
            >>> s1.index.values
            array([('Alice', 'Seattle'), ('Bob', 'New York'), ('Aritra', 'Kona')],
                dtype=object)

        Returns:
            The index labels of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def shape(self):
        """Return a tuple of the shape of the underlying data."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtype(self):
        """
        Return the dtype object of the underlying data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtypes(self):
        """
        Return the dtype object of the underlying data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def name(self) -> Hashable:
        """
        Return the name of the Series.

        The name of a Series becomes its index or column name if it is used
        to form a DataFrame. It is also used whenever displaying the Series
        using the interpreter.

        Returns:
            hashable object: The name of the Series, also the column name
                if part of a DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def T(self) -> Series:
        """Return the transpose, which is by definition self."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transpose(self) -> Series:
        """
        Return the transpose, which is by definition self.

        Returns:
            Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reset_index(
        self,
        *,
        drop: bool = False,
        name=lib.no_default,
    ) -> DataFrame | Series | None:
        """
        Generate a new DataFrame or Series with the index reset.

        This is useful when the index needs to be treated as a column, or
        when the index is meaningless and needs to be reset to the default
        before another operation.

        Args:
            drop (bool, default False):
                Just reset the index, without inserting it as a column in
                the new DataFrame.
            name (object, optional):
                The name to use for the column containing the original Series
                values. Uses ``self.name`` by default. This argument is ignored
                when `drop` is True.

        Returns:
            Series or DataFrame or None; When `drop` is False (the default),
                a DataFrame is returned. The newly created columns will come first
                in the DataFrame, followed by the original Series values.
                When `drop` is True, a `Series` is returned.
                In either case, if ``inplace=True``, no value is returned.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __repr__(self) -> str:
        """
        Return a string representation for a particular Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # IO methods (to / from other formats)

    def to_string(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        na_rep: str = "NaN",
        float_format: str | None = None,
        header: bool = True,
        index: bool = True,
        length: bool = False,
        dtype: bool = False,
        name: bool = False,
        max_rows: int | None = None,
        min_rows: int | None = None,
    ) -> str | None:
        """
        Render a string representation of the Series.

        Args:
            buf (StringIO-like, optional):
                Buffer to write to.
            na_rep (str, optional):
                String representation of NaN to use, default 'NaN'.
            float_format (one-parameter function, optional):
                Formatter function to apply to columns' elements if they are
                floats, default None.
            header (bool, default True):
                Add the Series header (index name).
            index (bool, optional):
                Add index (row) labels, default True.
            length (bool, default False):
                Add the Series length.
            dtype (bool, default False):
                Add the Series dtype.
            name (bool, default False):
                Add the Series name if not None.
            max_rows (int, optional):
                Maximum number of rows to show before truncating. If None, show
                all.
            min_rows (int, optional):
                The number of rows to display in a truncated repr (when number
                of rows is above `max_rows`).

        Returns:
            str or None: String representation of Series if ``buf=None``,
                otherwise None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_markdown(
        self,
        buf: IO[str] | None = None,
        mode: str = "wt",
        index: bool = True,
        **kwargs,
    ) -> str | None:
        """
        Print {klass} in Markdown-friendly format.

        Args:
            buf (str, Path or StringIO-like, optional, default None):
                Buffer to write to. If None, the output is returned as a string.
            mode (str, optional):
                Mode in which file is opened, "wt" by default.
            index (bool, optional, default True):
                Add index (row) labels.

        Returns:
            str: {klass} in Markdown-friendly format.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_dict(self, into: type[dict] = dict) -> Mapping:
        """
        Convert Series to {label -> value} dict or dict-like object.

        Args:
            into (class, default dict):
                The collections.abc.Mapping subclass to use as the return
                object. Can be the actual class or an empty
                instance of the mapping type you want.  If you want a
                collections.defaultdict, you must pass it initialized.

        Returns:
            collections.abc.Mapping: Key-value representation of Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_frame(self, name=None) -> DataFrame:
        """
        Convert Series to DataFrame.

        The column in the new dataframe will be named name (the keyword parameter)
        if the name parameter is provided and not None.

        Args:
            name (Hashable, default None)

        Returns:
            bigframes.dataframe.DataFrame: DataFrame representation of Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_excel(self, excel_writer, sheet_name):
        """
        Write Series to an Excel sheet.

        To write a single Series to an Excel .xlsx file it is only necessary to
        specify a target file name. To write to multiple sheets it is necessary to
        create an `ExcelWriter` object with a target file name, and specify a sheet
        in the file to write to.

        Multiple sheets may be written to by specifying unique `sheet_name`.
        With all data written to the file it is necessary to save the changes.
        Note that creating an `ExcelWriter` object with a file name that already
        exists will result in the contents of the existing file being erased.

        Args:
            excel_writer (path-like, file-like, or ExcelWriter object):
                File path or existing ExcelWriter.
            sheet_name (str, default 'Sheet1'):
                Name of sheet to contain Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_latex(self, buf=None, columns=None, header=True, index=True, **kwargs):
        """
        Render object to a LaTeX tabular, longtable, or nested table.

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

        Returns:
            str or None: If buf is None, returns the result as a string.
                Otherwise returns None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def tolist(self) -> list:
        """
        Return a list of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period).

        Returns:
            list: list of the values
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    to_list = tolist

    def to_numpy(self, dtype, copy=False, na_value=None):
        """
        A NumPy ndarray representing the values in this Series or Index.

        Args:
            dtype (str or numpy.dtype, optional):
                The dtype to pass to :meth:`numpy.asarray`.
            copy (bool, default False):
                Whether to ensure that the returned value is not a view on
                another array. Note that ``copy=False`` does not *ensure* that
                ``to_numpy()`` is no-copy. Rather, ``copy=True`` ensure that
                a copy is made, even if not strictly necessary.
            na_value (Any, optional):
                The value to use for missing values. The default value depends
                on `dtype` and the type of the array.
            ``**kwargs``:
                Additional keywords passed through to the ``to_numpy`` method
                of the underlying array (for extension arrays).

        Returns:
            numpy.ndarray: A NumPy ndarray representing the values in this
                Series or Index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_pickle(self, path, **kwargs):
        """
        Pickle (serialize) object to file.

        Args:
            path (str, path object, or file-like object):
                String, path object (implementing ``os.PathLike[str]``), or file-like
                object implementing a binary ``write()`` function. File path where
                the pickled object will be stored.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_xarray(self):
        """
        Return an xarray object from the pandas object.

        Returns:
            xarray.DataArray or xarray.Dataset: Data in the pandas structure
                converted to Dataset if the object is a DataFrame, or a DataArray if
                the object is a Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_json(
        self,
        path_or_buf=None,
        orient: Literal[
            "split", "records", "index", "columns", "values", "table"
        ] = "columns",
        **kwarg,
    ) -> str | None:
        """
        Convert the object to a JSON string.

        Note NaN's and None will be converted to null and datetime objects
        will be converted to UNIX timestamps.

        Args:
            path_or_buf (str, path object, file-like object, or None, default None):
                String, path object (implementing os.PathLike[str]), or file-like
                object implementing a write() function. If None, the result is
                returned as a string.
            orient ({"split", "records", "index", "columns", "values", "table"}, default "columns"):
                Indication of expected JSON string format.
                'split' : dict like {{'index' -> [index], 'columns' -> [columns],'data' -> [values]}}
                'records' : list like [{{column -> value}}, ... , {{column -> value}}]
                'index' : dict like {{index -> {{column -> value}}}}
                'columns' : dict like {{column -> {{index -> value}}}}
                'values' : just the values array
                'table' : dict like {{'schema': {{schema}}, 'data': {{data}}}}
                Describing the data, where data component is like ``orient='records'``.

        Returns:
            None or str: If path_or_buf is None, returns the resulting json format as a
                string. Otherwise returns None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_csv(self, path_or_buf: str, *, index: bool = True) -> str | None:
        """
        Write object to a comma-separated values (csv) file.

        Args:
            path_or_buf (str, path object, file-like object, or None, default None):
                String, path object (implementing os.PathLike[str]), or file-like
                object implementing a write() function. If None, the result is
                returned as a string. If a non-binary file object is passed, it should
                be opened with `newline=''`, disabling universal newlines. If a binary
                file object is passed, `mode` might need to contain a `'b'`.

        Returns:
            None or str: If path_or_buf is None, returns the resulting csv format
                as a string. Otherwise returns None.
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
            scalar or Series: Aggregated results
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def count(self):
        """
        Return number of non-NA/null observations in the Series.

        Returns:
            int or Series (if level specified): Number of non-null values in the
                Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self) -> int:
        """
        Return number of unique elements in the object.

        Excludes NA values by default.

        Returns:
            int: number of unique elements in the object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mode(self) -> Series:
        """
        Return the mode(s) of the Series.

        The mode is the value that appears most often. There can be multiple modes.

        Always returns Series even if only one value is returned.

        Returns:
            bigframes.series.Series: Modes of the Series in sorted order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop_duplicates(
        self,
        *,
        keep="first",
    ) -> Series | None:
        """
        Return Series with duplicate values removed.

        Args:
            keep ({'first', 'last', ``False``}, default 'first'):
                Method to handle dropping duplicates:

                'first' : Drop duplicates except for the first occurrence.
                'last' : Drop duplicates except for the last occurrence.
                ``False`` : Drop all duplicates.

        Returns:
            bigframes.series.Series: Series with duplicates dropped or None if ``inplace=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def duplicated(self, keep="first") -> Series:
        """
        Indicate duplicate Series values.

        Duplicated values are indicated as ``True`` values in the resulting
        Series. Either all duplicates, all except the first or all except the
        last occurrence of duplicates can be indicated.

        Args:
            keep ({'first', 'last', False}, default 'first'):
                Method to handle dropping duplicates:

                'first' : Mark duplicates as ``True`` except for the first
                occurrence.
                'last' : Mark duplicates as ``True`` except for the last
                occurrence.
                ``False`` : Mark all duplicates as ``True``.

        Returns:
            bigframes.series.Series: Series indicating whether each value has occurred in the
                preceding values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmin(self) -> Hashable:
        """
        Return the row label of the minimum value.

        If multiple values equal the minimum, the first row label with that
        value is returned.

        Returns:
            Index: Label of the minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmax(self) -> Hashable:
        """
        Return the row label of the maximum value.

        If multiple values equal the maximum, the first row label with that
        value is returned.

        Returns:
            Index: Label of the maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def round(self, decimals: int = 0) -> Series:
        """
        Round each value in a Series to the given number of decimals.

        Args:
            decimals (int, default 0):
                Number of decimal places to round to. If decimals is negative,
                it specifies the number of positions to the left of the decimal point.

        Returns:
            bigframes.series.Series: Rounded values of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def corr(self, other, method="pearson", min_periods=None) -> float:
        """
        Compute the correlation with the other Series.  Non-number values are ignored in the
        computation.

        Uses the "Pearson" method of correlation.  Numbers are converted to float before
        calculation, so the result may be unstable.

        Args:
            other (Series):
                The series with which this is to be correlated.
            method (string, default "pearson"):
                Correlation method to use - currently only "pearson" is supported.
            min_periods (int, default None):
                The minimum number of observations needed to return a result.  Non-default values
                are not yet supported, so a result will be returned for at least two observations.

        Returns:
            float;  Will return NaN if there are fewer than two numeric pairs, either series has a
                variance or covariance of zero, or any input value is infinite.
        """
        raise NotImplementedError("abstract method")

    def diff(self) -> Series:
        """
        First discrete difference of element.

        Calculates the difference of a {klass} element compared with another
        element in the {klass} (default is element in previous row).

        Args:
            periods (int, default 1):
                Periods to shift for calculating difference, accepts negative
                values.

        Returns:
            {klass}: First differences of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def dot(self, other) -> Series | np.ndarray:
        """
        Compute the dot product between the Series and the columns of other.

        This method computes the dot product between the Series and another
        one, or the Series and each columns of a DataFrame, or the Series and
        each columns of an array.

        It can also be called using `self @ other` in Python >= 3.5.

        .. note::
            The Series and other has to share the same index if other is a Series
            or a DataFrame.
            BigQuery Dataframes does not validate this property and will produce
            incorrect results if indices are not equal.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0, 1, 2, 3])
            >>> other = bpd.Series([-1, 2, -3, 4])
            >>> s.dot(other)
            8

        You can also use the operator ``@`` for the dot product:

            >>> s @ other
            8

        Args:
            other (Series):
                The other object to compute the dot product with its columns.

        Returns:
            scalar, Series or numpy.ndarray: Return the dot product of the Series
                and other if other is a Series, the Series of the dot product of
                Series and each rows of other if other is a DataFrame or a
                numpy.ndarray between the Series and each columns of the numpy array.


        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __matmul__(self, other):
        """
        Matrix multiplication using binary `@` operator in Python>=3.5.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rmatmul__(self, other):
        """
        Matrix multiplication using binary `@` operator in Python>=3.5.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sort_values(
        self,
        *,
        axis: Axis = 0,
        ascending: bool | int | Sequence[bool] | Sequence[int] = True,
        kind: str = "quicksort",
        na_position: str = "last",
    ) -> Series | None:
        """
        Sort by the values.

        Sort a Series in ascending or descending order by some
        criterion.

        Args:
            axis (0 or 'index'):
                Unused. Parameter needed for compatibility with DataFrame.
            ascending (bool or list of bools, default True):
                If True, sort values in ascending order, otherwise descending.
            kind (str, default to 'quicksort'):
                Choice of sorting algorithm. Accepts 'quicksort’, ‘mergesort’,
                ‘heapsort’, ‘stable’. Ignored except when determining whether to
                sort stably. 'mergesort' or 'stable' will result in stable reorder
            na_position ({'first' or 'last'}, default 'last'):
                Argument 'first' puts NaNs at the beginning, 'last' puts NaNs at
                the end.

        Returns:
            bigframes.series.Series: Series ordered by values or None if ``inplace=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sort_index(
        self,
        *,
        axis: Axis = 0,
        ascending: bool | Sequence[bool] = True,
        na_position: NaPosition = "last",
    ) -> Series | None:
        """
        Sort Series by index labels.

        Returns a new Series sorted by label if `inplace` argument is
        ``False``, otherwise updates the original series and returns None.

        Args:
            axis ({0 or 'index'}):
                Unused. Parameter needed for compatibility with DataFrame.
            ascending (bool or list-like of bools, default True):
                Sort ascending vs. descending. When the index is a MultiIndex the
                sort direction can be controlled for each level individually.
            na_position ({'first', 'last'}, default 'last'):
                If 'first' puts NaNs at the beginning, 'last' puts NaNs at the end.
                Not implemented for MultiIndex.

        Returns:
            bigframes.series.Series: The original Series sorted by the labels or None if
                ``inplace=True``.

        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nlargest(
        self, n: int = 5, keep: Literal["first", "last", "all"] = "first"
    ) -> Series:
        """
        Return the largest `n` elements.

        Args:
            n (int, default 5):
                Return this many descending sorted values.
            keep ({'first', 'last', 'all'}, default 'first'):
                When there are duplicate values that cannot all fit in a
                Series of `n` elements:
                ``first`` : return the first `n` occurrences in order
                of appearance.
                ``last`` : return the last `n` occurrences in reverse
                order of appearance.
                ``all`` : keep all occurrences. This can result in a Series of
                size larger than `n`.

        Returns:
            bigframes.series.Series: The `n` largest values in the Series, sorted in decreasing order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nsmallest(self, n: int = 5, keep: str = "first") -> Series:
        """
        Return the smallest `n` elements.

        Args:
            n (int, default 5):
                Return this many ascending sorted values.
            keep ({'first', 'last', 'all'}, default 'first'):
                When there are duplicate values that cannot all fit in a
                Series of `n` elements:

                ``first`` : return the first `n` occurrences in order
                of appearance.
                ``last`` : return the last `n` occurrences in reverse
                order of appearance.
                ``all`` : keep all occurrences. This can result in a Series of
                size larger than `n`.

        Returns:
            bigframes.series.Series: The `n` smallest values in the Series, sorted in increasing order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # function application

    def apply(
        self,
        func,
    ) -> DataFrame | Series:
        """
        Invoke function on values of a Series.

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

            >>> minutes = bpd.Series([0, 30, 60, 90, 120])
            >>> minutes
            0      0
            1     30
            2     60
            3     90
            4    120
            dtype: Int64

            >>> hours = minutes.apply(minutes_to_hours)
            >>> hours
            0    0.0
            1    0.5
            2    1.0
            3    1.5
            4    2.0
            dtype: Float64

        You could turn a user defined function with external package
        dependencies into a BigQuery DataFrames remote function. You would
        provide the names of the packages via ``packages`` param.

            >>> @bpd.remote_function(
            ...     [str],
            ...     str,
            ...     reuse=False,
            ...     packages=["cryptography"],
            ... )
            ... def get_hash(input):
            ...     from cryptography.fernet import Fernet
            ...
            ...     # handle missing value
            ...     if input is None:
            ...         input = ""
            ...
            ...     key = Fernet.generate_key()
            ...     f = Fernet(key)
            ...     return f.encrypt(input.encode()).decode()

            >>> names = bpd.Series(["Alice", "Bob"])
            >>> hashes = names.apply(get_hash)

        Args:
            func (function):
                BigFrames DataFrames ``remote_function`` to apply. The function
                should take a scalar and return a scalar. It will be applied to
                every element in the ``Series``.

        Returns:
            bigframes.series.Series: A new Series with values representing the
            return value of the ``func`` applied to each element of the original
            Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def groupby(
        self,
        by=None,
        axis: Axis = 0,
        level=None,
        as_index: bool = True,
        *,
        dropna: bool = True,
    ) -> SeriesGroupBy:
        """Group Series using a mapper or by a Series of columns.

        A groupby operation involves some combination of splitting the
        object, applying a function, and combining the results. This can be
        used to group large amounts of data and compute operations on these
        groups.

        Args:
            by (mapping, function, label, pd.Grouper or list of such, default None):
                Used to determine the groups for the groupby.
                If ``by`` is a function, it's called on each value of the object's
                index. If a dict or Series is passed, the Series or dict VALUES
                will be used to determine the groups (the Series' values are first
                aligned; see ``.align()`` method). If a list or ndarray of length
                equal to the selected axis is passed (see the `groupby user guide
                <https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#splitting-an-object-into-groups>`_),
                the values are used as-is to determine the groups. A label or list
                of labels may be passed to group by the columns in ``self``.
                Notice that a tuple is interpreted as a (single) key.
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                Split along rows (0) or columns (1). For `Series` this parameter
                is unused and defaults to 0.
            level (int, level name, or sequence of such, default None):
                If the axis is a MultiIndex (hierarchical), group by a particular
                level or levels. Do not specify both ``by`` and ``level``.
            as_index (bool, default True):
                Return object with group labels as the
                index. Only relevant for DataFrame input. as_index=False is
                effectively "SQL-style" grouped output. This argument has no effect
                on filtrations (see the "filtrations in the user guide"
                `<https://pandas.pydata.org/docs/dev/user_guide/groupby.html#filtration>`_),
                such as ``head()``, ``tail()``, ``nth()`` and in transformations
                (see the "transformations in the user guide"
                `<https://pandas.pydata.org/docs/dev/user_guide/groupby.html#transformation>`_).
            dropna : bool, default True
                If True, and if group keys contain NA values, NA values together
                with row/column will be dropped.
                If False, NA values will also be treated as the key in groups.

        Returns:
            bigframes.core.groupby.SeriesGroupBy: Returns a groupby object that contains
                information about the groups.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reindex(self, index=None):
        """
        Conform Series to new index with optional filling logic.

        Places NA/NaN in locations having no value in the previous index. A new object
        is produced unless the new index is equivalent to the current one and
        ``copy=False``.

        Args:
            index (array-like, optional):
                New labels for the index. Preferably an Index object to avoid
                duplicating data.

        Returns:
            Series: Series with changed index.
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
    ) -> Series | None:
        """
        Return Series with specified index labels removed.

        Remove elements of a Series based on specifying the index labels.
        When using a multi-index, labels on different levels can be removed
        by specifying the level.

        Args:
            labels (single label or list-like):
                Index labels to drop.
            axis:
                Unused. Parameter needed for compatibility with DataFrame.
            index:
                Redundant for application on Series, but 'index' can be used instead
                of 'labels'.
            columns:
                No change is made to the Series; use 'index' or 'labels' instead.
            level:
                For MultiIndex, level for which the labels will be removed.

        Returns:
            bigframes.series.Series: Series with specified index labels removed
                or None if ``inplace=True``.

        Raises:
            KeyError: If none of the labels are found in the index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reorder_levels(self, order: Sequence, axis) -> Series:
        """
        Rearrange index levels using input order.

        May not drop or duplicate levels.

        Args:
            order (list of int representing new level order):
                Reference level by number or key.

            axis ({0 or 'index', 1 or 'columns'}, default 0):
                For `Series` this parameter is unused and defaults to 0.


        Returns:
            type of caller (new object)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def swaplevel(self, i, j):
        """
        Swap levels i and j in a `MultiIndex`.

        Default is to swap the two innermost levels of the index.

        Args:
            i, j (int or str):
                Levels of the indices to be swapped. Can pass level name as string.

        Returns:
            Series: Series with levels swapped in MultiIndex
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def droplevel(self, level, axis):
        """
        Return Series with requested index / column level(s) removed.

        Args:
            level (int, str, or list-like):
                If a string is given, must be the name of a level
                If list-like, elements must be names or positional indexes
                of levels.

            axis ({0 or 'index', 1 or 'columns'}, default 0):
                For `Series` this parameter is unused and defaults to 0.

        Returns:
            Series with requested index / column level(s) removed.
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
            Series:
                Returns the same object type as the caller, interpolated at
                some or all ``NaN`` values
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fillna(
        self,
        value=None,
    ) -> Series | None:
        """
        Fill NA/NaN values using the specified method.

        Args:
            value (scalar, dict, Series, or DataFrame, default None):
                Value to use to fill holes (e.g. 0).

        Returns:
            Series or None: Object with missing values filled or None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def replace(
        self,
        to_replace,
        value=None,
    ) -> Series | None:
        """
        Replace values given in `to_replace` with `value`.

        Values of the Series/DataFrame are replaced with other values dynamically.
        This differs from updating with ``.loc`` or ``.iloc``, which require
        you to specify a location to update with some value.

        Args:
            to_replace (str, regex, list, int, float or None):
                How to find the values that will be replaced.

                * numeric, str or regex:

                    - numeric: numeric values equal to `to_replace` will be
                      replaced with `value`
                    - str: string exactly matching `to_replace` will be replaced
                      with `value`
                    - regex: regexs matching `to_replace` will be replaced with
                      `value`

                * list of str, regex, or numeric:

                    - First, if `to_replace` and `value` are both lists, they
                      **must** be the same length.
                    - Second, if ``regex=True`` then all of the strings in **both**
                      lists will be interpreted as regexs otherwise they will match
                      directly. This doesn't matter much for `value` since there
                      are only a few possible substitution regexes you can use.
                    - str, regex and numeric rules apply as above.

            value (scalar, default None):
                Value to replace any values matching `to_replace` with.
                For a DataFrame a dict of values can be used to specify which
                value to use for each column (columns not in the dict will not be
                filled). Regular expressions, strings and lists or dicts of such
                objects are also allowed.
            regex (bool, default False):
                Whether to interpret `to_replace` and/or `value` as regular
                expressions. If this is ``True`` then `to_replace` *must* be a
                string.

        Returns:
            Series/DataFrame: Object after replacement.

        Raises:
            TypeError:
                * If `to_replace` is not a scalar, array-like, ``dict``, or ``None``
                * If `to_replace` is a ``dict`` and `value` is not a ``list``,
                  ``dict``, ``ndarray``, or ``Series``
                * If `to_replace` is ``None`` and `regex` is not compilable
                  into a regular expression or is a list, dict, ndarray, or
                  Series.
                * When replacing multiple ``bool`` or ``datetime64`` objects and
                  the arguments to `to_replace` does not match the type of the
                  value being replaced
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def dropna(self, *, axis=0, inplace: bool = False, how=None) -> Series:
        """
        Return a new Series with missing values removed.

        Args:
            axis (0 or 'index'):
                Unused. Parameter needed for compatibility with DataFrame.
            inplace (bool, default False):
                Unsupported, do not set.
            how (str, optional):
                Not in use. Kept for compatibility.

        Returns:
            Series: Series with NA entries dropped from it.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def between(
        self,
        left,
        right,
        inclusive: Literal["both", "neither", "left", "right"] = "both",
    ) -> Series:
        """
        Return boolean Series equivalent to left <= series <= right.

        This function returns a boolean vector containing `True` wherever the
        corresponding Series element is between the boundary values `left` and
        `right`. NA values are treated as `False`.

        Args:
            left (scalar or list-like):
                Left boundary.
            right (scalar or list-like):
                Right boundary.
            inclusive ({"both", "neither", "left", "right"}):
                Include boundaries. Whether to set each bound as closed or open.

        Returns:
            Series: Series representing whether each element is between left and
            right (inclusive).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumprod(self):
        """
        Return cumulative product over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        product.

        Returns:
            bigframes.series.Series: Return cumulative sum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumsum(self):
        """
        Return cumulative sum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        sum.

        Args:
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                    The index or the name of the axis. 0 is equivalent to None or 'index'.
                    For `Series` this parameter is unused and defaults to 0.

        Returns:
            scalar or Series: Return cumulative sum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummax(self):
        """
        Return cumulative maximum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        maximum.

        Args:
            axis ({{0 or 'index', 1 or 'columns'}}, default 0):
                The index or the name of the axis. 0 is equivalent to None or 'index'.
                For `Series` this parameter is unused and defaults to 0.

        Returns:
            bigframes.series.Series: Return cumulative maximum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummin(self):
        """
        Return cumulative minimum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        minimum.

        Args:
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                The index or the name of the axis. 0 is equivalent to None or 'index'.
                For `Series` this parameter is unused and defaults to 0.
            skipna (bool, default True):
                Exclude NA/null values. If an entire row/column is NA, the result
                will be NA.
            `*args`, `**kwargs`:
                Additional keywords have no effect but might be accepted for
                compatibility with NumPy.

        Returns:
            bigframes.series.Series: Return cumulative minimum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def eq(self, other) -> Series:
        """Return equal of Series and other, element-wise (binary operator eq).

        Equivalent to ``other == series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ne(self, other) -> Series:
        """Return not equal of Series and other, element-wise (binary operator ne).

        Equivalent to ``other != series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def le(self, other) -> Series:
        """Get 'less than or equal to' of Series and other, element-wise (binary operator `<=`).

        Equivalent to ``series <= other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other: Series, or scalar value

        Returns:
            bigframes.series.Series. The result of the comparison.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lt(self, other) -> Series:
        """Get 'less than' of Series and other, element-wise (binary operator `<`).

         Equivalent to ``series < other``, but with support to substitute a fill_value for
         missing data in either one of the inputs.

        Args:
             other (Series, or scalar value):

         Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ge(self, other) -> Series:
        """Get 'greater than or equal to' of Series and other, element-wise (binary operator `>=`).

        Equivalent to ``series >= other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def gt(self, other) -> Series:
        """Get 'less than or equal to' of Series and other, element-wise (binary operator `<=`).

        Equivalent to ``series <= other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def add(self, other) -> Series:
        """Return addition of Series and other, element-wise (binary operator add).

        Equivalent to ``series + other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def radd(self, other) -> Series:
        """Return addition of Series and other, element-wise (binary operator radd).

        Equivalent to ``other + series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sub(
        self,
        other,
    ) -> Series:
        """Return subtraction of Series and other, element-wise (binary operator sub).

        Equivalent to ``series - other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rsub(self, other) -> Series:
        """Return subtraction of Series and other, element-wise (binary operator rsub).

        Equivalent to ``other - series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mul(self, other) -> Series:
        """Return multiplication of Series and other, element-wise (binary operator mul).

        Equivalent to ``other * series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rmul(self, other) -> Series:
        """Return multiplication of Series and other, element-wise (binary operator mul).

        Equivalent to ``series * others``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            Series: The result of the operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def truediv(self, other) -> Series:
        """Return floating division of Series and other, element-wise (binary operator truediv).

        Equivalent to ``series / other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rtruediv(self, other) -> Series:
        """Return floating division of Series and other, element-wise (binary operator rtruediv).

        Equivalent to ``other / series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def floordiv(self, other) -> Series:
        """Return integer division of Series and other, element-wise (binary operator floordiv).

        Equivalent to ``series // other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rfloordiv(self, other) -> Series:
        """Return integer division of Series and other, element-wise (binary operator rfloordiv).

        Equivalent to ``other // series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mod(self, other) -> Series:
        """Return modulo of Series and other, element-wise (binary operator mod).

        Equivalent to ``series % other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rmod(self, other) -> Series:
        """Return modulo of Series and other, element-wise (binary operator mod).

        Equivalent to ``series % other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pow(self, other) -> Series:
        """Return Exponential power of series and other, element-wise (binary operator `pow`).

        Equivalent to ``series ** other``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rpow(self, other) -> Series:
        """Return Exponential power of series and other, element-wise (binary operator `rpow`).

        Equivalent to ``other ** series``, but with support to substitute a fill_value for
        missing data in either one of the inputs.

        Args:
            other (Series, or scalar value):

        Returns:
            bigframes.series.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def divmod(self, other) -> Series:
        """Return integer division and modulo of Series and other, element-wise (binary operator divmod).

        Equivalent to divmod(series, other).

        Args:
            other: Series, or scalar value

        Returns:
            2-Tuple of Series. The result of the operation. The result is always
            consistent with (floordiv, mod) (though pandas may not).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rdivmod(self, other) -> Series:
        """Return integer division and modulo of Series and other, element-wise (binary operator rdivmod).

        Equivalent to other divmod series.

        Args:
            other: Series, or scalar value

        Returns:
            2-Tuple of Series. The result of the operation. The result is always
            consistent with (rfloordiv, rmod) (though pandas may not).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def all(
        self,
    ):
        """
        Return whether all elements are True, potentially over an axis.

        Returns True unless there at least one element within a Series or along a
        DataFrame axis that is False or equivalent (e.g. zero or empty).

        Returns:
            scalar or Series: If level is specified, then, Series is returned;
                otherwise, scalar is returned.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def any(
        self,
    ):
        """
        Return whether any element is True, potentially over an axis.

        Returns False unless there is at least one element within a series or along
        a Dataframe axis that is True or equivalent (e.g. non-zero or non-empty).

        Returns:
            scalar or Series: If level is specified, then, Series is returned;
                otherwise, scalar is returned.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(
        self,
    ):
        """
        Return the maximum of the values over the requested axis.

        If you want the index of the maximum, use ``idxmax``. This is the equivalent
        of the ``numpy.ndarray`` method ``argmax``.


        Returns:
            scalar or scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(
        self,
    ):
        """
        Return the maximum of the values over the requested axis.

        If you want the index of the minimum, use ``idxmin``. This is the equivalent
        of the ``numpy.ndarray`` method ``argmin``.

        Returns:
            scalar or scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(
        self,
    ):
        """
        Return sample standard deviation over requested axis.

        Normalized by N-1 by default.


        Returns
        -------
        scalar or Series (if level specified)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(
        self,
    ):
        """
        Return unbiased variance over requested axis.

        Normalized by N-1 by default.

        Returns:
            scalar or Series (if level specified)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(self):
        """Return the sum of the values over the requested axis.

        This is equivalent to the method ``numpy.sum``.

        Returns:
            scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(self):
        """Return the mean of the values over the requested axis.

        Returns:
            scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def median(self, *, exact: bool = False):
        """Return the median of the values over the requested axis.

        Args:
            exact (bool. default False):
                Default False. Get the exact median instead of an approximate
                one. Note: ``exact=True`` not yet supported.

        Returns:
            scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def prod(self):
        """Return the product of the values over the requested axis.

        Returns:
            scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def skew(self):
        """Return unbiased skew over requested axis.

        Normalized by N-1.

        Returns:
            scalar
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def kurt(self):
        """Return unbiased kurtosis over requested axis.

        Kurtosis obtained using Fisher’s definition of kurtosis (kurtosis of normal == 0.0). Normalized by N-1.

        Returns:
            scalar or scalar: Unbiased kurtosis over requested axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def where(self, cond, other):
        """Replace values where the condition is False.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([10, 11, 12, 13, 14])
            >>> s
            0    10
            1    11
            2    12
            3    13
            4    14
            dtype: Int64

        You can filter the values in the Series based on a condition. The values
        matching the condition would be kept, and not matching would be replaced.
        The default replacement value is ``NA``.

            >>> s.where(s % 2 == 0)
            0      10
            1    <NA>
            2      12
            3    <NA>
            4      14
            dtype: Int64

        You can specify a custom replacement value for non-matching values.

            >>> s.where(s % 2 == 0, -1)
            0    10
            1    -1
            2    12
            3    -1
            4    14
            dtype: Int64
            >>> s.where(s % 2 == 0, 100*s)
            0      10
            1    1100
            2      12
            3    1300
            4      14
            dtype: Int64

        Args:
            cond (bool Series/DataFrame, array-like, or callable):
                Where cond is True, keep the original value. Where False, replace
                with corresponding value from other. If cond is callable, it is
                computed on the Series/DataFrame and returns boolean
                Series/DataFrame or array. The callable must not change input
                Series/DataFrame (though pandas doesn’t check it).
            other (scalar, Series/DataFrame, or callable):
                Entries where cond is False are replaced with corresponding value
                from other. If other is callable, it is computed on the
                Series/DataFrame and returns scalar or Series/DataFrame.
                The callable must not change input Series/DataFrame (though pandas
                doesn’t check it). If not specified, entries will be filled with
                the corresponding NULL value (np.nan for numpy dtypes, pd.NA for
                extension dtypes).

        Returns:
            bigframes.series.Series: Series after the replacement.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mask(self, cond, other):
        """Replace values where the condition is True.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([10, 11, 12, 13, 14])
            >>> s
            0    10
            1    11
            2    12
            3    13
            4    14
            dtype: Int64

        You can mask the values in the Series based on a condition. The values
        matching the condition would be masked.

            >>> s.mask(s % 2 == 0)
            0    <NA>
            1      11
            2    <NA>
            3      13
            4    <NA>
            dtype: Int64

        You can specify a custom mask value.

            >>> s.mask(s % 2 == 0, -1)
            0    -1
            1    11
            2    -1
            3    13
            4    -1
            dtype: Int64
            >>> s.mask(s % 2 == 0, 100*s)
            0    1000
            1      11
            2    1200
            3      13
            4    1400
            dtype: Int64

        You can also use a remote function to evaluate the mask condition. This
        is useful in situation such as the following, where the mask
        condition is evaluated based on a complicated business logic which cannot
        be expressed in form of a Series.

            >>> @bpd.remote_function([str], bool, reuse=False)
            ... def should_mask(name):
            ...     hash = 0
            ...     for char_ in name:
            ...         hash += ord(char_)
            ...     return hash % 2 == 0

            >>> s = bpd.Series(["Alice", "Bob", "Caroline"])
            >>> s
            0       Alice
            1         Bob
            2    Caroline
            dtype: string
            >>> s.mask(should_mask)
            0        <NA>
            1         Bob
            2    Caroline
            dtype: string
            >>> s.mask(should_mask, "REDACTED")
            0    REDACTED
            1         Bob
            2    Caroline
            dtype: string

        Args:
            cond (bool Series/DataFrame, array-like, or callable):
                Where cond is False, keep the original value. Where True, replace
                with corresponding value from other. If cond is callable, it is
                computed on the Series/DataFrame and should return boolean
                Series/DataFrame or array. The callable must not change input
                Series/DataFrame (though pandas doesn’t check it).
            other (scalar, Series/DataFrame, or callable):
                Entries where cond is True are replaced with corresponding value
                from other. If other is callable, it is computed on the
                Series/DataFrame and should return scalar or Series/DataFrame.
                The callable must not change input Series/DataFrame (though pandas
                doesn’t check it). If not specified, entries will be filled with
                the corresponding NULL value (np.nan for numpy dtypes, pd.NA for
                extension dtypes).

        Returns:
            bigframes.series.Series: Series after the replacement.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def clip(self):
        """Trim values at input threshold(s).

        Assigns values outside boundary to boundary values. Thresholds can be
        singular values or array like, and in the latter case the clipping is
        performed element-wise in the specified axis.

        Args:
            lower (float or array-like, default None):
                Minimum threshold value. All values below this threshold will be set to it. A missing threshold (e.g NA) will not clip the value.

            upper (float or array-like, default None):
                Maximum threshold value. All values above this threshold will be set to it. A missing threshold (e.g NA) will not clip the value.

        Returns:
            Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def unstack(self, level):
        """
        Unstack, also known as pivot, Series with MultiIndex to produce DataFrame.

        Args:
            level (int, str, or list of these, default last level):
                Level(s) to unstack, can pass level name.

        Returns:
            DataFrame: Unstacked Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmax(self):
        """
        Return int position of the smallest value in the Series.

        If the minimum is achieved in multiple locations, the first row position is returned.

        Returns:
            Series: Row position of the maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmin(self):
        """
        Return int position of the largest value in the Series.

        If the maximum is achieved in multiple locations, the first row position is returned.

        Returns:
            Series: Row position of the minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename(self, index, **kwargs) -> Series | None:
        """
        Alter Series index labels or name.

        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is. Extra labels listed don't throw an
        error.

        Alternatively, change ``Series.name`` with a scalar value.

        Args:
            index (scalar, hashable sequence, dict-like or function optional):
                Functions or dict-like are transformations to apply to
                the index.
                Scalar or hashable sequence-like will alter the ``Series.name``
                attribute.

        Returns:
            bigframes.series.Series: Series with index labels.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename_axis(self, mapper, **kwargs):
        """
        Set the name of the axis for the index or columns.

        Args:
            mapper (scalar, list-like, optional):
                Value to set the axis name attribute.

        Returns:
            bigframes.series.Series: Series with the name of the axis set.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        *,
        dropna: bool = True,
    ) -> Series:
        """
        Return a Series containing counts of unique values.

        The resulting object will be in descending order so that the
        first element is the most frequently-occurring element.
        Excludes NA values by default.

        Args:
            normalize (bool, default False):
                If True then the object returned will contain the relative
                frequencies of the unique values.
            sort (bool, default True):
                Sort by frequencies.
            ascending (bool, default False):
                Sort in ascending order.
            dropna (bool, default True):
                Don't include counts of NaN.

        Returns:
            Series: Series containing counts of unique values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def str(self):
        """
        Vectorized string functions for Series and Index.

        NAs stay NA unless handled otherwise by a particular method. Patterned
        after Python’s string methods, with some inspiration from R’s stringr package.

        Returns:
            bigframes.operations.strings.StringMethods:
                An accessor containing string methods.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isin(self, values):
        """
        Whether elements in Series are contained in values.

        Return a boolean Series showing whether each element in the Series matches an
        element in the passed sequence of values exactly.

        .. note::
            This function treats all NaN-like values(e.g., pd.NA, numpy.nan, None) as
            the same. That is, if any form of NaN is present in values, all forms
            of NaN in the series will be considered a match. (though pandas may not)

        Args:
            values (list-like):
                The sequence of values to test. Passing in a single string will raise a
                TypeError. Instead, turn a single string into a list of one element.

        Returns:
            bigframes.series.Series: Series of booleans indicating if each element is in values.

        Raises:
            TypeError: If input is not list-like.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically increasing.

        Returns:
            bool
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically decreasing.

        Returns:
            bool
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def map(
        self,
        arg,
        na_action=None,
        *,
        verify_integrity=False,
    ) -> Series:
        """
        Map values of Series according to an input mapping or function.

        Used for substituting each value in a Series with another value,
        that may be derived from a remote function, ``dict``, or a :class:`Series`.

        If arg is a remote function, the overhead for remote functions
        applies. If mapping with a dict, fully deferred computation is possible.
        If mapping with a Series, fully deferred computation is only possible if
        verify_integrity=False.

        .. note::
            Bigframes does not yet support ``dict`` subclasses that define
            ``__missing__`` (i.e. provide a method for default values). These
            are treated the same as ``dict``.

        Args:
            arg (function, Mapping, Series):
                remote function, collections.abc.Mapping subclass or Series
                Mapping correspondence.
            na_action: (str, default None)
                Only None is currently supported, indicating that arg may
                map <NA> values to scalars. <NA> values won't be ignored.
                Passing 'ignore' will raise NotImplementedException.
            verify_integrity: (bool, default False)
                Only applies when arg is a Series. If True, throw if the Series
                index contains duplicate entries (this matches pandas behavior).
                If False, skip the expensive computation, and any duplicate
                index entries will produce duplicate rows in the result for each
                index entry.

        Returns:
            Series: Same index as caller.
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
