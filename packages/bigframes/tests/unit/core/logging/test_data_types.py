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

import pandas as pd
import pyarrow as pa
import pytest

from bigframes import dtypes
from bigframes.core.logging import data_types

UNKNOWN_TYPE = pd.ArrowDtype(pa.time64("ns"))

PA_STRUCT_TYPE = pa.struct([("city", pa.string()), ("pop", pa.int64())])

PA_LIST_TYPE = pa.list_(pa.int64())


@pytest.mark.parametrize(
    ("dtype", "expected_mask"),
    [
        (None, 0),
        (UNKNOWN_TYPE, 1 << 0),
        (dtypes.INT_DTYPE, 1 << 1),
        (dtypes.FLOAT_DTYPE, 1 << 2),
        (dtypes.BOOL_DTYPE, 1 << 3),
        (dtypes.STRING_DTYPE, 1 << 4),
        (dtypes.BYTES_DTYPE, 1 << 5),
        (dtypes.DATE_DTYPE, 1 << 6),
        (dtypes.TIME_DTYPE, 1 << 7),
        (dtypes.DATETIME_DTYPE, 1 << 8),
        (dtypes.TIMESTAMP_DTYPE, 1 << 9),
        (dtypes.TIMEDELTA_DTYPE, 1 << 10),
        (dtypes.NUMERIC_DTYPE, 1 << 11),
        (dtypes.BIGNUMERIC_DTYPE, 1 << 12),
        (dtypes.GEO_DTYPE, 1 << 13),
        (dtypes.JSON_DTYPE, 1 << 14),
        (pd.ArrowDtype(PA_STRUCT_TYPE), 1 << 15),
        (pd.ArrowDtype(PA_LIST_TYPE), 1 << 16),
        (dtypes.OBJ_REF_DTYPE, (1 << 15) | (1 << 17)),
    ],
)
def test_get_dtype_mask(dtype, expected_mask):
    assert data_types._get_dtype_mask(dtype) == expected_mask
