"""
Data structure for 1-dimensional cross-sectional and time series data
"""
from __future__ import annotations

from typing import (
    Hashable,
    IO,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from bigframes_vendored.pandas.core.generic import NDFrame
import numpy
import numpy as np
from pandas._typing import Axis, FilePath, NaPosition, WriteBuffer
from pandas.api import extensions as pd_ext

from bigframes import constants

if TYPE_CHECKING:
    from bigframes_vendored.pandas.core.frame import DataFrame
    from bigframes_vendored.pandas.core.groupby import SeriesGroupBy


class Series(NDFrame):  # type: ignore[misc]
    @property
    def dt(self):
        """
        Accessor object for datetime-like properties of the Series values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> seconds_series = bpd.Series(pd.date_range("2000-01-01", periods=3, freq="s"))
            >>> seconds_series
            0    2000-01-01 00:00:00
            1    2000-01-01 00:00:01
            2    2000-01-01 00:00:02
            dtype: timestamp[us][pyarrow]

            >>> seconds_series.dt.second
            0    0
            1    1
            2    2
            dtype: Int64

            >>> hours_series = bpd.Series(pd.date_range("2000-01-01", periods=3, freq="h"))
            >>> hours_series
            0    2000-01-01 00:00:00
            1    2000-01-01 01:00:00
            2    2000-01-01 02:00:00
            dtype: timestamp[us][pyarrow]

            >>> hours_series.dt.hour
            0    0
            1    1
            2    2
            dtype: Int64

            >>> quarters_series = bpd.Series(pd.date_range("2000-01-01", periods=3, freq="QE"))
            >>> quarters_series
            0    2000-03-31 00:00:00
            1    2000-06-30 00:00:00
            2    2000-09-30 00:00:00
            dtype: timestamp[us][pyarrow]

            >>> quarters_series.dt.quarter
            0    1
            1    2
            2    3
            dtype: Int64

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
            Index([10, 20, 30], dtype='Int64')
            >>> s.index.values
            array([10, 20, 30])

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
            MultiIndex([( 'Alice',  'Seattle'),
                        (   'Bob', 'New York'),
                        ('Aritra',     'Kona')],
                      names=['Name', 'Location'])
            >>> s1.index.values
            array([('Alice', 'Seattle'), ('Bob', 'New York'), ('Aritra', 'Kona')],
                  dtype=object)

        Returns:
            Index:
                The index object of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def shape(self):
        """Return a tuple of the shape of the underlying data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 4, 9, 16])
            >>> s.shape
            (4,)
            >>> s = bpd.Series(['Alice', 'Bob', bpd.NA])
            >>> s.shape
            (3,)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtype(self):
        """
        Return the dtype object of the underlying data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s.dtype
            Int64Dtype()
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def name(self) -> Hashable:
        """
        Return the name of the Series.

        The name of a Series becomes its index or column name if it is used
        to form a DataFrame. It is also used whenever displaying the Series
        using the interpreter.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        For a Series:

            >>> s = bpd.Series([1, 2, 3], dtype="Int64", name='Numbers')
            >>> s
            0    1
            1    2
            2    3
            Name: Numbers, dtype: Int64
            >>> s.name
            'Numbers'

            >>> s.name = "Integers"
            >>> s
            0    1
            1    2
            2    3
            Name: Integers, dtype: Int64

        If the Series is part of a DataFrame:

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df
               col1  col2
            0     1     3
            1     2     4
            <BLANKLINE>
            [2 rows x 2 columns]
            >>> s = df["col1"]
            >>> s.name
            'col1'

        Returns:
            hashable object:
                The name of the Series, also the column name
                if part of a DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def hasnans(self) -> bool:
        """
        Return True if there are any NaNs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, None])
            >>> s
            0     1.0
            1     2.0
            2     3.0
            3    <NA>
            dtype: Float64
            >>> s.hasnans
            np.True_

        Returns:
            bool
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def T(self) -> Series:
        """Return the transpose, which is by definition self.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Ant', 'Bear', 'Cow'])
            >>> s
            0     Ant
            1    Bear
            2     Cow
            dtype: string

            >>> s.T
            0     Ant
            1    Bear
            2     Cow
            dtype: string

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transpose(self) -> Series:
        """
        Return the transpose, which is by definition self.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Ant', 'Bear', 'Cow'])
            >>> s
            0     Ant
            1    Bear
            2     Cow
            dtype: string

            >>> s.transpose()
            0     Ant
            1    Bear
            2     Cow
            dtype: string

        Returns:
            bigframes.pandas.Series:
                Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def reset_index(
        self,
        *,
        drop: bool = False,
        name=pd_ext.no_default,
    ) -> DataFrame | Series | None:
        """
        Generate a new DataFrame or Series with the index reset.

        This is useful when the index needs to be treated as a column, or
        when the index is meaningless and needs to be reset to the default
        before another operation.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4], name='foo',
            ...                index=['a', 'b', 'c', 'd'])
            >>> s.index.name = "idx"
            >>> s
            idx
            a    1
            b    2
            c    3
            d    4
            Name: foo, dtype: Int64

        Generate a DataFrame with default index.

            >>> s.reset_index()
                idx  foo
            0     a    1
            1     b    2
            2     c    3
            3     d    4
            <BLANKLINE>
            [4 rows x 2 columns]

        To specify the name of the new column use ``name`` param.

            >>> s.reset_index(name="bar")
                idx   bar
            0     a    1
            1     b    2
            2     c    3
            3     d    4
            <BLANKLINE>
            [4 rows x 2 columns]

        To generate a new Series with the default index set param ``drop=True``.

            >>> s.reset_index(drop=True)
            0    1
            1    2
            2    3
            3    4
            Name: foo, dtype: Int64

            >>> arrays = [np.array(['bar', 'bar', 'baz', 'baz']),
            ...           np.array(['one', 'two', 'one', 'two'])]
            >>> s2 = bpd.Series(
            ...     range(4), name='foo',
            ...     index=pd.MultiIndex.from_arrays(arrays,
            ...                                     names=['a', 'b']))

        If level is not set, all levels are removed from the Index.

            >>> s2.reset_index()
                 a    b  foo
            0  bar  one    0
            1  bar  two    1
            2  baz  one    2
            3  baz  two    3
            <BLANKLINE>
            [4 rows x 3 columns]

        Args:
            drop (bool, default False):
                Just reset the index, without inserting it as a column in
                the new DataFrame.
            name (object, optional):
                The name to use for the column containing the original Series
                values. Uses ``self.name`` by default. This argument is ignored
                when `drop` is True.

        Returns:
            bigframes.pandas.Series or bigframes.pandas.DataFrame or None:
                When `drop` is False (the default),
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

    def keys(self):
        """
        Return alias for index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3], index=[0, 1, 2])
            >>> s.keys()
            Index([0, 1, 2], dtype='Int64')

        Returns:
            Index:
                Index of the Series.
        """
        return self.index

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
        *,
        allow_large_results: Optional[bool] = None,
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
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB.

        Returns:
            str or None:
                String representation of Series if ``buf=None``, otherwise None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_markdown(
        self,
        buf: IO[str] | None = None,
        mode: str = "wt",
        index: bool = True,
        *,
        allow_large_results: Optional[bool] = None,
        **kwargs,
    ) -> str | None:
        """
        Print Series in Markdown-friendly format.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["elk", "pig", "dog", "quetzal"], name="animal")
            >>> print(s.to_markdown())
            |    | animal   |
            |---:|:---------|
            |  0 | elk      |
            |  1 | pig      |
            |  2 | dog      |
            |  3 | quetzal  |

        Output markdown with a tabulate option.

            >>> print(s.to_markdown(tablefmt="grid"))
            +----+----------+
            |    | animal   |
            +====+==========+
            |  0 | elk      |
            +----+----------+
            |  1 | pig      |
            +----+----------+
            |  2 | dog      |
            +----+----------+
            |  3 | quetzal  |
            +----+----------+

        Args:
            buf (str, Path or StringIO-like, optional, default None):
                Buffer to write to. If None, the output is returned as a string.
            mode (str, optional):
                Mode in which file is opened, "wt" by default.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow
                large query results over the default size limit of 10 GB.
            index (bool, optional, default True):
                Add index (row) labels.

        Returns:
            str:
                Series in Markdown-friendly format.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_dict(
        self,
        into: type[dict] = dict,
        *,
        allow_large_results: Optional[bool] = None,
    ) -> Mapping:
        """
        Convert Series to {label -> value} dict or dict-like object.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> from collections import OrderedDict, defaultdict
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4])
            >>> s.to_dict()
            {np.int64(0): 1, np.int64(1): 2, np.int64(2): 3, np.int64(3): 4}

            >>> s.to_dict(into=OrderedDict)
            OrderedDict({np.int64(0): 1, np.int64(1): 2, np.int64(2): 3, np.int64(3): 4})

            >>> dd = defaultdict(list)
            >>> s.to_dict(into=dd)
            defaultdict(<class 'list'>, {np.int64(0): 1, np.int64(1): 2, np.int64(2): 3, np.int64(3): 4})

        Args:
            into (class, default dict):
                The collections.abc.Mapping subclass to use as the return
                object. Can be the actual class or an empty
                instance of the mapping type you want.  If you want a
                collections.defaultdict, you must pass it initialized.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB.

        Returns:
            collections.abc.Mapping:
                Key-value representation of Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_frame(self, name=None) -> DataFrame:
        """
        Convert Series to DataFrame.

        The column in the new dataframe will be named name (the keyword parameter)
        if the name parameter is provided and not None.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["a", "b", "c"],
            ...                name="vals")
            >>> s.to_frame()
              vals
            0    a
            1    b
            2    c
            <BLANKLINE>
            [3 rows x 1 columns]

        Args:
            name (Hashable, default None)

        Returns:
            bigframes.pandas.DataFrame:
                DataFrame representation of Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_excel(
        self,
        excel_writer,
        sheet_name,
        *,
        allow_large_results=None,
    ):
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
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_latex(
        self,
        buf=None,
        columns=None,
        header=True,
        index=True,
        *,
        allow_large_results=None,
        **kwargs,
    ):
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
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB.

        Returns:
            str or None:
                If buf is None, returns the result as a string.
                Otherwise returns None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def tolist(self, *, allow_large_results: Optional[bool] = None) -> list:
        """
        Return a list of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s
            0    1
            1    2
            2    3
            dtype: Int64

            >>> s.to_list()
            [1, 2, 3]

        Args:
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow
                large query results over the default size limit of 10 GB.

        Returns:
            list:
                list of the values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    to_list = tolist

    def to_numpy(
        self, dtype, copy=False, na_value=pd_ext.no_default, *, allow_large_results=None
    ):
        """
        A NumPy ndarray representing the values in this Series or Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series(pd.Categorical(['a', 'b', 'a']))
            >>> ser.to_numpy()
            array(['a', 'b', 'a'], dtype=object)

        Specify the dtype to control how datetime-aware data is represented. Use
        dtype=object to return an ndarray of pandas Timestamp objects, each with
        the correct tz.

            >>> ser = bpd.Series(pd.date_range('2000', periods=2, tz="CET"))
            >>> ser.to_numpy(dtype=object)
            array([Timestamp('1999-12-31 23:00:00+0000', tz='UTC'),
                   Timestamp('2000-01-01 23:00:00+0000', tz='UTC')], dtype=object)

        Or ``dtype=datetime64[ns]`` to return an ndarray of native datetime64 values.
        The values are converted to UTC and the timezone info is dropped.

            >>> ser.to_numpy(dtype="datetime64[ns]")
            array(['1999-12-31T23:00:00.000000000', '2000-01-01T23:00:00.000000000'],
                  dtype='datetime64[ns]')

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
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow
                large query results over the default size limit of 10 GB.
            ``**kwargs``:
                Additional keywords passed through to the ``to_numpy`` method
                of the underlying array (for extension arrays).

        Returns:
            numpy.ndarray:
                A NumPy ndarray representing the values in this
                Series or Index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_pickle(self, path, *, allow_large_results=None, **kwargs):
        """
        Pickle (serialize) object to file.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> original_df = bpd.DataFrame({"foo": range(5), "bar": range(5, 10)})
            >>> original_df
               foo  bar
            0    0    5
            1    1    6
            2    2    7
            3    3    8
            4    4    9
            <BLANKLINE>
            [5 rows x 2 columns]

            >>> original_df.to_pickle("./dummy.pkl")

            >>> unpickled_df = bpd.read_pickle("./dummy.pkl")
            >>> unpickled_df
               foo  bar
            0    0    5
            1    1    6
            2    2    7
            3    3    8
            4    4    9
            <BLANKLINE>
            [5 rows x 2 columns]

        Args:
            path (str, path object, or file-like object):
                String, path object (implementing ``os.PathLike[str]``), or file-like
                object implementing a binary ``write()`` function. File path where
                the pickled object will be stored.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow
                large query results over the default size limit of 10 GB.

        Returns:
            None
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_xarray(self, *, allow_large_results=None):
        """
        Return an xarray object from the pandas object.

        Returns:
            xarray.DataArray or xarray.Dataset:
                Data in the pandas structure
                converted to Dataset if the object is a DataFrame, or a DataArray if
                the object is a Series.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def agg(self, func):
        """
        Aggregate using one or more operations over the specified axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4])
            >>> s
            0    1
            1    2
            2    3
            3    4
            dtype: Int64

            >>> s.agg('min')
            np.int64(1)

            >>> s.agg(['min', 'max'])
            min    1
            max    4
            dtype: Int64

        Args:
            func (function):
                Function to use for aggregating the data.
                Accepted combinations are: string function name, list of
                function names, e.g. ``['sum', 'mean']``.

        Returns:
            scalar or bigframes.pandas.Series:
                Aggregated results.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def count(self):
        """
        Return number of non-NA/null observations in the Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0.0, 1.0, bpd.NA])
            >>> s
            0     0.0
            1     1.0
            2    <NA>
            dtype: Float64
            >>> s.count()
            np.int64(2)

        Returns:
            int or bigframes.pandas.Series (if level specified):
                Number of non-null values in the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self) -> int:
        """
        Return number of unique elements in the object.

        Excludes NA values by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 3, 5, 7, 7])
            >>> s
            0    1
            1    3
            2    5
            3    7
            4    7
            dtype: Int64

            >>> s.nunique()
            np.int64(4)

        Returns:
            int:
                number of unique elements in the object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def unique(self, keep_order=True) -> Series:
        """
        Return unique values of Series object.

        By default, uniques are returned in order of appearance. Hash table-based unique,
        therefore does NOT sort.

        Args:
            keep_order (bool, default True):
                If True, preserves the order of the first appearance of each unique value.
                If False, returns the elements in ascending order, which can be faster.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, 1, 3, 3], name='A')
            >>> s
            0    2
            1    1
            2    3
            3    3
            Name: A, dtype: Int64

        Example with order preservation: Slower, but keeps order

            >>> s.unique()
            0    2
            1    1
            2    3
            Name: A, dtype: Int64

        Example without order preservation: Faster, but loses original order

            >>> s.unique(keep_order=False)
            0    1
            1    2
            2    3
            Name: A, dtype: Int64

        Returns:
            bigframes.pandas.Series:
                The unique values returned as a Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mode(self) -> Series:
        """
        Return the mode(s) of the Series.

        The mode is the value that appears most often. There can be multiple modes.

        Always returns Series even if only one value is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, 4, 8, 2, 4, None])
            >>> s.mode()
            0    2.0
            1    4.0
            dtype: Float64

        Returns:
            bigframes.pandas.Series:
                Modes of the Series in sorted order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop_duplicates(
        self,
        *,
        keep="first",
    ) -> Series | None:
        """
        Return Series with duplicate values removed.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Generate a Series with duplicated entries.

            >>> s = bpd.Series(['llama', 'cow', 'llama', 'beetle', 'llama', 'hippo'],
            ...                name='animal')
            >>> s
            0     llama
            1       cow
            2     llama
            3    beetle
            4     llama
            5     hippo
            Name: animal, dtype: string

        With the 'keep' parameter, the selection behaviour of duplicated values
        can be changed. The value 'first' keeps the first occurrence for each set
        of duplicated entries. The default value of keep is 'first'.

            >>> s.drop_duplicates()
            0     llama
            1       cow
            3    beetle
            5     hippo
            Name: animal, dtype: string

        The value 'last' for parameter 'keep' keeps the last occurrence for
        each set of duplicated entries.

            >>> s.drop_duplicates(keep='last')
            1       cow
            3    beetle
            4     llama
            5     hippo
            Name: animal, dtype: string

        The value False for parameter 'keep' discards all sets of duplicated entries.

            >>> s.drop_duplicates(keep=False)
            1       cow
            3    beetle
            5     hippo
            Name: animal, dtype: string

        Args:
            keep ({'first', 'last', ``False``}, default 'first'):
                Method to handle dropping duplicates:

                'first' : Drop duplicates except for the first occurrence.
                'last' : Drop duplicates except for the last occurrence.
                ``False`` : Drop all duplicates.

        Returns:
            bigframes.pandas.Series:
                Series with duplicates dropped or None if ``inplace=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def duplicated(self, keep="first") -> Series:
        """
        Indicate duplicate Series values.

        Duplicated values are indicated as ``True`` values in the resulting
        Series. Either all duplicates, all except the first or all except the
        last occurrence of duplicates can be indicated.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        By default, for each set of duplicated values, the first occurrence is
        set on False and all others on True:

            >>> animals = bpd.Series(['llama', 'cow', 'llama', 'beetle', 'llama'])
            >>> animals.duplicated()
            0    False
            1    False
            2     True
            3    False
            4     True
            dtype: boolean

        which is equivalent to

            >>> animals.duplicated(keep='first')
            0    False
            1    False
            2     True
            3    False
            4     True
            dtype: boolean

        By using 'last', the last occurrence of each set of duplicated values
        is set on False and all others on True:

            >>> animals.duplicated(keep='last')
            0     True
            1    False
            2     True
            3    False
            4    False
            dtype: boolean

        By setting keep on False, all duplicates are True:

            >>> animals.duplicated(keep=False)
            0     True
            1    False
            2     True
            3    False
            4     True
            dtype: boolean

        Args:
            keep ({'first', 'last', False}, default 'first'):
                Method to handle dropping duplicates:

                'first' : Mark duplicates as ``True`` except for the first
                occurrence.
                'last' : Mark duplicates as ``True`` except for the last
                occurrence.
                ``False`` : Mark all duplicates as ``True``.

        Returns:
            bigframes.pandas.Series:
                Series indicating whether each value has occurred in the
                preceding values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmin(self) -> Hashable:
        """
        Return the row label of the minimum value.

        If multiple values equal the minimum, the first row label with that
        value is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(data=[1, None, 4, 1],
            ...                index=['A', 'B', 'C', 'D'])
            >>> s
            A     1.0
            B    <NA>
            C     4.0
            D     1.0
            dtype: Float64

            >>> s.idxmin()
            'A'

        Returns:
            Index: Label of the minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def idxmax(self) -> Hashable:
        """
        Return the row label of the maximum value.

        If multiple values equal the maximum, the first row label with that
        value is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(data=[1, None, 4, 3, 4],
            ...                index=['A', 'B', 'C', 'D', 'E'])
            >>> s
            A     1.0
            B    <NA>
            C     4.0
            D     3.0
            E     4.0
            dtype: Float64

            >>> s.idxmax()
            'C'

        Returns:
            Index: Label of the maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def round(self, decimals: int = 0) -> Series:
        """
        Round each value in a Series to the given number of decimals.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0.1, 1.3, 2.7])
            >>> s.round()
            0    0.0
            1    1.0
            2    3.0
            dtype: Float64

            >>> s = bpd.Series([0.123, 1.345, 2.789])
            >>> s.round(decimals=2)
            0    0.12
            1    1.34
            2    2.79
            dtype: Float64

        Args:
            decimals (int, default 0):
                Number of decimal places to round to. If decimals is negative,
                it specifies the number of positions to the left of the decimal point.

        Returns:
            bigframes.pandas.Series:
                Rounded values of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def explode(self, *, ignore_index: Optional[bool] = False) -> Series:
        """
        Transform each element of a list-like to a row.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([[1, 2, 3], [], [3, 4]])
            >>> s
            0    [1 2 3]
            1         []
            2      [3 4]
            dtype: list<item: int64>[pyarrow]

            >>> s.explode()
            0       1
            0       2
            0       3
            1    <NA>
            2       3
            2       4
            dtype: Int64

        Args:
            ignore_index (bool, default False):
                If True, the resulting index will be labeled 0, 1, …, n - 1.

        Returns:
            bigframes.pandas.Series:
                Exploded lists to rows; index will be duplicated for these rows.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def corr(self, other, method="pearson", min_periods=None) -> float:
        """
        Compute the correlation with the other Series.  Non-number values are ignored in the
        computation.

        Uses the "Pearson" method of correlation.  Numbers are converted to float before
        calculation, so the result may be unstable.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series([.2, .0, .6, .2])
            >>> s2 = bpd.Series([.3, .6, .0, .1])
            >>> s1.corr(s2)
            np.float64(-0.8510644963469901)

            >>> s1 = bpd.Series([1, 2, 3], index=[0, 1, 2])
            >>> s2 = bpd.Series([1, 2, 3], index=[2, 1, 0])
            >>> s1.corr(s2)
            np.float64(-1.0)

        Args:
            other (Series):
                The series with which this is to be correlated.
            method (string, default "pearson"):
                Correlation method to use - currently only "pearson" is supported.
            min_periods (int, default None):
                The minimum number of observations needed to return a result.  Non-default values
                are not yet supported, so a result will be returned for at least two observations.

        Returns:
            float:
                Will return NaN if there are fewer than two numeric pairs, either series has a
                variance or covariance of zero, or any input value is infinite.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def autocorr(self, lag: int = 1) -> float:
        """
        Compute the lag-N autocorrelation.

        This method computes the Pearson correlation between
        the Series and its shifted self.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0.25, 0.5, 0.2, -0.05])
            >>> s.autocorr()  # doctest: +ELLIPSIS
            np.float64(0.10355263309024067)

            >>> s.autocorr(lag=2)
            np.float64(-1.0)

        If the Pearson correlation is not well defined, then 'NaN' is returned.

            >>> s = bpd.Series([1, 0, 0, 0])
            >>> s.autocorr()
            np.float64(nan)

        Args:
            lag (int, default 1):
                Number of lags to apply before performing autocorrelation.

        Returns:
            float:
                The Pearson correlation between self and self.shift(lag).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cov(
        self,
        other,
    ) -> float:
        """
        Compute covariance with Series, excluding missing values.

        The two `Series` objects are not required to be the same length and
        will be aligned internally before the covariance is calculated.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series([0.90010907, 0.13484424, 0.62036035])
            >>> s2 = bpd.Series([0.12528585, 0.26962463, 0.51111198])
            >>> s1.cov(s2)
            np.float64(-0.01685762652715874)

        Args:
            other (Series):
                Series with which to compute the covariance.

        Returns:
            float:
                Covariance between Series and other normalized by N-1
                (unbiased estimator).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def diff(self) -> Series:
        """
        First discrete difference of element.

        Calculates the difference of a Series element compared with another
        element in the Series (default is element in previous row).


        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Difference with previous row

            >>> s = bpd.Series([1, 1, 2, 3, 5, 8])
            >>> s.diff()
            0    <NA>
            1       0
            2       1
            3       1
            4       2
            5       3
            dtype: Int64

        Difference with 3rd previous row

            >>> s.diff(periods=3)
            0    <NA>
            1    <NA>
            2    <NA>
            3       2
            4       4
            5       6
            dtype: Int64

        Difference with following row

            >>> s.diff(periods=-1)
            0       0
            1      -1
            2      -1
            3      -2
            4      -3
            5    <NA>
            dtype: Int64

        Args:
            periods (int, default 1):
                Periods to shift for calculating difference, accepts negative
                values.

        Returns:
            bigframes.pandas.Series:
                First differences of the Series.
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
            np.int64(8)

        You can also use the operator ``@`` for the dot product:

            >>> s @ other
            np.int64(8)

        Args:
            other (Series):
                The other object to compute the dot product with its columns.

        Returns:
            scalar, bigframes.pandas.Series or numpy.ndarray:
                Return the dot product of the Series
                and other if other is a Series, the Series of the dot product of
                Series and each rows of other if other is a DataFrame or a
                numpy.ndarray between the Series and each columns of the numpy array.


        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __matmul__(self, other):
        """
        Matrix multiplication using binary `@` operator.
        """
        return NotImplemented

    def __rmatmul__(self, other):
        """
        Matrix multiplication using binary `@` operator.
        """
        return NotImplemented

    def sort_values(
        self,
        *,
        axis: Axis = 0,
        inplace: bool = False,
        ascending: bool | int | Sequence[bool] | Sequence[int] = True,
        kind: str = "quicksort",
        na_position: str = "last",
    ):
        """
        Sort by the values.

        Sort a Series in ascending or descending order by some
        criterion.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([np.nan, 1, 3, 10, 5])
            >>> s
            0    <NA>
            1     1.0
            2     3.0
            3    10.0
            4     5.0
            dtype: Float64

        Sort values ascending order (default behaviour):

            >>> s.sort_values(ascending=True)
            1     1.0
            2     3.0
            4     5.0
            3    10.0
            0    <NA>
            dtype: Float64

        Sort values descending order:

            >>> s.sort_values(ascending=False)
            3    10.0
            4     5.0
            2     3.0
            1     1.0
            0    <NA>
            dtype: Float64

        Sort values putting NAs first:

            >>> s.sort_values(na_position='first')
            0    <NA>
            1     1.0
            2     3.0
            4     5.0
            3    10.0
            dtype: Float64

        Sort a series of strings:

            >>> s = bpd.Series(['z', 'b', 'd', 'a', 'c'])
            >>> s
            0    z
            1    b
            2    d
            3    a
            4    c
            dtype: string

            >>> s.sort_values()
            3    a
            1    b
            4    c
            2    d
            0    z
            dtype: string

        Args:
            axis (0 or 'index'):
                Unused. Parameter needed for compatibility with DataFrame.
            inplace (bool, default False):
                Whether to modify the Series rather than creating a new one.
            ascending (bool or list of bools, default True):
                If True, sort values in ascending order, otherwise descending.
            kind (str, default to 'quicksort'):
                Choice of sorting algorithm. Accepts quicksort', 'mergesort',
                'heapsort', 'stable'. Ignored except when determining whether to
                sort stably. 'mergesort' or 'stable' will result in stable reorder
            na_position ({'first' or 'last'}, default 'last'):
                Argument 'first' puts NaNs at the beginning, 'last' puts NaNs at
                the end.

        Returns:
            bigframes.pandas.Series or None:
                Series ordered by values or None if ``inplace=True``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sort_index(
        self,
        *,
        axis: Axis = 0,
        inplace: bool = False,
        ascending: bool | Sequence[bool] = True,
        na_position: NaPosition = "last",
    ):
        """
        Sort Series by index labels.

        Returns a new Series sorted by label if `inplace` argument is
        ``False``, otherwise updates the original series and returns None.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['a', 'b', 'c', 'd'], index=[3, 2, 1, 4])
            >>> s.sort_index()
            1    c
            2    b
            3    a
            4    d
            dtype: string

        Sort Descending

            >>> s.sort_index(ascending=False)
            4    d
            3    a
            2    b
            1    c
            dtype: string

        By default NaNs are put at the end, but use na_position to place them at
        the beginning

            >>> s = bpd.Series(['a', 'b', 'c', 'd'], index=[3, 2, 1, np.nan])
            >>> s.sort_index(na_position='first')
            <NA>    d
            1.0     c
            2.0     b
            3.0     a
            dtype: string

        Args:
            axis ({0 or 'index'}):
                Unused. Parameter needed for compatibility with DataFrame.
            inplace (bool, default False):
                Whether to modify the Series rather than creating a new one.
            ascending (bool or list-like of bools, default True):
                Sort ascending vs. descending. When the index is a MultiIndex the
                sort direction can be controlled for each level individually.
            na_position ({'first', 'last'}, default 'last'):
                If 'first' puts NaNs at the beginning, 'last' puts NaNs at the end.
                Not implemented for MultiIndex.

        Returns:
            bigframes.pandas.Series or None:
                The original Series sorted by the labels or None if
                ``inplace=True``.

        """

        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nlargest(
        self, n: int = 5, keep: Literal["first", "last", "all"] = "first"
    ) -> Series:
        """
        Return the largest `n` elements.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> countries_population = {"Italy": 59000000, "France": 65000000,
            ...                          "Malta": 434000, "Maldives": 434000,
            ...                          "Brunei": 434000, "Iceland": 337000,
            ...                          "Nauru": 11300, "Tuvalu": 11300,
            ...                          "Anguilla": 11300, "Montserrat": 5200}
            >>> s = bpd.Series(countries_population)
            >>> s
            Italy         59000000
            France        65000000
            Malta           434000
            Maldives        434000
            Brunei          434000
            Iceland         337000
            Nauru            11300
            Tuvalu           11300
            Anguilla         11300
            Montserrat        5200
            dtype: Int64

        The n largest elements where `n=5` by default.

            >>> s.nlargest()
            France      65000000
            Italy       59000000
            Malta         434000
            Maldives      434000
            Brunei        434000
            dtype: Int64

        The n largest elements where `n=3`. Default keep value is `first` so Malta
          will be kept.

            >>> s.nlargest(3)
            France    65000000
            Italy     59000000
            Malta       434000
            dtype: Int64

        The n largest elements where `n=3` and keeping the last duplicates. Brunei
        will be kept since it is the last with value 434000 based on the index order.

            >>> s.nlargest(3, keep='last')
            France    65000000
            Italy     59000000
            Brunei      434000
            dtype: Int64

        The n largest elements where n`=3` with all duplicates kept. Note that the
        returned Series has five elements due to the three duplicates.

            >>> s.nlargest(3, keep='all')
            France      65000000
            Italy       59000000
            Malta         434000
            Maldives      434000
            Brunei        434000
            dtype: Int64

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
            bigframes.pandas.Series:
                The `n` largest values in the Series, sorted in decreasing order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nsmallest(self, n: int = 5, keep: str = "first") -> Series:
        """
        Return the smallest `n` elements.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> countries_population = {"Italy": 59000000, "France": 65000000,
            ...                          "Malta": 434000, "Maldives": 434000,
            ...                          "Brunei": 434000, "Iceland": 337000,
            ...                          "Nauru": 11300, "Tuvalu": 11300,
            ...                          "Anguilla": 11300, "Montserrat": 5200}
            >>> s = bpd.Series(countries_population)
            >>> s
            Italy         59000000
            France        65000000
            Malta           434000
            Maldives        434000
            Brunei          434000
            Iceland         337000
            Nauru            11300
            Tuvalu           11300
            Anguilla         11300
            Montserrat        5200
            dtype: Int64

        The n smallest elements where `n=5` by default.

            >>> s.nsmallest()
            Montserrat      5200
            Nauru          11300
            Tuvalu         11300
            Anguilla       11300
            Iceland       337000
            dtype: Int64

        The n smallest elements where `n=3`. Default keep value is `first` so
        Nauru and Tuvalu will be kept.

            >>> s.nsmallest(3)
            Montserrat     5200
            Nauru         11300
            Tuvalu        11300
            dtype: Int64

        The n smallest elements where `n=3` with all duplicates kept. Note that
        the returned Series has four elements due to the three duplicates.

            >>> s.nsmallest(3, keep='all')
            Montserrat     5200
            Nauru         11300
            Tuvalu        11300
            Anguilla      11300
            dtype: Int64

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
            bigframes.pandas.Series:
                The `n` smallest values in the Series, sorted in increasing order.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # function application

    def apply(
        self,
        func,
        by_row="compat",
    ) -> DataFrame | Series:
        """
        Invoke function on values of a Series.

        Can be ufunc (a NumPy function that applies to the entire Series) or a
        Python function that only works on single values. If it is an arbitrary
        python function then converting it into a `remote_function` is recommended.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        For applying arbitrary python function a `remote_function` is recommended.
        Let's use ``reuse=False`` flag to make sure a new `remote_function`
        is created every time we run the following code, but you can skip it
        to potentially reuse a previously deployed `remote_function` from
        the same user defined function.

            >>> @bpd.remote_function(reuse=False, cloud_function_service_account="default")
            ... def minutes_to_hours(x: int) -> float:
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

        To turn a user defined function with external package dependencies into
        a `remote_function`, you would provide the names of the packages via
        `packages` param.

            >>> @bpd.remote_function(
            ...     reuse=False,
            ...     packages=["cryptography"],
            ...     cloud_function_service_account="default"
            ... )
            ... def get_hash(input: str) -> str:
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

        You could return an array output from the remote function.

            >>> @bpd.remote_function(reuse=False, cloud_function_service_account="default")
            ... def text_analyzer(text: str) -> list[int]:
            ...     words = text.count(" ") + 1
            ...     periods = text.count(".")
            ...     exclamations = text.count("!")
            ...     questions = text.count("?")
            ...     return [words, periods, exclamations, questions]

            >>> texts = bpd.Series([
            ...     "The quick brown fox jumps over the lazy dog.",
            ...     "I love this product! It's amazing.",
            ...     "Hungry? Wanna eat? Lets go!"
            ... ])
            >>> features = texts.apply(text_analyzer)
            >>> features
            0    [9 1 0 0]
            1    [6 1 1 0]
            2    [5 0 1 2]
            dtype: list<item: int64>[pyarrow]

        Simple vectorized functions, lambdas or ufuncs can be applied directly
        with `by_row=False`.

            >>> nums = bpd.Series([1, 2, 3, 4])
            >>> nums
            0    1
            1    2
            2    3
            3    4
            dtype: Int64
            >>> nums.apply(lambda x: x*x + 2*x + 1, by_row=False)
            0     4
            1     9
            2    16
            3    25
            dtype: Int64

            >>> def is_odd(num):
            ...     return num % 2 == 1
            >>> nums.apply(is_odd, by_row=False)
            0     True
            1    False
            2     True
            3    False
            dtype: boolean

            >>> nums.apply(np.log, by_row=False)
            0         0.0
            1    0.693147
            2    1.098612
            3    1.386294
            dtype: Float64

        Args:
            func (function):
                BigFrames DataFrames ``remote_function`` to apply. The function
                should take a scalar and return a scalar. It will be applied to
                every element in the ``Series``.
            by_row (False or "compat", default "compat"):
                If `"compat"` , func must be a remote function which will be
                passed each element of the Series, like `Series.map`. If False,
                the func will be passed the whole Series at once.

        Returns:
            bigframes.pandas.Series:
                A new Series with values representing the
                return value of the ``func`` applied to each element of the
                original Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def combine(
        self,
        other: Series | Hashable,
        func,
    ) -> Series:
        """
        Combine the Series with a Series or scalar according to `func`.

        Combine the Series and `other` using `func` to perform elementwise
        selection for combined Series.
        `fill_value` is assumed when value is missing at some index
        from one of the two objects being combined.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

        Consider 2 Datasets ``s1`` and ``s2`` containing
        highest clocked speeds of different birds.

            >>> s1 = bpd.Series({'falcon': 330.0, 'eagle': 160.0})
            >>> s1
            falcon    330.0
            eagle     160.0
            dtype: Float64
            >>> s2 = bpd.Series({'falcon': 345.0, 'eagle': 200.0, 'duck': 30.0})
            >>> s2
            falcon    345.0
            eagle     200.0
            duck       30.0
            dtype: Float64

        Now, to combine the two datasets and view the highest speeds
        of the birds across the two datasets

            >>> s1.combine(s2, np.maximum)
            falcon    345.0
            eagle     200.0
            duck       <NA>
            dtype: Float64

        Args:
            other (Series or scalar):
                The value(s) to be combined with the `Series`.
            func (function):
                BigFrames DataFrames ``remote_function`` to apply.
                Takes two scalars as inputs and returns an element.
                Also accepts some numpy binary functions.

        Returns:
            bigframes.pandas.Series:
                The result of combining the Series with the other object.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can group by a named index level.

            >>> s = bpd.Series([380, 370., 24., 26.],
            ...                index=["Falcon", "Falcon", "Parrot", "Parrot"],
            ...                name="Max Speed")
            >>> s.index.name="Animal"
            >>> s
            Animal
            Falcon    380.0
            Falcon    370.0
            Parrot     24.0
            Parrot     26.0
            Name: Max Speed, dtype: Float64
            >>> s.groupby("Animal").mean()
            Animal
            Falcon    375.0
            Parrot     25.0
            Name: Max Speed, dtype: Float64

        You can also group by more than one index levels.

            >>> import pandas as pd
            >>> s = bpd.Series([380, 370., 24., 26.],
            ...                index=pd.MultiIndex.from_tuples(
            ...                    [("Falcon", "Clear"),
            ...                     ("Falcon", "Cloudy"),
            ...                     ("Parrot", "Clear"),
            ...                     ("Parrot", "Clear")],
            ...                    names=["Animal", "Sky"]),
            ...                name="Max Speed")
            >>> s
            Animal    Sky
            Falcon  Clear     380.0
                    Cloudy    370.0
            Parrot  Clear      24.0
                    Clear      26.0
            Name: Max Speed, dtype: Float64

            >>> s.groupby("Animal").mean()
            Animal
            Falcon    375.0
            Parrot     25.0
            Name: Max Speed, dtype: Float64

            >>> s.groupby("Sky").mean()
            Sky
            Clear     143.333333
            Cloudy         370.0
            Name: Max Speed, dtype: Float64

            >>> s.groupby(["Animal", "Sky"]).mean()
            Animal  Sky
            Falcon  Clear     380.0
                    Cloudy    370.0
            Parrot  Clear      25.0
            Name: Max Speed, dtype: Float64

        You can also group by values in a Series provided the index matches with
        the original series.

            >>> df = bpd.DataFrame({'Animal': ['Falcon', 'Falcon', 'Parrot', 'Parrot'],
            ...                     'Max Speed': [380., 370., 24., 26.],
            ...                     'Age': [10., 20., 4., 6.]})
            >>> df
            Animal  Max Speed   Age
            0  Falcon      380.0  10.0
            1  Falcon      370.0  20.0
            2  Parrot       24.0   4.0
            3  Parrot       26.0   6.0
            <BLANKLINE>
            [4 rows x 3 columns]

            >>> df['Max Speed'].groupby(df['Animal']).mean()
            Animal
            Falcon    375.0
            Parrot     25.0
            Name: Max Speed, dtype: Float64

            >>> df['Age'].groupby(df['Animal']).max()
            Animal
            Falcon    20.0
            Parrot     6.0
            Name: Age, dtype: Float64

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
            bigframes.core.groupby.SeriesGroupBy:
                Returns a groupby object that contains
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(data=np.arange(3), index=['A', 'B', 'C'])
            >>> s
            A    0
            B    1
            C    2
            dtype: Int64

        Drop labels B and C:

            >>> s.drop(labels=['B', 'C'])
            A    0
            dtype: Int64

        Drop 2nd level label in MultiIndex Series:

            >>> import pandas as pd
            >>> midx = pd.MultiIndex(levels=[['llama', 'cow', 'falcon'],
            ...                              ['speed', 'weight', 'length']],
            ...                      codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
            ...                             [0, 1, 2, 0, 1, 2, 0, 1, 2]])

            >>> s = bpd.Series([45, 200, 1.2, 30, 250, 1.5, 320, 1, 0.3],
            ...               index=midx)
            >>> s
            llama   speed      45.0
                    weight    200.0
                    length      1.2
            cow     speed      30.0
                    weight    250.0
                    length      1.5
            falcon  speed     320.0
                    weight      1.0
                    length      0.3
            dtype: Float64

            >>> s.drop(labels='weight', level=1)
            llama   speed      45.0
                    length      1.2
            cow     speed      30.0
                    length      1.5
            falcon  speed     320.0
                    length      0.3
            dtype: Float64

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
            bigframes.pandas.Series or None:
                Series with specified index labels removed
                or None if ``inplace=True``.

        Raises:
            KeyError:
                If none of the labels are found in the index.
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
            bigframes.pandas.Series:
                Series with levels swapped in MultiIndex
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
            bigframes.pandas.Series:
                Series with requested index / column level(s) removed.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def interpolate(self, method: str = "linear"):
        """
        Fill NaN values using an interpolation method.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

        Filling in NaN in a Series via linear interpolation.

            >>> s = bpd.Series([0, 1, np.nan, 3])
            >>> s
            0     0.0
            1     1.0
            2    <NA>
            3     3.0
            dtype: Float64

            >>> s.interpolate()
            0    0.0
            1    1.0
            2    2.0
            3    3.0
            dtype: Float64

        Args:
            method (str, default 'linear'):
                Interpolation technique to use. Only 'linear' supported.
                'linear': Ignore the index and treat the values as equally spaced.
                This is the only method supported on MultiIndexes.
                'index', 'values': use the actual numerical values of the index.
                'pad': Fill in NaNs using existing values.
                'nearest', 'zero', 'slinear': Emulates `scipy.interpolate.interp1d`
        Returns:
            bigframes.pandas.Series:
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([np.nan, 2, np.nan, -1])
            >>> s
            0    <NA>
            1     2.0
            2    <NA>
            3    -1.0
            dtype: Float64

        Replace all NA elements with 0s.

            >>> s.fillna(0)
            0    0.0
            1    2.0
            2    0.0
            3   -1.0
            dtype: Float64

        You can use fill values from another Series:

            >>> s_fill = bpd.Series([11, 22, 33])
            >>> s.fillna(s_fill)
            0    11.0
            1     2.0
            2    33.0
            3    -1.0
            dtype: Float64

        Args:
            value (scalar, dict, Series, or DataFrame, default None):
                Value to use to fill holes (e.g. 0).

        Returns:
            bigframes.pandas.Series or None:
                Object with missing values filled or None.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4, 5])
            >>> s
            0    1
            1    2
            2    3
            3    4
            4    5
            dtype: Int64

            >>> s.replace(1, 5)
            0    5
            1    2
            2    3
            3    4
            4    5
            dtype: Int64

        You can replace a list of values:

            >>> s.replace([1, 3, 5], -1)
            0    -1
            1     2
            2    -1
            3     4
            4    -1
            dtype: Int64

        You can use a replacement mapping:

            >>> s.replace({1: 5, 3: 10})
            0     5
            1     2
            2    10
            3     4
            4     5
            dtype: Int64

        With a string Series you can use a simple string replacement or a regex
        replacement:

            >>> s = bpd.Series(["Hello", "Another Hello"])
            >>> s.replace("Hello", "Hi")
            0               Hi
            1    Another Hello
            dtype: string

            >>> s.replace("Hello", "Hi", regex=True)
            0            Hi
            1    Another Hi
            dtype: string

            >>> s.replace("^Hello", "Hi", regex=True)
            0               Hi
            1    Another Hello
            dtype: string

            >>> s.replace("Hello$", "Hi", regex=True)
            0            Hi
            1    Another Hi
            dtype: string

            >>> s.replace("[Hh]e", "__", regex=True)
            0            __llo
            1    Anot__r __llo
            dtype: string

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
            bigframes.pandas.Series or bigframes.pandas.DataFrame:
                Object after replacement.

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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

        Drop NA values from a Series:

            >>> ser = bpd.Series([1., 2., np.nan])
            >>> ser
            0     1.0
            1     2.0
            2    <NA>
            dtype: Float64

            >>> ser.dropna()
            0    1.0
            1    2.0
            dtype: Float64

        Empty strings are not considered NA values. ``None`` is considered an NA value.

            >>> ser = bpd.Series(['2', bpd.NA, '', None, 'I stay'], dtype='object')
            >>> ser
            0         2
            1      <NA>
            2
            3      <NA>
            4    I stay
            dtype: string

            >>> ser.dropna()
            0         2
            2
            4    I stay
            dtype: string

        Args:
            axis (0 or 'index'):
                Unused. Parameter needed for compatibility with DataFrame.
            inplace (bool, default False):
                Unsupported, do not set.
            how (str, optional):
                Not in use. Kept for compatibility.

        Returns:
            bigframes.pandas.Series:
                Series with NA entries dropped from it.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

        Boundary values are included by default:

            >>> s = bpd.Series([2, 0, 4, 8, np.nan])
            >>> s.between(1, 4)
            0     True
            1    False
            2     True
            3    False
            4     <NA>
            dtype: boolean

        With inclusive set to "neither" boundary values are excluded:

            >>> s.between(1, 4, inclusive="neither")
            0     True
            1    False
            2    False
            3    False
            4     <NA>
            dtype: boolean

        left and right can be any scalar value:

            >>> s = bpd.Series(['Alice', 'Bob', 'Carol', 'Eve'])
            >>> s.between('Anna', 'Daniel')
            0    False
            1     True
            2     True
            3    False
            dtype: boolean

        Args:
            left (scalar or list-like):
                Left boundary.
            right (scalar or list-like):
                Right boundary.
            inclusive ({"both", "neither", "left", "right"}):
                Include boundaries. Whether to set each bound as closed or open.

        Returns:
            bigframes.pandas.Series:
                Series representing whether each element is between left and
                right (inclusive).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def case_when(
        self,
        caselist: List[Tuple[Series, Series]],
    ) -> Series:
        """Replace values where the conditions are True.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> c = bpd.Series([6, 7, 8, 9], name="c")
            >>> a = bpd.Series([0, 0, 1, 2])
            >>> b = bpd.Series([0, 3, 4, 5])

            >>> c.case_when(
            ...     caselist=[
            ...         (a.gt(0), a),  # condition, replacement
            ...         (b.gt(0), b),
            ...     ]
            ... )
            0    6
            1    3
            2    1
            3    2
            Name: c, dtype: Int64

        If you'd like to change the type, add a case with the condition True at the end of the case list

            >>> c.case_when(
            ...     caselist=[
            ...         (a.gt(0), 'a'),  # condition, replacement
            ...         (b.gt(0), 'b'),
            ...         (True, 'c'),
            ...     ]
            ... )
            0    c
            1    b
            2    a
            3    a
            Name: c, dtype: string

        **See also:**

        - :func:`bigframes.pandas.Series.mask` : Replace values where the condition is True.

        Args:
            caselist (A list of tuples of conditions and expected replacements):
                Takes the form:  ``(condition0, replacement0)``,
                ``(condition1, replacement1)``, ... .
                ``condition`` should be a 1-D boolean array-like object
                or a callable. If ``condition`` is a callable,
                it is computed on the Series
                and should return a boolean Series or array.
                The callable must not change the input Series
                (though pandas doesn`t check it). ``replacement`` should be a
                1-D array-like object, a scalar or a callable.
                If ``replacement`` is a callable, it is computed on the Series
                and should return a scalar or Series. The callable
                must not change the input Series
                (though pandas doesn`t check it).

        Returns:
            bigframes.pandas.Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumprod(self):
        """
        Return cumulative product over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        product.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, np.nan, 5, -1, 0])
            >>> s
            0     2.0
            1    <NA>
            2     5.0
            3    -1.0
            4     0.0
            dtype: Float64

        By default, NA values are ignored.

            >>> s.cumprod()
            0     2.0
            1    <NA>
            2    10.0
            3   -10.0
            4     0.0
            dtype: Float64

        Returns:
            bigframes.pandas.Series:
                Return cumulative sum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumsum(self):
        """
        Return cumulative sum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        sum.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, np.nan, 5, -1, 0])
            >>> s
            0     2.0
            1    <NA>
            2     5.0
            3    -1.0
            4     0.0
            dtype: Float64

        By default, NA values are ignored.

            >>> s.cumsum()
            0     2.0
            1    <NA>
            2     7.0
            3     6.0
            4     6.0
            dtype: Float64

        Args:
            axis ({0 or 'index', 1 or 'columns'}, default 0):
                    The index or the name of the axis. 0 is equivalent to None or 'index'.
                    For `Series` this parameter is unused and defaults to 0.

        Returns:
            bigframes.pandas.Series:
                Return cumulative sum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummax(self):
        """
        Return cumulative maximum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        maximum.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, np.nan, 5, -1, 0])
            >>> s
            0     2.0
            1    <NA>
            2     5.0
            3    -1.0
            4     0.0
            dtype: Float64

        By default, NA values are ignored.

            >>> s.cummax()
            0     2.0
            1    <NA>
            2     5.0
            3     5.0
            4     5.0
            dtype: Float64


        Returns:
            bigframes.pandas.Series:
                Return cumulative maximum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummin(self):
        """
        Return cumulative minimum over a DataFrame or Series axis.

        Returns a DataFrame or Series of the same size containing the cumulative
        minimum.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([2, np.nan, 5, -1, 0])
            >>> s
            0     2.0
            1    <NA>
            2     5.0
            3    -1.0
            4     0.0
            dtype: Float64

        By default, NA values are ignored.

            >>> s.cummin()
            0     2.0
            1    <NA>
            2     2.0
            3    -1.0
            4    -1.0
            dtype: Float64

        Returns:
            bigframes.pandas.Series:
                Return cumulative minimum of scalar or Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def eq(self, other) -> Series:
        """Return equal of Series and other, element-wise (binary operator eq).

        Equivalent to ``other == series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.eq(b)
            a    True
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: boolean

        Args:
            other (Series or scalar value)

        Returns:
            Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ne(self, other) -> Series:
        """Return not equal of Series and other, element-wise (binary operator ne).

        Equivalent to ``other != series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.ne(b)
            a    False
            b     <NA>
            c     <NA>
            d     <NA>
            e     <NA>
            dtype: boolean

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def le(self, other) -> Series:
        """Get 'less than or equal to' of Series and other, element-wise (binary
        operator le).

        Equivalent to ``series <= other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.le(b)
            a    True
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: boolean

        Args:
            other: Series, or scalar value

        Returns:
            bigframes.pandas.Series:
                The result of the comparison.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def lt(self, other) -> Series:
        """Get 'less than' of Series and other, element-wise (binary operator lt).

         Equivalent to ``series < other``, but with support to substitute a
         fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.lt(b)
            a    False
            b     <NA>
            c     <NA>
            d     <NA>
            e     <NA>
            dtype: boolean

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def ge(self, other) -> Series:
        """Get 'greater than or equal to' of Series and other, element-wise
        (binary operator ge).

        Equivalent to ``series >= other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.ge(b)
            a    True
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: boolean

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def gt(self, other) -> Series:
        """Return Greater than of series and other, element-wise
        (binary operator gt).

        Equivalent to ``series <= other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.gt(b)
            a    False
            b     <NA>
            c     <NA>
            d     <NA>
            e     <NA>
            dtype: boolean

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series: The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def add(self, other) -> Series:
        """Return addition of Series and other, element-wise (binary operator
        add).

        Equivalent to ``series + other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 2, 3, bpd.NA])
            >>> a
            0       1
            1       2
            2       3
            3    <NA>
            dtype: Int64

            >>> b = bpd.Series([10, 20, 30, 40])
            >>> b
            0     10
            1     20
            2     30
            3     40
            dtype: Int64

            >>> a.add(b)
            0      11
            1      22
            2      33
            3    <NA>
            dtype: Int64

        You can also use the mathematical operator ``+``:

            >>> a + b
            0      11
            1      22
            2      33
            3    <NA>
            dtype: Int64

        Adding two Series with explicit indexes:

            >>> a = bpd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
            >>> b = bpd.Series([10, 20, 30, 40], index=['a', 'b', 'd', 'e'])
            >>> a.add(b)
            a      11
            b      22
            c    <NA>
            d      34
            e    <NA>
            dtype: Int64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __add__(self, other):
        """Get addition of Series and other, element-wise, using operator `+`.

        Equivalent to `Series.add(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1.5, 2.6], index=['elk', 'moose'])
            >>> s
            elk      1.5
            moose    2.6
            dtype: Float64

        You can add a scalar.

            >>> s + 1.5
            elk      3.0
            moose    4.1
            dtype: Float64

        You can add another Series with index aligned.

            >>> delta = bpd.Series([1.5, 2.6], index=['elk', 'moose'])
            >>> s + delta
            elk      3.0
            moose    5.2
            dtype: Float64

        Adding any mis-aligned index will result in invalid values.

            >>> delta = bpd.Series([1.5, 2.6], index=['moose', 'bison'])
            >>> s + delta
            elk      <NA>
            moose     4.1
            bison    <NA>
            dtype: Float64

        Args:
            other (scalar or Series):
                Object to be added to the Series.

        Returns:
            bigframes.pandas.Series:
                The result of adding `other` to Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def radd(self, other) -> Series:
        """Return addition of Series and other, element-wise (binary operator
        radd).

        Equivalent to ``other + series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.add(b)
            a     2.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series, or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __radd__(self, other):
        """Get addition of Series and other, element-wise, using operator `+`.

        Equivalent to `Series.radd(other)`.

        Args:
            other (scalar or Series):
                Object to which Series should be added.

        Returns:
            bigframes.pandas.Series:
                The result of adding Series to `other`.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sub(
        self,
        other,
    ) -> Series:
        """Return subtraction of Series and other, element-wise (binary operator
        sub).

        Equivalent to ``series - other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.subtract(b)
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series, or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __sub__(self, other):
        """Get subtraction of other from Series, element-wise, using operator `-`.

        Equivalent to `Series.sub(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1.5, 2.6], index=['elk', 'moose'])
            >>> s
            elk      1.5
            moose    2.6
            dtype: Float64

        You can subtract a scalar.

            >>> s - 1.5
            elk      0.0
            moose    1.1
            dtype: Float64

        You can subtract another Series with index aligned.

            >>> delta = bpd.Series([0.5, 1.0], index=['elk', 'moose'])
            >>> s - delta
            elk      1.0
            moose    1.6
            dtype: Float64

        Adding any mis-aligned index will result in invalid values.

            >>> delta = bpd.Series([0.5, 1.0], index=['moose', 'bison'])
            >>> s - delta
            elk      <NA>
            moose     2.1
            bison    <NA>
            dtype: Float64

        Args:
            other (scalar or Series):
                Object to subtract from the Series.

        Returns:
            bigframes.pandas.Series:
                The result of subtraction.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rsub(self, other) -> Series:
        """Return subtraction of Series and other, element-wise (binary operator
        rsub).

        Equivalent to ``other - series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.subtract(b)
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series, or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rsub__(self, other):
        """Get subtraction of Series from other, element-wise, using operator `-`.

        Equivalent to `Series.rsub(other)`.

        Args:
            other (scalar or Series):
                Object to subtract the Series from.

        Returns:
            bigframes.pandas.Series:
                The result of subtraction.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mul(self, other) -> Series:
        """Return multiplication of Series and other, element-wise (binary
        operator mul).

        Equivalent to ``other * series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.multiply(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __mul__(self, other):
        """
        Get multiplication of Series with other, element-wise, using operator `*`.

        Equivalent to `Series.mul(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can multiply with a scalar:

            >>> s = bpd.Series([1, 2, 3])
            >>> s * 3
            0    3
            1    6
            2    9
            dtype: Int64

        You can also multiply with another Series:

            >>> s1 = bpd.Series([2, 3, 4])
            >>> s * s1
            0     2
            1     6
            2    12
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to multiply with the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the multiplication.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rmul(self, other) -> Series:
        """Return multiplication of Series and other, element-wise (binary
        operator mul).

        Equivalent to ``series * others``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.multiply(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rmul__(self, other):
        """
        Get multiplication of other with Series, element-wise, using operator `*`.

        Equivalent to `Series.rmul(other)`.

        Args:
            other (scalar or Series):
                Object to multiply the Series with.

        Returns:
            bigframes.pandas.Series: The result of the multiplication.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def truediv(self, other) -> Series:
        """Return floating division of Series and other, element-wise (binary
        operator truediv).

        Equivalent to ``series / other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.divide(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __truediv__(self, other):
        """
        Get division of Series by other, element-wise, using operator `/`.

        Equivalent to `Series.truediv(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can multiply with a scalar:

            >>> s = bpd.Series([1, 2, 3])
            >>> s / 2
            0    0.5
            1    1.0
            2    1.5
            dtype: Float64

        You can also multiply with another Series:

            >>> denominator = bpd.Series([2, 3, 4])
            >>> s / denominator
            0         0.5
            1    0.666667
            2        0.75
            dtype: Float64

        Args:
            other (scalar or Series):
                Object to divide the Series by.

        Returns:
            bigframes.pandas.Series:
                The result of the division.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rtruediv(self, other) -> Series:
        """Return floating division of Series and other, element-wise (binary
        operator rtruediv).

        Equivalent to ``other / series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.divide(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rtruediv__(self, other):
        """
        Get division of other by Series, element-wise, using operator `/`.

        Equivalent to `Series.rtruediv(other)`.

        Args:
            other (scalar or Series):
                Object to divide by the Series.

        Returns:
            bigframes.pandas.Series: The result of the division.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def floordiv(self, other) -> Series:
        """Return integer division of Series and other, element-wise
        (binary operator floordiv).

        Equivalent to ``series // other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.floordiv(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __floordiv__(self, other):
        """
        Get integer division of Series by other, using arithmetic operator `//`.

        Equivalent to `Series.floordiv(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can divide by a scalar:

            >>> s = bpd.Series([15, 30, 45])
            >>> s // 2
            0     7
            1    15
            2    22
            dtype: Int64

        You can also divide by another DataFrame:

            >>> divisor = bpd.Series([3, 4, 4])
            >>> s // divisor
            0     5
            1     7
            2    11
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to divide the Series by.

        Returns:
            bigframes.pandas.Series:
                The result of the integer division.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rfloordiv(self, other) -> Series:
        """Return integer division of Series and other, element-wise (binary
        operator rfloordiv).

        Equivalent to ``other // series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.floordiv(b)
            a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rfloordiv__(self, other):
        """
        Get integer division of other by Series, using arithmetic operator `//`.

        Equivalent to `Series.rfloordiv(other)`.

        Args:
            other (scalar or Series):
                Object to divide by the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the integer division.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mod(self, other) -> Series:
        """Return modulo of Series and other, element-wise (binary operator mod).

        Equivalent to ``series % other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.mod(b)
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __mod__(self, other):
        """
        Get modulo of Series with other, element-wise, using operator `%`.

        Equivalent to `Series.mod(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can modulo with a scalar:

            >>> s = bpd.Series([1, 2, 3])
            >>> s % 3
            0    1
            1    2
            2    0
            dtype: Int64

        You can also modulo with another Series:

            >>> modulo = bpd.Series([3, 3, 3])
            >>> s % modulo
            0    1
            1    2
            2    0
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to modulo the Series by.

        Returns:
            bigframes.pandas.Series:
                The result of the modulo.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rmod(self, other) -> Series:
        """Return modulo of Series and other, element-wise (binary operator mod).

        Equivalent to ``series % other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.mod(b)
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rmod__(self, other):
        """
        Get modulo of other with Series, element-wise, using operator `%`.

        Equivalent to `Series.rmod(other)`.

        Args:
            other (scalar or Series):
                Object to modulo by the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the modulo.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pow(self, other) -> Series:
        """Return Exponential power of series and other, element-wise (binary
        operator `pow`).

        Equivalent to ``series ** other``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.pow(b)
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __pow__(self, other):
        """
        Get exponentiation of Series with other, element-wise, using operator
        `**`.

        Equivalent to `Series.pow(other)`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        You can exponentiate with a scalar:

            >>> s = bpd.Series([1, 2, 3])
            >>> s ** 2
            0    1
            1    4
            2    9
            dtype: Int64

        You can also exponentiate with another Series:

            >>> exponent = bpd.Series([3, 2, 1])
            >>> s ** exponent
            0    1
            1    4
            2    3
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to exponentiate the Series with.

        Returns:
            bigframes.pandas.Series:
                The result of the exponentiation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rpow(self, other) -> Series:
        """Return Exponential power of series and other, element-wise (binary
        operator `rpow`).

        Equivalent to ``other ** series``, but with support to substitute a
        fill_value for missing data in either one of the inputs.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.pow(b)
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            e    <NA>
            dtype: Float64

        Args:
            other (Series or scalar value)

        Returns:
            bigframes.pandas.Series:
                The result of the operation.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __rpow__(self, other):
        """
        Get exponentiation of other with Series, element-wise, using operator
        `**`.

        Equivalent to `Series.rpow(other)`.

        Args:
            other (scalar or Series):
                Object to exponentiate with the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the exponentiation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def divmod(self, other) -> Series:
        """Return integer division and modulo of Series and other, element-wise
        (binary operator divmod).

        Equivalent to divmod(series, other).

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.divmod(b)
            (a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64,
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64)

        Args:
            other: Series, or scalar value

        Returns:
            Tuple[bigframes.pandas.Series, bigframes.pandas.Series]:
                The result of the operation. The result is always
                consistent with (floordiv, mod) (though pandas may not).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rdivmod(self, other) -> Series:
        """Return integer division and modulo of Series and other, element-wise (binary operator rdivmod).

        Equivalent to other divmod series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> a = bpd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
            >>> a
            a     1.0
            b     1.0
            c     1.0
            d    <NA>
            dtype: Float64

            >>> b = bpd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
            >>> b
            a     1.0
            b    <NA>
            d     1.0
            e    <NA>
            dtype: Float64

            >>> a.divmod(b)
            (a     1.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64,
            a     0.0
            b    <NA>
            c    <NA>
            d    <NA>
            e    <NA>
            dtype: Float64)

        Args:
            other: Series, or scalar value

        Returns:
            Tuple[bigframes.pandas.Series, bigframes.pandas.Series]:
                The result of the operation. The result is always
                consistent with (rfloordiv, rmod) (though pandas may not).

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def combine_first(self, other) -> Series:
        """
        Update null elements with value in the same location in 'other'.

        Combine two Series objects by filling null values in one Series with
        non-null values from the other Series. Result index will be the union
        of the two indexes.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s1 = bpd.Series([1, np.nan])
            >>> s2 = bpd.Series([3, 4, 5])
            >>> s1.combine_first(s2)
            0    1.0
            1    4.0
            2    5.0
            dtype: Float64

        Null values still persist if the location of that null value
        does not exist in `other`

            >>> s1 = bpd.Series({'falcon': np.nan, 'eagle': 160.0})
            >>> s2 = bpd.Series({'eagle': 200.0, 'duck': 30.0})
            >>> s1.combine_first(s2)
            falcon     <NA>
            eagle     160.0
            duck       30.0
            dtype: Float64

        Args:
            other (Series):
                The value(s) to be used for filling null values.

        Returns:
            bigframes.pandas.Series:
                The result of combining the provided Series with the other object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def update(self, other) -> None:
        """
        Modify Series in place using values from passed Series.

        Uses non-NA values from passed Series to make updates. Aligns
        on index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import pandas as pd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s.update(bpd.Series([4, 5, 6]))
            >>> s
            0    4
            1    5
            2    6
            dtype: Int64

            >>> s = bpd.Series(['a', 'b', 'c'])
            >>> s.update(bpd.Series(['d', 'e'], index=[0, 2]))
            >>> s
            0    d
            1    b
            2    e
            dtype: string

            >>> s = bpd.Series([1, 2, 3])
            >>> s.update(bpd.Series([4, 5, 6, 7, 8]))
            >>> s
            0    4
            1    5
            2    6
            dtype: Int64

            If ``other`` contains NaNs the corresponding values are not updated
            in the original Series.

            >>> s = bpd.Series([1, 2, 3])
            >>> s.update(bpd.Series([4, np.nan, 6], dtype=pd.Int64Dtype()))
            >>> s
            0    4
            1    2
            2    6
            dtype: Int64

        ``other`` can also be a non-Series object type
        that is coercible into a Series

            >>> s = bpd.Series([1, 2, 3])
            >>> s.update([4, np.nan, 6])
            >>> s
            0    4.0
            1    2.0
            2    6.0
            dtype: Float64

            >>> s = bpd.Series([1, 2, 3])
            >>> s.update({1: 9})
            >>> s
            0    1
            1    9
            2    3
            dtype: Int64

        Args:
            other (Series, or object coercible into Series)

        Returns:
            None
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
            scalar or bigframes.pandas.Series:
                If level is specified, then, Series is returned;
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

        For Series input, the output is a scalar indicating whether any element is True.

            >>> bpd.Series([False, False]).any()
            np.False_

            >>> bpd.Series([True, False]).any()
            np.True_

            >>> bpd.Series([], dtype="float64").any()
            np.False_

            >>> bpd.Series([np.nan]).any()
            np.False_

        Returns:
            scalar or bigframes.pandas.Series:
                If level is specified, then, Series is returned;
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Calculating the max of a Series:

            >>> s = bpd.Series([1, 3])
            >>> s
            0    1
            1    3
            dtype: Int64

            >>> s.max()
            np.int64(3)

        Calculating the max of a Series containing ``NA`` values:

            >>> s = bpd.Series([1, 3, bpd.NA])
            >>> s
            0       1
            1       3
            2    <NA>
            dtype: Int64

            >>> s.max()
            np.int64(3)

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(
        self,
    ):
        """
        Return the maximum of the values over the requested axis.

        If you want the index of the minimum, use ``idxmin``. This is the equivalent
        of the ``numpy.ndarray`` method ``argmin``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Calculating the min of a Series:

            >>> s = bpd.Series([1, 3])
            >>> s
            0    1
            1    3
            dtype: Int64

            >>> s.min()
            np.int64(1)

        Calculating the min of a Series containing ``NA`` values:

            >>> s = bpd.Series([1, 3, bpd.NA])
            >>> s
            0       1
            1       3
            2    <NA>
            dtype: Int64

            >>> s.min()
            np.int64(1)

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(
        self,
    ):
        """
        Return sample standard deviation over requested axis.

        Normalized by N-1 by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'person_id': [0, 1, 2, 3],
            ...                     'age': [21, 25, 62, 43],
            ...                     'height': [1.61, 1.87, 1.49, 2.01]}
            ...                   ).set_index('person_id')
            >>> df
                       age  height
            person_id
            0           21    1.61
            1           25    1.87
            2           62    1.49
            3           43    2.01
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> df.std()
            age       18.786076
            height     0.237417
            dtype: Float64

        Returns:
            scalar or bigframes.pandas.Series (if level specified)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(
        self,
    ):
        """
        Return unbiased variance over requested axis.

        Normalized by N-1 by default.

        Returns:
            scalar or bigframes.pandas.Series (if level specified):
                Variance.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(self):
        """Return the sum of the values over the requested axis.

        This is equivalent to the method ``numpy.sum``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Calculating the sum of a Series:

            >>> s = bpd.Series([1, 3])
            >>> s
            0    1
            1    3
            dtype: Int64

            >>> s.sum()
            np.int64(4)

        Calculating the sum of a Series containing ``NA`` values:

            >>> s = bpd.Series([1, 3, bpd.NA])
            >>> s
            0       1
            1       3
            2    <NA>
            dtype: Int64

            >>> s.sum()
            np.int64(4)

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(self):
        """Return the mean of the values over the requested axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Calculating the mean of a Series:

            >>> s = bpd.Series([1, 3])
            >>> s
            0    1
            1    3
            dtype: Int64

            >>> s.mean()
            np.float64(2.0)

        Calculating the mean of a Series containing ``NA`` values:

            >>> s = bpd.Series([1, 3, bpd.NA])
            >>> s
            0       1
            1       3
            2    <NA>
            dtype: Int64

            >>> s.mean()
            np.float64(2.0)

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def median(self, *, exact: bool = True):
        """Return the median of the values over the requested axis.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s.median()
            np.float64(2.0)

        With a DataFrame

            >>> df = bpd.DataFrame({'a': [1, 2], 'b': [2, 3]}, index=['tiger', 'zebra'])
            >>> df
                   a  b
            tiger  1  2
            zebra  2  3
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df.median()
            a    1.5
            b    2.5
            dtype: Float64

        Args:
            exact (bool. default True):
                Default True. Get the exact median instead of an approximate
                one.

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def quantile(
        self,
        q: Union[float, Sequence[float]] = 0.5,
    ) -> Union[Series, float]:
        """
        Return value at the given quantile.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4])
            >>> s.quantile(.5)
            np.float64(2.5)

            >>> s.quantile([.25, .5, .75])
            0.25    1.75
            0.5      2.5
            0.75    3.25
            dtype: Float64

        Args:
            q (Union[float, Sequence[float], default 0.5 (50% quantile)):
                The quantile(s) to compute, which can lie in range: 0 <= q <= 1.

        Returns:
            Union[float, bigframes.pandas.Series]:
                If ``q`` is an array, a Series will be returned where the
                index is ``q`` and the values are the quantiles, otherwise
                a float will be returned.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def prod(self):
        """Return the product of the values over the requested axis.

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def describe(self):
        """
        Generate descriptive statistics.

        Descriptive statistics include those that summarize the central
        tendency, dispersion and shape of a
        dataset's distribution, excluding ``NaN`` values.

        .. note::
            Percentile values are approximates only.

        .. note::
            For numeric data, the result's index will include ``count``,
            ``mean``, ``std``, ``min``, ``max`` as well as lower, ``50`` and
            upper percentiles. By default the lower percentile is ``25`` and the
            upper percentile is ``75``. The ``50`` percentile is the
            same as the median.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['A', 'A', 'B'])
            >>> s
            0    A
            1    A
            2    B
            dtype: string

            >>> s.describe()
            count      3
            nunique    2
            Name: 0, dtype: Int64

        Returns:
            bigframes.pandas.Series:
                Summary statistics of the Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def skew(self):
        """Return unbiased skew over requested axis.

        Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s.skew()
            np.float64(0.0)

        With a DataFrame

            >>> df = bpd.DataFrame({'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [1, 3, 5]},
            ...                    index=['tiger', 'zebra', 'cow'])
            >>> df
                    a   b   c
            tiger   1   2   1
            zebra   2   3   3
            cow     3   4   5
            <BLANKLINE>
            [3 rows x 3 columns]

            >>> df.skew()
            a   0.0
            b   0.0
            c   0.0
            dtype: Float64

        Returns:
            scalar: Scalar.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def kurt(self):
        """Return unbiased kurtosis over requested axis.

        Kurtosis obtained using Fisher’s definition of kurtosis (kurtosis of
        normal == 0.0). Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 2, 3], index=['cat', 'dog', 'dog', 'mouse'])
            >>> s
            cat      1
            dog      2
            dog      2
            mouse    3
            dtype: Int64

            >>> s.kurt()
            np.float64(1.5)

        With a DataFrame

            >>> df = bpd.DataFrame({'a': [1, 2, 2, 3], 'b': [3, 4, 4, 4]},
            ...                    index=['cat', 'dog', 'dog', 'mouse'])
            >>> df
                   a  b
            cat    1  3
            dog    2  4
            dog    2  4
            mouse  3  4
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> df.kurt()
            a    1.5
            b    4.0
            dtype: Float64

        Returns:
            scalar or scalar:
                Unbiased kurtosis over requested axis.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def item(self: Series, *args, **kwargs):
        """Return the first element of the underlying data as a Python scalar.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([1])
            >>> s.item()
            np.int64(1)

        Returns:
            scalar: The first element of Series.

        Raises:
            ValueError: If the data is not length = 1.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def items(self):
        """
        Lazily iterate over (index, value) tuples.

        This method returns an iterable tuple (index, value).
        This is convenient if you want to create a lazy iterator.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['A', 'B', 'C'])
            >>> for index, value in s.items():
            ...     print(f"Index : {index}, Value : {value}")
            Index : 0, Value : A
            Index : 1, Value : B
            Index : 2, Value : C

        Returns:
            iterable:
              Iterable of tuples containing the (index, value) pairs from a
              Series.
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
            bigframes.pandas.Series:
                Series after the replacement.
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
        matching the condition would be masked. The condition can be provided in
        formm of a Series.

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

            >>> @bpd.remote_function(reuse=False, cloud_function_service_account="default")
            ... def should_mask(name: str) -> bool:
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

        Simple vectorized (i.e. they only perform operations supported on a
        Series) lambdas or python functions can be used directly.

            >>> nums = bpd.Series([1, 2, 3, 4], name="nums")
            >>> nums
            0    1
            1    2
            2    3
            3    4
            Name: nums, dtype: Int64
            >>> nums.mask(lambda x: (x+1) % 2 == 1)
            0        1
            1     <NA>
            2        3
            3     <NA>
            Name: nums, dtype: Int64

            >>> def is_odd(num):
            ...     return num % 2 == 1
            >>> nums.mask(is_odd)
            0     <NA>
            1        2
            2     <NA>
            3        4
            Name: nums, dtype: Int64

        Args:
            cond (bool Series/DataFrame, array-like, or callable):
                Where cond is False, keep the original value. Where True, replace
                with corresponding value from other. If cond is callable, it is
                computed on the Series/DataFrame and should return boolean
                Series/DataFrame or array. The callable must not change input
                Series/DataFrame (though pandas doesn't check it).
            other (scalar, Series/DataFrame, or callable):
                Entries where cond is True are replaced with corresponding value
                from other. If other is callable, it is computed on the
                Series/DataFrame and should return scalar or Series/DataFrame.
                The callable must not change input Series/DataFrame (though pandas
                doesn't check it). If not specified, entries will be filled with
                the corresponding NULL value (np.nan for numpy dtypes, pd.NA for
                extension dtypes).

        Returns:
            bigframes.pandas.Series:
                Series after the replacement.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def clip(self, lower, upper):
        """Trim values at input threshold(s).

        Assigns values outside boundary to boundary values. Thresholds can be
        singular values or array like, and in the latter case the clipping is
        performed element-wise in the specified axis.

        Args:
            lower (float or array-like, default None):
                Minimum threshold value. All values below this threshold will
                be set to it. A missing threshold (e.g NA) will not clip the value.

            upper (float or array-like, default None):
                Maximum threshold value. All values above this threshold will
                be set to it. A missing threshold (e.g NA) will not clip the value.

        Returns:
            bigframes.pandas.Series:
                Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def unstack(self, level):
        """
        Unstack, also known as pivot, Series with MultiIndex to produce DataFrame.

        Returns:
            bigframes.pandas.DataFrame: Unstacked Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmax(self):
        """
        Return int position of the largest value in the series.

        If the maximum is achieved in multiple locations, the first row position
        is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Consider dataset containing cereal calories.

            >>> s = bpd.Series({'Corn Flakes': 100.0, 'Almond Delight': 110.0,
            ...                 'Cinnamon Toast Crunch': 120.0, 'Cocoa Puff': 110.0})
            >>> s
            Corn Flakes              100.0
            Almond Delight           110.0
            Cinnamon Toast Crunch    120.0
            Cocoa Puff               110.0
            dtype: Float64

            >>> s.argmax()
            np.int64(2)

            >>> s.argmin()
            np.int64(0)

        The maximum cereal calories is the third element and the minimum cereal
        calories is the first element, since series is zero-indexed.

        Returns:
            int:
                Row position of the maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmin(self):
        """
        Return int position of the smallest value in the Series.

        If the minimum is achieved in multiple locations, the first row position
        is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Consider dataset containing cereal calories.

            >>> s = bpd.Series({'Corn Flakes': 100.0, 'Almond Delight': 110.0,
            ...                 'Cinnamon Toast Crunch': 120.0, 'Cocoa Puff': 110.0})
            >>> s
            Corn Flakes              100.0
            Almond Delight           110.0
            Cinnamon Toast Crunch    120.0
            Cocoa Puff               110.0
            dtype: Float64

            >>> s.argmax()
            np.int64(2)

            >>> s.argmin()
            np.int64(0)

        The maximum cereal calories is the third element and the minimum cereal
        calories is the first element, since series is zero-indexed.

        Returns:
            int:
                Row position of the minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename(self, index, *, inplace, **kwargs):
        """
        Alter Series index labels or name.

        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is. Extra labels listed don't throw an
        error.

        Alternatively, change ``Series.name`` with a scalar value.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> s
            0    1
            1    2
            2    3
            dtype: Int64

        You can changes the Series name by specifying a string scalar:

            >>> s.rename("my_name")
            0    1
            1    2
            2    3
            Name: my_name, dtype: Int64

        You can change the labels by specifying a mapping:

            >>> s.rename({1: 3, 2: 5})
            0    1
            3    2
            5    3
            dtype: Int64

        Args:
            index (scalar, hashable sequence, dict-like or function optional):
                Functions or dict-like are transformations to apply to
                the index.
                Scalar or hashable sequence-like will alter the ``Series.name``
                attribute.
            inplace (bool):
                Default False. Whether to return a new Series.

        Returns:
            bigframes.pandas.Series | None:
                Series with index labels or None if ``inplace=True``.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename_axis(self, mapper, *, inplace, **kwargs):
        """
        Set the name of the axis for the index or columns.

        Args:
            mapper (scalar, list-like, optional):
                Value to set the axis name attribute.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Series

            >>> s = bpd.Series(["dog", "cat", "monkey"])
            >>> s
            0       dog
            1       cat
            2    monkey
            dtype: string

            >>> s.rename_axis("animal")
            animal
            0       dog
            1       cat
            2    monkey
            dtype: string

        DataFrame

            >>> df = bpd.DataFrame({"num_legs": [4, 4, 2],
            ...                     "num_arms": [0, 0, 2]},
            ...                    ["dog", "cat", "monkey"])
            >>> df
                    num_legs  num_arms
            dog            4         0
            cat            4         0
            monkey         2         2
            <BLANKLINE>
            [3 rows x 2 columns]

            >>> df = df.rename_axis("animal")
            >>> df
                    num_legs  num_arms
            animal
            dog            4         0
            cat            4         0
            monkey         2         2
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.Series or  bigframes.pandas.DataFrame:
                The same type as the caller.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([3, 1, 2, 3, 4, bpd.NA], dtype="Int64")

            >>> s
            0       3
            1       1
            2       2
            3       3
            4       4
            5    <NA>
            dtype: Int64

        ``value_counts`` sorts the result by counts in a descending order by default:

            >>> s.value_counts()
            3      2
            1      1
            2      1
            4      1
            Name: count, dtype: Int64

        You can normalize the counts to return relative frequencies by setting ``normalize=True``:

            >>> s.value_counts(normalize=True)
            3    0.4
            1    0.2
            2    0.2
            4    0.2
            Name: proportion, dtype: Float64

        You can get the values in the ascending order of the counts by setting ``ascending=True``:

            >>> s.value_counts(ascending=True)
            1    1
            2    1
            4    1
            3    2
            Name: count, dtype: Int64

        You can include the counts of the ``NA`` values by setting ``dropna=False``:

            >>> s.value_counts(dropna=False)
            3       2
            1       1
            2       1
            4       1
            <NA>    1
            Name: count, dtype: Int64

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
            bigframes.pandas.Series:
                Series containing counts of unique values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def str(self):
        """
        Vectorized string functions for Series and Index.

        NAs stay NA unless handled otherwise by a particular method. Patterned
        after Python’s string methods, with some inspiration from R’s stringr package.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(["A_Str_Series"])
            >>> s
            0    A_Str_Series
            dtype: string

            >>> s.str.lower()
            0    a_str_series
            dtype: string

            >>> s.str.replace("_", "")
            0    AStrSeries
            dtype: string

        Returns:
            bigframes.operations.strings.StringMethods:
                An accessor containing string methods.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def plot(self):
        """
        Make plots of Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series([1, 2, 3, 3])
            >>> plot = ser.plot(kind='hist', title="My plot")
            >>> plot
            <Axes: title={'center': 'My plot'}, ylabel='Frequency'>

        Returns:
            bigframes.operations.plotting.PlotAccessor:
                An accessor making plots.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['llama', 'cow', 'llama', 'beetle', 'llama',
            ...                 'hippo'], name='animal')
            >>> s
            0     llama
            1       cow
            2     llama
            3    beetle
            4     llama
            5     hippo
            Name: animal, dtype: string

        To invert the boolean values, use the ~ operator:

            >>> ~s.isin(['cow', 'llama'])
            0    False
            1    False
            2    False
            3     True
            4    False
            5     True
            Name: animal, dtype: boolean

        Passing a single string as s.isin('llama') will raise an error. Use a
        list of one element instead:

            >>> s.isin(['llama'])
            0     True
            1    False
            2     True
            3    False
            4     True
            5    False
            Name: animal, dtype: boolean

        Strings and integers are distinct and are therefore not comparable:

            >>> bpd.Series([1]).isin(['1'])
            0    False
            dtype: boolean
            >>> bpd.Series([1.1]).isin(['1.1'])
            0    False
            dtype: boolean

        Args:
            values (list-like):
                The sequence of values to test. Passing in a single string will raise a
                TypeError. Instead, turn a single string into a list of one element.

        Returns:
            bigframes.pandas.Series: Series of booleans indicating if each element is in values.

        Raises:
            TypeError: If input is not list-like.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically increasing.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 2])
            >>> s.is_monotonic_increasing
            np.True_

            >>> s = bpd.Series([3, 2, 1])
            >>> s.is_monotonic_increasing
            np.False_

        Returns:
            bool:
                Boolean.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return boolean if values in the object are monotonically decreasing.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([3, 2, 2, 1])
            >>> s.is_monotonic_decreasing
            np.True_

            >>> s = bpd.Series([1, 2, 3])
            >>> s.is_monotonic_decreasing
            np.False_

        Returns:
            bool:
                Boolean.
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

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['cat', 'dog', bpd.NA, 'rabbit'])
            >>> s
            0       cat
            1       dog
            2      <NA>
            3    rabbit
            dtype: string

        `map` can accepts a `dict`. Values that are not found in the `dict` are
        converted to `NA`:

            >>> s.map({'cat': 'kitten', 'dog': 'puppy'})
            0    kitten
            1     puppy
            2      <NA>
            3      <NA>
            dtype: string

        It also accepts a remote function:

            >>> @bpd.remote_function(cloud_function_service_account="default")
            ... def my_mapper(val: str) -> str:
            ...     vowels = ["a", "e", "i", "o", "u"]
            ...     if val:
            ...         return "".join([
            ...             ch.upper() if ch in vowels else ch for ch in val
            ...         ])
            ...     return "N/A"

            >>> s.map(my_mapper)
            0       cAt
            1       dOg
            2       N/A
            3    rAbbIt
            dtype: string

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
            bigframes.pandas.Series:
                Same index as caller.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def iloc(self):
        """Purely integer-location based indexing for selection by position.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> mydict = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},
            ...               {'a': 100, 'b': 200, 'c': 300, 'd': 400},
            ...               {'a': 1000, 'b': 2000, 'c': 3000, 'd': 4000}]
            >>> df = bpd.DataFrame(mydict)
            >>> df
                  a     b     c     d
            0     1     2     3     4
            1   100   200   300   400
            2  1000  2000  3000  4000
            <BLANKLINE>
            [3 rows x 4 columns]

        Indexing just the rows

        With a scalar integer.

            >>> type(df.iloc[0])
            <class 'pandas.core.series.Series'>

            >>> df.iloc[0]
            a    1
            b    2
            c    3
            d    4
            Name: 0, dtype: Int64

        With a list of integers.

            >>> df.iloc[0]
            a    1
            b    2
            c    3
            d    4
            Name: 0, dtype: Int64

            >>> type(df.iloc[[0]])
            <class 'bigframes.dataframe.DataFrame'>

            >>> df.iloc[[0, 1]]
                a    b    c    d
            0    1    2    3    4
            1  100  200  300  400
            <BLANKLINE>
            [2 rows x 4 columns]

        With a slice object.

            >>> df.iloc[:3]
                  a     b     c     d
            0     1     2     3     4
            1   100   200   300   400
            2  1000  2000  3000  4000
            <BLANKLINE>
            [3 rows x 4 columns]

        Indexing both axes

        You can mix the indexer types for the index and columns. Use : to select
        the entire axis.

        With scalar integers.

            >>> df.iloc[0, 1]
            np.int64(2)

        Returns:
            bigframes.core.indexers.IlocSeriesIndexer:
                Purely integer-location Indexers.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def loc(self):
        """Access a group of rows and columns by label(s) or a boolean array.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([[1, 2], [4, 5], [7, 8]],
            ...                    index=['cobra', 'viper', 'sidewinder'],
            ...                    columns=['max_speed', 'shield'])
            >>> df
                        max_speed  shield
            cobra               1       2
            viper               4       5
            sidewinder          7       8
            <BLANKLINE>
            [3 rows x 2 columns]

        Single label. Note this returns the row as a Series.

            >>> df.loc['viper']
            max_speed    4
            shield       5
            Name: viper, dtype: Int64

        List of labels. Note using [[]] returns a DataFrame.

            >>> df.loc[['viper', 'sidewinder']]
                        max_speed  shield
            viper               4       5
            sidewinder          7       8
            <BLANKLINE>
            [2 rows x 2 columns]

        Slice with labels for row and single label for column. As mentioned
        above, note that both the start and stop of the slice are included.

            >>> df.loc['cobra', 'shield']
            np.int64(2)

        Index (same behavior as df.reindex)

            >>> df.loc[bpd.Index(["cobra", "viper"], name="foo")]
                  max_speed  shield
            cobra          1       2
            viper          4       5
            <BLANKLINE>
            [2 rows x 2 columns]

        Conditional that returns a boolean Series with column labels specified

            >>> df.loc[df['shield'] > 6, ['max_speed']]
                        max_speed
            sidewinder          7
            <BLANKLINE>
            [1 rows x 1 columns]

        Multiple conditional using | that returns a boolean Series

            >>> df.loc[(df['max_speed'] > 4) | (df['shield'] < 5)]
                        max_speed  shield
            cobra               1       2
            sidewinder          7       8
            <BLANKLINE>
            [2 rows x 2 columns]

        Please ensure that each condition is wrapped in parentheses ().

        Set value for an entire column

            >>> df.loc[:, 'max_speed'] = 30
            >>> df
                        max_speed  shield
            cobra              30       2
            viper              30       5
            sidewinder         30       8
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.core.indexers.LocSeriesIndexer:
                Indexers object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def iat(self):
        """Access a single value for a row/column pair by integer position.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],
            ...                    columns=['A', 'B', 'C'])
            >>> df
                A       B       C
            0   0       2       3
            1   0       4       1
            2   10      20      30
            <BLANKLINE>
            [3 rows x 3 columns]

        Get value at specified row/column pair

            >>> df.iat[1, 2]
            np.int64(1)

        Get value within a series

            >>> df.loc[0].iat[1]
            np.int64(2)

        Returns:
            bigframes.core.indexers.IatSeriesIndexer:
                Indexers object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def at(self):
        """Access a single value for a row/column label pair.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([[0, 2, 3], [0, 4, 1], [10, 20, 30]],
            ...                    index=[4, 5, 6], columns=['A', 'B', 'C'])
            >>> df
                A   B   C
            4   0   2   3
            5   0   4   1
            6  10  20  30
            <BLANKLINE>
            [3 rows x 3 columns]

        Get value at specified row/column pair

            >>> df.at[4, 'B']
            np.int64(2)

        Get value at specified row label

            >>> df.loc[5].at['B']
            np.int64(4)

        Returns:
            bigframes.core.indexers.AtSeriesIndexer:
                Indexers object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def values(self):
        """
        Return Series as ndarray or ndarray-like depending on the dtype.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> bpd.Series([1, 2, 3]).values
            array([1, 2, 3])

            >>> bpd.Series(list('aabc')).values
            array(['a', 'a', 'b', 'c'], dtype=object)

        Returns:
            numpy.ndarray or ndarray-like:
                Values in the Series.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def size(self) -> int:
        """Return the number of elements in the underlying data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        For Series:

            >>> s = bpd.Series(['Ant', 'Bear', 'Cow'])
            >>> s
            0     Ant
            1    Bear
            2     Cow
            dtype: string
            >>> s.size
            3

        For Index:

            >>> idx = bpd.Index(bpd.Series([1, 2, 3]))
            >>> idx.size
            3

        Returns:
            int:
                Return the number of elements in the underlying data.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __array__(self, dtype=None, copy: Optional[bool] = None) -> numpy.ndarray:
        """
        Returns the values as NumPy array.

        Equivalent to `Series.to_numpy(dtype)`.

        Users should not call this directly. Rather, it is invoked by
        `numpy.array` and `numpy.asarray`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> import numpy as np

            >>> ser = bpd.Series([1, 2, 3])

            >>> np.asarray(ser)
            array([1, 2, 3])

        Args:
            dtype (str or numpy.dtype, optional):
                The dtype to use for the resulting NumPy array. By default,
                the dtype is inferred from the data.
            copy (bool or None, optional):
                Whether to copy the data, False is not supported.

        Returns:
            numpy.ndarray:
                The values in the series converted to a `numpy.ndarray` with the
                specified dtype.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __len__(self):
        """Returns number of values in the Series, serves `len` operator.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3])
            >>> len(s)
            3
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __invert__(self):
        """
        Returns the logical inversion (binary NOT) of the Series, element-wise
        using operator `~`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series([True, False, True])
            >>> ~ser
            0    False
            1     True
            2    False
            dtype: boolean

        Returns:
            bigframes.pandas.Series:
                The inverted values in the series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __and__(self, other):
        """Get bitwise AND of Series and other, element-wise, using operator `&`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0, 1, 2, 3])

        You can operate with a scalar.

            >>> s & 6
            0    0
            1    0
            2    2
            3    2
            dtype: Int64

        You can operate with another Series.

            >>> s1 = bpd.Series([5, 6, 7, 8])
            >>> s & s1
            0    0
            1    0
            2    2
            3    0
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to bitwise AND with the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __or__(self, other):
        """Get bitwise OR of Series and other, element-wise, using operator `|`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0, 1, 2, 3])

        You can operate with a scalar.

            >>> s | 6
            0    6
            1    7
            2    6
            3    7
            dtype: Int64

        You can operate with another Series.

            >>> s1 = bpd.Series([5, 6, 7, 8])
            >>> s | s1
            0     5
            1     7
            2     7
            3    11
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to bitwise OR with the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __xor__(self, other):
        """Get bitwise XOR of Series and other, element-wise, using operator `^`.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0, 1, 2, 3])

        You can operate with a scalar.

            >>> s ^ 6
            0    6
            1    7
            2    4
            3    5
            dtype: Int64

        You can operate with another Series.

            >>> s1 = bpd.Series([5, 6, 7, 8])
            >>> s ^ s1
            0     5
            1     7
            2     5
            3    11
            dtype: Int64

        Args:
            other (scalar or Series):
                Object to bitwise XOR with the Series.

        Returns:
            bigframes.pandas.Series:
                The result of the operation.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __getitem__(self, indexer):
        """Gets the specified index from the Series.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([15, 30, 45])
            >>> s[1]
            np.int64(30)

            >>> s[0:2]
            0    15
            1    30
            dtype: Int64

        Args:
            indexer (int or slice):
                Index or slice of indices.

        Returns:
            bigframes.pandas.Series or Value:
                Value(s) at the requested index(es).
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
