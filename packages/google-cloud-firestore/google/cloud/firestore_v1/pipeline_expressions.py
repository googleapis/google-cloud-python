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
"""
.. warning::
    **Preview API**: Firestore Pipelines is currently in preview and is
    subject to potential breaking changes in future releases.
"""

from __future__ import annotations
from typing import (
    Any,
    Generic,
    TypeVar,
    Sequence,
)
from abc import ABC
from abc import abstractmethod
from enum import Enum
import datetime
from google.cloud.firestore_v1.types.document import Value
from google.cloud.firestore_v1.types.query import StructuredQuery as Query_pb
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1._helpers import GeoPoint
from google.cloud.firestore_v1._helpers import encode_value
from google.cloud.firestore_v1._helpers import decode_value

CONSTANT_TYPE = TypeVar(
    "CONSTANT_TYPE",
    str,
    int,
    float,
    bool,
    datetime.datetime,
    bytes,
    GeoPoint,
    Vector,
    None,
)


class Ordering:
    """Represents the direction for sorting results in a pipeline."""

    class Direction(Enum):
        ASCENDING = "ascending"
        DESCENDING = "descending"

    def __init__(self, expr, order_dir: Direction | str = Direction.ASCENDING):
        """
        Initializes an Ordering instance

        Args:
            expr (Expression | str): The expression or field path string to sort by.
                If a string is provided, it's treated as a field path.
            order_dir (Direction | str): The direction to sort in.
                Defaults to ascending
        """
        self.expr = expr if isinstance(expr, Expression) else Field.of(expr)
        self.order_dir = (
            Ordering.Direction[order_dir.upper()]
            if isinstance(order_dir, str)
            else order_dir
        )

    def __repr__(self):
        if self.order_dir is Ordering.Direction.ASCENDING:
            order_str = ".ascending()"
        else:
            order_str = ".descending()"
        return f"{self.expr!r}{order_str}"

    def _to_pb(self) -> Value:
        return Value(
            map_value={
                "fields": {
                    "direction": Value(string_value=self.order_dir.value),
                    "expression": self.expr._to_pb(),
                }
            }
        )


