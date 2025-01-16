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
import datetime
import typing

import numpy as np
import pandas as pd
from pandas.tseries import offsets

from bigframes import dtypes
from bigframes.operations import base_ops


@dataclasses.dataclass(frozen=True)
class FloorDtOp(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "floor_dt"
    freq: str

    def output_type(self, *input_types):
        return input_types[0]


@dataclasses.dataclass(frozen=True)
class DatetimeToIntegerLabelOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "datetime_to_integer_label"
    freq: offsets.DateOffset
    closed: typing.Optional[typing.Literal["right", "left"]]
    origin: typing.Union[
        typing.Union[pd.Timestamp, datetime.datetime, np.datetime64, int, float, str],
        typing.Literal["epoch", "start", "start_day", "end", "end_day"],
    ]

    def output_type(self, *input_types):
        return dtypes.INT_DTYPE


@dataclasses.dataclass(frozen=True)
class IntegerLabelToDatetimeOp(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "integer_label_to_datetime"
    freq: offsets.DateOffset
    label: typing.Optional[typing.Literal["right", "left"]]
    origin: typing.Union[
        typing.Union[pd.Timestamp, datetime.datetime, np.datetime64, int, float, str],
        typing.Literal["epoch", "start", "start_day", "end", "end_day"],
    ]

    def output_type(self, *input_types):
        return input_types[1]
