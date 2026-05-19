# Copyright 2026 Google LLC
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

#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: scripts/data/sql-functions/aead.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from typing import cast

import pytest

import bigframes.bigquery._operations.aead as aead
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_decrypt_bytes(scalar_types_df: bpd.DataFrame, snapshot):
    result = aead.decrypt_bytes(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
    ).to_frame()
    snapshot.assert_match(result.sql, "out.sql")


def test_decrypt_string(scalar_types_df: bpd.DataFrame, snapshot):
    result = aead.decrypt_string(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()
    snapshot.assert_match(result.sql, "out.sql")


def test_encrypt(scalar_types_df: bpd.DataFrame, snapshot):
    result = aead.encrypt(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
    ).to_frame()
    snapshot.assert_match(result.sql, "out.sql")