class Expression(ABC):
    """Represents an expression that can be evaluated to a value within the
    execution of a pipeline.

    Expressionessions are the building blocks for creating complex queries and
    transformations in Firestore pipelines. They can represent:

    - **Field references:** Access values from document fields.
    - **Literals:** Represent constant values (strings, numbers, booleans).
    - **FunctionExpression calls:** Apply functions to one or more expressions.
    - **Aggregations:** Calculate aggregate values (e.g., sum, average) over a set of documents.

    The `Expression` class provides a fluent API for building expressions. You can chain
    together method calls to create complex expressions.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def _to_pb(self) -> Value:
        raise NotImplementedError

    @staticmethod
    def _cast_to_expr_or_convert_to_constant(
        o: Any, include_vector=False
    ) -> "Expression":
        """Convert arbitrary object to an Expression."""
        if isinstance(o, Expression):
            return o
        if isinstance(o, dict):
            return Map(o)
        if isinstance(o, list):
            if include_vector and all([isinstance(i, (float, int)) for i in o]):
                return Constant(Vector(o))
            else:
                return Array(o)
        return Constant(o)

    class expose_as_static:
        """
        Decorator to mark instance methods to be exposed as static methods as well as instance
        methods.

        When called statically, the first argument is converted to a Field expression if needed.

        Example:
            >>> Field.of("test").add(5)
            >>> FunctionExpression.add("test", 5)
        """

        def __init__(self, instance_func):
            self.instance_func = instance_func

        def static_func(self, first_arg, *other_args, **kwargs):
            if not isinstance(first_arg, (Expression, str)):
                raise TypeError(
                    f"'{self.instance_func.__name__}' must be called on an Expression or a string representing a field. got {type(first_arg)}."
                )
            first_expr = (
                Field.of(first_arg)
                if not isinstance(first_arg, Expression)
                else first_arg
            )
            return self.instance_func(first_expr, *other_args, **kwargs)

        def __get__(self, instance, owner):
            if instance is None:
                return self.static_func
            else:
                return self.instance_func.__get__(instance, owner)

    @expose_as_static
    def add(self, other: Expression | float) -> "Expression":
        """Creates an expression that adds this expression to another expression or constant.

        Example:
            >>> # Add the value of the 'quantity' field and the 'reserve' field.
            >>> Field.of("quantity").add(Field.of("reserve"))
            >>> # Add 5 to the value of the 'age' field
            >>> Field.of("age").add(5)

        Args:
            other: The expression or constant value to add to this expression.

        Returns:
            A new `Expression` representing the addition operation.
        """
        return FunctionExpression(
            "add", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def subtract(self, other: Expression | float) -> "Expression":
        """Creates an expression that subtracts another expression or constant from this expression.

        Example:
            >>> # Subtract the 'discount' field from the 'price' field
            >>> Field.of("price").subtract(Field.of("discount"))
            >>> # Subtract 20 from the value of the 'total' field
            >>> Field.of("total").subtract(20)

        Args:
            other: The expression or constant value to subtract from this expression.

        Returns:
            A new `Expression` representing the subtraction operation.
        """
        return FunctionExpression(
            "subtract", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def multiply(self, other: Expression | float) -> "Expression":
        """Creates an expression that multiplies this expression by another expression or constant.

        Example:
            >>> # Multiply the 'quantity' field by the 'price' field
            >>> Field.of("quantity").multiply(Field.of("price"))
            >>> # Multiply the 'value' field by 2
            >>> Field.of("value").multiply(2)

        Args:
            other: The expression or constant value to multiply by.

        Returns:
            A new `Expression` representing the multiplication operation.
        """
        return FunctionExpression(
            "multiply", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def divide(self, other: Expression | float) -> "Expression":
        """Creates an expression that divides this expression by another expression or constant.

        Example:
            >>> # Divide the 'total' field by the 'count' field
            >>> Field.of("total").divide(Field.of("count"))
            >>> # Divide the 'value' field by 10
            >>> Field.of("value").divide(10)

        Args:
            other: The expression or constant value to divide by.

        Returns:
            A new `Expression` representing the division operation.
        """
        return FunctionExpression(
            "divide", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def mod(self, other: Expression | float) -> "Expression":
        """Creates an expression that calculates the modulo (remainder) to another expression or constant.

        Example:
            >>> # Calculate the remainder of dividing the 'value' field by field 'divisor'.
            >>> Field.of("value").mod(Field.of("divisor"))
            >>> # Calculate the remainder of dividing the 'value' field by 5.
            >>> Field.of("value").mod(5)

        Args:
            other: The divisor expression or constant.

        Returns:
            A new `Expression` representing the modulo operation.
        """
        return FunctionExpression(
            "mod", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def abs(self) -> "Expression":
        """Creates an expression that calculates the absolute value of this expression.

        Example:
            >>> # Get the absolute value of the 'change' field.
            >>> Field.of("change").abs()

        Returns:
            A new `Expression` representing the absolute value.
        """
        return FunctionExpression("abs", [self])

    @expose_as_static
    def ceil(self) -> "Expression":
        """Creates an expression that calculates the ceiling of this expression.

        Example:
            >>> # Get the ceiling of the 'value' field.
            >>> Field.of("value").ceil()

        Returns:
            A new `Expression` representing the ceiling value.
        """
        return FunctionExpression("ceil", [self])

    @expose_as_static
    def exp(self) -> "Expression":
        """Creates an expression that computes e to the power of this expression.

        Example:
            >>> # Compute e to the power of the 'value' field
            >>> Field.of("value").exp()

        Returns:
            A new `Expression` representing the exponential value.
        """
        return FunctionExpression("exp", [self])

    @expose_as_static
    def floor(self) -> "Expression":
        """Creates an expression that calculates the floor of this expression.

        Example:
            >>> # Get the floor of the 'value' field.
            >>> Field.of("value").floor()

        Returns:
            A new `Expression` representing the floor value.
        """
        return FunctionExpression("floor", [self])

    @expose_as_static
    def ln(self) -> "Expression":
        """Creates an expression that calculates the natural logarithm of this expression.

        Example:
            >>> # Get the natural logarithm of the 'value' field.
            >>> Field.of("value").ln()

        Returns:
            A new `Expression` representing the natural logarithm.
        """
        return FunctionExpression("ln", [self])

    @expose_as_static
    def log(self, base: Expression | float) -> "Expression":
        """Creates an expression that calculates the logarithm of this expression with a given base.

        Example:
            >>> # Get the logarithm of 'value' with base 2.
            >>> Field.of("value").log(2)
            >>> # Get the logarithm of 'value' with base from 'base_field'.
            >>> Field.of("value").log(Field.of("base_field"))

        Args:
            base: The base of the logarithm.

        Returns:
            A new `Expression` representing the logarithm.
        """
        return FunctionExpression(
            "log", [self, self._cast_to_expr_or_convert_to_constant(base)]
        )

    @expose_as_static
    def log10(self) -> "Expression":
        """Creates an expression that calculates the base 10 logarithm of this expression.

        Example:
            >>> Field.of("value").log10()

        Returns:
            A new `Expression` representing the logarithm.
        """
        return FunctionExpression("log10", [self])

    @expose_as_static
    def pow(self, exponent: Expression | float) -> "Expression":
        """Creates an expression that calculates this expression raised to the power of the exponent.

        Example:
            >>> # Raise 'base_val' to the power of 2.
            >>> Field.of("base_val").pow(2)
            >>> # Raise 'base_val' to the power of 'exponent_val'.
            >>> Field.of("base_val").pow(Field.of("exponent_val"))

        Args:
            exponent: The exponent.

        Returns:
            A new `Expression` representing the power operation.
        """
        return FunctionExpression(
            "pow", [self, self._cast_to_expr_or_convert_to_constant(exponent)]
        )

    @expose_as_static
    def round(self) -> "Expression":
        """Creates an expression that rounds this expression to the nearest integer.

        Example:
            >>> # Round the 'value' field.
            >>> Field.of("value").round()

        Returns:
            A new `Expression` representing the rounded value.
        """
        return FunctionExpression("round", [self])

    @expose_as_static
    def sqrt(self) -> "Expression":
        """Creates an expression that calculates the square root of this expression.

        Example:
            >>> # Get the square root of the 'area' field.
            >>> Field.of("area").sqrt()

        Returns:
            A new `Expression` representing the square root.
        """
        return FunctionExpression("sqrt", [self])

    @expose_as_static
    def logical_maximum(self, *others: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that returns the larger value between this expression
        and another expression or constant, based on Firestore's value type ordering.

        Firestore's value type ordering is described here:
        https://cloud.google.com/firestore/docs/concepts/data-types#value_type_ordering

        Example:
            >>> # Returns the larger value between the 'discount' field and the 'cap' field.
            >>> Field.of("discount").logical_maximum(Field.of("cap"))
            >>> # Returns the larger value between the 'value' field and some ints
            >>> Field.of("value").logical_maximum(10, 20, 30)

        Args:
            others: The other expression or constant values to compare with.

        Returns:
            A new `Expression` representing the logical maximum operation.
        """
        return FunctionExpression(
            "maximum",
            [self] + [self._cast_to_expr_or_convert_to_constant(o) for o in others],
            infix_name_override="logical_maximum",
        )

    @expose_as_static
    def logical_minimum(self, *others: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that returns the smaller value between this expression
        and another expression or constant, based on Firestore's value type ordering.

        Firestore's value type ordering is described here:
        https://cloud.google.com/firestore/docs/concepts/data-types#value_type_ordering

        Example:
            >>> # Returns the smaller value between the 'discount' field and the 'floor' field.
            >>> Field.of("discount").logical_minimum(Field.of("floor"))
            >>> # Returns the smaller value between the 'value' field and some ints
            >>> Field.of("value").logical_minimum(10, 20, 30)

        Args:
            others: The other expression or constant values to compare with.

        Returns:
            A new `Expression` representing the logical minimum operation.
        """
        return FunctionExpression(
            "minimum",
            [self] + [self._cast_to_expr_or_convert_to_constant(o) for o in others],
            infix_name_override="logical_minimum",
        )

    @expose_as_static
    def equal(self, other: Expression | CONSTANT_TYPE) -> "BooleanExpression":
        """Creates an expression that checks if this expression is equal to another
        expression or constant value.

        Example:
            >>> # Check if the 'age' field is equal to 21
            >>> Field.of("age").equal(21)
            >>> # Check if the 'city' field is equal to "London"
            >>> Field.of("city").equal("London")

        Args:
            other: The expression or constant value to compare for equality.

        Returns:
            A new `Expression` representing the equality comparison.
        """
        return BooleanExpression(
            "equal", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def not_equal(self, other: Expression | CONSTANT_TYPE) -> "BooleanExpression":
        """Creates an expression that checks if this expression is not equal to another
        expression or constant value.

        Example:
            >>> # Check if the 'status' field is not equal to "completed"
            >>> Field.of("status").not_equal("completed")
            >>> # Check if the 'country' field is not equal to "USA"
            >>> Field.of("country").not_equal("USA")

        Args:
            other: The expression or constant value to compare for inequality.

        Returns:
            A new `Expression` representing the inequality comparison.
        """
        return BooleanExpression(
            "not_equal", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def greater_than(self, other: Expression | CONSTANT_TYPE) -> "BooleanExpression":
        """Creates an expression that checks if this expression is greater than another
        expression or constant value.

        Example:
            >>> # Check if the 'age' field is greater than the 'limit' field
            >>> Field.of("age").greater_than(Field.of("limit"))
            >>> # Check if the 'price' field is greater than 100
            >>> Field.of("price").greater_than(100)

        Args:
            other: The expression or constant value to compare for greater than.

        Returns:
            A new `Expression` representing the greater than comparison.
        """
        return BooleanExpression(
            "greater_than", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def greater_than_or_equal(
        self, other: Expression | CONSTANT_TYPE
    ) -> "BooleanExpression":
        """Creates an expression that checks if this expression is greater than or equal
        to another expression or constant value.

        Example:
            >>> # Check if the 'quantity' field is greater than or equal to field 'requirement' plus 1
            >>> Field.of("quantity").greater_than_or_equal(Field.of('requirement').add(1))
            >>> # Check if the 'score' field is greater than or equal to 80
            >>> Field.of("score").greater_than_or_equal(80)

        Args:
            other: The expression or constant value to compare for greater than or equal to.

        Returns:
            A new `Expression` representing the greater than or equal to comparison.
        """
        return BooleanExpression(
            "greater_than_or_equal",
            [self, self._cast_to_expr_or_convert_to_constant(other)],
        )

    @expose_as_static
    def less_than(self, other: Expression | CONSTANT_TYPE) -> "BooleanExpression":
        """Creates an expression that checks if this expression is less than another
        expression or constant value.

        Example:
            >>> # Check if the 'age' field is less than 'limit'
            >>> Field.of("age").less_than(Field.of('limit'))
            >>> # Check if the 'price' field is less than 50
            >>> Field.of("price").less_than(50)

        Args:
            other: The expression or constant value to compare for less than.

        Returns:
            A new `Expression` representing the less than comparison.
        """
        return BooleanExpression(
            "less_than", [self, self._cast_to_expr_or_convert_to_constant(other)]
        )

    @expose_as_static
    def less_than_or_equal(
        self, other: Expression | CONSTANT_TYPE
    ) -> "BooleanExpression":
        """Creates an expression that checks if this expression is less than or equal to
        another expression or constant value.

        Example:
            >>> # Check if the 'quantity' field is less than or equal to 20
            >>> Field.of("quantity").less_than_or_equal(Constant.of(20))
            >>> # Check if the 'score' field is less than or equal to 70
            >>> Field.of("score").less_than_or_equal(70)

        Args:
            other: The expression or constant value to compare for less than or equal to.

        Returns:
            A new `Expression` representing the less than or equal to comparison.
        """
        return BooleanExpression(
            "less_than_or_equal",
            [self, self._cast_to_expr_or_convert_to_constant(other)],
        )

    @expose_as_static
    def equal_any(
        self, array: Array | Sequence[Expression | CONSTANT_TYPE] | Expression
    ) -> "BooleanExpression":
        """Creates an expression that checks if this expression is equal to any of the
        provided values or expressions.

        Example:
            >>> # Check if the 'category' field is either "Electronics" or value of field 'primaryType'
            >>> Field.of("category").equal_any(["Electronics", Field.of("primaryType")])

        Args:
            array: The values or expressions to check against.

        Returns:
            A new `Expression` representing the 'IN' comparison.
        """
        return BooleanExpression(
            "equal_any",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(array),
            ],
        )

    @expose_as_static
    def not_equal_any(
        self, array: Array | list[Expression | CONSTANT_TYPE] | Expression
    ) -> "BooleanExpression":
        """Creates an expression that checks if this expression is not equal to any of the
        provided values or expressions.

        Example:
            >>> # Check if the 'status' field is neither "pending" nor "cancelled"
            >>> Field.of("status").not_equal_any(["pending", "cancelled"])

        Args:
            array: The values or expressions to check against.

        Returns:
            A new `Expression` representing the 'NOT IN' comparison.
        """
        return BooleanExpression(
            "not_equal_any",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(array),
            ],
        )

    @expose_as_static
    def array_get(self, offset: Expression | int) -> "FunctionExpression":
        """
        Creates an expression that indexes into an array from the beginning or end and returns the
        element. A negative offset starts from the end.

        Example:
            >>> Array([1,2,3]).array_get(0)

        Args:
            offset: the index of the element to return

        Returns:
            A new `Expression` representing the `array_get` operation.
        """
        return FunctionExpression(
            "array_get", [self, self._cast_to_expr_or_convert_to_constant(offset)]
        )

    @expose_as_static
    def array_contains(
        self, element: Expression | CONSTANT_TYPE
    ) -> "BooleanExpression":
        """Creates an expression that checks if an array contains a specific element or value.

        Example:
            >>> # Check if the 'sizes' array contains the value from the 'selectedSize' field
            >>> Field.of("sizes").array_contains(Field.of("selectedSize"))
            >>> # Check if the 'colors' array contains "red"
            >>> Field.of("colors").array_contains("red")

        Args:
            element: The element (expression or constant) to search for in the array.

        Returns:
            A new `Expression` representing the 'array_contains' comparison.
        """
        return BooleanExpression(
            "array_contains", [self, self._cast_to_expr_or_convert_to_constant(element)]
        )

    @expose_as_static
    def array_contains_all(
        self,
        elements: Array | list[Expression | CONSTANT_TYPE] | Expression,
    ) -> "BooleanExpression":
        """Creates an expression that checks if an array contains all the specified elements.

        Example:
            >>> # Check if the 'tags' array contains both "news" and "sports"
            >>> Field.of("tags").array_contains_all(["news", "sports"])
            >>> # Check if the 'tags' array contains both of the values from field 'tag1' and "tag2"
            >>> Field.of("tags").array_contains_all([Field.of("tag1"), "tag2"])

        Args:
            elements: The list of elements (expressions or constants) to check for in the array.

        Returns:
            A new `Expression` representing the 'array_contains_all' comparison.
        """
        return BooleanExpression(
            "array_contains_all",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(elements),
            ],
        )

    @expose_as_static
    def array_contains_any(
        self,
        elements: Array | list[Expression | CONSTANT_TYPE] | Expression,
    ) -> "BooleanExpression":
        """Creates an expression that checks if an array contains any of the specified elements.

        Example:
            >>> # Check if the 'categories' array contains either values from field "cate1" or "cate2"
            >>> Field.of("categories").array_contains_any([Field.of("cate1"), Field.of("cate2")])
            >>> # Check if the 'groups' array contains either the value from the 'userGroup' field
            >>> # or the value "guest"
            >>> Field.of("groups").array_contains_any([Field.of("userGroup"), "guest"])

        Args:
            elements: The list of elements (expressions or constants) to check for in the array.

        Returns:
            A new `Expression` representing the 'array_contains_any' comparison.
        """
        return BooleanExpression(
            "array_contains_any",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(elements),
            ],
        )

    @expose_as_static
    def array_length(self) -> "Expression":
        """Creates an expression that calculates the length of an array.

        Example:
            >>> # Get the number of items in the 'cart' array
            >>> Field.of("cart").array_length()

        Returns:
            A new `Expression` representing the length of the array.
        """
        return FunctionExpression("array_length", [self])

    @expose_as_static
    def array_reverse(self) -> "Expression":
        """Creates an expression that returns the reversed content of an array.

        Example:
            >>> # Get the 'preferences' array in reversed order.
            >>> Field.of("preferences").array_reverse()

        Returns:
            A new `Expression` representing the reversed array.
        """
        return FunctionExpression("array_reverse", [self])

    @expose_as_static
    def array_concat(
        self, *other_arrays: Array | list[Expression | CONSTANT_TYPE] | Expression
    ) -> "Expression":
        """Creates an expression that concatenates an array expression with another array.

        Example:
            >>> # Combine the 'tags' array with a new array and an array field
            >>> Field.of("tags").array_concat(["newTag1", "newTag2", Field.of("otherTag")])

        Args:
            array: The list of constants or expressions to concat with.

        Returns:
            A new `Expression` representing the concatenated array.
        """
        return FunctionExpression(
            "array_concat",
            [self]
            + [self._cast_to_expr_or_convert_to_constant(arr) for arr in other_arrays],
        )

    @expose_as_static
    def concat(self, *others: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that concatenates expressions together

        Args:
            *others: The expressions to concatenate.

        Returns:
            A new `Expression` representing the concatenated value.
        """
        return FunctionExpression(
            "concat",
            [self] + [self._cast_to_expr_or_convert_to_constant(o) for o in others],
        )

    @expose_as_static
    def length(self) -> "Expression":
        """
        Creates an expression that calculates the length of the expression if it is a string, array, map, or blob.

        Example:
            >>> # Get the length of the 'name' field.
            >>> Field.of("name").length()

        Returns:
            A new `Expression` representing the length of the expression.
        """
        return FunctionExpression("length", [self])

    @expose_as_static
    def is_absent(self) -> "BooleanExpression":
        """Creates an expression that returns true if a value is absent. Otherwise, returns false even if
        the value is null.

        Example:
            >>> # Check if the 'email' field is absent.
            >>> Field.of("email").is_absent()

        Returns:
            A new `BooleanExpressionession` representing the isAbsent operation.
        """
        return BooleanExpression("is_absent", [self])

    @expose_as_static
    def if_absent(self, default_value: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that returns a default value if an expression evaluates to an absent value.

        Example:
            >>> # Return the value of the 'email' field, or "N/A" if it's absent.
            >>> Field.of("email").if_absent("N/A")

        Args:
            default_value: The expression or constant value to return if this expression is absent.

        Returns:
            A new `Expression` representing the ifAbsent operation.
        """
        return FunctionExpression(
            "if_absent",
            [self, self._cast_to_expr_or_convert_to_constant(default_value)],
        )

    @expose_as_static
    def is_error(self):
        """Creates an expression that checks if a given expression produces an error

        Example:
            >>> # Resolves to True if an expression produces an error
            >>> Field.of("value").divide("string").is_error()

        Returns:
            A new `Expression` representing the isError operation.
        """
        return FunctionExpression("is_error", [self])

    @expose_as_static
    def if_error(self, then_value: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that returns ``then_value`` if this expression evaluates to an error.
        Otherwise, returns the value of this expression.

        Example:
            >>> # Resolves to 0 if an expression produces an error
            >>> Field.of("value").divide("string").if_error(0)

        Args:
            then_value: The value to return if this expression evaluates to an error.

        Returns:
            A new `Expression` representing the ifError operation.
        """
        return FunctionExpression(
            "if_error", [self, self._cast_to_expr_or_convert_to_constant(then_value)]
        )

    @expose_as_static
    def exists(self) -> "BooleanExpression":
        """Creates an expression that checks if a field exists in the document.

        Example:
            >>> # Check if the document has a field named "phoneNumber"
            >>> Field.of("phoneNumber").exists()

        Returns:
            A new `Expression` representing the 'exists' check.
        """
        return BooleanExpression("exists", [self])

    @expose_as_static
    def sum(self) -> "Expression":
        """Creates an aggregation that calculates the sum of a numeric field across multiple stage inputs.

        Example:
            >>> # Calculate the total revenue from a set of orders
            >>> Field.of("orderAmount").sum().as_("totalRevenue")

        Returns:
            A new `AggregateFunction` representing the 'sum' aggregation.
        """
        return AggregateFunction("sum", [self])

    @expose_as_static
    def average(self) -> "Expression":
        """Creates an aggregation that calculates the average (mean) of a numeric field across multiple
        stage inputs.

        Example:
            >>> # Calculate the average age of users
            >>> Field.of("age").average().as_("averageAge")

        Returns:
            A new `AggregateFunction` representing the 'avg' aggregation.
        """
        return AggregateFunction("average", [self])

    @expose_as_static
    def count(self) -> "Expression":
        """Creates an aggregation that counts the number of stage inputs with valid evaluations of the
        expression or field.

        Example:
            >>> # Count the total number of products
            >>> Field.of("productId").count().as_("totalProducts")

        Returns:
            A new `AggregateFunction` representing the 'count' aggregation.
        """
        return AggregateFunction("count", [self])

    @expose_as_static
    def count_if(self) -> "Expression":
        """Creates an aggregation that counts the number of values of the provided field or expression
        that evaluate to True.

        Example:
            >>> # Count the number of adults
            >>> Field.of("age").greater_than(18).count_if().as_("totalAdults")


        Returns:
            A new `AggregateFunction` representing the 'count_if' aggregation.
        """
        return AggregateFunction("count_if", [self])

    @expose_as_static
    def count_distinct(self) -> "Expression":
        """Creates an aggregation that counts the number of distinct values of the
        provided field or expression.

        Example:
            >>> # Count the total number of countries in the data
            >>> Field.of("country").count_distinct().as_("totalCountries")

        Returns:
            A new `AggregateFunction` representing the 'count_distinct' aggregation.
        """
        return AggregateFunction("count_distinct", [self])

    @expose_as_static
    def minimum(self) -> "Expression":
        """Creates an aggregation that finds the minimum value of a field across multiple stage inputs.

        Example:
            >>> # Find the lowest price of all products
            >>> Field.of("price").minimum().as_("lowestPrice")

        Returns:
            A new `AggregateFunction` representing the 'minimum' aggregation.
        """
        return AggregateFunction("minimum", [self])

    @expose_as_static
    def maximum(self) -> "Expression":
        """Creates an aggregation that finds the maximum value of a field across multiple stage inputs.

        Example:
            >>> # Find the highest score in a leaderboard
            >>> Field.of("score").maximum().as_("highestScore")

        Returns:
            A new `AggregateFunction` representing the 'maximum' aggregation.
        """
        return AggregateFunction("maximum", [self])

    @expose_as_static
    def char_length(self) -> "Expression":
        """Creates an expression that calculates the character length of a string.

        Example:
            >>> # Get the character length of the 'name' field
            >>> Field.of("name").char_length()

        Returns:
            A new `Expression` representing the length of the string.
        """
        return FunctionExpression("char_length", [self])

    @expose_as_static
    def byte_length(self) -> "Expression":
        """Creates an expression that calculates the byte length of a string in its UTF-8 form.

        Example:
            >>> # Get the byte length of the 'name' field
            >>> Field.of("name").byte_length()

        Returns:
            A new `Expression` representing the byte length of the string.
        """
        return FunctionExpression("byte_length", [self])

    @expose_as_static
    def like(self, pattern: Expression | str) -> "BooleanExpression":
        """Creates an expression that performs a case-sensitive string comparison.

        Example:
            >>> # Check if the 'title' field contains the word "guide" (case-sensitive)
            >>> Field.of("title").like("%guide%")
            >>> # Check if the 'title' field matches the pattern specified in field 'pattern'.
            >>> Field.of("title").like(Field.of("pattern"))

        Args:
            pattern: The pattern (string or expression) to search for. You can use "%" as a wildcard character.

        Returns:
            A new `Expression` representing the 'like' comparison.
        """
        return BooleanExpression(
            "like", [self, self._cast_to_expr_or_convert_to_constant(pattern)]
        )

    @expose_as_static
    def regex_contains(self, regex: Expression | str) -> "BooleanExpression":
        """Creates an expression that checks if a string contains a specified regular expression as a
        substring.

        Example:
            >>> # Check if the 'description' field contains "example" (case-insensitive)
            >>> Field.of("description").regex_contains("(?i)example")
            >>> # Check if the 'description' field contains the regular expression stored in field 'regex'
            >>> Field.of("description").regex_contains(Field.of("regex"))

        Args:
            regex: The regular expression (string or expression) to use for the search.

        Returns:
            A new `Expression` representing the 'contains' comparison.
        """
        return BooleanExpression(
            "regex_contains", [self, self._cast_to_expr_or_convert_to_constant(regex)]
        )

    @expose_as_static
    def regex_match(self, regex: Expression | str) -> "BooleanExpression":
        """Creates an expression that checks if a string matches a specified regular expression.

        Example:
            >>> # Check if the 'email' field matches a valid email pattern
            >>> Field.of("email").regex_match("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
            >>> # Check if the 'email' field matches a regular expression stored in field 'regex'
            >>> Field.of("email").regex_match(Field.of("regex"))

        Args:
            regex: The regular expression (string or expression) to use for the match.

        Returns:
            A new `Expression` representing the regular expression match.
        """
        return BooleanExpression(
            "regex_match", [self, self._cast_to_expr_or_convert_to_constant(regex)]
        )

    @expose_as_static
    def string_contains(self, substring: Expression | str) -> "BooleanExpression":
        """Creates an expression that checks if this string expression contains a specified substring.

        Example:
            >>> # Check if the 'description' field contains "example".
            >>> Field.of("description").string_contains("example")
            >>> # Check if the 'description' field contains the value of the 'keyword' field.
            >>> Field.of("description").string_contains(Field.of("keyword"))

        Args:
            substring: The substring (string or expression) to use for the search.

        Returns:
            A new `Expression` representing the 'contains' comparison.
        """
        return BooleanExpression(
            "string_contains",
            [self, self._cast_to_expr_or_convert_to_constant(substring)],
        )

    @expose_as_static
    def starts_with(self, prefix: Expression | str) -> "BooleanExpression":
        """Creates an expression that checks if a string starts with a given prefix.

        Example:
            >>> # Check if the 'name' field starts with "Mr."
            >>> Field.of("name").starts_with("Mr.")
            >>> # Check if the 'fullName' field starts with the value of the 'firstName' field
            >>> Field.of("fullName").starts_with(Field.of("firstName"))

        Args:
            prefix: The prefix (string or expression) to check for.

        Returns:
            A new `Expression` representing the 'starts with' comparison.
        """
        return BooleanExpression(
            "starts_with", [self, self._cast_to_expr_or_convert_to_constant(prefix)]
        )

    @expose_as_static
    def ends_with(self, postfix: Expression | str) -> "BooleanExpression":
        """Creates an expression that checks if a string ends with a given postfix.

        Example:
            >>> # Check if the 'filename' field ends with ".txt"
            >>> Field.of("filename").ends_with(".txt")
            >>> # Check if the 'url' field ends with the value of the 'extension' field
            >>> Field.of("url").ends_with(Field.of("extension"))

        Args:
            postfix: The postfix (string or expression) to check for.

        Returns:
            A new `Expression` representing the 'ends with' comparison.
        """
        return BooleanExpression(
            "ends_with", [self, self._cast_to_expr_or_convert_to_constant(postfix)]
        )

    @expose_as_static
    def string_concat(self, *elements: Expression | CONSTANT_TYPE) -> "Expression":
        """Creates an expression that concatenates string expressions, fields or constants together.

        Example:
            >>> # Combine the 'firstName', " ", and 'lastName' fields into a single string
            >>> Field.of("firstName").string_concat(" ", Field.of("lastName"))

        Args:
            *elements: The expressions or constants (typically strings) to concatenate.

        Returns:
            A new `Expression` representing the concatenated string.
        """
        return FunctionExpression(
            "string_concat",
            [self] + [self._cast_to_expr_or_convert_to_constant(el) for el in elements],
        )

    @expose_as_static
    def to_lower(self) -> "Expression":
        """Creates an expression that converts a string to lowercase.

        Example:
            >>> # Convert the 'name' field to lowercase
            >>> Field.of("name").to_lower()

        Returns:
            A new `Expression` representing the lowercase string.
        """
        return FunctionExpression("to_lower", [self])

    @expose_as_static
    def to_upper(self) -> "Expression":
        """Creates an expression that converts a string to uppercase.

        Example:
            >>> # Convert the 'title' field to uppercase
            >>> Field.of("title").to_upper()

        Returns:
            A new `Expression` representing the uppercase string.
        """
        return FunctionExpression("to_upper", [self])

    @expose_as_static
    def trim(self) -> "Expression":
        """Creates an expression that removes leading and trailing whitespace from a string.

        Example:
            >>> # Trim whitespace from the 'userInput' field
            >>> Field.of("userInput").trim()

        Returns:
            A new `Expression` representing the trimmed string.
        """
        return FunctionExpression("trim", [self])

    @expose_as_static
    def string_reverse(self) -> "Expression":
        """Creates an expression that reverses a string.

        Example:
            >>> # Reverse the 'userInput' field
            >>> Field.of("userInput").reverse()

        Returns:
            A new `Expression` representing the reversed string.
        """
        return FunctionExpression("string_reverse", [self])

    @expose_as_static
    def substring(
        self, position: Expression | int, length: Expression | int | None = None
    ) -> "Expression":
        """Creates an expression that returns a substring of the results of this expression.


        Example:
            >>> Field.of("description").substring(5, 10)
            >>> Field.of("description").substring(5)

        Args:
            position: the index of the first character of the substring.
            length: the length of the substring. If not provided the substring
                will end at the end of the input.

        Returns:
            A new `Expression` representing the extracted substring.
        """
        args = [self, self._cast_to_expr_or_convert_to_constant(position)]
        if length is not None:
            args.append(self._cast_to_expr_or_convert_to_constant(length))
        return FunctionExpression("substring", args)

    @expose_as_static
    def join(self, delimeter: Expression | str) -> "Expression":
        """Creates an expression that joins the elements of an array into a string


        Example:
            >>> Field.of("tags").join(", ")

        Args:
            delimiter: The delimiter to add between the elements of the array.

        Returns:
            A new `Expression` representing the joined string.
        """
        return FunctionExpression(
            "join", [self, self._cast_to_expr_or_convert_to_constant(delimeter)]
        )

    @expose_as_static
    def map_get(self, key: str | Constant[str]) -> "Expression":
        """Accesses a value from the map produced by evaluating this expression.

        Example:
            >>> Map({"city": "London"}).map_get("city")
            >>> Field.of("address").map_get("city")

        Args:
            key: The key to access in the map.

        Returns:
            A new `Expression` representing the value associated with the given key in the map.
        """
        return FunctionExpression(
            "map_get", [self, self._cast_to_expr_or_convert_to_constant(key)]
        )

    @expose_as_static
    def map_remove(self, key: str | Constant[str]) -> "Expression":
        """Remove a key from a the map produced by evaluating this expression.

        Example:
            >>> Map({"city": "London"}).map_remove("city")
            >>> Field.of("address").map_remove("city")

        Args:
            key: The key to remove in the map.

        Returns:
            A new `Expression` representing the map_remove operation.
        """
        return FunctionExpression(
            "map_remove", [self, self._cast_to_expr_or_convert_to_constant(key)]
        )

    @expose_as_static
    def map_merge(
        self,
        *other_maps: Map
        | dict[str | Constant[str], Expression | CONSTANT_TYPE]
        | Expression,
    ) -> "Expression":
        """Creates an expression that merges one or more dicts into a single map.

        Example:
            >>> Map({"city": "London"}).map_merge({"country": "UK"}, {"isCapital": True})
            >>> Field.of("settings").map_merge({"enabled":True}, FunctionExpression.conditional(Field.of('isAdmin'), {"admin":True}, {}})

        Args:
            *other_maps: Sequence of maps to merge into the resulting map.

        Returns:
            A new `Expression` representing the value associated with the given key in the map.
        """
        return FunctionExpression(
            "map_merge",
            [self] + [self._cast_to_expr_or_convert_to_constant(m) for m in other_maps],
        )

    @expose_as_static
    def cosine_distance(self, other: Expression | list[float] | Vector) -> "Expression":
        """Calculates the cosine distance between two vectors.

        Example:
            >>> # Calculate the cosine distance between the 'userVector' field and the 'itemVector' field
            >>> Field.of("userVector").cosine_distance(Field.of("itemVector"))
            >>> # Calculate the Cosine distance between the 'location' field and a target location
            >>> Field.of("location").cosine_distance([37.7749, -122.4194])

        Args:
            other: The other vector (represented as an Expression, list of floats, or Vector) to compare against.

        Returns:
            A new `Expression` representing the cosine distance between the two vectors.
        """
        return FunctionExpression(
            "cosine_distance",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(other, include_vector=True),
            ],
        )

    @expose_as_static
    def euclidean_distance(
        self, other: Expression | list[float] | Vector
    ) -> "Expression":
        """Calculates the Euclidean distance between two vectors.

        Example:
            >>> # Calculate the Euclidean distance between the 'location' field and a target location
            >>> Field.of("location").euclidean_distance([37.7749, -122.4194])
            >>> # Calculate the Euclidean distance between two vector fields: 'pointA' and 'pointB'
            >>> Field.of("pointA").euclidean_distance(Field.of("pointB"))

        Args:
            other: The other vector (represented as an Expression, list of floats, or Vector) to compare against.

        Returns:
            A new `Expression` representing the Euclidean distance between the two vectors.
        """
        return FunctionExpression(
            "euclidean_distance",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(other, include_vector=True),
            ],
        )

    @expose_as_static
    def dot_product(self, other: Expression | list[float] | Vector) -> "Expression":
        """Calculates the dot product between two vectors.

        Example:
            >>> # Calculate the dot product between a feature vector and a target vector
            >>> Field.of("features").dot_product([0.5, 0.8, 0.2])
            >>> # Calculate the dot product between two document vectors: 'docVector1' and 'docVector2'
            >>> Field.of("docVector1").dot_product(Field.of("docVector2"))

        Args:
            other: The other vector (represented as an Expression, list of floats, or Vector) to calculate dot product with.

        Returns:
            A new `Expression` representing the dot product between the two vectors.
        """
        return FunctionExpression(
            "dot_product",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(other, include_vector=True),
            ],
        )

    @expose_as_static
    def vector_length(self) -> "Expression":
        """Creates an expression that calculates the length (dimension) of a Firestore Vector.

        Example:
            >>> # Get the vector length (dimension) of the field 'embedding'.
            >>> Field.of("embedding").vector_length()

        Returns:
            A new `Expression` representing the length of the vector.
        """
        return FunctionExpression("vector_length", [self])

    @expose_as_static
    def timestamp_to_unix_micros(self) -> "Expression":
        """Creates an expression that converts a timestamp to the number of microseconds since the epoch
        (1970-01-01 00:00:00 UTC).

        Truncates higher levels of precision by rounding down to the beginning of the microsecond.

        Example:
            >>> # Convert the 'timestamp' field to microseconds since the epoch.
            >>> Field.of("timestamp").timestamp_to_unix_micros()

        Returns:
            A new `Expression` representing the number of microseconds since the epoch.
        """
        return FunctionExpression("timestamp_to_unix_micros", [self])

    @expose_as_static
    def unix_micros_to_timestamp(self) -> "Expression":
        """Creates an expression that converts a number of microseconds since the epoch (1970-01-01
        00:00:00 UTC) to a timestamp.

        Example:
            >>> # Convert the 'microseconds' field to a timestamp.
            >>> Field.of("microseconds").unix_micros_to_timestamp()

        Returns:
            A new `Expression` representing the timestamp.
        """
        return FunctionExpression("unix_micros_to_timestamp", [self])

    @expose_as_static
    def timestamp_to_unix_millis(self) -> "Expression":
        """Creates an expression that converts a timestamp to the number of milliseconds since the epoch
        (1970-01-01 00:00:00 UTC).

        Truncates higher levels of precision by rounding down to the beginning of the millisecond.

        Example:
            >>> # Convert the 'timestamp' field to milliseconds since the epoch.
            >>> Field.of("timestamp").timestamp_to_unix_millis()

        Returns:
            A new `Expression` representing the number of milliseconds since the epoch.
        """
        return FunctionExpression("timestamp_to_unix_millis", [self])

    @expose_as_static
    def unix_millis_to_timestamp(self) -> "Expression":
        """Creates an expression that converts a number of milliseconds since the epoch (1970-01-01
        00:00:00 UTC) to a timestamp.

        Example:
            >>> # Convert the 'milliseconds' field to a timestamp.
            >>> Field.of("milliseconds").unix_millis_to_timestamp()

        Returns:
            A new `Expression` representing the timestamp.
        """
        return FunctionExpression("unix_millis_to_timestamp", [self])

    @expose_as_static
    def timestamp_to_unix_seconds(self) -> "Expression":
        """Creates an expression that converts a timestamp to the number of seconds since the epoch
        (1970-01-01 00:00:00 UTC).

        Truncates higher levels of precision by rounding down to the beginning of the second.

        Example:
            >>> # Convert the 'timestamp' field to seconds since the epoch.
            >>> Field.of("timestamp").timestamp_to_unix_seconds()

        Returns:
            A new `Expression` representing the number of seconds since the epoch.
        """
        return FunctionExpression("timestamp_to_unix_seconds", [self])

    @expose_as_static
    def unix_seconds_to_timestamp(self) -> "Expression":
        """Creates an expression that converts a number of seconds since the epoch (1970-01-01 00:00:00
        UTC) to a timestamp.

        Example:
            >>> # Convert the 'seconds' field to a timestamp.
            >>> Field.of("seconds").unix_seconds_to_timestamp()

        Returns:
            A new `Expression` representing the timestamp.
        """
        return FunctionExpression("unix_seconds_to_timestamp", [self])

    @expose_as_static
    def timestamp_add(
        self, unit: Expression | str, amount: Expression | float
    ) -> "Expression":
        """Creates an expression that adds a specified amount of time to this timestamp expression.

        Example:
            >>> # Add a duration specified by the 'unit' and 'amount' fields to the 'timestamp' field.
            >>> Field.of("timestamp").timestamp_add(Field.of("unit"), Field.of("amount"))
            >>> # Add 1.5 days to the 'timestamp' field.
            >>> Field.of("timestamp").timestamp_add("day", 1.5)

        Args:
            unit: The expression or string evaluating to the unit of time to add, must be one of
                  'microsecond', 'millisecond', 'second', 'minute', 'hour', 'day'.
            amount: The expression or float representing the amount of time to add.

        Returns:
            A new `Expression` representing the resulting timestamp.
        """
        return FunctionExpression(
            "timestamp_add",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(unit),
                self._cast_to_expr_or_convert_to_constant(amount),
            ],
        )

    @expose_as_static
    def timestamp_subtract(
        self, unit: Expression | str, amount: Expression | float
    ) -> "Expression":
        """Creates an expression that subtracts a specified amount of time from this timestamp expression.

        Example:
            >>> # Subtract a duration specified by the 'unit' and 'amount' fields from the 'timestamp' field.
            >>> Field.of("timestamp").timestamp_subtract(Field.of("unit"), Field.of("amount"))
            >>> # Subtract 2.5 hours from the 'timestamp' field.
            >>> Field.of("timestamp").timestamp_subtract("hour", 2.5)

        Args:
            unit: The expression or string evaluating to the unit of time to subtract, must be one of
                  'microsecond', 'millisecond', 'second', 'minute', 'hour', 'day'.
            amount: The expression or float representing the amount of time to subtract.

        Returns:
            A new `Expression` representing the resulting timestamp.
        """
        return FunctionExpression(
            "timestamp_subtract",
            [
                self,
                self._cast_to_expr_or_convert_to_constant(unit),
                self._cast_to_expr_or_convert_to_constant(amount),
            ],
        )

    @expose_as_static
    def collection_id(self):
        """Creates an expression that returns the collection ID from a path.

        Example:
            >>> # Get the collection ID from a path.
            >>> Field.of("__name__").collection_id()

        Returns:
            A new `Expression` representing the collection ID.
        """
        return FunctionExpression("collection_id", [self])

    @expose_as_static
    def document_id(self):
        """Creates an expression that returns the document ID from a path.

        Example:
            >>> # Get the document ID from a path.
            >>> Field.of("__name__").document_id()

        Returns:
            A new `Expression` representing the document ID.
        """
        return FunctionExpression("document_id", [self])

    def ascending(self) -> Ordering:
        """Creates an `Ordering` that sorts documents in ascending order based on this expression.

        Example:
            >>> # Sort documents by the 'name' field in ascending order
            >>> client.pipeline().collection("users").sort(Field.of("name").ascending())

        Returns:
            A new `Ordering` for ascending sorting.
        """
        return Ordering(self, Ordering.Direction.ASCENDING)

    def descending(self) -> Ordering:
        """Creates an `Ordering` that sorts documents in descending order based on this expression.

        Example:
            >>> # Sort documents by the 'createdAt' field in descending order
            >>> client.pipeline().collection("users").sort(Field.of("createdAt").descending())

        Returns:
            A new `Ordering` for descending sorting.
        """
        return Ordering(self, Ordering.Direction.DESCENDING)

    def as_(self, alias: str) -> "AliasedExpression":
        """Assigns an alias to this expression.

        Aliases are useful for renaming fields in the output of a stage or for giving meaningful
        names to calculated values.

        Example:
            >>> # Calculate the total price and assign it the alias "totalPrice" and add it to the output.
            >>> client.pipeline().collection("items").add_fields(
            ...     Field.of("price").multiply(Field.of("quantity")).as_("totalPrice")
            ... )

        Args:
            alias: The alias to assign to this expression.

        Returns:
            A new `Selectable` (typically an `AliasedExpression`) that wraps this
            expression and associates it with the provided alias.
        """
        return AliasedExpression(self, alias)


