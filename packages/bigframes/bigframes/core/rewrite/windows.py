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

import dataclasses

from bigframes import operations as ops
from bigframes.core import nodes


def rewrite_range_rolling(node: nodes.BigFrameNode) -> nodes.BigFrameNode:
    if not isinstance(node, nodes.WindowOpNode):
        return node

    if not node.window_spec.is_range_bounded:
        return node

    if len(node.window_spec.ordering) != 1:
        raise ValueError(
            "Range rolling should only be performed on exactly one column."
        )

    ordering_expr = node.window_spec.ordering[0]

    new_ordering = dataclasses.replace(
        ordering_expr,
        scalar_expression=ops.UnixMicros().as_expr(ordering_expr.scalar_expression),
    )

    return dataclasses.replace(
        node,
        window_spec=dataclasses.replace(node.window_spec, ordering=(new_ordering,)),
    )
