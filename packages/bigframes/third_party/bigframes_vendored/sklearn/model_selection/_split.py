"""
The :mod:`sklearn.model_selection._split` module includes classes and
functions to split the data based on a preset strategy.
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#         Gael Varoquaux <gael.varoquaux@normalesup.org>
#         Olivier Grisel <olivier.grisel@ensta.org>
#         Raghav RV <rvraghav93@gmail.com>
#         Leandro Hermida <hermidal@cs.umd.edu>
#         Rodion Martynov <marrodion@gmail.com>
# License: BSD 3 clause


from abc import ABCMeta

from bigframes import constants


class _BaseKFold(metaclass=ABCMeta):
    """Base class for K-Fold cross-validators."""

    def split(self, X, y=None):
        """Generate indices to split data into training and test set.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                BigFrames DataFrame or Series of shape (n_samples, n_features)
                Training data, where `n_samples` is the number of samples
                and `n_features` is the number of features.

            y (bigframes.dataframe.DataFrame, bigframes.series.Series or None):
                BigFrames DataFrame, Series of shape (n_samples,) or None.
                The target variable for supervised learning problems. Default to None.

        Yields:
            X_train (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The training data for that split.

            X_test (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The testing data for that split.

            y_train (bigframes.dataframe.DataFrame, bigframes.series.Series or None):
                The training label for that split.

            y_test (bigframes.dataframe.DataFrame, bigframes.series.Series or None):
                The testing label for that split.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def get_n_splits(self):
        """Returns the number of splitting iterations in the cross-validator.

        Returns:
            int: the number of splitting iterations in the cross-validator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


class KFold(_BaseKFold):
    """K-Fold cross-validator.

    Split data in train/test sets. Split dataset into k consecutive folds.

    Each fold is then used once as a validation while the k - 1 remaining
    folds form the training set.

    Args:
        n_splits (int):
            Number of folds. Must be at least 2. Default to 5.

        random_state (Optional[int]):
            A seed to use for randomly choosing the rows of the split. If not
            set, a random split will be generated each time. Default to None.
    """


def train_test_split(
    *arrays,
    test_size=None,
    train_size=None,
    random_state=None,
    stratify=None,
):
    """Splits dataframes or series into random train and test subsets.

    Args:
        *arrays (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A sequence of BigQuery DataFrames or Series that can be joined on
            their indexes.
        test_size (default None):
            The proportion of the dataset to include in the test split. If
            None, this will default to the complement of train_size. If both
            are none, it will be set to 0.25.
        train_size (default None):
            The proportion of the dataset to include in the train split. If
            None, this will default to the complement of test_size.
        random_state (default None):
            A seed to use for randomly choosing the rows of the split. If not
            set, a random split will be generated each time.
        stratify: (bigframes.series.Series or None, default None):
            If not None, data is split in a stratified fashion, using this as the class labels. Each split has the same distribution of the class labels with the original dataset.
            Default to None.
            Note: By setting the stratify parameter, the memory consumption and generated SQL will be linear to the unique values in the Series. May return errors if the unique values size is too large.

    Returns:
        List[Union[bigframes.dataframe.DataFrame, bigframes.series.Series]]: A list of BigQuery DataFrames or Series.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
