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

"""Imported models."""

from __future__ import annotations

from typing import cast, Optional, Union

from google.cloud import bigquery

import bigframes
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd


@log_adapter.class_logger
class TensorFlowModel(base.Predictor):
    """Imported TensorFlow model.

    Args:
        session (BigQuery Session):
            BQ session to create the model
        model_path (str):
            GCS path that holds the model files."""

    def __init__(
        self,
        session: Optional[bigframes.Session] = None,
        model_path: Optional[str] = None,
    ):
        self.session = session or bpd.get_global_session()
        self.model_path = model_path
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    def _create_bqml_model(self):
        options = {"model_type": "TENSORFLOW", "model_path": self.model_path}
        return self._bqml_model_factory.create_imported_model(
            session=self.session, options=options
        )

    @classmethod
    def _from_bq(
        cls, session: bigframes.Session, model: bigquery.Model
    ) -> TensorFlowModel:
        assert model.model_type == "TENSORFLOW"

        tf_model = cls(session=session, model_path=None)
        tf_model._bqml_model = core.BqmlModel(session, model)
        return tf_model

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame):
                Input DataFrame, schema is defined by the model.

        Returns:
            bigframes.dataframe.DataFrame: Output DataFrame, schema is defined by the model."""

        if not self._bqml_model:
            if self.model_path is None:
                raise ValueError("Model GCS path must be provided.")
            self._bqml_model = self._create_bqml_model()
        self._bqml_model = cast(core.BqmlModel, self._bqml_model)

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.predict(X)

    def to_gbq(self, model_name: str, replace: bool = False) -> TensorFlowModel:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            TensorFlowModel: saved model."""
        if not self._bqml_model:
            if self.model_path is None:
                raise ValueError("Model GCS path must be provided.")
            self._bqml_model = self._create_bqml_model()
        self._bqml_model = cast(core.BqmlModel, self._bqml_model)

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)


@log_adapter.class_logger
class ONNXModel(base.Predictor):
    """Imported Open Neural Network Exchange (ONNX) model.

    Args:
        session (BigQuery Session):
            BQ session to create the model
        model_path (str):
            Cloud Storage path that holds the model files."""

    def __init__(
        self,
        session: Optional[bigframes.Session] = None,
        model_path: Optional[str] = None,
    ):
        self.session = session or bpd.get_global_session()
        self.model_path = model_path
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    def _create_bqml_model(self):
        options = {"model_type": "ONNX", "model_path": self.model_path}
        return self._bqml_model_factory.create_imported_model(
            session=self.session, options=options
        )

    @classmethod
    def _from_bq(cls, session: bigframes.Session, model: bigquery.Model) -> ONNXModel:
        assert model.model_type == "ONNX"

        onnx_model = cls(session=session, model_path=None)
        onnx_model._bqml_model = core.BqmlModel(session, model)
        return onnx_model

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Input DataFrame or Series, schema is defined by the model.

        Returns:
            bigframes.dataframe.DataFrame: Output DataFrame, schema is defined by the model."""

        if not self._bqml_model:
            if self.model_path is None:
                raise ValueError("Model GCS path must be provided.")
            self._bqml_model = self._create_bqml_model()
        self._bqml_model = cast(core.BqmlModel, self._bqml_model)

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.predict(X)

    def to_gbq(self, model_name: str, replace: bool = False) -> ONNXModel:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            ONNXModel: saved model."""
        if not self._bqml_model:
            if self.model_path is None:
                raise ValueError("Model GCS path must be provided.")
            self._bqml_model = self._create_bqml_model()
        self._bqml_model = cast(core.BqmlModel, self._bqml_model)

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)
