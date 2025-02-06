# contains code from https://github.com/geopandas/geopandas/blob/main/geopandas/geoseries.py
from __future__ import annotations

from typing import TYPE_CHECKING

from bigframes import constants

if TYPE_CHECKING:
    import bigframes.series


class GeoSeries:
    """
    A Series object designed to store geometry objects.

    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> from shapely.geometry import Point
        >>> bpd.options.display.progress_bar = None

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

    @property
    def x(self) -> bigframes.series.Series:
        """Return the x location of point geometries in a GeoSeries

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import geopandas.array
            >>> import shapely
            >>> bpd.options.display.progress_bar = None

            >>> series = bpd.Series(
            ...     [shapely.Point(1, 2), shapely.Point(2, 3), shapely.Point(3, 4)],
            ...     dtype=geopandas.array.GeometryDtype()
            ... )
            >>> series.geo.x
            0    1.0
            1    2.0
            2    3.0
            dtype: Float64

        Returns:
            bigframes.pandas.Series:
                Return the x location (longitude) of point geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def y(self) -> bigframes.series.Series:
        """Return the y location of point geometries in a GeoSeries

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import geopandas.array
            >>> import shapely
            >>> bpd.options.display.progress_bar = None

            >>> series = bpd.Series(
            ...     [shapely.Point(1, 2), shapely.Point(2, 3), shapely.Point(3, 4)],
            ...     dtype=geopandas.array.GeometryDtype()
            ... )
            >>> series.geo.y
            0    2.0
            1    3.0
            2    4.0
            dtype: Float64

        Returns:
            bigframes.pandas.Series:
                Return the y location (latitude) of point geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @classmethod
    def from_xy(cls, x, y, index=None, **kwargs) -> bigframes.geopandas.GeoSeries:
        """
        Alternate constructor to create a GeoSeries of Point geometries from
        lists or arrays of x, y coordinates.

        In case of geographic coordinates, it is assumed that longitude is
        captured by x coordinates and latitude by y.

          **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import bigframes.geopandas
            >>> bpd.options.display.progress_bar = None

            >>> x = [2.5, 5, -3.0]
            >>> y = [0.5, 1, 1.5]

            >>> s = bigframes.geopandas.GeoSeries.from_xy(x, y)
            >>> s
            0    POINT (2.5 0.5)
            1        POINT (5 1)
            2     POINT (-3 1.5)
            dtype: geometry

        Args:
            x, y (array-like):
                longitude is x coordinates and latitude y coordinates.

            index (array-like or Index, optional):
                The index for the GeoSeries. If not given and all coordinate
                inputs are Series with an equal index, that index is used..

            **kwargs:
                Additional arguments passed to the Series constructor, e.g. `name`.

        Returns:
            bigframes.geopandas.GeoSeries:
                A GeoSeries of Point geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
