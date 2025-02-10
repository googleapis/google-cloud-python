# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/backends/sql/datatypes.py

from __future__ import annotations

from functools import partial
from typing import NoReturn

import bigframes_vendored.ibis.common.exceptions as com
import bigframes_vendored.ibis.expr.datatypes as dt
from bigframes_vendored.ibis.formats import TypeMapper
import sqlglot as sg
import sqlglot.expressions as sge

typecode = sge.DataType.Type

_from_sqlglot_types = {
    typecode.BIGDECIMAL: partial(dt.Decimal, 76, 38),
    typecode.BIGINT: dt.Int64,
    typecode.BINARY: dt.Binary,
    typecode.BOOLEAN: dt.Boolean,
    typecode.CHAR: dt.String,
    typecode.DATE: dt.Date,
    typecode.DATE32: dt.Date,
    typecode.DOUBLE: dt.Float64,
    typecode.ENUM: dt.String,
    typecode.ENUM8: dt.String,
    typecode.ENUM16: dt.String,
    typecode.FLOAT: dt.Float32,
    typecode.FIXEDSTRING: dt.String,
    typecode.HSTORE: partial(dt.Map, dt.string, dt.string),
    typecode.INET: dt.INET,
    typecode.INT128: partial(dt.Decimal, 38, 0),
    typecode.INT256: partial(dt.Decimal, 76, 0),
    typecode.INT: dt.Int32,
    typecode.IPADDRESS: dt.INET,
    typecode.JSON: dt.JSON,
    typecode.JSONB: partial(dt.JSON, binary=True),
    typecode.LONGBLOB: dt.Binary,
    typecode.LONGTEXT: dt.String,
    typecode.MEDIUMBLOB: dt.Binary,
    typecode.MEDIUMTEXT: dt.String,
    typecode.MONEY: dt.Decimal(19, 4),
    typecode.NCHAR: dt.String,
    typecode.UUID: dt.UUID,
    typecode.NAME: dt.String,
    typecode.NULL: dt.Null,
    typecode.NVARCHAR: dt.String,
    typecode.OBJECT: partial(dt.Map, dt.string, dt.json),
    typecode.ROWVERSION: partial(dt.Binary, nullable=False),
    typecode.SMALLINT: dt.Int16,
    typecode.SMALLMONEY: dt.Decimal(10, 4),
    typecode.TEXT: dt.String,
    typecode.TIME: dt.Time,
    typecode.TIMETZ: dt.Time,
    typecode.TINYBLOB: dt.Binary,
    typecode.TINYINT: dt.Int8,
    typecode.TINYTEXT: dt.String,
    typecode.UBIGINT: dt.UInt64,
    typecode.UINT: dt.UInt32,
    typecode.USMALLINT: dt.UInt16,
    typecode.UTINYINT: dt.UInt8,
    typecode.UUID: dt.UUID,
    typecode.VARBINARY: dt.Binary,
    typecode.VARCHAR: dt.String,
    typecode.VARIANT: dt.JSON,
    typecode.SET: partial(dt.Array, dt.string),
    #############################
    # Unsupported sqlglot types #
    #############################
    # BIT = auto() # mysql
    # BIGSERIAL = auto()
    # DATETIME64 = auto() # clickhouse
    # ENUM = auto()
    # INT4RANGE = auto()
    # INT4MULTIRANGE = auto()
    # INT8RANGE = auto()
    # INT8MULTIRANGE = auto()
    # NUMRANGE = auto()
    # NUMMULTIRANGE = auto()
    # TSRANGE = auto()
    # TSMULTIRANGE = auto()
    # TSTZRANGE = auto()
    # TSTZMULTIRANGE = auto()
    # DATERANGE = auto()
    # DATEMULTIRANGE = auto()
    # HLLSKETCH = auto()
    # IMAGE = auto()
    # IPPREFIX = auto()
    # SERIAL = auto()
    # SET = auto()
    # SMALLSERIAL = auto()
    # SUPER = auto()
    # TIMESTAMPLTZ = auto()
    # UNKNOWN = auto()  # Sentinel value, useful for type annotation
    # UINT128 = auto()
    # UINT256 = auto()
    # USERDEFINED = "USER-DEFINED"
    # XML = auto()
}

