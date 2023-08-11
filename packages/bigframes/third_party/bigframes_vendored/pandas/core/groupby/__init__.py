# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/groupby/groupby.py
"""
Provide the groupby split-apply-combine paradigm. Define the GroupBy
class providing the base-class of operations.

The SeriesGroupBy and DataFrameGroupBy sub-class
(defined in pandas.core.groupby.generic)
expose these user-facing objects to provide specific functionality.
"""
from __future__ import annotations


class GroupBy:
    """
    Class for grouping and aggregating relational data.
    """

    def any(self):
        """
        Return True if any value in the group is true, else False.

        Returns:
            Series or DataFrame: DataFrame or Series of boolean values,
                where a value is True if any element is True within its
                respective group, False otherwise.
        """
        raise NotImplementedError("abstract property")

    def all(self):
        """
        Return True if all values in the group are true, else False.

        Returns:
            Series or DataFrame: DataFrame or Series of boolean values,
                where a value is True if all elements are True within its
                respective group, False otherwise.
        """
        raise NotImplementedError("abstract property")

    def count(self):
        """
        Compute count of group, excluding missing values.

        Returns:
            Series or DataFrame: Count of values within each group.
        """
        raise NotImplementedError("abstract property")

    def mean(
        self,
        numeric_only: bool = False,
    ):
        """
        Compute mean of groups, excluding missing values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.

        Returns:
            pandas.Series or pandas.DataFrame: Mean of groups.
        """
        raise NotImplementedError("abstract property")

    def median(
        self,
        numeric_only: bool = False,
        *,
        exact: bool = False,
    ):
        """
        Compute median of groups, excluding missing values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            exact (bool, default False):
                Calculate the exact median instead of an approximation. Note:
                    ``exact=True`` not yet supported.

        Returns:
            pandas.Series or pandas.DataFrame: Median of groups.
        """
        raise NotImplementedError("abstract property")

    def std(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Compute standard deviation of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            Series or DataFrame: Standard deviation of values within each group.
        """
        raise NotImplementedError("abstract property")

    def var(
        self,
        *,
        numeric_only: bool = False,
    ):
        """
        Compute variance of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Args:
            numeric_only (bool, default False):
                Include only `float`, `int` or `boolean` data.

        Returns:
            Series or DataFrame
                Variance of values within each group.
        """
        raise NotImplementedError("abstract property")

    def sum(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
    ):
        """
        Compute sum of group values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` non-NA values are present the result will be NA.

        Returns:
            Series or DataFrame: Computed sum of values within each group.
        """
        raise NotImplementedError("abstract property")

    def prod(self, numeric_only: bool = False, min_count: int = 0):
        """
        Compute prod of group values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` non-NA values are present the result will be NA.

        Returns:
            Series or DataFrame: Computed prod of values within each group.
        """
        raise NotImplementedError("abstract property")

    def min(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
    ):
        """
        Compute min of group values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` non-NA values are present the result will be NA.

        Returns:
            Series or DataFrame: Computed min of values within each group.
        """
        raise NotImplementedError("abstract property")

    def max(
        self,
        numeric_only: bool = False,
        min_count: int = -1,
    ):
        """
        Compute max of group values.

        Args:
            numeric_only (bool, default False):
                Include only float, int, boolean columns.
            min_count (int, default 0):
                The required number of valid values to perform the operation. If fewer
                than ``min_count`` non-NA values are present the result will be NA.

        Returns:
            Series or DataFrame: Computed max of values within each group.
        """
        raise NotImplementedError("abstract property")

    def cumcount(self, ascending: bool = True):
        """
        Number each item in each group from 0 to the length of that group - 1.

        Args:
            ascending (bool, default True):
                If False, number in reverse, from length of group - 1 to 0.

        Returns:
            Series: Sequence number of each element within each group.
        """
        raise NotImplementedError("abstract property")

    def cumprod(self, *args, **kwargs):
        """
        Cumulative product for each group.

        Returns:
            Series or DataFrame: Cumulative product for each group.
        """
        raise NotImplementedError("abstract property")

    def cumsum(self, *args, **kwargs):
        """
        Cumulative sum for each group.

        Returns:
            Series or DataFrame: Cumulative sum for each group.
        """
        raise NotImplementedError("abstract property")

    def cummin(self, *args, numeric_only: bool = False, **kwargs):
        """
        Cumulative min for each group.

        Returns:
            Series or DataFrame: Cumulative min for each group.
        """
        raise NotImplementedError("abstract property")

    def cummax(self, *args, numeric_only: bool = False, **kwargs):
        """
        Cumulative max for each group.

        Returns:
            Series or DataFrame: Cumulative max for each group.
        """
        raise NotImplementedError("abstract property")

    def diff(self):
        """
        First discrete difference of element.
        Calculates the difference of each element compared with another
        element in the group (default is element in previous row).

        Returns:
            Series or DataFrame: First differences.
        """
        raise NotImplementedError("abstract property")

    def shift(self, periods: int = 1):
        """
        Shift each group by periods observations.

        Args:
            periods (int, default 1):
                Number of periods to shift.

        Returns:
            Series or DataFrame: Object shifted within each group.
        """
        raise NotImplementedError("abstract property")

    def rolling(self, *args, **kwargs):
        """
        Returns a rolling grouper, providing rolling functionality per group.

        Args:
            min_periods (int, default None):
                Minimum number of observations in window required to have a value;
                otherwise, result is ``np.nan``.

                For a window that is specified by an offset,
                ``min_periods`` will default to 1.

                For a window that is specified by an integer, ``min_periods`` will default
                to the size of the window.

        Returns:
            Series or DataFrame: Return a new grouper with our rolling appended.
        """
        raise NotImplementedError("abstract property")

    def expanding(self, *args, **kwargs):
        """
        Provides expanding functionality.

        Returns:
            Series or DataFrame: A expanding grouper, providing expanding functionality per group.
        """
        raise NotImplementedError("abstract property")


class SeriesGroupBy(GroupBy):
    pass


class DataFrameGroupBy(GroupBy):
    pass
