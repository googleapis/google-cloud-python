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

    # GeoSeries.area overrides Series.area with something totally different.
    # Ignore this type error, as we are trying to be as close to geopandas as
    # we can.
    @property
    def area(self, crs=None) -> bigframes.series.Series:  # type: ignore
        """[Not Implemented] Use ``bigframes.bigquery.st_area(series)``,
        instead to return the area in square meters.

        In GeoPandas, this returns a Series containing the area of each geometry
        in the GeoSeries expressed in the units of the CRS.

        Args:
            crs (optional):
                Coordinate Reference System of the geometry objects. Can be
                anything accepted by pyproj.CRS.from_user_input(), such as an
                authority string (eg “EPSG:4326”) or a WKT string.

        Returns:
            bigframes.pandas.Series:
                Series of float representing the areas.

        Raises:
            NotImplementedError:
                GeoSeries.area is not supported. Use bigframes.bigquery.st_area(series), instead.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def x(self) -> bigframes.series.Series:
        """Return the x location of point geometries in a GeoSeries

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import geopandas.array
            >>> import shapely.geometry
            >>> bpd.options.display.progress_bar = None

            >>> series = bpd.Series(
            ...     [shapely.geometry.Point(1, 2), shapely.geometry.Point(2, 3), shapely.geometry.Point(3, 4)],
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
            >>> import shapely.geometry
            >>> bpd.options.display.progress_bar = None

            >>> series = bpd.Series(
            ...     [shapely.geometry.Point(1, 2), shapely.geometry.Point(2, 3), shapely.geometry.Point(3, 4)],
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

    @property
    def boundary(self) -> bigframes.geopandas.GeoSeries:
        """
        Returns a GeoSeries of lower dimensional objects representing each
        geometry's set-theoretic boundary.

        **Examples:**

            >>> import bigframes.pandas as bpd
            >>> import geopandas.array
            >>> import shapely.geometry
            >>> bpd.options.display.progress_bar = None

            >>> from shapely.geometry import Polygon, LineString, Point
            >>> s = geopandas.GeoSeries(
            ...     [
            ...         Polygon([(0, 0), (1, 1), (0, 1)]),
            ...         LineString([(0, 0), (1, 1), (1, 0)]),
            ...         Point(0, 0),
            ...     ]
            ... )
            >>> s
            0    POLYGON ((0 0, 1 1, 0 1, 0 0))
            1        LINESTRING (0 0, 1 1, 1 0)
            2                       POINT (0 0)
            dtype: geometry

            >>> s.boundary
            0    LINESTRING (0 0, 1 1, 0 1, 0 0)
            1          MULTIPOINT ((0 0), (1 0))
            2           GEOMETRYCOLLECTION EMPTY
            dtype: geometry

        Returns:
            bigframes.geopandas.GeoSeries:
                A GeoSeries of lower dimensional objects representing each
                geometry's set-theoretic boundary
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
                inputs are Series with an equal index, that index is used.

            **kwargs:
                Additional arguments passed to the Series constructor, e.g. `name`.

        Returns:
            bigframes.geopandas.GeoSeries:
                A GeoSeries of Point geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @classmethod
    def from_wkt(cls, data, index=None) -> bigframes.geopandas.GeoSeries:
        """
        Alternate constructor to create a GeoSeries from a list or array of
        WKT objects.

        **Examples:**

            >>> import bigframes as bpd
            >>> import bigframes.geopandas
            >>> bpd.options.display.progress_bar = None

            >>> wkts = [
            ... 'POINT (1 1)',
            ... 'POINT (2 2)',
            ... 'POINT (3 3)',
            ... ]
            >>> s = bigframes.geopandas.GeoSeries.from_wkt(wkts)
            >>> s
            0    POINT (1 1)
            1    POINT (2 2)
            2    POINT (3 3)
            dtype: geometry

        Args:
            data (array-like):
                Series, list, or array of WKT objects.

            index (array-like or Index, optional):
                The index for the GeoSeries.

        Returns:
            bigframes.geopandas.GeoSeries:
                A GeoSeries of geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def to_wkt(self) -> bigframes.series.Series:
        """
        Convert GeoSeries geometries to WKT

        **Examples:**

            >>> import bigframes as bpd
            >>> import bigframes.geopandas
            >>> from shapely.geometry import Point
            >>> bpd.options.display.progress_bar = None

            >>> s = bigframes.geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
            >>> s
            0    POINT (1 1)
            1    POINT (2 2)
            2    POINT (3 3)
            dtype: geometry

            >>> s.to_wkt()
            0    POINT(1 1)
            1    POINT(2 2)
            2    POINT(3 3)
            dtype: string

        Returns:
            bigframes.series.Series:
                WKT representations of the geometries.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def difference(self: GeoSeries, other: GeoSeries) -> GeoSeries:  # type: ignore
        """
        Returns a GeoSeries of the points in each aligned geometry that are not
        in other.

        The operation works on a 1-to-1 row-wise manner.

        **Examples:**

            >>> import bigframes as bpd
            >>> import bigframes.geopandas
            >>> from shapely.geometry import Polygon, LineString, Point
            >>> bpd.options.display.progress_bar = None

        We can check two GeoSeries against each other, row by row:

            >>> s1 = bigframes.geopandas.GeoSeries(
            ...    [
            ...        Polygon([(0, 0), (2, 2), (0, 2)]),
            ...        Polygon([(0, 0), (2, 2), (0, 2)]),
            ...        LineString([(0, 0), (2, 2)]),
            ...        LineString([(2, 0), (0, 2)]),
            ...        Point(0, 1),
            ...    ],
            ... )
            >>> s2 = bigframes.geopandas.GeoSeries(
            ...    [
            ...        Polygon([(0, 0), (1, 1), (0, 1)]),
            ...        LineString([(1, 0), (1, 3)]),
            ...        LineString([(2, 0), (0, 2)]),
            ...        Point(1, 1),
            ...        Point(0, 1),
            ...    ],
            ...    index=range(1, 6),
            ... )

            >>> s1
            0    POLYGON ((0 0, 2 2, 0 2, 0 0))
            1    POLYGON ((0 0, 2 2, 0 2, 0 0))
            2             LINESTRING (0 0, 2 2)
            3             LINESTRING (2 0, 0 2)
            4                       POINT (0 1)
            dtype: geometry

            >>> s2
            1    POLYGON ((0 0, 1 1, 0 1, 0 0))
            2             LINESTRING (1 0, 1 3)
            3             LINESTRING (2 0, 0 2)
            4                       POINT (1 1)
            5                       POINT (0 1)
            dtype: geometry

            >>> s1.difference(s2)
            0                                               None
            1    POLYGON ((0.99954 1, 2 2, 0 2, 0 1, 0.99954 1))
            2                   LINESTRING (0 0, 1 1.00046, 2 2)
            3                           GEOMETRYCOLLECTION EMPTY
            4                                        POINT (0 1)
            5                                               None
            dtype: geometry

        We can also check difference of single shapely geometries:

            >>> polygon_s1 = bigframes.geopandas.GeoSeries(
            ...     [
            ...         Polygon([(0, 0), (10, 0), (10, 10), (0, 0)])
            ...     ]
            ... )
            >>> polygon_s2 = bigframes.geopandas.GeoSeries(
            ...     [
            ...         Polygon([(4, 2), (6, 2), (8, 6), (4, 2)])
            ...     ]
            ... )

            >>> polygon_s1
            0    POLYGON ((0 0, 10 0, 10 10, 0 0))
            dtype: geometry

            >>> polygon_s2
            0    POLYGON ((4 2, 6 2, 8 6, 4 2))
            dtype: geometry

            >>> polygon_s1.difference(polygon_s2)
            0    POLYGON ((0 0, 10 0, 10 10, 0 0), (8 6, 6 2, 4...
            dtype: geometry

        Additionally, we can check difference of a GeoSeries against a single shapely geometry:

            >>> s1.difference(polygon_s2)
            0    POLYGON ((0 0, 2 2, 0 2, 0 0))
            1                              None
            2                              None
            3                              None
            4                              None
            dtype: geometry

        Args:
            other (bigframes.geopandas.GeoSeries or geometric object):
                The GeoSeries (elementwise) or geometric object to find the
                difference to.

        Returns:
            bigframes.geopandas.GeoSeries:
                A GeoSeries of the points in each aligned geometry that are not
                in other.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def distance(self: GeoSeries, other: GeoSeries) -> bigframes.series.Series:
        """
        [Not Implemented] Use ``bigframes.bigquery.st_distance(series, other)``
        instead to return the shorted distance between two
        ``GEOGRAPHY`` objects in meters.

        In GeoPandas, this returns a Series of the distances between each
        aligned geometry in the expressed in the units of the CRS.

        Args:
            other:
                The Geoseries (elementwise) or geometric object to find the distance to.

        Returns:
            bigframes.pandas.Series:
                Series of float representing the distances.

        Raises:
            NotImplementedError:
                GeoSeries.distance is not supported. Use
                ``bigframes.bigquery.st_distance(series, other)``, instead.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    def intersection(self: GeoSeries, other: GeoSeries) -> GeoSeries:  # type: ignore
        """
        Returns a GeoSeries of the intersection of points in each aligned
        geometry with other.

        The operation works on a 1-to-1 row-wise manner.

        **Examples:**

            >>> import bigframes as bpd
            >>> import bigframes.geopandas
            >>> from shapely.geometry import Polygon, LineString, Point
            >>> bpd.options.display.progress_bar = None

        We can check two GeoSeries against each other, row by row.

            >>> s1 = bigframes.geopandas.GeoSeries(
            ...    [
            ...        Polygon([(0, 0), (2, 2), (0, 2)]),
            ...        Polygon([(0, 0), (2, 2), (0, 2)]),
            ...        LineString([(0, 0), (2, 2)]),
            ...        LineString([(2, 0), (0, 2)]),
            ...        Point(0, 1),
            ...    ],
            ... )
            >>> s2 = bigframes.geopandas.GeoSeries(
            ...    [
            ...        Polygon([(0, 0), (1, 1), (0, 1)]),
            ...        LineString([(1, 0), (1, 3)]),
            ...        LineString([(2, 0), (0, 2)]),
            ...        Point(1, 1),
            ...        Point(0, 1),
            ...    ],
            ...    index=range(1, 6),
            ... )

            >>> s1
            0    POLYGON ((0 0, 2 2, 0 2, 0 0))
            1    POLYGON ((0 0, 2 2, 0 2, 0 0))
            2             LINESTRING (0 0, 2 2)
            3             LINESTRING (2 0, 0 2)
            4                       POINT (0 1)
            dtype: geometry

            >>> s2
            1    POLYGON ((0 0, 1 1, 0 1, 0 0))
            2             LINESTRING (1 0, 1 3)
            3             LINESTRING (2 0, 0 2)
            4                       POINT (1 1)
            5                       POINT (0 1)
            dtype: geometry

            >>> s1.intersection(s2)
            0                                    None
            1    POLYGON ((0 0, 0.99954 1, 0 1, 0 0))
            2                       POINT (1 1.00046)
            3                   LINESTRING (2 0, 0 2)
            4                GEOMETRYCOLLECTION EMPTY
            5                                    None
            dtype: geometry


        We can also do intersection of each geometry and a single shapely geometry:

            >>> s1.intersection(bigframes.geopandas.GeoSeries([Polygon([(0, 0), (1, 1), (0, 1)])]))
            0    POLYGON ((0 0, 0.99954 1, 0 1, 0 0))
            1                                    None
            2                                    None
            3                                    None
            4                                    None
            dtype: geometry


        Args:
            other (GeoSeries or geometric object):
                The Geoseries (elementwise) or geometric object to find the
                intersection with.

        Returns:
            bigframes.geopandas.GeoSeries:
                The Geoseries (elementwise) of the intersection of points in
                each aligned geometry with other.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)

    @property
    def is_closed(self: GeoSeries) -> bigframes.series.Series:
        """
        [Not Implemented] Use ``bigframes.bigquery.st_isclosed(series)``
        instead to return a boolean indicating if a shape is closed.

        In GeoPandas, this returns a Series of booleans with value True if a
        LineString's or LinearRing's first and last points are equal.

        Returns False for any other geometry type.

        Returns:
            bigframes.pandas.Series:
                Series of booleans.

        Raises:
            NotImplementedError:
                GeoSeries.is_closed is not supported. Use
                ``bigframes.bigquery.st_isclosed(series)``, instead.
        """
        raise NotImplementedError(constants.ABSTRACT_METHOD_ERROR_MESSAGE)
