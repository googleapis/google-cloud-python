"""Metrics to assess performance on classification task given class prediction.
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
#          Jatin Shah <jatindshah@gmail.com>
#          Saurabh Jha <saurabh.jhaa@gmail.com>
#          Bernardo Stein <bernardovstein@gmail.com>
#          Shangwu Yao <shangwuyao@gmail.com>
#          Michal Karbownik <michakarbownik@gmail.com>
# License: BSD 3 clause

from bigframes import constants


def accuracy_score(y_true, y_pred, normalize=True) -> float:
    """Accuracy classification score.

    Args:
        y_true (Series or DataFrame of shape (n_samples,)):
            Ground truth (correct) labels.
        y_pred (Series or DataFrame of shape (n_samples,)):
            Predicted labels, as returned by a classifier.
        normalize (bool, default True):
            Default to True. If ``False``, return the number of correctly
            classified samples. Otherwise, return the fraction of correctly
            classified samples.

    Returns:
        float: If ``normalize == True``, return the fraction of correctly
            classified samples (float), else returns the number of correctly
            classified samples (int).
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def confusion_matrix(
    y_true,
    y_pred,
):
    """Compute confusion matrix to evaluate the accuracy of a classification.

    By definition a confusion matrix :math:`C` is such that :math:`C_{i, j}`
    is equal to the number of observations known to be in group :math:`i` and
    predicted to be in group :math:`j`.

    Thus in binary classification, the count of true negatives is
    :math:`C_{0,0}`, false negatives is :math:`C_{1,0}`, true positives is
    :math:`C_{1,1}` and false positives is :math:`C_{0,1}`.

    Args:
        y_true (Series or DataFrame of shape (n_samples,)):
            Ground truth (correct) target values.
        y_pred (Series or DataFrame of shape (n_samples,)):
            Estimated targets as returned by a classifier.

    Returns:
        DataFrame of shape (n_samples, n_features): Confusion matrix whose
            i-th row and j-th   column entry indicates the number of
            samples with true label being i-th class and predicted label
            being j-th class.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def recall_score(
    y_true,
    y_pred,
    average: str = "binary",
):
    """Compute the recall.

    The recall is the ratio ``tp / (tp + fn)`` where ``tp`` is the number of
    true positives and ``fn`` the number of false negatives. The recall is
    intuitively the ability of the classifier to find all the positive samples.

    The best value is 1 and the worst value is 0.

    Args:
        y_true (Series or DataFrame of shape (n_samples,)):
            Ground truth (correct) target values.
        y_pred (Series or DataFrame of shape (n_samples,)):
            Estimated targets as returned by a classifier.
        average ({'micro', 'macro', 'samples', 'weighted', 'binary'} or None, \
                default='binary'):
            This parameter is required for multiclass/multilabel targets.
            Possible values are 'None', 'micro', 'macro', 'samples', 'weighted', 'binary'.

    Returns:
        float (if average is not None) or Series of float of shape n_unique_labels,): Recall
            of the positive class in binary classification or weighted
            average of the recall of each class for the multiclass task.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def precision_score(
    y_true,
    y_pred,
    average: str = "binary",
):
    """Compute the precision.

    The precision is the ratio ``tp / (tp + fp)`` where ``tp`` is the number of
    true positives and ``fp`` the number of false positives. The precision is
    intuitively the ability of the classifier not to label as positive a sample
    that is negative.

    The best value is 1 and the worst value is 0.

    Args:
        y_true: Series or DataFrame of shape (n_samples,)
            Ground truth (correct) target values.
        y_pred: Series or DataFrame of shape (n_samples,)
            Estimated targets as returned by a classifier.
        average: {'micro', 'macro', 'samples', 'weighted', 'binary'} or None, \
                default='binary'
            This parameter is required for multiclass/multilabel targets.
            Possible values are 'None', 'micro', 'macro', 'samples', 'weighted', 'binary'.

    Returns:
        precision: float (if average is not None) or Series of float of shape \
                (n_unique_labels,).
            Precision of the positive class in binary classification or weighted
            average of the precision of each class for the multiclass task.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def f1_score(
    y_true,
    y_pred,
    average: str = "binary",
):
    """Compute the F1 score, also known as balanced F-score or F-measure.

    The F1 score can be interpreted as a harmonic mean of the precision and
    recall, where an F1 score reaches its best value at 1 and worst score at 0.
    The relative contribution of precision and recall to the F1 score are
    equal. The formula for the F1 score is: F1 = 2 * (precision * recall) / (precision + recall).

    In the multi-class and multi-label case, this is the average of
    the F1 score of each class with weighting depending on the ``average``
    parameter.

    Args:
        y_true: Series or DataFrame of shape (n_samples,)
            Ground truth (correct) target values.
        y_pred: Series or DataFrame of shape (n_samples,)
            Estimated targets as returned by a classifier.
        average: {'micro', 'macro', 'samples', 'weighted', 'binary'} or None, \
                default='binary'
            This parameter is required for multiclass/multilabel targets.
            Possible values are 'None', 'micro', 'macro', 'samples', 'weighted', 'binary'.

    Returns:
        f1_score: float or Series of float, shape = [n_unique_labels]
            F1 score of the positive class in binary classification or weighted
            average of the F1 scores of each class for the multiclass task.

    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
