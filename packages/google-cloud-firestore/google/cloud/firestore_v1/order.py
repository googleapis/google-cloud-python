# -*- coding: utf-8 -*-
# Copyright 2017 Google LLC All rights reserved.
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

"""Order semantics for Firestore types matching backend database indexes."""

from __future__ import annotations

import collections.abc
import datetime
import decimal
import math
from enum import Enum
from typing import Any, Tuple

from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from google.cloud.firestore_v1._helpers import GeoPoint, decode_dict
from google.cloud.firestore_v1.base_document import BaseDocumentReference
from google.cloud.firestore_v1.bson import (
    BSONBinary,
    BSONDecimal128,
    BSONInt32,
    BSONMaxKey,
    BSONMinKey,
    BSONObjectID,
    BSONRegex,
    BSONTimestamp,
)
from google.cloud.firestore_v1.vector import Vector


class _RefValue:
    """Internal wrapper for DocumentReference path comparison."""

    def __init__(self, value: str):
        self.value = value


def _extract_canonical_value(val: Any) -> Any:
    """Extract canonical native Python representation from protobuf or BSON objects."""
    if val is None or isinstance(
        val,
        (
            bool,
            BSONMinKey,
            BSONMaxKey,
            BSONObjectID,
            BSONDecimal128,
            BSONTimestamp,
            BSONRegex,
            BSONBinary,
            BSONInt32,
            GeoPoint,
            Vector,
            _RefValue,
            BaseDocumentReference,
        ),
    ):
        return val

    # Handle protobuf Value message
    if hasattr(val, "_pb") or hasattr(val, "WhichOneof"):
        value_pb = getattr(val, "_pb", val)
        vtype = value_pb.WhichOneof("value_type")
        if vtype == "null_value":
            return None
        elif vtype == "boolean_value":
            return value_pb.boolean_value
        elif vtype == "integer_value":
            return value_pb.integer_value
        elif vtype == "double_value":
            return value_pb.double_value
        elif vtype == "timestamp_value":
            return DatetimeWithNanoseconds.from_timestamp_pb(value_pb.timestamp_value)
        elif vtype == "string_value":
            return value_pb.string_value
        elif vtype == "bytes_value":
            return value_pb.bytes_value
        elif vtype == "reference_value":
            return _RefValue(value_pb.reference_value)
        elif vtype == "geo_point_value":
            return GeoPoint(
                value_pb.geo_point_value.latitude, value_pb.geo_point_value.longitude
            )
        elif vtype == "array_value":
            return [_extract_canonical_value(x) for x in value_pb.array_value.values]
        elif vtype == "map_value":
            decoded = decode_dict(
                value_pb.map_value.fields, client=None, decode_bson=True
            )
            return _extract_canonical_value(decoded)

    # Handle legacy map dictionary with single key signature
    if isinstance(val, dict) and len(val) == 1:
        key = next(iter(val))
        if key in (
            "__oid__",
            "__decimal128__",
            "__int__",
            "__minkey__",
            "__maxkey__",
            "__timestamp__",
            "__regex__",
            "__binary__",
        ):
            v = val[key]
            if key == "__oid__" and isinstance(v, str):
                return BSONObjectID(v)
            elif key == "__decimal128__" and isinstance(v, str):
                return BSONDecimal128(v)
            elif key == "__int__" and isinstance(v, int):
                return BSONInt32(v)
            elif key == "__minkey__":
                return BSONMinKey()
            elif key == "__maxkey__":
                return BSONMaxKey()
            elif key == "__timestamp__" and isinstance(
                v, (dict, collections.abc.Mapping)
            ):
                return BSONTimestamp(v.get("seconds", 0), v.get("increment", 0))
            elif key == "__regex__" and isinstance(v, (dict, collections.abc.Mapping)):
                return BSONRegex(v.get("pattern", ""), v.get("options", ""))
            elif key == "__binary__" and isinstance(v, (dict, collections.abc.Mapping)):
                return BSONBinary(v.get("bytes", b""), subtype=v.get("sub_type", 0))
            else:
                try:
                    decoded = decode_dict(val, client=None, decode_bson=True)
                    if not isinstance(decoded, dict):
                        return _extract_canonical_value(decoded)
                except Exception:
                    pass

    if isinstance(val, (list, tuple)):
        return [_extract_canonical_value(x) for x in val]

    if isinstance(val, dict):
        return {k: _extract_canonical_value(v) for k, v in val.items()}

    return val


