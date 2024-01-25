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

import dataclasses
import functools

import pandas as pd

import bigframes.dtypes
from bigframes.dtypes import ExpressionType

# TODO: Apply input type constraints to help pre-empt invalid expression construction


@dataclasses.dataclass
class OpTypeRule:
    def output_type(self, *input_types: ExpressionType) -> ExpressionType:
        raise NotImplementedError("Abstract typing rule has no output type")

    @property
    def as_method(self):
        def meth(_, *input_types: ExpressionType) -> ExpressionType:
            return self.output_type(*input_types)

        return meth


@dataclasses.dataclass
class InputType(OpTypeRule):
    def output_type(self, *input_types: ExpressionType) -> ExpressionType:
        assert len(input_types) == 1
        return input_types[0]


@dataclasses.dataclass
class RealNumeric(OpTypeRule):
    def output_type(self, *input_types: ExpressionType) -> ExpressionType:
        all_ints = all(pd.api.types.is_integer(input) for input in input_types)
        if all_ints:
            return bigframes.dtypes.FLOAT_DTYPE
        else:
            return functools.reduce(
                lambda t1, t2: bigframes.dtypes.lcd_etype(t1, t2), input_types
            )


@dataclasses.dataclass
class Supertype(OpTypeRule):
    def output_type(self, *input_types: ExpressionType) -> ExpressionType:
        return functools.reduce(
            lambda t1, t2: bigframes.dtypes.lcd_etype(t1, t2), input_types
        )


@dataclasses.dataclass
class Fixed(OpTypeRule):
    out_type: ExpressionType

    def output_type(self, *input_types: ExpressionType) -> ExpressionType:
        return self.out_type


# Common type rules
NUMERIC = Supertype()
REAL_NUMERIC = RealNumeric()
PREDICATE = Fixed(bigframes.dtypes.BOOL_DTYPE)
INTEGER = Fixed(bigframes.dtypes.INT_DTYPE)
STRING = Fixed(bigframes.dtypes.STRING_DTYPE)
INPUT_TYPE = InputType()
