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

from sqlglot import expressions as sge

from bigframes.operations import aggregations as agg_ops

# We should've been more specific about input types. Unfortunately,
# MyPy doesn't support more rigorous checks.
CompilationFunc = typing.Callable[..., sge.Expression]


class OpRegistration:
    def __init__(self) -> None:
        self._registered_ops: dict[str, CompilationFunc] = {}

    def register(
        self, op: agg_ops.WindowOp | type[agg_ops.WindowOp]
    ) -> typing.Callable[[CompilationFunc], CompilationFunc]:
        def decorator(item: CompilationFunc):
            def arg_checker(*args, **kwargs):
                if not isinstance(args[0], agg_ops.WindowOp):
                    raise ValueError(
                        "The first parameter must be a window operator. "
                        f"Got {type(args[0])}"
                    )
                return item(*args, **kwargs)

            key = str(op)
            if key in self._registered_ops:
                raise ValueError(f"{key} is already registered")
            self._registered_ops[key] = item
            return arg_checker

        return decorator

    def __getitem__(self, op: str | agg_ops.WindowOp) -> CompilationFunc:
        key = op if isinstance(op, type) else type(op)
        if str(key) not in self._registered_ops:
            raise ValueError(f"{key} is not registered")
        return self._registered_ops[str(key)]
