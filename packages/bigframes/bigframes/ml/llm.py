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

"""LLM models."""

from __future__ import annotations

from typing import cast, Iterable, Literal, Mapping, Optional, Union
import warnings

import bigframes_vendored.constants as constants
from google.cloud import bigquery

from bigframes import dtypes, exceptions
import bigframes.bigquery as bbq
from bigframes.core import blocks, global_session, log_adapter
import bigframes.dataframe
from bigframes.ml import base, core, globals, utils
import bigframes.series

_BQML_PARAMS_MAPPING = {
    "max_iterations": "maxIterations",
}

_TEXT_EMBEDDING_005_ENDPOINT = "text-embedding-005"
_TEXT_EMBEDDING_004_ENDPOINT = "text-embedding-004"
_TEXT_MULTILINGUAL_EMBEDDING_002_ENDPOINT = "text-multilingual-embedding-002"
_TEXT_EMBEDDING_ENDPOINTS = (
    _TEXT_EMBEDDING_005_ENDPOINT,
    _TEXT_EMBEDDING_004_ENDPOINT,
    _TEXT_MULTILINGUAL_EMBEDDING_002_ENDPOINT,
)

_MULTIMODAL_EMBEDDING_001_ENDPOINT = "multimodalembedding@001"

_GEMINI_1P5_PRO_PREVIEW_ENDPOINT = "gemini-1.5-pro-preview-0514"
_GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT = "gemini-1.5-flash-preview-0514"
_GEMINI_1P5_PRO_001_ENDPOINT = "gemini-1.5-pro-001"
_GEMINI_1P5_PRO_002_ENDPOINT = "gemini-1.5-pro-002"
_GEMINI_1P5_FLASH_001_ENDPOINT = "gemini-1.5-flash-001"
_GEMINI_1P5_FLASH_002_ENDPOINT = "gemini-1.5-flash-002"
_GEMINI_2_FLASH_EXP_ENDPOINT = "gemini-2.0-flash-exp"
_GEMINI_2_FLASH_001_ENDPOINT = "gemini-2.0-flash-001"
_GEMINI_2_FLASH_LITE_001_ENDPOINT = "gemini-2.0-flash-lite-001"
_GEMINI_2P5_PRO_PREVIEW_ENDPOINT = "gemini-2.5-pro-preview-05-06"
_GEMINI_ENDPOINTS = (
    _GEMINI_1P5_PRO_PREVIEW_ENDPOINT,
    _GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT,
    _GEMINI_1P5_PRO_001_ENDPOINT,
    _GEMINI_1P5_PRO_002_ENDPOINT,
    _GEMINI_1P5_FLASH_001_ENDPOINT,
    _GEMINI_1P5_FLASH_002_ENDPOINT,
    _GEMINI_2_FLASH_EXP_ENDPOINT,
    _GEMINI_2_FLASH_001_ENDPOINT,
    _GEMINI_2_FLASH_LITE_001_ENDPOINT,
)
_GEMINI_PREVIEW_ENDPOINTS = (
    _GEMINI_1P5_PRO_PREVIEW_ENDPOINT,
    _GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT,
    _GEMINI_2_FLASH_EXP_ENDPOINT,
)
_GEMINI_FINE_TUNE_SCORE_ENDPOINTS = (
    _GEMINI_1P5_PRO_002_ENDPOINT,
    _GEMINI_1P5_FLASH_002_ENDPOINT,
    _GEMINI_2_FLASH_001_ENDPOINT,
    _GEMINI_2_FLASH_LITE_001_ENDPOINT,
)
_GEMINI_MULTIMODAL_ENDPOINTS = (
    _GEMINI_1P5_PRO_001_ENDPOINT,
    _GEMINI_1P5_PRO_002_ENDPOINT,
    _GEMINI_1P5_FLASH_001_ENDPOINT,
    _GEMINI_1P5_FLASH_002_ENDPOINT,
    _GEMINI_2_FLASH_EXP_ENDPOINT,
    _GEMINI_2_FLASH_001_ENDPOINT,
    _GEMINI_2_FLASH_LITE_001_ENDPOINT,
)

