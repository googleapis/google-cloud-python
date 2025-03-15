# Changelog

## [0.4.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.13...google-cloud-bigquery-biglake-v0.4.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([3a85796](https://github.com/googleapis/google-cloud-python/commit/3a85796774ebf728cbc9e82dc536316530ac78c1))

## [0.4.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.12...google-cloud-bigquery-biglake-v0.4.13) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))
* Add support for reading selective GAPIC generation methods from service YAML ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))

## [0.4.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.11...google-cloud-bigquery-biglake-v0.4.12) (2024-12-12)


### Features

* Add support for opt-in debug logging ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))

## [0.4.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.10...google-cloud-bigquery-biglake-v0.4.11) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([4ed4108](https://github.com/googleapis/google-cloud-python/commit/4ed41088ab3cbadfe4de7fa170f172666015ed24))

## [0.4.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.9...google-cloud-bigquery-biglake-v0.4.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13200](https://github.com/googleapis/google-cloud-python/issues/13200)) ([19dc048](https://github.com/googleapis/google-cloud-python/commit/19dc0485852406b90743297bcf257020e6012593))

## [0.4.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.8...google-cloud-bigquery-biglake-v0.4.9) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.4.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.7...google-cloud-bigquery-biglake-v0.4.8) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.4.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.6...google-cloud-bigquery-biglake-v0.4.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12382](https://github.com/googleapis/google-cloud-python/issues/12382)) ([d5db265](https://github.com/googleapis/google-cloud-python/commit/d5db2656c011be2264bd778244caf8e23d288c75))

## [0.4.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.5...google-cloud-bigquery-biglake-v0.4.6) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12304](https://github.com/googleapis/google-cloud-python/issues/12304)) ([c52e0cd](https://github.com/googleapis/google-cloud-python/commit/c52e0cdbddf44c96f642d8d596c5413c4006ba82))

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.4...google-cloud-bigquery-biglake-v0.4.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.3...google-cloud-bigquery-biglake-v0.4.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.2...google-cloud-bigquery-biglake-v0.4.3) (2023-12-07)


### Features

* Add support for python 3.12 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Introduce compatibility with native namespace packages ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Use `retry_async` instead of `retry` in async client ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))

## [0.4.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.1...google-cloud-bigquery-biglake-v0.4.2) (2023-09-19)


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## [0.4.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.4.0...google-cloud-bigquery-biglake-v0.4.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.3.0...google-cloud-bigquery-biglake-v0.4.0) (2023-06-19)


### Bug Fixes

* Use `google.cloud.bigquery_biglake` to avoid conflict with `google.cloud.bigquery` ([20f83e0](https://github.com/googleapis/google-cloud-python/commit/20f83e0e374d8cb6bb315336c928aa9a964e3f15))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.2.0...google-cloud-bigquery-biglake-v0.3.0) (2023-04-12)


### Features

* add BigQuery BigLake v1 API ([02e6b75](https://github.com/googleapis/google-cloud-python/commit/02e6b7504844110a3d9967fa77908a844a026e1f))
* set BigQuery BigLake v1 as the default import ([02e6b75](https://github.com/googleapis/google-cloud-python/commit/02e6b7504844110a3d9967fa77908a844a026e1f))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.1.1...google-cloud-bigquery-biglake-v0.2.0) (2023-04-06)


### Features

* add RenameTable, etag, and ListTables view ([#11050](https://github.com/googleapis/google-cloud-python/issues/11050)) ([b791900](https://github.com/googleapis/google-cloud-python/commit/b7919001ccd7773307b806b5fff68166352e01b2))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-biglake-v0.1.0...google-cloud-bigquery-biglake-v0.1.1) (2023-03-25)


### Documentation

* Fix formatting of request arg in docstring ([#10867](https://github.com/googleapis/google-cloud-python/issues/10867)) ([d34a425](https://github.com/googleapis/google-cloud-python/commit/d34a425f7d0f02bebaf20d24b725b8c25c699697))

## 0.1.0 (2023-03-17)


### Features

* add initial files for google.cloud.bigquery.biglake.v1alpha1 ([#10861](https://github.com/googleapis/google-cloud-python/issues/10861)) ([06db74d](https://github.com/googleapis/google-cloud-python/commit/06db74d8af7cb3de73e981996d851f3bf68946a8))

## Changelog
