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
        auto_class_weights (default False):
            Default False. If True, balance class labels using weights for each
            class in inverse proportion to the frequency of that class.
    """

    def fit(
        self,
        X,
        y,
        transforms: Optional[List[str]] = None,
    ):
        """Fit the model according to the given training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                DataFrame of shape (n_samples,). Target vector relative to X.

            transforms (Optional[List[str]], default None):
                Do not use. Internal param to be deprecated.
                Use bigframes.ml.pipeline instead.


        Returns:
            LogisticRegression: Fitted Estimator.
        """
        raise NotImplementedError("abstract method")
