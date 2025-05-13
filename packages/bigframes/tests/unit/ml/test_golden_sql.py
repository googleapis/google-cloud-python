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

from unittest import mock

from google.cloud import bigquery
import pandas as pd
import pytest

import bigframes
from bigframes.ml import core, decomposition, linear_model
import bigframes.ml.core
import bigframes.pandas as bpd

TEMP_MODEL_ID = bigquery.ModelReference.from_string(
    "test-project._anon123.temp_model_id"
)


@pytest.fixture
def mock_session():
    mock_session = mock.create_autospec(spec=bigframes.Session)

    mock_session._anonymous_dataset = bigquery.DatasetReference(
        TEMP_MODEL_ID.project, TEMP_MODEL_ID.dataset_id
    )
    mock_session._bq_kms_key_name = None
    mock_session._metrics = None

    query_job = mock.create_autospec(bigquery.QueryJob)
    type(query_job).destination = mock.PropertyMock(
        return_value=bigquery.TableReference(
            mock_session._anonymous_dataset, TEMP_MODEL_ID.model_id
        )
    )
    mock_session._start_query_ml_ddl.return_value = (None, query_job)

    return mock_session


@pytest.fixture
def bqml_model_factory(monkeypatch):
    monkeypatch.setattr(
        bigframes.ml.core.BqmlModelFactory,
        "_create_model_ref",
        mock.Mock(return_value=TEMP_MODEL_ID),
    )
    bqml_model_factory = core.BqmlModelFactory()

    return bqml_model_factory


@pytest.fixture
def mock_y(mock_session):
    mock_y = mock.create_autospec(spec=bpd.DataFrame)
    mock_y._session = mock_session
    mock_y.columns = pd.Index(["input_column_label"])
    mock_y.cache.return_value = mock_y
    mock_y.copy.return_value = mock_y

    return mock_y


@pytest.fixture
def mock_X(mock_y, mock_session):
    mock_X = mock.create_autospec(spec=bpd.DataFrame)
    mock_X._session = mock_session
    mock_X._to_sql_query.return_value = (
        "input_X_sql",
        ["index_column_id"],
        ["index_column_label"],
    )
    type(mock_X).sql = mock.PropertyMock(return_value="input_X_sql_property")
    mock_X.reset_index(drop=True).cache().sql = "input_X_no_index_sql"
    mock_X.join(mock_y).sql = "input_X_y_sql"
    mock_X.join(mock_y).cache.return_value = mock_X.join(mock_y)
    mock_X.join(mock_y)._to_sql_query.return_value = (
        "input_X_y_sql",
        ["index_column_id"],
        ["index_column_label"],
    )

    mock_X.join(mock_y).reset_index(drop=True).sql = "input_X_y_no_index_sql"
    mock_X.join(mock_y).reset_index(drop=True).cache.return_value = mock_X.join(
        mock_y
    ).reset_index(drop=True)
    mock_X.join(mock_y).reset_index(drop=True)._to_sql_query.return_value = (
        "input_X_y_no_index_sql",
        ["index_column_id"],
        ["index_column_label"],
    )

    mock_X.cache.return_value = mock_X
    mock_X.copy.return_value = mock_X

    return mock_X


@pytest.fixture
def bqml_model(mock_session):
    bqml_model = core.BqmlModel(
        mock_session, bigquery.Model("model_project.model_dataset.model_id")
    )

    return bqml_model


def test_linear_regression_default_fit(
    bqml_model_factory, mock_session, mock_X, mock_y
):
    model = linear_model.LinearRegression()
    model._bqml_model_factory = bqml_model_factory
    model.fit(mock_X, mock_y)

    mock_session._start_query_ml_ddl.assert_called_once_with(
        "CREATE OR REPLACE MODEL `test-project`.`_anon123`.`temp_model_id`\nOPTIONS(\n  model_type='LINEAR_REG',\n  data_split_method='NO_SPLIT',\n  optimize_strategy='auto_strategy',\n  fit_intercept=True,\n  l2_reg=0.0,\n  max_iterations=20,\n  learn_rate_strategy='line_search',\n  min_rel_progress=0.01,\n  calculate_p_values=False,\n  enable_global_explain=False,\n  INPUT_LABEL_COLS=['input_column_label'])\nAS input_X_y_no_index_sql"
    )


def test_linear_regression_params_fit(bqml_model_factory, mock_session, mock_X, mock_y):
    model = linear_model.LinearRegression(fit_intercept=False)
    model._bqml_model_factory = bqml_model_factory
    model.fit(mock_X, mock_y)

    mock_session._start_query_ml_ddl.assert_called_once_with(
        "CREATE OR REPLACE MODEL `test-project`.`_anon123`.`temp_model_id`\nOPTIONS(\n  model_type='LINEAR_REG',\n  data_split_method='NO_SPLIT',\n  optimize_strategy='auto_strategy',\n  fit_intercept=False,\n  l2_reg=0.0,\n  max_iterations=20,\n  learn_rate_strategy='line_search',\n  min_rel_progress=0.01,\n  calculate_p_values=False,\n  enable_global_explain=False,\n  INPUT_LABEL_COLS=['input_column_label'])\nAS input_X_y_no_index_sql"
    )


