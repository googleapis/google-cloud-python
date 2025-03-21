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

import abc
import dataclasses
from typing import Callable

import bigframes.dtypes
from bigframes.dtypes import ExpressionType


@dataclasses.dataclass
class TypeSignature(abc.ABC):
    """
    Type Signature represent a mapping from input types to output type.

    Type signatures should throw a TypeError if the input types cannot be handled by the operation.
    """

    @property
    @abc.abstractmethod
    def as_method(self):
        """Convert the signature into an object method. Convenience function for constructing ops that use the signature."""
        ...


class UnaryTypeSignature(TypeSignature):
    @abc.abstractmethod
    def output_type(self, input_type: ExpressionType) -> ExpressionType:
        ...

    @property
    def as_method(self):
        def meth(_, *input_types: ExpressionType) -> ExpressionType:
            assert len(input_types) == 1
            return self.output_type(input_types[0])

        return meth


class BinaryTypeSignature(TypeSignature):
    @abc.abstractmethod
    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        ...

    @property
    def as_method(self):
        def meth(_, *input_types: ExpressionType) -> ExpressionType:
            assert len(input_types) == 2
            return self.output_type(input_types[0], input_types[1])

        return meth


@dataclasses.dataclass
class TypePreserving(UnaryTypeSignature):
    type_predicate: Callable[[ExpressionType], bool]
    description: str

    def output_type(self, input_type: ExpressionType) -> ExpressionType:
        if not self.type_predicate(input_type):
            raise TypeError(
                f"Type {input_type} is not supported. Type must be {self.description}"
            )
        return input_type


@dataclasses.dataclass
class FixedOutputType(UnaryTypeSignature):
    type_predicate: Callable[[ExpressionType], bool]
    fixed_type: ExpressionType
    description: str

    def output_type(self, input_type: ExpressionType) -> ExpressionType:
        if (input_type is not None) and not self.type_predicate(input_type):
            raise TypeError(
                f"Type {input_type} is not supported. Type must be {self.description}"
            )
        return self.fixed_type


@dataclasses.dataclass
class UnaryRealNumeric(UnaryTypeSignature):
    """Type signature for real-valued functions like exp, log, sin, tan."""

    def output_type(self, type: ExpressionType) -> ExpressionType:
        if type is None:
            return bigframes.dtypes.FLOAT_DTYPE
        if not bigframes.dtypes.is_numeric(type):
            raise TypeError(f"Type {type} is not numeric")
        if type in (bigframes.dtypes.INT_DTYPE, bigframes.dtypes.BOOL_DTYPE):
            # Real numeric ops produce floats on int input
            return bigframes.dtypes.FLOAT_DTYPE
        return type


@dataclasses.dataclass
class BinaryNumeric(BinaryTypeSignature):
    """Type signature for numeric functions like multiply, modulo that can map ints to ints."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if (left_type is not None) and not bigframes.dtypes.is_numeric(left_type):
            raise TypeError(f"Type {left_type} is not numeric")
        if (right_type is not None) and not bigframes.dtypes.is_numeric(right_type):
            raise TypeError(f"Type {right_type} is not numeric")
        return bigframes.dtypes.coerce_to_common(left_type, right_type)


@dataclasses.dataclass
@dataclasses.dataclass
class BinaryGeo(BinaryTypeSignature):
    """Type signature for geo functions like difference that can map geo to geo."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if (left_type is not None) and not bigframes.dtypes.is_geo_like(left_type):
            raise TypeError(f"Type {left_type} is not geo")
        if (right_type is not None) and not bigframes.dtypes.is_geo_like(right_type):
            raise TypeError(f"Type {right_type} is not numeric")
        return bigframes.dtypes.GEO_DTYPE


