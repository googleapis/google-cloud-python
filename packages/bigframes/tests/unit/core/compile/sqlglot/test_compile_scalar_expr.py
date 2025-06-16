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

import bigframes

pytest.importorskip("pytest_snapshot")


def test_compile_numerical_add(compiler_session: bigframes.Session, snapshot):
    bf_df = compiler_session.read_gbq_table("test-project.test_dataset.test_table")
    bf_df["int64_col"] = bf_df["int64_col"] + bf_df["int64_col"]
    snapshot.assert_match(bf_df.sql, "out.sql")


def test_compile_string_add(compiler_session: bigframes.Session, snapshot):
    bf_df = compiler_session.read_gbq_table("test-project.test_dataset.test_table")
    bf_df["string_col"] = bf_df["string_col"] + "a"
    snapshot.assert_match(bf_df.sql, "out.sql")
