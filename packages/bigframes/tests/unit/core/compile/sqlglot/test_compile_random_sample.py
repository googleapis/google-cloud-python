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

from bigframes.core import nodes
import bigframes.core as core
import bigframes.core.compile.sqlglot as sqlglot

pytest.importorskip("pytest_snapshot")


def test_compile_random_sample(
    scalar_types_array_value: core.ArrayValue,
    snapshot,
):
    """This test verifies the SQL compilation of a RandomSampleNode.

    Because BigFrames doesn't expose a public API for creating a random sample
    operation, this test constructs the node directly and then compiles it to SQL.
    """
    node = nodes.RandomSampleNode(scalar_types_array_value.node, fraction=0.1)
    sql = sqlglot.compiler.SQLGlotCompiler().compile(node)
    snapshot.assert_match(sql, "out.sql")
