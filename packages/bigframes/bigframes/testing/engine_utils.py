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

import pandas.testing

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
    # Convert to pandas, as pandas has better comparison utils than arrow
    assert e1_result.schema == e2_result.schema
    e1_table = e1_result.to_pandas()
    e2_table = e2_result.to_pandas()
    pandas.testing.assert_frame_equal(e1_table, e2_table, rtol=1e-10)
