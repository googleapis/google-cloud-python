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

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import substrait.algebra_pb2 as algebra_pb2
import substrait.plan_pb2 as plan_pb2
from google.protobuf import json_format

from bigframes.core import bigframe_node, nodes
import bigframes.core.expression as ex
import pandas as pd


class SubstraitCompiler:
    """
    Compiles BigFrameNode plans to Substrait schema (JSON representation).
    """

    def compile(self, plan: bigframe_node.BigFrameNode) -> Optional[bytes]:
        """
        Compiles a BigFrameNode to Substrait bytes (JSON encoded via protobuf).
        """
        if not self.can_compile(plan):
            return None

        plan_dict = self._compile_node(plan)
        
        pb_plan = plan_pb2.Plan()
        pb_plan.version.minor_number = 42
        
        plan_rel = pb_plan.relations.add()
        json_format.ParseDict(plan_dict, plan_rel.root.input)
        
        plan_rel.root.names.extend([item.column for item in plan.schema.items])
        
        extensions = [
            ("add", 1),
            ("sub", 2),
            ("mul", 3),
            ("div", 4),
            ("eq", 5),
            ("ne", 6),
            ("lt", 7),
            ("gt", 8),
            ("le", 9),
            ("ge", 10),
        ]
        for name, anchor in extensions:
             ext = pb_plan.extensions.add()
             ext.extension_function.function_anchor = anchor
             ext.extension_function.name = name
             
        return json_format.MessageToJson(pb_plan).encode('utf-8')

    def can_compile(self, plan: bigframe_node.BigFrameNode) -> bool:
        """
        Checks if the plan can be compiled to Substrait.
        For the skeleton, we support ReadLocalNode, SelectionNode, and FilterNode.
        """
        supported_nodes = (
            nodes.ReadLocalNode,
            nodes.SelectionNode,
            nodes.FilterNode,
            nodes.SliceNode,
            nodes.ProjectionNode,
            nodes.JoinNode,
            nodes.AggregateNode,
        )
        return all(isinstance(node, supported_nodes) for node in plan.unique_nodes())

    def _compile_node(self, node: bigframe_node.BigFrameNode) -> Dict[str, Any]:
        if isinstance(node, nodes.ReadLocalNode):
            return self._compile_read(node)
        elif isinstance(node, nodes.SelectionNode):
            return self._compile_selection(node)
        elif isinstance(node, nodes.FilterNode):
            return self._compile_filter(node)
        elif isinstance(node, nodes.SliceNode):
            return self._compile_slice(node)
        elif isinstance(node, nodes.ProjectionNode):
            return self._compile_projection(node)
        elif isinstance(node, nodes.JoinNode):
            return self._compile_join(node)
        elif isinstance(node, nodes.AggregateNode):
            return self._compile_aggregate(node)
        else:
            raise NotImplementedError(f"Node type {type(node)} not supported in Substrait compiler yet")

    def _compile_read(self, node: nodes.ReadLocalNode) -> Dict[str, Any]:
        table_name = f"table_{node.local_data_source.id.hex}"
        
        rel = algebra_pb2.Rel()
        read_rel = rel.read
        read_rel.named_table.names.append(table_name)
        
        schema_dict = self._convert_schema(node.local_data_source.schema)
        json_format.ParseDict(schema_dict, read_rel.base_schema)
        
        return json_format.MessageToDict(rel, preserving_proto_field_name=True)

    def _compile_selection(self, node: nodes.SelectionNode) -> Dict[str, Any]:
        # Selection usually maps to ProjectRel or FilterRel depending on if it filters or just selects columns.
        # If it's just column selection (Projection), it's a ProjectRel.
        # Let's assume it's a ProjectRel for now.
        input_rel = self._compile_node(node.child)
        return {
            "project": {
                "input": input_rel,
                "expressions": [
                    # Skeletal expression mapping
                    {"selection": {"direct_reference": {"struct_field": {"field": i}}}} 
                    for i in range(len(node.schema))
                ]
            }
        }

    def _compile_filter(self, node: nodes.FilterNode) -> Dict[str, Any]:
        input_rel = self._compile_node(node.child)
        condition_rel = self._compile_expression(node.condition, node.child)
        return {
            "filter": {
                "input": input_rel,
                "condition": condition_rel
            }
        }

    def _compile_slice(self, node: nodes.SliceNode) -> Dict[str, Any]:
        input_rel = self._compile_node(node.child)
        count = node.stop if node.stop is not None else -1
        offset = node.start if node.start is not None else 0
        
        return {
            "fetch": {
                "input": input_rel,
                "offset": offset,
                "count": count
            }
        }

    def _compile_projection(self, node: nodes.ProjectionNode) -> Dict[str, Any]:
        input_rel_dict = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        project_rel = rel.project
        
        json_format.ParseDict(input_rel_dict, project_rel.input)
        
        # DataFusion ProjectRel seems to be additive (appends to input).
        # So we don't need to add passthrough expressions for input fields.
        
        # Add new assignments
        for expr, _ in node.assignments:
             expr_dict = self._compile_expression(expr, node.child)
             expr_pb = project_rel.expressions.add()
             json_format.ParseDict(expr_dict, expr_pb)
             
        return json_format.MessageToDict(rel, preserving_proto_field_name=True)

    def _compile_join(self, node: nodes.JoinNode) -> Dict[str, Any]:
        left_rel = self._compile_node(node.left_child)
        right_rel = self._compile_node(node.right_child)
        
        type_map = {
            "inner": "JOIN_TYPE_INNER",
            "left": "JOIN_TYPE_LEFT",
            "right": "JOIN_TYPE_RIGHT",
            "outer": "JOIN_TYPE_OUTER",
            "cross": "JOIN_TYPE_CROSS",
        }
        join_type = type_map.get(node.type, "JOIN_TYPE_UNSPECIFIED")
        
        left_len = len(node.left_child.schema)
        
        eq_expressions = []
        for left_deref, right_deref in node.conditions:
             left_idx = list(node.left_child.ids).index(left_deref.id)
             right_idx = list(node.right_child.ids).index(right_deref.id) + left_len
             
             eq_expressions.append({
                 "scalar_function": {
                     "function_reference": 0,
                     "arguments": [
                         {"value": {"selection": {"direct_reference": {"struct_field": {"field": left_idx}}}}},
                         {"value": {"selection": {"direct_reference": {"struct_field": {"field": right_idx}}}}}
                     ]
                 }
             })
             
        if len(eq_expressions) > 1:
             expr = eq_expressions[0]
        elif len(eq_expressions) == 1:
             expr = eq_expressions[0]
        else:
             expr = {"literal": {"boolean": True}}
             
        return {
            "join": {
                "left": left_rel,
                "right": right_rel,
                "expression": expr,
                "type": join_type
            }
        }

    def _compile_aggregate(self, node: nodes.AggregateNode) -> Dict[str, Any]:
        input_rel = self._compile_node(node.child)
        
        groupings = []
        grouping_expressions = []
        for deref in node.by_column_ids:
             idx = list(node.child.ids).index(deref.id)
             grouping_expressions.append({"selection": {"direct_reference": {"struct_field": {"field": idx}}}})
        if grouping_expressions:
             groupings.append({"grouping_expressions": grouping_expressions})
             
        measures = []
        for agg, _ in node.aggregations:
             func_ref = 1 if "Sum" in type(agg).__name__ else 2
             args = []
             if hasattr(agg, "column_references"):
                  for col_id in agg.column_references:
                       try:
                           idx = list(node.child.ids).index(col_id)
                           args.append({"value": {"selection": {"direct_reference": {"struct_field": {"field": idx}}}}})
                       except ValueError:
                           pass
             measures.append({
                 "measure": {
                     "function_reference": func_ref,
                     "arguments": args
                 }
             })
             
        return {
            "aggregate": {
                "input": input_rel,
                "groupings": groupings,
                "measures": measures
            }
        }

    def _compile_expression(self, expr: ex.Expression, child: nodes.BigFrameNode) -> Dict[str, Any]:
        if isinstance(expr, ex.ScalarConstantExpression):
             val = expr.value
             if isinstance(val, int):
                  return {"literal": {"i64": val}}
             elif isinstance(val, float):
                  return {"literal": {"fp64": val}}
             elif isinstance(val, str):
                  return {"literal": {"string": val}}
             elif pd.isna(val):
                  return {"literal": {"null": {"varchar": {"length": 0}}}}
             else:
                  return {"literal": {"string": str(val)}}
                  
        elif isinstance(expr, ex.DerefOp):
             try:
                  # print(f"DerefOp: id={expr.id}, child.ids={list(child.ids)}") # Debug
                  idx = list(child.ids).index(expr.id)
                  return {"selection": {"direct_reference": {"struct_field": {"field": idx}}}}
             except ValueError:
                  raise ValueError(f"Column {expr.id} not found in child schema")
                  
        elif isinstance(expr, ex.OpExpression):
             op_name = expr.op.name
             op_mapping = {
                 "add": 1,
                 "sub": 2,
                 "mul": 3,
                 "div": 4,
                 "eq": 5,
                 "ne": 6,
                 "lt": 7,
                 "gt": 8,
                 "le": 9,
                 "ge": 10,
             }
             if op_name not in op_mapping:
                  raise NotImplementedError(f"Operation {op_name} not supported in Substrait compiler yet")
             func_ref = op_mapping[op_name]
             
             args = [self._compile_expression(arg, child) for arg in expr.inputs]
             return {
                 "scalar_function": {
                     "function_reference": func_ref,
                     "arguments": [{"value": arg} for arg in args]
                 }
             }
        else:
             raise NotImplementedError(f"Expression type {type(expr)} not supported in Substrait compiler yet")

    def _convert_schema(self, schema: Any) -> Dict[str, Any]:
        # Convert bigframes schema to Substrait Type.NamedStruct
        fields = []
        types = []
        for item in schema.items:
             col = item.column
             name = col.name if hasattr(col, "name") else str(col)
             fields.append(name)
             types.append(self._convert_type(item.dtype))
             
        return {
            "names": fields,
            "struct": {"types": types}
        }

    def _convert_type(self, dtype: Any) -> Dict[str, Any]:
        import bigframes.dtypes
        if dtype == bigframes.dtypes.INT_DTYPE:
             return {"i64": {}}
        elif dtype == bigframes.dtypes.FLOAT_DTYPE:
             return {"fp64": {}}
        elif dtype == bigframes.dtypes.BOOL_DTYPE:
             return {"bool": {}}
        elif dtype == bigframes.dtypes.STRING_DTYPE:
             return {"string": {}}
        else:
             # Fallback to string for now
             return {"string": {}}
