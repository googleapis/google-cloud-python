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

import dataclasses
import typing

import bigframes.core
import bigframes.core.compile.sqlglot as sqlglot
import bigframes.session.executor


@dataclasses.dataclass
class SQLCompilerExecutor(bigframes.session.executor.Executor):
    """Executor for SQL compilation using sqlglot."""

    compiler = sqlglot

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: typing.Optional[str] = None,
        ordered: bool = True,
        enable_cache: bool = False,
    ) -> str:
        if offset_column:
            array_value, _ = array_value.promote_offsets()

        # Compared with BigQueryCachingExecutor, SQLCompilerExecutor skips
        # caching the subtree.
        return self.compiler.SQLGlotCompiler().compile(
            array_value.node, ordered=ordered
        )
