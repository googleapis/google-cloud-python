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
    compose,
    core,
    decomposition,
    ensemble,
    forecasting,
    imported,
    linear_model,
    llm,
    pipeline,
    preprocessing,
    utils,
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
        "XGBOOST": imported.XGBoostModel,
    }
)

_BQML_ENDPOINT_TYPE_MAPPING = MappingProxyType(
    {
        llm._TEXT_GENERATOR_BISON_ENDPOINT: llm.PaLM2TextGenerator,
        llm._TEXT_GENERATOR_BISON_32K_ENDPOINT: llm.PaLM2TextGenerator,
        llm._EMBEDDING_GENERATOR_GECKO_ENDPOINT: llm.PaLM2TextEmbeddingGenerator,
        llm._EMBEDDING_GENERATOR_GECKO_MULTILINGUAL_ENDPOINT: llm.PaLM2TextEmbeddingGenerator,
        llm._GEMINI_PRO_ENDPOINT: llm.GeminiTextGenerator,
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
    imported.XGBoostModel,
    llm.PaLM2TextGenerator,
    llm.PaLM2TextEmbeddingGenerator,
    pipeline.Pipeline,
    compose.ColumnTransformer,
    preprocessing.PreprocessingType,
]:
    """Load a BQML model to BigQuery DataFrames ML.

    Args:
        session: a BigQuery DataFrames session.
        bq_model: a BigQuery model.

    Returns:
        A BigQuery DataFrames ML model object.
    """
    # TODO(garrettwu): the entire condition only to TRANSFORM_ONLY when b/331679273 is fixed.
    if (
        bq_model.model_type == "TRANSFORM_ONLY"
        or bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        and "transformColumns" in bq_model._properties
        and not _is_bq_model_remote(bq_model)
    ):
        return _transformer_from_bq(session, bq_model)

    if _is_bq_model_pipeline(bq_model):
        return pipeline.Pipeline._from_bq(session, bq_model)

    return _model_from_bq(session, bq_model)


def _transformer_from_bq(session: bigframes.Session, bq_model: bigquery.Model):
    transformer = compose.ColumnTransformer._extract_from_bq_model(bq_model)._merge(
        bq_model
    )
    transformer._bqml_model = core.BqmlModel(session, bq_model)

    return transformer


def _model_from_bq(session: bigframes.Session, bq_model: bigquery.Model):
    if bq_model.model_type in _BQML_MODEL_TYPE_MAPPING:
        return _BQML_MODEL_TYPE_MAPPING[bq_model.model_type]._from_bq(  # type: ignore
            session=session, model=bq_model
        )
    if _is_bq_model_remote(bq_model):
        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_endpoint = bqml_endpoint.split("/")[-1]
        model_name, _ = utils.parse_model_endpoint(model_endpoint)

        return _BQML_ENDPOINT_TYPE_MAPPING[model_name]._from_bq(  # type: ignore
            session=session, model=bq_model
        )

    raise NotImplementedError(
        f"Model type {bq_model.model_type} is not yet supported by BigQuery DataFrames. {constants.FEEDBACK_LINK}"
    )


def _is_bq_model_pipeline(bq_model: bigquery.Model) -> bool:
    return "transformColumns" in bq_model._properties


def _is_bq_model_remote(bq_model: bigquery.Model) -> bool:
    return (
        bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        and "remoteModelInfo" in bq_model._properties
        and "endpoint" in bq_model._properties["remoteModelInfo"]
    )
