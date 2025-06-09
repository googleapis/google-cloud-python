# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import Union

import shapely  # type: ignore

from bigframes import operations as ops
import bigframes.geopandas
import bigframes.series

"""
Search functions defined from
https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions
"""


def st_area(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
) -> bigframes.series.Series:
    """
    Returns the area in square meters covered by the polygons in the input
    `GEOGRAPHY`.

    If geography_expression is a point or a line, returns zero. If
    geography_expression is a collection, returns the area of the polygons
    in the collection; if the collection doesn't contain polygons, returns zero.


    .. note::
        BigQuery's Geography functions, like `st_area`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data


    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> from shapely.geometry import Polygon, LineString, Point
        >>> bpd.options.display.progress_bar = None

        >>> series = bigframes.geopandas.GeoSeries(
        ...         [
        ...             Polygon([(0.0, 0.0), (0.1, 0.1), (0.0, 0.1)]),
        ...             Polygon([(0.10, 0.4), (0.9, 0.5), (0.10, 0.5)]),
        ...             Polygon([(0.1, 0.1), (0.2, 0.1), (0.2, 0.2)]),
        ...             LineString([(0, 0), (1, 1), (0, 1)]),
        ...             Point(0, 1),
        ...         ]
        ... )
        >>> series
        0              POLYGON ((0 0, 0.1 0.1, 0 0.1, 0 0))
        1    POLYGON ((0.1 0.4, 0.9 0.5, 0.1 0.5, 0.1 0.4))
        2    POLYGON ((0.1 0.1, 0.2 0.1, 0.2 0.2, 0.1 0.1))
        3                        LINESTRING (0 0, 1 1, 0 1)
        4                                       POINT (0 1)
        dtype: geometry

        >>> bbq.st_area(series)
        0    61821689.855985
        1    494563347.88721
        2    61821689.855841
        3                0.0
        4                0.0
        dtype: Float64

    Use `round()` to round the outputed areas to the neares ten millions

        >>> bbq.st_area(series).round(-7)
        0     60000000.0
        1    490000000.0
        2     60000000.0
        3            0.0
        4            0.0
        dtype: Float64

    Args:
        series (bigframes.pandas.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.

    Returns:
      bigframes.pandas.Series:
          Series of float representing the areas.
    """
    series = series._apply_unary_op(ops.geo_area_op)
    series.name = None
    return series


def st_difference(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
    other: Union[
        bigframes.series.Series,
        bigframes.geopandas.GeoSeries,
        shapely.geometry.base.BaseGeometry,
    ],
) -> bigframes.series.Series:
    """
    Returns a `GEOGRAPHY` that represents the point set difference of
    `geography_1` and `geography_2`. Therefore, the result consists of the part
    of `geography_1` that doesn't intersect with `geography_2`.

    If `geometry_1` is completely contained in `geometry_2`, then `ST_DIFFERENCE`
    returns an empty `GEOGRAPHY`.

    .. note::
        BigQuery's Geography functions, like `st_difference`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data

    **Examples:**

        >>> import bigframes as bpd
        >>> import bigframes.bigquery as bbq
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

        >>> bbq.st_difference(s1, s2)
        0                                               None
        1    POLYGON ((0.99954 1, 2 2, 0 2, 0 1, 0.99954 1))
        2                   LINESTRING (0 0, 1 1.00046, 2 2)
        3                           GEOMETRYCOLLECTION EMPTY
        4                                        POINT (0 1)
        5                                               None
        dtype: geometry

    Additionally, we can check difference of a GeoSeries against a single shapely geometry:

        >>> polygon = Polygon([(0, 0), (10, 0), (10, 10), (0, 0)])
        >>> bbq.st_difference(s1, polygon)
        0    POLYGON ((1.97082 2.00002, 0 2, 0 0, 1.97082 2...
        1    POLYGON ((1.97082 2.00002, 0 2, 0 0, 1.97082 2...
        2                             GEOMETRYCOLLECTION EMPTY
        3                    LINESTRING (0.99265 1.00781, 0 2)
        4                                          POINT (0 1)
        dtype: geometry

    Args:
        series (bigframes.pandas.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.
        other (bigframes.pandas.Series | bigframes.geopandas.GeoSeries | shapely.Geometry):
            The series or geometric object to subtract from the geography
            objects in ``series``.

    Returns:
        bigframes.series.Series:
            A GeoSeries of the points in each aligned geometry that are not
            in other.
    """
    return series._apply_binary_op(other, ops.geo_st_difference_op)


