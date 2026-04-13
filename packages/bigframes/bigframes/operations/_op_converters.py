# Copyright 2024 Google LLC
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

import bigframes.operations as ops


def convert_index(key: int) -> ops.ArrayIndexOp:
    if key < 0:
        raise NotImplementedError("Negative indexing is not supported.")
    return ops.ArrayIndexOp(index=key)


def convert_slice(key: slice) -> ops.ArraySliceOp:
    if key.step is not None and key.step != 1:
        raise NotImplementedError(f"Only a step of 1 is allowed, got {key.step}")

    if (key.start is not None and key.start < 0) or (
        key.stop is not None and key.stop < 0
    ):
        raise NotImplementedError("Slicing with negative numbers is not allowed.")

    return ops.ArraySliceOp(
        start=key.start if key.start is not None else 0,
        stop=key.stop,
        step=key.step,
    )
