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

"""Matrix Decomposition models. This module is styled after Scikit-Learn's decomposition module:
https://scikit-learn.org/stable/modules/decomposition.html."""

from __future__ import annotations

from typing import List, Optional, Union

from google.cloud import bigquery

import bigframes
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.decomposition._pca


@log_adapter.class_logger
class PCA(
    base.UnsupervisedTrainablePredictor,
    third_party.bigframes_vendored.sklearn.decomposition._pca.PCA,
):
    __doc__ = third_party.bigframes_vendored.sklearn.decomposition._pca.PCA.__doc__

    def __init__(self, n_components: int = 3):
        self.n_components = n_components
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(cls, session: bigframes.Session, model: bigquery.Model) -> PCA:
        assert model.model_type == "PCA"

        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        if "numPrincipalComponents" in last_fitting:
            kwargs["n_components"] = int(last_fitting["numPrincipalComponents"])

        new_pca = cls(**kwargs)
        new_pca._bqml_model = core.BqmlModel(session, model)
        return new_pca

    def _fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,
        transforms: Optional[List[str]] = None,
    ) -> PCA:
        (X,) = utils.convert_to_dataframe(X)

        self._bqml_model = self._bqml_model_factory.create_model(
            X_train=X,
            transforms=transforms,
            options={
                "model_type": "PCA",
                "num_principal_components": self.n_components,
            },
        )
        return self

    @property
    def components_(self) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before calling components_.")

        return self._bqml_model.principal_components()

    @property
    def explained_variance_(self) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError(
                "A model must be fitted before calling explained_variance_."
            )

        return self._bqml_model.principal_component_info()[
            ["principal_component_id", "eigenvalue"]
        ].rename(columns={"eigenvalue": "explained_variance"})

    @property
    def explained_variance_ratio_(self) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError(
                "A model must be fitted before calling explained_variance_ratio_."
            )

        return self._bqml_model.principal_component_info()[
            ["principal_component_id", "explained_variance_ratio"]
        ]

    def predict(self, X: Union[bpd.DataFrame, bpd.Series]) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.predict(X)

    def to_gbq(self, model_name: str, replace: bool = False) -> PCA:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            PCA: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)

    def score(
        self,
        X=None,
        y=None,
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        # TODO(b/291973741): X param is ignored. Update BQML supports input in ML.EVALUTE.
        return self._bqml_model.evaluate()
