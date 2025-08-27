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

from bigframes.core import array_value
import bigframes.operations as ops
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_str_contains(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.StrContainsOp("(?i)hEllo").as_expr("string_col"),
            ops.StrContainsOp("Hello").as_expr("string_col"),
            ops.StrContainsOp("T").as_expr("string_col"),
            ops.StrContainsOp(".*").as_expr("string_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_str_contains_regex(
    scalars_array_value: array_value.ArrayValue, engine
):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.StrContainsRegexOp("(?i)hEllo").as_expr("string_col"),
            ops.StrContainsRegexOp("Hello").as_expr("string_col"),
            ops.StrContainsRegexOp("T").as_expr("string_col"),
            ops.StrContainsRegexOp(".*").as_expr("string_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_str_startswith(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.StartsWithOp("He").as_expr("string_col"),
            ops.StartsWithOp("llo").as_expr("string_col"),
            ops.StartsWithOp(("He", "T", "ca")).as_expr("string_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_str_endswith(scalars_array_value: array_value.ArrayValue, engine):
    arr, _ = scalars_array_value.compute_values(
        [
            ops.EndsWithOp("!").as_expr("string_col"),
            ops.EndsWithOp("llo").as_expr("string_col"),
            ops.EndsWithOp(("He", "T", "ca")).as_expr("string_col"),
        ]
    )
    assert_equivalence_execution(arr.node, REFERENCE_ENGINE, engine)
