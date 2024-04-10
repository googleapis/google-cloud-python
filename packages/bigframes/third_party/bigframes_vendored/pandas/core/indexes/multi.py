# Contains code from https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexes/multi.py
from __future__ import annotations

from typing import Hashable, Iterable, Sequence

import bigframes_vendored.pandas.core.indexes.base

from bigframes import constants


class MultiIndex(bigframes_vendored.pandas.core.indexes.base.Index):
    """
    A multi-level, or hierarchical, index object for pandas objects.
    """

    @classmethod
    def from_tuples(
        cls,
        tuples: Iterable[tuple[Hashable, ...]],
        sortorder: int | None = None,
        names: Sequence[Hashable] | Hashable | None = None,
    ) -> MultiIndex:
        """
        Convert list of tuples to MultiIndex.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> tuples = [(1, 'red'), (1, 'blue'),
            ...           (2, 'red'), (2, 'blue')]
            >>> bpd.MultiIndex.from_tuples(tuples, names=('number', 'color'))
            MultiIndex([(1,  'red'),
                        (1, 'blue'),
                        (2,  'red'),
                        (2, 'blue')],
                    names=['number', 'color'])

        Args:
            tuples (list / sequence of tuple-likes):
                Each tuple is the index of one row/column.
            sortorder (int or None):
                Level of sortedness (must be lexicographically sorted by that
                level).
            names (list / sequence of str, optional):
                Names for the levels in the index.

        Returns:
            MultiIndex
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @classmethod
    def from_arrays(
        cls,
        arrays,
        sortorder: int | None = None,
        names=None,
    ) -> MultiIndex:
        """
        Convert arrays to MultiIndex.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> bpd.options.display.progress_bar = None
            >>> arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue']]
            >>> bpd.MultiIndex.from_arrays(arrays, names=('number', 'color'))
            MultiIndex([(1,  'red'),
                        (1, 'blue'),
                        (2,  'red'),
                        (2, 'blue')],
                    names=['number', 'color'])

        Args:
            arrays (list / sequence of array-likes):
                Each array-like gives one level's value for each data point.
                len(arrays) is the number of levels.
            sortorder (int or None):
                Level of sortedness (must be lexicographically sorted by that
                level).
            names (list / sequence of str, optional):
                Names for the levels in the index.

        Returns:
            MultiIndex
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
