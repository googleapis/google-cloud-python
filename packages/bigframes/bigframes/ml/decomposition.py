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

from typing import List, Literal, Optional, Union

import bigframes_vendored.sklearn.decomposition._mf
import bigframes_vendored.sklearn.decomposition._pca
from google.cloud import bigquery

from bigframes.core import log_adapter
from bigframes.ml import base, core, globals, utils
import bigframes.pandas as bpd
import bigframes.session

_BQML_PARAMS_MAPPING = {
    "svd_solver": "pcaSolver",
    "feedback_type": "feedbackType",
    "num_factors": "numFactors",
    "user_col": "userColumn",
    "item_col": "itemColumn",
    "_input_label_columns": "inputLabelColumns",
    "l2_reg": "l2Regularization",
}


@log_adapter.class_logger
class PCA(
    base.UnsupervisedTrainablePredictor,
    bigframes_vendored.sklearn.decomposition._pca.PCA,
):
    __doc__ = bigframes_vendored.sklearn.decomposition._pca.PCA.__doc__

    def __init__(
        self,
        n_components: Optional[Union[int, float]] = None,
        *,
        svd_solver: Literal["full", "randomized", "auto"] = "auto",
    ):
        self.n_components = n_components
        self.svd_solver = svd_solver
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> PCA:
        assert bq_model.model_type == "PCA"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        last_fitting = bq_model.training_runs[-1]["trainingOptions"]
        if "numPrincipalComponents" in last_fitting:
            kwargs["n_components"] = int(last_fitting["numPrincipalComponents"])
        elif "pcaExplainedVarianceRatio" in last_fitting:
            kwargs["n_components"] = float(last_fitting["pcaExplainedVarianceRatio"])

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options: dict = {
            "model_type": "PCA",
            "pca_solver": self.svd_solver,
        }

        assert self.n_components is not None
        if 0 < self.n_components < 1:
            options["pca_explained_variance_ratio"] = float(self.n_components)
        elif self.n_components >= 1:
            options["num_principal_components"] = int(self.n_components)

        return options

    def _fit(
        self,
        X: utils.ArrayType,
        y=None,
        transforms: Optional[List[str]] = None,
    ) -> PCA:
        (X,) = utils.batch_convert_to_dataframe(X)

        # To mimic sklearn's behavior
        if self.n_components is None:
            self.n_components = min(X.shape)
        self._bqml_model = self._bqml_model_factory.create_model(
            X_train=X,
            transforms=transforms,
            options=self._bqml_options,
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

    def predict(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before predict")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.predict(X)

    def detect_anomalies(
        self,
        X: utils.ArrayType,
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

    def to_gbq(self, model_name: str, replace: bool = False) -> PCA:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            PCA: Saved model."""
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

        # TODO(b/291973741): X param is ignored. Update BQML supports input in ML.EVALUATE.
        return self._bqml_model.evaluate()


@log_adapter.class_logger
class MatrixFactorization(
    base.UnsupervisedTrainablePredictor,
    bigframes_vendored.sklearn.decomposition._mf.MatrixFactorization,
):
    __doc__ = bigframes_vendored.sklearn.decomposition._mf.MatrixFactorization.__doc__

    def __init__(
        self,
        *,
        feedback_type: Literal["explicit", "implicit"] = "explicit",
        num_factors: int,
        user_col: str,
        item_col: str,
        rating_col: str = "rating",
        # TODO: Add support for hyperparameter tuning.
        l2_reg: float = 1.0,
    ):

        feedback_type = feedback_type.lower()  # type: ignore
        if feedback_type not in ("explicit", "implicit"):
            raise ValueError("Expected feedback_type to be `explicit` or `implicit`.")

        self.feedback_type = feedback_type

        if not isinstance(num_factors, int):
            raise TypeError(
                f"Expected num_factors to be an int, but got {type(num_factors)}."
            )

        if num_factors < 0:
            raise ValueError(
                f"Expected num_factors to be a positive integer, but got {num_factors}."
            )

        self.num_factors = num_factors

        if not isinstance(user_col, str):
            raise TypeError(f"Expected user_col to be a str, but got {type(user_col)}.")

        self.user_col = user_col

        if not isinstance(item_col, str):
            raise TypeError(f"Expected item_col to be STR, but got {type(item_col)}.")

        self.item_col = item_col

        if not isinstance(rating_col, str):
            raise TypeError(
                f"Expected rating_col to be a str, but got {type(rating_col)}."
            )

        self._input_label_columns = [rating_col]

        if not isinstance(l2_reg, (float, int)):
            raise TypeError(
                f"Expected l2_reg to be a float or int, but got {type(l2_reg)}."
            )

        self.l2_reg = l2_reg
        self._bqml_model: Optional[core.BqmlModel] = None
        self._bqml_model_factory = globals.bqml_model_factory()

    @property
    def rating_col(self) -> str:
        """str: The rating column name. Defaults to 'rating'."""
        return self._input_label_columns[0]

    @classmethod
    def _from_bq(
        cls, session: bigframes.session.Session, bq_model: bigquery.Model
    ) -> MatrixFactorization:
        assert bq_model.model_type == "MATRIX_FACTORIZATION"

        kwargs = utils.retrieve_params_from_bq_model(
            cls, bq_model, _BQML_PARAMS_MAPPING
        )

        model = cls(**kwargs)
        model._bqml_model = core.BqmlModel(session, bq_model)
        return model

    @property
    def _bqml_options(self) -> dict:
        """The model options as they will be set for BQML"""
        options: dict = {
            "model_type": "matrix_factorization",
            "feedback_type": self.feedback_type,
            "user_col": self.user_col,
            "item_col": self.item_col,
            "rating_col": self.rating_col,
            "l2_reg": self.l2_reg,
        }

        if self.num_factors is not None:
            options["num_factors"] = self.num_factors

        return options

    def _fit(
        self,
        X: utils.ArrayType,
        y=None,
        transforms: Optional[List[str]] = None,
    ) -> MatrixFactorization:
        if y is not None:
            raise ValueError(
                "Label column not supported for Matrix Factorization model but y was not `None`"
            )

        (X,) = utils.batch_convert_to_dataframe(X)

        self._bqml_model = self._bqml_model_factory.create_model(
            X_train=X,
            transforms=transforms,
            options=self._bqml_options,
        )
        return self

    def predict(self, X: utils.ArrayType) -> bpd.DataFrame:
        if not self._bqml_model:
            raise RuntimeError("A model must be fitted before recommend")

        (X,) = utils.batch_convert_to_dataframe(X, session=self._bqml_model.session)

        return self._bqml_model.recommend(X)

    def to_gbq(self, model_name: str, replace: bool = False) -> MatrixFactorization:
        """Save the model to BigQuery.

        Args:
            model_name (str):
                The name of the model.
            replace (bool, default False):
                Determine whether to replace if the model already exists. Default to False.

        Returns:
            MatrixFactorization: Saved model."""
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

        if X is not None and y is not None:
            X, y = utils.batch_convert_to_dataframe(
                X, y, session=self._bqml_model.session
            )
            input_data = X.join(y, how="outer")
        else:
            input_data = X

        return self._bqml_model.evaluate(input_data)
