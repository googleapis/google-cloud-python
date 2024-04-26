# Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#          Mathieu Blondel <mathieu@mblondel.org>
#          Robert Layton <robertlayton@gmail.com>
#          Andreas Mueller <amueller@ais.uni-bonn.de>
#          Philippe Gervais <philippe.gervais@inria.fr>
#          Lars Buitinck
#          Joel Nothman <joel.nothman@gmail.com>
# License: BSD 3 clause

from bigframes import constants
import bigframes.pandas as bpd


def paired_cosine_distances(X, Y) -> bpd.DataFrame:
    """Compute the paired cosine distances between X and Y.

    Args:
        X (Series or single column DataFrame of array of numeric type):
            Input data.
        Y (Series or single column DataFrame of array of numeric type):
            Input data. X and Y are mapped by indexes, must have the same index.

    Returns:
        bigframes.dataframe.DataFrame: DataFrame with columns of X, Y and cosine_distance.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def paired_manhattan_distance(X, Y) -> bpd.DataFrame:
    """Compute the L1 distances between the vectors in X and Y.

    Args:
        X (Series or single column DataFrame of array of numeric type):
            Input data.
        Y (Series or single column DataFrame of array of numeric type):
            Input data. X and Y are mapped by indexes, must have the same index.

    Returns:
        bigframes.dataframe.DataFrame: DataFrame with columns of X, Y and manhattan_distance.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)


def paired_euclidean_distances(X, Y) -> bpd.DataFrame:
    """Compute the paired euclidean distances between X and Y.

    Args:
        X (Series or single column DataFrame of array of numeric type):
            Input data.
        Y (Series or single column DataFrame of array of numeric type):
            Input data. X and Y are mapped by indexes, must have the same index.

    Returns:
        bigframes.dataframe.DataFrame: DataFrame with columns of X, Y and euclidean_distance.
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
