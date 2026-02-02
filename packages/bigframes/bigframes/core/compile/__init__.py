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

from typing import Any

from bigframes import options
from bigframes.core.compile.api import test_only_ibis_inferred_schema
from bigframes.core.compile.configs import CompileRequest, CompileResult


def compiler() -> Any:
    """Returns the appropriate compiler module based on session options."""
    if options.experiments.sql_compiler == "experimental":
        import bigframes.core.compile.sqlglot.compiler as sqlglot_compiler

        return sqlglot_compiler
    else:
        import bigframes.core.compile.ibis_compiler.ibis_compiler as ibis_compiler

        return ibis_compiler


__all__ = [
    "test_only_ibis_inferred_schema",
    "CompileRequest",
    "CompileResult",
    "compiler",
]
