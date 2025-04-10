# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/generic.py
from __future__ import annotations

from typing import Callable, Iterator, Literal, Optional, TYPE_CHECKING

import bigframes_vendored.constants as constants
from bigframes_vendored.pandas.core import indexing
import bigframes_vendored.pandas.core.common as common

if TYPE_CHECKING:
    from bigframes_vendored.pandas.pandas._typing import T


class NDFrame(indexing.IndexingMixin):
    """
    N-dimensional analogue of DataFrame. Store multi-dimensional in a
    size-mutable, labeled data structure
    """

    # ----------------------------------------------------------------------
    # Axis

    @property
    def ndim(self) -> int:
        """Return an int representing the number of axes / array dimensions.

        Returns:
            int: Return 1 if Series. Otherwise return 2 if DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def size(self) -> int:
        """Return an int representing the number of elements in this object.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series({'a': 1, 'b': 2, 'c': 3})
            >>> s.size
            3

            >>> df = bpd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
            >>> df.size
            4

        Returns:
            int: Return the number of rows if Series. Otherwise return the number of
                rows times number of columns if DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __iter__(self) -> Iterator:
        """
        Iterate over column axis for DataFrame, or values for Series.

        Returns:
            Iterator:
                Iterator of DataFrame or Series values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ... })
            >>> for x in df:
            ...     print(x)
            A
            B

            >>> series = bpd.Series(["a", "b", "c"], index=[10, 20, 30])
            >>> for x in series:
            ...     print(x)
            a
            b
            c
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # -------------------------------------------------------------------------
    # Unary Methods

    def abs(self):
        """Return a Series/DataFrame with absolute numeric value of each element.

        This function only applies to elements that are all numeric.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                A Series or DataFrame containing the absolute value of each element.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def astype(self, dtype):
        """
        Cast a pandas object to a specified dtype ``dtype``.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Create a DataFrame:

            >>> d = {'col1': [1, 2], 'col2': [3, 4]}
            >>> df = bpd.DataFrame(data=d)
            >>> df.dtypes
            col1    Int64
            col2    Int64
            dtype: object

        Cast all columns to ``Float64``:

            >>> df.astype('Float64').dtypes
            col1    Float64
            col2    Float64
            dtype: object

        Create a series of type ``Int64``:

            >>> ser = bpd.Series([2023010000246789, 1624123244123101, 1054834234120101], dtype='Int64')
            >>> ser
            0    2023010000246789
            1    1624123244123101
            2    1054834234120101
            dtype: Int64

        Convert to ``Float64`` type:

            >>> ser.astype('Float64')
            0    2023010000246789.0
            1    1624123244123101.0
            2    1054834234120101.0
            dtype: Float64

        Convert to ``pd.ArrowDtype(pa.timestamp("us", tz="UTC"))`` type:

            >>> ser.astype("timestamp[us, tz=UTC][pyarrow]")
            0    2034-02-08 11:13:20.246789+00:00
            1    2021-06-19 17:20:44.123101+00:00
            2    2003-06-05 17:30:34.120101+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]

        Note that this is equivalent of using ``to_datetime`` with ``unit='us'``:

            >>> bpd.to_datetime(ser, unit='us', utc=True)
            0    2034-02-08 11:13:20.246789+00:00
            1    2021-06-19 17:20:44.123101+00:00
            2    2003-06-05 17:30:34.120101+00:00
            dtype: timestamp[us, tz=UTC][pyarrow]

        Convert ``pd.ArrowDtype(pa.timestamp("us", tz="UTC"))`` type to ``Int64`` type:

            >>> timestamp_ser = ser.astype("timestamp[us, tz=UTC][pyarrow]")
            >>> timestamp_ser.astype('Int64')
            0    2023010000246789
            1    1624123244123101
            2    1054834234120101
            dtype: Int64

        Args:
            dtype (str, data type or pandas.ExtensionDtype):
                A dtype supported by BigQuery DataFrame include ``'boolean'``,
                ``'Float64'``, ``'Int64'``, ``'int64\\[pyarrow\\]'``,
                ``'string'``, ``'string\\[pyarrow\\]'``,
                ``'timestamp\\[us, tz=UTC\\]\\[pyarrow\\]'``,
                ``'timestamp\\[us\\]\\[pyarrow\\]'``,
                ``'date32\\[day\\]\\[pyarrow\\]'``,
                ``'time64\\[us\\]\\[pyarrow\\]'``.
                A pandas.ExtensionDtype include ``pandas.BooleanDtype()``,
                ``pandas.Float64Dtype()``, ``pandas.Int64Dtype()``,
                ``pandas.StringDtype(storage="pyarrow")``,
                ``pd.ArrowDtype(pa.date32())``,
                ``pd.ArrowDtype(pa.time64("us"))``,
                ``pd.ArrowDtype(pa.timestamp("us"))``,
                ``pd.ArrowDtype(pa.timestamp("us", tz="UTC"))``.
            errors ({'raise', 'null'}, default 'raise'):
                Control raising of exceptions on invalid data for provided dtype.
                If 'raise', allow exceptions to be raised if any value fails cast
                If 'null', will assign null value if value fails cast

        Returns:
            bigframes.pandas.DataFrame:
                A BigQuery DataFrame.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Iteration

    @property
    def empty(self) -> bool:
        """Indicates whether Series/DataFrame is empty.

        True if Series/DataFrame is entirely empty (no items), meaning any of the
        axes are of length 0.

        .. note::
            If Series/DataFrame contains only NA values, it is still not
            considered empty.

        Returns:
            bool: If Series/DataFrame is empty, return True, if not return False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # I/O Methods

    def to_json(
        self,
        path_or_buf,
        orient: Optional[
            Literal["split", "records", "index", "columns", "values", "table"]
        ] = None,
        *,
        index: bool = True,
        lines: bool = False,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        """Convert the object to a JSON string, written to Cloud Storage.

        Note NaN's and None will be converted to null and datetime objects
        will be converted to UNIX timestamps.

        .. note::
            Only ``orient='records'`` and ``lines=True`` is supported so far.

        Args:
            path_or_buf (str, path object, file-like object, or None, default None):
                String, path object (implementing os.PathLike[str]), or file-like
                object implementing a write() function. If None, the result is
                returned as a string.

                Can be a destination URI of Cloud Storage files(s) to store the extracted
                dataframe in format of ``gs://<bucket_name>/<object_name_or_glob>``.
                Must contain a wildcard `*` character.

                If the data size is more than 1GB, you must use a wildcard to
                export the data into multiple files and the size of the files
                varies.
            orient ({`split`, `records`, `index`, `columns`, `values`, `table`}, default 'columns):
                Indication of expected JSON string format.

                * Series:

                    - default is 'index'
                    - allowed values are: {{'split', 'records', 'index', 'table'}}.

                * DataFrame:

                    - default is 'columns'
                    - allowed values are: {{'split', 'records', 'index', 'columns',
                      'values', 'table'}}.

                * The format of the JSON string:

                    - 'split' : dict like {{'index' -> [index], 'columns' -> [columns],
                      'data' -> [values]}}
                    - 'records' : list like [{{column -> value}}, ... , {{column -> value}}]
                    - 'index' : dict like {{index -> {{column -> value}}}}
                    - 'columns' : dict like {{column -> {{index -> value}}}}
                    - 'values' : just the values array
                    - 'table' : dict like {{'schema': {{schema}}, 'data': {{data}}}}

                    Describing the data, where data component is like ``orient='records'``.
            index (bool, default True):
                If True, write row names (index).

            lines (bool, default False):
                If 'orient' is 'records' write out line-delimited json format. Will
                throw ValueError if incorrect 'orient' since others are not
                list-like.

            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB. This parameter has
                no effect when results are saved to Google Cloud Storage (GCS).

        Returns:
            None or str:
                If path_or_buf is None, returns the resulting json format as a
                string. Otherwise returns None.

        Raises:
            ValueError:
                If ``lines`` is True but ``records`` is not provided as value for ``orient``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_csv(
        self,
        path_or_buf,
        *,
        index: bool = True,
        allow_large_results: Optional[bool] = None,
    ) -> Optional[str]:
        """Write object to a comma-separated values (csv) file on Cloud Storage.

        Args:
            path_or_buf (str, path object, file-like object, or None, default None):
                String, path object (implementing os.PathLike[str]), or file-like
                object implementing a write() function. If None, the result is
                returned as a string. If a non-binary file object is passed, it should
                be opened with `newline=''`, disabling universal newlines. If a binary
                file object is passed, `mode` might need to contain a `'b'`.

                Alternatively, a destination URI of Cloud Storage files(s) to store the
                extracted dataframe in format of
                ``gs://<bucket_name>/<object_name_or_glob>``.

                If the data size is more than 1GB, you must use a wildcard to
                export the data into multiple files and the size of the files
                varies.

                None, file-like objects or local file paths not yet supported.

            index (bool, default True):
                If True, write row names (index).

            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow large
                query results over the default size limit of 10 GB. This parameter has
                no effect when results are saved to Google Cloud Storage (GCS).

        Returns:
            None or str: If path_or_buf is None, returns the resulting json format as a
            string. Otherwise returns None.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Unsorted

    def get(self, key, default=None):
        """
        Get item from object for given key (ex: DataFrame column).

        Returns default value if not found.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame(
            ...     [
            ...         [24.3, 75.7, "high"],
            ...         [31, 87.8, "high"],
            ...         [22, 71.6, "medium"],
            ...         [35, 95, "medium"],
            ...     ],
            ...     columns=["temp_celsius", "temp_fahrenheit", "windspeed"],
            ...     index=["2014-02-12", "2014-02-13", "2014-02-14", "2014-02-15"],
            ... )
            >>> df
                        temp_celsius  temp_fahrenheit windspeed
            2014-02-12          24.3             75.7      high
            2014-02-13          31.0             87.8      high
            2014-02-14          22.0             71.6    medium
            2014-02-15          35.0             95.0    medium
            <BLANKLINE>
            [4 rows x 3 columns]

            >>> df.get(["temp_celsius", "windspeed"])
                        temp_celsius windspeed
            2014-02-12          24.3      high
            2014-02-13          31.0      high
            2014-02-14          22.0    medium
            2014-02-15          35.0    medium
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> ser = df['windspeed']
            >>> ser
            2014-02-12      high
            2014-02-13      high
            2014-02-14    medium
            2014-02-15    medium
            Name: windspeed, dtype: string
            >>> ser.get('2014-02-13')
            'high'

        If the key is not found, the default value will be used.

            >>> df.get(["temp_celsius", "temp_kelvin"])
            >>> df.get(["temp_celsius", "temp_kelvin"], default="default_value")
            'default_value'

        Args:
            key: object

        Returns:
            Any:
                same type as items contained in object
        """
        try:
            return self[key]
        except (KeyError, ValueError, IndexError):
            return default

    def add_prefix(self, prefix: str, axis: int | str | None = None):
        """Prefix labels with string `prefix`.

        For Series, the row labels are prefixed.
        For DataFrame, the column labels are prefixed.

        Args:
            prefix (str):
                The string to add before each label.
            axis (int or str or None, default None):
                ``{{0 or 'index', 1 or 'columns', None}}``, default None. Axis
                to add prefix on.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                New Series or DataFrame with updated labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def add_suffix(self, suffix: str, axis: int | str | None = None):
        """Suffix labels with string `suffix`.

        For Series, the row labels are suffixed.
        For DataFrame, the column labels are suffixed.

        Args:
            suffix:
                The string to add after each label.
            axis:
                ``{{0 or 'index', 1 or 'columns', None}}``, default None. Axis
                to add suffix on

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                New Series or DataFrame with updated labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def head(self, n: int = 5):
        """Return the first `n` rows.

        This function returns the first `n` rows for the object based
        on position. It is useful for quickly testing if your object
        has the right type of data in it.

        For negative values of `n`, this function returns
        all rows except the last `|n|` rows, equivalent to ``df[:n]``.

        If n is larger than the number of rows, this function returns all rows.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'animal': ['alligator', 'bee', 'falcon', 'lion',
            ...                     'monkey', 'parrot', 'shark', 'whale', 'zebra']})
            >>> df
                animal
            0  alligator
            1        bee
            2     falcon
            3       lion
            4     monkey
            5     parrot
            6      shark
            7      whale
            8      zebra
            <BLANKLINE>
            [9 rows x 1 columns]

        Viewing the first 5 lines:

            >>> df.head()
                animal
            0  alligator
            1        bee
            2     falcon
            3       lion
            4     monkey
            <BLANKLINE>
            [5 rows x 1 columns]

        Viewing the first `n` lines (three in this case):

            >>> df.head(3)
                animal
            0  alligator
            1        bee
            2     falcon
            <BLANKLINE>
            [3 rows x 1 columns]

        For negative values of `n`:

            >>> df.head(-3)
                animal
            0  alligator
            1        bee
            2     falcon
            3       lion
            4     monkey
            5     parrot
            <BLANKLINE>
            [6 rows x 1 columns]

        Args:
            n (int, default 5):
                Default 5. Number of rows to select.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                The first ``n`` rows of the caller object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def tail(self, n: int = 5):
        """Return the last `n` rows.

        This function returns last `n` rows from the object based on
        position. It is useful for quickly verifying data, for example,
        after sorting or appending rows.

        For negative values of `n`, this function returns all rows except
        the first `|n|` rows, equivalent to ``df[|n|:]``.

        If n is larger than the number of rows, this function returns all rows.

        Args:
            n (int, default 5):
                Number of rows to select.

        Returns:
            bigframes.pandas.DataFrame:
                The last `n` rows of the caller object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sample(
        self,
        n: Optional[int] = None,
        frac: Optional[float] = None,
        *,
        random_state: Optional[int] = None,
        sort: Optional[bool | Literal["random"]] = "random",
    ):
        """Return a random sample of items from an axis of object.

        You can use `random_state` for reproducibility.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'num_legs': [2, 4, 8, 0],
            ...                     'num_wings': [2, 0, 0, 0],
            ...                     'num_specimen_seen': [10, 2, 1, 8]},
            ...                    index=['falcon', 'dog', 'spider', 'fish'])
            >>> df
                    num_legs  num_wings  num_specimen_seen
            falcon         2          2                 10
            dog            4          0                  2
            spider         8          0                  1
            fish           0          0                  8
            <BLANKLINE>
            [4 rows x 3 columns]

        Fetch one random row from the DataFrame (Note that we use `random_state`
        to ensure reproducibility of the examples):

            >>> df.sample(random_state=1)
                 num_legs  num_wings  num_specimen_seen
            dog         4          0                  2
            <BLANKLINE>
            [1 rows x 3 columns]

        A random 50% sample of the DataFrame:

            >>> df.sample(frac=0.5, random_state=1)
                  num_legs  num_wings  num_specimen_seen
            dog          4          0                  2
            fish         0          0                  8
            <BLANKLINE>
            [2 rows x 3 columns]

        Extract 3 random elements from the Series `df['num_legs']`:

            >>> s = df['num_legs']
            >>> s.sample(n=3, random_state=1)
            dog       4
            fish      0
            spider    8
            Name: num_legs, dtype: Int64

        Args:
            n (Optional[int], default None):
                Number of items from axis to return. Cannot be used with `frac`.
                Default = 1 if `frac` = None.
            frac (Optional[float], default None):
                Fraction of axis items to return. Cannot be used with `n`.
            random_state (Optional[int], default None):
                Seed for random number generator.
            sort (Optional[bool|Literal["random"]], default "random"):

                - 'random' (default): No specific ordering will be applied after
                  sampling.
                - 'True' : Index columns will determine the sample's order.
                - 'False': The sample will retain the original object's order.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                A new object of same type as caller containing `n` items randomly
                sampled from the caller object.

        Raises:
            ValueError:
                If both ``n`` and ``frac`` are specified.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Internal Interface Methods

    @property
    def dtypes(self):
        """Return the dtypes in the DataFrame.

        This returns a Series with the data type of each column.
        The result's index is the original DataFrame's columns. Columns
        with mixed types aren't supported yet in BigQuery DataFrames.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'float': [1.0], 'int': [1], 'string': ['foo']})
            >>> df.dtypes
            float             Float64
            int                 Int64
            string    string[pyarrow]
            dtype: object

        Returns:
            pandas.Series:
                A *pandas* Series with the data type of each column.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def copy(self):
        """Make a copy of this object's indices and data.

        A new object will be created with a copy of the calling object's data
        and indices. Modifications to the data or indices of the copy will not
        be reflected in the original object.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Modification in the original Series will not affect the copy Series:

            >>> s = bpd.Series([1, 2], index=["a", "b"])
            >>> s
            a    1
            b    2
            dtype: Int64

            >>> s_copy = s.copy()
            >>> s_copy
            a    1
            b    2
            dtype: Int64

            >>> s.loc['b'] = 22
            >>> s
            a     1
            b    22
            dtype: Int64
            >>> s_copy
            a    1
            b    2
            dtype: Int64

        Modification in the original DataFrame will not affect the copy DataFrame:

            >>> df = bpd.DataFrame({'a': [1, 3], 'b': [2, 4]})
            >>> df
               a  b
            0  1  2
            1  3  4
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df_copy = df.copy()
            >>> df_copy
               a  b
            0  1  2
            1  3  4
            <BLANKLINE>
            [2 rows x 2 columns]

            >>> df.loc[df["b"] == 2, "b"] = 22
            >>> df
               a   b
            0  1  22
            1  3   4
            <BLANKLINE>
            [2 rows x 2 columns]
            >>> df_copy
               a  b
            0  1  2
            1  3  4
            <BLANKLINE>
            [2 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Object type matches caller.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Action Methods

    def ffill(self, *, limit: Optional[int] = None):
        """Fill NA/NaN values by propagating the last valid observation to next valid.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([[np.nan, 2, np.nan, 0],
            ...                     [3, 4, np.nan, 1],
            ...                     [np.nan, np.nan, np.nan, np.nan],
            ...                     [np.nan, 3, np.nan, 4]],
            ...                    columns=list("ABCD")).astype("Float64")
            >>> df
                  A     B     C     D
            0  <NA>   2.0  <NA>   0.0
            1   3.0   4.0  <NA>   1.0
            2  <NA>  <NA>  <NA>  <NA>
            3  <NA>   3.0  <NA>   4.0
            <BLANKLINE>
            [4 rows x 4 columns]

        Fill NA/NaN values in DataFrames:

            >>> df.ffill()
                  A    B     C    D
            0  <NA>  2.0  <NA>  0.0
            1   3.0  4.0  <NA>  1.0
            2   3.0  4.0  <NA>  1.0
            3   3.0  3.0  <NA>  4.0
            <BLANKLINE>
            [4 rows x 4 columns]


        Fill NA/NaN values in Series:

            >>> series = bpd.Series([1, np.nan, 2, 3])
            >>> series.ffill()
            0    1.0
            1    1.0
            2    2.0
            3    3.0
            dtype: Float64

        Args:
            limit : int, default None
                If method is specified, this is the maximum number of consecutive
                NaN values to forward/backward fill. In other words, if there is
                a gap with more than this number of consecutive NaNs, it will only
                be partially filled. If method is not specified, this is the
                maximum number of entries along the entire axis where NaNs will be
                filled. Must be greater than 0 if not None.


        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series or None:
                Object with missing values filled.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def bfill(self, *, limit: Optional[int] = None):
        """Fill NA/NaN values by using the next valid observation to fill the gap.

        Args:
            limit : int, default None
                If method is specified, this is the maximum number of consecutive
                NaN values to forward/backward fill. In other words, if there is
                a gap with more than this number of consecutive NaNs, it will only
                be partially filled. If method is not specified, this is the
                maximum number of entries along the entire axis where NaNs will be
                filled. Must be greater than 0 if not None.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series or None:
                Object with missing values filled.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isna(self) -> NDFrame:
        """Detect missing values.

        Return a boolean same-sized object indicating if the values are NA.
        NA values get mapped to True values. Everything else gets mapped to
        False values. Characters such as empty strings ``''`` or
        :attr:`numpy.inf` are not considered NA values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> import numpy as np

            >>> df = bpd.DataFrame(dict(
            ...         age=[5, 6, np.nan],
            ...         born=[bpd.NA, "1940-04-25", "1940-04-25"],
            ...         name=['Alfred', 'Batman', ''],
            ...         toy=[None, 'Batmobile', 'Joker'],
            ... ))
            >>> df
                age        born    name        toy
            0   5.0        <NA>  Alfred       <NA>
            1   6.0  1940-04-25  Batman  Batmobile
            2  <NA>  1940-04-25              Joker
            <BLANKLINE>
            [3 rows x 4 columns]

        Show which entries in a DataFrame are NA:

            >>> df.isna()
                age   born   name    toy
            0  False   True  False   True
            1  False  False  False  False
            2   True  False  False  False
            <BLANKLINE>
            [3 rows x 4 columns]

            >>> df.isnull()
                age   born   name    toy
            0  False   True  False   True
            1  False  False  False  False
            2   True  False  False  False
            <BLANKLINE>
            [3 rows x 4 columns]

        Show which entries in a Series are NA:

            >>> ser = bpd.Series([5, None, 6, np.nan, bpd.NA])
            >>> ser
            0       5
            1    <NA>
            2       6
            3    <NA>
            4    <NA>
            dtype: Int64

            >>> ser.isna()
            0    False
            1     True
            2    False
            3     True
            4     True
            dtype: boolean

            >>> ser.isnull()
            0    False
            1     True
            2    False
            3     True
            4     True
            dtype: boolean

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Mask of bool values for each element that indicates whether an
                element is an NA value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    isnull = isna

    def notna(self) -> NDFrame:
        """Detect existing (non-missing) values.

        Return a boolean same-sized object indicating if the values are not NA.
        Non-missing values get mapped to True. Characters such as empty
        strings ``''`` or :attr:`numpy.inf` are not considered NA values.
        NA values get mapped to False values.

        Returns:
            NDFrame: Mask of bool values for each element that indicates whether an
            element is not an NA value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    notnull = notna

    def take(self, indices, axis=0, **kwargs) -> NDFrame:
        """Return the elements in the given positional indices along an axis.

        This means that we are not indexing according to actual values in the index
        attribute of the object. We are indexing according to the actual position of
        the element in the object.

        Args:
            indices (list-like):
                An array of ints indicating which positions to take.
            axis ({0 or 'index', 1 or 'columns', None}, default 0):
                The axis on which to select elements. 0 means that we are selecting rows,
                1 means that we are selecting columns. For Series this parameter is
                unused and defaults to 0.
            **kwargs:
                For compatibility with numpy.take(). Has no effect on the output.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Same type as input object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def filter(
        self,
        items=None,
        like: str | None = None,
        regex: str | None = None,
        axis=None,
    ) -> NDFrame:
        """
        Subset the dataframe rows or columns according to the specified index labels.

        Note that this routine does not filter a dataframe on its
        contents. The filter is applied to the labels of the index.

        Args:
            items (list-like):
                Keep labels from axis which are in items.
            like (str):
                Keep labels from axis for which "like in label == True".
            regex (str (regular expression)):
                Keep labels from axis for which re.search(regex, label) == True.
            axis ({0 or 'index', 1 or 'columns', None}, default None):
                The axis to filter on, expressed either as an index (int)
                or axis name (str). By default this is the info axis, 'columns' for
                DataFrame. For `Series` this parameter is unused and defaults to `None`.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Same type as input object.

        Raises:
            ValueError:
                If value provided is not exactly one of ``items``, ``like``, or ``regex``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def shift(
        self,
        periods: int = 1,
    ) -> NDFrame:
        """Shift index by desired number of periods.

        Shifts the index without realigning the data.

        Args:
            periods int:
                Number of periods to shift. Can be positive or negative.

        Returns:
            NDFrame:  Copy of input object, shifted.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pct_change(self, periods: int = 1):
        """
        Fractional change between the current and a prior element.

        Computes the fractional change from the immediately previous row by
        default. This is useful in comparing the fraction of change in a time
        series of elements.

        .. note::

            Despite the name of this method, it calculates fractional change
            (also known as per unit change or relative change) and not
            percentage change. If you need the percentage change, multiply
            these values by 100.

        Args:
            periods (int, default 1):
                Periods to shift for forming percent change.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series: The same type as the calling object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rank(
        self,
        axis=0,
        method: str = "average",
        numeric_only: bool = False,
        na_option: str = "keep",
        ascending: bool = True,
    ):
        """
        Compute numerical data ranks (1 through n) along axis.

        By default, equal values are assigned a rank that is the average of the
        ranks of those values.

        Args:
            method ({'average', 'min', 'max', 'first', 'dense'}, default 'average'):
                How to rank the group of records that have the same value (i.e. ties):
                `average`: average rank of the group, `min`: lowest rank in the group
                max`: highest rank in the group, `first`: ranks assigned in order they
                appear in the array, `dense`: like 'min', but rank always increases by
                1 between groups.

            numeric_only (bool, default False):
                For DataFrame objects, rank only numeric columns if set to True.

            na_option ({'keep', 'top', 'bottom'}, default 'keep'):
                How to rank NaN values: `keep`: assign NaN rank to NaN values,
                , `top`: assign lowest rank to NaN values, `bottom`: assign highest
                rank to NaN values.

            ascending (bool, default True):
                Whether or not the elements should be ranked in ascending order.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Return a Series or DataFrame with data ranks as values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rolling(
        self,
        window,
        min_periods: int | None = None,
        on: str | None = None,
        closed: Literal["right", "left", "both", "neither"] = "right",
    ):
        """
        Provide rolling window calculations.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([0,1,2,3,4])
            >>> s.rolling(window=3).min()
            0    <NA>
            1    <NA>
            2       0
            3       1
            4       2
            dtype: Int64

            >>> df = bpd.DataFrame({'A': [0,1,2,3], 'B': [0,2,4,6]})
            >>> df.rolling(window=2, on='A', closed='both').sum()
            A     B
            0  0  <NA>
            1  1     2
            2  2     6
            3  3    12
            <BLANKLINE>
            [4 rows x 2 columns]

        Args:
            window (int, pandas.Timedelta, numpy.timedelta64, datetime.timedelta, str):
                Size of the moving window.

                If an integer, the fixed number of observations used for
                each window.

                If a string, the timedelta representation in string. This string
                must be parsable by pandas.Timedelta().

                Otherwise, the time range for each window.

            min_periods (int, default None):
                Minimum number of observations in window required to have a value;
                otherwise, result is ``np.nan``.

                For a window that is specified by an integer, ``min_periods`` will default
                to the size of the window.

                For a window that is not spicified by an interger, ``min_periods`` will default
                to 1.

            on (str, optional):
                For a DataFrame, a column label on which to calculate the rolling window,
                rather than the DataFrame’s index.

            closed (str, default 'right'):
                If 'right', the first point in the window is excluded from calculations.
                If 'left', the last point in the window is excluded from calculations.
                If 'both', the no points in the window are excluded from calculations.
                If 'neither', the first and last points in the window are excluded from calculations.

        Returns:
            bigframes.core.window.Window: ``Window`` subclass if a ``win_type`` is passed.
                ``Rolling`` subclass if ``win_type`` is not passed.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def expanding(self, min_periods=1):
        """
        Provide expanding window calculations.

        Args:
            min_periods (int, default 1):
                Minimum number of observations in window required to have a value;
                otherwise, result is ``np.nan``.

        Returns:
            bigframes.core.window.Window: ``Expanding`` subclass.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def pipe(
        self,
        func: Callable[..., T] | tuple[Callable[..., T], str],
        *args,
        **kwargs,
    ) -> T:
        """
        Apply chainable functions that expect Series or DataFrames.

        **Examples:**

        Constructing a income DataFrame from a dictionary.

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> data = [[8000, 1000], [9500, np.nan], [5000, 2000]]
            >>> df = bpd.DataFrame(data, columns=['Salary', 'Others'])
            >>> df
               Salary  Others
            0    8000  1000.0
            1    9500    <NA>
            2    5000  2000.0
            <BLANKLINE>
            [3 rows x 2 columns]

        Functions that perform tax reductions on an income DataFrame.

            >>> def subtract_federal_tax(df):
            ...     return df * 0.9
            >>> def subtract_state_tax(df, rate):
            ...     return df * (1 - rate)
            >>> def subtract_national_insurance(df, rate, rate_increase):
            ...     new_rate = rate + rate_increase
            ...     return df * (1 - new_rate)

        Instead of writing

            >>> subtract_national_insurance(
            ...     subtract_state_tax(subtract_federal_tax(df), rate=0.12),
            ...     rate=0.05,
            ...     rate_increase=0.02)  # doctest: +SKIP

        You can write

            >>> (
            ...     df.pipe(subtract_federal_tax)
            ...     .pipe(subtract_state_tax, rate=0.12)
            ...     .pipe(subtract_national_insurance, rate=0.05, rate_increase=0.02)
            ... )
                Salary   Others
            0  5892.48   736.56
            1  6997.32     <NA>
            2   3682.8  1473.12
            <BLANKLINE>
            [3 rows x 2 columns]

        If you have a function that takes the data as (say) the second
        argument, pass a tuple indicating which keyword expects the
        data. For example, suppose ``national_insurance`` takes its data as ``df``
        in the second argument:

            >>> def subtract_national_insurance(rate, df, rate_increase):
            ...     new_rate = rate + rate_increase
            ...     return df * (1 - new_rate)
            >>> (
            ...     df.pipe(subtract_federal_tax)
            ...     .pipe(subtract_state_tax, rate=0.12)
            ...     .pipe(
            ...         (subtract_national_insurance, 'df'),
            ...         rate=0.05,
            ...         rate_increase=0.02
            ...     )
            ... )
                Salary   Others
            0  5892.48   736.56
            1  6997.32     <NA>
            2   3682.8  1473.12
            <BLANKLINE>
            [3 rows x 2 columns]

        Args:
            func (function):
                Function to apply to this object.
                ``args``, and ``kwargs`` are passed into ``func``.
                Alternatively a ``(callable, data_keyword)`` tuple where
                ``data_keyword`` is a string indicating the keyword of
                ``callable`` that expects this object.
            args (iterable, optional):
                Positional arguments passed into ``func``.
            kwargs (mapping, optional):
                A dictionary of keyword arguments passed into ``func``.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Object of same type as caller
        """
        return common.pipe(self, func, *args, **kwargs)

    def __nonzero__(self):
        """Returns the truth value of the object."""
        raise ValueError(
            f"The truth value of a {type(self).__name__} is ambiguous. "
            "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
        )

    __bool__ = __nonzero__

    def __getattr__(self, name: str):
        """
        After regular attribute access, try looking up the name
        This allows simpler access to columns for interactive use.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

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
