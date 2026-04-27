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

import json

import pytest

from bigframes import dataframe
from bigframes import operations as ops
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")

CONNECTION_ID = "bigframes-dev.us.bigframes-default-connection"


def test_ai_generate(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
        output_schema=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_connection_id(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
        output_schema=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_output_schema(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
        output_schema="x INT64, y FLOAT64",
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_model_param(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerate(
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
        output_schema=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateBool(
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateBool(
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateBool(
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateInt(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateInt(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateInt(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIGenerateDouble(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateDouble(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
        request_type="shared",
        model_params=None,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIGenerateDouble(
        # The prompt does not make semantic sense but we only care about syntax correctness.
        prompt_context=(None, " is the same as ", None),
        connection_id=None,
        endpoint=None,
        request_type="shared",
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


def test_ai_embed(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIEmbed(
        endpoint="text-embedding-005",
        model=None,
        task_type=None,
        title=None,
        model_params=None,
        connection_id=None,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_connection_id(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIEmbed(
        endpoint="text-embedding-005",
        model=None,
        task_type=None,
        title=None,
        model_params=None,
        connection_id=CONNECTION_ID,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_model(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    op = ops.AIEmbed(
        endpoint=None,
        model="embeddinggemma-300m",
        task_type=None,
        title=None,
        model_params=None,
        connection_id=None,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_task_type_and_title(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    op = ops.AIEmbed(
        endpoint="text-embedding-005",
        model=None,
        task_type="retrieval_document",
        title="My Document",
        model_params=json.dumps({"outputDimensionality": 256}),
        connection_id=None,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_if(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"

    op = ops.AIIf(
        prompt_context=(None, " is the same as ", None),
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_classify(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"

    op = ops.AIClassify(
        prompt_context=(None,),
        categories=("greeting", "rejection"),
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [op.as_expr(col_name)], ["result"])

    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_score(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"

    op = ops.AIScore(
        prompt_context=(None, " is the same as ", None),
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(
        scalar_types_df, [op.as_expr(col_name, col_name)], ["result"]
    )

    snapshot.assert_match(sql, "out.sql")
