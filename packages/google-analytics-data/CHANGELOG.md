# Changelog

### [0.6.1](https://www.github.com/googleapis/python-analytics-data/compare/v0.6.0...v0.6.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#82](https://www.github.com/googleapis/python-analytics-data/issues/82)) ([acd60f1](https://www.github.com/googleapis/python-analytics-data/commit/acd60f15ae2192e54b180776b62ee2ea9fce7d3f))

## [0.6.0](https://www.github.com/googleapis/python-analytics-data/compare/v0.5.1...v0.6.0) (2021-06-08)


### Features

* support self-signed JWT flow for service accounts ([ff2beb8](https://www.github.com/googleapis/python-analytics-data/commit/ff2beb8f923570a78772712dc140fc7ba99148d6))


### Bug Fixes

* add async client to %name_%version/init.py ([ff2beb8](https://www.github.com/googleapis/python-analytics-data/commit/ff2beb8f923570a78772712dc140fc7ba99148d6))

### [0.5.1](https://www.github.com/googleapis/python-analytics-data/compare/v0.5.0...v0.5.1) (2021-05-28)


### Bug Fixes

* **deps:** require google-api-core>=1.22.2 ([675ae9f](https://www.github.com/googleapis/python-analytics-data/commit/675ae9fb45bc4ea1adbbba1a302f04daf6368fbf))


### Documentation

* add sample code for Data API v1 ([#57](https://www.github.com/googleapis/python-analytics-data/issues/57)) ([a1e63c5](https://www.github.com/googleapis/python-analytics-data/commit/a1e63c56f5fa5835c528724c9d861c18cb34d6ad))

## [0.5.0](https://www.github.com/googleapis/python-analytics-data/compare/v0.4.1...v0.5.0) (2021-04-01)


### Features

* add `kind` field which is used to distinguish between response types ([#60](https://www.github.com/googleapis/python-analytics-data/issues/60)) ([83f1fc1](https://www.github.com/googleapis/python-analytics-data/commit/83f1fc1af4baa799d3f457127ef2fe687b0aa49d))
* add `potentially_thresholded_requests_per_hour` field to `PropertyQuota` ([83f1fc1](https://www.github.com/googleapis/python-analytics-data/commit/83f1fc1af4baa799d3f457127ef2fe687b0aa49d))


### Documentation

* update quickstart samples to support the Data API v1 beta ([#50](https://www.github.com/googleapis/python-analytics-data/issues/50)) ([ad51cf2](https://www.github.com/googleapis/python-analytics-data/commit/ad51cf28f6c3e306780ca48eb26299b4158068ad))
* update region tag names to match the convention ([#55](https://www.github.com/googleapis/python-analytics-data/issues/55)) ([747f551](https://www.github.com/googleapis/python-analytics-data/commit/747f551c4b3a2f5b3d4602788b8f9c19cbd9904b))

### [0.4.1](https://www.github.com/googleapis/python-analytics-data/compare/v0.4.0...v0.4.1) (2021-03-16)


### Bug Fixes

* fix from_service_account_info for async clients ([#44](https://www.github.com/googleapis/python-analytics-data/issues/44)) ([fdebf9b](https://www.github.com/googleapis/python-analytics-data/commit/fdebf9b96e915a06fecaeb83c1ca59de077249a8))
* **v1beta:** (BREAKING) rename the 'page_size', 'page_token', 'total_size' fields to 'limit', 'offset' and 'row_count' respectively ([8fd57a3](https://www.github.com/googleapis/python-analytics-data/commit/8fd57a340b7e052dc9c4d6c33882add75405eb8b))

## [0.4.0](https://www.github.com/googleapis/python-analytics-data/compare/v0.3.0...v0.4.0) (2021-02-25)


### Features

* add v1beta ([#35](https://www.github.com/googleapis/python-analytics-data/issues/35)) ([8b43efe](https://www.github.com/googleapis/python-analytics-data/commit/8b43efe93086e1846ad68173fac3929492e98e0a))

## [0.3.0](https://www.github.com/googleapis/python-analytics-data/compare/v0.2.0...v0.3.0) (2021-01-06)


### Features

* add custom_definition to DimensionMetadata object and MetricMetadata object ([9bd3477](https://www.github.com/googleapis/python-analytics-data/commit/9bd347737319ea5cae0cf6556d55cd8397a06811))
* add from_service_account_info factory and fix sphinx identifiers  ([#27](https://www.github.com/googleapis/python-analytics-data/issues/27)) ([2775104](https://www.github.com/googleapis/python-analytics-data/commit/2775104b84dda7cccc0fe2813cb8fde5e8930ae8))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([#22](https://www.github.com/googleapis/python-analytics-data/issues/22)) ([b3dc882](https://www.github.com/googleapis/python-analytics-data/commit/b3dc88221da924816f04e8c0ce716c0d45555d4c))

## [0.2.0](https://www.github.com/googleapis/python-analytics-data/compare/v0.1.0...v0.2.0) (2020-11-16)


### Features

* add support for realtime reports ([#12](https://www.github.com/googleapis/python-analytics-data/issues/12)) ([929c44c](https://www.github.com/googleapis/python-analytics-data/commit/929c44c466fa1cb08255c0be730b2a9d1d2e2c04)), closes [/github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py#L27-L32](https://www.github.com/googleapis//github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py/issues/L27-L32)


### Documentation

* added a sample ([#7](https://www.github.com/googleapis/python-analytics-data/issues/7)) ([a4bcc31](https://www.github.com/googleapis/python-analytics-data/commit/a4bcc3147efd800b2ef754fe1af27361842e7cdc))

## 0.1.0 (2020-09-14)


### Features

* generate v1alpha1 ([488c410](https://www.github.com/googleapis/python-analytics-data/commit/488c4106c782f55a59c90a4a311e4f6431a1b1c1))
