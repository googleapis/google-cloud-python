# Changelog

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.5...google-maps-routeoptimization-v0.1.6) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.4...google-maps-routeoptimization-v0.1.5) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.3...google-maps-routeoptimization-v0.1.4) (2024-09-30)


### Features

* A new field `route_token` is added to message `.google.maps.routeoptimization.v1.ShipmentRoute.Transition` ([32b254c](https://github.com/googleapis/google-cloud-python/commit/32b254c110626aff2194aceb93f131f745cfcf29))
* Add support for generating route tokens  ([32b254c](https://github.com/googleapis/google-cloud-python/commit/32b254c110626aff2194aceb93f131f745cfcf29))


### Documentation

* A comment for field `code` in message `.google.maps.routeoptimization.v1.OptimizeToursValidationError` is changed ([32b254c](https://github.com/googleapis/google-cloud-python/commit/32b254c110626aff2194aceb93f131f745cfcf29))
* A comment for field `populate_transition_polylines` in message `.google.maps.routeoptimization.v1.OptimizeToursRequest` is changed ([32b254c](https://github.com/googleapis/google-cloud-python/commit/32b254c110626aff2194aceb93f131f745cfcf29))
* A comment for method `BatchOptimizeTours` in service `RouteOptimization` is changed ([32b254c](https://github.com/googleapis/google-cloud-python/commit/32b254c110626aff2194aceb93f131f745cfcf29))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.2...google-maps-routeoptimization-v0.1.3) (2024-09-16)


### Features

* [google-maps-routeoptimization] minor fields and documentation update ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A new field `cost_per_kilometer_below_soft_max` is added to message `.google.maps.routeoptimization.v1.DistanceLimit` ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A new field `route_modifiers` is added to message `.google.maps.routeoptimization.v1.Vehicle` ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A new message `RouteModifiers` is added ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))


### Documentation

* A comment for enum value `CODE_UNSPECIFIED` in enum `Code` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for enum value `DEFAULT_SOLVE` in enum `SolvingMode` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for enum value `RELAX_VISIT_TIMES_AND_SEQUENCE_AFTER_THRESHOLD` in enum `Level` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for field `code` in message `.google.maps.routeoptimization.v1.OptimizeToursValidationError` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for field `reasons` in message `.google.maps.routeoptimization.v1.SkippedShipment` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for field `validation_errors` in message `.google.maps.routeoptimization.v1.OptimizeToursResponse` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for message `OptimizeToursValidationError` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for message `TimeWindow` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))
* A comment for method `BatchOptimizeTours` in service `RouteOptimization` is changed ([366f6f1](https://github.com/googleapis/google-cloud-python/commit/366f6f10e29a9d9cc307cbd1f16deb4decf26050))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.1...google-maps-routeoptimization-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-maps-routeoptimization-v0.1.0...google-maps-routeoptimization-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## 0.1.0 (2024-05-16)


### Features

* add initial files for google.maps.routeoptimization.v1 ([#12670](https://github.com/googleapis/google-cloud-python/issues/12670)) ([524cd1e](https://github.com/googleapis/google-cloud-python/commit/524cd1ea815839983f803502d3b8e0dece40544a))

## Changelog
