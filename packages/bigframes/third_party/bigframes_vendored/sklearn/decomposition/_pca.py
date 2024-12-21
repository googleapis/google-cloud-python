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

from bigframes_vendored.sklearn.base import BaseEstimator

from bigframes import constants


class PCA(BaseEstimator, metaclass=ABCMeta):
    """Principal component analysis (PCA).

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> from bigframes.ml.decomposition import PCA
        >>> bpd.options.display.progress_bar = None
        >>> X = bpd.DataFrame({"feat0": [-1, -2, -3, 1, 2, 3], "feat1": [-1, -1, -2, 1, 1, 2]})
        >>> pca = PCA(n_components=2).fit(X)
        >>> pca.predict(X) # doctest:+SKIP
            principal_component_1  principal_component_2
        0              -0.755243               0.157628
        1               -1.05405              -0.141179
        2              -1.809292               0.016449
        3               0.755243              -0.157628
        4                1.05405               0.141179
        5               1.809292              -0.016449
        <BLANKLINE>
        [6 rows x 2 columns]
        >>> pca.explained_variance_ratio_ # doctest:+SKIP
            principal_component_id  explained_variance_ratio
        0                       1                   0.00901
        1                       0                   0.99099
        <BLANKLINE>
        [2 rows x 2 columns]

    Args:
        n_components (int, float or None, default None):
            Number of components to keep. If n_components is not set, all
            components are kept, n_components = min(n_samples, n_features).
            If 0 < n_components < 1, select the number of components such that the amount of variance that needs to be explained is greater than the percentage specified by n_components.
        svd_solver ("full", "randomized" or "auto", default "auto"):
            The solver to use to calculate the principal components. Details: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca#pca_solver.

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
            PCA: Fitted estimator.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def score(self, X=None, y=None):
        """Calculate evaluation metrics of the model.

        .. note::

            Output matches that of the BigQuery ML.EVALUATE function.
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
            X (bigframes.dataframe.DataFrame or bigframes.series.Series or pandas.core.frame.DataFrame or pandas.core.series.Series):
                Series or a DataFrame to predict.

        Returns:
            bigframes.dataframe.DataFrame: Predicted DataFrames."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def components_(self):
        """Principal axes in feature space, representing the directions of maximum variance in the data.

        Returns:
            bigframes.dataframe.DataFrame: DataFrame of principal components, containing following columns:
                principal_component_id: An integer that identifies the principal component.

                feature: The column name that contains the feature.

                numerical_value: If feature is numeric, the value of feature for the principal component that principal_component_id identifies. If feature isn't numeric, the value is NULL.

                categorical_value: A list of mappings containing information about categorical features. Each mapping contains the following fields:
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
