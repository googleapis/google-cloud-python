# Changelog

## [0.6.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.16...google-cloud-apigee-registry-v0.6.17) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))

## [0.6.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.15...google-cloud-apigee-registry-v0.6.16) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.6.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.14...google-cloud-apigee-registry-v0.6.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.6.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.13...google-cloud-apigee-registry-v0.6.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))

## [0.6.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.12...google-cloud-apigee-registry-v0.6.13) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.6.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.11...google-cloud-apigee-registry-v0.6.12) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.6.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.10...google-cloud-apigee-registry-v0.6.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.6.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.9...google-cloud-apigee-registry-v0.6.10) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))

## [0.6.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.8...google-cloud-apigee-registry-v0.6.9) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12381](https://github.com/googleapis/google-cloud-python/issues/12381)) ([48ae8ab](https://github.com/googleapis/google-cloud-python/commit/48ae8aba7ec71a382e001b3a659022f942c3b436))

## [0.6.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.7...google-cloud-apigee-registry-v0.6.8) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12280](https://github.com/googleapis/google-cloud-python/issues/12280)) ([2d75d0e](https://github.com/googleapis/google-cloud-python/commit/2d75d0e67ca4cccddc688bd37c14ac80564a2e65))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12303](https://github.com/googleapis/google-cloud-python/issues/12303)) ([fbb80c3](https://github.com/googleapis/google-cloud-python/commit/fbb80c32f7db91e25bd1cc30966f630728ff6d6a))

## [0.6.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.6...google-cloud-apigee-registry-v0.6.7) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))

## [0.6.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.5...google-cloud-apigee-registry-v0.6.6) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([a0392ee](https://github.com/googleapis/google-cloud-python/commit/a0392eeb59fcc6ea7c55283110b92aa24a4d40a0))

## [0.6.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.4...google-cloud-apigee-registry-v0.6.5) (2023-12-07)


### Features

* Add support for python 3.12 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Introduce compatibility with native namespace packages ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Use `retry_async` instead of `retry` in async client ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))

## [0.6.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.3...google-cloud-apigee-registry-v0.6.4) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.6.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-apigee-registry-v0.6.2...google-cloud-apigee-registry-v0.6.3) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.6.2](https://github.com/googleapis/python-apigee-registry/compare/v0.6.1...v0.6.2) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#74](https://github.com/googleapis/python-apigee-registry/issues/74)) ([6edd830](https://github.com/googleapis/python-apigee-registry/commit/6edd830cf67736a19a31ceb6a5d9867777bf27c3))

## [0.6.1](https://github.com/googleapis/python-apigee-registry/compare/v0.6.0...v0.6.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([7cad108](https://github.com/googleapis/python-apigee-registry/commit/7cad1083fa938ef0f4ab3fc75bd7a4e99fb572b3))


### Documentation

