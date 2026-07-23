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


import pytest

import bigframes.operations.googlesql as gsql_ops
from bigframes.core import array_value
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

polars = pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


def test_engines_googlesql_st_area(
    scalars_array_value: array_value.ArrayValue, bq_engine, sqlglot_engine
):
    expr = gsql_ops.ST_AREA.as_expr("geography_col")

    arr, _ = scalars_array_value.compute_values([expr])

    assert_equivalence_execution(arr.node, bq_engine, sqlglot_engine)
