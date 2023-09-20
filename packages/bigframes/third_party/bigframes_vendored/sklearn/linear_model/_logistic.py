"""
Logistic Regression
"""

# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
#         Fabian Pedregosa <f@bianp.net>
#         Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#         Manoj Kumar <manojkumarsivaraj334@gmail.com>
#         Lars Buitinck
#         Simon Wu <s8wu@uwaterloo.ca>
#         Arthur Mensch <arthur.mensch@m4x.org
# Original location: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/linear_model/_logistic.py


from typing import List, Optional

from bigframes import constants
from third_party.bigframes_vendored.sklearn.linear_model._base import (
    BaseEstimator,
    LinearClassifierMixin,
)


class LogisticRegression(LinearClassifierMixin, BaseEstimator):
    """Logistic Regression (aka logit, MaxEnt) classifier.

    Args:
        fit_intercept (default True):
            Default True. Specifies if a constant (a.k.a. bias or intercept)
            should be added to the decision function.
        class_weights (dict or 'balanced', default None):
            Default None. Weights associated with classes in the form
            ``{class_label: weight}``.If not given, all classes are supposed
            to have weight one. The "balanced" mode uses the values of y to
            automatically adjust weights inversely proportional to class
            frequencies in the input data as
            ``n_samples / (n_classes * np.bincount(y))``. Dict isn't
            supported now.
    """

    def fit(
        self,
        X,
        y,
    ):
        """Fit the model according to the given training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples,). Target vector relative to X.


        Returns:
            LogisticRegression: Fitted Estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
