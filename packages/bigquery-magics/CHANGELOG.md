# Changelog

## [0.8.1](https://github.com/googleapis/python-bigquery-magics/compare/v0.8.0...v0.8.1) (2025-03-21)


### Bug Fixes

* Remove setup.cfg configuration for creating universal wheels ([#106](https://github.com/googleapis/python-bigquery-magics/issues/106)) ([fe3ec29](https://github.com/googleapis/python-bigquery-magics/commit/fe3ec29fefb7ca9195484d13f2bf15c65cf20614))


### Dependencies

* Bump minimum required version of spanner-graph-notebook to 1.1.5 ([#110](https://github.com/googleapis/python-bigquery-magics/issues/110)) ([756ac0d](https://github.com/googleapis/python-bigquery-magics/commit/756ac0d0910a0622aee88ed558886456311976e9))

## [0.8.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.7.0...v0.8.0) (2025-03-13)


### Features

* Fix graph visualization to work with latest spanner-graph-notebook code; also, allow visualization when only some columns are json. ([#102](https://github.com/googleapis/python-bigquery-magics/issues/102)) ([c33297c](https://github.com/googleapis/python-bigquery-magics/commit/c33297cf2a1db9a0bd2e8c078be1e06239122459))
* Support multiple columns in graph visualization ([#100](https://github.com/googleapis/python-bigquery-magics/issues/100)) ([dbb6442](https://github.com/googleapis/python-bigquery-magics/commit/dbb64426dd617697785bccf15d98c32f8217c33e))

## [0.7.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.6.0...v0.7.0) (2025-03-11)


### Features

* Support visualization of graph queries by adding the --graph argument. ([#94](https://github.com/googleapis/python-bigquery-magics/issues/94)) ([3c054f5](https://github.com/googleapis/python-bigquery-magics/commit/3c054f5e27b5097c18899ff732fccebdf36b47e6))


### Bug Fixes

* Resolve issue where pre-release versions of dependencies are installed ([#97](https://github.com/googleapis/python-bigquery-magics/issues/97)) ([79c59e7](https://github.com/googleapis/python-bigquery-magics/commit/79c59e7b8ceba6f2be1fbe16d12b69b5a0b4d774))

## [0.6.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.5.0...v0.6.0) (2025-02-12)


### Features

* Add '--use-geodataframe' argument to return a GeoDataFrame ([#91](https://github.com/googleapis/python-bigquery-magics/issues/91)) ([fc04f34](https://github.com/googleapis/python-bigquery-magics/commit/fc04f343d0e9c5c6b11e784d698c28865c2909cd))
* Add an is_registered global value to indicate whether the extension has been loaded ([#83](https://github.com/googleapis/python-bigquery-magics/issues/83)) ([0bc4473](https://github.com/googleapis/python-bigquery-magics/commit/0bc4473d550c612241ea1428f7538938257b2656))

## [0.5.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.4.0...v0.5.0) (2024-12-17)


### Features

* Add `%%bqsql` as an alias to the `%%bigquery` magic ([#72](https://github.com/googleapis/python-bigquery-magics/issues/72)) ([03fe1d5](https://github.com/googleapis/python-bigquery-magics/commit/03fe1d544ef22865c07c680873f980c64bbc7abc))
* Add `bigquery_magics.context.default_variable` option ([#70](https://github.com/googleapis/python-bigquery-magics/issues/70)) ([72ed882](https://github.com/googleapis/python-bigquery-magics/commit/72ed882c9359718a702bab2bca76933548650064))

## [0.4.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.3.0...v0.4.0) (2024-09-24)


### Features

* Add support for overriding `context.engine` by magic argument ([#60](https://github.com/googleapis/python-bigquery-magics/issues/60)) ([ff57f14](https://github.com/googleapis/python-bigquery-magics/commit/ff57f14aa43c60ffc02b8966da2405c31ea42c64))

## [0.3.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.2.0...v0.3.0) (2024-09-20)


### Features

* Add support for BigQuery DataFrames. Set `context.engine` to 'bigframes' to support query results larger than 10 GB ([#58](https://github.com/googleapis/python-bigquery-magics/issues/58)) ([90ba05f](https://github.com/googleapis/python-bigquery-magics/commit/90ba05f3d918979788e01b0cd3201ac8f01741a9))

## [0.2.0](https://github.com/googleapis/python-bigquery-magics/compare/v0.1.1...v0.2.0) (2024-08-27)


### Features

* Depend on pydata-google-auth to fetch credentials ([#49](https://github.com/googleapis/python-bigquery-magics/issues/49)) ([8db23fc](https://github.com/googleapis/python-bigquery-magics/commit/8db23fc60624baae9c0dffd500d8856cb6e92f42))

## [0.1.1](https://github.com/googleapis/python-bigquery-magics/compare/v0.1.0...v0.1.1) (2024-08-22)


### Dependencies

* Depend on ipykernel 5.5.6+ instead of 6.0+ ([83d8fac](https://github.com/googleapis/python-bigquery-magics/commit/83d8facf6d04752c1f8c5e25575a3975c9b30e1c))


### Documentation

* Correct links to project pages in README ([#33](https://github.com/googleapis/python-bigquery-magics/issues/33)) ([ace5020](https://github.com/googleapis/python-bigquery-magics/commit/ace5020ff8ae374145579e75cb996150680f2bde))
* Update the IPython Magics docs ([#27](https://github.com/googleapis/python-bigquery-magics/issues/27)) ([62e88b3](https://github.com/googleapis/python-bigquery-magics/commit/62e88b3f4a595ecdc4a00d661b956c5d50fd6c35))

## 0.1.0 (2024-04-25)


### Features

* Initial copy from google-cloud-bigquery ([4a69d26](https://github.com/googleapis/python-bigquery-magics/commit/4a69d26ae3e5e7c659c7b79ac935393abb4146e3))


### Documentation

* Clean up docs and let the nox pass ([#24](https://github.com/googleapis/python-bigquery-magics/issues/24)) ([275712f](https://github.com/googleapis/python-bigquery-magics/commit/275712f4e4b647cda2d253e1f6b7a2fa093ee7c1))
* Reset the changelog for the new package ([#22](https://github.com/googleapis/python-bigquery-magics/issues/22)) ([f7d9c14](https://github.com/googleapis/python-bigquery-magics/commit/f7d9c1445feac32e468a3e06ca55c9474a1ae548))

## Changelog

[PyPI History][1]

[1]: https://pypi.org/project/bigquery-magics/#history
