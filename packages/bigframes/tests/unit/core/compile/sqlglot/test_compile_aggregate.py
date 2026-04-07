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


def test_compile_aggregate(scalar_types_df: bpd.DataFrame, snapshot):
    result = scalar_types_df["int64_too"].groupby(scalar_types_df["bool_col"]).sum()
    snapshot.assert_match(result.to_frame().sql, "out.sql")


def test_compile_aggregate_wo_dropna(scalar_types_df: bpd.DataFrame, snapshot):
    result = (
        scalar_types_df["int64_too"]
        .groupby(scalar_types_df["bool_col"], dropna=False)
        .sum()
    )
    snapshot.assert_match(result.to_frame().sql, "out.sql")
