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

import typing

import bigframes_vendored.constants as constants
import numpy as np
import pandas as pd
import pyarrow as pa
import sqlglot as sg

import bigframes.dtypes


class SQLGlotType:
    @classmethod
    def from_bigframes_dtype(
        cls,
        bigframes_dtype: typing.Union[
            bigframes.dtypes.DtypeString, bigframes.dtypes.Dtype, np.dtype[typing.Any]
        ],
    ) -> str:
        if bigframes_dtype == bigframes.dtypes.INT_DTYPE:
            return "INT64"
        elif bigframes_dtype == bigframes.dtypes.FLOAT_DTYPE:
            return "FLOAT64"
        elif bigframes_dtype == bigframes.dtypes.STRING_DTYPE:
            return "STRING"
        elif bigframes_dtype == bigframes.dtypes.BOOL_DTYPE:
            return "BOOLEAN"
        elif bigframes_dtype == bigframes.dtypes.DATE_DTYPE:
            return "DATE"
        elif bigframes_dtype == bigframes.dtypes.TIME_DTYPE:
            return "TIME"
        elif bigframes_dtype == bigframes.dtypes.DATETIME_DTYPE:
            return "DATETIME"
        elif bigframes_dtype == bigframes.dtypes.TIMESTAMP_DTYPE:
            return "TIMESTAMP"
        elif bigframes_dtype == bigframes.dtypes.BYTES_DTYPE:
            return "BYTES"
        elif bigframes_dtype == bigframes.dtypes.NUMERIC_DTYPE:
            return "NUMERIC"
        elif bigframes_dtype == bigframes.dtypes.BIGNUMERIC_DTYPE:
            return "BIGNUMERIC"
        elif bigframes_dtype == bigframes.dtypes.JSON_DTYPE:
            return "JSON"
        elif bigframes_dtype == bigframes.dtypes.GEO_DTYPE:
            return "GEOGRAPHY"
        elif bigframes_dtype == bigframes.dtypes.TIMEDELTA_DTYPE:
            return "INT64"
        elif isinstance(bigframes_dtype, pd.ArrowDtype):
            if pa.types.is_list(bigframes_dtype.pyarrow_dtype):
                inner_bigframes_dtype = bigframes.dtypes.arrow_dtype_to_bigframes_dtype(
                    bigframes_dtype.pyarrow_dtype.value_type
                )
                return (
                    f"ARRAY<{SQLGlotType.from_bigframes_dtype(inner_bigframes_dtype)}>"
                )
            elif pa.types.is_struct(bigframes_dtype.pyarrow_dtype):
                struct_type = typing.cast(pa.StructType, bigframes_dtype.pyarrow_dtype)
                inner_fields: list[str] = []
                for i in range(struct_type.num_fields):
                    field = struct_type.field(i)
                    key = sg.to_identifier(field.name).sql("bigquery")
                    dtype = SQLGlotType.from_bigframes_dtype(
                        bigframes.dtypes.arrow_dtype_to_bigframes_dtype(field.type)
                    )
                    inner_fields.append(f"{key} {dtype}")
                return "STRUCT<{}>".format(", ".join(inner_fields))

        raise ValueError(
            f"Unsupported type for {bigframes_dtype}. {constants.FEEDBACK_LINK}"
        )