* Add documentation for enums ([7cad108](https://github.com/googleapis/python-apigee-registry/commit/7cad1083fa938ef0f4ab3fc75bd7a4e99fb572b3))

## [0.6.0](https://github.com/googleapis/python-apigee-registry/compare/v0.5.1...v0.6.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#61](https://github.com/googleapis/python-apigee-registry/issues/61)) ([25fd09a](https://github.com/googleapis/python-apigee-registry/commit/25fd09ad4040abbee1f5c49b19806fab33a1b849))

## [0.5.1](https://github.com/googleapis/python-apigee-registry/compare/v0.5.0...v0.5.1) (2022-12-14)


### Bug Fixes

* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([f1fd8d9](https://github.com/googleapis/python-apigee-registry/commit/f1fd8d9ee3920f4e9e68e2a8000dee98db2b95ac))
* Drop usage of pkg_resources ([f1fd8d9](https://github.com/googleapis/python-apigee-registry/commit/f1fd8d9ee3920f4e9e68e2a8000dee98db2b95ac))
* Fix timeout default values ([f1fd8d9](https://github.com/googleapis/python-apigee-registry/commit/f1fd8d9ee3920f4e9e68e2a8000dee98db2b95ac))


### Documentation

* **samples:** Snippetgen should call await on the operation coroutine before calling result ([f1fd8d9](https://github.com/googleapis/python-apigee-registry/commit/f1fd8d9ee3920f4e9e68e2a8000dee98db2b95ac))

## [0.5.0](https://github.com/googleapis/python-apigee-registry/compare/v0.4.0...v0.5.0) (2022-11-16)


### Features

* Add typing to proto.Message based class attributes ([27dfa13](https://github.com/googleapis/python-apigee-registry/commit/27dfa13adb20d6f39612113effa483c4e1aa8142))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([27dfa13](https://github.com/googleapis/python-apigee-registry/commit/27dfa13adb20d6f39612113effa483c4e1aa8142))

## [0.4.0](https://github.com/googleapis/python-apigee-registry/compare/v0.3.2...v0.4.0) (2022-11-08)


### Features

* add support for `google.cloud.apigee_registry.__version__` ([1fd5915](https://github.com/googleapis/python-apigee-registry/commit/1fd59157f3fb26022451aa5d395f1a99c91c63c3))


### Bug Fixes

* Add dict typing for client_options ([1fd5915](https://github.com/googleapis/python-apigee-registry/commit/1fd59157f3fb26022451aa5d395f1a99c91c63c3))

## [0.3.2](https://github.com/googleapis/python-apigee-registry/compare/v0.3.1...v0.3.2) (2022-10-10)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#42](https://github.com/googleapis/python-apigee-registry/issues/42)) ([d3a30ab](https://github.com/googleapis/python-apigee-registry/commit/d3a30abbca1f51b0312983132063387a55b0f8d6))
* **deps:** require google-api-core&gt;=1.33.2 ([d3a30ab](https://github.com/googleapis/python-apigee-registry/commit/d3a30abbca1f51b0312983132063387a55b0f8d6))

## [0.3.1](https://github.com/googleapis/python-apigee-registry/compare/v0.3.0...v0.3.1) (2022-09-30)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#39](https://github.com/googleapis/python-apigee-registry/issues/39)) ([e9b08c2](https://github.com/googleapis/python-apigee-registry/commit/e9b08c20a8a4424dee0e624a9207e84c9f2dfddf))

## [0.3.0](https://github.com/googleapis/python-apigee-registry/compare/v0.2.1...v0.3.0) (2022-09-16)


### Features

* Add support for REST transport ([#30](https://github.com/googleapis/python-apigee-registry/issues/30)) ([268c41c](https://github.com/googleapis/python-apigee-registry/commit/268c41c5eff4b5453c27fa1e043d32f970b667cf))


### Bug Fixes

* **deps:** require google-api-core>=1.33.1,>=2.8.0 ([268c41c](https://github.com/googleapis/python-apigee-registry/commit/268c41c5eff4b5453c27fa1e043d32f970b667cf))
* **deps:** require protobuf >= 3.20.1 ([268c41c](https://github.com/googleapis/python-apigee-registry/commit/268c41c5eff4b5453c27fa1e043d32f970b667cf))

## [0.2.1](https://github.com/googleapis/python-apigee-registry/compare/v0.2.0...v0.2.1) (2022-09-01)


### Bug Fixes

* Additional error codes added to service configuration for retry ([#22](https://github.com/googleapis/python-apigee-registry/issues/22)) ([72e8d3e](https://github.com/googleapis/python-apigee-registry/commit/72e8d3e2d1f48e8347b68aa4a281a504246a5d1e))

## [0.2.0](https://github.com/googleapis/python-apigee-registry/compare/v0.1.2...v0.2.0) (2022-08-21)


### Features

* added support for `force` field for API and API version deletion ([#14](https://github.com/googleapis/python-apigee-registry/issues/14)) ([9ba15f0](https://github.com/googleapis/python-apigee-registry/commit/9ba15f019f49c920b98b62ef4bd930f28703f316))

## [0.1.2](https://github.com/googleapis/python-apigee-registry/compare/v0.1.1...v0.1.2) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#11](https://github.com/googleapis/python-apigee-registry/issues/11)) ([5e5a1b0](https://github.com/googleapis/python-apigee-registry/commit/5e5a1b07059588758b43ab7fcafdff8c1175e8da))
* **deps:** require proto-plus >= 1.22.0 ([5e5a1b0](https://github.com/googleapis/python-apigee-registry/commit/5e5a1b07059588758b43ab7fcafdff8c1175e8da))

## [0.1.1](https://github.com/googleapis/python-apigee-registry/compare/v0.1.0...v0.1.1) (2022-07-18)


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([6cafce7](https://github.com/googleapis/python-apigee-registry/commit/6cafce783dc2266f7f34577a331e304c94dc6d5e))

## 0.1.0 (2022-07-08)


### Features

* generate v1 ([7bf7420](https://github.com/googleapis/python-apigee-registry/commit/7bf742007d11014a705bfe1a3ca346fb35ca34b6))
