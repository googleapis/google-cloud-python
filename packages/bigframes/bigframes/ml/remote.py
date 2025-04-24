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

"""BigFrames general remote models."""

from __future__ import annotations

from typing import Mapping, Optional
import warnings

from bigframes.core import global_session, log_adapter
import bigframes.dataframe
import bigframes.exceptions as bfe
from bigframes.ml import base, core, globals, utils
import bigframes.session

_REMOTE_MODEL_STATUS = "remote_model_status"


@log_adapter.class_logger
class VertexAIModel(base.BaseEstimator):
    """Remote model from a Vertex AI HTTPS endpoint. User must specify HTTPS endpoint, input schema and output schema.
    For more information, see Deploy model on Vertex AI: https://cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial#Deploy-Model-on-Vertex-AI.

    Args:
        endpoint (str):
            Vertex AI HTTPS endpoint.
        input (Mapping):
            Input schema: `{column_name: column_type}`. Supported types are "bool", "string", "int64", "float64", "array<bool>", "array<string>", "array<int64>", "array<float64>".
        output (Mapping):
            Output label schema: `{column_name: column_type}`. Supported the same types as the input.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            If None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
            permission if the connection isn't fully set up.
    """

    def __init__(
        self,
        endpoint: str,
        input: Mapping[str, str],
        output: Mapping[str, str],
        *,
        session: Optional[bigframes.session.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.endpoint = endpoint
        self.input = input
        self.output = output
        self.session = session or global_session.get_global_session()

        self._bq_connection_manager = self.session.bqconnectionmanager
        self.connection_name = connection_name

        self._bqml_model_factory = globals.bqml_model_factory()
        self._bqml_model: core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        # Parse and create connection if needed.
        self.connection_name = self.session._create_bq_connection(
            connection=self.connection_name, iam_role="aiplatform.user"
        )

        options = {
            "endpoint": self.endpoint,
        }

        self.input = {
            k: utils.standardize_type(v, globals._REMOTE_MODEL_SUPPORTED_DTYPES)
            for k, v in self.input.items()
        }
        self.output = {
            k: utils.standardize_type(v, globals._REMOTE_MODEL_SUPPORTED_DTYPES)
            for k, v in self.output.items()
        }

        return self._bqml_model_factory.create_remote_model(
            session=self.session,
            connection_name=self.connection_name,
            input=self.input,
            output=self.output,
            options=options,
        )

    def predict(
        self,
        X: utils.ArrayType,
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from the input DataFrame.

        Args:
            X (bigframes.pandas.DataFrame or bigframes.pandas.Series or pandas.DataFrame or pandas.Series):
                Input DataFrame or Series, which needs to comply with the input parameter of the model.

        Returns:
            bigframes.pandas.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        df = self._bqml_model.predict(X)

        # unlike LLM models, the general remote model status is null for successful runs.
        if (df[_REMOTE_MODEL_STATUS].notna()).any():
            msg = bfe.format_message(
                f"Some predictions failed. Check column {_REMOTE_MODEL_STATUS} for "
                "detailed status. You may want to filter the failed rows and retry."
            )
            warnings.warn(msg, category=RuntimeWarning)

        return df
