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

from typing import cast, Union

import bigframes
import bigframes.constants as constants
from bigframes.core import blocks
from bigframes.ml import base, core, utils
import bigframes.pandas as bpd

_REMOTE_TEXT_GENERATOR_MODEL_CODE = "CLOUD_AI_LARGE_LANGUAGE_MODEL_V1"
_TEXT_GENERATE_RESULT_COLUMN = "ml_generate_text_llm_result"

_REMOTE_EMBEDDING_GENERATOR_MODEL_CODE = "CLOUD_AI_TEXT_EMBEDDING_MODEL_V1"
_EMBED_TEXT_RESULT_COLUMN = "text_embedding"


class PaLM2TextGenerator(base.Predictor):
    """PaLM2 text generator LLM model.

    Args:
        session (BigQuery Session):
            BQ session to create the model
        connection_name (str):
            connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<REGION>.<CONNECTION_NAME>"""

    def __init__(self, session: bigframes.Session, connection_name: str):
        self.session = session
        self.connection_name = connection_name
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        options = {
            "remote_service_type": _REMOTE_TEXT_GENERATOR_MODEL_CODE,
        }

        return core.create_bqml_remote_model(
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
                Default 0.

            max_output_tokens (int, default 128):
                Maximum number of tokens that can be generated in the response. Specify a lower value for shorter responses and a higher value for longer responses.
                A token may be smaller than a word. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.
                Default 128.

            top_k (int, default 40):
                Top-k changes how the model selects tokens for output. A top-k of 1 means the selected token is the most probable among all tokens
                in the model’s vocabulary (also called greedy decoding), while a top-k of 3 means that the next token is selected from among the 3 most probable tokens (using temperature).
                For each token selection step, the top K tokens with the highest probabilities are sampled. Then tokens are further filtered based on topP with the final token selected using temperature sampling.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 40.

            top_p (float, default 0.95)::
                Top-p changes how the model selects tokens for output. Tokens are selected from most K (see topK parameter) probable to least until the sum of their probabilities equals the top-p value.
                For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the top-p value is 0.5, then the model will select either A or B as the next token (using temperature)
                and not consider C at all.
                Specify a lower value for less random responses and a higher value for more random responses.
                Default 0.95.


        Returns:
            bigframes.dataframe.DataFrame: Output DataFrame with only 1 column as the output text results."""

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
        return cast(
            bpd.DataFrame,
            df[[_TEXT_GENERATE_RESULT_COLUMN]],
        )


class PaLM2TextEmbeddingGenerator(base.Predictor):
    """PaLM2 text embedding generator LLM model.

    Args:
        session (BigQuery Session):
            BQ session to create the model
        connection_name (str):
            connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<REGION>.<CONNECTION_NAME>"""

    def __init__(self, session: bigframes.Session, connection_name: str):
        self.session = session
        self.connection_name = connection_name
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        options = {
            "remote_service_type": _REMOTE_EMBEDDING_GENERATOR_MODEL_CODE,
        }

        return core.create_bqml_remote_model(
            session=self.session, connection_name=self.connection_name, options=options
        )

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Input DataFrame, which needs to contain a column with name "content". Only the column will be used as input. Content can include preamble, questions, suggestions, instructions, or examples.

        Returns:
            bigframes.dataframe.DataFrame: Output DataFrame with only 1 column as the output embedding results
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
        return cast(
            bpd.DataFrame,
            df[[_EMBED_TEXT_RESULT_COLUMN]],
        )
