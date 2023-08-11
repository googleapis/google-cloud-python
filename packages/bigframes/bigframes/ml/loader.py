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

from __future__ import annotations

from types import MappingProxyType
from typing import Union

from google.cloud import bigquery

import bigframes
import bigframes.constants as constants
from bigframes.ml import (
    cluster,
    decomposition,
    ensemble,
    forecasting,
    imported,
    linear_model,
    pipeline,
)

_BQML_MODEL_TYPE_MAPPING = MappingProxyType(
    {
        "LINEAR_REGRESSION": linear_model.LinearRegression,
        "LOGISTIC_REGRESSION": linear_model.LogisticRegression,
        "KMEANS": cluster.KMeans,
        "PCA": decomposition.PCA,
        "BOOSTED_TREE_REGRESSOR": ensemble.XGBRegressor,
        "BOOSTED_TREE_CLASSIFIER": ensemble.XGBClassifier,
        "ARIMA_PLUS": forecasting.ARIMAPlus,
        "RANDOM_FOREST_REGRESSOR": ensemble.RandomForestRegressor,
        "RANDOM_FOREST_CLASSIFIER": ensemble.RandomForestClassifier,
        "TENSORFLOW": imported.TensorFlowModel,
        "ONNX": imported.ONNXModel,
    }
)


def from_bq(
    session: bigframes.Session, bq_model: bigquery.Model
) -> Union[
    decomposition.PCA,
    cluster.KMeans,
    linear_model.LinearRegression,
    linear_model.LogisticRegression,
    ensemble.XGBRegressor,
    ensemble.XGBClassifier,
    forecasting.ARIMAPlus,
    ensemble.RandomForestRegressor,
    ensemble.RandomForestClassifier,
    imported.TensorFlowModel,
    imported.ONNXModel,
    pipeline.Pipeline,
]:
    """Load a BQML model to BigQuery DataFrames ML.

    Args:
        session: a BigQuery DataFrames session.
        bq_model: a BigQuery model.

    Returns:
        A BigQuery DataFrames ML model object.
    """
    if _is_bq_model_pipeline(bq_model):
        return pipeline.Pipeline._from_bq(session, bq_model)

    return _model_from_bq(session, bq_model)


def _model_from_bq(session: bigframes.Session, bq_model: bigquery.Model):
    if bq_model.model_type in _BQML_MODEL_TYPE_MAPPING:
        return _BQML_MODEL_TYPE_MAPPING[bq_model.model_type]._from_bq(  # type: ignore
            session=session, model=bq_model
        )

    raise NotImplementedError(
        f"Model type {bq_model.model_type} is not yet supported by BigQuery DataFrames. {constants.FEEDBACK_LINK}"
    )


def _is_bq_model_pipeline(bq_model: bigquery.Model) -> bool:
    return "transformColumns" in bq_model._properties
