# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py
from __future__ import annotations

from bigframes import constants


def crosstab(
    index,
    columns,
    values=None,
    rownames=None,
    colnames=None,
    aggfunc=None,
):
    """
    Compute a simple cross tabulation of two (or more) factors.

    By default, computes a frequency table of the factors unless an
    array of values and an aggregation function are passed.

    **Examples:**
        >>> a = np.array(["foo", "foo", "foo", "foo", "bar", "bar",
        ...               "bar", "bar", "foo", "foo", "foo"], dtype=object)
        >>> b = np.array(["one", "one", "one", "two", "one", "one",
        ...               "one", "two", "two", "two", "one"], dtype=object)
        >>> c = np.array(["dull", "dull", "shiny", "dull", "dull", "shiny",
        ...               "shiny", "dull", "shiny", "shiny", "shiny"],
        ...              dtype=object)
        >>> bpd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
        b    one        two
        c   dull shiny dull shiny
        a
        bar    1     2    1     0
        foo    2     2    1     2
        <BLANKLINE>
        [2 rows x 4 columns]

    Args:
        index (array-like, Series, or list of arrays/Series):
            Values to group by in the rows.
        columns (array-like, Series, or list of arrays/Series):
            Values to group by in the columns.
        values (array-like, optional):
            Array of values to aggregate according to the factors.
            Requires `aggfunc` be specified.
        rownames (sequence, default None):
            If passed, must match number of row arrays passed.
        colnames (sequence, default None):
            If passed, must match number of column arrays passed.
        aggfunc (function, optional):
            If specified, requires `values` be specified as well.

    Returns:
        DataFrame:
            Cross tabulation of the data.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