def st_distance(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
    other: Union[
        bigframes.series.Series,
        bigframes.geopandas.GeoSeries,
        shapely.geometry.base.BaseGeometry,
    ],
    *,
    use_spheroid: bool = False,
) -> bigframes.series.Series:
    """
    Returns the shortest distance in meters between two non-empty
    ``GEOGRAPHY`` objects.

    **Examples:**

        >>> import bigframes as bpd
        >>> import bigframes.bigquery as bbq
        >>> import bigframes.geopandas
        >>> from shapely.geometry import Polygon, LineString, Point
        >>> bpd.options.display.progress_bar = None

    We can check two GeoSeries against each other, row by row.

        >>> s1 = bigframes.geopandas.GeoSeries(
        ...    [
        ...        Point(0, 0),
        ...        Point(0.00001, 0),
        ...        Point(0.00002, 0),
        ...    ],
        ... )
        >>> s2 = bigframes.geopandas.GeoSeries(
        ...    [
        ...        Point(0.00001, 0),
        ...        Point(0.00003, 0),
        ...        Point(0.00005, 0),
        ...    ],
        ... )

        >>> bbq.st_distance(s1, s2, use_spheroid=True)
        0    1.113195
        1     2.22639
        2    3.339585
        dtype: Float64

    We can also calculate the distance of each geometry and a single shapely geometry:

        >>> bbq.st_distance(s2, Point(0.00001, 0))
        0         0.0
        1    2.223902
        2    4.447804
        dtype: Float64

    Args:
        series (bigframes.pandas.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.
        other (bigframes.pandas.Series | bigframes.geopandas.GeoSeries | shapely.Geometry):
            The series or geometric object to calculate the distance in meters
            to form the geography objects in ``series``.
        use_spheroid (optional, default ``False``):
            Determines how this function measures distance. If ``use_spheroid``
            is False, the function measures distance on the surface of a perfect
            sphere. If ``use_spheroid`` is True, the function measures distance
            on the surface of the `WGS84 spheroid
            <https://cloud.google.com/bigquery/docs/geospatial-data>`_. The
            default value of ``use_spheroid`` is False.

    Returns:
        bigframes.pandas.Series:
            The Series (elementwise) of the smallest distance between
            each aligned geometry with other.
    """
    return series._apply_binary_op(
        other, ops.GeoStDistanceOp(use_spheroid=use_spheroid)
    )


def st_intersection(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
    other: Union[
        bigframes.series.Series,
        bigframes.geopandas.GeoSeries,
        shapely.geometry.base.BaseGeometry,
    ],
) -> bigframes.series.Series:
    """
    Returns a `GEOGRAPHY` that represents the point set intersection of the two
    input `GEOGRAPHYs`. Thus, every point in the intersection appears in both
    `geography_1` and `geography_2`.

    .. note::
        BigQuery's Geography functions, like `st_intersection`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data

    **Examples:**

        >>> import bigframes as bpd
        >>> import bigframes.bigquery as bbq
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

        >>> bbq.st_intersection(s1, s2)
        0                                    None
        1    POLYGON ((0 0, 0.99954 1, 0 1, 0 0))
        2                       POINT (1 1.00046)
        3                   LINESTRING (2 0, 0 2)
        4                GEOMETRYCOLLECTION EMPTY
        5                                    None
        dtype: geometry

    We can also do intersection of each geometry and a single shapely geometry:

        >>> bbq.st_intersection(s1, Polygon([(0, 0), (1, 1), (0, 1)]))
        0    POLYGON ((0 0, 0.99954 1, 0 1, 0 0))
        1    POLYGON ((0 0, 0.99954 1, 0 1, 0 0))
        2             LINESTRING (0 0, 0.99954 1)
        3                GEOMETRYCOLLECTION EMPTY
        4                             POINT (0 1)
        dtype: geometry

    Args:
        series (bigframes.pandas.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.
        other (bigframes.pandas.Series | bigframes.geopandas.GeoSeries | shapely.Geometry):
            The series or geometric object to intersect with the geography
            objects in ``series``.

    Returns:
        bigframes.geopandas.GeoSeries:
            The Geoseries (elementwise) of the intersection of points in
            each aligned geometry with other.
    """
    return series._apply_binary_op(other, ops.geo_st_intersection_op)


