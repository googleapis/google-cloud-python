# Copyright 2023 Google LLC
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

from typing import Literal

from bigframes.core.compile.api import test_only_ibis_inferred_schema
from bigframes.core.compile.configs import CompileRequest, CompileResult


def compile_sql(
    request: CompileRequest,
    compiler_name: Literal["sqlglot", "ibis"] = "sqlglot",
) -> CompileResult:
    """Compiles a BigFrameNode according to the request into SQL."""
    if compiler_name == "sqlglot":
        import bigframes.core.compile.sqlglot.compiler as sqlglot_compiler

        return sqlglot_compiler.compile_sql(request)
    else:
        import bigframes.core.compile.ibis_compiler.ibis_compiler as ibis_compiler

        return ibis_compiler.compile_sql(request)


__all__ = [
    "test_only_ibis_inferred_schema",
    "CompileRequest",
    "CompileResult",
    "compile_sql",
]