_CLAUDE_3_SONNET_ENDPOINT = "claude-3-sonnet"
_CLAUDE_3_HAIKU_ENDPOINT = "claude-3-haiku"
_CLAUDE_3_5_SONNET_ENDPOINT = "claude-3-5-sonnet"
_CLAUDE_3_OPUS_ENDPOINT = "claude-3-opus"
_CLAUDE_3_ENDPOINTS = (
    _CLAUDE_3_SONNET_ENDPOINT,
    _CLAUDE_3_HAIKU_ENDPOINT,
    _CLAUDE_3_5_SONNET_ENDPOINT,
    _CLAUDE_3_OPUS_ENDPOINT,
)

_MODEL_NOT_SUPPORTED_WARNING = (
    "Model name '{model_name}' is not supported. "
    "We are currently aware of the following models: {known_models}. "
    "However, model names can change, and the supported models may be outdated. "
    "You should use this model name only if you are sure that it is supported in BigQuery."
)

_REMOVE_DEFAULT_MODEL_WARNING = "Since upgrading the default model can cause unintended breakages, the default model will be removed in BigFrames 3.0. Please supply an explicit model to avoid this message."

_GEMINI_MULTIMODAL_MODEL_NOT_SUPPORTED_WARNING = (
    "The model '{model_name}' may not be fully supported by GeminiTextGenerator for Multimodal prompts. "
    "GeminiTextGenerator is known to support the following models for Multimodal prompts: {known_models}. "
    "If you proceed with '{model_name}', it might not work as expected or could lead to errors with multimodal inputs."
)

_MODEL_DEPRECATE_WARNING = (
    "'{model_name}' is going to be deprecated. Use '{new_model_name}' ({link}) instead."
)


