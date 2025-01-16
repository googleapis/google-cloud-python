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

import dataclasses
import typing

import pandas as pd
import pyarrow as pa

from bigframes import dtypes
from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class StructFieldOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "struct_field"
    name_or_index: typing.Union[str, int]

    def output_type(self, *input_types):
        input_type = input_types[0]
        if not isinstance(input_type, pd.ArrowDtype):
            raise TypeError("field accessor input must be a struct type")

        pa_type = input_type.pyarrow_dtype
        if not isinstance(pa_type, pa.StructType):
            raise TypeError("field accessor input must be a struct type")

        pa_result_type = pa_type[self.name_or_index].type
        return dtypes.arrow_dtype_to_bigframes_dtype(pa_result_type)


@dataclasses.dataclass(frozen=True)
class StructOp(base_ops.NaryOp):
    name: typing.ClassVar[str] = "struct"
    column_names: tuple[str]

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        num_input_types = len(input_types)
        # value1, value2, ...
        assert num_input_types == len(self.column_names)
        fields = []

        for i in range(num_input_types):
            arrow_type = dtypes.bigframes_dtype_to_arrow_dtype(input_types[i])
            fields.append(
                pa.field(
                    self.column_names[i],
                    arrow_type,
                    nullable=(not pa.types.is_list(arrow_type)),
                )
            )
        return pd.ArrowDtype(
            pa.struct(fields)
        )  # [(name1, value1), (name2, value2), ...]
