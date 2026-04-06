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

from functools import singledispatchmethod
import json
from typing import Any, Dict, Optional, Sequence

import substrait.algebra_pb2 as algebra_pb2
import substrait.plan_pb2 as plan_pb2
import substrait.type_pb2 as type_pb2
from google.protobuf import json_format

from bigframes.core import bigframe_node, nodes
import bigframes.core.expression as ex
import pandas as pd
import bigframes.operations.numeric_ops as numeric_ops
import bigframes.operations.comparison_ops as comparison_ops


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

        pb_rel = self._compile_node(plan)
        
        pb_plan = plan_pb2.Plan()
        pb_plan.version.minor_number = 42
        
        plan_rel = pb_plan.relations.add()
        plan_rel.root.input.CopyFrom(pb_rel)
        
        plan_rel.root.names.extend([item.column for item in plan.schema.items])
        
        for name, anchor in self._EXTENSIONS.items():
             ext = pb_plan.extensions.add()
             ext.extension_function.function_anchor = anchor
             ext.extension_function.name = name
             
        return pb_plan.SerializeToString()

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
        return isinstance(plan, supported_nodes)

    def _compile_node(self, node: bigframe_node.BigFrameNode) -> algebra_pb2.Rel:
        if isinstance(node, nodes.ReadLocalNode):
             return self._compile_read(node)
        elif isinstance(node, nodes.SelectionNode):
             return self._compile_selection(node)
        elif isinstance(node, nodes.FilterNode):
             return self._compile_filter(node)
        elif isinstance(node, nodes.ProjectionNode):
             return self._compile_projection(node)
        elif isinstance(node, nodes.JoinNode):
             return self._compile_join(node)
        elif isinstance(node, nodes.AggregateNode):
             return self._compile_aggregate(node)
        else:
             raise NotImplementedError(f"Node type {type(node)} not supported in Substrait compiler yet")

    def _compile_read(self, node: nodes.ReadLocalNode) -> algebra_pb2.Rel:
        table_name = f"table_{node.local_data_source.id.hex}"
        
        rel = algebra_pb2.Rel()
        read_rel = rel.read
        read_rel.named_table.names.append(table_name)
        
        schema_dict = self._convert_schema(node.local_data_source.schema)
        json_format.ParseDict(schema_dict, read_rel.base_schema)
        
        return rel

    def _compile_selection(self, node: nodes.SelectionNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        project_rel = rel.project
        project_rel.input.CopyFrom(input_rel)
        
        child_ids = list(node.child.ids)
        num_exprs = 0
        for aliased_ref in node.input_output_pairs:
             source_id = aliased_ref.ref.id
             idx = child_ids.index(source_id)
             expr = project_rel.expressions.add()
             expr.selection.direct_reference.struct_field.field = idx
             num_exprs += 1
             
        project_rel.common.emit.output_mapping.extend([len(child_ids) + i for i in range(num_exprs)])
        
        return rel

    def _compile_filter(self, node: nodes.FilterNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        filter_rel = rel.filter
        filter_rel.input.CopyFrom(input_rel)
        
        condition_expr = self._compile_expression(node.predicate, node.child)
        filter_rel.condition.CopyFrom(condition_expr)
        
        return rel


    def _compile_projection(self, node: nodes.ProjectionNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        project_rel = rel.project
        project_rel.input.CopyFrom(input_rel)
        
        for expr, _ in node.assignments:
             expr_pb = self._compile_expression(expr, node.child)
             project_rel.expressions.add().CopyFrom(expr_pb)
             
        return rel

    def _compile_join(self, node: nodes.JoinNode) -> algebra_pb2.Rel:
        left_rel = self._compile_node(node.left_child)
        right_rel = self._compile_node(node.right_child)
        
        rel = algebra_pb2.Rel()
        join_rel = rel.join
        
        join_rel.left.CopyFrom(left_rel)
        join_rel.right.CopyFrom(right_rel)
        
        type_map = {
            "inner": algebra_pb2.JoinRel.JOIN_TYPE_INNER,
            "left": algebra_pb2.JoinRel.JOIN_TYPE_LEFT,
            "right": algebra_pb2.JoinRel.JOIN_TYPE_RIGHT,
            "outer": algebra_pb2.JoinRel.JOIN_TYPE_OUTER,
        }
        join_rel.type = type_map.get(node.type, algebra_pb2.JoinRel.JOIN_TYPE_UNSPECIFIED)
        
        left_len = len(node.left_child.schema)
        
        eq_expressions = []
        for left_deref, right_deref in node.conditions:
             left_idx = list(node.left_child.ids).index(left_deref.id)
             right_idx = list(node.right_child.ids).index(right_deref.id) + left_len
             
             eq_expr = algebra_pb2.Expression()
             eq_expr.scalar_function.function_reference = 5 # equal
             
             arg1 = eq_expr.scalar_function.arguments.add()
             arg1.value.selection.direct_reference.struct_field.field = left_idx
             
             arg2 = eq_expr.scalar_function.arguments.add()
             arg2.value.selection.direct_reference.struct_field.field = right_idx
             
             eq_expressions.append(eq_expr)
             
        if len(eq_expressions) > 1:
             expr = eq_expressions[0]
             for e in eq_expressions[1:]:
                  and_expr = algebra_pb2.Expression()
                  and_expr.scalar_function.function_reference = 13 # and
                  and_expr.scalar_function.arguments.add().value.CopyFrom(expr)
                  and_expr.scalar_function.arguments.add().value.CopyFrom(e)
                  expr = and_expr
        elif len(eq_expressions) == 1:
             expr = eq_expressions[0]
        else:
             expr = algebra_pb2.Expression()
             expr.literal.boolean = True
             
        join_rel.expression.CopyFrom(expr)
        
        return rel

    def _compile_aggregate(self, node: nodes.AggregateNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        agg_rel = rel.aggregate
        agg_rel.input.CopyFrom(input_rel)
        
        if node.by_column_ids:
             grouping = agg_rel.groupings.add()
             for deref in node.by_column_ids:
                  idx = list(node.child.ids).index(deref.id)
                  expr = grouping.grouping_expressions.add()
                  expr.selection.direct_reference.struct_field.field = idx
                  
        import bigframes.operations.aggregations as agg_ops
        for agg, _ in node.aggregations:
             if isinstance(agg.op, agg_ops.SumOp):
                  func_ref = 11
             elif isinstance(agg.op, agg_ops.MaxOp):
                  func_ref = 12
             else:
                  raise NotImplementedError(f"Aggregation {type(agg.op)} not supported in Substrait compiler yet")
                  
             measure = agg_rel.measures.add()
             measure.measure.function_reference = func_ref
             
             if hasattr(agg, "column_references"):
                  for col_id in agg.column_references:
                       try:
                           idx = list(node.child.ids).index(col_id)
                           arg = measure.measure.arguments.add()
                           arg.value.selection.direct_reference.struct_field.field = idx
                       except ValueError:
                           pass
                           
        return rel

    _EXTENSIONS = {
        "add": 1,
        "subtract": 2,
        "multiply": 3,
        "divide": 4,
        "equal": 5,
        "ne": 6,
        "lt": 7,
        "gt": 8,
        "lte": 9,
        "gte": 10,
        "sum": 11,
        "max": 12,
        "and": 13,
    }

    _OP_TO_EXTENSION = {
        numeric_ops.AddOp: "add",
        numeric_ops.SubOp: "subtract",
        numeric_ops.MulOp: "multiply",
        numeric_ops.DivOp: "divide",
        comparison_ops.EqOp: "equal",
        comparison_ops.NeOp: "ne",
        comparison_ops.LtOp: "lt",
        comparison_ops.GtOp: "gt",
        comparison_ops.LeOp: "lte",
        comparison_ops.GeOp: "gte",
    }

    @singledispatchmethod
    def _compile_expression(self, expr: ex.Expression, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         raise NotImplementedError(f"Expression type {type(expr)} not supported in Substrait compiler yet")

    @_compile_expression.register
    def _compile_scalar_constant(self, expr: ex.ScalarConstantExpression, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         val = expr.value
         if isinstance(val, int):
              pb_expr.literal.i64 = val
         elif isinstance(val, float):
              pb_expr.literal.fp64 = val
         elif isinstance(val, str):
              pb_expr.literal.string = val
         elif pd.isna(val):
              pb_expr.literal.null.varchar.length = 0
         else:
              pb_expr.literal.string = str(val)
         return pb_expr

    @_compile_expression.register
    def _compile_deref(self, expr: ex.DerefOp, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         try:
              idx = list(child.ids).index(expr.id)
              pb_expr.selection.direct_reference.struct_field.field = idx
              return pb_expr
         except ValueError:
              raise ValueError(f"Column {expr.id} not found in child schema")

    @_compile_expression.register
    def _compile_op_expr(self, expr: ex.OpExpression, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         return self._compile_op(expr.op, expr.inputs, child)

    @singledispatchmethod
    def _compile_op(self, op: Any, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         raise NotImplementedError(f"Op type {type(op)} not supported in Substrait compiler yet")

    @_compile_op.register(numeric_ops.AddOp)
    @_compile_op.register(numeric_ops.SubOp)
    @_compile_op.register(numeric_ops.MulOp)
    @_compile_op.register(numeric_ops.DivOp)
    @_compile_op.register(comparison_ops.EqOp)
    @_compile_op.register(comparison_ops.NeOp)
    @_compile_op.register(comparison_ops.LtOp)
    @_compile_op.register(comparison_ops.GtOp)
    @_compile_op.register(comparison_ops.LeOp)
    @_compile_op.register(comparison_ops.GeOp)
    def _compile_basic_binops(self, op: Any, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         op_class = type(op)
         ext_name = self._OP_TO_EXTENSION[op_class]
         return self._compile_basic_binop(ext_name, inputs, child)

    def _compile_basic_binop(self, ext_name: str, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS[ext_name]
         for arg in inputs:
              arg_expr = self._compile_expression(arg, child)
              pb_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
         return pb_expr

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
        elif dtype == bigframes.dtypes.BYTES_DTYPE:
             return {"binary": {}}
        elif dtype == bigframes.dtypes.DATE_DTYPE:
             return {"date": {}}
        elif dtype == bigframes.dtypes.DATETIME_DTYPE:
             return {"precision_timestamp": {"precision": 6}}
        elif dtype == bigframes.dtypes.TIMESTAMP_DTYPE:
             return {"precision_timestamp_tz": {"precision": 6}}
        elif dtype == bigframes.dtypes.TIME_DTYPE:
             # type_variation_reference 1 is for time64, precision 6 is for microseconds
             return {"precision_time": {"precision": 6, "type_variation_reference": 1}}
        elif dtype in (bigframes.dtypes.NUMERIC_DTYPE, bigframes.dtypes.BIGNUMERIC_DTYPE):
             arrow_dtype = dtype.pyarrow_dtype
             return {"decimal": {"precision": arrow_dtype.precision, "scale": arrow_dtype.scale}}
        elif dtype == bigframes.dtypes.TIMEDELTA_DTYPE:
             return {"interval_day": {"precision": 6, "type_variation_reference": 1}}
        else:
             # Fallback to string for now
             return {"string": {}}
