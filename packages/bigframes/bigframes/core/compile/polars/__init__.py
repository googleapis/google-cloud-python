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

"""Compiler for BigFrames expression to Polars LazyFrame expression.

Make sure to import all polars implementations here so that they get registered.
"""
from __future__ import annotations

import warnings

# The ops imports appear first so that the implementations can be registered.
# polars shouldn't be needed at import time, as register is a no-op if polars
# isn't installed.
import bigframes.core.compile.polars.operations.generic_ops  # noqa: F401
import bigframes.core.compile.polars.operations.numeric_ops  # noqa: F401
import bigframes.core.compile.polars.operations.struct_ops  # noqa: F401

try:
    import bigframes._importing

    # Use import_polars() instead of importing directly so that we check the
    # version numbers.
    bigframes._importing.import_polars()

    from bigframes.core.compile.polars.compiler import PolarsCompiler

    __all__ = ["PolarsCompiler"]
except Exception as exc:
    msg = f"Polars compiler not available as there was an exception importing polars. Details: {str(exc)}"
    warnings.warn(msg)
