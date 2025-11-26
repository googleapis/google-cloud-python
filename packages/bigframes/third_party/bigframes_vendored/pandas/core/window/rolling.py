# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/window/rolling.py
"""
Provide a generic structure to support window functions,
similar to how we have a Groupby object.
"""

from bigframes import constants


class Window:
    """Provide window calculations."""

    def count(self):
        """Calculate the window count of non-NULL observations."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def sum(self):
        """Calculate the weighted window sum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def mean(self):
        """Calculate the weighted window mean."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def var(self):
        """Calculate the weighted window variance."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def std(self):
        """Calculate the weighted window standard deviation."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def max(self):
        """Calculate the weighted window maximum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def min(self):
        """Calculate the weighted window minimum."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def agg(self, func):
        """
        Aggregate using one or more operations over the specified axis.

        **Examples:**

            >>> import bigframes.pandas as bpd

            >>> df = bpd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
            >>> df
               A  B  C
            0  1  4  7
            1  2  5  8
            2  3  6  9
            <BLANKLINE>
            [3 rows x 3 columns]

            >>> df.rolling(2).sum()
                  A     B     C
            0  <NA>  <NA>  <NA>
            1     3     9    15
            2     5    11    17
            <BLANKLINE>
            [3 rows x 3 columns]

            >>> df.rolling(2).agg({"A": "sum", "B": "min"})
                  A    B
            0  <NA> <NA>
            1     3    4
            2     5    5
            <BLANKLINE>
            [3 rows x 2 columns]

        Args:
            func (function, str, list or dict):
                Function to use for aggregating the data.

                Accepted combinations are:

                - string function name
                - list of function names, e.g. ``['sum', 'mean']``
                - dict of axis labels -> function names or list of such.

        Returns:
            Series or DataFrame

        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
