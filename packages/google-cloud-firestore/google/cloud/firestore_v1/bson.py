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

This module provides Python representations of BSON data types
for document field serialization in Google Cloud Firestore
according to the official Firestore BSON specification.

Example:
    >>> from google.cloud.firestore_v1.bson import BSONObjectId
    >>> doc_data = {"user_id": BSONObjectId("507f191e810c19729de860ea")}
"""

import abc
import re
from typing import Any, Dict, Union

__all__ = [
    "BSONObjectId",
    "BSONMinKey",
    "BSONMaxKey",
    "BSONInt32",
    "BSONBinary",
    "BSONTimestamp",
    "BSONRegex",
]

_OBJECT_ID_BYTES_LEN = 12
_HEX_24_REGEX = re.compile(r"^[0-9a-fA-F]{24}$")


class _BSONType(abc.ABC):
    """Abstract base class for all BSON type containers in Firestore."""

    __slots__ = ()

    @abc.abstractmethod
    def _to_map_value(self) -> Any:
        """Returns representation for wire serialization.

        Returns:
            Any: Map representation dictionary or raw bytes formatted for Firestore.
        """

    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Value equality comparison contract for BSON objects."""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Hash representation contract for set and dictionary keys."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class BSONObjectId(_BSONType):
    """Represents a 12-byte BSON ObjectId identifier.

    Args:
        value (Union[str, bytes]): A 24-character hexadecimal string
            or 12 raw bytes.

    Raises:
        TypeError: If value is not a string or bytes.
        ValueError: If string is not a 24-character hex string or bytes length is not 12.

    Example:
        >>> oid = BSONObjectId("507f191e810c19729de860ea")
        >>> oid.value
        '507f191e810c19729de860ea'
    """

    __slots__ = ("_value",)

    def __init__(self, value: Union[str, bytes]):
        if isinstance(value, str):
            if not _HEX_24_REGEX.match(value):
                raise ValueError(
                    "BSONObjectId string must be a 24-character hex string."
                )
            self._value: str = value.lower()
        elif isinstance(value, bytes):
            if len(value) != _OBJECT_ID_BYTES_LEN:
                raise ValueError(
                    f"BSONObjectId bytes input must be {_OBJECT_ID_BYTES_LEN} raw bytes."
                )
            self._value = value.hex()
        else:
            raise TypeError("BSONObjectId requires str or bytes.")

    @property
    def value(self) -> str:
        """str: The 24-character lowercase hexadecimal representation."""
        return self._value

    def _to_map_value(self) -> Dict[str, str]:
        """Returns legacy map dictionary representation for wire serialization."""
        return {"__oid__": self._value}

    def __repr__(self) -> str:
        return f"BSONObjectId('{self._value}')"

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONObjectId):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self), self._value))


class BSONMinKey(_BSONType):
    """Represents the BSON MinKey sentinel value for query range boundaries."""

    __slots__ = ()

    def _to_map_value(self) -> Dict[str, None]:
        """Returns map dictionary representation for wire serialization."""
        return {"__min__": None}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONMinKey):
            return True
        return NotImplemented

    def __hash__(self) -> int:
        return hash(type(self))


class BSONMaxKey(_BSONType):
    """Represents the BSON MaxKey sentinel value for query range boundaries."""

    __slots__ = ()

    def _to_map_value(self) -> Dict[str, None]:
        """Returns map dictionary representation for wire serialization."""
        return {"__max__": None}

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONMaxKey):
            return True
        return NotImplemented

    def __hash__(self) -> int:
        return hash(type(self))


class BSONInt32(_BSONType):
    """Represents a 32-bit signed integer value container for Firestore BSON.

    Args:
        value (int): A 32-bit signed integer value.

    Raises:
        TypeError: If value is not an integer or is a boolean.
        ValueError: If value is outside the 32-bit signed range (-2147483648 to 2147483647).

    Example:
        >>> int_val = BSONInt32(42)
        >>> int_val.value
        42
    """

    __slots__ = ("_value",)

    _MIN_INT32: int = -(1 << 31)
    _MAX_INT32: int = (1 << 31) - 1

    def __init__(self, value: int):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("BSONInt32 requires an int.")
        if not (self._MIN_INT32 <= value <= self._MAX_INT32):
            raise ValueError(
                f"BSONInt32 value must be between {self._MIN_INT32} and {self._MAX_INT32}."
            )
        self._value: int = value

    @property
    def value(self) -> int:
        """int: The 32-bit signed integer value."""
        return self._value

    def _to_map_value(self) -> Dict[str, int]:
        """Returns map dictionary representation for wire serialization."""
        return {"__int__": self._value}

    def __repr__(self) -> str:
        return f"BSONInt32({self._value})"

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        return self._value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONInt32):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self), self._value))


