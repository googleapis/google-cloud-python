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

from typing import List, Literal, Optional, Union

import bigframes_vendored.sklearn.cluster._kmeans
from google.cloud import bigquery
import pandas as pd

import bigframes
from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd

_BQML_PARAMS_MAPPING = {
    "n_clusters": "numClusters",
    "init": "kmeansInitializationMethod",
    "init_col": "kmeansInitializationColumn",
    "distance_type": "distanceType",
    "max_iter": "maxIterations",
    "tol": "minRelativeProgress",
    "warm_start": "warmStart",
}


@log_adapter.class_logger
class KMeans(
    base.UnsupervisedTrainablePredictor,
    bigframes_vendored.sklearn.cluster._kmeans.KMeans,
):

    __doc__ = bigframes_vendored.sklearn.cluster._kmeans.KMeans.__doc__

    def __init__(
        self,
        n_clusters: int = 8,
        *,
        init: Literal["kmeans++", "random", "custom"] = "kmeans++",
        init_col: Optional[str] = None,
        distance_type: Literal["euclidean", "cosine"] = "euclidean",
        max_iter: int = 20,
        tol: float = 0.01,
        warm_start: bool = False,
    ):
        self.n_clusters = n_clusters
        # allow the alias to be compatible with sklean
        self.init = "kmeans++" if init == "k-means++" else init
        self.init_col = init_col
        self.distance_type = distance_type
        self.max_iter = max_iter
        self.tol = tol
        self.warm_start = warm_start
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(cls, session: bigframes.Session, bq_model: bigquery.Model) -> KMeans:
        assert bq_model.model_type == "KMEANS"

        kwargs: dict = {}

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options = {
            "model_type": "KMEANS",
            "num_clusters": self.n_clusters,
            "KMEANS_INIT_METHOD": self.init,
            "DISTANCE_TYPE": self.distance_type,
            "MAX_ITERATIONS": self.max_iter,
            "MIN_REL_PROGRESS": self.tol,
            "WARM_START": self.warm_start,
        }

        if self.init_col is not None:
            options["KMEANS_INIT_COL"] = self.init_col

        return options

    def _fit(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
        transforms: Optional[List[str]] = None,
    ) -> KMeans:
        (X,) = utils.batch_convert_to_dataframe(X)

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
        X: utils.ArrayType,
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def detect_anomalies(
        self,
        X: Union[bpd.DataFrame, bpd.Series, pd.DataFrame, pd.Series],
        *,
        contamination: float = 0.1,
    ) -> bpd.DataFrame:
        """Detect the anomaly data points of the input.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or a DataFrame to detect anomalies.
            contamination (float, default 0.1):
                Identifies the proportion of anomalies in the training dataset that are used to create the model.
                The value must be in the range [0, 0.5].

        Returns:
            bigframes.dataframe.DataFrame: detected DataFrame."""
        if contamination < 0.0 or contamination > 0.5:
            raise ValueError(
                f"contamination must be [0.0, 0.5], but is {contamination}."
            )

        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before detect_anomalies")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.detect_anomalies(
            X, options={"contamination": contamination}
        )

    def to_gbq(self, model_name: str, replace: bool = False) -> KMeans:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            KMeans: Saved model."""
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before it can be saved")

        new_model = self._bqml_model.copy(model_name, replace)
        return new_model.session.read_gbq_model(model_name)

    def score(
        self,
        X: utils.ArrayType,
        y=None,  # ignored
    ) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before score")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.evaluate(X)