class TypeOrder(Enum):
    """The 17-rank BSON and Firestore data type priority order."""

    MIN_KEY = 1
    NULL = 2
    BOOLEAN = 3
    NUMBER = 4
    TIMESTAMP = 5
    BSON_TIMESTAMP = 6
    STRING = 7
    BLOB = 8
    BSON_BINARY = 9
    REF = 10
    BSON_OBJECT_ID = 11
    GEO_POINT = 12
    BSON_REGEX = 13
    ARRAY = 14
    VECTOR = 15
    OBJECT = 16
    MAX_KEY = 17

    @staticmethod
    def from_value(value) -> TypeOrder:
        cval = _extract_canonical_value(value)
        if isinstance(cval, BSONMinKey):
            return TypeOrder.MIN_KEY
        if cval is None:
            return TypeOrder.NULL
        if isinstance(cval, bool):
            return TypeOrder.BOOLEAN
        if isinstance(cval, (int, float, BSONInt32, BSONDecimal128)):
            return TypeOrder.NUMBER
        if isinstance(cval, (datetime.datetime, DatetimeWithNanoseconds)):
            return TypeOrder.TIMESTAMP
        if isinstance(cval, BSONTimestamp):
            return TypeOrder.BSON_TIMESTAMP
        if isinstance(cval, str):
            return TypeOrder.STRING
        if isinstance(cval, bytes):
            return TypeOrder.BLOB
        if isinstance(cval, BSONBinary):
            return TypeOrder.BSON_BINARY
        if isinstance(cval, (_RefValue, BaseDocumentReference)):
            return TypeOrder.REF
        if isinstance(cval, BSONObjectID):
            return TypeOrder.BSON_OBJECT_ID
        if isinstance(cval, GeoPoint):
            return TypeOrder.GEO_POINT
        if isinstance(cval, BSONRegex):
            return TypeOrder.BSON_REGEX
        if isinstance(cval, (list, tuple)):
            return TypeOrder.ARRAY
        if isinstance(cval, Vector):
            return TypeOrder.VECTOR
        if isinstance(cval, (dict, collections.abc.Mapping)):
            return TypeOrder.OBJECT
        if isinstance(cval, BSONMaxKey):
            return TypeOrder.MAX_KEY

        raise ValueError(f"Could not detect value type for {cval!r}")


_TYPE_ORDER_MAP = {
    TypeOrder.MIN_KEY: 1,
    TypeOrder.NULL: 2,
    TypeOrder.BOOLEAN: 3,
    TypeOrder.NUMBER: 4,
    TypeOrder.TIMESTAMP: 5,
    TypeOrder.BSON_TIMESTAMP: 6,
    TypeOrder.STRING: 7,
    TypeOrder.BLOB: 8,
    TypeOrder.BSON_BINARY: 9,
    TypeOrder.REF: 10,
    TypeOrder.BSON_OBJECT_ID: 11,
    TypeOrder.GEO_POINT: 12,
    TypeOrder.BSON_REGEX: 13,
    TypeOrder.ARRAY: 14,
    TypeOrder.VECTOR: 15,
    TypeOrder.OBJECT: 16,
    TypeOrder.MAX_KEY: 17,
}


