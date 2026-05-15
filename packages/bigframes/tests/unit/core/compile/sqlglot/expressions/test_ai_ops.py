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


def _construct_prompt(col_name, context):
    import bigframes.core.expression as ex
    elements = []
    for elem in context:
        if elem is None:
            elements.append(col_name)
        else:
            elements.append(ex.const(elem))
            
    struct_names = tuple(f"_field_{i+1}" for i in range(len(elements)))
    return ops.StructOp(column_names=struct_names).as_expr(*elements)


def test_ai_generate(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    op = ops.googlesql.AIGenerateOp()
    expr = op.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
        request_type="SHARED",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_connection_id(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    op = ops.googlesql.AIGenerateOp()
    expr = op.as_expr(
        prompt_expr,
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_output_schema(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    output_schema_str = "x INT64, y FLOAT64"
    op = ops.googlesql.AIGenerateOp(output_schema=output_schema_str)
    expr = op.as_expr(
        prompt_expr,
        connection_id=None,
        endpoint="gemini-2.5-flash",
        output_schema=output_schema_str,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_with_model_param(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    op = ops.googlesql.AIGenerateOp()
    expr = op.as_expr(
        prompt_expr,
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_BOOL.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_BOOL.as_expr(
        prompt_expr,
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_bool_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_BOOL.as_expr(
        prompt_expr,
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_INT.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_INT.as_expr(
        prompt_expr,
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_int_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_INT.as_expr(
        prompt_expr,
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_DOUBLE.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double_with_connection_id(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_DOUBLE.as_expr(
        prompt_expr,
        connection_id=CONNECTION_ID,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_generate_double_with_model_param(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_GENERATE_DOUBLE.as_expr(
        prompt_expr,
        model_params=json.dumps(dict()),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_embed(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_EMBED.as_expr(
        col_name,
        endpoint="text-embedding-005",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_connection_id(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_EMBED.as_expr(
        col_name,
        endpoint="text-embedding-005",
        connection_id=CONNECTION_ID,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_model(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_EMBED.as_expr(
        col_name,
        model="embeddinggemma-300m",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_embed_with_task_type_and_title(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    expr = ops.googlesql.AI_EMBED.as_expr(
        col_name,
        endpoint="text-embedding-005",
        task_type="RETRIEVAL_DOCUMENT",
        title="My Document",
        model_params=json.dumps({"outputDimensionality": 256}),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_if(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_IF.as_expr(
        prompt_expr,
        connection_id=connection_id,
        optimization_mode="MINIMIZE_COST",
        max_error_ratio=0.5,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_if_with_endpoint(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_IF.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_classify(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"

    expr = ops.googlesql.AI_CLASSIFY.as_expr(
        col_name,
        categories=("greeting", "rejection"),
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_classify_with_params(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_CLASSIFY.as_expr(
        col_name,
        categories=("greeting", "rejection"),
        examples=[{"input": "hi", "output": "greeting"}, {"input": "bye", "output": "rejection"}],
        endpoint="gemini-2.5-flash",
        max_error_ratio=0.1,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_classify_with_output_mode(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_CLASSIFY.as_expr(
        col_name,
        categories=("greeting", "rejection"),
        output_mode="multi",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_classify_multi_with_list_examples(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"

    examples = [
        {"input": "hi", "output": ["greeting", "positive"]},
        {"input": "bye", "output": ["rejection", "negative"]},
    ]
    expr = ops.googlesql.AI_CLASSIFY.as_expr(
        col_name,
        categories=("greeting", "rejection"),
        examples=examples,
        output_mode="multi",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_score(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_SCORE.as_expr(
        prompt_expr,
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_score_with_endpoint_and_max_error_ratio(
    scalar_types_df: dataframe.DataFrame, snapshot
):
    col_name = "string_col"
    prompt_expr = _construct_prompt(col_name, (None, " is the same as ", None))

    expr = ops.googlesql.AI_SCORE.as_expr(
        prompt_expr,
        endpoint="gemini-2.5-flash",
        max_error_ratio=0.5,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


@pytest.mark.parametrize("connection_id", [None, CONNECTION_ID])
def test_ai_similarity(scalar_types_df: dataframe.DataFrame, snapshot, connection_id):
    col_name = "string_col"

    expr = ops.googlesql.AI_SIMILARITY.as_expr(
        content1=col_name,
        content2=col_name,
        endpoint="text-embedding-005",
        connection_id=connection_id,
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_similarity_with_model(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_SIMILARITY.as_expr(
        content1=col_name,
        content2=col_name,
        model="embeddinggemma-300m",
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")


def test_ai_similarity_with_model_param(scalar_types_df: dataframe.DataFrame, snapshot):
    col_name = "string_col"

    expr = ops.googlesql.AI_SIMILARITY.as_expr(
        content1=col_name,
        content2=col_name,
        endpoint="text-embedding-005",
        model_params=json.dumps({"outputDimensionality": 256}),
    )

    sql = utils._apply_ops_to_sql(scalar_types_df, [expr], ["result"])
    snapshot.assert_match(sql, "out.sql")
