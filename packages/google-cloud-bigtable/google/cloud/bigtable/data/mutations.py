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
#
from __future__ import annotations
from typing import Any
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
from sys import getsizeof

import google.cloud.bigtable_v2.types.bigtable as types_pb
import google.cloud.bigtable_v2.types.data as data_pb

from google.cloud.bigtable.data.read_modify_write_rules import _MAX_INCREMENT_VALUE


# special value for SetCell mutation timestamps. If set, server will assign a timestamp
_SERVER_SIDE_TIMESTAMP = -1

# mutation entries above this should be rejected
_MUTATE_ROWS_REQUEST_MUTATION_LIMIT = 100_000


class Mutation(ABC):
    """Model class for mutations"""

    @abstractmethod
    def _to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    def _to_pb(self) -> data_pb.Mutation:
        """
        Convert the mutation to protobuf
        """
        return data_pb.Mutation(**self._to_dict())

    def is_idempotent(self) -> bool:
        """
        Check if the mutation is idempotent
        If false, the mutation will not be retried
        """
        return True

    def __str__(self) -> str:
        return str(self._to_dict())

    def size(self) -> int:
        """
        Get the size of the mutation in bytes
        """
        return getsizeof(self._to_dict())

    @classmethod
    def _from_dict(cls, input_dict: dict[str, Any]) -> Mutation:
        instance: Mutation | None = None
        try:
            if "set_cell" in input_dict:
                details = input_dict["set_cell"]
                instance = SetCell(
                    details["family_name"],
                    details["column_qualifier"],
                    details["value"],
                    details["timestamp_micros"],
                )
            elif "delete_from_column" in input_dict:
                details = input_dict["delete_from_column"]
                time_range = details.get("time_range", {})
                start = time_range.get("start_timestamp_micros", None)
                end = time_range.get("end_timestamp_micros", None)
                instance = DeleteRangeFromColumn(
                    details["family_name"], details["column_qualifier"], start, end
                )
            elif "delete_from_family" in input_dict:
                details = input_dict["delete_from_family"]
                instance = DeleteAllFromFamily(details["family_name"])
            elif "delete_from_row" in input_dict:
                instance = DeleteAllFromRow()
        except KeyError as e:
            raise ValueError("Invalid mutation dictionary") from e
        if instance is None:
            raise ValueError("No valid mutation found")
        if not issubclass(instance.__class__, cls):
            raise ValueError("Mutation type mismatch")
        return instance


class SetCell(Mutation):
    def __init__(
        self,
        family: str,
        qualifier: bytes | str,
        new_value: bytes | str | int,
        timestamp_micros: int | None = None,
    ):
        """
        Mutation to set the value of a cell

        Args:
          - family: The name of the column family to which the new cell belongs.
          - qualifier: The column qualifier of the new cell.
          - new_value: The value of the new cell. str or int input will be converted to bytes
          - timestamp_micros: The timestamp of the new cell. If None, the current timestamp will be used.
              Timestamps will be sent with milisecond-percision. Extra precision will be truncated.
              If -1, the server will assign a timestamp. Note that SetCell mutations with server-side
              timestamps are non-idempotent operations and will not be retried.
        """
        qualifier = qualifier.encode() if isinstance(qualifier, str) else qualifier
        if not isinstance(qualifier, bytes):
            raise TypeError("qualifier must be bytes or str")
        if isinstance(new_value, str):
            new_value = new_value.encode()
        elif isinstance(new_value, int):
            if abs(new_value) > _MAX_INCREMENT_VALUE:
                raise ValueError(
                    "int values must be between -2**63 and 2**63 (64-bit signed int)"
                )
            new_value = new_value.to_bytes(8, "big", signed=True)
        if not isinstance(new_value, bytes):
            raise TypeError("new_value must be bytes, str, or int")
        if timestamp_micros is None:
            # use current timestamp, with milisecond precision
            timestamp_micros = time.time_ns() // 1000
            timestamp_micros = timestamp_micros - (timestamp_micros % 1000)
        if timestamp_micros < _SERVER_SIDE_TIMESTAMP:
            raise ValueError(
                f"timestamp_micros must be positive (or {_SERVER_SIDE_TIMESTAMP} for server-side timestamp)"
            )
        self.family = family
        self.qualifier = qualifier
        self.new_value = new_value
        self.timestamp_micros = timestamp_micros

    def _to_dict(self) -> dict[str, Any]:
        """Convert the mutation to a dictionary representation"""
        return {
            "set_cell": {
                "family_name": self.family,
                "column_qualifier": self.qualifier,
                "timestamp_micros": self.timestamp_micros,
                "value": self.new_value,
            }
        }

    def is_idempotent(self) -> bool:
        """Check if the mutation is idempotent"""
        return self.timestamp_micros != _SERVER_SIDE_TIMESTAMP


