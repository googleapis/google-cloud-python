# Copyright 2023 Google LLC
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

import typing

import ibis.expr.types as ibis_types

from bigframes.core import log_adapter
import bigframes.dataframe
import bigframes.operations
import bigframes.operations.base
import bigframes.series
import third_party.bigframes_vendored.pandas.core.arrays.arrow.accessors as vendoracessors


class _StructField(bigframes.operations.UnaryOp):
    def __init__(self, name_or_index: str | int):
        self._name_or_index = name_or_index

    def _as_ibis(self, x: ibis_types.Value):
        struct_value = typing.cast(ibis_types.StructValue, x)
        if isinstance(self._name_or_index, str):
            name = self._name_or_index
        else:
            name = struct_value.names[self._name_or_index]
        return struct_value[name].name(name)


@log_adapter.class_logger
class StructAccessor(
    bigframes.operations.base.SeriesMethods, vendoracessors.StructAccessor
):
    __doc__ = vendoracessors.StructAccessor.__doc__

    def field(self, name_or_index: str | int) -> bigframes.series.Series:
        series = self._apply_unary_op(_StructField(name_or_index))
        if isinstance(name_or_index, str):
            name = name_or_index
        else:
            struct_field = self._dtype.pyarrow_dtype[name_or_index]
            name = struct_field.name
        return series.rename(name)

    def explode(self) -> bigframes.dataframe.DataFrame:
        import bigframes.pandas

        pa_type = self._dtype.pyarrow_dtype
        return bigframes.pandas.concat(
            [self.field(i) for i in range(pa_type.num_fields)], axis="columns"
        )
