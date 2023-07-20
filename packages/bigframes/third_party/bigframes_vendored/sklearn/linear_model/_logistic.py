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
        fit_intercept:
            Default True. Specifies if a constant (a.k.a. bias or intercept)
            should be added to the decision function.
        auto_class_weights:
            Default False. If True, balance class labels using weights for each
            class in inverse proportion to the frequency of that class.

    References:
        L-BFGS-B -- Software for Large-scale Bound-constrained Optimization
            Ciyou Zhu, Richard Byrd, Jorge Nocedal and Jose Luis Morales.
            http://users.iems.northwestern.edu/~nocedal/lbfgsb.html

        LIBLINEAR -- A Library for Large Linear Classification
            https://www.csie.ntu.edu.tw/~cjlin/liblinear/

        SAG -- Mark Schmidt, Nicolas Le Roux, and Francis Bach
            Minimizing Finite Sums with the Stochastic Average Gradient
            https://hal.inria.fr/hal-00860051/document

        SAGA -- Defazio, A., Bach F. & Lacoste-Julien S. (2014).
                "SAGA: A Fast Incremental Gradient Method With Support
                for Non-Strongly Convex Composite Objectives" (Arxiv <1407.0202>)

        Hsiang-Fu Yu, Fang-Lan Huang, Chih-Jen Lin (2011). Dual coordinate descent
            methods for logistic regression and maximum entropy models.
            Machine Learning 85(1-2):41-75.
            https://www.csie.ntu.edu.tw/~cjlin/papers/maxent_dual.pdf
    """

    def fit(
        self,
        X,
        y,
        transforms: Optional[List[str]] = None,
    ):
        """Fit the model according to the given training data.

        Args:
            X:
                DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y:
                DataFrame of shape (n_samples,). Target vector relative to X.

            transforms:
                An optional list of SQL expressions to apply over top of the
                model inputs as preprocessing. This preprocessing will be
                automatically reapplied to new input data (e.g. in .predict),
                and may contain steps (like ML.STANDARD_SCALER) that fit to the
                training data.

        Returns:
            Fitted estimator.
        """
        raise NotImplementedError("abstract method")
