# Changelog

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
