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

from bigframes import operations as ops
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_struct_field(nested_structs_types_df: bpd.DataFrame, snapshot):
    col_name = "people"
    bf_df = nested_structs_types_df[[col_name]]

    ops_map = {
        # When a name string is provided.
        "string": ops.StructFieldOp("name").as_expr(col_name),
        # When an index integer is provided.
        "int": ops.StructFieldOp(0).as_expr(col_name),
    }
    sql = utils._apply_unary_ops(bf_df, list(ops_map.values()), list(ops_map.keys()))

    snapshot.assert_match(sql, "out.sql")
