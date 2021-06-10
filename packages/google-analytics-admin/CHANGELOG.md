# Changelog

## [0.3.0](https://www.github.com/googleapis/python-analytics-admin/compare/v1.0.0...v0.3.0) (2021-06-09)


### Features

* add `ConversionEvent` methods to the API ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `ConversionEvent` type ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `CustomDimension` methods to the API ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `CustomDimension` type ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `CustomMetric` methods to the API ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `CustomMetric` type ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `GetGoogleSignalsSettings`, `UpdateGoogleSignalsSettings` methods to the API ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `GoogleSignalsSettings`  type ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `GoogleSignalsState`, `GoogleSignalsConsent` types ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add `MeasurementProtocolSecret` type ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* add MeasurementProtocolSecret methods to the API ([#71](https://www.github.com/googleapis/python-analytics-admin/issues/71)) ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* extend `ChangeHistoryResourceType` enum ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))


### Bug Fixes

* label `email_address` field of `UserLink` type as immutable ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))
* label `name` field of `UserLink` type as output only ([ab703de](https://www.github.com/googleapis/python-analytics-admin/commit/ab703deccb763ebc3b8be35a09e1cec27b8ef107))


### Documentation

* add Admin API samples for account management methods ([#58](https://www.github.com/googleapis/python-analytics-admin/issues/58)) ([2ecc350](https://www.github.com/googleapis/python-analytics-admin/commit/2ecc350759cfa50f02c0f29f75b647e260cacec0))
* add Admin API samples for account management methods ([#65](https://www.github.com/googleapis/python-analytics-admin/issues/65)) ([a3fecc4](https://www.github.com/googleapis/python-analytics-admin/commit/a3fecc47bb329aeba3706b7d6f0b26196c3a8977))
* add Admin API samples for property stream management methods ([#68](https://www.github.com/googleapis/python-analytics-admin/issues/68)) ([27da97e](https://www.github.com/googleapis/python-analytics-admin/commit/27da97e4574baec81ba3c13be8aece1efa689f75))
* add Admin API samples for property user link management methods ([#67](https://www.github.com/googleapis/python-analytics-admin/issues/67)) ([aa55627](https://www.github.com/googleapis/python-analytics-admin/commit/aa5562777009bbdd21fdc39990b50ac5fb19cc53))
* add samples for Google Analytics property management methods ([#74](https://www.github.com/googleapis/python-analytics-admin/issues/74)) ([bdb85be](https://www.github.com/googleapis/python-analytics-admin/commit/bdb85bee0125db8199d6a2a3cf18fbcbd443070b))


### Miscellaneous Chores

* release 0.3.0 ([#75](https://www.github.com/googleapis/python-analytics-admin/issues/75)) ([243b6c5](https://www.github.com/googleapis/python-analytics-admin/commit/243b6c558078bee738b01220384bc04840d59bbe))

## [0.2.0](https://www.github.com/googleapis/python-analytics-admin/compare/v0.1.0...v0.2.0) (2021-01-20)


### ⚠ BREAKING CHANGES

* `update_mask` field is required for all Update operations
* rename `country_code` field to `region_code` in `Account`
* rename `url_query_parameter` field to `uri_query_parameter` in `EnhancedMeasurementSettings`
* remove `parent` field from `GoogleAdsLink`
* remove unused fields from `EnhancedMeasurementSettings` (#29)

### Features

* add ListAccountSummaries ([#20](https://www.github.com/googleapis/python-analytics-admin/issues/20)) ([04d05d7](https://www.github.com/googleapis/python-analytics-admin/commit/04d05d7436a752dba18cb04d0e6882b1670114d7))
* add pagination support for `ListFirebaseLinks` operation ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))


### Bug Fixes

* `update_mask` field is required for all Update operations ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))
* remove `parent` field from `GoogleAdsLink` ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))
* remove unused fields from `EnhancedMeasurementSettings` ([#29](https://www.github.com/googleapis/python-analytics-admin/issues/29)) ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))
* rename `country_code` field to `region_code` in `Account` ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))
* rename `url_query_parameter` field to `uri_query_parameter` in `EnhancedMeasurementSettings` ([bc756a9](https://www.github.com/googleapis/python-analytics-admin/commit/bc756a9566497ab6ff997d26d7fa35c9a6355ecf))


### Documentation

* added a sample ([#9](https://www.github.com/googleapis/python-analytics-admin/issues/9)) ([60918d8](https://www.github.com/googleapis/python-analytics-admin/commit/60918d8896d37f32a19c3d5724611df5cc4d4619))

## 0.1.0 (2020-07-23)


### Features

* generate v1alpha ([496c679](https://www.github.com/googleapis/python-analytics-admin/commit/496c6792dab14ac680e5b80cc7af1de445023715))
