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

from bigframes import constants
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
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class LinearClassifierMixin(ClassifierMixin):
    def predict(self, X):
        """Predict class labels for samples in X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). The data matrix for
                which we want to get the predictions.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of shape (n_samples, n_input_columns + n_prediction_columns). Returns predicted values.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class LinearRegression(RegressorMixin, LinearModel):
    """Ordinary least squares Linear Regression.

    LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
    to minimize the residual sum of squares between the observed targets in
    the dataset, and the targets predicted by the linear approximation.

    Args:
        optimize_strategy (str, default "normal_equation"):
            The strategy to train linear regression models. Possible values are
            "auto_strategy", "batch_gradient_descent", "normal_equation". Default
            to "normal_equation".
        fit_intercept (bool, default True):
            Default ``True``. Whether to calculate the intercept for this
            model. If set to False, no intercept will be used in calculations
            (i.e. data is expected to be centered).
        l2_reg (float, default 0.0):
            The amount of L2 regularization applied. Default to 0.
        max_iterations (int, default 20):
            The maximum number of training iterations or steps. Default to 20.
        learn_rate_strategy (str, default "line_search"):
            The strategy for specifying the learning rate during training. Default to "line_search".
        early_stop (bool, default True):
            Whether training should stop after the first iteration in which the relative loss improvement is less than the value specified for min_rel_progress. Default to True.
        min_rel_progress (float, default 0.01):
            The minimum relative loss improvement that is necessary to continue training when EARLY_STOP is set to true. For example, a value of 0.01 specifies that each iteration must reduce the loss by 1% for training to continue. Default to 0.01.
        ls_init_learn_rate (float, default 0.1):
            Sets the initial learning rate that learn_rate_strategy='line_search' uses. This option can only be used if line_search is specified. Default to 0.1.
        calculate_p_values (bool, default False):
            Specifies whether to compute p-values and standard errors during training. Default to False.
        enable_global_explain (bool, default False):
            Whether to compute global explanations using explainable AI to evaluate global feature importance to the model. Default to False.
    """

    def fit(
        self,
        X,
        y,
    ):
        """Fit linear model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training data.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples,) or (n_samples, n_targets).
                Target values. Will be cast to X's dtype if necessary.

        Returns:
            LinearRegression: Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
