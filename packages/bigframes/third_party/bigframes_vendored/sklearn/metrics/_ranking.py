"""Metrics to assess performance on classification task given scores.
Functions named as ``*_score`` return a scalar value to maximize: the higher
the better.
Function named as ``*_error`` or ``*_loss`` return a scalar value to minimize:
the lower the better.
"""

# Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#          Mathieu Blondel <mathieu@mblondel.org>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Arnaud Joly <a.joly@ulg.ac.be>
#          Jochen Wersdorfer <jochen@wersdoerfer.de>
#          Lars Buitinck
#          Joel Nothman <joel.nothman@gmail.com>
#          Noel Dawe <noel@dawe.me>
#          Michal Karbownik <michakarbownik@gmail.com>
# License: BSD 3 clause

from bigframes import constants


def auc(x, y) -> float:
    """Compute Area Under the Curve (AUC) using the trapezoidal rule.

    This is a general function, given points on a curve.  For computing the
    area under the ROC-curve, see :func:`roc_auc_score`.  For an alternative
    way to summarize a precision-recall curve, see
    :func:`average_precision_score`.

    Args:
        x (Series or DataFrame of shape (n_samples,)):
            X coordinates. These must be either monotonic increasing or monotonic
            decreasing.
        y (Series or DataFrame of shape (n_samples,)):
            Y coordinates.

    Returns:
        float: Area Under the Curve.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def roc_auc_score(y_true, y_score) -> float:
    """Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) \
    from prediction scores.

    Args:
        y_true (Series or DataFrame of shape (n_samples,)):
            True labels or binary label indicators. The binary and multiclass cases
            expect labels with shape (n_samples,) while the multilabel case expects
            binary label indicators with shape (n_samples, n_classes).
        y_score (Series or DataFrame of shape (n_samples,)):
            Target scores.
            * In the binary case, it corresponds to an array of shape
            `(n_samples,)`. Both probability estimates and non-thresholded
            decision values can be provided. The probability estimates correspond
            to the **probability of the class with the greater label**,
            i.e. `estimator.classes_[1]` and thus
            `estimator.predict_proba(X, y)[:, 1]`. The decision values
            corresponds to the output of `estimator.decision_function(X, y)`.

    Returns:
        float: Area Under the Curve score.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def roc_curve(
    y_true,
    y_score,
    drop_intermediate: bool = True,
):
    """Compute Receiver operating characteristic (ROC).

    Args:
        y_true: Series or DataFrame of shape (n_samples,)
            True binary labels. If labels are not either {-1, 1} or {0, 1}, then
            pos_label should be explicitly given.
        y_score: Series or DataFrame of shape (n_samples,)
            Target scores, can either be probability estimates of the positive
            class, confidence values, or non-thresholded measure of decisions
            (as returned by "decision_function" on some classifiers).
        drop_intermediate: bool, default=True
            Default to True. Whether to drop some suboptimal thresholds which would not appear
            on a plotted ROC curve. This is useful in order to create lighter
            ROC curves.

    Returns:
        fpr:
            Increasing false positive rates such that element i is the false
            positive rate of predictions with score >= `thresholds[i]`.
        tpr:
            Increasing true positive rates such that element `i` is the true
            positive rate of predictions with score >= `thresholds[i]`.
        thresholds:
            Decreasing thresholds on the decision function used to compute
            fpr and tpr. `thresholds[0]` represents no instances being predicted
            and is arbitrarily set to `max(y_score) + 1`.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
