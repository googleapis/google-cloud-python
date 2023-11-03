# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/generic.py
from __future__ import annotations

from typing import Iterator, Literal, Optional

from bigframes import constants
from third_party.bigframes_vendored.pandas.core import indexing


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

        Returns:
            int: Return the number of rows if Series. Otherwise return the number of
                rows times number of columns if DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def __iter__(self) -> Iterator:
        """
        Iterate over info axis.

        Returns
            iterator: Info axis as iterator.

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
            10
            20
            30
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # -------------------------------------------------------------------------
    # Unary Methods

    def abs(self):
        """Return a Series/DataFrame with absolute numeric value of each element.

        This function only applies to elements that are all numeric.

        Returns:
            Series/DataFrame containing the absolute value of each element.
            Returns a Series/DataFrame containing the absolute value of each element.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def astype(self, dtype):
        """
        Cast a pandas object to a specified dtype ``dtype``.

        Args:
            dtype (str or pandas.ExtensionDtype):
                A dtype supported by BigQuery DataFrame include 'boolean','Float64','Int64',
                'string', 'tring[pyarrow]','timestamp[us, tz=UTC][pyarrow]',
                'timestamp[us][pyarrow]','date32[day][pyarrow]','time64[us][pyarrow]'
                A pandas.ExtensionDtype include pandas.BooleanDtype(), pandas.Float64Dtype(),
                pandas.Int64Dtype(), pandas.StringDtype(storage="pyarrow"),
                pd.ArrowDtype(pa.date32()), pd.ArrowDtype(pa.time64("us")),
                pd.ArrowDtype(pa.timestamp("us")), pd.ArrowDtype(pa.timestamp("us", tz="UTC")).

        Returns:
            same type as caller

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
        path_or_buf: str,
        orient: Literal[
            "split", "records", "index", "columns", "values", "table"
        ] = "columns",
        *,
        index: bool = True,
        lines: bool = False,
    ) -> str | None:
        """Convert the object to a JSON string, written to Cloud Storage.

        Note NaN's and None will be converted to null and datetime objects
        will be converted to UNIX timestamps.

        .. note::
            Only ``orient='records'`` and ``lines=True`` is supported so far.

        Args:
            path_or_buf (str):
                A destination URI of Cloud Storage files(s) to store the extracted
                dataframe in format of ``gs://<bucket_name>/<object_name_or_glob>``.
                Must contain a wildcard `*` character.

                If the data size is more than 1GB, you must use a wildcard to
                export the data into multiple files and the size of the files
                varies.

                None, file-like objects or local file paths not yet supported.
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

        Returns:
            None: String output not yet supported.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_csv(self, path_or_buf: str, *, index: bool = True) -> str | None:
        """Write object to a comma-separated values (csv) file on Cloud Storage.

        Args:
            path_or_buf (str):
                A destination URI of Cloud Storage files(s) to store the extracted dataframe
                in format of ``gs://<bucket_name>/<object_name_or_glob>``.

                If the data size is more than 1GB, you must use a wildcard to
                export the data into multiple files and the size of the files
                varies.

                None, file-like objects or local file paths not yet supported.

            index (bool, default True):
                If True, write row names (index).

        Returns:
            None: String output not yet supported.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Unsorted

    def get(self, key, default=None):
        """
        Get item from object for given key (ex: DataFrame column).

        Returns default value if not found.

        Args:
            key: object

        Returns:
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
            New Series or DataFrame with updated labels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def head(self, n: int = 5):
        """Return the first `n` rows.

        This function returns the first `n` rows for the object based
        on position. It is useful for quickly testing if your object
        has the right type of data in it.

        **Not yet supported** For negative values of `n`, this function returns
        all rows except the last `|n|` rows, equivalent to ``df[:n]``.

        If n is larger than the number of rows, this function returns all rows.

        Args:
            n (int, default 5):
                Default 5. Number of rows to select.

        Returns:
            The first `n` rows of the caller object.
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
            The last `n` rows of the caller object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sample(
        self,
        n: Optional[int] = None,
        frac: Optional[float] = None,
        *,
        random_state: Optional[int] = None,
    ):
        """Return a random sample of items from an axis of object.

        You can use `random_state` for reproducibility.

        Args:
            n (Optional[int], default None):
                Number of items from axis to return. Cannot be used with `frac`.
                Default = 1 if `frac` = None.
            frac (Optional[float], default None):
                Fraction of axis items to return. Cannot be used with `n`.
            random_state (Optional[int], default None):
                Seed for random number generator.

        Returns:
            A new object of same type as caller containing `n` items randomly
            sampled from the caller object.
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

        Returns:
            A *pandas* Series with the data type of each column.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def copy(self):
        """Make a copy of this object's indices and data.

        A new object will be created with a copy of the calling object's data
        and indices. Modifications to the data or indices of the copy will not
        be reflected in the original object.

        Returns:
            Object type matches caller.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    # ----------------------------------------------------------------------
    # Action Methods

    def ffill(self, *, limit: Optional[int] = None):
        """Fill NA/NaN values by propagating the last valid observation to next valid.

        Args:
            limit : int, default None
                If method is specified, this is the maximum number of consecutive
                NaN values to forward/backward fill. In other words, if there is
                a gap with more than this number of consecutive NaNs, it will only
                be partially filled. If method is not specified, this is the
                maximum number of entries along the entire axis where NaNs will be
                filled. Must be greater than 0 if not None.


        Returns:
            Series/DataFrame or None: Object with missing values filled.
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
            Series/DataFrame or None: Object with missing values filled.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isna(self) -> NDFrame:
        """Detect missing values.

        Return a boolean same-sized object indicating if the values are NA.
        NA values get mapped to True values. Everything else gets mapped to
        False values. Characters such as empty strings ``''`` or
        :attr:`numpy.inf` are not considered NA values.

        Returns:
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
            same type as input object
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
            Series or DataFrame: The same type as the calling object.
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
            same type as caller: Return a Series or DataFrame with data ranks as values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rolling(
        self,
        window,
        min_periods: int | None = None,
    ):
        """
        Provide rolling window calculations.

        Args:
            window (int, timedelta, str, offset, or BaseIndexer subclass):
                Size of the moving window.

                If an integer, the fixed number of observations used for
                each window.

                If a timedelta, str, or offset, the time period of each window. Each
                window will be a variable sized based on the observations included in
                the time-period. This is only valid for datetime-like indexes.
                To learn more about the offsets & frequency strings, please see `this link
                <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`__.

                If a BaseIndexer subclass, the window boundaries
                based on the defined ``get_window_bounds`` method. Additional rolling
                keyword arguments, namely ``min_periods``, ``center``, ``closed`` and
                ``step`` will be passed to ``get_window_bounds``.

            min_periods (int, default None):
                Minimum number of observations in window required to have a value;
                otherwise, result is ``np.nan``.

                For a window that is specified by an offset, ``min_periods`` will default to 1.

                For a window that is specified by an integer, ``min_periods`` will default
                to the size of the window.

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

    def __nonzero__(self):
        raise ValueError(
            f"The truth value of a {type(self).__name__} is ambiguous. "
            "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
        )

    __bool__ = __nonzero__
