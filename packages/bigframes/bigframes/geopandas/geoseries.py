# Copyright 2024 Google LLC
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

import bigframes_vendored.constants as constants
import bigframes_vendored.geopandas.geoseries as vendored_geoseries
import geopandas.array  # type: ignore

import bigframes.geopandas
import bigframes.operations as ops
import bigframes.series


class GeoSeries(vendored_geoseries.GeoSeries, bigframes.series.Series):
    __doc__ = vendored_geoseries.GeoSeries.__doc__

    def __init__(self, data=None, index=None, **kwargs):
        super().__init__(
            data=data, index=index, dtype=geopandas.array.GeometryDtype(), **kwargs
        )

    @property
    def length(self):
        raise NotImplementedError(
            "GeoSeries.length is not yet implemented. Please use bigframes.bigquery.st_length(geoseries) instead."
        )

    @property
    def x(self) -> bigframes.series.Series:
        series = self._apply_unary_op(ops.geo_x_op)
        series.name = None
        return series

    @property
    def y(self) -> bigframes.series.Series:
        series = self._apply_unary_op(ops.geo_y_op)
        series.name = None
        return series

    # GeoSeries.area overrides Series.area with something totally different.
    # Ignore this type error, as we are trying to be as close to geopandas as
    # we can.
    @property
    def area(self, crs=None) -> bigframes.series.Series:  # type: ignore
        raise NotImplementedError(
            f"GeoSeries.area is not supported. Use bigframes.bigquery.st_area(series), instead. {constants.FEEDBACK_LINK}"
        )

    @property
    def boundary(self) -> bigframes.series.Series:  # type: ignore
        series = self._apply_unary_op(ops.geo_st_boundary_op)
        series.name = None
        return series

    @property
    def is_closed(self) -> bigframes.series.Series:
        # TODO(tswast): GeoPandas doesn't treat Point as closed. Use ST_LENGTH
        # when available to filter out "closed" shapes that return false in
        # GeoPandas.
        raise NotImplementedError(
            f"GeoSeries.is_closed is not supported. Use bigframes.bigquery.st_isclosed(series), instead. {constants.FEEDBACK_LINK}"
        )

    @classmethod
    def from_wkt(cls, data, index=None) -> GeoSeries:
        series = bigframes.series.Series(data, index=index)

        return cls(series._apply_unary_op(ops.geo_st_geogfromtext_op))

    @classmethod
    def from_xy(cls, x, y, index=None, session=None, **kwargs) -> GeoSeries:
        # TODO: if either x or y is local and the other is remote. Use the
        # session from the remote object.
        series_x = bigframes.series.Series(x, index=index, session=session, **kwargs)
        series_y = bigframes.series.Series(y, index=index, session=session, **kwargs)

        return cls(series_x._apply_binary_op(series_y, ops.geo_st_geogpoint_op))

    def to_wkt(self: GeoSeries) -> bigframes.series.Series:
        series = self._apply_unary_op(ops.geo_st_astext_op)
        series.name = None
        return series

    def difference(self: GeoSeries, other: GeoSeries) -> bigframes.series.Series:  # type: ignore
        return self._apply_binary_op(other, ops.geo_st_difference_op)

    def distance(self: GeoSeries, other: GeoSeries) -> bigframes.series.Series:  # type: ignore
        raise NotImplementedError(
            f"GeoSeries.distance is not supported. Use bigframes.bigquery.st_distance(series, other), instead. {constants.FEEDBACK_LINK}"
        )

    def intersection(self: GeoSeries, other: GeoSeries) -> bigframes.series.Series:  # type: ignore
        return self._apply_binary_op(other, ops.geo_st_intersection_op)
