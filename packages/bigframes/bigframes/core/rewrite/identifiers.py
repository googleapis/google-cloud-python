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
from __future__ import annotations

import typing

from bigframes.core import identifiers, nodes


# TODO: May as well just outright remove selection nodes in this process.
def remap_variables(
    root: nodes.BigFrameNode,
    id_generator: typing.Iterator[identifiers.ColumnId],
) -> typing.Tuple[
    nodes.BigFrameNode,
    dict[identifiers.ColumnId, identifiers.ColumnId],
]:
    """Remaps `ColumnId`s in the BFET to produce deterministic and sequential UIDs.

    Note: this will convert a DAG to a tree.
    """
    child_replacement_map = dict()
    ref_mapping = dict()
    # Sequential ids are assigned bottom-up left-to-right
    for child in root.child_nodes:
        new_child, child_var_mapping = remap_variables(child, id_generator=id_generator)
        child_replacement_map[child] = new_child
        ref_mapping.update(child_var_mapping)

    # This is actually invalid until we've replaced all of children, refs and var defs
    with_new_children = root.transform_children(
        lambda node: child_replacement_map[node]
    )

    with_new_refs = with_new_children.remap_refs(ref_mapping)

    node_var_mapping = {old_id: next(id_generator) for old_id in root.node_defined_ids}
    with_new_vars = with_new_refs.remap_vars(node_var_mapping)
    with_new_vars._validate()

    return (
        with_new_vars,
        node_var_mapping
        if root.defines_namespace
        else (ref_mapping | node_var_mapping),
    )
