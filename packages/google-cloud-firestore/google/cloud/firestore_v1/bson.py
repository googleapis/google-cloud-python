# -*- coding: utf-8 -*-
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
"""BSON data types support for Firestore Python SDK.

This module provides Python representations of BSON data types (such as
`BSONObjectID`, `BSONDecimal128`, `BSONTimestamp`, `BSONRegex`, `BSONBinary`,
`BSONInt32`, `BSONMinKey`, and `BSONMaxKey`) for document field serialization
in Google Cloud Firestore.

Example:
    >>> from google.cloud.firestore_v1.bson import BSONObjectID, BSONDecimal128
    >>> doc_data = {
    ...     "_id": BSONObjectID("507f191e810c19729de860ea"),
    ...     "price": BSONDecimal128("123.45"),
    ... }
"""

import abc
import decimal
import re
from typing import Any, Dict, Union

__all__ = [
    "BSONType",
    "BSONObjectID",
    "BSONDecimal128",
    "BSONTimestamp",
    "BSONRegex",
    "BSONBinary",
    "BSONInt32",
    "BSONMinKey",
    "BSONMaxKey",
]

_OBJECT_ID_BYTES_LEN = 12
_HEX_24_REGEX = re.compile(r"^[0-9a-fA-F]{24}$")


def _is_strict_int(val: Any) -> bool:
    """Verifies integer type while strictly excluding boolean subclasses.

    Args:
        val (Any): Value to check.

    Returns:
        bool: True if val is an int and not a bool, False otherwise.
    """
    return isinstance(val, int) and not isinstance(val, bool)


class BSONType(abc.ABC):
    """Abstract base class for all BSON type containers in Firestore."""

    __slots__ = ()

    @abc.abstractmethod
    def to_map_value(self) -> Dict[str, Any]:
        """Returns legacy map dictionary representation for wire serialization.

        Returns:
            Dict[str, Any]: Map representation dictionary formatted for Firestore.
        """

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Value equality comparison contract for BSON objects."""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Hash representation contract for set and dictionary keys."""


class BSONObjectID(BSONType):
    """Represents a 12-byte BSON ObjectID identifier.

    Args:
        value (Union[str, bytes]): A 24-character hexadecimal string
            or 12 raw bytes.

    Raises:
        TypeError: If value is not a string or bytes.
        ValueError: If string is not a 24-character hex string or bytes length is not 12.

    Example:
        >>> oid = BSONObjectID("507f191e810c19729de860ea")
        >>> oid.value
        '507f191e810c19729de860ea'
    """

    __slots__ = ("_value",)

    def __init__(self, value: Union[str, bytes]):
        if isinstance(value, str):
            if not _HEX_24_REGEX.match(value):
                raise ValueError(
                    "BSONObjectID string must be a 24-character hex string."
                )
            self._value: str = value.lower()
        elif isinstance(value, bytes):
            if len(value) != _OBJECT_ID_BYTES_LEN:
                raise ValueError(
                    f"BSONObjectID bytes input must be {_OBJECT_ID_BYTES_LEN} raw bytes."
                )
            self._value = value.hex()
        else:
            raise TypeError("BSONObjectID requires str or bytes.")

    @property
    def value(self) -> str:
        """str: The 24-character lowercase hexadecimal representation."""
        return self._value

    def to_map_value(self) -> Dict[str, str]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__oid__": self._value}

    def __repr__(self) -> str:
        return f"BSONObjectID('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONObjectID):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)


