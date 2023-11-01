# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/concat.py
"""
Concat routines
"""
from __future__ import annotations

from bigframes import constants


def concat(
    objs,
    *,
    axis=0,
    join: str = "outer",
    ignore_index: bool = False,
):
    """
    Concatenate BigQuery DataFrames objects along a particular axis.

    Allows optional set logic along the other axes.

    Can also add a layer of hierarchical indexing on the concatenation axis,
    which may be useful if the labels are the same (or overlapping) on
    the passed axis number.

    Parameters
    ----------
    objs:
        Objects to concatenate. Any None objects will be dropped silently unless
        they are all None in which case a ValueError will be raised.
    axis : {0/'index', 1/'columns'}, default 0
        The axis to concatenate along.
    join: {'inner', 'outer'}, default 'outer'
        How to handle indexes on other axis (or axes).
    ignore_index : bool, default False
        If True, do not use the index values along the concatenation axis. The
        resulting axis will be labeled 0, ..., n - 1. This is useful if you are
        concatenating objects where the concatenation axis does not have
        meaningful indexing information. Note the index values on the other
        axes are still respected in the join.

    Returns
    -------
    object, type of objs
        When concatenating all ``Series`` along the index (axis=0), a
        ``Series`` is returned. When ``objs`` contains at least one
        ``DataFrame``, a ``DataFrame`` is returned.

    Notes
    -----
    It is not recommended to build DataFrames by adding single rows in a
    for loop. Build a list of rows and make a DataFrame in a single concat.

    Examples
    --------
    Combine two ``Series``.

    >>> import bigframes.pandas as pd
    >>> pd.options.display.progress_bar = None
    >>> s1 = pd.Series(['a', 'b'])
    >>> s2 = pd.Series(['c', 'd'])
    >>> pd.concat([s1, s2])
    0    a
    1    b
    0    c
    1    d
    dtype: string

    Clear the existing index and reset it in the result
    by setting the ``ignore_index`` option to ``True``.

    >>> pd.concat([s1, s2], ignore_index=True)
    0    a
    1    b
    2    c
    3    d
    dtype: string

    Combine two ``DataFrame`` objects with identical columns.

    >>> df1 = pd.DataFrame([['a', 1], ['b', 2]],
    ...                    columns=['letter', 'number'])
    >>> df1
      letter  number
    0      a       1
    1      b       2
    <BLANKLINE>
    [2 rows x 2 columns]
    >>> df2 = pd.DataFrame([['c', 3], ['d', 4]],
    ...                    columns=['letter', 'number'])
    >>> df2
      letter  number
    0      c       3
    1      d       4
    <BLANKLINE>
    [2 rows x 2 columns]
    >>> pd.concat([df1, df2])
      letter  number
    0      a       1
    1      b       2
    0      c       3
    1      d       4
    <BLANKLINE>
    [4 rows x 2 columns]

    Combine ``DataFrame`` objects with overlapping columns
    and return everything. Columns outside the intersection will
    be filled with ``NaN`` values.

    >>> df3 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']],
    ...                    columns=['letter', 'number', 'animal'])
    >>> df3
      letter  number animal
    0      c       3    cat
    1      d       4    dog
    <BLANKLINE>
    [2 rows x 3 columns]
    >>> pd.concat([df1, df3])
      letter  number animal
    0      a       1   <NA>
    1      b       2   <NA>
    0      c       3    cat
    1      d       4    dog
    <BLANKLINE>
    [4 rows x 3 columns]

    Combine ``DataFrame`` objects with overlapping columns
    and return only those that are shared by passing ``inner`` to
    the ``join`` keyword argument.

    >>> pd.concat([df1, df3], join="inner")
      letter  number
    0      a       1
    1      b       2
    0      c       3
    1      d       4
    <BLANKLINE>
    [4 rows x 2 columns]
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
