# Changelog

## [0.5.19](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.18...google-cloud-bigquery-data-exchange-v0.5.19) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([3a85796](https://github.com/googleapis/google-cloud-python/commit/3a85796774ebf728cbc9e82dc536316530ac78c1))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))

## [0.5.18](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.17...google-cloud-bigquery-data-exchange-v0.5.18) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.5.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.16...google-cloud-bigquery-data-exchange-v0.5.17) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))
* Add support for reading selective GAPIC generation methods from service YAML ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))

## [0.5.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.15...google-cloud-bigquery-data-exchange-v0.5.16) (2024-12-12)


### Features

* Add support for opt-in debug logging ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))

## [0.5.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.14...google-cloud-bigquery-data-exchange-v0.5.15) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([4ed4108](https://github.com/googleapis/google-cloud-python/commit/4ed41088ab3cbadfe4de7fa170f172666015ed24))

## [0.5.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.13...google-cloud-bigquery-data-exchange-v0.5.14) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13200](https://github.com/googleapis/google-cloud-python/issues/13200)) ([19dc048](https://github.com/googleapis/google-cloud-python/commit/19dc0485852406b90743297bcf257020e6012593))

## [0.5.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.12...google-cloud-bigquery-data-exchange-v0.5.13) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.5.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.11...google-cloud-bigquery-data-exchange-v0.5.12) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.5.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.10...google-cloud-bigquery-data-exchange-v0.5.11) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12382](https://github.com/googleapis/google-cloud-python/issues/12382)) ([d5db265](https://github.com/googleapis/google-cloud-python/commit/d5db2656c011be2264bd778244caf8e23d288c75))

## [0.5.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.9...google-cloud-bigquery-data-exchange-v0.5.10) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12304](https://github.com/googleapis/google-cloud-python/issues/12304)) ([c52e0cd](https://github.com/googleapis/google-cloud-python/commit/c52e0cdbddf44c96f642d8d596c5413c4006ba82))

## [0.5.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.8...google-cloud-bigquery-data-exchange-v0.5.9) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))

## [0.5.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.7...google-cloud-bigquery-data-exchange-v0.5.8) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## [0.5.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.6...google-cloud-bigquery-data-exchange-v0.5.7) (2023-12-07)


### Features

* Add support for python 3.12 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Introduce compatibility with native namespace packages ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Use `retry_async` instead of `retry` in async client ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))

## [0.5.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.5...google-cloud-bigquery-data-exchange-v0.5.6) (2023-09-19)


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## [0.5.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.4...google-cloud-bigquery-data-exchange-v0.5.5) (2023-08-03)


### Documentation