@log_adapter.class_logger
class TextEmbeddingGenerator(base.RetriableRemotePredictor):
    """Text embedding generator LLM model.

    .. note::
        text-embedding-004 is going to be deprecated. Use text-embedding-005(https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.TextEmbeddingGenerator) instead.

    Args:
        model_name (str, Default to "text-embedding-004"):
            The model for text embedding. Possible values are "text-embedding-005", "text-embedding-004"
            or "text-multilingual-embedding-002". text-embedding models returns model embeddings for text inputs.
            text-multilingual-embedding models returns model embeddings for text inputs which support over 100 languages.
            If no setting is provided, "text-embedding-004" will be used by
            default and a warning will be issued.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context.
    """

    def __init__(
        self,
        *,
        model_name: Optional[
            Literal[
                "text-embedding-005",
                "text-embedding-004",
                "text-multilingual-embedding-002",
            ]
        ] = None,
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        if model_name is None:
            model_name = "text-embedding-004"
            msg = exceptions.format_message(_REMOVE_DEFAULT_MODEL_WARNING)
            warnings.warn(msg, category=FutureWarning, stacklevel=2)
        self.model_name = model_name
        self.session = session or global_session.get_global_session()
        self.connection_name = connection_name

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        self.connection_name = self.session._create_bq_connection(
            connection=self.connection_name, iam_role="aiplatform.user"
        )

        if self.model_name not in _TEXT_EMBEDDING_ENDPOINTS:
            msg = exceptions.format_message(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_TEXT_EMBEDDING_ENDPOINTS),
                )
            )
            warnings.warn(msg)
        if self.model_name == "text-embedding-004":
            msg = exceptions.format_message(
                _MODEL_DEPRECATE_WARNING.format(
                    model_name=self.model_name,
                    new_model_name="text-embedding-005",
                    link="https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.TextEmbeddingGenerator",
                )
            )
            warnings.warn(msg)

        options = {
            "endpoint": self.model_name,
        }
        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> TextEmbeddingGenerator:
        assert bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        assert "remoteModelInfo" in bq_model._properties
        assert "endpoint" in bq_model._properties["remoteModelInfo"]
        assert "connection" in bq_model._properties["remoteModelInfo"]

        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_connection = bq_model._properties["remoteModelInfo"]["connection"]
        model_endpoint = bqml_endpoint.split("/")[-1]

        model = cls(
            session=session,
            model_name=model_endpoint,  # type: ignore
            connection_name=model_connection,
        )

        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    def predict(
        self, X: utils.ArrayType, *, max_retries: int = 0
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "content" column for prediction.

            max_retries (int, default 0):
                Max number of retries if the prediction for any rows failed. Each try needs to make progress (i.e. has successfully predicted rows) to continue the retry.
                Each retry will append newly succeeded rows. When the max retries are reached, the remaining rows (the ones without successful predictions) will be appended to the end of the result.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        if max_retries < 0:
            raise ValueError(
                f"max_retries must be larger than or equal to 0, but is {max_retries}."
            )

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "content"})

        options: dict = {}

        return self._predict_and_retry(
            core.BqmlModel.generate_embedding_tvf,
            X,
            options=options,
            max_retries=max_retries,
        )

    def to_gbq(self, model_name: str, replace: bool = False) -> TextEmbeddingGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            TextEmbeddingGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class MultimodalEmbeddingGenerator(base.RetriableRemotePredictor):
    """Multimodal embedding generator LLM model.

    .. note::
        BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        model_name (str, Default to "multimodalembedding@001"):
            The model for multimodal embedding. Can set to "multimodalembedding@001". Multimodal-embedding models returns model embeddings for text, image and video inputs.
            If no setting is provided, "multimodalembedding@001" will be used by
            default and a warning will be issued.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context.
    """

    def __init__(
        self,
        *,
        model_name: Optional[Literal["multimodalembedding@001"]] = None,
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        if model_name is None:
            model_name = "multimodalembedding@001"
            msg = exceptions.format_message(_REMOVE_DEFAULT_MODEL_WARNING)
            warnings.warn(msg, category=FutureWarning, stacklevel=2)
        self.model_name = model_name
        self.session = session or global_session.get_global_session()
        self.connection_name = connection_name

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        self.connection_name = self.session._create_bq_connection(
            connection=self.connection_name, iam_role="aiplatform.user"
        )

        if self.model_name != _MULTIMODAL_EMBEDDING_001_ENDPOINT:
            msg = exceptions.format_message(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=_MULTIMODAL_EMBEDDING_001_ENDPOINT,
                )
            )
            warnings.warn(msg)

        options = {
            "endpoint": self.model_name,
        }
        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> MultimodalEmbeddingGenerator:
        assert bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        assert "remoteModelInfo" in bq_model._properties
        assert "endpoint" in bq_model._properties["remoteModelInfo"]
        assert "connection" in bq_model._properties["remoteModelInfo"]

        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_connection = bq_model._properties["remoteModelInfo"]["connection"]
        model_endpoint = bqml_endpoint.split("/")[-1]

        model = cls(
            session=session,
            model_name=model_endpoint,  # type: ignore
            connection_name=model_connection,
        )

        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    def predict(
        self, X: utils.ArrayType, *, max_retries: int = 0
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "content" column for prediction.
                The content column must be of string type or BigFrames Blob of image or video.

            max_retries (int, default 0):
                Max number of retries if the prediction for any rows failed. Each try needs to make progress (i.e. has successfully predicted rows) to continue the retry.
                Each retry will append newly succeeded rows. When the max retries are reached, the remaining rows (the ones without successful predictions) will be appended to the end of the result.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        if max_retries < 0:
            raise ValueError(
                f"max_retries must be larger than or equal to 0, but is {max_retries}."
            )

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "content"})

        # TODO(garrettwu): remove transform to ObjRefRuntime when BQML supports ObjRef as input
        if X["content"].dtype == dtypes.OBJ_REF_DTYPE:
            X["content"] = X["content"].blob._get_runtime("R", with_metadata=True)

        options: dict = {}

        return self._predict_and_retry(
            core.BqmlModel.generate_embedding_tvf,
            X,
            options=options,
            max_retries=max_retries,
        )

    def to_gbq(
        self, model_name: str, replace: bool = False
    ) -> MultimodalEmbeddingGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            MultimodalEmbeddingGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class GeminiTextGenerator(base.RetriableRemotePredictor):
    """Gemini text generator LLM model.

    .. note::
        gemini-1.5-X are going to be deprecated. Use gemini-2.0-X (https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator) instead.

    Args:
        model_name (str, Default to "gemini-2.0-flash-001"):
            The model for natural language tasks. Accepted values are
            "gemini-1.5-pro-preview-0514", "gemini-1.5-flash-preview-0514",
            "gemini-1.5-pro-001", "gemini-1.5-pro-002", "gemini-1.5-flash-001",
            "gemini-1.5-flash-002", "gemini-2.0-flash-exp",
            "gemini-2.0-flash-lite-001", and "gemini-2.0-flash-001".
            If no setting is provided, "gemini-2.0-flash-001" will be used by
            default and a warning will be issued.

        .. note::
            "gemini-1.5-X" is going to be deprecated. Please use gemini-2.0-X instead. For example, "gemini-2.0-flash-001".
            "gemini-2.0-flash-exp", "gemini-1.5-pro-preview-0514" and "gemini-1.5-flash-preview-0514" is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
            permission if the connection isn't fully set up.
        max_iterations (Optional[int], Default to 300):
            The number of steps to run when performing supervised tuning.
    """

    def __init__(
        self,
        *,
        model_name: Optional[
            Literal[
                "gemini-1.5-pro-preview-0514",
                "gemini-1.5-flash-preview-0514",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-flash-001",
                "gemini-1.5-flash-002",
                "gemini-2.0-flash-exp",
                "gemini-2.0-flash-001",
                "gemini-2.0-flash-lite-001",
            ]
        ] = None,
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
        max_iterations: int = 300,
    ):
        if model_name in _GEMINI_PREVIEW_ENDPOINTS:
            msg = exceptions.format_message(
                f'Model {model_name} is subject to the "Pre-GA Offerings Terms" in '
                "the General Service Terms section of the Service Specific Terms"
                "(https://cloud.google.com/terms/service-terms#1). Pre-GA products and "
                'features are available "as is" and might have limited support. For '
                "more information, see the launch stage descriptions "
                "(https://cloud.google.com/products#product-launch-stages)."
            )
            warnings.warn(msg, category=exceptions.PreviewWarning)

        if model_name is None:
            model_name = "gemini-2.0-flash-001"
            msg = exceptions.format_message(_REMOVE_DEFAULT_MODEL_WARNING)
            warnings.warn(msg, category=FutureWarning, stacklevel=2)

        self.model_name = model_name
        self.session = session or global_session.get_global_session()
        self.max_iterations = max_iterations
        self.connection_name = connection_name

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        self.connection_name = self.session._create_bq_connection(
            connection=self.connection_name, iam_role="aiplatform.user"
        )

        if self.model_name not in _GEMINI_ENDPOINTS:
            msg = exceptions.format_message(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_GEMINI_ENDPOINTS),
                )
            )
            warnings.warn(msg)
        if self.model_name.startswith("gemini-1.5"):
            msg = exceptions.format_message(
                _MODEL_DEPRECATE_WARNING.format(
                    model_name=self.model_name,
                    new_model_name="gemini-2.0-X",
                    link="https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator",
                )
            )
            warnings.warn(msg)

        options = {"endpoint": self.model_name}

        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> GeminiTextGenerator:
        assert bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        assert "remoteModelInfo" in bq_model._properties
        assert "endpoint" in bq_model._properties["remoteModelInfo"]
        assert "connection" in bq_model._properties["remoteModelInfo"]

        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_connection = bq_model._properties["remoteModelInfo"]["connection"]
        model_endpoint = bqml_endpoint.split("/")[-1]

        model = cls(
            model_name=model_endpoint, session=session, connection_name=model_connection
        )
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options = {
            "max_iterations": self.max_iterations,
            "data_split_method": "NO_SPLIT",
        }
        return options

    def fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ) -> GeminiTextGenerator:
        """Fine tune GeminiTextGenerator model. Only support "gemini-1.5-pro-002",
           "gemini-1.5-flash-002", "gemini-2.0-flash-001",
           and "gemini-2.0-flash-lite-001"models for now.

        .. note::

            This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples, n_features). Training data.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series:
                Training labels.

        Returns:
            GeminiTextGenerator: Fitted estimator.
        """
        if self.model_name not in _GEMINI_FINE_TUNE_SCORE_ENDPOINTS:
            msg = exceptions.format_message(
                "fit() only supports gemini-1.5-pro-002, gemini-1.5-flash-002, gemini-2.0-flash-001, or gemini-2.0-flash-lite-001 model."
            )
            warnings.warn(msg)

        X, y = utils.batch_convert_to_dataframe(X, y)

        options = self._bqml_options
        options["endpoint"] = self.model_name
        options["prompt_col"] = X.columns.tolist()[0]

        self._bqml_model = self._bqml_model_factory.create_llm_remote_model(
            X, y, options=options, connection_name=cast(str, self.connection_name)
        )
        return self

    def predict(
        self,
        X: utils.ArrayType,
        *,
        temperature: float = 0.9,
        max_output_tokens: int = 8192,
        top_k: int = 40,
        top_p: float = 1.0,
        ground_with_google_search: bool = False,
        max_retries: int = 0,
        prompt: Optional[Iterable[Union[str, bigframes.series.Series]]] = None,
        output_schema: Optional[Mapping[str, str]] = None,
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, the "prompt" column, or created by "prompt" parameter, is used for prediction.
                Prompts can include preamble, questions, suggestions, instructions, or examples.

            temperature (float, default 0.9):
                The temperature is used for sampling during the response generation, which occurs when topP and topK are applied. Temperature controls the degree of randomness in token selection. Lower temperatures are good for prompts that require a more deterministic and less open-ended or creative response, while higher temperatures can lead to more diverse or creative results. A temperature of 0 is deterministic: the highest probability response is always selected.
                Default 0.9. Possible values [0.0, 1.0].

            max_output_tokens (int, default 8192):
                Maximum number of tokens that can be generated in the response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.
                Specify a lower value for shorter responses and a higher value for potentially longer responses.
                Default 8192. Possible values are in the range [1, 8192].

            top_k (int, default 40):
                Top-K changes how the model selects tokens for output. A top-K of 1 means the next selected token is the most probable among all tokens in the model's vocabulary (also called greedy decoding), while a top-K of 3 means that the next token is selected from among the three most probable tokens by using temperature.
                For each token selection step, the top-K tokens with the highest probabilities are sampled. Then tokens are further filtered based on top-P with the final token selected using temperature sampling.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 40. Possible values [1, 40].

            top_p (float, default 0.95):
                Top-P changes how the model selects tokens for output. Tokens are selected from the most (see top-K) to least probable until the sum of their probabilities equals the top-P value. For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the top-P value is 0.5, then the model will select either A or B as the next token by using temperature and excludes C as a candidate.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 1.0. Possible values [0.0, 1.0].

            ground_with_google_search (bool, default False):
                Enables Grounding with Google Search for the Vertex AI model. When set
                to True, the model incorporates relevant information from Google Search
                results into its responses, enhancing their accuracy and factualness.
                This feature provides an additional column, `ml_generate_text_grounding_result`,
                in the response output, detailing the sources used for grounding.
                Note: Using this feature may impact billing costs. Refer to the pricing
                page for details: https://cloud.google.com/vertex-ai/generative-ai/pricing#google_models
                The default is `False`.

            max_retries (int, default 0):
                Max number of retries if the prediction for any rows failed. Each try needs to make progress (i.e. has successfully predicted rows) to continue the retry.
                Each retry will append newly succeeded rows. When the max retries are reached, the remaining rows (the ones without successful predictions) will be appended to the end of the result.

            prompt (Iterable of str or bigframes.series.Series, or None, default None):
                .. note::
                    BigFrames Blob is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
                    Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
                    and might have limited support. For more information, see the launch stage descriptions
                    (https://cloud.google.com/products#product-launch-stages).

                Construct a prompt struct column for prediction based on the input. The input must be an Iterable that can take string literals,
                such as "summarize", string column(s) of X, such as X["str_col"], or blob column(s) of X, such as X["blob_col"].
                It creates a struct column of the items of the iterable, and use the concatenated result as the input prompt. No-op if set to None.
            output_schema (Mapping[str, str] or None, default None):
                The schema used to generate structured output as a bigframes DataFrame. The schema is a string key-value pair of <column_name>:<type>.
                Supported types are int64, float64, bool, string, array<type> and struct<column type>. If None, output text result.
        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        if temperature < 0.0 or temperature > 1.0:
            raise ValueError(f"temperature must be [0.0, 1.0], but is {temperature}.")

        if max_output_tokens not in range(1, 8193):
            raise ValueError(
                f"max_output_token must be [1, 8192] for Gemini model, but is {max_output_tokens}."
            )

        if top_k not in range(1, 41):
            raise ValueError(f"top_k must be [1, 40], but is {top_k}.")

        if top_p < 0.0 or top_p > 1.0:
            raise ValueError(f"top_p must be [0.0, 1.0], but is {top_p}.")

        if max_retries < 0:
            raise ValueError(
                f"max_retries must be larger than or equal to 0, but is {max_retries}."
            )

        session = self._bqml_model.session
        (X,) = utils.batch_convert_to_dataframe(X, session=session)

        if prompt:
            if self.model_name not in _GEMINI_MULTIMODAL_ENDPOINTS:
                msg = exceptions.format_message(
                    _GEMINI_MULTIMODAL_MODEL_NOT_SUPPORTED_WARNING.format(
                        model_name=self.model_name,
                        known_models=", ".join(_GEMINI_MULTIMODAL_ENDPOINTS),
                    )
                )
                warnings.warn(msg)

            df_prompt = X[[X.columns[0]]].rename(
                columns={X.columns[0]: "bigframes_placeholder_col"}
            )
            for i, item in enumerate(prompt):
                # must be distinct str column labels to construct a struct
                if isinstance(item, str):
                    label = f"input_{i}"
                else:  # Series
                    label = f"input_{i}_{item.name}"

                # TODO(garrettwu): remove transform to ObjRefRuntime when BQML supports ObjRef as input
                if (
                    isinstance(item, bigframes.series.Series)
                    and item.dtype == dtypes.OBJ_REF_DTYPE
                ):
                    item = item.blob._get_runtime("R", with_metadata=True)

                df_prompt[label] = item
            df_prompt = df_prompt.drop(columns="bigframes_placeholder_col")
            X["prompt"] = bbq.struct(df_prompt)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "prompt"})

        options: dict = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            # "top_k": top_k, # TODO(garrettwu): the option is deprecated in Gemini 1.5 forward.
            "top_p": top_p,
            "ground_with_google_search": ground_with_google_search,
        }
        if output_schema:
            output_schema = {
                k: utils.standardize_type(v) for k, v in output_schema.items()
            }
            options["output_schema"] = output_schema
            return self._predict_and_retry(
                core.BqmlModel.generate_table_tvf,
                X,
                options=options,
                max_retries=max_retries,
            )

        return self._predict_and_retry(
            core.BqmlModel.generate_text_tvf,
            X,
            options=options,
            max_retries=max_retries,
        )

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        task_type: Literal[
            "text_generation", "classification", "summarization", "question_answering"
        ] = "text_generation",
    ) -> bigframes.dataframe.DataFrame:
        """Calculate evaluation metrics of the model. Only support
            "gemini-1.5-pro-002", "gemini-1.5-flash-002",
            "gemini-2.0-flash-lite-001", and "gemini-2.0-flash-001".

        .. note::

            This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#remote-model-llm
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                A BigQuery DataFrame as evaluation data, which contains only one column of input_text
                that contains the prompt text to use when evaluating the model.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                A BigQuery DataFrame as evaluation labels, which contains only one column of output_text
                that you would expect to be returned by the model.
            task_type (str):
                The type of the task for LLM model. Default to "text_generation".
                Possible values: "text_generation", "classification", "summarization", and "question_answering".

        Returns:
            bigframes.dataframe.DataFrame: The DataFrame as evaluation result.
        """
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        if self.model_name not in _GEMINI_FINE_TUNE_SCORE_ENDPOINTS:
            msg = exceptions.format_message(
                "score() only supports gemini-1.5-pro-002, gemini-1.5-flash-2, gemini-2.0-flash-001, and gemini-2.0-flash-lite-001 model."
            )
            warnings.warn(msg)

        X, y = utils.batch_convert_to_dataframe(X, y, session=self._bqml_model.session)

        if len(X.columns) != 1 or len(y.columns) != 1:
            raise ValueError(
                f"Only support one column as input for X and y. {constants.FEEDBACK_LINK}"
            )

        # BQML identified the column by name
        X_col_label = cast(blocks.Label, X.columns[0])
        y_col_label = cast(blocks.Label, y.columns[0])
        X = X.rename(columns={X_col_label: "input_text"})
        y = y.rename(columns={y_col_label: "output_text"})

        input_data = X.join(y, how="outer")

        return self._bqml_model.llm_evaluate(input_data, task_type)

    def to_gbq(self, model_name: str, replace: bool = False) -> GeminiTextGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            GeminiTextGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class Claude3TextGenerator(base.RetriableRemotePredictor):
    """Claude3 text generator LLM model.

    Go to Google Cloud Console -> Vertex AI -> Model Garden page to enabe the models before use. Must have the Consumer Procurement Entitlement Manager Identity and Access Management (IAM) role to enable the models.
    https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#grant-permissions

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).


    .. note::

        The models only available in specific regions. Check https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude#regions for details.

    Args:
        model_name (str, Default to "claude-3-sonnet"):
            The model for natural language tasks. Possible values are "claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet" and "claude-3-opus".
            "claude-3-sonnet" is Anthropic's dependable combination of skills and speed. It is engineered to be dependable for scaled AI deployments across a variety of use cases.
            "claude-3-haiku" is Anthropic's fastest, most compact vision and text model for near-instant responses to simple queries, meant for seamless AI experiences mimicking human interactions.
            "claude-3-5-sonnet" is Anthropic's most powerful AI model and maintains the speed and cost of Claude 3 Sonnet, which is a mid-tier model.
            "claude-3-opus" is Anthropic's second-most powerful AI model, with strong performance on highly complex tasks.
            https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude#available-claude-models
            If no setting is provided, "claude-3-sonnet" will be used by default
            and a warning will be issued.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
            permission if the connection isn't fully set up.
    """

    def __init__(
        self,
        *,
        model_name: Optional[
            Literal[
                "claude-3-sonnet",
                "claude-3-haiku",
                "claude-3-5-sonnet",
                "claude-3-opus",
            ]
        ] = None,
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        if model_name is None:
            model_name = "claude-3-sonnet"
            msg = exceptions.format_message(_REMOVE_DEFAULT_MODEL_WARNING)
            warnings.warn(msg, category=FutureWarning, stacklevel=2)
        self.model_name = model_name
        self.session = session or global_session.get_global_session()
        self.connection_name = connection_name

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        self.connection_name = self.session._create_bq_connection(
            connection=self.connection_name, iam_role="aiplatform.user"
        )

        if self.model_name not in _CLAUDE_3_ENDPOINTS:
            msg = exceptions.format_message(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_CLAUDE_3_ENDPOINTS),
                )
            )
            warnings.warn(msg)
        options = {
            "endpoint": self.model_name,
        }

        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> Claude3TextGenerator:
        assert bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        assert "remoteModelInfo" in bq_model._properties
        assert "endpoint" in bq_model._properties["remoteModelInfo"]
        assert "connection" in bq_model._properties["remoteModelInfo"]

        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_connection = bq_model._properties["remoteModelInfo"]["connection"]
        model_endpoint = bqml_endpoint.split("/")[-1]

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(
            **kwargs,
            session=session,
            model_name=model_endpoint,
            connection_name=model_connection,
        )
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options = {
            "data_split_method": "NO_SPLIT",
        }
        return options

    def predict(
        self,
        X: utils.ArrayType,
        *,
        max_output_tokens: int = 128,
        top_k: int = 40,
        top_p: float = 0.95,
        max_retries: int = 0,
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "prompt" column for prediction.
                Prompts can include preamble, questions, suggestions, instructions, or examples.

            max_output_tokens (int, default 128):
                Maximum number of tokens that can be generated in the response. Specify a lower value for shorter responses and a higher value for longer responses.
                A token may be smaller than a word. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.
                Default 128. Possible values are in the range [1, 4096].

            top_k (int, default 40):
                Top-k changes how the model selects tokens for output. A top-k of 1 means the selected token is the most probable among all tokens
                in the model's vocabulary (also called greedy decoding), while a top-k of 3 means that the next token is selected from among the 3 most probable tokens (using temperature).
                For each token selection step, the top K tokens with the highest probabilities are sampled. Then tokens are further filtered based on topP with the final token selected using temperature sampling.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 40. Possible values [1, 40].

            top_p (float, default 0.95)::
                Top-p changes how the model selects tokens for output. Tokens are selected from most K (see topK parameter) probable to least until the sum of their probabilities equals the top-p value.
                For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the top-p value is 0.5, then the model will select either A or B as the next token (using temperature)
                and not consider C at all.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 0.95. Possible values [0.0, 1.0].

            max_retries (int, default 0):
                Max number of retries if the prediction for any rows failed. Each try needs to make progress (i.e. has successfully predicted rows) to continue the retry.
                Each retry will append newly succeeded rows. When the max retries are reached, the remaining rows (the ones without successful predictions) will be appended to the end of the result.


        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        if max_output_tokens not in range(1, 4097):
            raise ValueError(
                f"max_output_token must be [1, 4096], but is {max_output_tokens}."
            )

        if top_k not in range(1, 41):
            raise ValueError(f"top_k must be [1, 40], but is {top_k}.")

        if top_p < 0.0 or top_p > 1.0:
            raise ValueError(f"top_p must be [0.0, 1.0], but is {top_p}.")

        if max_retries < 0:
            raise ValueError(
                f"max_retries must be larger than or equal to 0, but is {max_retries}."
            )

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "prompt"})

        options = {
            "max_output_tokens": max_output_tokens,
            "top_k": top_k,
            "top_p": top_p,
        }

        return self._predict_and_retry(
            core.BqmlModel.generate_text_tvf,
            X,
            options=options,
            max_retries=max_retries,
        )

    def to_gbq(self, model_name: str, replace: bool = False) -> Claude3TextGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            Claude3TextGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
