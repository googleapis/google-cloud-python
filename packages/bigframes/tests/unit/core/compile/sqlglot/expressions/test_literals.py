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

import bigframes.core.expression as ex
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_float_literals(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    ops_map = {
        "inf": ex.const(float("inf")),
        "ninf": ex.const(float("-inf")),
        "nan": ex.const(float("nan")),
        "neg_zero": ex.const(-0.0),
        "0.00001": ex.const(0.00001),
        "1E-10": ex.const(1e-10),
    }
    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")
