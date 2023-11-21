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

"""Clustering models. This module is styled after Scikit-Learn's cluster module:
https://scikit-learn.org/stable/modules/clustering.html."""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from google.cloud import bigquery

import bigframes
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd
import third_party.bigframes_vendored.sklearn.cluster._kmeans


@log_adapter.class_logger
class KMeans(
    base.UnsupervisedTrainablePredictor,
    third_party.bigframes_vendored.sklearn.cluster._kmeans.KMeans,
):

    __doc__ = third_party.bigframes_vendored.sklearn.cluster._kmeans.KMeans.__doc__

    def __init__(self, n_clusters: int = 8):
        self.n_clusters = n_clusters
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(cls, session: bigframes.Session, model: bigquery.Model) -> KMeans:
        assert model.model_type == "KMEANS"

        kwargs = {}

        # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
        last_fitting = model.training_runs[-1]["trainingOptions"]
        if "numClusters" in last_fitting:
            kwargs["n_clusters"] = int(last_fitting["numClusters"])

        new_kmeans = cls(**kwargs)
        new_kmeans._bqml_model = core.BqmlModel(session, model)
        return new_kmeans

    @property
    def _bqml_options(self) -> Dict[str, str | int | float | List[str]]:
        """The model options as they will be set for BQML"""
        return {"model_type": "KMEANS", "num_clusters": self.n_clusters}

    def _fit(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
        transforms: Optional[List[str]] = None,
    ) -> KMeans:
        (X,) = utils.convert_to_dataframe(X)

        self._bqml_model = self._bqml_model_factory.create_model(
            X_train=X,
            transforms=transforms,
            options=self._bqml_options,
        )
        return self

    @property
    def cluster_centers_(self) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError(
                "A model must be fitted before calling cluster_centers_."
            )

        return self._bqml_model.centroids()

    def predict(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.predict(X)

    def to_gbq(self, model_name: str, replace: bool = False) -> KMeans:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                the name of the model.
            replace (bool, default False):
                whether to replace if the model already exists. Default to False.

        Returns:
            KMeans: saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)

    def score(
        self,
        X: Union[bpd.DataFrame, bpd.Series],
        y=None,  # ignored
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        (X,) = utils.convert_to_dataframe(X)

        return self._bqml_model.evaluate(X)
