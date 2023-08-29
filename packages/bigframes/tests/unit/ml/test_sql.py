# Copyright 2023 Google LLC
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

import bigframes.ml.sql as ml_sql


def test_options_produces_correct_sql():
    sql = ml_sql.options(model_type="lin_reg", input_label_cols=["col_a"], l1_reg=0.6)
    assert (
        sql
        == """OPTIONS(
  model_type="lin_reg",
  input_label_cols=["col_a"],
  l1_reg=0.6)"""
    )


def test_transform_produces_correct_sql():
    sql = ml_sql.transform(
        "ML.STANDARD_SCALER(col_a) OVER(col_a) AS scaled_col_a",
        "ML.ONE_HOT_ENCODER(col_b) OVER(col_b) AS encoded_col_b",
    )
    assert (
        sql
        == """TRANSFORM(
  ML.STANDARD_SCALER(col_a) OVER(col_a) AS scaled_col_a,
  ML.ONE_HOT_ENCODER(col_b) OVER(col_b) AS encoded_col_b)"""
    )


def test_standard_scaler_produces_correct_sql():
    sql = ml_sql.ml_standard_scaler("col_a", "scaled_col_a")
    assert sql == "ML.STANDARD_SCALER(col_a) OVER() AS scaled_col_a"


def test_one_hot_encoder_produces_correct_sql():
    sql = ml_sql.ml_one_hot_encoder("col_a", "none", 1000000, 0, "encoded_col_a")
    assert (
        sql == "ML.ONE_HOT_ENCODER(col_a, 'none', 1000000, 0) OVER() AS encoded_col_a"
    )


def test_create_model_produces_correct_sql():
    sql = ml_sql.create_model(
        model_name="my_dataset.my_model",
        source_sql="my_source_sql",
        options_sql="my_options_sql",
    )
    assert (
        sql
        == """CREATE TEMP MODEL `my_dataset.my_model`
my_options_sql
AS my_source_sql"""
    )


def test_create_model_transform_produces_correct_sql():
    sql = ml_sql.create_model(
        model_name="my_model",
        source_sql="my_source_sql",
        options_sql="my_options_sql",
        transform_sql="my_transform_sql",
    )
    assert (
        sql
        == """CREATE TEMP MODEL `my_model`
my_transform_sql
my_options_sql
AS my_source_sql"""
    )


def test_create_remote_model_produces_correct_sql():
    sql = ml_sql.create_remote_model(
        model_name="my_model",
        connection_name="my_project.us.my_connection",
        options_sql="my_options_sql",
    )
    assert (
        sql
        == """CREATE TEMP MODEL `my_model`
REMOTE WITH CONNECTION `my_project.us.my_connection`
my_options_sql"""
    )


def test_create_imported_model_produces_correct_sql():
    sql = ml_sql.create_imported_model(
        model_name="my_model",
        options_sql="my_options_sql",
    )
    assert (
        sql
        == """CREATE TEMP MODEL `my_model`
my_options_sql"""
    )


def test_alter_model_correct_sql():
    sql = ml_sql.alter_model(
        model_name="my_dataset.my_model",
        options_sql="my_options_sql",
    )
    assert (
        sql
        == """ALTER MODEL `my_dataset.my_model`
SET my_options_sql"""
    )


def test_ml_predict_produces_correct_sql():
    sql = ml_sql.ml_predict(
        model_name="my_dataset.my_model", source_sql="SELECT * FROM my_table"
    )
    assert (
        sql
        == """SELECT * FROM ML.PREDICT(MODEL `my_dataset.my_model`,
  (SELECT * FROM my_table))"""
    )


def test_ml_evaluate_produces_correct_sql():
    sql = ml_sql.ml_evaluate(
        model_name="my_dataset.my_model", source_sql="SELECT * FROM my_table"
    )
    assert (
        sql
        == """SELECT * FROM ML.EVALUATE(MODEL `my_dataset.my_model`,
  (SELECT * FROM my_table))"""
    )


def test_ml_evaluate_no_source_produces_correct_sql():
    sql = ml_sql.ml_evaluate(model_name="my_dataset.my_model")
    assert sql == """SELECT * FROM ML.EVALUATE(MODEL `my_dataset.my_model`)"""


def test_ml_centroids_produces_correct_sql():
    sql = ml_sql.ml_centroids(model_name="my_dataset.my_model")
    assert sql == """SELECT * FROM ML.CENTROIDS(MODEL `my_dataset.my_model`)"""


def test_ml_generate_text_produces_correct_sql():
    sql = ml_sql.ml_generate_text(
        model_name="my_dataset.my_model",
        source_sql="SELECT * FROM my_table",
        struct_options="STRUCT(value AS item)",
    )
    assert (
        sql
        == """SELECT * FROM ML.GENERATE_TEXT(MODEL `my_dataset.my_model`,
  (SELECT * FROM my_table), STRUCT(value AS item))"""
    )


def test_ml_principal_components_produces_correct_sql():
    sql = ml_sql.ml_principal_components(model_name="my_dataset.my_model")
    assert (
        sql == """SELECT * FROM ML.PRINCIPAL_COMPONENTS(MODEL `my_dataset.my_model`)"""
    )


def test_ml_principal_component_info_produces_correct_sql():
    sql = ml_sql.ml_principal_component_info(model_name="my_dataset.my_model")
    assert (
        sql
        == """SELECT * FROM ML.PRINCIPAL_COMPONENT_INFO(MODEL `my_dataset.my_model`)"""
    )
