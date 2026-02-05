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

import pytest

import bigframes.bigquery.ml as ml
import bigframes.pandas as bpd


@pytest.fixture(scope="session")
def embedding_model(bq_connection, dataset_id):
    model_name = f"{dataset_id}.embedding_model"
    return ml.create_model(
        model_name=model_name,
        options={"endpoint": "gemini-embedding-001"},
        connection_name=bq_connection,
    )


def test_generate_embedding(embedding_model):
    df = bpd.DataFrame(
        {
            "content": [
                "What is BigQuery?",
                "What is BQML?",
            ]
        }
    )

    result = ml.generate_embedding(embedding_model, df)
    assert len(result) == 2
    assert "ml_generate_embedding_result" in result.columns
    assert "ml_generate_embedding_status" in result.columns


def test_generate_embedding_with_options(embedding_model):
    df = bpd.DataFrame(
        {
            "content": [
                "What is BigQuery?",
                "What is BQML?",
            ]
        }
    )

    result = ml.generate_embedding(
        embedding_model, df, task_type="RETRIEVAL_DOCUMENT", output_dimensionality=256
    )
    assert len(result) == 2
    assert "ml_generate_embedding_result" in result.columns
    assert "ml_generate_embedding_status" in result.columns
    embedding = result["ml_generate_embedding_result"].to_pandas()
    assert len(embedding[0]) == 256


def test_create_model_linear_regression(dataset_id):
    df = bpd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    model_name = f"{dataset_id}.linear_regression_model"

    result = ml.create_model(
        model_name=model_name,
        options={"model_type": "LINEAR_REG", "input_label_cols": ["y"]},
        training_data=df,
    )

    assert result["modelType"] == "LINEAR_REGRESSION"


def test_create_model_with_transform(dataset_id):
    df = bpd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    model_name = f"{dataset_id}.transform_model"

    result = ml.create_model(
        model_name=model_name,
        options={"model_type": "LINEAR_REG", "input_label_cols": ["y"]},
        training_data=df,
        transform=["x * 2 AS x_doubled", "y"],
    )

    assert result["modelType"] == "LINEAR_REGRESSION"
