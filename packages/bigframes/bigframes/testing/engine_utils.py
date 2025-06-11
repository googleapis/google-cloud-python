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

from bigframes.core import nodes
from bigframes.session import semi_executor


def assert_equivalence_execution(
    node: nodes.BigFrameNode,
    engine1: semi_executor.SemiExecutor,
    engine2: semi_executor.SemiExecutor,
):
    e1_result = engine1.execute(node, ordered=True)
    e2_result = engine2.execute(node, ordered=True)
    assert e1_result is not None
    assert e2_result is not None
    # Schemas might have extra nullity markers, normalize to node expected schema, which should be looser
    e1_table = e1_result.to_arrow_table().cast(node.schema.to_pyarrow())
    e2_table = e2_result.to_arrow_table().cast(node.schema.to_pyarrow())
    assert e1_table.equals(e2_table), f"{e1_table} is not equal to {e2_table}"
