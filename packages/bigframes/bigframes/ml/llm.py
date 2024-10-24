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

from typing import cast, Literal, Optional
import warnings

import bigframes_vendored.constants as constants
from google.cloud import bigquery
import typing_extensions

import bigframes
from bigframes import clients, exceptions
from bigframes.core import blocks, log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd

_BQML_PARAMS_MAPPING = {
    "max_iterations": "maxIterations",
}

_TEXT_GENERATOR_BISON_ENDPOINT = "text-bison"
_TEXT_GENERATOR_BISON_32K_ENDPOINT = "text-bison-32k"
_TEXT_GENERATOR_ENDPOINTS = (
    _TEXT_GENERATOR_BISON_ENDPOINT,
    _TEXT_GENERATOR_BISON_32K_ENDPOINT,
)

_EMBEDDING_GENERATOR_GECKO_ENDPOINT = "textembedding-gecko"
_EMBEDDING_GENERATOR_GECKO_MULTILINGUAL_ENDPOINT = "textembedding-gecko-multilingual"
_PALM2_EMBEDDING_GENERATOR_ENDPOINTS = (
    _EMBEDDING_GENERATOR_GECKO_ENDPOINT,
    _EMBEDDING_GENERATOR_GECKO_MULTILINGUAL_ENDPOINT,
)

_TEXT_EMBEDDING_004_ENDPOINT = "text-embedding-004"
_TEXT_MULTILINGUAL_EMBEDDING_002_ENDPOINT = "text-multilingual-embedding-002"
_TEXT_EMBEDDING_ENDPOINTS = (
    _TEXT_EMBEDDING_004_ENDPOINT,
    _TEXT_MULTILINGUAL_EMBEDDING_002_ENDPOINT,
)

