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
import bigframes.dtypes as dtypes
import pandas as pd
import bigframes.operations as ops
import bigframes.operations.numeric_ops as numeric_ops
import bigframes.operations.comparison_ops as comparison_ops
import bigframes.operations.generic_ops as generic_ops
import bigframes.operations.bool_ops as bool_ops
import bigframes.operations.struct_ops as struct_ops


class SubstraitCompiler:
    """
    Compiles BigFrameNode plans to Substrait schema (JSON representation).
    """

    def _print_node_tree(self, node: bigframe_node.BigFrameNode, indent: int = 0):
        import sys
        try:
            ids = list(node.ids)
        except Exception as e:
            ids = f"<error: {e}>"
        sys.stderr.write("  " * indent + f"- {type(node).__name__}: ids={ids}\n")
        sys.stderr.flush()
        for child in node.child_nodes:
             self._print_node_tree(child, indent + 1)

    def compile(self, plan: bigframe_node.BigFrameNode) -> Optional[bytes]:
        """
        Compiles a BigFrameNode to Substrait bytes (JSON encoded via protobuf).
        """
        if not self.can_compile(plan):
            return None

        import sys
        sys.stderr.write("DEBUG TREE:\n")
        sys.stderr.flush()
        self._print_node_tree(plan)

        pb_rel = self._compile_node(plan)
        
        pb_plan = plan_pb2.Plan()
        pb_plan.version.minor_number = 42
        
        plan_rel = pb_plan.relations.add()
        plan_rel.root.input.CopyFrom(pb_rel)
        
        for item in plan.schema.items:
             plan_rel.root.names.extend(self._get_substrait_names(item.column, item.dtype))
        
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
            nodes.OrderByNode,
            nodes.PromoteOffsetsNode,
            nodes.WindowOpNode,
            nodes.ConcatNode,
        )
        import sys
        for n in plan.unique_nodes():
             if not isinstance(n, supported_nodes):
                  sys.stderr.write(f"UNSUPPORTED NODE TYPE: {type(n).__name__} -> {n}\n")
                  sys.stderr.flush()
        return all(isinstance(n, supported_nodes) for n in plan.unique_nodes())

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
        elif isinstance(node, nodes.OrderByNode):
             return self._compile_orderby(node)
        elif isinstance(node, nodes.SliceNode):
             return self._compile_slice(node)
        elif isinstance(node, nodes.PromoteOffsetsNode):
             return self._compile_promote_offsets(node)
        elif isinstance(node, nodes.WindowOpNode):
             return self._compile_window(node)
        elif isinstance(node, nodes.ConcatNode):
             return self._compile_concat(node)
        else:
             raise NotImplementedError(f"Node type {type(node)} not supported in Substrait compiler yet")

    def _compile_read(self, node: nodes.ReadLocalNode) -> algebra_pb2.Rel:
        table_name = f"table_{id(node)}"
        
        rel = algebra_pb2.Rel()
        read_rel = rel.read
        read_rel.named_table.names.append(table_name)
        
        import bigframes.dtypes as dtypes
        fields = []
        types = []
        for item in node.scan_list.items:
             col_dtype = node.local_data_source.schema.get_type(item.source_id)
             fields.extend(self._get_substrait_names(item.id.sql, col_dtype))
             types.append(self._convert_type(col_dtype))
             
        if node.offsets_col is not None:
             fields.append(node.offsets_col.sql)
             types.append(self._convert_type(dtypes.INT_DTYPE))
             
        schema_dict = {
            "names": fields,
            "struct": {"types": types}
        }
        print("SCHEMA_DICT:", schema_dict)
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

    def _compile_promote_offsets(self, node: nodes.PromoteOffsetsNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        project_rel = rel.project
        project_rel.input.CopyFrom(input_rel)
        
        # Add a dummy literal i64 = 0 for the offsets column
        expr = project_rel.expressions.add()
        expr.literal.i64 = 0
        
        child_ids = list(node.child.ids)
        project_rel.common.emit.output_mapping.extend(range(len(child_ids) + 1))
        
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
             
        child_ids = list(node.child.ids)
        num_exprs = len(node.assignments)
        project_rel.common.emit.output_mapping.extend(range(len(child_ids) + num_exprs))
        
        return rel

    def _compile_join(self, node: nodes.JoinNode) -> algebra_pb2.Rel:
        left_rel = self._compile_node(node.left_child)
        right_rel = self._compile_node(node.right_child)
        
        rel = algebra_pb2.Rel()
        if node.type == "cross":
             cross_rel = rel.cross
             cross_rel.left.CopyFrom(left_rel)
             cross_rel.right.CopyFrom(right_rel)
             return rel
             
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
        
        import sys
        sys.stderr.write(f"JOIN CONDITIONS: {node.conditions}\n")
        sys.stderr.flush()
        
        eq_expressions = []
        for left_deref, right_deref in node.conditions:
             left_idx = list(node.left_child.ids).index(left_deref.id)
             right_idx = list(node.right_child.ids).index(right_deref.id) + left_len
             
             arg1 = algebra_pb2.Expression()
             arg1.selection.direct_reference.struct_field.field = left_idx
             
             arg2 = algebra_pb2.Expression()
             arg2.selection.direct_reference.struct_field.field = right_idx
             
             eq_expr = algebra_pb2.Expression()
             eq_expr.scalar_function.function_reference = self._EXTENSIONS["equal"]
             eq_expr.scalar_function.arguments.add().value.CopyFrom(arg1)
             eq_expr.scalar_function.arguments.add().value.CopyFrom(arg2)
             
             isnull1_expr = algebra_pb2.Expression()
             isnull1_expr.scalar_function.function_reference = self._EXTENSIONS["is_null"]
             isnull1_expr.scalar_function.arguments.add().value.CopyFrom(arg1)
             
             isnull2_expr = algebra_pb2.Expression()
             isnull2_expr.scalar_function.function_reference = self._EXTENSIONS["is_null"]
             isnull2_expr.scalar_function.arguments.add().value.CopyFrom(arg2)
             
             both_null_expr = algebra_pb2.Expression()
             both_null_expr.scalar_function.function_reference = self._EXTENSIONS["and"]
             both_null_expr.scalar_function.arguments.add().value.CopyFrom(isnull1_expr)
             both_null_expr.scalar_function.arguments.add().value.CopyFrom(isnull2_expr)
             
             null_safe_eq = algebra_pb2.Expression()
             null_safe_eq.scalar_function.function_reference = self._EXTENSIONS["or"]
             null_safe_eq.scalar_function.arguments.add().value.CopyFrom(eq_expr)
             null_safe_eq.scalar_function.arguments.add().value.CopyFrom(both_null_expr)
             
             eq_expressions.append(null_safe_eq)
             
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

    def _compile_window(self, node: nodes.WindowOpNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)

        # ProjectRel 1: Evaluate all window functions (standard ones + lag/lead for DiffOp)
        rel1 = algebra_pb2.Rel()
        project_rel1 = rel1.project
        project_rel1.input.CopyFrom(input_rel)

        import bigframes.dtypes as dtypes
        import bigframes.operations.aggregations as agg_ops
        import bigframes.core.window_spec as window_spec_module
        
        has_diff = False
        has_struct_fill = False
        for cdef in node.agg_exprs:
             op = cdef.expression.op
             if isinstance(op, agg_ops.DiffOp):
                  has_diff = True
             if isinstance(op, (agg_ops.LastNonNullOp, agg_ops.FirstNonNullOp)) and len(node.window_spec.ordering) > 0:
                  has_struct_fill = True

             expr = project_rel1.expressions.add()
             wf = expr.window_function

             if isinstance(op, agg_ops.DiffOp):
                  periods = op.periods
                  if periods >= 0:
                       func_name = "lag"
                  else:
                       func_name = "lead"
                       periods = -periods
             elif isinstance(op, agg_ops.SumOp):
                  func_name = "sum"
             elif isinstance(op, agg_ops.MaxOp):
                  func_name = "max"
             elif isinstance(op, agg_ops.MinOp):
                  func_name = "min"
             elif isinstance(op, agg_ops.MeanOp):
                  func_name = "mean"
             elif isinstance(op, agg_ops.CountOp):
                  func_name = "count"
             elif isinstance(op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                  func_name = "count"
             elif isinstance(op, agg_ops.StdOp):
                  func_name = "stddev"
             elif isinstance(op, agg_ops.VarOp):
                  func_name = "var"
             elif isinstance(op, agg_ops.PopVarOp):
                  func_name = "var_pop"
             elif isinstance(op, agg_ops.RowNumberOp):
                  func_name = "row_number"
             elif isinstance(op, agg_ops.RankOp):
                  func_name = "rank"
             elif isinstance(op, agg_ops.DenseRankOp):
                  func_name = "dense_rank"
             elif isinstance(op, agg_ops.FirstOp):
                  func_name = "first_value"
             elif isinstance(op, agg_ops.FirstNonNullOp):
                  if len(node.window_spec.ordering) > 0:
                       func_name = "min"
                  else:
                       func_name = "first_value"
             elif isinstance(op, agg_ops.LastOp):
                  func_name = "last_value"
             elif isinstance(op, agg_ops.LastNonNullOp):
                  if len(node.window_spec.ordering) > 0:
                       func_name = "max"
                  else:
                       func_name = "last_value"
             elif isinstance(op, agg_ops.ShiftOp):
                  periods = op.periods
                  if periods >= 0:
                       func_name = "lag"
                  else:
                       func_name = "lead"
                       periods = -periods
             else:
                  raise NotImplementedError(f"Aggregation operator {type(op).__name__} not supported in window compilation yet")

             wf.function_reference = self._EXTENSIONS[func_name]

             if isinstance(op, (agg_ops.LastNonNullOp, agg_ops.FirstNonNullOp)) and len(node.window_spec.ordering) > 0:
                  import bigframes.operations.generic_ops as generic_ops
                  from google.protobuf import json_format

                  input_expr = cdef.expression.children[0]
                  order_expr = node.window_spec.ordering[0].scalar_expression
                  in_dtype_val = self._get_expression_dtype(input_expr, node.child)

                  # Build NOT_NULL(input_expr)
                  cond = algebra_pb2.Expression()
                  cond.scalar_function.function_reference = self._EXTENSIONS[self._OP_TO_EXTENSION[generic_ops.NotNullOp]]
                  cond_arg = cond.scalar_function.arguments.add()
                  cond_arg.value.CopyFrom(self._compile_expression(input_expr, node.child))
                  json_format.ParseDict({"bool": {}}, cond.scalar_function.output_type)

                  # Build struct_expr struct(order_expr, input_expr)
                  struct_expr = algebra_pb2.Expression()
                  struct_expr.scalar_function.function_reference = self._EXTENSIONS["struct"]
                  
                  arg0 = struct_expr.scalar_function.arguments.add()
                  arg0.value.CopyFrom(self._compile_expression(order_expr, node.child))
                  
                  arg1 = struct_expr.scalar_function.arguments.add()
                  arg1.value.CopyFrom(self._compile_expression(input_expr, node.child))

                  # Output type of struct is struct<i64, target_type>
                  struct_type = {
                      "struct": {
                          "types": [
                              {"i64": {}},
                              self._convert_type(in_dtype_val)
                          ]
                      }
                  }
                  json_format.ParseDict(struct_type, struct_expr.scalar_function.output_type)

                  is_min = isinstance(op, agg_ops.FirstNonNullOp)
                  dummy_idx = 9223372036854775807 if is_min else -1

                  # Build dummy struct struct(dummy_idx, NULL)
                  dummy_struct = algebra_pb2.Expression()
                  dummy_struct.scalar_function.function_reference = self._EXTENSIONS["struct"]
                  
                  arg0_d = dummy_struct.scalar_function.arguments.add()
                  arg0_d.value.literal.i64 = dummy_idx
                  
                  arg1_d = dummy_struct.scalar_function.arguments.add()
                  target_type_proto = type_pb2.Type()
                  json_format.ParseDict(self._convert_type(in_dtype_val), target_type_proto)
                  arg1_d.value.literal.null.CopyFrom(target_type_proto)
                  
                  json_format.ParseDict(struct_type, dummy_struct.scalar_function.output_type)

                  # Build IfThen expression
                  ifthen_expr = algebra_pb2.Expression()
                  if_clause = ifthen_expr.if_then.ifs.add()
                  getattr(if_clause, "if").CopyFrom(cond)
                  if_clause.then.CopyFrom(struct_expr)
                  getattr(ifthen_expr.if_then, "else").CopyFrom(dummy_struct)

                  arg = wf.arguments.add()
                  arg.value.CopyFrom(ifthen_expr)
             else:
                  for child_expr in cdef.expression.children:
                       arg = wf.arguments.add()
                       arg.value.CopyFrom(self._compile_expression(child_expr, node.child))

             if isinstance(op, (agg_ops.ShiftOp, agg_ops.DiffOp)):
                  arg = wf.arguments.add()
                  arg.value.literal.i64 = periods

             if isinstance(op, (agg_ops.LastNonNullOp, agg_ops.FirstNonNullOp)) and len(node.window_spec.ordering) > 0:
                  import bigframes.dtypes as dtypes
                  import pandas as pd
                  import pyarrow as pa
                  input_expr = cdef.expression.children[0]
                  order_expr = node.window_spec.ordering[0].scalar_expression
                  in_dtype_order = self._get_expression_dtype(order_expr, node.child)
                  in_dtype_val = self._get_expression_dtype(input_expr, node.child)
                  arrow_order = dtypes.bigframes_dtype_to_arrow_dtype(in_dtype_order)
                  arrow_val = dtypes.bigframes_dtype_to_arrow_dtype(in_dtype_val)

                  struct_dtype = pd.ArrowDtype(pa.struct([
                      pa.field("c0", arrow_order, nullable=True),
                      pa.field("c1", arrow_val, nullable=True)
                  ]))
                  from google.protobuf import json_format
                  json_format.ParseDict(self._convert_type(struct_dtype), wf.output_type)
             else:
                  dt = node.field_by_id[cdef.id].dtype
                  from google.protobuf import json_format
                  json_format.ParseDict(self._convert_type(dt), wf.output_type)

             # Compile Bounds
             if isinstance(node.window_spec.bounds, window_spec_module.RowsWindowBounds):
                  wf.bounds_type = algebra_pb2.Expression.WindowFunction.BoundsType.BOUNDS_TYPE_ROWS
                  self._compile_bound(node.window_spec.bounds.start, wf.lower_bound)
                  self._compile_bound(node.window_spec.bounds.end, wf.upper_bound)
             elif isinstance(node.window_spec.bounds, window_spec_module.RangeWindowBounds):
                  wf.bounds_type = algebra_pb2.Expression.WindowFunction.BoundsType.BOUNDS_TYPE_RANGE
                  self._compile_bound(node.window_spec.bounds.start, wf.lower_bound)
                  self._compile_bound(node.window_spec.bounds.end, wf.upper_bound)
             else:
                  wf.bounds_type = algebra_pb2.Expression.WindowFunction.BoundsType.BOUNDS_TYPE_ROWS
                  wf.lower_bound.unbounded.CopyFrom(algebra_pb2.Expression.WindowFunction.Bound.Unbounded())
                  wf.upper_bound.unbounded.CopyFrom(algebra_pb2.Expression.WindowFunction.Bound.Unbounded())

             # Partition Expressions
             for part_expr in node.window_spec.grouping_keys:
                  expr_pb = self._compile_expression(part_expr, node.child)
                  wf.partitions.add().CopyFrom(expr_pb)

             # Sorts
             for sort_expr in node.window_spec.ordering:
                  expr_pb = self._compile_expression(sort_expr.scalar_expression, node.child)
                  sort_field = wf.sorts.add()
                  sort_field.expr.CopyFrom(expr_pb)
                  if sort_expr.direction.is_ascending:
                       if sort_expr.na_last:
                            sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_LAST
                       else:
                            sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_FIRST
                  else:
                       if sort_expr.na_last:
                            sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_LAST
                       else:
                            sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_FIRST

        child_ids = list(node.child.ids)
        num_exprs = len(node.agg_exprs)
        
        if not (has_diff or has_struct_fill):
             project_rel1.common.emit.output_mapping.extend(range(len(child_ids) + num_exprs))
             return rel1

        # ProjectRel 2: Compute subtraction for DiffOp columns or extract struct fields
        rel2 = algebra_pb2.Rel()
        project_rel2 = rel2.project
        project_rel2.input.CopyFrom(rel1)

        num_cols_rel1 = len(child_ids) + num_exprs
        new_expr_idx = 0
        output_mapping = list(range(len(child_ids)))

        for cdef_idx, cdef in enumerate(node.agg_exprs):
             op = cdef.expression.op
             if isinstance(op, agg_ops.DiffOp):
                  expr = project_rel2.expressions.add()
                  expr.scalar_function.function_reference = self._EXTENSIONS["subtract"]

                  # Arg 1: current column
                  col_idx = list(node.child.ids).index(cdef.expression.children[0].id)
                  arg1 = expr.scalar_function.arguments.add()
                  arg1.value.selection.direct_reference.struct_field.field = col_idx

                  # Arg 2: lag column from rel1
                  lag_idx = len(child_ids) + cdef_idx
                  arg2 = expr.scalar_function.arguments.add()
                  arg2.value.selection.direct_reference.struct_field.field = lag_idx

                  dt = node.field_by_id[cdef.id].dtype
                  from google.protobuf import json_format
                  json_format.ParseDict(self._convert_type(dt), expr.scalar_function.output_type)

                  # Output mapping points to this newly projected expression
                  output_mapping.append(num_cols_rel1 + new_expr_idx)
                  new_expr_idx += 1
             elif isinstance(op, (agg_ops.LastNonNullOp, agg_ops.FirstNonNullOp)) and len(node.window_spec.ordering) > 0:
                  from google.protobuf import json_format

                  window_col_idx = len(child_ids) + cdef_idx
                  is_min = isinstance(op, agg_ops.FirstNonNullOp)
                  dummy_idx = 9223372036854775807 if is_min else -1

                  # 1. Build get_field(window_col_idx, "c0")
                  get_c0 = algebra_pb2.Expression()
                  get_c0.scalar_function.function_reference = self._EXTENSIONS["get_field"]
                  arg0 = get_c0.scalar_function.arguments.add()
                  arg0.value.selection.direct_reference.struct_field.field = window_col_idx
                  arg1 = get_c0.scalar_function.arguments.add()
                  arg1.value.literal.string = "c0"
                  json_format.ParseDict({"i64": {}}, get_c0.scalar_function.output_type)

                  # 2. Build get_c0 == dummy_idx
                  eq_c0 = algebra_pb2.Expression()
                  eq_c0.scalar_function.function_reference = self._EXTENSIONS["equal"]
                  arg0 = eq_c0.scalar_function.arguments.add()
                  arg0.value.CopyFrom(get_c0)
                  arg1 = eq_c0.scalar_function.arguments.add()
                  arg1.value.literal.i64 = dummy_idx
                  json_format.ParseDict({"bool": {}}, eq_c0.scalar_function.output_type)

                  # 3. Build the IfThen expression
                  expr = project_rel2.expressions.add()
                  if_clause = expr.if_then.ifs.add()
                  getattr(if_clause, "if").CopyFrom(eq_c0)

                  # Then value: NULL of target type
                  dt = node.field_by_id[cdef.id].dtype
                  target_type_proto = type_pb2.Type()
                  json_format.ParseDict(self._convert_type(dt), target_type_proto)
                  if_clause.then.literal.null.CopyFrom(target_type_proto)

                  # Else value: get_field(window_col_idx, "c1")
                  get_c1 = algebra_pb2.Expression()
                  get_c1.scalar_function.function_reference = self._EXTENSIONS["get_field"]
                  arg0 = get_c1.scalar_function.arguments.add()
                  arg0.value.selection.direct_reference.struct_field.field = window_col_idx
                  arg1 = get_c1.scalar_function.arguments.add()
                  arg1.value.literal.string = "c1"
                  json_format.ParseDict(self._convert_type(dt), get_c1.scalar_function.output_type)

                  getattr(expr.if_then, "else").CopyFrom(get_c1)

                  # Output mapping points to this newly projected expression
                  output_mapping.append(num_cols_rel1 + new_expr_idx)
                  new_expr_idx += 1
             else:
                  # Output mapping points to the direct window column from rel1
                  output_mapping.append(len(child_ids) + cdef_idx)

        project_rel2.common.emit.output_mapping.extend(output_mapping)
        return rel2

    def _compile_bound(self, val: typing.Optional[int], bound_msg: algebra_pb2.Expression.WindowFunction.Bound):
        if val is None:
             bound_msg.unbounded.CopyFrom(algebra_pb2.Expression.WindowFunction.Bound.Unbounded())
        elif val == 0:
             bound_msg.current_row.CopyFrom(algebra_pb2.Expression.WindowFunction.Bound.CurrentRow())
        elif val < 0:
             bound_msg.preceding.offset = -val
        else:
             bound_msg.following.offset = val

    def _compile_concat(self, node: nodes.ConcatNode) -> algebra_pb2.Rel:
        rel = algebra_pb2.Rel()
        set_rel = rel.set
        set_rel.op = algebra_pb2.SetRel.SetOp.SET_OP_UNION_ALL

        for child in node.children:
             set_rel.inputs.append(self._compile_node(child))

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
        import bigframes.dtypes as dtypes
        size_count = 0
        for agg, out_col_id in node.aggregations:
             distinct = False
             if isinstance(agg.op, agg_ops.SumOp):
                  func_ref = self._EXTENSIONS["sum"]
             elif isinstance(agg.op, agg_ops.MaxOp):
                  func_ref = self._EXTENSIONS["max"]
             elif isinstance(agg.op, agg_ops.MinOp):
                  func_ref = self._EXTENSIONS["min"]
             elif isinstance(agg.op, agg_ops.MeanOp):
                  func_ref = self._EXTENSIONS["mean"]
             elif isinstance(agg.op, agg_ops.CountOp):
                  func_ref = self._EXTENSIONS["count"]
             elif isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                  func_ref = self._EXTENSIONS["count"]
             elif isinstance(agg.op, agg_ops.NuniqueOp):
                  func_ref = self._EXTENSIONS["count"]
                  distinct = True
             elif isinstance(agg.op, agg_ops.StdOp):
                  func_ref = self._EXTENSIONS["stddev"]
             elif isinstance(agg.op, agg_ops.VarOp):
                  func_ref = self._EXTENSIONS["var"]
             elif isinstance(agg.op, agg_ops.PopVarOp):
                  func_ref = self._EXTENSIONS["var_pop"]
             elif isinstance(agg.op, agg_ops.AnyValueOp):
                  func_ref = self._EXTENSIONS["min"]
             elif isinstance(agg.op, agg_ops.AllOp):
                  func_ref = self._EXTENSIONS["bool_and"]
             elif isinstance(agg.op, agg_ops.AnyOp):
                  func_ref = self._EXTENSIONS["bool_or"]
             elif isinstance(agg.op, agg_ops.ProductOp):
                  func_ref = self._EXTENSIONS["product"]
             elif isinstance(agg.op, agg_ops.MedianOp):
                  func_ref = self._EXTENSIONS["median"]
             else:
                  raise NotImplementedError(f"Aggregation {type(agg.op)} not supported in Substrait compiler yet")
                  
             measure = agg_rel.measures.add()
             measure.measure.function_reference = func_ref
             if distinct or isinstance(agg.op, agg_ops.NuniqueOp):
                  measure.measure.invocation = algebra_pb2.AggregateFunction.AGGREGATION_INVOCATION_DISTINCT
             
             if isinstance(agg.op, (agg_ops.SizeOp, agg_ops.SizeUnaryOp)):
                  size_count += 1
                  arg = measure.measure.arguments.add()
                  arg.value.literal.i64 = size_count
             elif hasattr(agg, "column_references"):
                  for col_id in agg.column_references:
                       try:
                           idx = list(node.child.ids).index(col_id)
                           field_expr = algebra_pb2.Expression()
                           field_expr.selection.direct_reference.struct_field.field = idx
                           
                           col_dtype = node.child.schema.items[idx].dtype
                           is_bool = col_dtype == dtypes.BOOL_DTYPE
                           if isinstance(agg.op, (agg_ops.StdOp, agg_ops.VarOp, agg_ops.PopVarOp)) or (isinstance(agg.op, (agg_ops.SumOp, agg_ops.MeanOp)) and is_bool):
                                casted_expr = self._compile_cast(field_expr, dtypes.FLOAT_DTYPE)
                                arg = measure.measure.arguments.add()
                                arg.value.CopyFrom(casted_expr)
                           else:
                                arg = measure.measure.arguments.add()
                                arg.value.CopyFrom(field_expr)
                       except ValueError:
                           pass
                            
        if node.dropna and node.by_column_ids:
             not_null_exprs = []
             for idx in range(len(node.by_column_ids)):
                  key_expr = algebra_pb2.Expression()
                  key_expr.selection.direct_reference.struct_field.field = idx
                  
                  not_null_op = algebra_pb2.Expression()
                  not_null_op.scalar_function.function_reference = self._EXTENSIONS["is_not_null"]
                  not_null_op.scalar_function.arguments.add().value.CopyFrom(key_expr)
                  not_null_exprs.append(not_null_op)
                  
             if len(not_null_exprs) > 1:
                  expr = not_null_exprs[0]
                  for e in not_null_exprs[1:]:
                       and_expr = algebra_pb2.Expression()
                       and_expr.scalar_function.function_reference = self._EXTENSIONS["and"]
                       and_expr.scalar_function.arguments.add().value.CopyFrom(expr)
                       and_expr.scalar_function.arguments.add().value.CopyFrom(e)
                       expr = and_expr
             else:
                  expr = not_null_exprs[0]
                  
             filter_rel = algebra_pb2.Rel()
             filter_rel.filter.input.CopyFrom(rel)
             filter_rel.filter.condition.CopyFrom(expr)
             rel = filter_rel

        return rel

    def _compile_orderby(self, node: nodes.OrderByNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        sort_rel = rel.sort
        sort_rel.input.CopyFrom(input_rel)
        
        for ord_expr in node.by:
             sort_field = sort_rel.sorts.add()
             
             # Compile the expression:
             expr_pb = self._compile_expression(ord_expr.scalar_expression, node.child)
             sort_field.expr.CopyFrom(expr_pb)
             
             # Map sort direction:
             is_asc = ord_expr.direction.is_ascending
             if is_asc:
                  if ord_expr.na_last:
                       sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_LAST
                  else:
                       sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_ASC_NULLS_FIRST
             else:
                  if ord_expr.na_last:
                       sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_LAST
                  else:
                       sort_field.direction = algebra_pb2.SortField.SortDirection.SORT_DIRECTION_DESC_NULLS_FIRST
                       
        return rel

    def _compile_slice(self, node: nodes.SliceNode) -> algebra_pb2.Rel:
        input_rel = self._compile_node(node.child)
        
        rel = algebra_pb2.Rel()
        fetch_rel = rel.fetch
        fetch_rel.input.CopyFrom(input_rel)
        
        is_simple = (node.start is None or node.start >= 0) and (node.stop is None or node.stop >= 0) and (node.step is None or node.step == 1)
        
        if is_simple:
             start = node.start if node.start is not None else 0
             fetch_rel.offset = start
             
             if node.stop is not None:
                  fetch_rel.count = max(0, node.stop - start)
             else:
                  fetch_rel.count = -1
        else:
             fetch_rel.offset = 0
             fetch_rel.count = -1
              
        return rel

    _EXTENSIONS = {
        "add": 1,
        "subtract": 2,
        "multiply": 3,
        "divide": 4,
        "equal": 5,
        "not_equal": 6,
        "lt": 7,
        "gt": 8,
        "lte": 9,
        "gte": 10,
        "sum": 11,
        "max": 12,
        "and": 13,
        "min": 14,
        "mean": 15,
        "count": 16,
        "stddev": 17,
        "var": 18,
        "any_value": 19,
        "all": 20,
        "any": 21,
        "coalesce": 22,
        "or": 23,
        "least": 24,
        "greatest": 25,
        "is_null": 26,
        "is_not_null": 27,
        "nullif": 28,
        "sqrt": 29,
        "bool_and": 30,
        "bool_or": 31,
        "product": 32,
        "not": 33,
        "mod": 34,
        "floor": 35,
        "abs": 36,
        "ceil": 37,
        "median": 38,
        "xor": 40,
        "var_pop": 53,
        "row_number": 60,
        "rank": 61,
        "dense_rank": 62,
        "first_value": 63,
        "last_value": 64,
        "lag": 65,
        "lead": 66,
        "struct": 67,
        "get_field": 68,
    }

    _OP_TO_EXTENSION = {
        numeric_ops.AddOp: "add",
        numeric_ops.SubOp: "subtract",
        numeric_ops.MulOp: "multiply",
        numeric_ops.DivOp: "divide",
        numeric_ops.ModOp: "mod",
        comparison_ops.EqOp: "equal",
        comparison_ops.NeOp: "not_equal",
        comparison_ops.LtOp: "lt",
        comparison_ops.GtOp: "gt",
        comparison_ops.LeOp: "lte",
        comparison_ops.GeOp: "gte",
        generic_ops.FillNaOp: "coalesce",
        generic_ops.CoalesceOp: "coalesce",
        bool_ops.AndOp: "and",
        bool_ops.OrOp: "or",
        bool_ops.XorOp: "xor",
        generic_ops.InvertOp: "not",
        numeric_ops.AbsOp: "abs",
        numeric_ops.CeilOp: "ceil",
        numeric_ops.FloorOp: "floor",
        generic_ops.IsNullOp: "is_null",
        generic_ops.NotNullOp: "is_not_null",
    }

    @singledispatchmethod
    def _compile_expression(self, expr: ex.Expression, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         raise NotImplementedError(f"Expression type {type(expr)} not supported in Substrait compiler yet")

    @_compile_expression.register
    def _compile_scalar_constant(self, expr: ex.ScalarConstantExpression, child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         import datetime
         pb_expr = algebra_pb2.Expression()
         val = expr.value
         if isinstance(val, bool):
              pb_expr.literal.boolean = val
         elif isinstance(val, int):
              pb_expr.literal.i64 = val
         elif isinstance(val, float):
              pb_expr.literal.fp64 = val
         elif isinstance(val, str):
              pb_expr.literal.string = val
         elif isinstance(val, (pd.Timestamp, datetime.datetime)):
              if getattr(val, "tzinfo", None) is not None:
                   epoch = pd.Timestamp("1970-01-01", tz=val.tzinfo)
                   us = int((val - epoch).total_seconds() * 1_000_000)
                   pb_expr.literal.precision_timestamp_tz.precision = 6
                   pb_expr.literal.precision_timestamp_tz.value = us
              else:
                   epoch = pd.Timestamp("1970-01-01")
                   us = int((val - epoch).total_seconds() * 1_000_000)
                   pb_expr.literal.precision_timestamp.precision = 6
                   pb_expr.literal.precision_timestamp.value = us
         elif isinstance(val, datetime.date):
              epoch = datetime.date(1970, 1, 1)
              days = (val - epoch).days
              pb_expr.literal.date = days
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

    @_compile_op.register(ops.AsTypeOp)
    def _compile_astype(self, op: ops.AsTypeOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         arg_expr = self._compile_expression(inputs[0], child)
         return self._compile_cast(arg_expr, op.to_type)

    @_compile_op.register(struct_ops.StructOp)
    def _compile_struct_op(self, op: struct_ops.StructOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS["struct"]
         for arg in inputs:
              arg_expr = self._compile_expression(arg, child)
              pb_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
         return pb_expr

    @_compile_op.register(struct_ops.StructFieldOp)
    def _compile_struct_field_op(self, op: struct_ops.StructFieldOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS["get_field"]
         
         # Arg 0: the struct
         arg_expr = self._compile_expression(inputs[0], child)
         pb_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
         
         # Arg 1: the field name as string literal
         literal_expr = algebra_pb2.Expression()
         literal_expr.literal.string = str(op.name_or_index)
         pb_expr.scalar_function.arguments.add().value.CopyFrom(literal_expr)
         return pb_expr

    def _compile_cast(self, input_expr: algebra_pb2.Expression, target_dtype: Any) -> algebra_pb2.Expression:
         if input_expr.HasField("literal") and input_expr.literal.HasField("null"):
              pb_expr = algebra_pb2.Expression()
              type_dict = self._convert_type(target_dtype)
              json_format.ParseDict(type_dict, pb_expr.literal.null)
              return pb_expr

         pb_expr = algebra_pb2.Expression()
         cast = pb_expr.cast
         cast.input.CopyFrom(input_expr)
         
         type_dict = self._convert_type(target_dtype)
         json_format.ParseDict(type_dict, cast.type)
         
         cast.failure_behavior = algebra_pb2.Expression.Cast.FAILURE_BEHAVIOR_RETURN_NULL
         return pb_expr

    def _get_expression_dtype(self, expr: ex.Expression, child: nodes.BigFrameNode) -> Any:
         import bigframes.dtypes as dtypes
         if isinstance(expr, ex.ScalarConstantExpression):
              if expr.value is None or pd.isna(expr.value):
                   return None
              return expr.dtype or dtypes.infer_literal_type(expr.value)
         elif isinstance(expr, ex.DerefOp):
              try:
                   idx = list(child.ids).index(expr.id)
                   return child.schema.items[idx].dtype
              except ValueError:
                   pass
         elif isinstance(expr, ex.OpExpression):
              try:
                   input_dtypes = [self._get_expression_dtype(inp, child) for inp in expr.inputs]
                   return expr.op.output_type(*input_dtypes)
              except Exception:
                   pass
         return dtypes.STRING_DTYPE

    def _get_common_type(self, dtypes_list: Sequence[Any]) -> Any:
         import bigframes.dtypes as dtypes
         non_null_dtypes = [dt for dt in dtypes_list if dt is not None]
         if not non_null_dtypes:
              return dtypes.STRING_DTYPE
         if len(set(non_null_dtypes)) == 1:
              return non_null_dtypes[0]
         if any(dt == dtypes.STRING_DTYPE for dt in non_null_dtypes):
              return dtypes.STRING_DTYPE
         if any(dt == dtypes.FLOAT_DTYPE for dt in non_null_dtypes):
              return dtypes.FLOAT_DTYPE
         if any(dt == dtypes.INT_DTYPE for dt in non_null_dtypes):
              return dtypes.INT_DTYPE
         return dtypes.STRING_DTYPE

    @_compile_op.register(ops.CaseWhenOp)
    def _compile_casewhen(self, op: ops.CaseWhenOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         ifthen = pb_expr.if_then
         
         then_dtypes = [self._get_expression_dtype(inputs[idx], child) for idx in range(1, len(inputs), 2)]
         common_dtype = self._get_common_type(then_dtypes)
         
         for idx in range(0, len(inputs), 2):
              pred = self._compile_expression(inputs[idx], child)
              val_expr = self._compile_expression(inputs[idx+1], child)
              
              val_dtype = then_dtypes[idx // 2]
              if val_dtype != common_dtype:
                   val = self._compile_cast(val_expr, common_dtype)
              else:
                   val = val_expr
                   
              if_clause = ifthen.ifs.add()
              getattr(if_clause, "if").CopyFrom(pred)
              if_clause.then.CopyFrom(val)
              
         type_dict = self._convert_type(common_dtype)
         json_format.ParseDict(type_dict, getattr(ifthen, "else").literal.null)
         return pb_expr

    @_compile_op.register(generic_ops.WhereOp)
    def _compile_where(self, op: generic_ops.WhereOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         ifthen = pb_expr.if_then
         
         pred = self._compile_expression(inputs[1], child)
         then_val = self._compile_expression(inputs[0], child)
         else_val = self._compile_expression(inputs[2], child)
         
         then_dtype = self._get_expression_dtype(inputs[0], child)
         else_dtype = self._get_expression_dtype(inputs[2], child)
         common_dtype = self._get_common_type([then_dtype, else_dtype])
         
         casted_then = self._compile_cast(then_val, common_dtype)
         casted_else = self._compile_cast(else_val, common_dtype)
         
         if_clause = ifthen.ifs.add()
         getattr(if_clause, "if").CopyFrom(pred)
         if_clause.then.CopyFrom(casted_then)
         
         getattr(ifthen, "else").CopyFrom(casted_else)
         return pb_expr

    @_compile_op.register(numeric_ops.DivOp)
    def _compile_div_op(self, op: numeric_ops.DivOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         import bigframes.dtypes as dtypes
         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS["divide"]
         for arg in inputs:
              arg_expr = self._compile_expression(arg, child)
              casted_arg = self._compile_cast(arg_expr, dtypes.FLOAT_DTYPE)
              pb_expr.scalar_function.arguments.add().value.CopyFrom(casted_arg)
         return pb_expr

    @_compile_op.register(numeric_ops.FloorDivOp)
    def _compile_floor_div_op(self, op: numeric_ops.FloorDivOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         import bigframes.dtypes as dtypes
         
         dividend_expr = self._compile_expression(inputs[0], child)
         divisor_expr = self._compile_expression(inputs[1], child)
         
         # Calculate standard floor division
         div_expr = algebra_pb2.Expression()
         div_expr.scalar_function.function_reference = self._EXTENSIONS["divide"]
         
         # Cast to float for standard division
         casted_dividend = self._compile_cast(dividend_expr, dtypes.FLOAT_DTYPE)
         casted_divisor = self._compile_cast(divisor_expr, dtypes.FLOAT_DTYPE)
         
         div_expr.scalar_function.arguments.add().value.CopyFrom(casted_dividend)
         div_expr.scalar_function.arguments.add().value.CopyFrom(casted_divisor)
         
         floor_expr = algebra_pb2.Expression()
         floor_expr.scalar_function.function_reference = self._EXTENSIONS["floor"]
         floor_expr.scalar_function.arguments.add().value.CopyFrom(div_expr)
         
         # If both operands are integer/boolean, we short-circuit division by 0 to return 0
         left_dtype = self._get_expression_dtype(inputs[0], child)
         right_dtype = self._get_expression_dtype(inputs[1], child)
         
         is_left_int = left_dtype == dtypes.INT_DTYPE or left_dtype == dtypes.BOOL_DTYPE
         is_right_int = right_dtype == dtypes.INT_DTYPE or right_dtype == dtypes.BOOL_DTYPE
         
         if is_left_int and is_right_int:
              # If divisor is 0, return 0 * dividend (to propagate nulls)
              zero_i64 = algebra_pb2.Expression()
              zero_i64.literal.i64 = 0
              
              eq_expr = algebra_pb2.Expression()
              eq_expr.scalar_function.function_reference = self._EXTENSIONS["equal"]
              eq_expr.scalar_function.arguments.add().value.CopyFrom(divisor_expr)
              eq_expr.scalar_function.arguments.add().value.CopyFrom(zero_i64)
              
              zero_result = algebra_pb2.Expression()
              zero_result.scalar_function.function_reference = self._EXTENSIONS["multiply"]
              zero_result.scalar_function.arguments.add().value.CopyFrom(dividend_expr)
              zero_result.scalar_function.arguments.add().value.CopyFrom(zero_i64)
              
              pb_expr = algebra_pb2.Expression()
              ifthen = pb_expr.if_then
              if_clause = ifthen.ifs.add()
              getattr(if_clause, "if").CopyFrom(eq_expr)
              if_clause.then.CopyFrom(zero_result)
              
              # Else, cast float floor_expr to int64
              casted_floor = self._compile_cast(floor_expr, dtypes.INT_DTYPE)
              getattr(ifthen, "else").CopyFrom(casted_floor)
              return pb_expr
         
         return floor_expr

    @_compile_op.register(generic_ops.IsInOp)
    def _compile_isin(self, op: generic_ops.IsInOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         pb_expr.singular_or_list.value.CopyFrom(self._compile_expression(inputs[0], child))
         for val in op.values:
              opt_expr = self._compile_expression(ex.const(val), child)
              pb_expr.singular_or_list.options.add().CopyFrom(opt_expr)
         return pb_expr

    @_compile_op.register(generic_ops.FillNaOp)
    def _compile_fillna_op(self, op: generic_ops.FillNaOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         first_expr = self._compile_expression(inputs[0], child)
         first_dtype = self._get_expression_dtype(inputs[0], child)
         second_expr = self._compile_expression(inputs[1], child)
         second_dtype = self._get_expression_dtype(inputs[1], child)

         if first_dtype is not None and second_dtype != first_dtype:
              second_expr = self._compile_cast(second_expr, first_dtype)

         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS["coalesce"]
         pb_expr.scalar_function.arguments.add().value.CopyFrom(first_expr)
         pb_expr.scalar_function.arguments.add().value.CopyFrom(second_expr)
         return pb_expr

    @_compile_op.register(generic_ops.CoalesceOp)
    @_compile_op.register(numeric_ops.AddOp)
    @_compile_op.register(numeric_ops.SubOp)
    @_compile_op.register(numeric_ops.MulOp)
    @_compile_op.register(comparison_ops.EqOp)
    @_compile_op.register(comparison_ops.NeOp)
    @_compile_op.register(comparison_ops.LtOp)
    @_compile_op.register(comparison_ops.GtOp)
    @_compile_op.register(comparison_ops.LeOp)
    @_compile_op.register(comparison_ops.GeOp)
    @_compile_op.register(bool_ops.AndOp)
    @_compile_op.register(bool_ops.OrOp)
    @_compile_op.register(bool_ops.XorOp)
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

    @_compile_op.register(numeric_ops.ModOp)
    def _compile_mod_op(self, op: numeric_ops.ModOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         import bigframes.dtypes as dtypes
         a_expr = self._compile_expression(inputs[0], child)
         b_expr = self._compile_expression(inputs[1], child)
         
         div_expr = algebra_pb2.Expression()
         div_expr.scalar_function.function_reference = self._EXTENSIONS["divide"]
         
         a_float = self._compile_cast(a_expr, dtypes.FLOAT_DTYPE)
         b_float = self._compile_cast(b_expr, dtypes.FLOAT_DTYPE)
         div_expr.scalar_function.arguments.add().value.CopyFrom(a_float)
         div_expr.scalar_function.arguments.add().value.CopyFrom(b_float)
         
         floor_expr = algebra_pb2.Expression()
         floor_expr.scalar_function.function_reference = self._EXTENSIONS["floor"]
         floor_expr.scalar_function.arguments.add().value.CopyFrom(div_expr)
         
         mul_expr = algebra_pb2.Expression()
         mul_expr.scalar_function.function_reference = self._EXTENSIONS["multiply"]
         mul_expr.scalar_function.arguments.add().value.CopyFrom(b_float)
         mul_expr.scalar_function.arguments.add().value.CopyFrom(floor_expr)
         
         sub_expr = algebra_pb2.Expression()
         sub_expr.scalar_function.function_reference = self._EXTENSIONS["subtract"]
         sub_expr.scalar_function.arguments.add().value.CopyFrom(a_float)
         sub_expr.scalar_function.arguments.add().value.CopyFrom(mul_expr)
         
         a_dtype = self._get_expression_dtype(inputs[0], child)
         b_dtype = self._get_expression_dtype(inputs[1], child)
         common_dtype = self._get_common_type([a_dtype, b_dtype])
         
         if common_dtype == dtypes.INT_DTYPE:
              return self._compile_cast(sub_expr, dtypes.INT_DTYPE)
         return sub_expr

    @_compile_op.register(numeric_ops.AbsOp)
    @_compile_op.register(numeric_ops.CeilOp)
    @_compile_op.register(numeric_ops.FloorOp)
    @_compile_op.register(generic_ops.IsNullOp)
    @_compile_op.register(generic_ops.NotNullOp)
    def _compile_standard_unaryops(self, op: Any, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         op_class = type(op)
         ext_name = self._OP_TO_EXTENSION[op_class]
         return self._compile_basic_unaryop(ext_name, inputs, child)

    @_compile_op.register(numeric_ops.PosOp)
    def _compile_pos_op(self, op: numeric_ops.PosOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         # Unary plus is a no-op
         return self._compile_expression(inputs[0], child)

    @_compile_op.register(numeric_ops.NegOp)
    def _compile_neg_op(self, op: numeric_ops.NegOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         # Compile negation as subtraction: 0 - x
         arg_expr = self._compile_expression(inputs[0], child)
         arg_dtype = self._get_expression_dtype(inputs[0], child)
         
         zero_expr = algebra_pb2.Expression()
         if arg_dtype == dtypes.FLOAT_DTYPE:
              zero_expr.literal.fp64 = 0.0
         else:
              zero_expr.literal.i64 = 0
              
         sub_expr = algebra_pb2.Expression()
         sub_expr.scalar_function.function_reference = self._EXTENSIONS["subtract"]
         sub_expr.scalar_function.arguments.add().value.CopyFrom(zero_expr)
         sub_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
         return sub_expr

    @_compile_op.register(generic_ops.InvertOp)
    def _compile_invert_op(self, op: generic_ops.InvertOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         arg_expr = self._compile_expression(inputs[0], child)
         arg_dtype = self._get_expression_dtype(inputs[0], child)
         
         if arg_dtype == dtypes.BOOL_DTYPE:
              # Logical negation
              not_expr = algebra_pb2.Expression()
              not_expr.scalar_function.function_reference = self._EXTENSIONS["not"]
              not_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
              return not_expr
         else:
              # Bitwise negation (two's complement mathematically equivalent to: -x - 1)
              zero_i64 = algebra_pb2.Expression()
              zero_i64.literal.i64 = 0
              
              neg_expr = algebra_pb2.Expression()
              neg_expr.scalar_function.function_reference = self._EXTENSIONS["subtract"]
              neg_expr.scalar_function.arguments.add().value.CopyFrom(zero_i64)
              neg_expr.scalar_function.arguments.add().value.CopyFrom(arg_expr)
              
              one_i64 = algebra_pb2.Expression()
              one_i64.literal.i64 = 1
              
              result_expr = algebra_pb2.Expression()
              result_expr.scalar_function.function_reference = self._EXTENSIONS["subtract"]
              result_expr.scalar_function.arguments.add().value.CopyFrom(neg_expr)
              result_expr.scalar_function.arguments.add().value.CopyFrom(one_i64)
              return result_expr

    def _compile_basic_unaryop(self, ext_name: str, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         pb_expr = algebra_pb2.Expression()
         pb_expr.scalar_function.function_reference = self._EXTENSIONS[ext_name]
         arg_expr = self._compile_expression(inputs[0], child)
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

    def _get_substrait_names(self, name: str, dtype: Any) -> list[str]:
        import bigframes.dtypes as dtypes
        names = [name]
        if dtypes.is_struct_like(dtype):
             fields_dict = dtypes.get_struct_fields(dtype)
             for f_name, f_dtype in fields_dict.items():
                  names.extend(self._get_substrait_names(f_name, f_dtype))
        return names

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
        elif bigframes.dtypes.is_struct_like(dtype):
             fields_dict = bigframes.dtypes.get_struct_fields(dtype)
             return {"struct": {"types": [self._convert_type(f_dtype) for f_dtype in fields_dict.values()]}}
        elif bigframes.dtypes.is_array_like(dtype):
             inner_dtype = bigframes.dtypes.get_array_inner_type(dtype)
             return {"list": {"type": self._convert_type(inner_dtype)}}
        else:
             # Fallback to string for now
             return {"string": {}}

    @_compile_op.register(ops.ArrayReduceOp)
    def _compile_array_reduce(self, op: ops.ArrayReduceOp, inputs: Sequence[ex.Expression], child: nodes.BigFrameNode) -> algebra_pb2.Expression:
         import bigframes.operations.array_ops as arr_ops
         import bigframes.operations.aggregations as agg_ops
         import bigframes.dtypes as dtypes
         
         arr_expr = inputs[0]
         if not (isinstance(arr_expr, ex.OpExpression) and isinstance(arr_expr.op, arr_ops.ToArrayOp)):
              raise NotImplementedError(f"ArrayReduceOp only supported on ToArrayOp in Substrait compiler, got {type(arr_expr)}")
              
         array_inputs = arr_expr.inputs
         if not array_inputs:
              pb_expr = algebra_pb2.Expression()
              pb_expr.literal.null.varchar.length = 0
              return pb_expr
              
         compiled_inputs = [self._compile_expression(inp, child) for inp in array_inputs]
         input_dtypes = [self._get_expression_dtype(inp, child) for inp in array_inputs]
         common_dtype = self._get_common_type(input_dtypes)
         
         # For boolean aggregates, all operands must be Boolean.
         # For others, cast all elements to the common dtype first to resolve type coercion issues.
         if isinstance(op.aggregation, (agg_ops.AllOp, agg_ops.AnyOp)):
              casted_inputs = [self._compile_cast(expr, dtypes.BOOL_DTYPE) for expr in compiled_inputs]
         else:
              casted_inputs = [self._compile_cast(expr, common_dtype) for expr in compiled_inputs]
         
         def get_zero():
              z = algebra_pb2.Expression()
              if common_dtype == dtypes.FLOAT_DTYPE:
                   z.literal.fp64 = 0.0
              else:
                   z.literal.i64 = 0
              return z
              
         def call_binary(ext_name, left, right):
              pb = algebra_pb2.Expression()
              pb.scalar_function.function_reference = self._EXTENSIONS[ext_name]
              pb.scalar_function.arguments.add().value.CopyFrom(left)
              pb.scalar_function.arguments.add().value.CopyFrom(right)
              return pb
              
         def call_unary(ext_name, arg):
              pb = algebra_pb2.Expression()
              pb.scalar_function.function_reference = self._EXTENSIONS[ext_name]
              pb.scalar_function.arguments.add().value.CopyFrom(arg)
              return pb
              
         def cast_expr(expr, target):
              return self._compile_cast(expr, target)

         if isinstance(op.aggregation, agg_ops.AllOp):
              coalesced = []
              for ci in casted_inputs:
                   true_expr = algebra_pb2.Expression()
                   true_expr.literal.boolean = True
                   coalesced.append(call_binary("coalesce", ci, true_expr))
              
              res = coalesced[0]
              for next_expr in coalesced[1:]:
                   res = call_binary("and", res, next_expr)
              return res

         elif isinstance(op.aggregation, agg_ops.AnyOp):
              coalesced = []
              for ci in casted_inputs:
                   false_expr = algebra_pb2.Expression()
                   false_expr.literal.boolean = False
                   coalesced.append(call_binary("coalesce", ci, false_expr))
              
              res = coalesced[0]
              for next_expr in coalesced[1:]:
                   res = call_binary("or", res, next_expr)
              return res

         elif isinstance(op.aggregation, agg_ops.SumOp):
              coalesced = []
              for ci in casted_inputs:
                   coalesced.append(call_binary("coalesce", ci, get_zero()))
              
              res = coalesced[0]
              for next_expr in coalesced[1:]:
                   res = call_binary("add", res, next_expr)
              return res

         elif isinstance(op.aggregation, agg_ops.MinOp):
              res = casted_inputs[0]
              for next_expr in casted_inputs[1:]:
                   res = call_binary("least", res, next_expr)
              return res

         elif isinstance(op.aggregation, agg_ops.MaxOp):
              res = casted_inputs[0]
              for next_expr in casted_inputs[1:]:
                   res = call_binary("greatest", res, next_expr)
              return res

         elif isinstance(op.aggregation, agg_ops.MeanOp):
              coalesced = []
              for ci in casted_inputs:
                   coalesced.append(call_binary("coalesce", ci, get_zero()))
              sum_expr = coalesced[0]
              for next_expr in coalesced[1:]:
                   sum_expr = call_binary("add", sum_expr, next_expr)
                   
              counts = []
              for ci in compiled_inputs:
                   is_not_null_expr = call_unary("is_not_null", ci)
                   counts.append(cast_expr(is_not_null_expr, dtypes.INT_DTYPE))
                   
              count_expr = counts[0]
              for next_expr in counts[1:]:
                   count_expr = call_binary("add", count_expr, next_expr)
                   
              zero_i64 = algebra_pb2.Expression()
              zero_i64.literal.i64 = 0
              denom = call_binary("nullif", count_expr, zero_i64)
              sum_float = cast_expr(sum_expr, dtypes.FLOAT_DTYPE)
              denom_float = cast_expr(denom, dtypes.FLOAT_DTYPE)
              return call_binary("divide", sum_float, denom_float)

         elif isinstance(op.aggregation, (agg_ops.VarOp, agg_ops.PopVarOp, agg_ops.StdOp)):
              coalesced = []
              for ci in casted_inputs:
                   coalesced.append(call_binary("coalesce", ci, get_zero()))
              sum_expr = coalesced[0]
              for next_expr in coalesced[1:]:
                   sum_expr = call_binary("add", sum_expr, next_expr)
                   
              counts = []
              for ci in compiled_inputs:
                   is_not_null_expr = call_unary("is_not_null", ci)
                   counts.append(cast_expr(is_not_null_expr, dtypes.INT_DTYPE))
                   
              count_expr = counts[0]
              for next_expr in counts[1:]:
                   count_expr = call_binary("add", count_expr, next_expr)
                   
              zero_i64 = algebra_pb2.Expression()
              zero_i64.literal.i64 = 0
              denom = call_binary("nullif", count_expr, zero_i64)
              sum_float = cast_expr(sum_expr, dtypes.FLOAT_DTYPE)
              denom_float = cast_expr(denom, dtypes.FLOAT_DTYPE)
              mean_expr = call_binary("divide", sum_float, denom_float)
              
              sq_diffs = []
              for ci in casted_inputs:
                   diff = call_binary("subtract", ci, mean_expr)
                   sq_diff = call_binary("multiply", diff, diff)
                   
                   zero_float = algebra_pb2.Expression()
                   zero_float.literal.fp64 = 0.0
                   sq_diffs.append(call_binary("coalesce", sq_diff, zero_float))
                   
              sum_sq_diff = sq_diffs[0]
              for next_expr in sq_diffs[1:]:
                   sum_sq_diff = call_binary("add", sum_sq_diff, next_expr)
                   
              if isinstance(op.aggregation, agg_ops.PopVarOp):
                   denom_var = call_binary("nullif", count_expr, zero_i64)
              else:
                   one_i64 = algebra_pb2.Expression()
                   one_i64.literal.i64 = 1
                   count_minus_one = call_binary("subtract", count_expr, one_i64)
                   denom_var = call_binary("nullif", count_minus_one, zero_i64)
              denom_var_float = cast_expr(denom_var, dtypes.FLOAT_DTYPE)
              var_expr = call_binary("divide", sum_sq_diff, denom_var_float)
              
              if isinstance(op.aggregation, agg_ops.StdOp):
                   return call_unary("sqrt", var_expr)
              return var_expr

         else:
              raise NotImplementedError(f"Array reduction aggregate {type(op.aggregation)} not supported in Substrait compiler yet")
