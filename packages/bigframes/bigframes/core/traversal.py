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

import bigframes.core.nodes as nodes


def is_trivially_executable(node: nodes.BigFrameNode) -> bool:
    if local_only(node):
        return True
    children_trivial = all(is_trivially_executable(child) for child in node.child_nodes)
    self_trivial = (not node.non_local) and (node.row_preserving)
    return children_trivial and self_trivial


def local_only(node: nodes.BigFrameNode) -> bool:
    return all(isinstance(node, nodes.ReadLocalNode) for node in node.roots)
