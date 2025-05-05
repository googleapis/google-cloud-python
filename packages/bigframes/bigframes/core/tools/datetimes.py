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

import bigframes_vendored.constants as constants
import bigframes_vendored.pandas.core.tools.datetimes as vendored_pandas_datetimes
import pandas as pd

import bigframes.dataframe
import bigframes.dtypes
import bigframes.operations as ops
import bigframes.series


def to_datetime(
    arg: Union[
        Union[int, float, str, datetime],
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

    if format and unit and arg.dtype in (bigframes.dtypes.INT_DTYPE, bigframes.dtypes.FLOAT_DTYPE):  # type: ignore
        raise ValueError("cannot specify both format and unit")

    if unit and arg.dtype not in (bigframes.dtypes.INT_DTYPE, bigframes.dtypes.FLOAT_DTYPE):  # type: ignore
        raise NotImplementedError(
            f"Unit parameter is not supported for non-numerical input types. {constants.FEEDBACK_LINK}"
        )

    if arg.dtype in (bigframes.dtypes.TIMESTAMP_DTYPE, bigframes.dtypes.DATETIME_DTYPE):
        to_type = (
            bigframes.dtypes.TIMESTAMP_DTYPE if utc else bigframes.dtypes.DATETIME_DTYPE
        )
        return arg._apply_unary_op(ops.AsTypeOp(to_type=to_type))  # type: ignore
    if (not utc) and arg.dtype == bigframes.dtypes.STRING_DTYPE:
        if format:
            raise NotImplementedError(
                f"Customized formats are not supported for string inputs when utc=False. Please set utc=True if possible. {constants.FEEDBACK_LINK}"
            )

        assert unit is None

        # The following operations evaluate individual values to infer a format,
        # so cache if needed.
        arg = arg._cached(force=False)

        as_datetime = arg._apply_unary_op(  # type: ignore
            ops.ToDatetimeOp(
                format=format,
                unit=unit,
            )
        )
        failed_datetime_cast = arg.notnull() & as_datetime.isnull()
        is_utc = arg._apply_unary_op(
            ops.EndsWithOp(
                pat=("Z", "-00:00", "+00:00", "-0000", "+0000", "-00", "+00")
            )
        )

        # Cast to DATETIME shall succeed if all inputs are tz-naive.
        if not failed_datetime_cast.any():
            return as_datetime

        if is_utc.all():
            return arg._apply_unary_op(  # type: ignore
                ops.ToTimestampOp(
                    format=format,
                    unit=unit,
                )
            )

        raise NotImplementedError(
            f"Non-UTC string inputs are not supported when utc=False. Please set utc=True if possible. {constants.FEEDBACK_LINK}"
        )
    # If utc:
    elif utc:
        return arg._apply_unary_op(  # type: ignore
            ops.ToTimestampOp(
                format=format,
                unit=unit,
            )
        )
    else:
        return arg._apply_unary_op(  # type: ignore
            ops.ToDatetimeOp(
                format=format,
                unit=unit,
            )
        )