_GEMINI_PRO_ENDPOINT = "gemini-pro"
_GEMINI_1P5_PRO_PREVIEW_ENDPOINT = "gemini-1.5-pro-preview-0514"
_GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT = "gemini-1.5-flash-preview-0514"
_GEMINI_1P5_PRO_001_ENDPOINT = "gemini-1.5-pro-001"
_GEMINI_1P5_PRO_002_ENDPOINT = "gemini-1.5-pro-002"
_GEMINI_1P5_FLASH_001_ENDPOINT = "gemini-1.5-flash-001"
_GEMINI_1P5_FLASH_002_ENDPOINT = "gemini-1.5-flash-002"
_GEMINI_ENDPOINTS = (
    _GEMINI_PRO_ENDPOINT,
    _GEMINI_1P5_PRO_PREVIEW_ENDPOINT,
    _GEMINI_1P5_PRO_FLASH_PREVIEW_ENDPOINT,
    _GEMINI_1P5_PRO_001_ENDPOINT,
    _GEMINI_1P5_PRO_002_ENDPOINT,
    _GEMINI_1P5_FLASH_001_ENDPOINT,
    _GEMINI_1P5_FLASH_002_ENDPOINT,
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


_ML_GENERATE_TEXT_STATUS = "ml_generate_text_status"
_ML_EMBED_TEXT_STATUS = "ml_embed_text_status"
_ML_GENERATE_EMBEDDING_STATUS = "ml_generate_embedding_status"

_MODEL_NOT_SUPPORTED_WARNING = (
    "Model name '{model_name}' is not supported. "
    "We are currently aware of the following models: {known_models}. "
    "However, model names can change, and the supported models may be outdated. "
    "You should use this model name only if you are sure that it is supported in BigQuery."
)


@typing_extensions.deprecated(
    "PaLM2TextGenerator is going to be deprecated. Use GeminiTextGenerator(https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator) instead. ",
    category=exceptions.ApiDeprecationWarning,
)
@log_adapter.class_logger
class PaLM2TextGenerator(base.BaseEstimator):
    """PaLM2 text generator LLM model.

    .. note::
        PaLM2TextGenerator is going to be deprecated. Use GeminiTextGenerator(https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator) instead.

    Args:
        model_name (str, Default to "text-bison"):
            The model for natural language tasks. “text-bison” returns model fine-tuned to follow natural language instructions
            and is suitable for a variety of language tasks. "text-bison-32k" supports up to 32k tokens per request.
            Default to "text-bison".
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
        model_name: Literal["text-bison", "text-bison-32k"] = "text-bison",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
        max_iterations: int = 300,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self.max_iterations = max_iterations
        self._bq_connection_manager = self.session.bqconnectionmanager

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = clients.resolve_full_bq_connection_name(
            connection_name,
            default_project=self.session._project,
            default_location=self.session._location,
        )

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        if not self.connection_name:
            raise ValueError(
                "Must provide connection_name, either in constructor or through session options."
            )

        if self._bq_connection_manager:
            connection_name_parts = self.connection_name.split(".")
            if len(connection_name_parts) != 3:
                raise ValueError(
                    f"connection_name must be of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>, got {self.connection_name}."
                )
            self._bq_connection_manager.create_bq_connection(
                project_id=connection_name_parts[0],
                location=connection_name_parts[1],
                connection_id=connection_name_parts[2],
                iam_role="aiplatform.user",
            )

        if self.model_name not in _TEXT_GENERATOR_ENDPOINTS:
            warnings.warn(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_TEXT_GENERATOR_ENDPOINTS),
                )
            )

        options = {
            "endpoint": self.model_name,
        }

        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> PaLM2TextGenerator:
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
            "max_iterations": self.max_iterations,
            "data_split_method": "NO_SPLIT",
        }
        return options

    def fit(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
    ) -> PaLM2TextGenerator:
        """Fine tune PaLM2TextGenerator model.

        .. note::

            This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
            Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
            and might have limited support. For more information, see the launch stage descriptions
            (https://cloud.google.com/products#product-launch-stages).

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                DataFrame of shape (n_samples, n_features). Training data.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Training labels.

        Returns:
            PaLM2TextGenerator: Fitted estimator.
        """
        X, y = utils.convert_to_dataframe(X, y)

        options = self._bqml_options
        options["endpoint"] = self.model_name + "@001"
        options["prompt_col"] = X.columns.tolist()[0]

        self._bqml_model = self._bqml_model_factory.create_llm_remote_model(
            X,
            y,
            options=options,
            connection_name=self.connection_name,
        )
        return self

    def predict(
        self,
        X: utils.ArrayType,
        *,
        temperature: float = 0.0,
        max_output_tokens: int = 128,
        top_k: int = 40,
        top_p: float = 0.95,
    ) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "prompt" column for prediction.
                Prompts can include preamble, questions, suggestions, instructions, or examples.

            temperature (float, default 0.0):
                The temperature is used for sampling during the response generation, which occurs when topP and topK are applied.
                Temperature controls the degree of randomness in token selection. Lower temperatures are good for prompts that expect a true or correct response,
                while higher temperatures can lead to more diverse or unexpected results. A temperature of 0 is deterministic:
                the highest probability token is always selected. For most use cases, try starting with a temperature of 0.2.
                Default 0. Possible values [0.0, 1.0].

            max_output_tokens (int, default 128):
                Maximum number of tokens that can be generated in the response. Specify a lower value for shorter responses and a higher value for longer responses.
                A token may be smaller than a word. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.
                Default 128. For the 'text-bison' model, possible values are in the range [1, 1024]. For the 'text-bison-32k' model, possible values are in the range [1, 8192].
                Please ensure that the specified value for max_output_tokens is within the appropriate range for the model being used.

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


        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        if temperature < 0.0 or temperature > 1.0:
            raise ValueError(f"temperature must be [0.0, 1.0], but is {temperature}.")

        if (
            self.model_name == _TEXT_GENERATOR_BISON_ENDPOINT
            and max_output_tokens not in range(1, 1025)
        ):
            raise ValueError(
                f"max_output_token must be [1, 1024] for TextBison model, but is {max_output_tokens}."
            )

        if (
            self.model_name == _TEXT_GENERATOR_BISON_32K_ENDPOINT
            and max_output_tokens not in range(1, 8193)
        ):
            raise ValueError(
                f"max_output_token must be [1, 8192] for TextBison 32k model, but is {max_output_tokens}."
            )

        if top_k not in range(1, 41):
            raise ValueError(f"top_k must be [1, 40], but is {top_k}.")

        if top_p < 0.0 or top_p > 1.0:
            raise ValueError(f"top_p must be [0.0, 1.0], but is {top_p}.")

        (X,) = utils.convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "prompt"})

        options = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_text(X, options)

        if (df[_ML_GENERATE_TEXT_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_GENERATE_TEXT_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        task_type: Literal[
            "text_generation", "classification", "summarization", "question_answering"
        ] = "text_generation",
    ) -> bpd.DataFrame:
        """Calculate evaluation metrics of the model.

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

        X, y = utils.convert_to_dataframe(X, y, session=self._bqml_model.session)

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

    def to_gbq(self, model_name: str, replace: bool = False) -> PaLM2TextGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            PaLM2TextGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@typing_extensions.deprecated(
    "PaLM2TextEmbeddingGenerator has been deprecated. Use TextEmbeddingGenerator(https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.TextEmbeddingGenerator) instead. ",
    category=exceptions.ApiDeprecationWarning,
)
@log_adapter.class_logger
class PaLM2TextEmbeddingGenerator(base.BaseEstimator):
    """PaLM2 text embedding generator LLM model.

    .. note::
        PaLM2TextEmbeddingGenerator has been deprecated. Use TextEmbeddingGenerator(https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.TextEmbeddingGenerator) instead.


    Args:
        model_name (str, Default to "textembedding-gecko"):
            The model for text embedding. “textembedding-gecko” returns model embeddings for text inputs.
            "textembedding-gecko-multilingual" returns model embeddings for text inputs which support over 100 languages.
            Default to "textembedding-gecko".
        version (str or None):
            Model version. Accepted values are "001", "002", "003", "latest" etc. Will use the default version if unset.
            See https://cloud.google.com/vertex-ai/docs/generative-ai/learn/model-versioning for details.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context.
    """

    def __init__(
        self,
        *,
        model_name: Literal[
            "textembedding-gecko", "textembedding-gecko-multilingual"
        ] = "textembedding-gecko",
        version: Optional[str] = None,
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.model_name = model_name
        self.version = version
        self.session = session or bpd.get_global_session()
        self._bq_connection_manager = self.session.bqconnectionmanager

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = clients.resolve_full_bq_connection_name(
            connection_name,
            default_project=self.session._project,
            default_location=self.session._location,
        )

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        if not self.connection_name:
            raise ValueError(
                "Must provide connection_name, either in constructor or through session options."
            )

        if self._bq_connection_manager:
            connection_name_parts = self.connection_name.split(".")
            if len(connection_name_parts) != 3:
                raise ValueError(
                    f"connection_name must be of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>, got {self.connection_name}."
                )
            self._bq_connection_manager.create_bq_connection(
                project_id=connection_name_parts[0],
                location=connection_name_parts[1],
                connection_id=connection_name_parts[2],
                iam_role="aiplatform.user",
            )

        if self.model_name not in _PALM2_EMBEDDING_GENERATOR_ENDPOINTS:
            warnings.warn(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_PALM2_EMBEDDING_GENERATOR_ENDPOINTS),
                )
            )

        endpoint = (
            self.model_name + "@" + self.version if self.version else self.model_name
        )
        options = {
            "endpoint": endpoint,
        }
        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, bq_model: bigquery.Model
    ) -> PaLM2TextEmbeddingGenerator:
        assert bq_model.model_type == "MODEL_TYPE_UNSPECIFIED"
        assert "remoteModelInfo" in bq_model._properties
        assert "endpoint" in bq_model._properties["remoteModelInfo"]
        assert "connection" in bq_model._properties["remoteModelInfo"]

        # Parse the remote model endpoint
        bqml_endpoint = bq_model._properties["remoteModelInfo"]["endpoint"]
        model_connection = bq_model._properties["remoteModelInfo"]["connection"]
        model_endpoint = bqml_endpoint.split("/")[-1]

        model_name, version = utils.parse_model_endpoint(model_endpoint)

        model = cls(
            session=session,
            # str to literals
            model_name=model_name,  # type: ignore
            version=version,
            connection_name=model_connection,
        )

        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    def predict(self, X: utils.ArrayType) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "content" column for prediction.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        (X,) = utils.convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "content"})

        options = {
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_embedding(X, options)
        df = df.rename(
            columns={
                "ml_generate_embedding_result": "text_embedding",
                "ml_generate_embedding_statistics": "statistics",
                "ml_generate_embedding_status": _ML_EMBED_TEXT_STATUS,
            }
        )

        if (df[_ML_EMBED_TEXT_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_EMBED_TEXT_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df

    def to_gbq(
        self, model_name: str, replace: bool = False
    ) -> PaLM2TextEmbeddingGenerator:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            PaLM2TextEmbeddingGenerator: Saved model."""

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class TextEmbeddingGenerator(base.BaseEstimator):
    """Text embedding generator LLM model.

    Args:
        model_name (str, Default to "text-embedding-004"):
            The model for text embedding. Possible values are "text-embedding-004" or "text-multilingual-embedding-002".
            text-embedding models returns model embeddings for text inputs.
            text-multilingual-embedding models returns model embeddings for text inputs which support over 100 languages.
            Default to "text-embedding-004".
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context.
    """

    def __init__(
        self,
        *,
        model_name: Literal[
            "text-embedding-004", "text-multilingual-embedding-002"
        ] = "text-embedding-004",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self._bq_connection_manager = self.session.bqconnectionmanager

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = clients.resolve_full_bq_connection_name(
            connection_name,
            default_project=self.session._project,
            default_location=self.session._location,
        )

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        if not self.connection_name:
            raise ValueError(
                "Must provide connection_name, either in constructor or through session options."
            )

        if self._bq_connection_manager:
            connection_name_parts = self.connection_name.split(".")
            if len(connection_name_parts) != 3:
                raise ValueError(
                    f"connection_name must be of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>, got {self.connection_name}."
                )
            self._bq_connection_manager.create_bq_connection(
                project_id=connection_name_parts[0],
                location=connection_name_parts[1],
                connection_id=connection_name_parts[2],
                iam_role="aiplatform.user",
            )

        if self.model_name not in _TEXT_EMBEDDING_ENDPOINTS:
            warnings.warn(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_TEXT_EMBEDDING_ENDPOINTS),
                )
            )

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

    def predict(self, X: utils.ArrayType) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "content" column for prediction.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        (X,) = utils.convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "content"})

        options = {
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_embedding(X, options)

        if (df[_ML_GENERATE_EMBEDDING_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_GENERATE_EMBEDDING_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df

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
class GeminiTextGenerator(base.BaseEstimator):
    """Gemini text generator LLM model.

    Args:
        model_name (str, Default to "gemini-pro"):
            The model for natural language tasks. Accepted values are "gemini-pro", "gemini-1.5-pro-preview-0514", "gemini-1.5-flash-preview-0514", "gemini-1.5-pro-001", "gemini-1.5-pro-002", "gemini-1.5-flash-001" and "gemini-1.5-flash-002". Default to "gemini-pro".

        .. note::
            "gemini-1.5-pro-preview-0514" and "gemini-1.5-flash-preview-0514" is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
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
        model_name: Literal[
            "gemini-pro",
            "gemini-1.5-pro-preview-0514",
            "gemini-1.5-flash-preview-0514",
            "gemini-1.5-pro-001",
            "gemini-1.5-pro-002",
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-002",
        ] = "gemini-pro",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
        max_iterations: int = 300,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self.max_iterations = max_iterations
        self._bq_connection_manager = self.session.bqconnectionmanager

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = clients.resolve_full_bq_connection_name(
            connection_name,
            default_project=self.session._project,
            default_location=self.session._location,
        )

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        if not self.connection_name:
            raise ValueError(
                "Must provide connection_name, either in constructor or through session options."
            )

        if self._bq_connection_manager:
            connection_name_parts = self.connection_name.split(".")
            if len(connection_name_parts) != 3:
                raise ValueError(
                    f"connection_name must be of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>, got {self.connection_name}."
                )
            self._bq_connection_manager.create_bq_connection(
                project_id=connection_name_parts[0],
                location=connection_name_parts[1],
                connection_id=connection_name_parts[2],
                iam_role="aiplatform.user",
            )

        if self.model_name not in _GEMINI_ENDPOINTS:
            warnings.warn(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_GEMINI_ENDPOINTS),
                )
            )

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
        """Fine tune GeminiTextGenerator model. Only support "gemini-pro" model for now.

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
        if self._bqml_model.model_name.startswith("gemini-1.5"):
            raise NotImplementedError("Fit is not supported for gemini-1.5 model.")

        X, y = utils.convert_to_dataframe(X, y)

        options = self._bqml_options
        options["endpoint"] = "gemini-1.0-pro-002"
        options["prompt_col"] = X.columns.tolist()[0]

        self._bqml_model = self._bqml_model_factory.create_llm_remote_model(
            X,
            y,
            options=options,
            connection_name=self.connection_name,
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
    ) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Input DataFrame or Series, can contain one or more columns. If multiple columns are in the DataFrame, it must contain a "prompt" column for prediction.
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

            top_p (float, default 0.95)::
                Top-P changes how the model selects tokens for output. Tokens are selected from the most (see top-K) to least probable until the sum of their probabilities equals the top-P value. For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the top-P value is 0.5, then the model will select either A or B as the next token by using temperature and excludes C as a candidate.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 1.0. Possible values [0.0, 1.0].


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

        (X,) = utils.convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "prompt"})

        options = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_text(X, options)

        if (df[_ML_GENERATE_TEXT_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_GENERATE_TEXT_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df

    def score(
        self,
        X: utils.ArrayType,
        y: utils.ArrayType,
        task_type: Literal[
            "text_generation", "classification", "summarization", "question_answering"
        ] = "text_generation",
    ) -> bpd.DataFrame:
        """Calculate evaluation metrics of the model. Only "gemini-pro" model is supported for now.

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

        # TODO(ashleyxu): Support gemini-1.5 when the rollout is ready. b/344891364.
        if self._bqml_model.model_name.startswith("gemini-1.5"):
            raise NotImplementedError("Score is not supported for gemini-1.5 model.")

        X, y = utils.convert_to_dataframe(X, y, session=self._bqml_model.session)

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
class Claude3TextGenerator(base.BaseEstimator):
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
            Default to "claude-3-sonnet".
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
        model_name: Literal[
            "claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet", "claude-3-opus"
        ] = "claude-3-sonnet",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self._bq_connection_manager = self.session.bqconnectionmanager

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = clients.resolve_full_bq_connection_name(
            connection_name,
            default_project=self.session._project,
            default_location=self.session._location,
        )

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        if not self.connection_name:
            raise ValueError(
                "Must provide connection_name, either in constructor or through session options."
            )

        if self._bq_connection_manager:
            connection_name_parts = self.connection_name.split(".")
            if len(connection_name_parts) != 3:
                raise ValueError(
                    f"connection_name must be of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>, got {self.connection_name}."
                )
            self._bq_connection_manager.create_bq_connection(
                project_id=connection_name_parts[0],
                location=connection_name_parts[1],
                connection_id=connection_name_parts[2],
                iam_role="aiplatform.user",
            )

        if self.model_name not in _CLAUDE_3_ENDPOINTS:
            warnings.warn(
                _MODEL_NOT_SUPPORTED_WARNING.format(
                    model_name=self.model_name,
                    known_models=", ".join(_CLAUDE_3_ENDPOINTS),
                )
            )

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
    ) -> bpd.DataFrame:
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

        (X,) = utils.convert_to_dataframe(X, session=self._bqml_model.session)

        if len(X.columns) == 1:
            # BQML identified the column by name
            col_label = cast(blocks.Label, X.columns[0])
            X = X.rename(columns={col_label: "prompt"})

        options = {
            "max_output_tokens": max_output_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_text(X, options)

        if (df[_ML_GENERATE_TEXT_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_GENERATE_TEXT_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df

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
