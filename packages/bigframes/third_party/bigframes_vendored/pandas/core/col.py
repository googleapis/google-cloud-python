# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/col.py
from __future__ import annotations

from collections.abc import Hashable

from bigframes import constants


class Expression:
    """
    Class representing a deferred column.

    This is not meant to be instantiated directly. Instead, use :meth:`pandas.col`.
    """


def col(col_name: Hashable) -> Expression:
    """
    Generate deferred object representing a column of a DataFrame.

    Any place which accepts ``lambda df: df[col_name]``, such as
    :meth:`DataFrame.assign` or :meth:`DataFrame.loc`, can also accept
    ``pd.col(col_name)``.

    Args:
        col_name (Hashable):
            Column name.

    Returns:
        Expression:
            A deferred object representing a column of a DataFrame.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


__all__ = ["Expression", "col"]
