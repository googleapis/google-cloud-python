# Copyright 2025 Google LLC
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

import dataclasses
import functools
from typing import Any, Dict, Iterable, Optional, Sequence, TYPE_CHECKING

from bigframes.core import blocks
import bigframes.enums

if TYPE_CHECKING:
    import bigframes.dataframe


@dataclasses.dataclass(frozen=True)
class InterchangeColumn:
    _dataframe: InterchangeDataFrame
    _pos: int

    @functools.cache
    def _arrow_column(self):
        # Conservatively downloads the whole underlying dataframe
        # This is much better if multiple columns end up being used,
        # but does incur a lot of overhead otherwise.
        return self._dataframe._arrow_dataframe().get_column(self._pos)

    def size(self) -> int:
        return self._arrow_column().size()

    @property
    def offset(self) -> int:
        return self._arrow_column().offset

    @property
    def dtype(self):
        return self._arrow_column().dtype

    @property
    def describe_categorical(self):
        raise TypeError(f"Column type {self.dtype} is not categorical")

    @property
    def describe_null(self):
        return self._arrow_column().describe_null

    @property
    def null_count(self):
        return self._arrow_column().null_count

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._arrow_column().metadata

    def num_chunks(self) -> int:
        return self._arrow_column().num_chunks()

    def get_chunks(self, n_chunks: Optional[int] = None) -> Iterable:
        return self._arrow_column().get_chunks(n_chunks=n_chunks)

    def get_buffers(self):
        return self._arrow_column().get_buffers()


@dataclasses.dataclass(frozen=True)
class InterchangeDataFrame:
    """
    Implements the dataframe interchange format.

    Mostly implemented by downloading result to pyarrow, and using pyarrow interchange implementation.
    """

    _value: blocks.Block

    version: int = 0  # version of the protocol

    def __dataframe__(
        self, nan_as_null: bool = False, allow_copy: bool = True
    ) -> InterchangeDataFrame:
        return self

    @classmethod
    def _from_bigframes(cls, df: bigframes.dataframe.DataFrame):
        block = df._block.with_column_labels(
            [str(label) for label in df._block.column_labels]
        )
        return cls(block)

    # In future, could potentially rely on executor to refetch batches efficiently with caching,
    # but safest for now to just request a single execution and save the whole table.
    @functools.cache
    def _arrow_dataframe(self):
        arrow_table, _ = self._value.reset_index(
            replacement=bigframes.enums.DefaultIndexKind.NULL
        ).to_arrow(allow_large_results=False)
        return arrow_table.__dataframe__()

    @property
    def metadata(self):
        # Allows round-trip without materialization
        return {"bigframes.block": self._value}

    def num_columns(self) -> int:
        """
        Return the number of columns in the DataFrame.
        """
        return len(self._value.value_columns)

    def num_rows(self) -> Optional[int]:
        return self._value.shape[0]

    def num_chunks(self) -> int:
        return self._arrow_dataframe().num_chunks()

    def column_names(self) -> Iterable[str]:
        return [col for col in self._value.column_labels]

    def get_column(self, i: int) -> InterchangeColumn:
        return InterchangeColumn(self, i)

    # For single column getters, we download the whole dataframe still
    # This is inefficient in some cases, but more efficient in other
    def get_column_by_name(self, name: str) -> InterchangeColumn:
        col_id = self._value.resolve_label_exact(name)
        assert col_id is not None
        pos = self._value.value_columns.index(col_id)
        return InterchangeColumn(self, pos)

    def get_columns(self) -> Iterable[InterchangeColumn]:
        return [InterchangeColumn(self, i) for i in range(self.num_columns())]

    def select_columns(self, indices: Sequence[int]) -> InterchangeDataFrame:
        col_ids = [self._value.value_columns[i] for i in indices]
        new_value = self._value.select_columns(col_ids)
        return InterchangeDataFrame(new_value)

    def select_columns_by_name(self, names: Sequence[str]) -> InterchangeDataFrame:
        col_ids = [self._value.resolve_label_exact(name) for name in names]
        assert all(id is not None for id in col_ids)
        new_value = self._value.select_columns(col_ids)  # type: ignore
        return InterchangeDataFrame(new_value)

    def get_chunks(self, n_chunks: Optional[int] = None) -> Iterable:
        return self._arrow_dataframe().get_chunks(n_chunks)
