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
# This file was generated from: scripts/data/sql-functions/global_namespace/array.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from typing import cast

import pytest

import bigframes.bigquery._operations.global_namespace.array as array
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_array_concat(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_concat(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_first(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_first(
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_first_n(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_first_n(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_includes(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_includes(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_includes_all(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_includes_all(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_includes_any(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_includes_any(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_is_distinct(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_is_distinct(
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_last(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_last(
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_length(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_length(
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_reverse(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_reverse(
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_slice(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_slice(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_array_to_string(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.array_to_string(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
        cast(bpd.Series, scalar_types_df["bytes_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_flatten(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.flatten(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")


def test_generate_array(scalar_types_df: bpd.DataFrame, snapshot):
    result = array.generate_array(
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
        cast(bpd.Series, scalar_types_df["string_col"]),
    ).to_frame()

    snapshot.assert_match(result.sql.rstrip() + "\n", "out.sql")
