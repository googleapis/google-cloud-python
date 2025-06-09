# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexes/base.py
from __future__ import annotations

from collections.abc import Hashable
import typing

from bigframes import constants


class Index:
    """Immutable sequence used for indexing and alignment.

    The basic object storing axis labels for all objects.

    Args:
        data (pandas.Series | pandas.Index | bigframes.series.Series | bigframes.core.indexes.base.Index):
            Labels (1-dimensional).
        dtype:
            Data type for the output Index. If not specified, this will be
            inferred from `data`.
        name:
            Name to be stored in the index.
        session (Optional[bigframes.session.Session]):
            BigQuery DataFrames session where queries are run. If not set,
            a default session is used.
    """

    @property
    def name(self):
        """Returns Index name.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 2, 3], name='x')
            >>> idx
            Index([1, 2, 3], dtype='Int64', name='x')
            >>> idx.name
            'x'

        Returns:
            blocks.Label:
                Index or MultiIndex name
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def names(self):
        """Returns the names of the Index.

        Returns:
            Sequence[blocks.Label]:
                A Sequence of Index or MultiIndex name
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def values(self):
        """Return an array representing the data in the Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

            >>> idx.values
            array([1, 2, 3])

        Returns:
            array:
                Numpy.ndarray or ExtensionArray
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def ndim(self):
        """
        Number of dimensions of the underlying data, by definition 1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series(['Ant', 'Bear', 'Cow'])
            >>> s
            0     Ant
            1    Bear
            2     Cow
            dtype: string

            >>> s.ndim
            1

        For Index:

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

            >>> idx.ndim
            1

        Returns:
            int:
                Number or dimensions.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def size(self) -> int:
        """
        Return the number of elements in the underlying data.

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

        For Index:

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

        Returns:
            int:
                Number of elements
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def empty(self) -> bool:
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Return a boolean if the values are equal or increasing.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> bool(bpd.Index([1, 2, 3]).is_monotonic_increasing)
            True

            >>> bool(bpd.Index([1, 2, 2]).is_monotonic_increasing)
            True

            >>> bool(bpd.Index([1, 3, 2]).is_monotonic_increasing)
            False

        Returns:
            bool:
              True, if the values monotonically increasing, otherwise False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_monotonic_decreasing(self) -> bool:
        """
        Return a boolean if the values are equal or decreasing.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> bool(bpd.Index([3, 2, 1]).is_monotonic_decreasing)
            True

            >>> bool(bpd.Index([3, 2, 2]).is_monotonic_decreasing)
            True

            >>> bool(bpd.Index([3, 1, 2]).is_monotonic_decreasing)
            False

        Returns:
            bool:
              True, if the values monotonically decreasing, otherwise False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @classmethod
    def from_frame(cls, frame) -> Index:
        """
        Make a MultiIndex from a DataFrame.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([['HI', 'Temp'], ['HI', 'Precip'],
            ...                     ['NJ', 'Temp'], ['NJ', 'Precip']],
            ...                    columns=['a', 'b'])
            >>> df
                a       b
            0  HI    Temp
            1  HI  Precip
            2  NJ    Temp
            3  NJ  Precip
            <BLANKLINE>
            [4 rows x 2 columns]

            >>> bpd.MultiIndex.from_frame(df)
            Index([0, 1, 2, 3], dtype='Int64')

        Args:
          frame (Union[bigframes.pandas.Series, bigframes.pandas.DataFrame]):
              bigframes.pandas.Series or bigframes.pandas.DataFrame to convert
              to bigframes.pandas.Index.

        Returns:
            bigframes.pandas.Index:
                The Index representation of the given Series or DataFrame.

        Raises:
            bigframes.exceptions.NullIndexError:
                If Index is Null.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def shape(self):
        """
        Return a tuple of the shape of the underlying data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

            >>> idx.shape
            (3,)

        Returns:
            Tuple[int]:
                A Tuple of integers representing the shape.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def nlevels(self) -> int:
        """Integer number of levels in this MultiIndex

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> mi = bpd.MultiIndex.from_arrays([['a'], ['b'], ['c']])
            >>> mi
            MultiIndex([('a', 'b', 'c')],
                       )
            >>> mi.nlevels
            3

        Returns:
            int:
                Number of levels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_unique(self) -> bool:
        """Return if the index has unique values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 5, 7, 7])
            >>> idx.is_unique
            False

            >>> idx = bpd.Index([1, 5, 7])
            >>> idx.is_unique
            True

        Returns:
            bool:
                True if the index has unique values, otherwise False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def has_duplicates(self) -> bool:
        """Check if the Index has duplicate values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 5, 7, 7])
            >>> bool(idx.has_duplicates)
            True

            >>> idx = bpd.Index([1, 5, 7])
            >>> bool(idx.has_duplicates)
            False

        Returns:
            bool:
                Whether or not the Index has duplicate values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtype(self):
        """Return the dtype object of the underlying data.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

            >>> idx.dtype
            Int64Dtype()
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def dtypes(self):
        """Return the dtypes as a Series for the underlying MultiIndex.

        Returns:
            Pandas.Series:
                Pandas.Series of the MultiIndex dtypes.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def T(self) -> Index:
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

        For Index:

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx.T
            Index([1, 2, 3], dtype='Int64')

        Returns:
            bigframes.pandas.Index:
                Index
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def copy(
        self,
        name=None,
    ) -> Index:
        """
        Make a copy of this object.

        Name is set on the new object.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index(['a', 'b', 'c'])
            >>> new_idx = idx.copy()
            >>> idx is new_idx
            False

        Args:
            name (Label, optional):
                Set name for new object.

        Returns:
            bigframes.pandas.Index:
                Index reference to new object, which is a copy of this object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transpose(self) -> Index:
        """
        Return the transpose, which is by definition self.

        Returns:
            bigframes.pandas.Index
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def astype(self, dtype):
        """Create an Index with values cast to dtypes.

        The class of a new Index is determined by dtype. When conversion is
        impossible, a TypeError exception is raised.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, 2, 3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')


        Args:
            dtype (str, data type, or pandas.ExtensionDtype):
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
            bigframes.pandas.Index: Index with values cast to specified dtype.

        Raises:
            ValueError:
                If ``errors`` is not one of ``raise``.
            TypeError:
                MultiIndex with more than 1 level does not support ``astype``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def get_level_values(self, level) -> Index:
        """
        Return an Index of values for requested level.

        This is primarily useful to get an individual level of values from a
        MultiIndex, but is provided on Index as well for compatibility.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index(list('abc'))
            >>> idx
            Index(['a', 'b', 'c'], dtype='string')

        Get level values by supplying level as integer:

            >>> idx.get_level_values(0)
            Index(['a', 'b', 'c'], dtype='string')

        Args:
            level (int or str):
                It is either the integer position or the name of the level.

        Returns:
            bigframes.pandas.Index:
                Calling object, as there is only one level in the Index.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_series(self):
        """
        Create a Series with both index and values equal to the index keys.

        Useful with map for returning an indexer based on an index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index(['Ant', 'Bear', 'Cow'], name='animal')

        By default, the original index and original name is reused.

            >>> idx.to_series()
            animal
            Ant      Ant
            Bear    Bear
            Cow      Cow
            Name: animal, dtype: string

        To enforce a new index, specify new labels to index:

            >>> idx.to_series(index=[0, 1, 2])
            0     Ant
            1    Bear
            2     Cow
            Name: animal, dtype: string

        To override the name of the resulting column, specify name:

            >>> idx.to_series(name='zoo')
            animal
            Ant      Ant
            Bear    Bear
            Cow      Cow
            Name: zoo, dtype: string

        Args:
            index (Index, optional):
                Index of resulting Series. If None, defaults to original index.
            name (str, optional):
                Name of resulting Series. If None, defaults to name of original
                index.

        Returns:
            bigframes.pandas.Series:
                The dtype will be based on the type of the Index values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def isin(self, values):
        """
        Return a boolean array where the index values are in `values`.

        Compute boolean array to check whether each index value is found in the
        passed set of values. The length of the returned boolean array matches
        the length of the index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1,2,3])
            >>> idx
            Index([1, 2, 3], dtype='Int64')

        Check whether each index value in a list of values.

            >>> idx.isin([1, 4])
            Index([True, False, False], dtype='boolean')

            >>> midx = bpd.MultiIndex.from_arrays([[1,2,3],
            ...                                   ['red', 'blue', 'green']],
            ...                                   names=('number', 'color'))
            >>> midx
            MultiIndex([(1,   'red'),
                        (2,  'blue'),
                        (3, 'green')],
                       names=['number', 'color'])

        Args:
            values (set or list-like):
                Sought values.

        Returns:
            bigframes.pandas.Series:
                Series of boolean values.

        Raises:
            TypeError:
                If object passed to ``isin()`` is not a list-like
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def all(self) -> bool:
        """Return whether all elements are Truthy.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        True, because nonzero integers are considered True.

            >>> bool(bpd.Index([1, 2, 3]).all())
            True

            False, because 0 is considered False.

            >>> bool(bpd.Index([0, 1, 2]).all())
            False

        Returns:
            bool:
                A single element array-like may be converted to bool.

        Raises:
            TypeError:
                MultiIndex with more than 1 level does not support ``all``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def any(self) -> bool:
        """Return whether any element is Truthy.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> index = bpd.Index([0, 1, 2])
            >>> bool(index.any())
            True

            >>> index = bpd.Index([0, 0, 0])
            >>> bool(index.any())
            False

        Returns:
            bool:
                A single element array-like may be converted to bool.

        Raises:
            TypeError:
                MultiIndex with more than 1 level does not support ``any``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(self):
        """Return the minimum value of the Index.

         **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([3, 2, 1])
            >>> int(idx.min())
            1

            >>> idx = bpd.Index(['c', 'b', 'a'])
            >>> idx.min()
            'a'

        Returns:
            scalar:
                Minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(self):
        """Return the maximum value of the Index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([3, 2, 1])
            >>> int(idx.max())
            3

            >>> idx = bpd.Index(['c', 'b', 'a'])
            >>> idx.max()
            'c'

        Returns:
            scalar:
                Maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmin(self) -> int:
        """
        Return int position of the smallest value in the series.

        If the minimum is achieved in multiple locations,
        the first row position is returned.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

        Consider dataset containing cereal calories

            >>> s = bpd.Series({'Corn Flakes': 100.0, 'Almond Delight': 110.0,
            ...                'Cinnamon Toast Crunch': 120.0, 'Cocoa Puff': 110.0})
            >>> s
            Corn Flakes              100.0
            Almond Delight           110.0
            Cinnamon Toast Crunch    120.0
            Cocoa Puff               110.0
            dtype: Float64

            >>> int(s.argmax())
            2

            >>> int(s.argmin())
            0

        The maximum cereal calories is the third element and the minimum
        cereal calories is the first element, since series is zero-indexed.

        Returns:
            int:
                Row position of the minimum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def argmax(self) -> int:
        """
        Return int position of the largest value in the Series.

        If the maximum is achieved in multiple locations,
        the first row position is returned.

        **Examples:**

        Consider dataset containing cereal calories

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series({'Corn Flakes': 100.0, 'Almond Delight': 110.0,
            ...                'Cinnamon Toast Crunch': 120.0, 'Cocoa Puff': 110.0})
            >>> s
            Corn Flakes              100.0
            Almond Delight           110.0
            Cinnamon Toast Crunch    120.0
            Cocoa Puff               110.0
            dtype: Float64

            >>> int(s.argmax())
            2

            >>> int(s.argmin())
            0

        The maximum cereal calories is the third element and the minimum
        cereal calories is the first element, since series is zero-indexed.

        Returns:
            int:
                Row position of the maximum value.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self) -> int:
        """Return number of unique elements in the object.

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

            >>> int(s.nunique())
            4

        Returns:
            int:
                Number of unique elements
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sort_values(
        self, *, ascending: bool = True, na_position: str = "last"
    ) -> Index:
        """
        Return a sorted copy of the index.

        Return a sorted copy of the index, and optionally return the indices
        that sorted the index itself.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([10, 100, 1, 1000])
            >>> idx
            Index([10, 100, 1, 1000], dtype='Int64')

        Sort values in ascending order (default behavior).

            >>> idx.sort_values()
            Index([1, 10, 100, 1000], dtype='Int64')

        Args:
            ascending (bool, default True):
                Should the index values be sorted in an ascending order.
            na_position ({'first' or 'last'}, default 'last'):
                Argument 'first' puts NaNs at the beginning, 'last' puts NaNs at
                the end.

        Returns:
            pandas.Index: Sorted copy of the index.

        Raises:
            ValueError:
                If ``no_position`` is not one of ``first`` or ``last``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def value_counts(
        self,
        normalize: bool = True,
        sort: bool = True,
        ascending: bool = False,
        *,
        dropna: bool = True,
    ):
        """Return a Series containing counts of unique values.

        The resulting object will be in descending order so that the
        first element is the most frequently-occurring element.
        Excludes NA values by default.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> index = bpd.Index([3, 1, 2, 3, 4, np.nan])
            >>> index.value_counts()
            3.0    2
            1.0    1
            2.0    1
            4.0    1
            Name: count, dtype: Int64

        With normalize set to True, returns the relative frequency by
        dividing all values by the sum of values.

            >>> s = bpd.Series([3, 1, 2, 3, 4, np.nan])
            >>> s.value_counts(normalize=True)
            3.0    0.4
            1.0    0.2
            2.0    0.2
            4.0    0.2
            Name: proportion, dtype: Float64

        ``dropna``

        With dropna set to False we can also see NaN index values.

            >>> s.value_counts(dropna=False)
            3.0     2
            1.0     1
            2.0     1
            4.0     1
            <NA>    1
            Name: count, dtype: Int64

        Args:
            normalize (bool, default False):
                If True, then the object returned will contain the relative
                frequencies of the unique values.
            sort (bool, default True):
                Sort by frequencies.
            ascending (bool, default False):
                Sort in ascending order.
            dropna (bool, default True):
                Don't include counts of NaN.

        Returns:
            bigframes.pandas.Series
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def fillna(self, value) -> Index:
        """
        Fill NA/NaN values with the specified value.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([np.nan, np.nan, 3])
            >>> idx.fillna(0)
            Index([0.0, 0.0, 3.0], dtype='Float64')

        Args:
            value (scalar):
                Scalar value to use to fill holes (e.g. 0).
                This value cannot be a list-likes.

        Returns:
            bigframes.pandas.Index

        Raises:
            TypeError:
                MultiIndex with more than 1 level does not support ``fillna``.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rename(self, name, *, inplace):
        """
        Alter Index or MultiIndex name.

        Able to set new names without level. Defaults to returning new index.
        Length of names must match number of levels in MultiIndex.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index(['A', 'C', 'A', 'B'], name='score')
            >>> idx.rename('grade')
            Index(['A', 'C', 'A', 'B'], dtype='string', name='grade')

        Args:
            name (label or list of labels):
                Name(s) to set.
            inplace (bool):
                Default False.  Modifies the object directly, instead of
                creating a new Index or MultiIndex.

        Returns:
            bigframes.pandas.Index | None:
                The same type as the caller or None if ``inplace=True``.

        Raises:
            ValueError:
                If ``name`` is not the same length as levels.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop(self, labels) -> Index:
        """
        Make new Index with passed list of labels deleted.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index(['a', 'b', 'c'])
            >>> idx.drop(['a'])
            Index(['b', 'c'], dtype='string')

        Args:
            labels (array-like or scalar):

        Returns:
            bigframes.pandas.Index: Will be same type as self.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def dropna(self, how: typing.Literal["all", "any"] = "any"):
        """Return Index without NA/NaN values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> idx = bpd.Index([1, np.nan, 3])
            >>> idx.dropna()
            Index([1.0, 3.0], dtype='Float64')

        Args:
            how ({'any', 'all'}, default 'any'):
                If the Index is a MultiIndex, drop the value when any or all levels
                are NaN.

        Returns:
            bigframes.pandas.Index

        Raises:
            ValueError:
                If ``how`` is not ``any`` or ``all``
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def drop_duplicates(self, *, keep: str = "first"):
        """
        Return Index with duplicate values removed.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            Generate an pandas.Index with duplicate values.

            >>> idx = bpd.Index(['lama', 'cow', 'lama', 'beetle', 'lama', 'hippo'])

        The keep parameter controls which duplicate values are removed.
        The value ``first`` keeps the first occurrence for each set of
        duplicated entries. The default value of keep is ``first``.

            >>> idx.drop_duplicates(keep='first')
            Index(['lama', 'cow', 'beetle', 'hippo'], dtype='string')

        The value ``last`` keeps the last occurrence for each set of
        duplicated entries.

            >>> idx.drop_duplicates(keep='last')
            Index(['cow', 'beetle', 'lama', 'hippo'], dtype='string')

        The value ``False`` discards all sets of duplicated entries.

            >>> idx.drop_duplicates(keep=False)
            Index(['cow', 'beetle', 'hippo'], dtype='string')

        Args:
            keep ({'first', 'last', ``False``}, default 'first'):
                One of:
                'first' : Drop duplicates except for the first occurrence.
                'last' : Drop duplicates except for the last occurrence.
                ``False`` : Drop all duplicates.

        Returns:
            bigframes.pandas.Index
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def unique(self, level: Hashable | int | None = None):
        """
        Returns unique values in the index.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> idx = bpd.Index([1, 1, 2, 3, 3])
            >>> idx.unique()
            Index([1, 2, 3], dtype='Int64')

        Args:
            level (int or hashable, optional):
                Only return values from specified level (for MultiIndex).
                If int, gets the level by integer position, else by level name.

        Returns:
            bigframes.pandas.Index
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def item(self, *args, **kwargs):
        """Return the first element of the underlying data as a Python scalar.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> s = bpd.Series([1], index=['a'])
            >>> s.index.item()
            'a'

        Returns:
            scalar: The first element of Index.

        Raises:
            ValueError: If the data is not length = 1.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_numpy(self, dtype, *, allow_large_results=None):
        """
        A NumPy ndarray representing the values in this Series or Index.

        Args:
            dtype:
                The dtype to pass to :meth:`numpy.asarray`.
            allow_large_results (bool, default None):
                If not None, overrides the global setting to allow or disallow
                large query results over the default size limit of 10 GB.
            **kwargs:
                Additional keywords passed through to the ``to_numpy`` method
                of the underlying array (for extension arrays).

        Returns:
            numpy.ndarray
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