class BSONBinary(_BSONType):
    """Represents a BSON binary data container with a subtype for Firestore.

    Args:
        data (Union[bytes, bytearray]): The binary byte payload.
        subtype (int): A 1-byte BSON binary subtype tag (1 to 255).

    Raises:
        TypeError: If data is not bytes/bytearray or subtype is not an integer/is a boolean.
        ValueError: If subtype is outside the 1-byte range (1 to 255).

    Example:
        >>> binary = BSONBinary(b"hello world", subtype=128)
        >>> binary.data
        b'hello world'
        >>> binary.subtype
        128
    """

    __slots__ = ("_data", "_subtype")

    _MIN_SUBTYPE: int = 1
    _MAX_SUBTYPE: int = 255

    def __init__(self, data: Union[bytes, bytearray], subtype: int):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("BSONBinary data must be bytes or bytearray.")
        if isinstance(subtype, bool) or not isinstance(subtype, int):
            raise TypeError("BSONBinary subtype must be an int.")
        if not (self._MIN_SUBTYPE <= subtype <= self._MAX_SUBTYPE):
            raise ValueError(
                f"BSONBinary subtype must be between {self._MIN_SUBTYPE} and {self._MAX_SUBTYPE}."
            )
        self._data: bytes = bytes(data)
        self._subtype: int = subtype

    @property
    def data(self) -> bytes:
        """bytes: The binary byte payload."""
        return self._data

    @property
    def subtype(self) -> int:
        """int: The BSON binary subtype tag (1 to 255)."""
        return self._subtype

    def _to_map_value(self) -> Union[bytes, Dict[str, bytes]]:
        """Returns representation for wire serialization."""
        return {"__binary__": bytes([self._subtype]) + self._data}

    def __repr__(self) -> str:
        return f"BSONBinary({self._data!r}, subtype={self._subtype})"

    def __bytes__(self) -> bytes:
        return self._data

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONBinary):
            return self._data == other._data and self._subtype == other._subtype
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self), self._data, self._subtype))


class BSONTimestamp(_BSONType):
    """Container for BSON Timestamp values.

    Args:
        seconds (int): Seconds count.
        increment (int): Increment/ordinal.

    Raises:
        TypeError: If seconds or increment is not an int or is a bool.

    Example:
        >>> ts = BSONTimestamp(1700000000, 1)
        >>> ts.seconds
        1700000000
        >>> ts.increment
        1
    """

    __slots__ = ("_seconds", "_increment")

    def __init__(self, seconds: int, increment: int):
        if isinstance(seconds, bool) or not isinstance(seconds, int):
            raise TypeError("BSONTimestamp seconds must be an int.")
        if isinstance(increment, bool) or not isinstance(increment, int):
            raise TypeError("BSONTimestamp increment must be an int.")
        self._seconds: int = seconds
        self._increment: int = increment

    @property
    def seconds(self) -> int:
        """int: The seconds value."""
        return self._seconds

    @property
    def increment(self) -> int:
        """int: The increment value."""
        return self._increment

    def _to_map_value(self) -> Dict[str, Dict[str, int]]:
        """Returns map dictionary representation for wire serialization."""
        return {
            "__request_timestamp__": {
                "seconds": self._seconds,
                "increment": self._increment,
            }
        }

    def __repr__(self) -> str:
        return f"BSONTimestamp(seconds={self._seconds}, increment={self._increment})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONTimestamp):
            return (
                self._seconds == other._seconds and self._increment == other._increment
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self), self._seconds, self._increment))


class BSONRegex(_BSONType):
    """Represents a BSON Regular Expression container for Firestore.

    Args:
        pattern (str): The regular expression pattern string.
        options (Union[str, re.RegexFlag, int], optional): BSON regex option flags
            as a string (e.g. "i", "m", "s") or Python `re` flag integer (e.g. `re.I | re.M`).
            Defaults to "".

    Raises:
        TypeError: If pattern is not a string or options is invalid type.

    Example:
        >>> regex = BSONRegex("^hello.*$", options="i")
        >>> regex.pattern
        '^hello.*$'
        >>> regex.options
        'i'
    """

    __slots__ = ("_pattern", "_options")

    _FLAG_TO_OPTION: Dict[int, str] = {
        re.IGNORECASE: "i",
        re.LOCALE: "l",
        re.MULTILINE: "m",
        re.DOTALL: "s",
        re.UNICODE: "u",
        re.VERBOSE: "x",
    }

    def __init__(self, pattern: str, options: Union[str, re.RegexFlag, int] = ""):
        if not isinstance(pattern, str):
            raise TypeError("BSONRegex pattern must be a str.")

        if isinstance(options, bool):
            raise TypeError("BSONRegex options must be a str or re flag integer.")

        if isinstance(options, str):
            self._options: str = "".join(sorted(set(options)))
        elif isinstance(options, int):
            opts = []
            for flag, char in self._FLAG_TO_OPTION.items():
                if options & flag:
                    opts.append(char)
            self._options = "".join(sorted(opts))
        else:
            raise TypeError("BSONRegex options must be a str or re flag integer.")

        self._pattern: str = pattern

    @property
    def pattern(self) -> str:
        """str: The regular expression pattern string."""
        return self._pattern

    @property
    def options(self) -> str:
        """str: The normalized BSON regex option flags sorted alphabetically."""
        return self._options

    def _to_map_value(self) -> Dict[str, Dict[str, str]]:
        """Returns map dictionary representation for wire serialization."""
        return {
            "__regex__": {
                "pattern": self._pattern,
                "options": self._options,
            }
        }

    def __repr__(self) -> str:
        return f"BSONRegex({self._pattern!r}, options={self._options!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BSONRegex):
            return self._pattern == other._pattern and self._options == other._options
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self), self._pattern, self._options))
