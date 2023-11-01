# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/encoding.py
"""
Encoding routines
"""
from __future__ import annotations

from bigframes import constants


def get_dummies(
    data,
    prefix=None,
    prefix_sep="_",
    dummy_na=False,
    columns=None,
    drop_first=False,
    dtype=None,
):
    """
    Convert categorical variable into dummy/indicator variables.

    Each variable is converted in as many 0/1 variables as there are
    different values. Columns in the output are each named after a value;
    if the input is a DataFrame, the name of the original variable is
    prepended to the value.

    **Examples:**
        >>> import bigframes.pandas as pd
        >>> pd.options.display.progress_bar = None
        >>> s = pd.Series(list('abca'))
        >>> pd.get_dummies(s)
               a      b      c
        0   True  False  False
        1  False   True  False
        2  False  False   True
        3   True  False  False
        <BLANKLINE>
        [4 rows x 3 columns]

        >>> s1 = pd.Series(['a', 'b', None])
        >>> pd.get_dummies(s1)
               a      b
        0   True  False
        1  False   True
        2  False  False
        <BLANKLINE>
        [3 rows x 2 columns]

        >>> pd.get_dummies(s1, dummy_na=True)
               a      b   <NA>
        0   True  False  False
        1  False   True  False
        2  False  False   True
        <BLANKLINE>
        [3 rows x 3 columns]

        >>> df = pd.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'], 'C': [1, 2, 3]})
        >>> pd.get_dummies(df, prefix=['col1', 'col2'])
           C  col1_a  col1_b  col2_a  col2_b  col2_c
        0  1    True   False   False    True   False
        1  2   False    True    True   False   False
        2  3    True   False   False   False    True
        <BLANKLINE>
        [3 rows x 6 columns]

        >>> pd.get_dummies(pd.Series(list('abcaa')))
               a      b      c
        0   True  False  False
        1  False   True  False
        2  False  False   True
        3   True  False  False
        4   True  False  False
        <BLANKLINE>
        [5 rows x 3 columns]

        >>> pd.get_dummies(pd.Series(list('abcaa')), drop_first=True)
               b      c
        0  False  False
        1   True  False
        2  False   True
        3  False  False
        4  False  False
        <BLANKLINE>
        [5 rows x 2 columns]

    Args:
      data (Series or DataFrame):
        Data of which to get dummy indicators.

      prefix (str, list of str, or dict of str, default None):
        String to append DataFrame column names. Pass a list with length
        equal to the number of columns when calling get_dummies on a
        DataFrame. Alternatively, prefix can be a dictionary mapping column
        names to prefixes.

      prefix_sep (str, list of str, or dict of str, default '_'):
        Separator/delimiter to use, appended to prefix. Or pass a list or
        dictionary as with prefix.

      dummy_na (bool, default False):
        Add a column to indicate NaNs, if False NaNs are ignored.

      columns (list-like, default None):
        Column names in the DataFrame to be encoded. If columns is None
        then only the columns with string dtype will be converted.

      drop_first (bool, default False):
        Whether to get k-1 dummies out of k categorical levels by removing the
        first level.

      dtype (dtype, default bool):
        Data type for new columns. Only a single dtype is allowed.

    Returns:
      DataFrame: Dummy-coded data. If data contains other columns than the
      dummy-coded one(s), these will be prepended, unaltered, to the
      result.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
