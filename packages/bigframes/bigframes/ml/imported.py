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

from typing import cast, TYPE_CHECKING

if TYPE_CHECKING:
    import bigframes

import bigframes.ml.base
import bigframes.ml.core


class TensorFlowModel(bigframes.ml.base.Predictor):
    """Imported TensorFlow model.

    Args:
        session: BQ session to create the model
        model_path: GCS path that holds the model files."""

    def __init__(self, session: bigframes.Session, model_path: str):
        self.session = session
        self.model_path = model_path
        self._bqml_model: bigframes.ml.core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        options = {"model_type": "TENSORFLOW", "model_path": self.model_path}
        return bigframes.ml.core.create_bqml_imported_model(
            session=self.session, options=options
        )

    def predict(
        self, X: bigframes.dataframe.DataFrame
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X: Input DataFrame, schema is defined by the model.

        Returns: Output DataFrame, schema is defined by the model."""
        df = self._bqml_model.predict(X)
        return cast(
            bigframes.dataframe.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )


class OnnxModel(bigframes.ml.base.BaseEstimator):
    """Imported Open Neural Network Exchange (ONNX) model.

    Args:
        session: BQ session to create the model
        model_path: GCS path that holds the model files."""

    def __init__(self, session: bigframes.Session, model_path: str):
        self.session = session
        self.model_path = model_path
        self._bqml_model: bigframes.ml.core.BqmlModel = self._create_bqml_model()

    def _create_bqml_model(self):
        options = {"model_type": "ONNX", "model_path": self.model_path}
        return bigframes.ml.core.create_bqml_imported_model(
            session=self.session, options=options
        )

    def predict(
        self, X: bigframes.dataframe.DataFrame
    ) -> bigframes.dataframe.DataFrame:
        """Predict the result from input DataFrame.

        Args:
            X: Input DataFrame, schema is defined by the model.

        Returns: Output DataFrame, schema is defined by the model."""
        df = self._bqml_model.predict(X)
        return cast(
            bigframes.dataframe.DataFrame,
            df[
                [
                    cast(str, field.name)
                    for field in self._bqml_model.model.label_columns
                ]
            ],
        )
