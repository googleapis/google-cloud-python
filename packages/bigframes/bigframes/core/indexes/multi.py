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

from typing import cast, Hashable, Iterable, Sequence

import bigframes_vendored.pandas.core.indexes.multi as vendored_pandas_multindex
import pandas

from bigframes.core.indexes.base import Index


class MultiIndex(Index, vendored_pandas_multindex.MultiIndex):
    __doc__ = vendored_pandas_multindex.MultiIndex.__doc__

    @classmethod
    def from_tuples(
        cls,
        tuples: Iterable[tuple[Hashable, ...]],
        sortorder: int | None = None,
        names: Sequence[Hashable] | Hashable | None = None,
    ) -> MultiIndex:
        pd_index = pandas.MultiIndex.from_tuples(tuples, sortorder, names)
        # Index.__new__ should detect multiple levels and properly create a multiindex
        return cast(MultiIndex, Index(pd_index))

    @classmethod
    def from_arrays(
        cls,
        arrays,
        sortorder: int | None = None,
        names=None,
    ) -> MultiIndex:
        pd_index = pandas.MultiIndex.from_arrays(arrays, sortorder, names)
        # Index.__new__ should detect multiple levels and properly create a multiindex
        return cast(MultiIndex, Index(pd_index))
