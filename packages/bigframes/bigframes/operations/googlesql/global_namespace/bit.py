# Copyright 2026 Google LLC
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
#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: scripts/data/sql-functions/global_namespace/bit.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from __future__ import annotations

from typing import Any, Literal, Union

import bigframes.core.col
import bigframes.core.googlesql
import bigframes.core.sentinels as sentinels
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql

_BIT_COUNT_OP = googlesql.GoogleSqlScalarOp(
    "BIT_COUNT",
    args=(googlesql.ArgSpec(),),
    signature=lambda *args: dtypes.INT_DTYPE,
)


def bit_count(
    expression: Union[
        series.Series,
        bigframes.core.col.Expression,
        Union[Any, Literal[sentinels.Sentinel.ARGUMENT_DEFAULT], bytes, int],
    ],
) -> Union[series.Series, bigframes.core.col.Expression]:
    """The input, `expression`, must be an integer or `BYTES`. Returns the number of bits that are set in the input expression. For signed integers, this is the number of bits in two's complement form."""
    return bigframes.core.googlesql.apply_googlesql_scalar_op(
        _BIT_COUNT_OP,
        expression,
    )