_to_sqlglot_types = {
    dt.Null: typecode.NULL,
    dt.Boolean: typecode.BOOLEAN,
    dt.Int8: typecode.TINYINT,
    dt.Int16: typecode.SMALLINT,
    dt.Int32: typecode.INT,
    dt.Int64: typecode.BIGINT,
    dt.UInt8: typecode.UTINYINT,
    dt.UInt16: typecode.USMALLINT,
    dt.UInt32: typecode.UINT,
    dt.UInt64: typecode.UBIGINT,
    dt.Float16: typecode.FLOAT,
    dt.Float32: typecode.FLOAT,
    dt.Float64: typecode.DOUBLE,
    dt.String: typecode.VARCHAR,
    dt.Binary: typecode.VARBINARY,
    dt.INET: typecode.INET,
    dt.UUID: typecode.UUID,
    dt.MACADDR: typecode.VARCHAR,
    dt.Date: typecode.DATE,
    dt.Time: typecode.TIME,
}

_geotypes = {
    "POINT": dt.Point,
    "LINESTRING": dt.LineString,
    "POLYGON": dt.Polygon,
    "MULTIPOINT": dt.MultiPoint,
    "MULTILINESTRING": dt.MultiLineString,
    "MULTIPOLYGON": dt.MultiPolygon,
}


