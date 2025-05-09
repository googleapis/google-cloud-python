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

import bigframes_vendored.constants as constants
from google.cloud import bigquery

from bigframes.ml import (
    cluster,
    compose,
    core,
    decomposition,
    ensemble,
    forecasting,
    imported,
    impute,
    linear_model,
    llm,
    pipeline,
    preprocessing,
    utils,
)
import bigframes.session

_BQML_MODEL_TYPE_MAPPING = MappingProxyType(
    {
        "LINEAR_REGRESSION": linear_model.LinearRegression,
        "LOGISTIC_REGRESSION": linear_model.LogisticRegression,
        "KMEANS": cluster.KMeans,
        "MATRIX_FACTORIZATION": decomposition.MatrixFactorization,
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
        llm._GEMINI_1P5_PRO_PREVIEW_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_1P5_PRO_001_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_1P5_PRO_002_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_1P5_FLASH_001_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_1P5_FLASH_002_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_2_FLASH_EXP_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_2_FLASH_001_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_2_FLASH_LITE_001_ENDPOINT: llm.GeminiTextGenerator,
        llm._GEMINI_2P5_PRO_PREVIEW_ENDPOINT: llm.GeminiTextGenerator,
        llm._CLAUDE_3_HAIKU_ENDPOINT: llm.Claude3TextGenerator,
        llm._CLAUDE_3_SONNET_ENDPOINT: llm.Claude3TextGenerator,
        llm._CLAUDE_3_5_SONNET_ENDPOINT: llm.Claude3TextGenerator,
        llm._CLAUDE_3_OPUS_ENDPOINT: llm.Claude3TextGenerator,
        llm._TEXT_EMBEDDING_005_ENDPOINT: llm.TextEmbeddingGenerator,
        llm._TEXT_EMBEDDING_004_ENDPOINT: llm.TextEmbeddingGenerator,
        llm._TEXT_MULTILINGUAL_EMBEDDING_002_ENDPOINT: llm.TextEmbeddingGenerator,
        llm._MULTIMODAL_EMBEDDING_001_ENDPOINT: llm.MultimodalEmbeddingGenerator,
    }
)


def from_bq(
    session: bigframes.session.Session, bq_model: bigquery.Model
) -> Union[
    decomposition.MatrixFactorization,
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
    llm.Claude3TextGenerator,
    llm.TextEmbeddingGenerator,
    llm.MultimodalEmbeddingGenerator,
    pipeline.Pipeline,
    compose.ColumnTransformer,
    preprocessing.PreprocessingType,
    impute.SimpleImputer,
]:
    """Load a BQML model to BigQuery DataFrames ML.

    Args:
        session: a BigQuery DataFrames session.
        bq_model: a BigQuery model.

    Returns:
        A BigQuery DataFrames ML model object.
    """
    if bq_model.model_type == "TRANSFORM_ONLY":
        return _transformer_from_bq(session, bq_model)

    if _is_bq_model_pipeline(bq_model):
        return pipeline.Pipeline._from_bq(session, bq_model)

    return _model_from_bq(session, bq_model)


def _transformer_from_bq(session: bigframes.session.Session, bq_model: bigquery.Model):
    transformer = compose.ColumnTransformer._extract_from_bq_model(bq_model)._merge(
        bq_model
    )
    transformer._bqml_model = core.BqmlModel(session, bq_model)

    return transformer


def _model_from_bq(session: bigframes.session.Session, bq_model: bigquery.Model):
    if bq_model.model_type in _BQML_MODEL_TYPE_MAPPING:
        return _BQML_MODEL_TYPE_MAPPING[bq_model.model_type]._from_bq(  # type: ignore
            session=session, bq_model=bq_model
        )
    if _is_bq_model_remote(bq_model):
        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_endpoint = bqml_endpoint.split("/")[-1]
        model_name, _ = utils.parse_model_endpoint(model_endpoint)

        return _BQML_ENDPOINT_TYPE_MAPPING[model_name]._from_bq(  # type: ignore
            session=session, bq_model=bq_model
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
