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

import sys

import pytest

import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")

if sys.version_info < (3, 12):
    pytest.skip(
        "Skipping test due to inconsistent SQL formatting on Python < 3.12.",
        allow_module_level=True,
    )


def test_compile_isin(scalar_types_df: bpd.DataFrame, snapshot):
    bf_isin = scalar_types_df["int64_col"].isin(scalar_types_df["int64_too"]).to_frame()
    snapshot.assert_match(bf_isin.sql, "out.sql")


def test_compile_isin_not_nullable(scalar_types_df: bpd.DataFrame, snapshot):
    bf_isin = (
        scalar_types_df["rowindex_2"].isin(scalar_types_df["rowindex_2"]).to_frame()
    )
    snapshot.assert_match(bf_isin.sql, "out.sql")