class Order(object):
    """Order implements the ordering semantics of the backend."""

    @classmethod
    def compare(cls, left, right) -> int:
        left_canon = _extract_canonical_value(left)
        right_canon = _extract_canonical_value(right)

        left_type = TypeOrder.from_value(left_canon)
        right_type = TypeOrder.from_value(right_canon)

        if left_type != right_type:
            left_rank = _TYPE_ORDER_MAP[left_type]
            right_rank = _TYPE_ORDER_MAP[right_type]
            return (left_rank > right_rank) - (left_rank < right_rank)

        if left_type in (TypeOrder.MIN_KEY, TypeOrder.NULL, TypeOrder.MAX_KEY):
            return 0
        elif left_type == TypeOrder.BOOLEAN:
            return cls._compare_to(left_canon, right_canon)
        elif left_type == TypeOrder.NUMBER:
            return cls.compare_numbers(left_canon, right_canon)
        elif left_type == TypeOrder.TIMESTAMP:
            return cls.compare_timestamps(left_canon, right_canon)
        elif left_type == TypeOrder.BSON_TIMESTAMP:
            return cls.compare_bson_timestamps(left_canon, right_canon)
        elif left_type == TypeOrder.STRING:
            return cls._compare_to(left_canon, right_canon)
        elif left_type == TypeOrder.BLOB:
            return cls._compare_to(left_canon, right_canon)
        elif left_type == TypeOrder.BSON_BINARY:
            return cls.compare_bson_binary(left_canon, right_canon)
        elif left_type == TypeOrder.REF:
            return cls.compare_resource_paths(left_canon, right_canon)
        elif left_type == TypeOrder.BSON_OBJECT_ID:
            return cls._compare_to(left_canon.value, right_canon.value)
        elif left_type == TypeOrder.GEO_POINT:
            return cls.compare_geo_points(left_canon, right_canon)
        elif left_type == TypeOrder.BSON_REGEX:
            return cls.compare_bson_regex(left_canon, right_canon)
        elif left_type == TypeOrder.ARRAY:
            return cls.compare_arrays(left_canon, right_canon)
        elif left_type == TypeOrder.VECTOR:
            return cls.compare_vectors(left_canon, right_canon)
        elif left_type == TypeOrder.OBJECT:
            return cls.compare_objects(left_canon, right_canon)
        else:
            raise ValueError(f"Unknown TypeOrder {left_type}")

    @staticmethod
    def _to_decimal_or_nan(val) -> Any:
        if isinstance(val, BSONDecimal128):
            try:
                return val.to_decimal()
            except (decimal.DecimalException, ArithmeticError):
                return None
        if isinstance(val, float):
            if math.isnan(val):
                return "NaN"
            return decimal.Decimal(str(val))
        if isinstance(val, BSONInt32):
            return decimal.Decimal(val.value)
        if isinstance(val, int):
            return decimal.Decimal(val)
        if isinstance(val, str):
            try:
                return decimal.Decimal(val)
            except Exception:
                return None
        if isinstance(val, decimal.Decimal):
            return val
        return None

    @staticmethod
    def compare_numbers(left, right) -> int:
        d_left = Order._to_decimal_or_nan(left)
        d_right = Order._to_decimal_or_nan(right)

        left_is_nan = d_left == "NaN" or (
            isinstance(d_left, decimal.Decimal) and d_left.is_nan()
        )
        right_is_nan = d_right == "NaN" or (
            isinstance(d_right, decimal.Decimal) and d_right.is_nan()
        )

        if left_is_nan and right_is_nan:
            return 0
        if left_is_nan:
            return -1
        if right_is_nan:
            return 1

        if d_left is None or d_right is None:
            return 0

        if d_left == d_right:
            return 0
        return 1 if d_left > d_right else -1

    @staticmethod
    def _extract_ts_seconds_nanos(ts) -> Tuple[int, int]:
        if hasattr(ts, "seconds") and hasattr(ts, "nanos"):
            return (getattr(ts, "seconds", 0) or 0, getattr(ts, "nanos", 0) or 0)
        if isinstance(ts, DatetimeWithNanoseconds):
            ts_pb = ts.timestamp_pb()
            return (ts_pb.seconds or 0, ts_pb.nanos or 0)
        if isinstance(ts, datetime.datetime):
            dt_seconds = int(ts.timestamp())
            dt_nanos = ts.microsecond * 1000
            return (dt_seconds, dt_nanos)
        return (0, 0)

    @staticmethod
    def compare_timestamps(left, right) -> int:
        s1, n1 = Order._extract_ts_seconds_nanos(left)
        s2, n2 = Order._extract_ts_seconds_nanos(right)
        sec_cmp = Order._compare_to(s1, s2)
        if sec_cmp != 0:
            return sec_cmp
        return Order._compare_to(n1, n2)

    @staticmethod
    def compare_bson_timestamps(left: BSONTimestamp, right: BSONTimestamp) -> int:
        sec_cmp = Order._compare_to(left.seconds, right.seconds)
        if sec_cmp != 0:
            return sec_cmp
        return Order._compare_to(left.increment, right.increment)

    @staticmethod
    def compare_bson_binary(left: BSONBinary, right: BSONBinary) -> int:
        data_cmp = Order._compare_to(left.data, right.data)
        if data_cmp != 0:
            return data_cmp
        return Order._compare_to(left.subtype, right.subtype)

    @staticmethod
    def compare_resource_paths(left, right) -> int:
        p_left = (
            left.path
            if hasattr(left, "path")
            else (left.value if hasattr(left, "value") else str(left))
        )
        p_right = (
            right.path
            if hasattr(right, "path")
            else (right.value if hasattr(right, "value") else str(right))
        )

        left_segments = p_left.split("/")
        right_segments = p_right.split("/")
        shorter = min(len(left_segments), len(right_segments))
        for i in range(shorter):
            if left_segments[i] < right_segments[i]:
                return -1
            if left_segments[i] > right_segments[i]:
                return 1

        left_length = len(p_left)
        right_length = len(p_right)
        return (left_length > right_length) - (left_length < right_length)

    @staticmethod
    def compare_geo_points(left: GeoPoint, right: GeoPoint) -> int:
        cmp = (left.latitude > right.latitude) - (left.latitude < right.latitude)
        if cmp != 0:
            return cmp
        return (left.longitude > right.longitude) - (left.longitude < right.longitude)

    @staticmethod
    def compare_bson_regex(left: BSONRegex, right: BSONRegex) -> int:
        pat_cmp = Order._compare_to(left.pattern, right.pattern)
        if pat_cmp != 0:
            return pat_cmp
        return Order._compare_to(left.options, right.options)

    @staticmethod
    def compare_arrays(left: list, right: list) -> int:
        length = min(len(left), len(right))
        for i in range(length):
            cmp = Order.compare(left[i], right[i])
            if cmp != 0:
                return cmp
        return Order._compare_to(len(left), len(right))

    @staticmethod
    def compare_vectors(left: Vector, right: Vector) -> int:
        l_vals = list(left) if isinstance(left, (Vector, list, tuple)) else []
        r_vals = list(right) if isinstance(right, (Vector, list, tuple)) else []
        if len(l_vals) != len(r_vals):
            return Order._compare_to(len(l_vals), len(r_vals))
        return Order.compare_arrays(l_vals, r_vals)

    @staticmethod
    def compare_objects(left: dict, right: dict) -> int:
        def key_sort_tuple(k):
            k_canon = _extract_canonical_value(k)
            k_type = TypeOrder.from_value(k_canon)
            return (_TYPE_ORDER_MAP[k_type], str(k_canon))

        left_keys = sorted(left.keys(), key=key_sort_tuple)
        right_keys = sorted(right.keys(), key=key_sort_tuple)

        for lk, rk in zip(left_keys, right_keys):
            key_cmp = Order.compare(lk, rk)
            if key_cmp != 0:
                return key_cmp
            val_cmp = Order.compare(left[lk], right[rk])
            if val_cmp != 0:
                return val_cmp

        return Order._compare_to(len(left), len(right))

    @staticmethod
    def compare_blobs(left, right) -> int:
        left_bytes = getattr(left, "bytes_value", left)
        right_bytes = getattr(right, "bytes_value", right)
        return Order._compare_to(left_bytes, right_bytes)

    @staticmethod
    def compare_doubles(left, right) -> int:
        return Order.compare_numbers(left, right)

    @staticmethod
    def _compare_to(left, right) -> int:
        return (left > right) - (left < right)
