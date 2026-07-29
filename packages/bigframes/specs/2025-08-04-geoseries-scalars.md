# Implementing GeoSeries scalar operators

This project is to implement all GeoSeries scalar properties and methods in the
`bigframes.geopandas.GeoSeries` class. Likewise, all BigQuery GEOGRAPHY
functions should be exposed in the `bigframes.bigquery` module.

## Background

*Explain the context and why this change is necessary.*
*Include links to relevant issues or documentation.*

* https://geopandas.org/en/stable/docs/reference/geoseries.html
* https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions

## Acceptance Criteria

*Define the specific, measurable outcomes that indicate the task is complete.*
*Use a checklist format for clarity.*

### GeoSeries methods and properties

- [x] Constructor
- [x] GeoSeries.area
- [x] GeoSeries.boundary
- [ ] GeoSeries.bounds
- [ ] GeoSeries.total_bounds
- [x] GeoSeries.length
- [ ] GeoSeries.geom_type
- [ ] GeoSeries.offset_curve
- [x] GeoSeries.distance
- [ ] GeoSeries.hausdorff_distance
- [ ] GeoSeries.frechet_distance
- [ ] GeoSeries.representative_point
- [ ] GeoSeries.exterior
- [ ] GeoSeries.interiors
- [ ] GeoSeries.minimum_bounding_radius
- [ ] GeoSeries.minimum_clearance
- [x] GeoSeries.x
- [x] GeoSeries.y
- [ ] GeoSeries.z
- [ ] GeoSeries.m
- [ ] GeoSeries.get_coordinates
- [ ] GeoSeries.count_coordinates
- [ ] GeoSeries.count_geometries
- [ ] GeoSeries.count_interior_rings
- [ ] GeoSeries.set_precision
- [ ] GeoSeries.get_precision
- [ ] GeoSeries.get_geometry
- [x] GeoSeries.is_closed
- [ ] GeoSeries.is_empty
- [ ] GeoSeries.is_ring
- [ ] GeoSeries.is_simple
- [ ] GeoSeries.is_valid
- [ ] GeoSeries.is_valid_reason
- [ ] GeoSeries.is_valid_coverage
- [ ] GeoSeries.invalid_coverage_edges
- [ ] GeoSeries.has_m
- [ ] GeoSeries.has_z
- [ ] GeoSeries.is_ccw
- [ ] GeoSeries.contains
- [ ] GeoSeries.contains_properly
- [ ] GeoSeries.crosses
- [ ] GeoSeries.disjoint
- [ ] GeoSeries.dwithin
- [ ] GeoSeries.geom_equals
- [ ] GeoSeries.geom_equals_exact
- [ ] GeoSeries.geom_equals_identical
- [ ] GeoSeries.intersects
- [ ] GeoSeries.overlaps
- [ ] GeoSeries.touches
- [ ] GeoSeries.within
- [ ] GeoSeries.covers
- [ ] GeoSeries.covered_by
- [ ] GeoSeries.relate
- [ ] GeoSeries.relate_pattern
- [ ] GeoSeries.clip_by_rect
- [x] GeoSeries.difference
- [x] GeoSeries.intersection
- [ ] GeoSeries.symmetric_difference
- [ ] GeoSeries.union
- [x] GeoSeries.boundary
- [x] GeoSeries.buffer
- [x] GeoSeries.centroid
- [ ] GeoSeries.concave_hull
- [x] GeoSeries.convex_hull
- [ ] GeoSeries.envelope
- [ ] GeoSeries.extract_unique_points
- [ ] GeoSeries.force_2d
- [ ] GeoSeries.force_3d
- [ ] GeoSeries.make_valid
- [ ] GeoSeries.minimum_bounding_circle
- [ ] GeoSeries.maximum_inscribed_circle
- [ ] GeoSeries.minimum_clearance
- [ ] GeoSeries.minimum_clearance_line
- [ ] GeoSeries.minimum_rotated_rectangle
- [ ] GeoSeries.normalize
- [ ] GeoSeries.orient_polygons
- [ ] GeoSeries.remove_repeated_points
- [ ] GeoSeries.reverse
- [ ] GeoSeries.sample_points
- [ ] GeoSeries.segmentize
- [ ] GeoSeries.shortest_line
- [ ] GeoSeries.simplify
- [ ] GeoSeries.simplify_coverage
- [ ] GeoSeries.snap
- [ ] GeoSeries.transform
- [ ] GeoSeries.affine_transform
- [ ] GeoSeries.rotate
- [ ] GeoSeries.scale
- [ ] GeoSeries.skew
- [ ] GeoSeries.translate
- [ ] GeoSeries.interpolate
- [ ] GeoSeries.line_merge
- [ ] GeoSeries.project
- [ ] GeoSeries.shared_paths
- [ ] GeoSeries.build_area
- [ ] GeoSeries.constrained_delaunay_triangles
- [ ] GeoSeries.delaunay_triangles
- [ ] GeoSeries.explode
- [ ] GeoSeries.intersection_all
- [ ] GeoSeries.polygonize
- [ ] GeoSeries.union_all
- [ ] GeoSeries.voronoi_polygons
- [ ] GeoSeries.from_arrow
- [ ] GeoSeries.from_file
- [ ] GeoSeries.from_wkb
- [x] GeoSeries.from_wkt
- [x] GeoSeries.from_xy
- [ ] GeoSeries.to_arrow
- [ ] GeoSeries.to_file
- [ ] GeoSeries.to_json
- [ ] GeoSeries.to_wkb
- [x] GeoSeries.to_wkt
- [ ] GeoSeries.crs
- [ ] GeoSeries.set_crs
- [ ] GeoSeries.to_crs
- [ ] GeoSeries.estimate_utm_crs
- [ ] GeoSeries.fillna
- [ ] GeoSeries.isna
- [ ] GeoSeries.notna
- [ ] GeoSeries.clip
- [ ] GeoSeries.plot
- [ ] GeoSeries.explore
- [ ] GeoSeries.sindex
- [ ] GeoSeries.has_sindex
- [ ] GeoSeries.cx
- [ ] GeoSeries.__geo_interface__

