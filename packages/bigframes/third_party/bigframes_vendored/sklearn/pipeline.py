"""
The :mod:`sklearn.pipeline` module implements utilities to build a composite
estimator, as a chain of transforms and estimators.
"""
# Author: Edouard Duchesnay
#         Gael Varoquaux
#         Virgile Fritsch
#         Alexandre Gramfort
#         Lars Buitinck
# License: BSD

from abc import ABCMeta

from bigframes import constants
from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class Pipeline(BaseEstimator, metaclass=ABCMeta):
    """Pipeline of transforms with a final estimator.

    Sequentially apply a list of transforms and a final estimator.
    Intermediate steps of the pipeline must be `transforms`, that is, they
    must implement `fit` and `transform` methods.
    The final estimator only needs to implement `fit`.

    The purpose of the pipeline is to assemble several steps that can be
    cross-validated together while setting different parameters. This simplifies code, and allows deploying an estimator
    and peprocessing together, e.g. with `Pipeline.to_gbq(...).`
    """

    def fit(
        self,
        X,
        y,
    ):
        """Fit the model.

        Fit all the transformers one after the other and transform the
        data. Finally, fit the transformed data using the final estimator.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A DataFrame or Series representing training data. Must match the
                input requirements of the first step of the pipeline.
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                A DataFrame or Series representing training targets, if applicable.

        Returns:
            Pipeline: Pipeline with fitted steps.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def score(self, X, y):
    """Transform the data, and apply `score` with the final estimator.

    Call `transform` of each transformer in the pipeline. The transformed
    data are finally passed to the final estimator that calls
    `score` method. Only valid if the final estimator implements `score`.

    Args:
        X (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A DataFrame or Series as evaluation data.
        y (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A DataFrame or Series as evaluation labels.

    Returns:;
        DataFrame: A DataFrame representing the result
            of calling `score` on the final estimator.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def predict(self, X):
    """Predict the pipeline result for each sample in X.

    Args:
        X (bigframes.dataframe.DataFrame or bigframes.series.Series):
            A DataFrame or Series to predict.

    Returns:
        bigframes.dataframe.DataFrame: A Dataframe representing
            predicted result.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