@dataclass
class DeleteRangeFromColumn(Mutation):
    family: str
    qualifier: bytes
    # None represents 0
    start_timestamp_micros: int | None = None
    # None represents infinity
    end_timestamp_micros: int | None = None

    def __post_init__(self):
        if (
            self.start_timestamp_micros is not None
            and self.end_timestamp_micros is not None
            and self.start_timestamp_micros > self.end_timestamp_micros
        ):
            raise ValueError("start_timestamp_micros must be <= end_timestamp_micros")

    def _to_dict(self) -> dict[str, Any]:
        timestamp_range = {}
        if self.start_timestamp_micros is not None:
            timestamp_range["start_timestamp_micros"] = self.start_timestamp_micros
        if self.end_timestamp_micros is not None:
            timestamp_range["end_timestamp_micros"] = self.end_timestamp_micros
        return {
            "delete_from_column": {
                "family_name": self.family,
                "column_qualifier": self.qualifier,
                "time_range": timestamp_range,
            }
        }


@dataclass
class DeleteAllFromFamily(Mutation):
    family_to_delete: str

    def _to_dict(self) -> dict[str, Any]:
        return {
            "delete_from_family": {
                "family_name": self.family_to_delete,
            }
        }


@dataclass
class DeleteAllFromRow(Mutation):
    def _to_dict(self) -> dict[str, Any]:
        return {
            "delete_from_row": {},
        }


class RowMutationEntry:
    def __init__(self, row_key: bytes | str, mutations: Mutation | list[Mutation]):
        if isinstance(row_key, str):
            row_key = row_key.encode("utf-8")
        if isinstance(mutations, Mutation):
            mutations = [mutations]
        if len(mutations) == 0:
            raise ValueError("mutations must not be empty")
        elif len(mutations) > _MUTATE_ROWS_REQUEST_MUTATION_LIMIT:
            raise ValueError(
                f"entries must have <= {_MUTATE_ROWS_REQUEST_MUTATION_LIMIT} mutations"
            )
        self.row_key = row_key
        self.mutations = tuple(mutations)

    def _to_dict(self) -> dict[str, Any]:
        return {
            "row_key": self.row_key,
            "mutations": [mutation._to_dict() for mutation in self.mutations],
        }

    def _to_pb(self) -> types_pb.MutateRowsRequest.Entry:
        return types_pb.MutateRowsRequest.Entry(
            row_key=self.row_key,
            mutations=[mutation._to_pb() for mutation in self.mutations],
        )

    def is_idempotent(self) -> bool:
        """Check if the mutation is idempotent"""
        return all(mutation.is_idempotent() for mutation in self.mutations)

    def size(self) -> int:
        """
        Get the size of the mutation in bytes
        """
        return getsizeof(self._to_dict())

    @classmethod
    def _from_dict(cls, input_dict: dict[str, Any]) -> RowMutationEntry:
        return RowMutationEntry(
            row_key=input_dict["row_key"],
            mutations=[
                Mutation._from_dict(mutation) for mutation in input_dict["mutations"]
            ],
        )