class BSONDecimal128(BSONType):
    """Represents a BSON IEEE 754-2008 Decimal128 floating-point value.

    Args:
        value (Union[str, decimal.Decimal]): String decimal format or native Decimal.

    Raises:
        TypeError: If value is a boolean or invalid type.
        ValueError: If string format cannot be parsed into a Decimal128 value.

    Example:
        >>> dec = BSONDecimal128("123.45")
        >>> dec.to_decimal()
        Decimal('123.45')
    """

    __slots__ = ("_value",)

    def __init__(self, value: Union[str, decimal.Decimal]):
        if isinstance(value, bool):
            raise TypeError("BSONDecimal128 value cannot be bool.")

        if isinstance(value, decimal.Decimal):
            self._value: str = str(value)
        elif isinstance(value, str):
            try:
                decimal.Decimal(value)
            except (decimal.DecimalException, ArithmeticError, ValueError) as exc:
                raise ValueError(
                    f"Invalid Decimal128 string format: {value!r}"
                ) from exc
            self._value = value
        else:
            raise TypeError("BSONDecimal128 requires str or decimal.Decimal.")

    @property
    def value(self) -> str:
        """str: The string representation of the Decimal128 value."""
        return self._value

    def to_decimal(self) -> decimal.Decimal:
        """Converts to a native Python decimal.Decimal object.

        Returns:
            decimal.Decimal: Native Python Decimal instance.
        """
        return decimal.Decimal(self._value)

    def to_map_value(self) -> Dict[str, str]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__decimal128__": self._value}

    def __repr__(self) -> str:
        return f"BSONDecimal128('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONDecimal128):
            if self._value == other._value:
                return True
            other_dec = other.to_decimal()
        elif isinstance(other, decimal.Decimal):
            other_dec = other
        else:
            return False

        try:
            self_dec = self.to_decimal()
            if self_dec.is_nan() or other_dec.is_nan():
                return False
            return self_dec == other_dec
        except (decimal.DecimalException, ArithmeticError):
            return False

    def __hash__(self) -> int:
        try:
            d = self.to_decimal()
            if d.is_nan():
                return hash(self._value)
            return hash(d)
        except (decimal.DecimalException, ArithmeticError):
            return hash(self._value)


