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

import itertools
from typing import Sequence, Tuple

import bigframes.core.expression as ex
import bigframes.core.identifiers as ids
import bigframes.core.nodes as nodes
import bigframes.core.pruning as predicate_pruning
import bigframes.core.tree_properties as traversals
import bigframes.dtypes


def session_aware_cache_plan(
    root: nodes.BigFrameNode, session_forest: Sequence[nodes.BigFrameNode]
) -> Tuple[nodes.BigFrameNode, list[ids.ColumnId]]:
    """
    Determines the best node to cache given a target and a list of object roots for objects in a session.

    Returns the node to cache, and optionally a clustering column.
    """
    node_counts = traversals.count_nodes(session_forest)
    # These node types are cheap to re-compute, so it makes more sense to cache their children.
    de_cachable_types = (nodes.FilterNode, nodes.ProjectionNode, nodes.SelectionNode)
    caching_target = cur_node = root
    caching_target_refs = node_counts.get(caching_target, 0)

    filters: list[
        ex.Expression
    ] = []  # accumulate filters into this as traverse downwards
    clusterable_cols: set[ids.ColumnId] = set()
    while isinstance(cur_node, de_cachable_types):
        if isinstance(cur_node, nodes.FilterNode):
            # Filter node doesn't define any variables, so no need to chain expressions
            filters.append(cur_node.predicate)
        elif isinstance(cur_node, nodes.ProjectionNode):
            # Projection defines the variables that are used in the filter expressions, need to substitute variables with their scalar expressions
            # that instead reference variables in the child node.
            bindings = {name: expr for expr, name in cur_node.assignments}
            filters = [
                i.bind_refs(bindings, allow_partial_bindings=True) for i in filters
            ]
        elif isinstance(cur_node, nodes.SelectionNode):
            bindings = {output: input for input, output in cur_node.input_output_pairs}
            filters = [i.bind_refs(bindings) for i in filters]
        else:
            raise ValueError(f"Unexpected de-cached node: {cur_node}")

        cur_node = cur_node.child
        cur_node_refs = node_counts.get(cur_node, 0)
        if cur_node_refs > caching_target_refs:
            caching_target, caching_target_refs = cur_node, cur_node_refs
            cluster_compatible_cols = {
                field.id
                for field in cur_node.fields
                if bigframes.dtypes.is_clusterable(field.dtype)
            }
            # Cluster cols only consider the target object and not other sesssion objects
            clusterable_cols = set(
                itertools.chain.from_iterable(
                    map(
                        lambda f: predicate_pruning.cluster_cols_for_predicate(
                            f, cluster_compatible_cols
                        ),
                        filters,
                    )
                )
            )
    # BQ supports up to 4 cluster columns, just prioritize by alphabetical ordering
    # TODO: Prioritize caching columns by estimated filter selectivity
    return caching_target, sorted(list(clusterable_cols))[:4]
