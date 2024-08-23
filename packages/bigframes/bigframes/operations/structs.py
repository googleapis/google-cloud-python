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

import bigframes_vendored.pandas.core.arrays.arrow.accessors as vendoracessors
import pandas as pd

from bigframes.core import log_adapter
import bigframes.dataframe
import bigframes.dtypes
import bigframes.operations
import bigframes.operations.base
import bigframes.series


@log_adapter.class_logger
class StructAccessor(
    bigframes.operations.base.SeriesMethods, vendoracessors.StructAccessor
):
    __doc__ = vendoracessors.StructAccessor.__doc__

    def field(self, name_or_index: str | int) -> bigframes.series.Series:
        series = self._apply_unary_op(bigframes.operations.StructFieldOp(name_or_index))
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

    def dtypes(self) -> pd.Series:
        pa_type = self._dtype.pyarrow_dtype
        return pd.Series(
            data=[
                bigframes.dtypes.arrow_dtype_to_bigframes_dtype(pa_type.field(i).type)
                for i in range(pa_type.num_fields)
            ],
            index=[pa_type.field(i).name for i in range(pa_type.num_fields)],
        )


@log_adapter.class_logger
class StructFrameAccessor(vendoracessors.StructFrameAccessor):
    __doc__ = vendoracessors.StructAccessor.__doc__

    def __init__(self, data: bigframes.dataframe.DataFrame) -> None:
        self._parent = data

    def explode(self, column, *, separator: str = ".") -> bigframes.dataframe.DataFrame:
        df = self._parent
        column_labels = bigframes.core.explode.check_column(column)

        for label in column_labels:
            position = df.columns.to_list().index(label)
            df = df.drop(columns=label)
            subfields = self._parent[label].struct.explode()
            for subfield in reversed(subfields.columns):
                df.insert(
                    position, f"{label}{separator}{subfield}", subfields[subfield]
                )

        return df
