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

import os
import re
import threading
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple

import google.cloud.bigquery as bigquery

import bigframes.dtypes
import bigframes.session.executor as executor
from bigframes.core.expression import Parameter

if TYPE_CHECKING:
    import bigframes.core
    import bigframes.core.schema
    import bigframes.session.execution_spec as ex_spec


class ProductionizeBlockedError(RuntimeError):
    """Exception raised when an operation attempts immediate execution or data download in productionize mode."""

    pass


class ProductionizeState(threading.local):
    def __init__(self):
        super().__init__()
        self.active: bool = False
        self.pipeline: Optional[PipelineDefinition] = None


# Thread-local state singleton
_state = ProductionizeState()


class MockQueryJob:
    """A mock BigQuery QueryJob that only exposes the destination table."""

    def __init__(self, destination: bigquery.TableReference):
        self.destination = destination


class MockExecuteResult(executor.ExecuteResult):
    """A mock ExecuteResult returned during productionize interception."""

    def __init__(
        self,
        destination_table: Optional[bigquery.TableReference],
        schema: bigframes.core.schema.ArraySchema,
    ):
        self._schema = schema
        self._query_job = MockQueryJob(destination_table) if destination_table else None
        self._metadata = executor.ExecutionMetadata(
            query_job=self._query_job,
            bytes_processed=0,
        )

    @property
    def execution_metadata(self) -> executor.ExecutionMetadata:
        return self._metadata

    @property
    def schema(self) -> bigframes.core.schema.ArraySchema:
        return self._schema

    def batches(self, sample_rate: Optional[float] = None) -> executor.ResultsIterator:
        return executor.ResultsIterator(iter([]), self._schema, 0, 0)


