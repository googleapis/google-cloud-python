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

import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_compile_join(scalar_types_df: bpd.DataFrame, snapshot):
    left = scalar_types_df[["int64_col"]]
    right = scalar_types_df.set_index("int64_col")[["int64_too"]]
    join = left.join(right)
    snapshot.assert_match(join.sql, "out.sql")


def test_compile_join_w_how(scalar_types_df: bpd.DataFrame):
    left = scalar_types_df[["int64_col"]]
    right = scalar_types_df.set_index("int64_col")[["int64_too"]]

    join_sql = left.join(right, how="left").sql
    assert "LEFT JOIN" in join_sql
    assert "ON" in join_sql

    join_sql = left.join(right, how="right").sql
    assert "RIGHT JOIN" in join_sql
    assert "ON" in join_sql

    join_sql = left.join(right, how="outer").sql
    assert "FULL OUTER JOIN" in join_sql
    assert "ON" in join_sql

    join_sql = left.join(right, how="inner").sql
    assert "INNER JOIN" in join_sql
    assert "ON" in join_sql

    join_sql = left.merge(right, how="cross").sql
    assert "CROSS JOIN" in join_sql
    assert "ON" not in join_sql


@pytest.mark.parametrize(
    ("on"),
    ["bool_col", "int64_col", "float64_col", "string_col", "time_col", "numeric_col"],
)
def test_compile_join_w_on(scalar_types_df: bpd.DataFrame, on: str, snapshot):
    df = scalar_types_df[["rowindex", on]]
    merge = df.merge(df, left_on=on, right_on=on)
    snapshot.assert_match(merge.sql, "out.sql")
