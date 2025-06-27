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


def test_compile_readtable(scalar_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(scalar_types_df.sql, "out.sql")


def test_compile_readtable_w_repeated_types(repeated_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(repeated_types_df.sql, "out.sql")


def test_compile_readtable_w_nested_structs_types(
    nested_structs_types_df: bpd.DataFrame, snapshot
):
    snapshot.assert_match(nested_structs_types_df.sql, "out.sql")


def test_compile_readtable_w_json_types(json_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(json_types_df.sql, "out.sql")


def test_compile_readtable_w_ordering(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df = bf_df.sort_values("int64_col")
    snapshot.assert_match(bf_df.sql, "out.sql")


def test_compile_readtable_w_limit(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df = bf_df.sort_index().head(10)
    snapshot.assert_match(bf_df.sql, "out.sql")