### `bigframes.pandas` methods

Constructors: Functions that build new geography values from coordinates or
existing geographies.

- [x] ST_GEOGPOINT
- [ ] ST_MAKELINE
- [ ] ST_MAKEPOLYGON
- [ ] ST_MAKEPOLYGONORIENTED

Parsers	ST_GEOGFROM: Functions that create geographies from an external format
such as WKT and GeoJSON.

- [ ] ST_GEOGFROMGEOJSON
- [x] ST_GEOGFROMTEXT
- [ ] ST_GEOGFROMWKB
- [ ] ST_GEOGPOINTFROMGEOHASH

Formatters: Functions that export geographies to an external format such as WKT.

- [ ] ST_ASBINARY
- [ ] ST_ASGEOJSON
- [x] ST_ASTEXT
- [ ] ST_GEOHASH

Transformations: Functions that generate a new geography based on input.

- [x] ST_BOUNDARY
- [x] ST_BUFFER
- [ ] ST_BUFFERWITHTOLERANCE
- [x] ST_CENTROID
- [ ] ST_CENTROID_AGG (Aggregate)
- [ ] ST_CLOSESTPOINT
- [x] ST_CONVEXHULL
- [x] ST_DIFFERENCE
- [ ] ST_EXTERIORRING
- [ ] ST_INTERIORRINGS
- [x] ST_INTERSECTION
- [ ] ST_LINEINTERPOLATEPOINT
- [ ] ST_LINESUBSTRING
- [ ] ST_SIMPLIFY
- [ ] ST_SNAPTOGRID
- [ ] ST_UNION
- [ ] ST_UNION_AGG (Aggregate)

Accessors: Functions that provide access to properties of a geography without
side-effects.

- [ ] ST_DIMENSION
- [ ] ST_DUMP
- [ ] ST_ENDPOINT
- [ ] ST_GEOMETRYTYPE
- [x] ST_ISCLOSED
- [ ] ST_ISCOLLECTION
- [ ] ST_ISEMPTY
- [ ] ST_ISRING
- [ ] ST_NPOINTS
- [ ] ST_NUMGEOMETRIES
- [ ] ST_NUMPOINTS
- [ ] ST_POINTN
- [ ] ST_STARTPOINT
- [x] ST_X
- [x] ST_Y

Predicates: Functions that return TRUE or FALSE for some spatial relationship
between two geographies or some property of a geography. These functions are
commonly used in filter clauses.

- [ ] ST_CONTAINS
- [ ] ST_COVEREDBY
- [ ] ST_COVERS
- [ ] ST_DISJOINT
- [ ] ST_DWITHIN
- [ ] ST_EQUALS
- [ ] ST_HAUSDORFFDWITHIN
- [ ] ST_INTERSECTS
- [ ] ST_INTERSECTSBOX
- [ ] ST_TOUCHES
- [ ] ST_WITHIN

Measures: Functions that compute measurements of one or more geographies.

