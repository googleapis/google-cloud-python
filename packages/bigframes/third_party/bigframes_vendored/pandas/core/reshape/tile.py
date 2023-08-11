# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/tile.py
"""
Quantilization functions and related stuff
"""
from __future__ import annotations


def cut(
    x,
    bins,
    *,
    labels=None,
):
    """
    Bin values into discrete intervals.

    Use `cut` when you need to segment and sort data values into bins. This
    function is also useful for going from a continuous variable to a
    categorical variable. For example, `cut` could convert ages to groups of
    age ranges. Supports binning into an equal number of bins, or a
    pre-specified array of bins.

    ``labels=False`` implies you just want the bins back.

    Examples:

    .. code-block::

        import bigframes.pandas as pd

        pd.options.display.progress_bar = None
        s = pd.Series([0, 1, 1, 2])
        pd.cut(s, bins=4, labels=False)

        0    0
        1    1
        2    1
        3    3
        dtype: Int64

    Args:
        x (Series):
            The input Series to be binned. Must be 1-dimensional.
        bins (int):
            The criteria to bin by.

            int : Defines the number of equal-width bins in the range of `x`. The
            range of `x` is extended by .1% on each side to include the minimum
            and maximum values of `x`.
        labels (None):
            Specifies the labels for the returned bins. Must be the same length as
            the resulting bins. If False, returns only integer indicators of the
            bins. This affects the type of the output container (see below).
            If True, raises an error. When `ordered=False`, labels must be
            provided.

    Returns:
        Series: A Series representing the respective bin for each value
            of `x`. The type depends on the value of `labels`.
            sequence of scalars : returns a Series for Series `x` or a
            Categorical for all other inputs. The values stored within
            are whatever the type in the sequence is.
            False : returns an ndarray of integers.
    """
    raise NotImplementedError("abstract method")
