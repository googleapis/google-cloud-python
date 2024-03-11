from typing import Optional, Sequence

from bigframes import constants


class PlotAccessor:
    """
    Make plots of Series or DataFrame with the `matplotlib` backend.
    """

    def hist(self, by: Optional[Sequence[str]] = None, bins: int = 10, **kwargs):
        """
        Draw one histogram of the DataFrame’s columns.

        A histogram is a representation of the distribution of data.
        This function groups the values of all given Series in the DataFrame
        into bins and draws all bins in one :class:`matplotlib.axes.Axes`.
        This is useful when the DataFrame's Series are in a similar scale.

        Parameters
        ----------
        by : str or sequence, optional
            Column in the DataFrame to group by. It is not supported yet.
        bins : int, default 10
            Number of histogram bins to be used.
        **kwargs
            Additional keyword arguments are documented in
            :meth:`DataFrame.plot`.

        Returns
        -------
        class:`matplotlib.AxesSubplot`
            Return a histogram plot.

        Examples
        --------
        For Series:

        .. plot::
            :context: close-figs

            >>> import bigframes.pandas as bpd
            >>> import numpy as np
            >>> df = bpd.DataFrame(np.random.randint(1, 7, 6000), columns=['one'])
            >>> df['two'] = np.random.randint(1, 7, 6000) + np.random.randint(1, 7, 6000)
            >>> ax = df.plot.hist(bins=12, alpha=0.5)
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