- [ ] ST_ANGLE
- [x] ST_AREA
- [ ] ST_AZIMUTH
- [ ] ST_BOUNDINGBOX
- [x] ST_DISTANCE
- [ ] ST_EXTENT (Aggregate)
- [ ] ST_HAUSDORFFDISTANCE
- [ ] ST_LINELOCATEPOINT
- [x] ST_LENGTH
- [ ] ST_MAXDISTANCE
- [ ] ST_PERIMETER

Clustering: Functions that perform clustering on geographies.

- [ ] ST_CLUSTERDBSCAN

S2 functions: Functions for working with S2 cell coverings of GEOGRAPHY.

- [ ] S2_CELLIDFROMPOINT
- [ ] S2_COVERINGCELLIDS

Raster functions: Functions for analyzing geospatial rasters using geographies.

- [ ] 	ST_REGIONSTATS

## Detailed Steps

*Break down the implementation into small, actionable steps.*
*This section will guide the development process.*

### Implementing a new scalar geography operation

- [ ] **Define the operation dataclass:**
    - [ ] In `bigframes/operations/geo_ops.py`, create a new dataclass
          inheriting from `base_ops.UnaryOp` or `base_ops.BinaryOp`. Note that
          BinaryOp is for methods that take two **columns**. Any literal values can
          be passed as parameters to a UnaryOp.
    - [ ] Define the `name` of the operation and any parameters it requires.
    - [ ] Implement the `output_type` method to specify the data type of the result.
- [ ] **Export the new operation:**
    - [ ] In `bigframes/operations/__init__.py`, import your new operation dataclass and add it to the `__all__` list.
- [ ] **Implement the compilation logic:**
    - [ ] In `bigframes/core/compile/ibis_compiler/operations/geo_ops.py`:
        - [ ] If the BigQuery function has a direct equivalent in Ibis, you can often reuse an existing Ibis method.
        - [ ] If not, define a new Ibis UDF using `@ibis_udf.scalar.builtin` to map to the specific BigQuery function signature.
        - [ ] Create a new compiler implementation function (e.g., `geo_length_op_impl`).
        - [ ] Register this function to your operation dataclass using `@register_unary_op` or `@register_binary_op`.
    - [ ] In `bigframes/core/compile/sqlglot/expressions/geo_ops.py`:
        - [ ] Create a new compiler implementation function that generates the appropriate `sqlglot.exp` expression.
        - [ ] Register this function to your operation dataclass using `@register_unary_op` or `@register_binary_op`.
- [ ] **Implement the user-facing function or property:**
    - [ ] For a `bigframes.bigquery` function:
        - [ ] In `bigframes/bigquery/_operations/geo.py`, create the user-facing function (e.g., `st_length`).
        - [ ] The function should take a `Series` and any other parameters.
        - [ ] Inside the function, call `series._apply_unary_op` or `series._apply_binary_op`, passing the operation dataclass you created.
        - [ ] Add a comprehensive docstring with examples.
        - [ ] In `bigframes/bigquery/__init__.py`, import your new user-facing function and add it to the `__all__` list.
    - [ ] For a `GeoSeries` property or method:
        - [ ] In `bigframes/geopandas/geoseries.py`, create the property or
              method. Omit the docstring.
        - [ ] If the operation is not possible to be supported, such as if the
              geopandas method returns values in units corresponding to the
              coordinate system rather than meters that BigQuery uses, raise a
              `NotImplementedError` with a helpful message. Likewise, if a
              required parameter takes a value in terms of the coordinate
              system, but BigQuery uses meters, raise a `NotImplementedError`.
        - [ ] Otherwise, call `series._apply_unary_op` or `series._apply_binary_op`, passing the operation dataclass.
        - [ ] Add a comprehensive docstring with examples to the superclass in
              `third_party/bigframes_vendored/geopandas/geoseries.py`.
- [ ] **Add Tests:**
    - [ ] Add system tests in `tests/system/small/bigquery/test_geo.py` or `tests/system/small/geopandas/test_geoseries.py` to verify the end-to-end functionality. Test various inputs, including edge cases and `NULL` values.
    - [ ] If you are overriding a pandas or GeoPandas property and raising `NotImplementedError`, add a unit test to ensure the correct error is raised.

## Verification

*Specify the commands to run to verify the changes.*

- [ ] The `nox -r -s format lint lint_setup_py` linter should pass.
- [ ] The `nox -r -s mypy` static type checker should pass.
- [ ] The `nox -r -s docs docfx` docs should successfully build and include relevant docs in the output.
- [ ] All new and existing unit tests `pytest tests/unit` should pass.
- [ ] Identify all related system tests in the `tests/system` directories.
- [ ] All related system tests `pytest tests/system/small/path_to_relevant_test.py::test_name` should pass.

## Constraints

Follow the guidelines listed in GEMINI.md at the root of the repository.