class PipelineDefinition:
    """Context manager and recorder for a productionized BigQuery DataFrames pipeline."""

    def __init__(self, session: bigframes.session.Session):
        self.session = session
        # Maps target table name (str) -> Tuple[ArrayValue, TableOutputSpec]
        self.recorded_writes: Dict[
            str, Tuple[bigframes.core.ArrayValue, ex_spec.TableOutputSpec]
        ] = {}
        # List of GCS export specs and their corresponding ArrayValues
        self.recorded_exports: List[
            Tuple[ex_spec.GcsOutputSpec, bigframes.core.ArrayValue]
        ] = []
        # Maps UDF routine name (str) -> UDF DDL (str)
        self.recorded_udfs: Dict[str, str] = {}
        # Maps Ibis parameter name (str) -> User parameter name (str)
        self.recorded_params: Dict[str, str] = {}

    def __enter__(self) -> PipelineDefinition:
        self._prev_active = _state.active
        self._prev_pipeline = _state.pipeline

        _state.active = True
        _state.pipeline = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _state.active = self._prev_active
        _state.pipeline = self._prev_pipeline

    def _build_dependency_graph(self) -> Tuple[List[str], Dict[str, Set[str]]]:
        """Builds the dependency graph and returns the topologically sorted tables."""
        dependencies = {table: set() for table in self.recorded_writes}

        for table, (array_value, _) in self.recorded_writes.items():
            read_tables = _find_read_tables(array_value.node)
            for read_table in read_tables:
                if read_table in self.recorded_writes:
                    # table depends on read_table
                    dependencies[table].add(read_table)

        # Topological sort (DFS)
        visited = {}
        order = []

        def visit(node):
            if visited.get(node) == "visiting":
                raise ValueError(
                    f"Cyclic dependency detected in pipeline involving: {node}"
                )
            if visited.get(node) == "visited":
                return

            visited[node] = "visiting"
            for neighbor in dependencies.get(node, []):
                visit(neighbor)
            visited[node] = "visited"
            order.append(node)

        for node in dependencies:
            visit(node)

        return order, dependencies

    def to_sql(self) -> str:
        """Compiles the recorded pipeline into a single sequential SQL script."""
        if not self.recorded_writes and not self.recorded_udfs:
            return ""

        with self:
            order, _ = self._build_dependency_graph()
            statements = []

            # 1. Add UDF definitions
            for udf_ddl in self.recorded_udfs.values():
                statements.append(udf_ddl + ";")

            # 2. Add table creation statements
            for table_name in order:
                array_value, _ = self.recorded_writes[table_name]
                # Compile to SQL using the session's executor
                raw_sql = self.session._executor.to_sql(array_value, ordered=False)
                statements.append(
                    f"CREATE OR REPLACE TABLE `{table_name}` AS\n{raw_sql};"
                )

            sql = "\n\n".join(statements)

            # Rewrite Ibis-generated parameter names to user-defined names
            for ibis_name, user_name in self.recorded_params.items():
                sql = re.sub(rf"(?<!\w)@{ibis_name}(?!\w)", f"@{user_name}", sql)

            return sql

    def export_dataform(self, target_dir: str):
        """Exports the recorded pipeline as a local Dataform project in the target directory."""
        if not self.recorded_writes and not self.recorded_udfs:
            return

        with self:
            order, dependencies = self._build_dependency_graph()

            # Ensure the definitions directory exists
            defs_dir = os.path.join(target_dir, "definitions")
            os.makedirs(defs_dir, exist_ok=True)

            # 1. Export UDFs as Dataform operations
            udf_mapping = {}  # Maps routine name -> udf_id
            for routine_name, udf_ddl in self.recorded_udfs.items():
                parts = routine_name.split(".")
                udf_id = parts[-1]
                udf_mapping[routine_name] = udf_id

                config_block = (
                    f'config {{\n  type: "operations",\n  name: "{udf_id}"\n}}\n'
                )
                file_path = os.path.join(defs_dir, f"{udf_id}.sqlx")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(config_block)
                    f.write("\n")
                    f.write(udf_ddl)
                    f.write("\n")

            # 2. Export Tables
            for table_name in order:
                array_value, dest_spec = self.recorded_writes[table_name]

                # Parse the table name
                parts = table_name.split(".")
                if len(parts) == 3:
                    project_id, dataset_id, table_id = parts[0], parts[1], parts[2]
                elif len(parts) == 2:
                    project_id = self.session.bqclient.project
                    dataset_id, table_id = parts[0], parts[1]
                else:
                    raise ValueError(f"Invalid recorded table name: {table_name}")

                # Compile to SQL
                sql = self.session._executor.to_sql(array_value, ordered=False)

                # Rewrite Ibis-generated parameter names to Dataform variables
                for ibis_name, user_name in self.recorded_params.items():
                    sql = re.sub(
                        rf"(?<!\w)@{ibis_name}(?!\w)",
                        f"${{dataform.projectConfig.vars.{user_name}}}",
                        sql,
                    )

                # Rewrite query parameters to Dataform project variables (e.g. from SQLGlot)
                sql = _replace_parameter_refs(sql)

                # Identify table dependencies and rewrite their references to ${ref("...")}
                dep_table_ids = set()
                for dep_table in dependencies[table_name]:
                    dep_parts = dep_table.split(".")
                    dep_project, dep_dataset, dep_table_id = (
                        dep_parts[0],
                        dep_parts[1],
                        dep_parts[2],
                    )

                    # Replace the raw table reference in the SQL with the Dataform ref
                    sql = _replace_table_ref(
                        sql, dep_project, dep_dataset, dep_table_id
                    )
                    dep_table_ids.add(dep_table_id)

                # Identify UDF dependencies by scanning the SQL for UDF routine names or IDs
                for routine_name, udf_id in udf_mapping.items():
                    if (
                        routine_name.lower() in sql.lower()
                        or udf_id.lower() in sql.lower()
                    ):
                        dep_table_ids.add(udf_id)

                # Generate the Dataform config block
                df_type = "table"
                if dest_spec.if_exists == "append":
                    df_type = "incremental"
                elif dest_spec.if_exists == "fail":
                    df_type = "table"

                config_parts = [f'  type: "{df_type}",', f'  name: "{table_id}",']

                if dep_table_ids:
                    deps_str = ", ".join(f'"{d}"' for d in sorted(list(dep_table_ids)))
                    config_parts.append(f"  dependencies: [{deps_str}],")

                if dest_spec.cluster_cols:
                    cols_str = ", ".join(f'"{c}"' for c in dest_spec.cluster_cols)
                    config_parts.append(
                        f"  bigquery: {{\n    clustering: [{cols_str}]\n  }},"
                    )

                config_block = "config {\n" + "\n".join(config_parts) + "\n}\n"

                # Write the .sqlx file
                file_path = os.path.join(defs_dir, f"{table_id}.sqlx")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(config_block)
                    f.write("\n")
                    f.write(sql)
                    f.write("\n")