def test_linear_regression_predict(mock_session, bqml_model, mock_X):
    model = linear_model.LinearRegression()
    model._bqml_model = bqml_model
    model.predict(mock_X)

    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.PREDICT(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_sql))",
        index_col=["index_column_id"],
    )


def test_linear_regression_score(mock_session, bqml_model, mock_X, mock_y):
    model = linear_model.LinearRegression()
    model._bqml_model = bqml_model
    model.score(mock_X, mock_y)

    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.EVALUATE(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_y_sql))"
    )


def test_logistic_regression_default_fit(
    bqml_model_factory, mock_session, mock_X, mock_y
):
    model = linear_model.LogisticRegression()
    model._bqml_model_factory = bqml_model_factory
    model.fit(mock_X, mock_y)

    mock_session._start_query_ml_ddl.assert_called_once_with(
        "CREATE OR REPLACE MODEL `test-project`.`_anon123`.`temp_model_id`\nOPTIONS(\n  model_type='LOGISTIC_REG',\n  data_split_method='NO_SPLIT',\n  fit_intercept=True,\n  auto_class_weights=False,\n  optimize_strategy='auto_strategy',\n  l2_reg=0.0,\n  max_iterations=20,\n  learn_rate_strategy='line_search',\n  min_rel_progress=0.01,\n  calculate_p_values=False,\n  enable_global_explain=False,\n  INPUT_LABEL_COLS=['input_column_label'])\nAS input_X_y_no_index_sql"
    )


def test_logistic_regression_params_fit(
    bqml_model_factory, mock_session, mock_X, mock_y
):
    model = linear_model.LogisticRegression(
        fit_intercept=False,
        class_weight="balanced",
        l2_reg=0.2,
        tol=0.02,
        l1_reg=0.2,
        max_iterations=30,
        optimize_strategy="batch_gradient_descent",
        learning_rate_strategy="constant",
        learning_rate=0.2,
    )
    model._bqml_model_factory = bqml_model_factory
    model.fit(mock_X, mock_y)

    mock_session._start_query_ml_ddl.assert_called_once_with(
        "CREATE OR REPLACE MODEL `test-project`.`_anon123`.`temp_model_id`\nOPTIONS(\n  model_type='LOGISTIC_REG',\n  data_split_method='NO_SPLIT',\n  fit_intercept=False,\n  auto_class_weights=True,\n  optimize_strategy='batch_gradient_descent',\n  l2_reg=0.2,\n  max_iterations=30,\n  learn_rate_strategy='constant',\n  min_rel_progress=0.02,\n  calculate_p_values=False,\n  enable_global_explain=False,\n  l1_reg=0.2,\n  learn_rate=0.2,\n  INPUT_LABEL_COLS=['input_column_label'])\nAS input_X_y_no_index_sql"
    )


def test_logistic_regression_predict(mock_session, bqml_model, mock_X):
    model = linear_model.LogisticRegression()
    model._bqml_model = bqml_model
    model.predict(mock_X)

    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.PREDICT(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_sql))",
        index_col=["index_column_id"],
    )


def test_logistic_regression_score(mock_session, bqml_model, mock_X, mock_y):
    model = linear_model.LogisticRegression()
    model._bqml_model = bqml_model
    model.score(mock_X, mock_y)

    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.EVALUATE(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_y_sql))"
    )


def test_decomposition_mf_default_fit(bqml_model_factory, mock_session, mock_X):
    model = decomposition.MatrixFactorization(
        num_factors=34,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    model._bqml_model_factory = bqml_model_factory
    model.fit(mock_X)

    mock_session._start_query_ml_ddl.assert_called_once_with(
        "CREATE OR REPLACE MODEL `test-project`.`_anon123`.`temp_model_id`\nOPTIONS(\n  model_type='matrix_factorization',\n  feedback_type='explicit',\n  user_col='user_id',\n  item_col='item_col',\n  rating_col='rating_col',\n  l2_reg=9.83,\n  num_factors=34)\nAS input_X_no_index_sql"
    )


def test_decomposition_mf_predict(mock_session, bqml_model, mock_X):
    model = decomposition.MatrixFactorization(
        num_factors=34,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    model._bqml_model = bqml_model
    model.predict(mock_X)

    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.RECOMMEND(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_sql))",
        index_col=["index_column_id"],
    )


def test_decomposition_mf_score(mock_session, bqml_model):
    model = decomposition.MatrixFactorization(
        num_factors=34,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    model._bqml_model = bqml_model
    model.score()
    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.EVALUATE(MODEL `model_project`.`model_dataset`.`model_id`)"
    )


def test_decomposition_mf_score_with_x(mock_session, bqml_model, mock_X):
    model = decomposition.MatrixFactorization(
        num_factors=34,
        feedback_type="explicit",
        user_col="user_id",
        item_col="item_col",
        rating_col="rating_col",
        l2_reg=9.83,
    )
    model._bqml_model = bqml_model
    model.score(mock_X)
    mock_session.read_gbq.assert_called_once_with(
        "SELECT * FROM ML.EVALUATE(MODEL `model_project`.`model_dataset`.`model_id`,\n  (input_X_sql_property))"
    )