class Constant(Expression, Generic[CONSTANT_TYPE]):
    """Represents a constant literal value in an expression."""

    def __init__(self, value: CONSTANT_TYPE):
        self.value: CONSTANT_TYPE = value

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return other == self.value
        else:
            return other.value == self.value

    @staticmethod
    def of(value: CONSTANT_TYPE) -> Constant[CONSTANT_TYPE]:
        """Creates a constant expression from a Python value."""
        return Constant(value)

    def __repr__(self):
        value_str = repr(self.value)
        if isinstance(self.value, float) and value_str == "nan":
            value_str = "math.nan"
        return f"Constant.of({value_str})"

    def __hash__(self):
        return hash(self.value)

    def _to_pb(self) -> Value:
        return encode_value(self.value)


class FunctionExpression(Expression):
    """A base class for expressions that represent function calls."""

    def __init__(
        self,
        name: str,
        params: Sequence[Expression],
        *,
        use_infix_repr: bool = True,
        infix_name_override: str | None = None,
    ):
        self.name = name
        self.params = list(params)
        self._use_infix_repr = use_infix_repr
        self._infix_name_override = infix_name_override

    def __repr__(self):
        """
        Most FunctionExpressions can be triggered infix. Eg: Field.of('age').greater_than(18).

        Display them this way in the repr string where possible
        """
        if self._use_infix_repr:
            infix_name = self._infix_name_override or self.name
            if len(self.params) == 1:
                return f"{self.params[0]!r}.{infix_name}()"
            elif len(self.params) == 2:
                return f"{self.params[0]!r}.{infix_name}({self.params[1]!r})"
            else:
                return f"{self.params[0]!r}.{infix_name}({', '.join([repr(p) for p in self.params[1:]])})"
        return f"{self.__class__.__name__}({', '.join([repr(p) for p in self.params])})"

    def __eq__(self, other):
        if not isinstance(other, FunctionExpression):
            return False
        else:
            return other.name == self.name and other.params == self.params

    def _to_pb(self):
        return Value(
            function_value={
                "name": self.name,
                "args": [p._to_pb() for p in self.params],
            }
        )


