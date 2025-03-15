# Changelog

## [0.4.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.16...google-cloud-beyondcorp-clientconnectorservices-v0.4.17) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([3a85796](https://github.com/googleapis/google-cloud-python/commit/3a85796774ebf728cbc9e82dc536316530ac78c1))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))

## [0.4.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.15...google-cloud-beyondcorp-clientconnectorservices-v0.4.16) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.4.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.14...google-cloud-beyondcorp-clientconnectorservices-v0.4.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))
* Add support for reading selective GAPIC generation methods from service YAML ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))

## [0.4.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.13...google-cloud-beyondcorp-clientconnectorservices-v0.4.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))

## [0.4.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.12...google-cloud-beyondcorp-clientconnectorservices-v0.4.13) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([4ed4108](https://github.com/googleapis/google-cloud-python/commit/4ed41088ab3cbadfe4de7fa170f172666015ed24))

## [0.4.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.11...google-cloud-beyondcorp-clientconnectorservices-v0.4.12) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13200](https://github.com/googleapis/google-cloud-python/issues/13200)) ([19dc048](https://github.com/googleapis/google-cloud-python/commit/19dc0485852406b90743297bcf257020e6012593))

## [0.4.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.10...google-cloud-beyondcorp-clientconnectorservices-v0.4.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.4.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.9...google-cloud-beyondcorp-clientconnectorservices-v0.4.10) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.4.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.8...google-cloud-beyondcorp-clientconnectorservices-v0.4.9) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12382](https://github.com/googleapis/google-cloud-python/issues/12382)) ([d5db265](https://github.com/googleapis/google-cloud-python/commit/d5db2656c011be2264bd778244caf8e23d288c75))

## [0.4.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.7...google-cloud-beyondcorp-clientconnectorservices-v0.4.8) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12304](https://github.com/googleapis/google-cloud-python/issues/12304)) ([c52e0cd](https://github.com/googleapis/google-cloud-python/commit/c52e0cdbddf44c96f642d8d596c5413c4006ba82))

## [0.4.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.6...google-cloud-beyondcorp-clientconnectorservices-v0.4.7) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))

## [0.4.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.5...google-cloud-beyondcorp-clientconnectorservices-v0.4.6) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.4...google-cloud-beyondcorp-clientconnectorservices-v0.4.5) (2023-12-07)


### Features

* Add support for python 3.12 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Introduce compatibility with native namespace packages ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Use `retry_async` instead of `retry` in async client ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.3...google-cloud-beyondcorp-clientconnectorservices-v0.4.4) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientconnectorservices-v0.4.2...google-cloud-beyondcorp-clientconnectorservices-v0.4.3) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.4.2](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.4.1...v0.4.2) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#58](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/58)) ([f478e9e](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/f478e9e9406b1988f68fd1a8bed7b489c9614c40))

## [0.4.1](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.4.0...v0.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([8f3da00](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/8f3da0061a5c1b23bf5a2c0f1d723cf51fb67ba0))


### Documentation

* Add documentation for enums ([8f3da00](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/8f3da0061a5c1b23bf5a2c0f1d723cf51fb67ba0))

## [0.4.0](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.3.0...v0.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#46](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/46)) ([41bed78](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/41bed7878e81cacd1a8b73ad909c641f9cbdaeb1))

## [0.3.0](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.2.2...v0.3.0) (2022-12-14)


### Features

* Add support for `google.cloud.beyondcorp_clientconnectorservices.__version__` ([96d425c](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/96d425cdcbe6a72636b97d9da5418fee465614a9))
* Add typing to proto.Message based class attributes ([96d425c](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/96d425cdcbe6a72636b97d9da5418fee465614a9))


### Bug Fixes

* Add dict typing for client_options ([96d425c](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/96d425cdcbe6a72636b97d9da5418fee465614a9))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([f044545](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/f044545059fd9db57ce9512d9dda00069cad74ef))
* Drop usage of pkg_resources ([f044545](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/f044545059fd9db57ce9512d9dda00069cad74ef))
* Fix timeout default values ([f044545](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/f044545059fd9db57ce9512d9dda00069cad74ef))


### Documentation

* Fix minor docstring formatting ([96d425c](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/96d425cdcbe6a72636b97d9da5418fee465614a9))
* **samples:** Snippetgen handling of repeated enum field ([96d425c](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/96d425cdcbe6a72636b97d9da5418fee465614a9))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([f044545](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/f044545059fd9db57ce9512d9dda00069cad74ef))

## [0.2.2](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.2.1...v0.2.2) (2022-10-10)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#32](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/32)) ([2d5853a](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/2d5853ad56ea54d92aa720c7503c2b75a2bbc067))
* **deps:** require google-api-core&gt;=1.33.2 ([2d5853a](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/2d5853ad56ea54d92aa720c7503c2b75a2bbc067))

## [0.2.1](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.2.0...v0.2.1) (2022-10-03)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#29](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/29)) ([78a1015](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/78a1015b7a8cfa8aa29c640f5b48e57c9431644a))

## [0.2.0](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.1.1...v0.2.0) (2022-09-16)


### Features

* Add support for REST transport ([#24](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/24)) ([13d7217](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/13d7217b27d917e8fe7b07a4928146ab1cb9bc5c))


### Bug Fixes

* **deps:** require google-api-core>=1.33.1,>=2.8.0 ([13d7217](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/13d7217b27d917e8fe7b07a4928146ab1cb9bc5c))
* **deps:** require protobuf >= 3.20.1 ([13d7217](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/13d7217b27d917e8fe7b07a4928146ab1cb9bc5c))

## [0.1.1](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/compare/v0.1.0...v0.1.1) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#10](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/issues/10)) ([2a66542](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/2a66542bbd1cd282a874fb9e242546865200e31d))
* **deps:** require proto-plus >= 1.22.0 ([2a66542](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/2a66542bbd1cd282a874fb9e242546865200e31d))

## 0.1.0 (2022-07-20)


### Features

* generate v1 ([07a48b0](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/07a48b037cbf76f1b06371223dded295ab9c24b6))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([7c02a8e](https://github.com/googleapis/python-beyondcorp-clientconnectorservices/commit/7c02a8ea57e48946878a418f5c44b43a6f0f97a9))
