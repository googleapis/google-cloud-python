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


def test_obj_fetch_metadata(scalar_types_df: bpd.DataFrame, snapshot):
    blob_s = scalar_types_df["string_col"].str.to_blob()
    sql = blob_s.blob.version().to_frame().sql
    snapshot.assert_match(sql, "out.sql")


def test_obj_get_access_url(scalar_types_df: bpd.DataFrame, snapshot):
    blob_s = scalar_types_df["string_col"].str.to_blob()
    sql = blob_s.blob.read_url().to_frame().sql
    snapshot.assert_match(sql, "out.sql")


def test_obj_make_ref(scalar_types_df: bpd.DataFrame, snapshot):
    blob_df = scalar_types_df["string_col"].str.to_blob()
    snapshot.assert_match(blob_df.to_frame().sql, "out.sql")
