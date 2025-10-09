# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import cast, Hashable, Iterable, Optional, Sequence, TYPE_CHECKING

import bigframes_vendored.pandas.core.indexes.multi as vendored_pandas_multindex
import pandas

from bigframes.core import blocks
from bigframes.core import expression as ex
from bigframes.core.indexes.base import Index

if TYPE_CHECKING:
    import bigframes.session


class MultiIndex(Index, vendored_pandas_multindex.MultiIndex):
    __doc__ = vendored_pandas_multindex.MultiIndex.__doc__

    @classmethod
    def from_tuples(
        cls,
        tuples: Iterable[tuple[Hashable, ...]],
        sortorder: int | None = None,
        names: Sequence[Hashable] | Hashable | None = None,
        *,
        session: Optional[bigframes.session.Session] = None,
    ) -> MultiIndex:
        pd_index = pandas.MultiIndex.from_tuples(tuples, sortorder, names)
        # Index.__new__ should detect multiple levels and properly create a multiindex
        return cast(MultiIndex, Index(pd_index, session=session))

    @classmethod
    def from_arrays(
        cls,
        arrays,
        sortorder: int | None = None,
        names=None,
        *,
        session: Optional[bigframes.session.Session] = None,
    ) -> MultiIndex:
        pd_index = pandas.MultiIndex.from_arrays(arrays, sortorder, names)
        # Index.__new__ should detect multiple levels and properly create a multiindex
        return cast(MultiIndex, Index(pd_index, session=session))

    def __eq__(self, other) -> Index:  # type: ignore
        import bigframes.operations as ops
        import bigframes.operations.aggregations as agg_ops

        eq_result = self._apply_binop(other, ops.eq_op)._block.expr

        as_array = ops.ToArrayOp().as_expr(
            *(
                ops.fillna_op.as_expr(col, ex.const(False))
                for col in eq_result.column_ids
            )
        )
        reduced = ops.ArrayReduceOp(agg_ops.all_op).as_expr(as_array)
        result_expr, result_ids = eq_result.compute_values([reduced])
        return Index(
            blocks.Block(
                result_expr.select_columns(result_ids),
                index_columns=result_ids,
                column_labels=(),
                index_labels=[None],
            )
        )


class MultiIndexAccessor:
    """Proxy to MultiIndex constructors to allow a session to be passed in."""

    def __init__(self, session: bigframes.session.Session):
        self._session = session

    def __call__(self, *args, **kwargs) -> MultiIndex:
        """Construct a MultiIndex using the associated Session.

        See :class:`bigframes.pandas.MultiIndex`.
        """
        return MultiIndex(*args, session=self._session, **kwargs)

    def from_arrays(self, *args, **kwargs) -> MultiIndex:
        """Construct a MultiIndex using the associated Session.

        See :func:`bigframes.pandas.MultiIndex.from_arrays`.
        """
        return MultiIndex.from_arrays(*args, session=self._session, **kwargs)

    def from_frame(self, *args, **kwargs) -> MultiIndex:
        """Construct a MultiIndex using the associated Session.

        See :func:`bigframes.pandas.MultiIndex.from_frame`.
        """
        return cast(MultiIndex, MultiIndex.from_frame(*args, **kwargs))

    def from_tuples(self, *args, **kwargs) -> MultiIndex:
        """Construct a MultiIndex using the associated Session.

        See :func:`bigframes.pandas.MultiIndex.from_tuples`.
        """
        return MultiIndex.from_tuples(*args, session=self._session, **kwargs)
