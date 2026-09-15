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
"""BSON data types support for Firestore Python SDK."""

import binascii
import decimal
import re
from typing import Any, Dict, Tuple, Union

__all__ = [
    "BSONObjectID",
    "BSONDecimal128",
    "BSONTimestamp",
    "BSONRegex",
    "BSONBinary",
    "BSONInt32",
    "BSONMinKey",
    "BSONMaxKey",
]

_HEX_24_REGEX = re.compile(r"^[0-9a-fA-F]{24}$")


class BSONObjectID:
    """Represents a 12-byte BSON ObjectID."""

    __slots__ = ("_value",)

    def __init__(self, value: Union[str, bytes, bytearray, memoryview, "BSONObjectID"]):
        if isinstance(value, BSONObjectID):
            self._value: str = value.value
        elif isinstance(value, str):
            if not _HEX_24_REGEX.match(value):
                raise ValueError("BSONObjectID string must be a 24-character hex string.")
            self._value = value.lower()
        elif isinstance(value, (bytes, bytearray, memoryview)):
            raw_bytes = bytes(value)
            if len(raw_bytes) == 12:
                self._value = binascii.hexlify(raw_bytes).decode("ascii").lower()
            elif len(raw_bytes) == 24:
                try:
                    binascii.unhexlify(raw_bytes)
                except Exception as exc:
                    raise ValueError("BSONObjectID 24-byte input must be valid ASCII hex.") from exc
                self._value = raw_bytes.decode("ascii").lower()
            else:
                raise ValueError("BSONObjectID bytes input must be 12 raw bytes or 24 ASCII hex bytes.")
        else:
            raise TypeError("BSONObjectID requires str, bytes, bytearray, memoryview, or BSONObjectID instance.")

    @property
    def value(self) -> str:
        return self._value

    def to_map_value(self) -> Dict[str, str]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__oid__": self._value}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (self.__class__, (self._value,))

    def __repr__(self) -> str:
        return f"BSONObjectID('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONObjectID):
            return self._value == other._value
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self._value)


class BSONDecimal128:
    """Represents a BSON IEEE 754-2008 Decimal128 value."""

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
                raise ValueError(f"Invalid Decimal128 string format: {value!r}") from exc
            self._value = value
        else:
            raise TypeError("BSONDecimal128 requires str or decimal.Decimal.")

    @property
    def value(self) -> str:
        return self._value

    def to_decimal(self) -> decimal.Decimal:
        return decimal.Decimal(self._value)

    def to_map_value(self) -> Dict[str, str]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__decimal128__": self._value}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (self.__class__, (self._value,))

    def __repr__(self) -> str:
        return f"BSONDecimal128('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONDecimal128):
            try:
                d1 = self.to_decimal()
                d2 = other.to_decimal()
                if d1.is_nan() or d2.is_nan():
                    return False
                return d1 == d2
            except (decimal.DecimalException, ArithmeticError):
                return self._value == other._value
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        try:
            d = self.to_decimal()
            if d.is_nan():
                return hash(self._value)
            return hash(d)
        except (decimal.DecimalException, ArithmeticError):
            return hash(self._value)


class BSONTimestamp:
    """Represents a BSON Timestamp (seconds + increment uint32 pair)."""

    __slots__ = ("_seconds", "_increment")

    def __init__(self, seconds: int, increment: int):
        if type(seconds) is not int or type(increment) is not int:
            raise TypeError("seconds and increment must be ints.")
        if not (0 <= seconds <= 4294967295) or not (0 <= increment <= 4294967295):
            raise ValueError("seconds and increment must be uint32 (0 to 4294967295).")
        self._seconds: int = seconds
        self._increment: int = increment

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def increment(self) -> int:
        return self._increment

    def to_map_value(self) -> Dict[str, Dict[str, int]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__timestamp__": {"seconds": self._seconds, "increment": self._increment}}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (self.__class__, (self._seconds, self._increment))

    def __repr__(self) -> str:
        return f"BSONTimestamp(seconds={self._seconds}, increment={self._increment})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONTimestamp):
            return (self._seconds, self._increment) == (other._seconds, other._increment)
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._seconds, self._increment))


