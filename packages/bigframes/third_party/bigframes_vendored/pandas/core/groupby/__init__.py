# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/groupby/groupby.py
"""
Provide the groupby split-apply-combine paradigm. Define the GroupBy
class providing the base-class of operations.

The SeriesGroupBy and DataFrameGroupBy sub-class
(defined in pandas.core.groupby.generic)
expose these user-facing objects to provide specific functionality.
"""
from __future__ import annotations

from bigframes import constants


class GroupBy:
    """
    Class for grouping and aggregating relational data.
    """

    def any(self):
        """
        Return True if any value in the group is true, else False.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([1, 2, 0], index=lst)
            >>> ser.groupby(level=0).any()
            a     True
            b    False
            dtype: boolean

        For DataFrameGroupBy:

            >>> data = [[1, 0, 3], [1, 0, 6], [7, 1, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                    index=["ostrich", "penguin", "parrot"])
            >>> df.groupby(by=["a"]).any()
                    b       c
            a
            1   False    True
            7   True    True
            <BLANKLINE>
            [2 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                DataFrame or Series of boolean values,
                where a value is True if any element is True within its
                respective group; otherwise False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def all(self):
        """
        Return True if all values in the group are true, else False.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([1, 2, 0], index=lst)
            >>> ser.groupby(level=0).all()
            a     True
            b    False
            dtype: boolean

        For DataFrameGroupBy:

            >>> data = [[1, 0, 3], [1, 5, 6], [7, 8, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                    index=["ostrich", "penguin", "parrot"])
            >>> df.groupby(by=["a"]).all()
                    b       c
            a
            1   False    True
            7   True    True
            <BLANKLINE>
            [2 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                DataFrame or Series of boolean values,
                where a value is True if all elements are True within its
                respective group; otherwise False.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def count(self):
        """
        Compute count of group, excluding missing values.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([1, 2, np.nan], index=lst)
            >>> ser.groupby(level=0).count()
            a     2
            b     0
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, np.nan, 3], [1, np.nan, 6], [7, 8, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                    index=["cow", "horse", "bull"])
            >>> df.groupby(by=["a"]).count()
               b  c
            a
            1  0  2
            7  1  1
            <BLANKLINE>
            [2 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Count of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(
        self,
        numeric_only: bool = False,
    ):
        """
        Compute mean of groups, excluding missing values.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame({'A': [1, 1, 2, 1, 2],
            ...                    'B': [np.nan, 2, 3, 4, 5],
            ...                    'C': [1, 2, 1, 1, 2]}, columns=['A', 'B', 'C'])

        Groupby one column and return the mean of the remaining columns in each group.

            >>> df.groupby('A').mean()
                B         C
            A
            1  3.0  1.333333
            2  4.0       1.5
            <BLANKLINE>
            [2 rows x 2 columns]

        Groupby two columns and return the mean of the remaining column.

            >>> df.groupby(['A', 'B']).mean()
                     C
            A B
            1 2.0  2.0
              4.0  1.0
            2 3.0  1.0
              5.0  2.0
            <BLANKLINE>
            [4 rows x 1 columns]

        Groupby one column and return the mean of only particular column in the group.

            >>> df.groupby('A')['B'].mean()
            A
            1    3.0
            2    4.0
            Name: B, dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Mean of groups.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def median(
        self,
        numeric_only: bool = False,
        *,
        exact: bool = True,
    ):
        """
        Compute median of groups, excluding missing values.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
            >>> ser = bpd.Series([7, 2, 8, 4, 3, 3], index=lst)
            >>> ser.groupby(level=0).median()
            a    7.0
            b    3.0
            dtype: Float64

        For DataFrameGroupBy:

            >>> data = {'a': [1, 3, 5, 7, 7, 8, 3], 'b': [1, 4, 8, 4, 4, 2, 1]}
            >>> df = bpd.DataFrame(data, index=['dog', 'dog', 'dog',
            ...                    'mouse', 'mouse', 'mouse', 'mouse'])
            >>> df.groupby(level=0).median()
                    a    b
            dog    3.0  4.0
            mouse  7.0  3.0
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            exact (bool, default True):
                Calculate the exact median instead of an approximation.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Median of groups.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def quantile(self, q=0.5, *, numeric_only: bool = False):
        """
        Return group values at the given quantile, a la numpy.percentile.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> df = bpd.DataFrame([
            ...     ['a', 1], ['a', 2], ['a', 3],
            ...     ['b', 1], ['b', 3], ['b', 5]
            ... ], columns=['key', 'val'])
            >>> df.groupby('key').quantile()
                 val
            key
            a    2.0
            b    3.0
            <BLANKLINE>
            [2 rows x 1 columns]

        Args:
            q (float or array-like, default 0.5 (50% quantile)):
                Value(s) between 0 and 1 providing the quantile(s) to compute.
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Return type determined by caller of GroupBy object.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Compute standard deviation of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
            >>> ser = bpd.Series([7, 2, 8, 4, 3, 3], index=lst)
            >>> ser.groupby(level=0).std()
            a     3.21455
            b     0.57735
            dtype: Float64

        For DataFrameGroupBy:

            >>> data = {'a': [1, 3, 5, 7, 7, 8, 3], 'b': [1, 4, 8, 4, 4, 2, 1]}
            >>> df = bpd.DataFrame(data, index=['dog', 'dog', 'dog',
            ...                    'mouse', 'mouse', 'mouse', 'mouse'])
            >>> df.groupby(level=0).std()
                          a         b
            dog         2.0  3.511885
            mouse  2.217356       1.5
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Standard deviation of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Compute variance of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
            >>> ser = bpd.Series([7, 2, 8, 4, 3, 3], index=lst)
            >>> ser.groupby(level=0).var()
            a   10.333333
            b    0.333333
            dtype: Float64

        For DataFrameGroupBy:

            >>> data = {'a': [1, 3, 5, 7, 7, 8, 3], 'b': [1, 4, 8, 4, 4, 2, 1]}
            >>> df = bpd.DataFrame(data, index=['dog', 'dog', 'dog',
            ...                    'mouse', 'mouse', 'mouse', 'mouse'])
            >>> df.groupby(level=0).var()
                          a          b
            dog         4.0  12.333333
            mouse  4.916667       2.25
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Variance of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rank(
        self,
        method: str = "average",
        ascending: bool = True,
        na_option: str = "keep",
    ):
        """
        Provide the rank of values within each group.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame(
            ...     {
            ...         "group": ["a", "a", "a", "a", "a", "b", "b", "b", "b", "b"],
            ...         "value": [2, 4, 2, 3, 5, 1, 2, 4, 1, 5],
            ...     }
            ... )
            >>> df
            group  value
            0     a      2
            1     a      4
            2     a      2
            3     a      3
            4     a      5
            5     b      1
            6     b      2
            7     b      4
            8     b      1
            9     b      5
            <BLANKLINE>
            [10 rows x 2 columns]
            >>> for method in ['average', 'min', 'max', 'dense', 'first']:
            ...     df[f'{method}_rank'] = df.groupby('group')['value'].rank(method)
            >>> df
            group  value  average_rank  min_rank  max_rank  dense_rank  first_rank
            0     a      2           1.5       1.0       2.0         1.0         1.0
            1     a      4           4.0       4.0       4.0         3.0         4.0
            2     a      2           1.5       1.0       2.0         1.0         2.0
            3     a      3           3.0       3.0       3.0         2.0         3.0
            4     a      5           5.0       5.0       5.0         4.0         5.0
            5     b      1           1.5       1.0       2.0         1.0         1.0
            6     b      2           3.0       3.0       3.0         2.0         3.0
            7     b      4           4.0       4.0       4.0         3.0         4.0
            8     b      1           1.5       1.0       2.0         1.0         2.0
            9     b      5           5.0       5.0       5.0         4.0         5.0
            <BLANKLINE>
            [10 rows x 7 columns]

        Args:
            method ({'average', 'min', 'max', 'first', 'dense'}, default 'average'):
                * average: average rank of group.
                * min: lowest rank in group.
                * max: highest rank in group.
                * first: ranks assigned in order they appear in the array.
                * dense: like 'min', but rank always increases by 1 between groups.
            ascending (bool, default True):
                False for ranks by high (1) to low (N).
            na_option ({'keep', 'top', 'bottom'}, default 'keep'):
                * keep: leave NA values where they are.
                * top: smallest rank if ascending.
                * bottom: smallest rank if descending.

        Returns:
            DataFrame with ranking of values within each group
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def skew(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Return unbiased skew within groups.

        Normalized by N-1.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> ser = bpd.Series([390., 350., 357., np.nan, 22., 20., 30.],
            ...                  index=['Falcon', 'Falcon', 'Falcon', 'Falcon',
            ...                         'Parrot', 'Parrot', 'Parrot'],
            ...                  name="Max Speed")
            >>> ser.groupby(level=0).skew()
            Falcon    1.525174
            Parrot    1.457863
            Name: Max Speed, dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Variance of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def kurt(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Return unbiased kurtosis over requested axis.

        Kurtosis obtained using Fisher's definition of
        kurtosis (kurtosis of normal == 0.0). Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b']
            >>> ser = bpd.Series([0, 1, 1, 0, 0, 1, 2, 4, 5], index=lst)
            >>> ser.groupby(level=0).kurt()
            a        -6.0
            b   -1.963223
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Variance of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def kurtosis(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Return unbiased kurtosis over requested axis.

        Kurtosis obtained using Fisher's definition of
        kurtosis (kurtosis of normal == 0.0). Normalized by N-1.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b']
            >>> ser = bpd.Series([0, 1, 1, 0, 0, 1, 2, 4, 5], index=lst)
            >>> ser.groupby(level=0).kurtosis()
            a        -6.0
            b   -1.963223
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Variance of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
    ):
        """
        Compute sum of group values.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).sum()
            a     3
            b     7
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 5, 8], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["tiger", "leopard", "cheetah", "lion"])
            >>> df.groupby("a").sum()
                b   c
            a
            1  10   7
            2  11  17
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` and non-NA values are present, the result will be NA.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Computed sum of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def prod(self, numeric_only: bool = False, min_count: int = 0):
        """
        Compute prod of group values.
        (DataFrameGroupBy functionality is not yet available.)

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).prod()
            a     2.0
            b    12.0
            dtype: Float64

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` and non-NA values are present, the result will be NA.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Computed prod of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
    ):
        """
        Compute min of group values.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).min()
            a     1
            b     3
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 5, 8], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                    index=["tiger", "leopard", "cheetah", "lion"])
            >>> df.groupby(by=["a"]).min()
               b  c
            a
            1  2  2
            2  5  8
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` and non-NA values are present, the result will be NA.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Computed min of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
    ):
        """
        Compute max of group values.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).max()
            a     2
            b     4
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 5, 8], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                    index=["tiger", "leopard", "cheetah", "lion"])
            >>> df.groupby(by=["a"]).max()
               b  c
            a
            1  8  5
            2  6  9
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` and non-NA values are present, the result will be NA.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Computed max of values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumcount(self, ascending: bool = True):
        """
        Number each item in each group from 0 to the length of that group - 1.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b', 'c']
            >>> ser = bpd.Series([5, 1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).cumcount()
            a    0
            a    1
            b    0
            b    1
            c    0
            dtype: Int64
            >>> ser.groupby(level=0).cumcount(ascending=False)
            a    0
            a    1
            b    0
            b    1
            c    0
            dtype: Int64

        Args:
            ascending (bool, default True):
                If False, number in reverse, from length of group - 1 to 0.

        Returns:
            bigframes.pandas.Series:
                Sequence number of each element within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumprod(self, *args, **kwargs):
        """
        Cumulative product for each group.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([6, 2, 0], index=lst)
            >>> ser.groupby(level=0).cumprod()
            a     6.0
            a    12.0
            b     0.0
            dtype: Float64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["cow", "horse", "bull"])
            >>> df.groupby("a").cumprod()
                      b     c
            cow     8.0   2.0
            horse  16.0  10.0
            bull    6.0   9.0
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Cumulative product for each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cumsum(self, *args, **kwargs):
        """
        Cumulative sum for each group.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([6, 2, 0], index=lst)
            >>> ser.groupby(level=0).cumsum()
            a    6
            a    8
            b    0
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["fox", "gorilla", "lion"])
            >>> df.groupby("a").cumsum()
                      b  c
            fox       8  2
            gorilla  10  7
            lion      6  9
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Cumulative sum for each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummin(self, *args, numeric_only: bool = False, **kwargs):
        """
        Cumulative min for each group.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([6, 2, 0], index=lst)
            >>> ser.groupby(level=0).cummin()
            a    6
            a    2
            b    0
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["fox", "gorilla", "lion"])
            >>> df.groupby("a").cummin()
                     b  c
            fox      8  2
            gorilla  2  2
            lion     6  9
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Cumulative min for each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def cummax(self, *args, numeric_only: bool = False, **kwargs):
        """
        Cumulative max for each group.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([6, 2, 0], index=lst)
            >>> ser.groupby(level=0).cummax()
            a    6
            a    6
            b    0
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 8, 2], [1, 2, 5], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["fox", "gorilla", "lion"])
            >>> df.groupby("a").cummax()
                     b  c
            fox      8  2
            gorilla  8  5
            lion     6  9
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Cumulative max for each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def diff(self):
        """
        First discrete difference of element.
        Calculates the difference of each element compared with another
        element in the group (default is element in previous row).

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
            >>> ser = bpd.Series([7, 2, 8, 4, 3, 3], index=lst)
            >>> ser.groupby(level=0).diff()
            a    <NA>
            a      -5
            a       6
            b    <NA>
            b      -1
            b       0
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = {'a': [1, 3, 5, 7, 7, 8, 3], 'b': [1, 4, 8, 4, 4, 2, 1]}
            >>> df = bpd.DataFrame(data, index=['dog', 'dog', 'dog',
            ...                   'mouse', 'mouse', 'mouse', 'mouse'])
            >>> df.groupby(level=0).diff()
                      a     b
            dog    <NA>  <NA>
            dog       2     3
            dog       2     4
            mouse  <NA>  <NA>
            mouse     0     0
            mouse     1    -2
            mouse    -5    -1
            <BLANKLINE>
            [7 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                First differences.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def shift(self, periods: int = 1):
        """
        Shift each group by periods observations.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 4], index=lst)
            >>> ser.groupby(level=0).shift(1)
            a    <NA>
            a       1
            b    <NA>
            b       3
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 2, 3], [1, 5, 6], [2, 5, 8], [2, 6, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["tuna", "salmon", "catfish", "goldfish"])
            >>> df.groupby("a").shift(1)
                         b     c
            tuna      <NA>  <NA>
            salmon       2     3
            catfish   <NA>  <NA>
            goldfish     5     8
            <BLANKLINE>
            [4 rows x 2 columns]

        Args:
            periods (int, default 1):
                Number of periods to shift.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Object shifted within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def rolling(self, *args, **kwargs):
        """
        Returns a rolling grouper, providing rolling functionality per group.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'a', 'a', 'e']
            >>> ser = bpd.Series([1, 0, -2, -1, 2], index=lst)
            >>> ser.groupby(level=0).rolling(2).min()
            index  index
            a      a        <NA>
                a           0
                a          -2
                a          -2
            e      e        <NA>
            dtype: Int64

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
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Return a new grouper with our rolling appended.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def expanding(self, *args, **kwargs):
        """
        Provides expanding functionality.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'c', 'c', 'e']
            >>> ser = bpd.Series([1, 0, -2, -1, 2], index=lst)
            >>> ser.groupby(level=0).expanding().min()
            index  index
            a      a         1
                   a         0
            c      c        -2
                   c        -2
            e      e         2
            dtype: Int64

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                An expanding grouper, providing expanding functionality per group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def head(self, n: int = 5):
        """
        Return last first n rows of each group

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame([[1, 2], [1, 4], [5, 6]],
            ...                   columns=['A', 'B'])
            >>> df.groupby('A').head(1)
               A  B
            0  1  2
            2  5  6
            [2 rows x 2 columns]

        Args:
            n (int):
                If positive: number of entries to include from start of each group.
                If negative: number of entries to exclude from end of each group.

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                First n rows of the original DataFrame or Series

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def size(self):
        """
        Compute group sizes.

        **Examples:**

        For SeriesGroupBy:

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b']
            >>> ser = bpd.Series([1, 2, 3], index=lst)
            >>> ser
            a     1
            a     2
            b     3
            dtype: Int64
            >>> ser.groupby(level=0).size()
            a    2
            b    1
            dtype: Int64

        For DataFrameGroupBy:

            >>> data = [[1, 2, 3], [1, 5, 6], [7, 8, 9]]
            >>> df = bpd.DataFrame(data, columns=["a", "b", "c"],
            ...                   index=["owl", "toucan", "eagle"])
            >>> df
                    a  b  c
            owl     1  2  3
            toucan  1  5  6
            eagle   7  8  9
            [3 rows x 3 columns]
            >>> df.groupby("a").size()
            a
            1    2
            7    1
            dtype: Int64

        Returns:
            bigframes.pandas.DataFrame or bigframes.pandas.Series:
                Number of rows in each group as a Series if as_index is True
                or a DataFrame if as_index is False.

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class SeriesGroupBy(GroupBy):
    def agg(self, func):
        """
        Aggregate using one or more operations.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4], index=[1, 1, 2, 2])
            >>> s.groupby(level=0).agg(['min', 'max'])
               min  max
            1    1    2
            2    3    4
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            func : function, str, list, dict or None
                Function to use for aggregating the data.

                Accepted combinations are:

                - string function name
                - list of function names, e.g. ``['sum', 'mean']``

        Returns:
            bigframes.pandas.Series:
              A BigQuery Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def aggregate(self, func):
        """
        Aggregate using one or more operations.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> s = bpd.Series([1, 2, 3, 4], index=[1, 1, 2, 2])
            >>> s.groupby(level=0).aggregate(['min', 'max'])
               min  max
            1    1    2
            2    3    4
            <BLANKLINE>
            [2 rows x 2 columns]

        Args:
            func : function, str, list, dict or None
                Function to use for aggregating the data.

                Accepted combinations are:

                - string function name
                - list of function names, e.g. ``['sum', 'mean']``

        Returns:
            bigframes.pandas.Series:
                A BigQuery Series.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self):
        """
        Return number of unique elements in the group.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> lst = ['a', 'a', 'b', 'b']
            >>> ser = bpd.Series([1, 2, 3, 3], index=lst)
            >>> ser.groupby(level=0).nunique()
            a    2
            b    1
            dtype: Int64

        Returns:
            bigframes.pandas.Series:
                Number of unique values within each group.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class DataFrameGroupBy(GroupBy):
    def agg(self, func, **kwargs):
        """
        Aggregate using one or more operations.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> data = {"A": [1, 1, 2, 2],
            ...         "B": [1, 2, 3, 4],
            ...         "C": [0.362838, 0.227877, 1.267767, -0.562860]}
            >>> df = bpd.DataFrame(data)

        The aggregation is for each column.

            >>> df.groupby('A').agg('min')
                B         C
            A
            1  1  0.227877
            2  3  -0.56286
            <BLANKLINE>
            [2 rows x 2 columns]

        Multiple aggregations

            >>> df.groupby('A').agg(['min', 'max'])
                B             C
                   min max       min       max
            A
            1        1   2  0.227877  0.362838
            2        3   4  -0.56286  1.267767
            <BLANKLINE>
            [2 rows x 4 columns]

        Args:
            func (function, str, list, dict or None):
                Function to use for aggregating the data.

                Accepted combinations are:

                - string function name
                - list of function names, e.g. ``['sum', 'mean']``
                - dict of axis labels -> function names or list of such.
                - None, in which case ``**kwargs`` are used with Named Aggregation. Here the
                  output has one column for each element in ``**kwargs``. The name of the
                  column is keyword, whereas the value determines the aggregation used to compute
                  the values in the column.

            kwargs
                If ``func`` is None, ``**kwargs`` are used to define the output names and
                aggregations via Named Aggregation. See ``func`` entry.

        Returns:
            bigframes.pandas.DataFrame:
                A BigQuery DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def aggregate(self, func, **kwargs):
        """
        Aggregate using one or more operations.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> data = {"A": [1, 1, 2, 2],
            ...         "B": [1, 2, 3, 4],
            ...         "C": [0.362838, 0.227877, 1.267767, -0.562860]}
            >>> df = bpd.DataFrame(data)

        The aggregation is for each column.

            >>> df.groupby('A').aggregate('min')
                B         C
            A
            1  1  0.227877
            2  3  -0.56286
            <BLANKLINE>
            [2 rows x 2 columns]

        Multiple aggregations

            >>> df.groupby('A').agg(['min', 'max'])
                B             C
                   min max       min       max
            A
            1        1   2  0.227877  0.362838
            2        3   4  -0.56286  1.267767
            <BLANKLINE>
            [2 rows x 4 columns]

        Args:
            func (function, str, list, dict or None):
                Function to use for aggregating the data.

                Accepted combinations are:

                - string function name
                - list of function names, e.g. ``['sum', 'mean']``
                - dict of axis labels -> function names or list of such.
                - None, in which case ``**kwargs`` are used with Named Aggregation. Here the
                  output has one column for each element in ``**kwargs``. The name of the
                  column is keyword, whereas the value determines the aggregation used to compute
                  the values in the column.

            kwargs
                If ``func`` is None, ``**kwargs`` are used to define the output names and
                aggregations via Named Aggregation. See ``func`` entry.

        Returns:
            bigframes.pandas.DataFrame:
                A BigQuery DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def nunique(self):
        """
        Return DataFrame with counts of unique elements in each position.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> bpd.options.display.progress_bar = None

            >>> df = bpd.DataFrame({'id': ['spam', 'egg', 'egg', 'spam',
            ...                           'ham', 'ham'],
            ...                    'value1': [1, 5, 5, 2, 5, 5],
            ...                    'value2': list('abbaxy')})
            >>> df.groupby('id').nunique()
                  value1  value2
            id
            egg        1       1
            ham        1       2
            spam       2       1
            <BLANKLINE>
            [3 rows x 2 columns]

        Returns:
            bigframes.pandas.DataFrame:
                Number of unique values within a BigQuery DataFrame.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
