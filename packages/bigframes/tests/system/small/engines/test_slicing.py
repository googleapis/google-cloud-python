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

from bigframes.core import array_value, nodes
from bigframes.session import polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq"], indirect=True)
@pytest.mark.parametrize(
    ("start", "stop", "step"),
    [
        (1, None, None),
        (None, 4, None),
        (None, None, 2),
        (None, 50_000_000_000, 1),
        (5, 4, None),
        (3, None, 2),
        (1, 7, 2),
        (1, 7, 50_000_000_000),
        (-1, -7, -2),
        (None, -7, -2),
        (-1, None, -2),
        (-7, -1, 2),
        (-7, -1, None),
        (-7, 7, None),
        (7, -7, -2),
    ],
)
def test_engines_slice(
    scalars_array_value: array_value.ArrayValue,
    engine,
    start,
    stop,
    step,
):
    node = nodes.SliceNode(scalars_array_value.node, start, stop, step)
    assert_equivalence_execution(node, REFERENCE_ENGINE, engine)
