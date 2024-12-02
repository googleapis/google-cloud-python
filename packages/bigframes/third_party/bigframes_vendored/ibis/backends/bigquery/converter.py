# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/backends/bigquery/converter.py

from __future__ import annotations

from bigframes_vendored.ibis.formats.pandas import PandasData


class BigQueryPandasData(PandasData):
    @classmethod
    def convert_GeoSpatial(cls, s, dtype, pandas_type):
        import geopandas as gpd
        import shapely as shp

        return gpd.GeoSeries(shp.from_wkt(s))

    convert_Point = (
        convert_LineString
    ) = (
        convert_Polygon
    ) = (
        convert_MultiLineString
    ) = convert_MultiPoint = convert_MultiPolygon = convert_GeoSpatial
