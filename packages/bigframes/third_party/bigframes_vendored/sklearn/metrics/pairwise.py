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


def cosine_similarity(X, Y) -> bpd.DataFrame:
    """Compute cosine similarity between samples in X and Y.

    Cosine similarity, or the cosine kernel, computes similarity as the
    normalized dot product of X and Y:

        K(X, Y) = <X, Y> / (||X||*||Y||)

    Args:
        X (Series or single column DataFrame of array of numeric type):
            Input data.
        Y (Series or single column DataFrame of array of numeric type):
            Input data. X and Y are mapped by indexes, must have the same index.

    Returns:
        bigframes.dataframe.DataFrame: DataFrame with columns of X, Y and cosine_similarity
    """
    raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