class BinaryNumericGeo(BinaryTypeSignature):
    """Type signature for geo functions like from_xy that can map ints to ints."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if (left_type is not None) and not bigframes.dtypes.is_numeric(left_type):
            raise TypeError(f"Type {left_type} is not numeric")
        if (right_type is not None) and not bigframes.dtypes.is_numeric(right_type):
            raise TypeError(f"Type {right_type} is not numeric")
        return bigframes.dtypes.GEO_DTYPE


@dataclasses.dataclass
class BinaryRealNumeric(BinaryTypeSignature):
    """Type signature for real-valued functions like divide, arctan2, pow."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if (left_type is not None) and not bigframes.dtypes.is_numeric(left_type):
            raise TypeError(f"Type {left_type} is not numeric")
        if (right_type is not None) and not bigframes.dtypes.is_numeric(right_type):
            raise TypeError(f"Type {right_type} is not numeric")
        lcd_type = bigframes.dtypes.coerce_to_common(left_type, right_type)
        if lcd_type == bigframes.dtypes.INT_DTYPE:
            # Real numeric ops produce floats on int input
            return bigframes.dtypes.FLOAT_DTYPE
        return lcd_type


@dataclasses.dataclass
class CoerceCommon(BinaryTypeSignature):
    """Attempt to coerce inputs to a compatible type."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        try:
            return bigframes.dtypes.coerce_to_common(left_type, right_type)
        except TypeError:
            pass
        if bigframes.dtypes.can_coerce(left_type, right_type):
            return right_type
        if bigframes.dtypes.can_coerce(right_type, left_type):
            return left_type
        raise TypeError(f"Cannot coerce {left_type} and {right_type} to a common type.")


@dataclasses.dataclass
class Comparison(BinaryTypeSignature):
    """Type signature for comparison operators."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        common_type = CoerceCommon().output_type(left_type, right_type)
        if not bigframes.dtypes.is_comparable(common_type):
            raise TypeError(f"Types {left_type} and {right_type} are not comparable")
        return bigframes.dtypes.BOOL_DTYPE


@dataclasses.dataclass
class Logical(BinaryTypeSignature):
    """Type signature for logical operators like AND, OR and NOT."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if left_type is None or right_type is None:
            return bigframes.dtypes.BOOL_DTYPE
        if not bigframes.dtypes.is_binary_like(left_type):
            raise TypeError(f"Type {left_type} is not binary")
        if not bigframes.dtypes.is_binary_like(right_type):
            raise TypeError(f"Type {right_type} is not binary")
        if left_type != right_type:
            raise TypeError(
                "Bitwise operands {left_type} and {right_type} do not match"
            )
        return left_type


@dataclasses.dataclass
class VectorMetric(BinaryTypeSignature):
    """Type signature for logical operators like AND, OR and NOT."""

    def output_type(
        self, left_type: ExpressionType, right_type: ExpressionType
    ) -> ExpressionType:
        if not bigframes.dtypes.is_array_like(left_type):
            raise TypeError(f"Type {left_type} is not array-like")
        if not bigframes.dtypes.is_array_like(right_type):
            raise TypeError(f"Type {right_type} is not array-like")
        if left_type != right_type:
            raise TypeError(
                "Vector op operands {left_type} and {right_type} do not match"
            )
        return bigframes.dtypes.FLOAT_DTYPE


# Common type signatures
UNARY_NUMERIC = TypePreserving(bigframes.dtypes.is_numeric, description="numeric")
UNARY_NUMERIC_AND_TIMEDELTA = TypePreserving(
    lambda x: bigframes.dtypes.is_numeric(x) or x is bigframes.dtypes.TIMEDELTA_DTYPE,
    description="numeric_and_timedelta",
)
UNARY_REAL_NUMERIC = UnaryRealNumeric()
BINARY_NUMERIC = BinaryNumeric()
BINARY_REAL_NUMERIC = BinaryRealNumeric()
BLOB_TRANSFORM = TypePreserving(bigframes.dtypes.is_struct_like, description="blob")
COMPARISON = Comparison()
COERCE = CoerceCommon()
LOGICAL = Logical()
STRING_TRANSFORM = TypePreserving(
    bigframes.dtypes.is_string_like, description="numeric"
)
STRING_PREDICATE = FixedOutputType(
    bigframes.dtypes.is_string_like,
    bigframes.dtypes.BOOL_DTYPE,
    description="string-like",
)
DATELIKE_ACCESSOR = FixedOutputType(
    bigframes.dtypes.is_date_like, bigframes.dtypes.INT_DTYPE, description="date-like"
)
TIMELIKE_ACCESSOR = FixedOutputType(
    bigframes.dtypes.is_time_like, bigframes.dtypes.INT_DTYPE, description="time-like"
)
VECTOR_METRIC = VectorMetric()
