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

from bigframes.core import array_value, ordering
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_concat_self(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    result = scalars_array_value.concat([scalars_array_value, scalars_array_value])

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
def test_engines_concat_filtered_sorted(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    input_1 = scalars_array_value.select_columns(["float64_col", "int64_col"]).order_by(
        [ordering.ascending_over("int64_col")]
    )
    input_2 = scalars_array_value.filter_by_id("bool_col").select_columns(
        ["float64_col", "int64_too"]
    )

    result = input_1.concat([input_2, input_1, input_2])

    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)
