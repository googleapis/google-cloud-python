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
import bigframes.core.nodes as nodes
import bigframes.core.rewrite.slices


def test_rewrite_noop_slice(leaf):
    slice = nodes.SliceNode(leaf, None, None)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert result == leaf


def test_rewrite_reverse_slice(leaf):
    slice = nodes.SliceNode(leaf, None, None, -1)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert result == nodes.ReversedNode(leaf)


def test_rewrite_filter_slice(leaf):
    slice = nodes.SliceNode(leaf, None, 2)
    result = bigframes.core.rewrite.slices.rewrite_slice(slice)
    assert list(result.fields) == list(leaf.fields)
    assert isinstance(result.child, nodes.FilterNode)