class SqlglotType(TypeMapper):
    dialect: str | None = None
    """The dialect this parser is for."""

    default_nullable = True
    """Default nullability when not specified."""

    default_decimal_precision: int | None = None
    """Default decimal precision when not specified."""

    default_decimal_scale: int | None = None
    """Default decimal scale when not specified."""

    default_temporal_scale: int | None = None
    """Default temporal scale when not specified."""

    default_interval_precision: str | None = None
    """Default interval precision when not specified."""

    unknown_type_strings: dict[str, dt.DataType] = {}
    """String to ibis datatype mapping to use when converting unknown types."""

    @classmethod
    def to_ibis(cls, typ: sge.DataType, nullable: bool | None = None) -> dt.DataType:
        """Convert a sqlglot type to an ibis type."""
        typecode = typ.this

        # broken sqlglot thing
        if isinstance(typecode, sge.Interval):
            typ = sge.DataType(
                this=sge.DataType.Type.INTERVAL,
                expressions=[typecode.unit],
            )
            typecode = typ.this

        if method := getattr(cls, f"_from_sqlglot_{typecode.name}", None):
            dtype = method(*typ.expressions)
        else:
            dtype = _from_sqlglot_types[typecode](nullable=cls.default_nullable)

        if nullable is not None:
            return dtype.copy(nullable=nullable)
        else:
            return dtype

    @classmethod
    def from_ibis(cls, dtype: dt.DataType) -> sge.DataType:
        """Convert an Ibis dtype to an sqlglot dtype."""

        if method := getattr(cls, f"_from_ibis_{dtype.name}", None):
            return method(dtype)
        else:
            return sge.DataType(this=_to_sqlglot_types[type(dtype)])

    @classmethod
    def from_string(cls, text: str, nullable: bool | None = None) -> dt.DataType:
        if dtype := cls.unknown_type_strings.get(text.lower()):
            return dtype

        try:
            sgtype = sg.parse_one(text, into=sge.DataType, read=cls.dialect)
            return cls.to_ibis(sgtype, nullable=nullable)
        except sg.errors.ParseError:
            # If sqlglot can't parse the type fall back to `dt.unknown`
            pass

        return dt.unknown

    @classmethod
    def to_string(cls, dtype: dt.DataType) -> str:
        return cls.from_ibis(dtype).sql(dialect=cls.dialect)

    @classmethod
    def _from_sqlglot_ARRAY(cls, value_type: sge.DataType) -> dt.Array:
        return dt.Array(cls.to_ibis(value_type), nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_MAP(
        cls, key_type: sge.DataType, value_type: sge.DataType
    ) -> dt.Map:
        return dt.Map(
            cls.to_ibis(key_type),
            cls.to_ibis(value_type),
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_STRUCT(cls, *fields: sge.ColumnDef) -> dt.Struct:
        types = {}
        for i, field in enumerate(fields):
            if isinstance(field, sge.ColumnDef):
                types[field.name] = cls.to_ibis(field.args["kind"])
            else:
                types[f"f{i:d}"] = cls.from_string(str(field))
        return dt.Struct(types, nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_TIMESTAMP(cls, scale=None) -> dt.Timestamp:
        return dt.Timestamp(
            scale=cls.default_temporal_scale if scale is None else int(scale.this.this),
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_TIMESTAMPTZ(cls, scale=None) -> dt.Timestamp:
        return dt.Timestamp(
            timezone="UTC",
            scale=cls.default_temporal_scale if scale is None else int(scale.this.this),
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_TIMESTAMPLTZ(cls, scale=None) -> dt.Timestamp:
        return dt.Timestamp(
            timezone="UTC",
            scale=cls.default_temporal_scale if scale is None else int(scale.this.this),
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_TIMESTAMPNTZ(cls, scale=None) -> dt.Timestamp:
        return dt.Timestamp(
            timezone=None,
            scale=cls.default_temporal_scale if scale is None else int(scale.this.this),
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_INTERVAL(
        cls, precision_or_span: sge.IntervalSpan | None = None
    ) -> dt.Interval:
        nullable = cls.default_nullable
        if precision_or_span is None:
            precision_or_span = cls.default_interval_precision

        if isinstance(precision_or_span, str):
            return dt.Interval(precision_or_span, nullable=nullable)
        elif isinstance(precision_or_span, sge.IntervalSpan):
            if (expression := precision_or_span.expression) is not None:
                unit = expression.this
            else:
                unit = precision_or_span.this.this
            return dt.Interval(unit=unit, nullable=nullable)
        elif isinstance(precision_or_span, sge.Var):
            return dt.Interval(unit=precision_or_span.this, nullable=nullable)
        elif precision_or_span is None:
            raise com.IbisTypeError("Interval precision is None")
        else:
            raise com.IbisTypeError(precision_or_span)

    @classmethod
    def _from_sqlglot_DECIMAL(
        cls,
        precision: sge.DataTypeParam | None = None,
        scale: sge.DataTypeParam | None = None,
    ) -> dt.Decimal:
        if precision is None:
            precision = cls.default_decimal_precision
        else:
            precision = int(precision.this.this)

        if scale is None:
            scale = cls.default_decimal_scale
        else:
            scale = int(scale.this.this)

        return dt.Decimal(precision, scale, nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_GEOMETRY(
        cls, arg: sge.DataTypeParam | None = None, srid: sge.DataTypeParam | None = None
    ) -> sge.DataType:
        if arg is not None:
            typeclass = _geotypes[arg.this.this]
        else:
            typeclass = dt.GeoSpatial
        if srid is not None:
            srid = int(srid.this.this)
        return typeclass(geotype="geometry", nullable=cls.default_nullable, srid=srid)

    @classmethod
    def _from_sqlglot_GEOGRAPHY(
        cls, arg: sge.DataTypeParam | None = None, srid: sge.DataTypeParam | None = None
    ) -> sge.DataType:
        if arg is not None:
            typeclass = _geotypes[arg.this.this]
        else:
            typeclass = dt.GeoSpatial
        if srid is not None:
            srid = int(srid.this.this)
        return typeclass(geotype="geography", nullable=cls.default_nullable, srid=srid)

    @classmethod
    def _from_ibis_JSON(cls, dtype: dt.JSON) -> sge.DataType:
        return sge.DataType(this=typecode.JSONB if dtype.binary else typecode.JSON)

    @classmethod
    def _from_ibis_Interval(cls, dtype: dt.Interval) -> sge.DataType:
        assert dtype.unit is not None, "interval unit cannot be None"
        return sge.DataType(
            this=typecode.INTERVAL,
            expressions=[sge.Var(this=dtype.unit.name)],
        )

    @classmethod
    def _from_ibis_Array(cls, dtype: dt.Array) -> sge.DataType:
        value_type = cls.from_ibis(dtype.value_type)
        return sge.DataType(this=typecode.ARRAY, expressions=[value_type], nested=True)

    @classmethod
    def _from_ibis_Map(cls, dtype: dt.Map) -> sge.DataType:
        key_type = cls.from_ibis(dtype.key_type)
        value_type = cls.from_ibis(dtype.value_type)
        return sge.DataType(
            this=typecode.MAP, expressions=[key_type, value_type], nested=True
        )

    @classmethod
    def _from_ibis_Struct(cls, dtype: dt.Struct) -> sge.DataType:
        fields = [
            sge.ColumnDef(
                # always quote struct fields to allow reserved words as field names
                this=sg.to_identifier(name, quoted=True),
                kind=cls.from_ibis(field),
            )
            for name, field in dtype.items()
        ]
        return sge.DataType(this=typecode.STRUCT, expressions=fields, nested=True)

    @classmethod
    def _from_ibis_Decimal(cls, dtype: dt.Decimal) -> sge.DataType:
        if (precision := dtype.precision) is None:
            precision = cls.default_decimal_precision

        if (scale := dtype.scale) is None:
            scale = cls.default_decimal_scale

        expressions = []

        if precision is not None:
            expressions.append(sge.DataTypeParam(this=sge.Literal.number(precision)))

        if scale is not None:
            if precision is None:
                raise com.IbisTypeError(
                    "Decimal scale cannot be specified without precision"
                )
            expressions.append(sge.DataTypeParam(this=sge.Literal.number(scale)))

        return sge.DataType(this=typecode.DECIMAL, expressions=expressions or None)

    @classmethod
    def _from_ibis_Timestamp(cls, dtype: dt.Timestamp) -> sge.DataType:
        code = typecode.TIMESTAMP if dtype.timezone is None else typecode.TIMESTAMPTZ
        if dtype.scale is not None:
            scale = sge.DataTypeParam(this=sge.Literal.number(dtype.scale))
            return sge.DataType(this=code, expressions=[scale])
        else:
            return sge.DataType(this=code)

    @classmethod
    def _from_ibis_GeoSpatial(cls, dtype: dt.GeoSpatial):
        expressions = [None]

        if (srid := dtype.srid) is not None:
            expressions.append(sge.DataTypeParam(this=sge.convert(srid)))

        this = getattr(typecode, dtype.geotype.upper())

        return sge.DataType(this=this, expressions=expressions)

    @classmethod
    def _from_ibis_SpecificGeometry(cls, dtype: dt.GeoSpatial):
        expressions = [
            sge.DataTypeParam(this=sge.Var(this=dtype.__class__.__name__.upper()))
        ]

        if (srid := dtype.srid) is not None:
            expressions.append(sge.DataTypeParam(this=sge.convert(srid)))

        this = getattr(typecode, dtype.geotype.upper())
        return sge.DataType(this=this, expressions=expressions)

    _from_ibis_Point = (
        _from_ibis_LineString
    ) = (
        _from_ibis_Polygon
    ) = (
        _from_ibis_MultiLineString
    ) = _from_ibis_MultiPoint = _from_ibis_MultiPolygon = _from_ibis_SpecificGeometry


class BigQueryType(SqlglotType):
    dialect = "bigquery"

    default_decimal_precision = 38
    default_decimal_scale = 9

    @classmethod
    def _from_sqlglot_NUMERIC(cls) -> dt.Decimal:
        return dt.Decimal(
            cls.default_decimal_precision,
            cls.default_decimal_scale,
            nullable=cls.default_nullable,
        )

    @classmethod
    def _from_sqlglot_BIGNUMERIC(cls) -> dt.Decimal:
        return dt.Decimal(76, 38, nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_DATETIME(cls) -> dt.Timestamp:
        return dt.Timestamp(timezone=None, nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_TIMESTAMP(cls) -> dt.Timestamp:
        return dt.Timestamp(timezone=None, nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_TIMESTAMPTZ(cls) -> dt.Timestamp:
        return dt.Timestamp(timezone="UTC", nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_GEOGRAPHY(
        cls, arg: sge.DataTypeParam | None = None, srid: sge.DataTypeParam | None = None
    ) -> dt.GeoSpatial:
        return dt.GeoSpatial(
            geotype="geography", srid=4326, nullable=cls.default_nullable
        )

    @classmethod
    def _from_sqlglot_TINYINT(cls) -> dt.Int64:
        return dt.Int64(nullable=cls.default_nullable)

    _from_sqlglot_UINT = (
        _from_sqlglot_USMALLINT
    ) = (
        _from_sqlglot_UTINYINT
    ) = _from_sqlglot_INT = _from_sqlglot_SMALLINT = _from_sqlglot_TINYINT

    @classmethod
    def _from_sqlglot_UBIGINT(cls) -> NoReturn:
        raise com.UnsupportedBackendType(
            "Unsigned BIGINT isn't representable in BigQuery INT64"
        )

    @classmethod
    def _from_sqlglot_FLOAT(cls) -> dt.Float64:
        return dt.Float64(nullable=cls.default_nullable)

    @classmethod
    def _from_sqlglot_MAP(cls) -> NoReturn:
        raise com.UnsupportedBackendType("Maps are not supported in BigQuery")

    @classmethod
    def _from_ibis_Map(cls, dtype: dt.Map) -> NoReturn:
        raise com.UnsupportedBackendType("Maps are not supported in BigQuery")

    @classmethod
    def _from_ibis_Timestamp(cls, dtype: dt.Timestamp) -> sge.DataType:
        if dtype.timezone is None:
            return sge.DataType(this=sge.DataType.Type.DATETIME)
        elif dtype.timezone == "UTC":
            return sge.DataType(this=sge.DataType.Type.TIMESTAMPTZ)
        else:
            raise com.UnsupportedBackendType(
                "BigQuery does not support timestamps with timezones other than 'UTC'"
            )

    @classmethod
    def _from_ibis_Decimal(cls, dtype: dt.Decimal) -> sge.DataType:
        precision = dtype.precision
        scale = dtype.scale
        if (precision, scale) == (76, 38):
            return sge.DataType(this=sge.DataType.Type.BIGDECIMAL)
        elif (precision, scale) in ((38, 9), (None, None)):
            return sge.DataType(this=sge.DataType.Type.DECIMAL)
        else:
            raise com.UnsupportedBackendType(
                "BigQuery only supports decimal types with precision of 38 and "
                f"scale of 9 (NUMERIC) or precision of 76 and scale of 38 (BIGNUMERIC). "
                f"Current precision: {dtype.precision}. Current scale: {dtype.scale}"
            )

    @classmethod
    def _from_ibis_UInt64(cls, dtype: dt.UInt64) -> NoReturn:
        raise com.UnsupportedBackendType(
            f"Conversion from {dtype} to BigQuery integer type (Int64) is lossy"
        )

    @classmethod
    def _from_ibis_UInt32(cls, dtype: dt.UInt32) -> sge.DataType:
        return sge.DataType(this=sge.DataType.Type.BIGINT)

    _from_ibis_UInt8 = _from_ibis_UInt16 = _from_ibis_UInt32

    @classmethod
    def _from_ibis_GeoSpatial(cls, dtype: dt.GeoSpatial) -> sge.DataType:
        if (dtype.geotype, dtype.srid) == ("geography", 4326):
            return sge.DataType(this=sge.DataType.Type.GEOGRAPHY)
        else:
            raise com.UnsupportedBackendType(
                "BigQuery geography uses points on WGS84 reference ellipsoid."
                f"Current geotype: {dtype.geotype}, Current srid: {dtype.srid}"
            )


class BigQueryUDFType(BigQueryType):
    @classmethod
    def _from_ibis_Int64(cls, dtype: dt.Int64) -> NoReturn:
        raise com.UnsupportedBackendType(
            "int64 is not a supported input or output type in BigQuery UDFs; use float64 instead"
        )