class AggregateFunction(FunctionExpression):
    """A base class for aggregation functions that operate across multiple inputs."""


class Selectable(Expression):
    """Base class for expressions that can be selected or aliased in projection stages."""

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        else:
            return other._to_map() == self._to_map()

    @abstractmethod
    def _to_map(self) -> tuple[str, Value]:
        """
        Returns a str: Value representation of the Selectable
        """
        raise NotImplementedError

    @classmethod
    def _value_from_selectables(cls, *selectables: Selectable) -> Value:
        """
        Returns a Value representing a map of Selectables
        """
        return Value(
            map_value={
                "fields": {m[0]: m[1] for m in [s._to_map() for s in selectables]}
            }
        )

    @staticmethod
    def _to_value(field_list: Sequence[Selectable]) -> Value:
        return Value(
            map_value={
                "fields": {m[0]: m[1] for m in [f._to_map() for f in field_list]}
            }
        )


T = TypeVar("T", bound=Expression)


class AliasedExpression(Selectable, Generic[T]):
    """Wraps an expression with an alias."""

    def __init__(self, expr: T, alias: str):
        self.expr = expr
        self.alias = alias

    def _to_map(self):
        return self.alias, self.expr._to_pb()

    def __repr__(self):
        return f"{self.expr}.as_('{self.alias}')"

    def _to_pb(self):
        return Value(map_value={"fields": {self.alias: self.expr._to_pb()}})


