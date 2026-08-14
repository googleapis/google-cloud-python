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


# TODO: check order by with offset
def test_compile_explode_series(repeated_types_df: bpd.DataFrame, snapshot):
    s = repeated_types_df["int_list_col"].explode()
    snapshot.assert_match(s.to_frame().sql, "out.sql")


def test_compile_explode_dataframe(repeated_types_df: bpd.DataFrame, snapshot):
    exploded_columns = ["int_list_col", "string_list_col"]
    df = repeated_types_df[["rowindex", *exploded_columns]].explode(exploded_columns)
    snapshot.assert_match(df.sql, "out.sql")
