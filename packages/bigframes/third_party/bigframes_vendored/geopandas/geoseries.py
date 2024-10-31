# contains code from https://github.com/geopandas/geopandas/blob/main/geopandas/geoseries.py
from __future__ import annotations


class GeoSeries:
    """
    A Series object designed to store geometry objects.

    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> bpd.options.display.progress_bar = None
        >>> from shapely.geometry import Point
        >>> s = bigframes.geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
        >>> s
        0    POINT (1 1)
        1    POINT (2 2)
        2    POINT (3 3)
        dtype: geometry

    Args:
        data (array-like, dict, scalar value, bigframes.pandas.Series):
            The geometries to store in the GeoSeries.
        index (array-like, pandas.Index, bigframes.pandas.Index):
            The index for the GeoSeries.
        kwargs (dict):
            Additional arguments passed to the Series constructor,
            e.g. ``name``.
    """