class Field(Selectable):
    """Represents a reference to a field within a document."""

    DOCUMENT_ID = "__name__"

    def __init__(self, path: str):
        """Initializes a Field reference.

        Args:
            path: The dot-separated path to the field (e.g., "address.city").
                  Use Field.DOCUMENT_ID for the document ID.
        """
        self.path = path

    @staticmethod
    def of(path: str):
        """Creates a Field reference.

        Args:
            path: The dot-separated path to the field (e.g., "address.city").
                  Use Field.DOCUMENT_ID for the document ID.

        Returns:
            A new Field instance.
        """
        return Field(path)

    def _to_map(self):
        return self.path, self._to_pb()

    def __repr__(self):
        return f"Field.of({self.path!r})"

    def _to_pb(self):
        return Value(field_reference_value=self.path)


class BooleanExpression(FunctionExpression):
    """Filters the given data in some way."""

    @staticmethod
    def _from_query_filter_pb(filter_pb, client):
        if isinstance(filter_pb, Query_pb.CompositeFilter):
            sub_filters = [
                BooleanExpression._from_query_filter_pb(f, client)
                for f in filter_pb.filters
            ]
            if filter_pb.op == Query_pb.CompositeFilter.Operator.OR:
                return Or(*sub_filters)
            elif filter_pb.op == Query_pb.CompositeFilter.Operator.AND:
                return And(*sub_filters)
            else:
                raise TypeError(
                    f"Unexpected CompositeFilter operator type: {filter_pb.op}"
                )
        elif isinstance(filter_pb, Query_pb.UnaryFilter):
            field = Field.of(filter_pb.field.field_path)
            if filter_pb.op == Query_pb.UnaryFilter.Operator.IS_NAN:
                return And(field.exists(), field.equal(float("nan")))
            elif filter_pb.op == Query_pb.UnaryFilter.Operator.IS_NOT_NAN:
                return And(field.exists(), Not(field.equal(float("nan"))))
            elif filter_pb.op == Query_pb.UnaryFilter.Operator.IS_NULL:
                return And(field.exists(), field.equal(None))
            elif filter_pb.op == Query_pb.UnaryFilter.Operator.IS_NOT_NULL:
                return And(field.exists(), Not(field.equal(None)))
            else:
                raise TypeError(f"Unexpected UnaryFilter operator type: {filter_pb.op}")
        elif isinstance(filter_pb, Query_pb.FieldFilter):
            field = Field.of(filter_pb.field.field_path)
            value = decode_value(filter_pb.value, client)
            if filter_pb.op == Query_pb.FieldFilter.Operator.LESS_THAN:
                return And(field.exists(), field.less_than(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.LESS_THAN_OR_EQUAL:
                return And(field.exists(), field.less_than_or_equal(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.GREATER_THAN:
                return And(field.exists(), field.greater_than(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.GREATER_THAN_OR_EQUAL:
                return And(field.exists(), field.greater_than_or_equal(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.EQUAL:
                return And(field.exists(), field.equal(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.NOT_EQUAL:
                return And(field.exists(), field.not_equal(value))
            if filter_pb.op == Query_pb.FieldFilter.Operator.ARRAY_CONTAINS:
                return And(field.exists(), field.array_contains(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.ARRAY_CONTAINS_ANY:
                return And(field.exists(), field.array_contains_any(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.IN:
                return And(field.exists(), field.equal_any(value))
            elif filter_pb.op == Query_pb.FieldFilter.Operator.NOT_IN:
                return And(field.exists(), field.not_equal_any(value))
            else:
                raise TypeError(f"Unexpected FieldFilter operator type: {filter_pb.op}")
        elif isinstance(filter_pb, Query_pb.Filter):
            # unwrap oneof
            f = (
                filter_pb.composite_filter
                or filter_pb.field_filter
                or filter_pb.unary_filter
            )
            return BooleanExpression._from_query_filter_pb(f, client)
        else:
            raise TypeError(f"Unexpected filter type: {type(filter_pb)}")


class Array(FunctionExpression):
    """
    Creates an expression that creates a Firestore array value from an input list.

    Example:
        >>> Array(["bar", Field.of("baz")])

    Args:
        elements: The input list to evaluate in the expression
    """

    def __init__(self, elements: list[Expression | CONSTANT_TYPE]):
        if not isinstance(elements, list):
            raise TypeError("Array must be constructed with a list")
        converted_elements = [
            self._cast_to_expr_or_convert_to_constant(el) for el in elements
        ]
        super().__init__("array", converted_elements)

    def __repr__(self):
        return f"Array({self.params})"


class Map(FunctionExpression):
    """
    Creates an expression that creates a Firestore map value from an input dict.

    Example:
        >>> Expression.map({"foo": "bar", "baz": Field.of("baz")})

    Args:
        elements: The input dict to evaluate in the expression
    """

    def __init__(self, elements: dict[str | Constant[str], Expression | CONSTANT_TYPE]):
        element_list = []
        for k, v in elements.items():
            element_list.append(self._cast_to_expr_or_convert_to_constant(k))
            element_list.append(self._cast_to_expr_or_convert_to_constant(v))
        super().__init__("map", element_list)

    def __repr__(self):
        formatted_params = [
            a.value if isinstance(a, Constant) else a for a in self.params
        ]
        d = {a: b for a, b in zip(formatted_params[::2], formatted_params[1::2])}
        return f"Map({d})"


class And(BooleanExpression):
    """
    Represents an expression that performs a logical 'AND' operation on multiple filter conditions.

    Example:
        >>> # Check if the 'age' field is greater than 18 AND the 'city' field is "London" AND
        >>> # the 'status' field is "active"
        >>> And(Field.of("age").greater_than(18), Field.of("city").equal("London"), Field.of("status").equal("active"))

    Args:
        *conditions: The filter conditions to 'AND' together.
    """

    def __init__(self, *conditions: "BooleanExpression"):
        super().__init__("and", conditions, use_infix_repr=False)


class Not(BooleanExpression):
    """
    Represents an expression that negates a filter condition.

    Example:
        >>> # Find documents where the 'completed' field is NOT true
        >>> Not(Field.of("completed").equal(True))

    Args:
        condition: The filter condition to negate.
    """

    def __init__(self, condition: BooleanExpression):
        super().__init__("not", [condition], use_infix_repr=False)


class Or(BooleanExpression):
    """
    Represents expression that performs a logical 'OR' operation on multiple filter conditions.

    Example:
       >>> # Check if the 'age' field is greater than 18 OR the 'city' field is "London" OR
       >>> # the 'status' field is "active"
       >>> Or(Field.of("age").greater_than(18), Field.of("city").equal("London"), Field.of("status").equal("active"))

    Args:
        *conditions: The filter conditions to 'OR' together.
    """

    def __init__(self, *conditions: "BooleanExpression"):
        super().__init__("or", conditions, use_infix_repr=False)


class Xor(BooleanExpression):
    """
    Represents an expression that performs a logical 'XOR' (exclusive OR) operation on multiple filter conditions.

    Example:
       >>> # Check if only one of the conditions is true: 'age' greater than 18, 'city' is "London",
       >>> # or 'status' is "active".
       >>> Xor(Field.of("age").greater_than(18), Field.of("city").equal("London"), Field.of("status").equal("active"))

    Args:
        *conditions: The filter conditions to 'XOR' together.
    """

    def __init__(self, conditions: Sequence["BooleanExpression"]):
        super().__init__("xor", conditions, use_infix_repr=False)


class Conditional(BooleanExpression):
    """
    Represents a conditional expression that evaluates to a 'then' expression if a condition is true
    and an 'else' expression if the condition is false.

    Example:
        >>> # If 'age' is greater than 18, return "Adult"; otherwise, return "Minor".
        >>> Conditional(Field.of("age").greater_than(18), Constant.of("Adult"), Constant.of("Minor"));

    Args:
        condition: The condition to evaluate.
        then_expr: The expression to return if the condition is true.
        else_expr: The expression to return if the condition is false
    """

    def __init__(
        self, condition: BooleanExpression, then_expr: Expression, else_expr: Expression
    ):
        super().__init__(
            "conditional", [condition, then_expr, else_expr], use_infix_repr=False
        )


class Count(AggregateFunction):
    """
    Represents an aggregation that counts the number of stage inputs with valid evaluations of the
    expression or field.

    Example:
        >>> # Count the total number of products
        >>> Field.of("productId").count().as_("totalProducts")
        >>> Count(Field.of("productId"))
        >>> Count().as_("count")

    Args:
        expression: The expression or field to count. If None, counts all stage inputs.
    """

    def __init__(self, expression: Expression | None = None):
        expression_list = [expression] if expression else []
        super().__init__("count", expression_list, use_infix_repr=bool(expression_list))


class CurrentTimestamp(FunctionExpression):
    """Creates an expression that returns the current timestamp

    Returns:
        A new `Expression` representing the current timestamp.
    """

    def __init__(self):
        super().__init__("current_timestamp", [], use_infix_repr=False)