def st_isclosed(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
) -> bigframes.series.Series:
    """
    Returns TRUE for a non-empty Geography, where each element in the
    Geography has an empty boundary.

    .. note::
        BigQuery's Geography functions, like `st_isclosed`, interpret the geometry
        data type as a point set on the Earth's surface. A point set is a set
        of points, lines, and polygons on the WGS84 reference spheroid, with
        geodesic edges. See: https://cloud.google.com/bigquery/docs/geospatial-data

    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq

        >>> from shapely.geometry import Point, LineString, Polygon
        >>> bpd.options.display.progress_bar = None

        >>> series = bigframes.geopandas.GeoSeries(
        ...     [
        ...         Point(0, 0),  # Point
        ...         LineString([(0, 0), (1, 1)]),  # Open LineString
        ...         LineString([(0, 0), (1, 1), (0, 1), (0, 0)]),  # Closed LineString
        ...         Polygon([(0, 0), (1, 1), (0, 1), (0, 0)]),
        ...         None,
        ...     ]
        ... )
        >>> series
        0                                       POINT (0 0)
        1                            LINESTRING (0 0, 1 1)
        2             LINESTRING (0 0, 1 1, 0 1, 0 0)
        3             POLYGON ((0 0, 1 1, 0 1, 0 0))
        4                                           None
        dtype: geometry

        >>> bbq.st_isclosed(series)
        0     True
        1    False
        2     True
        3     False
        4     <NA>
        dtype: boolean

    Args:
        series (bigframes.pandas.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.

    Returns:
        bigframes.pandas.Series:
            Series of booleans indicating whether each geometry is closed.
    """
    series = series._apply_unary_op(ops.geo_st_isclosed_op)
    series.name = None
    return series


def st_length(
    series: Union[bigframes.series.Series, bigframes.geopandas.GeoSeries],
    *,
    use_spheroid: bool = False,
) -> bigframes.series.Series:
    """Returns the total length in meters of the lines in the input GEOGRAPHY.

    If a series element is a point or a polygon, returns zero for that row.
    If a series element is a collection, returns the length of the lines
    in the collection; if the collection doesn't contain lines, returns
    zero.

    The optional use_spheroid parameter determines how this function
    measures distance. If use_spheroid is FALSE, the function measures
    distance on the surface of a perfect sphere.

    The use_spheroid parameter currently only supports the value FALSE.  The
    default value of use_spheroid is FALSE. See:
    https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_length

    **Examples:**

        >>> import bigframes.geopandas
        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq

        >>> from shapely.geometry import Polygon, LineString, Point, GeometryCollection
        >>> bpd.options.display.progress_bar = None

        >>> series = bigframes.geopandas.GeoSeries(
        ...         [
        ...             LineString([(0, 0), (1, 0)]),  # Length will be approx 1 degree in meters
        ...             Polygon([(0.0, 0.0), (0.1, 0.1), (0.0, 0.1)]), # Length is 0
        ...             Point(0, 1),  # Length is 0
        ...             GeometryCollection([LineString([(0,0),(0,1)]), Point(1,1)]) # Length of LineString only
        ...         ]
        ... )

        >>> result = bbq.st_length(series)
        >>> result
        0    111195.101177
        1              0.0
        2              0.0
        3    111195.101177
        dtype: Float64

    Args:
        series (bigframes.series.Series | bigframes.geopandas.GeoSeries):
            A series containing geography objects.
        use_spheroid (bool, optional):
            Determines how this function measures distance.
            If FALSE (default), measures distance on a perfect sphere.
            Currently, only FALSE is supported.

    Returns:
        bigframes.series.Series:
            Series of floats representing the lengths in meters.
    """
    series = series._apply_unary_op(ops.GeoStLengthOp(use_spheroid=use_spheroid))
    series.name = None
    return series