class BSONTimestamp(BSONType):
    """Represents a BSON Timestamp (seconds + increment uint32 pair).

    Args:
        seconds (int): 32-bit unsigned integer timestamp in seconds.
        increment (int): 32-bit unsigned integer incrementing counter.

    Raises:
        TypeError: If seconds or increment is not an integer.
        ValueError: If seconds or increment is outside range [0, 4294967295].

    Example:
        >>> ts = BSONTimestamp(1700000000, 1)
        >>> ts.seconds
        1700000000
    """

    __slots__ = ("_seconds", "_increment")

    def __init__(self, seconds: int, increment: int):
        if not _is_strict_int(seconds) or not _is_strict_int(increment):
            raise TypeError("seconds and increment must be ints.")
        if not (0 <= seconds <= 4294967295) or not (0 <= increment <= 4294967295):
            raise ValueError("seconds and increment must be uint32 (0 to 4294967295).")
        self._seconds: int = int(seconds)
        self._increment: int = int(increment)

    @property
    def seconds(self) -> int:
        """int: The uint32 seconds component."""
        return self._seconds

    @property
    def increment(self) -> int:
        """int: The uint32 increment component."""
        return self._increment

    def to_map_value(self) -> Dict[str, Dict[str, int]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {
            "__timestamp__": {"seconds": self._seconds, "increment": self._increment}
        }

    def __repr__(self) -> str:
        return f"BSONTimestamp(seconds={self._seconds}, increment={self._increment})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONTimestamp):
            return (self._seconds, self._increment) == (
                other._seconds,
                other._increment,
            )
        return False

    def __hash__(self) -> int:
        return hash((self._seconds, self._increment))


class BSONRegex(BSONType):
    """Represents a BSON Regular Expression.

    Args:
        pattern (str): Regular expression pattern string.
        options (str, optional): BSON regex option flags string (e.g., "i", "m", "s").

    Raises:
        TypeError: If pattern or options is not a string.

    Example:
        >>> rx = BSONRegex("^[a-z]+$", "i")
        >>> rx.pattern
        '^[a-z]+$'
    """

    __slots__ = ("_pattern", "_options")

    def __init__(self, pattern: str, options: str = ""):
        if not isinstance(pattern, str) or not isinstance(options, str):
            raise TypeError("pattern and options must be strings.")
        self._pattern: str = pattern
        self._options: str = "".join(sorted(set(options)))

    @property
    def pattern(self) -> str:
        """str: Regular expression pattern string."""
        return self._pattern

    @property
    def options(self) -> str:
        """str: Sorted BSON regex option flags."""
        return self._options

    def to_map_value(self) -> Dict[str, Dict[str, str]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__regex__": {"pattern": self._pattern, "options": self._options}}

    def __repr__(self) -> str:
        return f"BSONRegex(pattern={self._pattern!r}, options={self._options!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONRegex):
            return (self._pattern, self._options) == (other._pattern, other._options)
        return False

    def __hash__(self) -> int:
        return hash((self._pattern, self._options))


class BSONBinary(BSONType):
    """Represents BSON Binary data with a subtype tag.

    Args:
        data (bytes): Raw binary payload bytes.
        subtype (int, optional): BSON binary subtype byte in range 0..255. Defaults to 0.

    Raises:
        TypeError: If data is not bytes or subtype is not an integer.
        ValueError: If subtype is outside range 0..255.

    Example:
        >>> bin_data = BSONBinary(b"raw_data", 0)
        >>> bin_data.data
        b'raw_data'
    """

    __slots__ = ("_subtype", "_data")

    def __init__(self, data: bytes, subtype: int = 0):
        if not _is_strict_int(subtype):
            raise TypeError("subtype must be an integer.")
        if not (0 <= subtype <= 255):
            raise ValueError("subtype must be in range 0..255.")
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes.")
        self._data: bytes = data
        self._subtype: int = int(subtype)

    @property
    def subtype(self) -> int:
        """int: The binary subtype integer."""
        return self._subtype

    @property
    def data(self) -> bytes:
        """bytes: The raw binary payload bytes."""
        return self._data

    def to_map_value(self) -> Dict[str, Dict[str, Any]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__binary__": {"sub_type": self._subtype, "bytes": self._data}}

    def __repr__(self) -> str:
        return f"BSONBinary(data={self._data!r}, subtype={self._subtype})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONBinary):
            return (self._data, self._subtype) == (other._data, other._subtype)
        return False

    def __hash__(self) -> int:
        return hash((self._data, self._subtype))


class BSONInt32(BSONType):
    """Represents a signed 32-bit integer BSON value.

    Args:
        value (int): Integer in signed 32-bit range [-2147483648, 2147483647].

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is outside 32-bit signed integer range.

    Example:
        >>> i = BSONInt32(42)
        >>> i.value
        42
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        if not _is_strict_int(value):
            raise TypeError("BSONInt32 value must be an integer.")
        if not (-2147483648 <= value <= 2147483647):
            raise ValueError("BSONInt32 out of range [-2147483648, 2147483647].")
        self._value: int = int(value)

    @property
    def value(self) -> int:
        """int: The 32-bit signed integer value."""
        return self._value

    def __int__(self) -> int:
        return self._value

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__int__": self._value}

    def __repr__(self) -> str:
        return f"BSONInt32({self._value})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONInt32):
            return self._value == other._value
        if type(other) is int and not isinstance(other, bool):
            return self._value == other
        return False

    def __hash__(self) -> int:
        return hash(self._value)


class BSONMinKey(BSONType):
    """Represents a BSON MinKey sentinel value.

    Example:
        >>> min_key = BSONMinKey()
    """

    __slots__ = ()

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__minkey__": 1}

    def __repr__(self) -> str:
        return "BSONMinKey()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BSONMinKey)

    def __hash__(self) -> int:
        return hash("BSONMinKey")


class BSONMaxKey(BSONType):
    """Represents a BSON MaxKey sentinel value.

    Example:
        >>> max_key = BSONMaxKey()
    """

    __slots__ = ()

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__maxkey__": 1}

    def __repr__(self) -> str:
        return "BSONMaxKey()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BSONMaxKey)

    def __hash__(self) -> int:
        return hash("BSONMaxKey")
