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

from __future__ import annotations

import typing
from typing import Generic, TypeVar

from bigframes import operations as ops

T = TypeVar("T")


class OpRegistration(Generic[T]):
    _registered_ops: dict[str, T] = {}

    def register(
        self, op: ops.ScalarOp | type[ops.ScalarOp]
    ) -> typing.Callable[[T], T]:
        key = typing.cast(str, op.name)

        def decorator(item: T):
            if key in self._registered_ops:
                raise ValueError(f"{key} is already registered")
            self._registered_ops[key] = item
            return item

        return decorator

    def __getitem__(self, key: str | ops.ScalarOp) -> T:
        if isinstance(key, ops.ScalarOp):
            return self._registered_ops[key.name]
        return self._registered_ops[key]
