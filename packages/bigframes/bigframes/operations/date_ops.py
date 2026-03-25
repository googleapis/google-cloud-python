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

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

DayOp = base_ops.create_unary_op(
    name="day",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
day_op = DayOp()

MonthOp = base_ops.create_unary_op(
    name="month",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
month_op = MonthOp()

YearOp = base_ops.create_unary_op(
    name="year",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
year_op = YearOp()

IsoDayOp = base_ops.create_unary_op(
    name="iso_day", type_signature=op_typing.DATELIKE_ACCESSOR
)
iso_day_op = IsoDayOp()

IsoWeekOp = base_ops.create_unary_op(
    name="iso_weeek",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
iso_week_op = IsoWeekOp()

IsoYearOp = base_ops.create_unary_op(
    name="iso_year",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
iso_year_op = IsoYearOp()

DayOfWeekOp = base_ops.create_unary_op(
    name="dayofweek",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
dayofweek_op = DayOfWeekOp()

DayOfYearOp = base_ops.create_unary_op(
    name="dayofyear",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
dayofyear_op = DayOfYearOp()

QuarterOp = base_ops.create_unary_op(
    name="quarter",
    type_signature=op_typing.DATELIKE_ACCESSOR,
)
quarter_op = QuarterOp()


@dataclasses.dataclass(frozen=True)
class DateDiffOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "date_diff"

    def output_type(self, *input_types: dtypes.ExpressionType) -> dtypes.ExpressionType:
        if input_types[0] is not input_types[1]:
            raise TypeError(
                f"two inputs have different types. left: {input_types[0]}, right: {input_types[1]}"
            )

        if input_types[0] != dtypes.DATE_DTYPE:
            raise TypeError("expected date input")

        return dtypes.TIMEDELTA_DTYPE


date_diff_op = DateDiffOp()