class BSONRegex:
    """Represents a BSON Regular Expression."""

    __slots__ = ("_pattern", "_options")

    def __init__(self, pattern: str, options: str = ""):
        if not isinstance(pattern, str) or not isinstance(options, str):
            raise TypeError("pattern and options must be strings.")
        self._pattern: str = pattern
        self._options: str = "".join(sorted(set(options)))

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def options(self) -> str:
        return self._options

    def to_map_value(self) -> Dict[str, Dict[str, str]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__regex__": {"pattern": self._pattern, "options": self._options}}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (self.__class__, (self._pattern, self._options))

    def __repr__(self) -> str:
        return f"BSONRegex(pattern={self._pattern!r}, options={self._options!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONRegex):
            return (self._pattern, self._options) == (other._pattern, other._options)
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._pattern, self._options))


class BSONBinary:
    """Represents BSON Binary data with a subtype."""

    __slots__ = ("_subtype", "_data")

    def __init__(self, data: Union[bytes, bytearray, memoryview], subtype: int = 0):
        if isinstance(subtype, bool) or type(subtype) is not int:
            raise TypeError("subtype must be an integer.")
        if not (0 <= subtype <= 255):
            raise ValueError("subtype must be in range 0..255.")
        try:
            self._data: bytes = bytes(data)
        except TypeError as exc:
            raise TypeError("data must be bytes-like.") from exc
        self._subtype: int = subtype

    @property
    def subtype(self) -> int:
        return self._subtype

    @property
    def data(self) -> bytes:
        return self._data

    def to_map_value(self) -> Dict[str, Dict[str, Any]]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__binary__": {"sub_type": self._subtype, "bytes": self._data}}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (self.__class__, (self._data, self._subtype))

    def __repr__(self) -> str:
        return f"BSONBinary(data={self._data!r}, subtype={self._subtype})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONBinary):
            return (self._data, self._subtype) == (other._data, other._subtype)
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self._data, self._subtype))


class BSONInt32(int):
    """Represents a signed 32-bit integer BSON value."""

    __slots__ = ()

    def __new__(cls, val: Any) -> "BSONInt32":
        if isinstance(val, bool):
            raise TypeError("BSONInt32 value cannot be bool.")
        if type(val) is not int and not isinstance(val, (int, BSONInt32)):
            raise TypeError("BSONInt32 value must be an integer.")
        if not (-2147483648 <= int(val) <= 2147483647):
            raise ValueError("BSONInt32 out of range [-2147483648, 2147483647].")
        return super().__new__(cls, val)

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__int__": int(self)}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (BSONInt32, (int(self),))


class BSONMinKey:
    """Represents a BSON MinKey sentinel."""

    __slots__ = ()
    _instance = None

    def __new__(cls) -> "BSONMinKey":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__minkey__": 1}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (BSONMinKey, ())

    def __copy__(self) -> "BSONMinKey":
        return self

    def __deepcopy__(self, memo: Any) -> "BSONMinKey":
        return self

    def __repr__(self) -> str:
        return "BSONMinKey()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BSONMinKey)

    def __ne__(self, other: Any) -> bool:
        return not isinstance(other, BSONMinKey)

    def __hash__(self) -> int:
        return hash("BSONMinKey")


class BSONMaxKey:
    """Represents a BSON MaxKey sentinel."""

    __slots__ = ()
    _instance = None

    def __new__(cls) -> "BSONMaxKey":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def to_map_value(self) -> Dict[str, int]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__maxkey__": 1}

    def __reduce__(self) -> Tuple[Any, Tuple[Any, ...]]:
        return (BSONMaxKey, ())

    def __copy__(self) -> "BSONMaxKey":
        return self

    def __deepcopy__(self, memo: Any) -> "BSONMaxKey":
        return self

    def __repr__(self) -> str:
        return "BSONMaxKey()"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BSONMaxKey)

    def __ne__(self, other: Any) -> bool:
        return not isinstance(other, BSONMaxKey)

    def __hash__(self) -> int:
        return hash("BSONMaxKey")
