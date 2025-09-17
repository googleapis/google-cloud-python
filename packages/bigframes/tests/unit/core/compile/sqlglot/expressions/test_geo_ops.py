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


def test_geo_area(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.geo_area_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_astext(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_astext_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_boundary(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_boundary_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_buffer(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.GeoStBufferOp(1.0, 8.0, False).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_centroid(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_centroid_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_convexhull(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_convexhull_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_geogfromtext(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_geogfromtext_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_isclosed(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.geo_st_isclosed_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_st_length(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.GeoStLengthOp(True).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_geo_x(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.geo_x_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_geo_y(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "geography_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.geo_y_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")
