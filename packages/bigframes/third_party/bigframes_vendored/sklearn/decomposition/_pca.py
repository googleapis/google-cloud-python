""" Principal Component Analysis.
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

from bigframes import constants
from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class PCA(BaseEstimator, metaclass=ABCMeta):
    """Principal component analysis (PCA).

    Linear dimensionality reduction using Singular Value Decomposition of the
    data to project it to a lower dimensional space. The input data is centered
    but not scaled for each feature before applying the SVD.

    It uses the LAPACK implementation of the full SVD or a randomized truncated
    SVD by the method of Halko et al. 2009, depending on the shape of the input
    data and the number of components to extract.

    It can also use the scipy.sparse.linalg ARPACK implementation of the
    truncated SVD.

    Args:
         n_components (Optional[int], default 3):
            Number of components to keep. if n_components is not set all components
            are kept.

    """

    def fit(self, X, y=None):
        """Fit the model according to the given training data.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or DataFrame of shape (n_samples, n_features). Training vector,
                where `n_samples` is the number of samples and `n_features` is
                the number of features.

            y (default None):
                Ignored.

        Returns:
            PCA: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def score(self, X=None, y=None):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUTE function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate#pca_models
            for the outputs relevant to this model type.

        Args:
            X (default None):
                Ignored.

            y (default None):
                Ignored.
        Returns:
            bigframes.dataframe.DataFrame: DataFrame that represents model metrics.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def predict(self, X):
        """Predict the closest cluster for each sample in X.

        Args:
            X (bigframes.dataframe.DataFrame or bigframes.series.Series):
                Series or a DataFrame to predict.

        Returns:
            bigframes.dataframe.DataFrame: predicted DataFrames."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def components_(self):
        """Principal axes in feature space, representing the directions of maximum variance in the data.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of principal components, containing following columns:
                principal_component_id: An integer that identifies the principal component.

                feature: The column name that contains the feature.

                numerical_value: If feature is numeric, the value of feature for the principal component that principal_component_id identifies. If feature isn't numeric, the value is NULL.

                categorical_value: An list of mappings containing information about categorical features. Each mapping contains the following fields:
                    categorical_value.category: The name of each category.

                    categorical_value.value: The value of categorical_value.category for the centroid that centroid_id identifies.

            The output contains one row per feature per component.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def explained_variance_(self):
        """The amount of variance explained by each of the selected components.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame containing following columns:
                principal_component_id: An integer that identifies the principal component.

                explained_variance: The factor by which the eigenvector is scaled. Eigenvalue and explained variance are the same concepts in PCA.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def explained_variance_ratio_(self):
        """Percentage of variance explained by each of the selected components.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame containing following columns:
                principal_component_id: An integer that identifies the principal component.

                explained_variance_ratio: the total variance is the sum of variances, also known as eigenvalues, of all
                of the individual principal components. The explained variance ratio by a principal component is
                the ratio between the variance, also known as eigenvalue, of that principal component and the total variance.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
