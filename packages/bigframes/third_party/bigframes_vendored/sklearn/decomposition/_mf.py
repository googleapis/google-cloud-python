""" Matrix Factorization.
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#         Olivier Grisel <olivier.grisel@ensta.org>
#         Mathieu Blondel <mathieu@mblondel.org>
#         Denis A. Engemann <denis-alexander.engemann@inria.fr>
#         Michael Eickenberg <michael.eickenberg@inria.fr>
#         Giorgio Patrini <giorgio.patrini@anu.edu.au>
#
# License: BSD 3 clause

from abc import ABCMeta

from bigframes_vendored.sklearn.base import BaseEstimator

from bigframes import constants


class MatrixFactorization(BaseEstimator, metaclass=ABCMeta):
    """Matrix Factorization (MF).

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> from bigframes.ml.decomposition import MatrixFactorization
        >>> bpd.options.display.progress_bar = None
        >>> X = bpd.DataFrame({
        ... "row": [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
        ... "column": [0,1] * 7,
        ... "value": [1, 1, 2, 1, 3, 1.2, 4, 1, 5, 0.8, 6, 1, 2, 3],
        ... })
        >>> model = MatrixFactorization(feedback_type='explicit', num_factors=6, user_col='row', item_col='column', rating_col='value', l2_reg=2.06)
        >>> W = model.fit(X)

    Args:
        feedback_type ('explicit' | 'implicit'):
            Specifies the feedback type for the model. The feedback type determines the algorithm that is used during training.
        num_factors (int or auto, default auto):
            Specifies the number of latent factors to use.
        user_col (str):
            The user column name.
        item_col (str):
            The item column name.
        l2_reg (float, default 1.0):
            A floating point value for L2 regularization. The default value is 1.0.
    """

    def fit(self, X, y=None):
        """Fit the model according to the given training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (default None):
                Ignored.

        Returns:
            bigframes.ml.decomposition.MatrixFactorization: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def score(self, X=None, y=None):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#matrix_factorization_models
            for the outputs relevant to this model type.

        Args:
            X (bigframes.dataframe.DataFrame | bigframes.series.Series | None):
                DataFrame of shape (n_samples, n_features). Test samples.

            y (bigframes.dataframe.DataFrame | bigframes.series.Series | None):
                DataFrame of shape (n_samples,) or (n_samples, n_outputs). True
                labels for `X`.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame that represents model metrics.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def predict(self, X):
        """Generate a predicted rating for every user-item row combination for a matrix factorization model.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or a DataFrame to predict.

        Returns:
            bigframes.dataframe.DataFrame: Predicted DataFrames."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
