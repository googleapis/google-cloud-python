"""
Generalized Linear Models.
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# Fabian Pedregosa <fabian.pedregosa@inria.fr>
# Olivier Grisel <olivier.grisel@ensta.org>
#         Vincent Michel <vincent.michel@inria.fr>
#         Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Mathieu Blondel <mathieu@mblondel.org>
#         Lars Buitinck
#         Maryan Morel <maryan.morel@polytechnique.edu>
#         Giorgio Patrini <giorgio.patrini@anu.edu.au>
#         Maria Telenczuk <https://github.com/maikia>
# License: BSD 3 clause
# Original location: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/linear_model/_base.py

from abc import ABCMeta
from typing import List, Optional

from third_party.bigframes_vendored.sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
    RegressorMixin,
)


class LinearModel(BaseEstimator, metaclass=ABCMeta):
    def predict(self, X):
        """Predict using the linear model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Samples.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples,). Returns predicted values.
        """
        raise NotImplementedError("abstract method")


class LinearClassifierMixin(ClassifierMixin):
    def predict(self, X):
        """Predict class labels for samples in X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            bigframes.dataframe.DataFrame:  DataFrame of shape (n_samples,), containing
                the class labels for each sample.
        """
        raise NotImplementedError("abstract method")


class LinearRegression(RegressorMixin, LinearModel):
    """Ordinary least squares Linear Regression.

    LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
    to minimize the residual sum of squares between the observed targets in
    the dataset, and the targets predicted by the linear approximation.

    Args:
        fit_intercept (default True):
            Default ``True``. Whether to calculate the intercept for this
            model. If set to False, no intercept will be used in calculations
            (i.e. data is expected to be centered).
    """

    def fit(
        self,
        X,
        y,
        transforms: Optional[List[str]] = None,
    ):
        """Fit linear model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training data.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Target values. Will be cast to X's dtype if necessary.

            transforms (Optional[List[str]], default None):
                Do not use. Internal param to be deprecated.
                Use bigframes.ml.pipeline instead.

        Returns:
            LinearRegression: Fitted Estimator.
        """
        raise NotImplementedError("abstract method")
