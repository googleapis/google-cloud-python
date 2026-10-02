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
"""Single source of truth for which RPCs are routed through the accelerator."""

from __future__ import annotations

# Names mirror the `_DataApiTarget` method names, not the gRPC method names.
# Adding an entry here is not enough on its own: the corresponding method must
# also include a top-of-function branch that dispatches to the accelerator
# service. Keep this set in lockstep with the bundled daemon's capabilities.
_ACCELERATOR_SUPPORTED: frozenset[str] = frozenset({"read_row", "mutate_row"})


def is_supported(method_name: str) -> bool:
    return method_name in _ACCELERATOR_SUPPORTED
