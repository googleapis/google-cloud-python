# Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#          Mathieu Blondel <mathieu@mblondel.org>
#          Olivier Grisel <olivier.grisel@ensta.org>
#          Andreas Mueller <amueller@ais.uni-bonn.de>
#          Joel Nothman <joel.nothman@gmail.com>
#          Hamzeh Alsalhi <ha258@cornell.edu>
# License: BSD 3 clause

from bigframes import constants
from third_party.bigframes_vendored.sklearn.base import BaseEstimator


class LabelEncoder(BaseEstimator):
    """Encode target labels with value between 0 and n_classes-1.

    This transformer should be used to encode target values, *i.e.* `y`, and
    not the input `X`.

    Args:
        min_frequency (Optional[int], default None):
            Specifies the minimum frequency below which a category will be considered infrequent.
            Default None.
            int: categories with a smaller cardinality will be considered infrequent as ßindex 0.
        max_categories (Optional[int], default None):
            Specifies an upper limit to the number of output features for each input feature
            when considering infrequent categories. If there are infrequent categories,
            max_categories includes the category representing the infrequent categories along with the frequent categories.
            Default None, set limit to 1,000,000.
    """

    def fit(self, y):
        """Fit label encoder.

        Args:
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The DataFrame or Series with training data.

        Returns:
            LabelEncoder: Fitted encoder.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def transform(self, y):
        """Transform y using label encoding.

        Args:
            y (bigframes.dataframe.DataFrame or bigframes.series.Series):
                The DataFrame or Series to be transformed.

        Returns:
            bigframes.dataframe.DataFrame: The result is an array-like of values."""
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
