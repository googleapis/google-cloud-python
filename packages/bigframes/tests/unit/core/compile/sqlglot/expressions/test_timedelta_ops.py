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


def test_to_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df["duration_us"] = bpd.to_timedelta(bf_df["int64_col"], "us")
    bf_df["duration_s"] = bpd.to_timedelta(bf_df["int64_col"], "s")
    bf_df["duration_w"] = bpd.to_timedelta(bf_df["int64_col"], "W")

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_timedelta_floor(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.timedelta_floor_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")
