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
"""BSON data type support for Cloud Firestore MongoDB compatibility workloads."""

from __future__ import annotations

from typing import Any, Dict, Union


class BSONObjectID:
    """A class representing BSON ObjectID in Python.

    Stored as a 24-character hexadecimal string.
    """

    def __init__(self, value: str):
        if not isinstance(value, str) or len(value) != 24 or not all(c in "0123456789abcdefABCDEF" for c in value):
            raise ValueError("BSONObjectID must be a 24-character hexadecimal string.")
        self._value = value.lower()

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONObjectID):
            return False
        return self._value == other._value

    def __repr__(self) -> str:
        return f"BSONObjectID('{self._value}')"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__oid__": self._value}


class BSONDecimal128:
    """A class representing BSON 128-bit Decimal in Python."""

    def __init__(self, value: Union[str, int, float]):
        self._value = str(value)

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONDecimal128):
            return False
        return self._value == other._value

    def __repr__(self) -> str:
        return f"BSONDecimal128('{self._value}')"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__decimal128__": self._value}


class BSONInt32:
    """A class representing BSON 32-bit Integer in Python."""

    def __init__(self, value: int):
        self._value = int(value)

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONInt32):
            return False
        return self._value == other._value

    def __repr__(self) -> str:
        return f"BSONInt32({self._value})"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__int__": self._value}


class BSONRegex:
    """A class representing BSON Regular Expression in Python."""

    def __init__(self, pattern: str, flags: str = ""):
        self._pattern = str(pattern)
        self._flags = str(flags) if flags is not None else ""

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def flags(self) -> str:
        return self._flags

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONRegex):
            return False
        return self._pattern == other._pattern and self._flags == other._flags

    def __repr__(self) -> str:
        return f"BSONRegex(pattern='{self._pattern}', flags='{self._flags}')"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__regex__": {"pattern": self._pattern, "options": self._flags}}


class BSONTimestamp:
    """A class representing BSON Timestamp in Python."""

    def __init__(self, seconds: int, increment: int):
        self._seconds = int(seconds)
        self._increment = int(increment)

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def increment(self) -> int:
        return self._increment

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONTimestamp):
            return False
        return self._seconds == other._seconds and self._increment == other._increment

    def __repr__(self) -> str:
        return f"BSONTimestamp(seconds={self._seconds}, increment={self._increment})"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__request_timestamp__": {"seconds": self._seconds, "increment": self._increment}}


class BSONBinary:
    """A class representing BSON Binary data in Python."""

    def __init__(self, sub_type: int, data: bytes):
        self._sub_type = int(sub_type)
        self._data = bytes(data)

    @property
    def sub_type(self) -> int:
        return self._sub_type

    @property
    def data(self) -> bytes:
        return self._data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSONBinary):
            return False
        return self._sub_type == other._sub_type and self._data == other._data

    def __repr__(self) -> str:
        return f"BSONBinary(sub_type={self._sub_type}, data={self._data!r})"

    def to_map_value(self) -> Dict[str, Any]:
        return {
            "__binary__": bytes([self._sub_type]) + self._data,
        }


class BSONMinKey:
    """A class representing BSON MinKey in Python."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BSONMinKey)

    def __repr__(self) -> str:
        return "BSONMinKey()"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__min__": None}


class BSONMaxKey:
    """A class representing BSON MaxKey in Python."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BSONMaxKey)

    def __repr__(self) -> str:
        return "BSONMaxKey()"

    def to_map_value(self) -> Dict[str, Any]:
        return {"__max__": None}

