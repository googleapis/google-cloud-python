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
