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

from typing import cast, Literal, Optional, Union
import warnings

import bigframes
from bigframes import clients, constants
from bigframes.core import blocks, log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd

_TEXT_GENERATOR_BISON_ENDPOINT = "text-bison"
_TEXT_GENERATOR_BISON_32K_ENDPOINT = "text-bison-32k"
_TEXT_GENERATOR_ENDPOINTS = (
    _TEXT_GENERATOR_BISON_ENDPOINT,
    _TEXT_GENERATOR_BISON_32K_ENDPOINT,
)

_EMBEDDING_GENERATOR_GECKO_ENDPOINT = "textembedding-gecko"
_EMBEDDING_GENERATOR_GECKO_MULTILINGUAL_ENDPOINT = "textembedding-gecko-multilingual"
_EMBEDDING_GENERATOR_ENDPOINTS = (
    _EMBEDDING_GENERATOR_GECKO_ENDPOINT,
    _EMBEDDING_GENERATOR_GECKO_MULTILINGUAL_ENDPOINT,
)

_ML_GENERATE_TEXT_STATUS = "ml_generate_text_status"
_ML_EMBED_TEXT_STATUS = "ml_embed_text_status"


@log_adapter.class_logger
class PaLM2TextGenerator(base.Predictor):
    """PaLM2 text generator LLM model.

    Args:
        model_name (str, Default to "text-bison"):
            The model for natural language tasks. “text-bison” returns model fine-tuned to follow natural language instructions
            and is suitable for a variety of language tasks. "text-bison-32k" supports up to 32k tokens per request.
            Default to "text-bison".
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            if None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
            permission if the connection isn't fully setup.
    """

    def __init__(
        self,
        model_name: Literal["text-bison", "text-bison-32k"] = "text-bison",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self._bq_connection_manager = clients.BqConnectionManager(
            self.session.bqconnectionclient, self.session.resourcemanagerclient
        )

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = self._bq_connection_manager.resolve_full_connection_name(
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
            raise ValueError(
                f"Model name {self.model_name} is not supported. We only support {', '.join(_TEXT_GENERATOR_ENDPOINTS)}."
            )

        options = {
            "endpoint": self.model_name,
        }

        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    def predict(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        temperature: float = 0.0,
        max_output_tokens: int = 128,
        top_k: int = 40,
        top_p: float = 0.95,
    ) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Input DataFrame or Series, which needs to contain a column with name "prompt". Only the column will be used as input.
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
                Default 128. Possible values [1, 1024].

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
        if max_output_tokens not in range(1, 1025):
            raise ValueError(
                f"max_output_token must be [1, 1024], but is {max_output_tokens}."
            )
        if top_k not in range(1, 41):
            raise ValueError(f"top_k must be [1, 40], but is {top_k}.")
        if top_p < 0.0 or top_p > 1.0:
            raise ValueError(f"top_p must be [0.0, 1.0], but is {top_p}.")

        (X,) = utils.convert_to_dataframe(X)

        if len(X.columns) != 1:
            raise ValueError(
                f"Only support one column as input. {constants.FEEDBACK_LINK}"
            )

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


@log_adapter.class_logger
class PaLM2TextEmbeddingGenerator(base.Predictor):
    """PaLM2 text embedding generator LLM model.

    Args:
        model_name (str, Default to "textembedding-gecko"):
            The model for text embedding. “textembedding-gecko” returns model embeddings for text inputs.
            "textembedding-gecko-multilingual" returns model embeddings for text inputs which support over 100 languages
            Default to "textembedding-gecko".
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            if None, use default connection in session context.
    """

    def __init__(
        self,
        model_name: Literal[
            "textembedding-gecko", "textembedding-gecko-multilingual"
        ] = "textembedding-gecko",
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.model_name = model_name
        self.session = session or bpd.get_global_session()
        self._bq_connection_manager = clients.BqConnectionManager(
            self.session.bqconnectionclient, self.session.resourcemanagerclient
        )

        connection_name = connection_name or self.session._bq_connection
        self.connection_name = self._bq_connection_manager.resolve_full_connection_name(
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

        if self.model_name not in _EMBEDDING_GENERATOR_ENDPOINTS:
            raise ValueError(
                f"Model name {self.model_name} is not supported. We only support {', '.join(_EMBEDDING_GENERATOR_ENDPOINTS)}."
            )

        options = {
            "endpoint": self.model_name,
        }
        return self._bqml_model_factory.create_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Input DataFrame, which needs to contain a column with name "content". Only the column will be used as input. Content can include preamble, questions, suggestions, instructions, or examples.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        # Params reference: https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
        (X,) = utils.convert_to_dataframe(X)

        if len(X.columns) != 1:
            raise ValueError(
                f"Only support one column as input. {constants.FEEDBACK_LINK}"
            )

        # BQML identified the column by name
        col_label = cast(blocks.Label, X.columns[0])
        X = X.rename(columns={col_label: "content"})

        options = {
            "flatten_json_output": True,
        }

        df = self._bqml_model.generate_text_embedding(X, options)

        if (df[_ML_EMBED_TEXT_STATUS] != "").any():
            warnings.warn(
                f"Some predictions failed. Check column {_ML_EMBED_TEXT_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df