def _find_read_tables(node: bigframes.core.nodes.BigFrameNode) -> Set[str]:
    """Traverses the AST and returns a set of all fully qualified table names read by the query."""
    from bigframes.core.nodes import ReadTableNode

    def reduction(n, children_results):
        results = set()
        for child_res in children_results:
            results.update(child_res)
        if isinstance(n, ReadTableNode):
            table_ref = n.source.table
            table_name = (
                f"{table_ref.project_id}.{table_ref.dataset_id}.{table_ref.table_id}"
            )
            results.add(table_name)
        return results

    return node.reduce_up(reduction)


def _replace_table_ref(
    sql: str, project_id: str, dataset_id: str, table_id: str
) -> str:
    """Replaces raw BigQuery table references in SQL with Dataform ref() calls."""
    p = re.escape(project_id)
    d = re.escape(dataset_id)
    t = re.escape(table_id)

    patterns = [
        rf"`{p}\.{d}\.{t}`",
        rf"`{d}\.{t}`",
        rf"{p}\.{d}\.{t}",
        rf"{d}\.{t}",
    ]

    combined_pattern = "|".join(patterns)
    return re.sub(combined_pattern, f'${{ref("{table_id}")}}', sql, flags=re.IGNORECASE)


def intercept_execution(
    array_value: bigframes.core.ArrayValue,
    execution_spec: ex_spec.ExecutionSpec,
    pipeline: PipelineDefinition,
) -> executor.ExecuteResult:
    """Intercepts execution requests and records them or blocks them accordingly."""
    import bigframes.session.execution_spec as xs

    dest_spec = execution_spec.destination_spec
    if isinstance(dest_spec, xs.TableOutputSpec):
        # Record the write operation (store both array_value and dest_spec)
        table_ref = dest_spec.table
        table_name = f"{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}"
        pipeline.recorded_writes[table_name] = (array_value, dest_spec)

        # Return a mock result so the calling code (like to_gbq) believes it succeeded
        return MockExecuteResult(table_ref, array_value.schema)

    elif isinstance(dest_spec, xs.GcsOutputSpec):
        # Record the GCS export operation
        pipeline.recorded_exports.append((dest_spec, array_value))
        return MockExecuteResult(None, array_value.schema)

    elif isinstance(dest_spec, xs.EphemeralTableSpec):
        # Ephemeral tables are used for caching/staging. We block them to keep the pipeline static.
        raise ProductionizeBlockedError(
            "Caching or temporary table materialization (e.g., df.cache()) is not supported "
            "in productionize mode. Please define a pure, lazy data pipeline."
        )

    else:
        # No destination spec means we are trying to download data to Python (to_pandas, head, etc.)
        raise ProductionizeBlockedError(
            "Immediate execution/data downloading is disabled in productionize mode. "
            "You cannot call to_pandas(), head(), shape, or other data-fetching operations "
            "inside this context."
        )


def productionize() -> PipelineDefinition:
    """Enters a 'productionize' context where execution is deferred and compiled into a pipeline."""
    import bigframes.core.global_session as global_session

    return PipelineDefinition(global_session.get_global_session())


def parameter(name: str, dtype: Any) -> Parameter:
    """Define a parameter for the productionized pipeline.

    Args:
        name: The name of the parameter (will be used as @name in SQL).
        dtype: The type of the parameter (e.g. int, str, datetime.date).
    """
    bf_dtype = bigframes.dtypes.bigframes_type(dtype)
    return Parameter(name, bf_dtype)


def _replace_parameter_refs(sql: str) -> str:
    """Replaces BigQuery query parameters (@param) with Dataform project variables (${dataform.projectConfig.vars.param})."""
    return re.sub(
        r"(?<!\w)@([a-zA-Z_][a-zA-Z0-9_]*)", r"${dataform.projectConfig.vars.\1}", sql
    )
