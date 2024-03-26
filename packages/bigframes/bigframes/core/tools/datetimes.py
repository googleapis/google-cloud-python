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

from collections.abc import Mapping
from datetime import datetime
from typing import Optional, Union

import bigframes_vendored.pandas.core.tools.datetimes as vendored_pandas_datetimes
import pandas as pd

import bigframes.constants as constants
import bigframes.dataframe
import bigframes.operations as ops
import bigframes.series


def to_datetime(
    arg: Union[
        vendored_pandas_datetimes.local_scalars,
        vendored_pandas_datetimes.local_iterables,
        bigframes.series.Series,
        bigframes.dataframe.DataFrame,
    ],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> Union[pd.Timestamp, datetime, bigframes.series.Series]:
    if isinstance(arg, (int, float, str, datetime)):
        return pd.to_datetime(
            arg,
            utc=utc,
            format=format,
            unit=unit,
        )

    if isinstance(arg, (Mapping, pd.DataFrame, bigframes.dataframe.DataFrame)):
        raise NotImplementedError(
            "Conversion of Mapping, pandas.DataFrame, or bigframes.dataframe.DataFrame "
            f"to datetime is not implemented. {constants.FEEDBACK_LINK}"
        )

    arg = bigframes.series.Series(arg)

    if not utc and arg.dtype not in ("Int64", "Float64"):  # type: ignore
        raise NotImplementedError(
            f"String and Timestamp requires utc=True. {constants.FEEDBACK_LINK}"
        )

    if format and unit and arg.dtype in ("Int64", "Float64"):  # type: ignore
        raise ValueError("cannot specify both format and unit")

    if unit and arg.dtype not in ("Int64", "Float64"):  # type: ignore
        raise NotImplementedError(
            f"Unit parameter is not supported for non-numerical input types. {constants.FEEDBACK_LINK}"
        )

    return arg._apply_unary_op(  # type: ignore
        ops.ToDatetimeOp(
            utc=utc,
            format=format,
            unit=unit,
        )
    )
