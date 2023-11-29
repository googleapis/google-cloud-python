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

from typing import Mapping, Optional, Union
import warnings

import bigframes
from bigframes import clients
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd

_SUPPORTED_DTYPES = (
    "bool",
    "string",
    "int64",
    "float64",
    "array<bool>",
    "array<string>",
    "array<int64>",
    "array<float64>",
)

_REMOTE_MODEL_STATUS = "remote_model_status"


@log_adapter.class_logger
class VertexAIModel(base.BaseEstimator):
    """Remote model from a Vertex AI https endpoint. User must specify https endpoint, input schema and output schema.
    How to deploy a model in Vertex AI https://cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial#Deploy-Model-on-Vertex-AI.

    Args:
        endpoint (str):
            Vertex AI https endpoint.
        input ({column_name: column_type}):
            Input schema. Supported types are "bool", "string", "int64", "float64", "array<bool>", "array<string>", "array<int64>", "array<float64>".
        output ({column_name: column_type}):
            Output label schema. Supported the same types as the input.
        session (bigframes.Session or None):
            BQ session to create the model. If None, use the global default session.
        connection_name (str or None):
            Connection to connect with remote service. str of the format <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
            if None, use default connection in session context. BigQuery DataFrame will try to create the connection and attach
            permission if the connection isn't fully setup.
    """

    def __init__(
        self,
        endpoint: str,
        input: Mapping[str, str],
        output: Mapping[str, str],
        session: Optional[bigframes.Session] = None,
        connection_name: Optional[str] = None,
    ):
        self.endpoint = endpoint
        self.input = input
        self.output = output
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

        options = {
            "endpoint": self.endpoint,
        }

        def standardize_type(v: str):
            v = v.lower()
            v = v.replace("boolean", "bool")

            if v not in _SUPPORTED_DTYPES:
                raise ValueError(
                    f"Data type {v} is not supported. We only support {', '.join(_SUPPORTED_DTYPES)}."
                )

            return v

        self.input = {k: standardize_type(v) for k, v in self.input.items()}
        self.output = {k: standardize_type(v) for k, v in self.output.items()}

        return self._bqml_model_factory.create_remote_model(
            session=self.session,
            connection_name=self.connection_name,
            input=self.input,
            output=self.output,
            options=options,
        )

    def predict(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        """Predict the result from the input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Input DataFrame or Series, which needs to comply with the input parameter of the model.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """

        (X,) = utils.convert_to_dataframe(X)

        df = self._bqml_model.predict(X)

        # unlike LLM models, the general remote model status is null for successful runs.
        if (df[_REMOTE_MODEL_STATUS].notna()).any():
            warnings.warn(
                f"Some predictions failed. Check column {_REMOTE_MODEL_STATUS} for detailed status. You may want to filter the failed rows and retry.",
                RuntimeWarning,
            )

        return df
