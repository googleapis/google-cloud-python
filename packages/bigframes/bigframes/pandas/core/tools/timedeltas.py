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

import typing

from bigframes_vendored.pandas.core.tools import (
    timedeltas as vendored_pandas_timedeltas,
)
import pandas as pd
import pandas.api.types as pdtypes

from bigframes import operations as ops
from bigframes import series, session


def to_timedelta(
    arg,
    unit: typing.Optional[vendored_pandas_timedeltas.UnitChoices] = None,
    *,
    session: typing.Optional[session.Session] = None,
):
    if isinstance(arg, series.Series):
        canonical_unit = "us" if unit is None else _canonicalize_unit(unit)
        return arg._apply_unary_op(ops.ToTimedeltaOp(canonical_unit))

    if pdtypes.is_list_like(arg):
        return to_timedelta(series.Series(arg), unit, session=session)

    return pd.to_timedelta(arg, unit)


to_timedelta.__doc__ = vendored_pandas_timedeltas.to_timedelta.__doc__


def _canonicalize_unit(
    unit: vendored_pandas_timedeltas.UnitChoices,
) -> typing.Literal["us", "ms", "s", "m", "h", "d", "W"]:
    if unit in {"w", "W"}:
        return "W"

    if unit in {"D", "d", "days", "day"}:
        return "d"

    if unit in {"hours", "hour", "hr", "h"}:
        return "h"

    if unit in {"m", "minute", "min", "minutes"}:
        return "m"

    if unit in {"s", "seconds", "sec", "second"}:
        return "s"

    if unit in {"ms", "milliseconds", "millisecond", "milli", "millis"}:
        return "ms"

    if unit in {"us", "microseconds", "microsecond", "µs", "micro", "micros"}:
        return "us"

    raise TypeError(f"Unrecognized unit: {unit}")
