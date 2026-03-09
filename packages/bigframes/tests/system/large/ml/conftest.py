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
import hashlib
import logging

from google.cloud import bigquery
import google.cloud.exceptions
import pytest

import bigframes
from bigframes.ml import core, linear_model

PERMANENT_DATASET = "bigframes_testing"


@pytest.fixture(scope="session")
def dataset_id_permanent(bigquery_client: bigquery.Client, project_id: str) -> str:
    """Create a dataset if it doesn't exist."""
    dataset_id = f"{project_id}.{PERMANENT_DATASET}"
    dataset = bigquery.Dataset(dataset_id)
    bigquery_client.create_dataset(dataset, exists_ok=True)
    return dataset_id


@pytest.fixture(scope="session")
def penguins_bqml_linear_model(session, penguins_linear_model_name) -> core.BqmlModel:
    model = session.bqclient.get_model(penguins_linear_model_name)
    return core.BqmlModel(session, model)


@pytest.fixture(scope="function")
def penguins_linear_model_w_global_explain(
    penguins_bqml_linear_model: core.BqmlModel,
) -> linear_model.LinearRegression:
    bf_model = linear_model.LinearRegression(enable_global_explain=True)
    bf_model._bqml_model = penguins_bqml_linear_model
    return bf_model


@pytest.fixture(scope="session")
def penguins_table_id(test_data_tables) -> str:
    return test_data_tables["penguins"]


@pytest.fixture(scope="session")
def penguins_linear_model_name(
    session: bigframes.Session, dataset_id_permanent, penguins_table_id
) -> str:
    """Provides a pretrained model as a test fixture that is cached across test runs.
    This lets us run system tests without having to wait for a model.fit(...)"""
    sql = f"""
CREATE OR REPLACE MODEL `$model_name`
OPTIONS (
    model_type='linear_reg',
    input_label_cols=['body_mass_g'],
    data_split_method='NO_SPLIT'
) AS
SELECT
  *
FROM
  `{penguins_table_id}`
WHERE
  body_mass_g IS NOT NULL"""
    # We use the SQL hash as the name to ensure the model is regenerated if this fixture is edited
    model_name = f"{dataset_id_permanent}.penguins_linear_reg_{hashlib.md5(sql.encode()).hexdigest()}"
    sql = sql.replace("$model_name", model_name)

    try:
        session.bqclient.get_model(model_name)
    except google.cloud.exceptions.NotFound:
        logging.info(
            "penguins_linear_model fixture was not found in the permanent dataset, regenerating it..."
        )
        session.bqclient.query(sql).result()
    finally:
        return model_name