* Minor formatting ([#11543](https://github.com/googleapis/google-cloud-python/issues/11543)) ([8cc031e](https://github.com/googleapis/google-cloud-python/commit/8cc031e723350890b4ceb6e813f24c4bcde3d65f))

## [0.5.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-bigquery-data-exchange-v0.5.3...google-cloud-bigquery-data-exchange-v0.5.4) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## [0.5.3](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.5.2...v0.5.3) (2023-04-13)


### Bug Fixes

* Remove `common` module ([#71](https://github.com/googleapis/python-bigquery-data-exchange/issues/71)) ([3bed959](https://github.com/googleapis/python-bigquery-data-exchange/commit/3bed9598d04e9c67e3ef3208d4ff5ff21b1779f6))

## [0.5.2](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.5.1...v0.5.2) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#69](https://github.com/googleapis/python-bigquery-data-exchange/issues/69)) ([665ebe3](https://github.com/googleapis/python-bigquery-data-exchange/commit/665ebe311308a0ef96ec9604bbee40e2568475ff))

## [0.5.1](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.5.0...v0.5.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([cbd289d](https://github.com/googleapis/python-bigquery-data-exchange/commit/cbd289d84c7b09a5d607b643cd0d09545fd98e81))


### Documentation

* Add documentation for enums ([cbd289d](https://github.com/googleapis/python-bigquery-data-exchange/commit/cbd289d84c7b09a5d607b643cd0d09545fd98e81))

## [0.5.0](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.4.0...v0.5.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#56](https://github.com/googleapis/python-bigquery-data-exchange/issues/56)) ([d261150](https://github.com/googleapis/python-bigquery-data-exchange/commit/d26115028f92a21a2d0dfc201e4d919da1116784))

## [0.4.0](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.3.2...v0.4.0) (2022-12-15)


### Features

* Add support for `google.cloud.bigquery_data_exchange.__version__` ([ca18099](https://github.com/googleapis/python-bigquery-data-exchange/commit/ca180995c0b22c20cb5023943fe6c6e67ddae4ee))
* Add typing to proto.Message based class attributes ([ca18099](https://github.com/googleapis/python-bigquery-data-exchange/commit/ca180995c0b22c20cb5023943fe6c6e67ddae4ee))


### Bug Fixes

* Add dict typing for client_options ([ca18099](https://github.com/googleapis/python-bigquery-data-exchange/commit/ca180995c0b22c20cb5023943fe6c6e67ddae4ee))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([2ded2d4](https://github.com/googleapis/python-bigquery-data-exchange/commit/2ded2d42a678be1af65546639bb1dae5eae19268))
* Drop usage of pkg_resources ([2ded2d4](https://github.com/googleapis/python-bigquery-data-exchange/commit/2ded2d42a678be1af65546639bb1dae5eae19268))
* Fix timeout default values ([2ded2d4](https://github.com/googleapis/python-bigquery-data-exchange/commit/2ded2d42a678be1af65546639bb1dae5eae19268))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([ca18099](https://github.com/googleapis/python-bigquery-data-exchange/commit/ca180995c0b22c20cb5023943fe6c6e67ddae4ee))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([2ded2d4](https://github.com/googleapis/python-bigquery-data-exchange/commit/2ded2d42a678be1af65546639bb1dae5eae19268))

## [0.3.2](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.3.1...v0.3.2) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#45](https://github.com/googleapis/python-bigquery-data-exchange/issues/45)) ([6d2e4d3](https://github.com/googleapis/python-bigquery-data-exchange/commit/6d2e4d3f7a6ff270d7eb6c73687810b5cbd4698f))

## [0.3.1](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.3.0...v0.3.1) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#43](https://github.com/googleapis/python-bigquery-data-exchange/issues/43)) ([f4fefa5](https://github.com/googleapis/python-bigquery-data-exchange/commit/f4fefa5846733f95f255a72112443fdd96244ed9))

## [0.3.0](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.2.1...v0.3.0) (2022-09-01)


### Features

* update BigQuery Analytics Hub API v1beta1 client ([#32](https://github.com/googleapis/python-bigquery-data-exchange/issues/32)) ([7c34320](https://github.com/googleapis/python-bigquery-data-exchange/commit/7c343209613ae0e303d5beb2b9aae526dc9069c8))


### Bug Fixes

* refactor references to Category message ([7c34320](https://github.com/googleapis/python-bigquery-data-exchange/commit/7c343209613ae0e303d5beb2b9aae526dc9069c8))


### Documentation

* improve proto documentation. ([7c34320](https://github.com/googleapis/python-bigquery-data-exchange/commit/7c343209613ae0e303d5beb2b9aae526dc9069c8))

## [0.2.1](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.2.0...v0.2.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#25](https://github.com/googleapis/python-bigquery-data-exchange/issues/25)) ([c3f6f45](https://github.com/googleapis/python-bigquery-data-exchange/commit/c3f6f45f30349066f98d81a00382f392b8d06db2))
* **deps:** require proto-plus >= 1.22.0 ([c3f6f45](https://github.com/googleapis/python-bigquery-data-exchange/commit/c3f6f45f30349066f98d81a00382f392b8d06db2))

## [0.2.0](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.1.1...v0.2.0) (2022-07-20)


### Features

* add audience parameter ([b2417eb](https://github.com/googleapis/python-bigquery-data-exchange/commit/b2417ebd2bf972c8984520b60ba68937254b3846))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#17](https://github.com/googleapis/python-bigquery-data-exchange/issues/17)) ([b2417eb](https://github.com/googleapis/python-bigquery-data-exchange/commit/b2417ebd2bf972c8984520b60ba68937254b3846))
* require python 3.7+ ([#19](https://github.com/googleapis/python-bigquery-data-exchange/issues/19)) ([938be32](https://github.com/googleapis/python-bigquery-data-exchange/commit/938be32fb56bc661d7f8e2a64a5dd4d3dc03c69b))

## [0.1.1](https://github.com/googleapis/python-bigquery-data-exchange/compare/v0.1.0...v0.1.1) (2022-06-07)


### Bug Fixes

* **deps:** require protobuf>=3.19.0,<4.0.0 ([#11](https://github.com/googleapis/python-bigquery-data-exchange/issues/11)) ([aae9d7b](https://github.com/googleapis/python-bigquery-data-exchange/commit/aae9d7b91a13a559f1d72f5f19ecef7950330818))

## 0.1.0 (2022-04-15)


### Features

* generate v1beta1 ([e48b946](https://github.com/googleapis/python-bigquery-data-exchange/commit/e48b9469e8a49123c56a3c6488bf5f682365dc4d))
