# Changelog

## [1.9.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.5...google-cloud-resource-settings-v1.9.6) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([42c4d04](https://github.com/googleapis/google-cloud-python/commit/42c4d04ee1362ba0ed0f1b6a134ac8e409875b63))

## [1.9.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.4...google-cloud-resource-settings-v1.9.5) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12869](https://github.com/googleapis/google-cloud-python/issues/12869)) ([e42edbc](https://github.com/googleapis/google-cloud-python/commit/e42edbcf7f4d8ed66b6645c96a01c55fb8cd7666))

## [1.9.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.3...google-cloud-resource-settings-v1.9.4) (2024-06-05)


### Documentation

* [google-cloud-resource-settings] Resource Settings is deprecated. As of November 7, 2023, no organizations will be onboarded for any of the enabled settings, and the service will be shut down on October 1, 2024 ([#12766](https://github.com/googleapis/google-cloud-python/issues/12766)) ([d2a2825](https://github.com/googleapis/google-cloud-python/commit/d2a282512c457c5b348aeef118b6ea7df5a2bb6f))

## [1.9.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.2...google-cloud-resource-settings-v1.9.3) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12387](https://github.com/googleapis/google-cloud-python/issues/12387)) ([12ce658](https://github.com/googleapis/google-cloud-python/commit/12ce658210f148eb93d9ff501568fb6f88e77f18))

## [1.9.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.1...google-cloud-resource-settings-v1.9.2) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([89c1b05](https://github.com/googleapis/google-cloud-python/commit/89c1b054f321b90ab4eed0139a3a2a79c369730d))

## [1.9.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.9.0...google-cloud-resource-settings-v1.9.1) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))

## [1.9.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.8.0...google-cloud-resource-settings-v1.9.0) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([4368029](https://github.com/googleapis/google-cloud-python/commit/436802904bfdafa7e90f94b128813506525e1605))

## [1.8.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.7.2...google-cloud-resource-settings-v1.8.0) (2023-12-07)


### Features

* Add support for python 3.12 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Introduce compatibility with native namespace packages ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Use `retry_async` instead of `retry` in async client ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))

## [1.7.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.7.1...google-cloud-resource-settings-v1.7.2) (2023-09-19)


### Documentation

* Minor formatting ([025219f](https://github.com/googleapis/google-cloud-python/commit/025219f5c04803651e20eae4c0186b87608f4db4))

## [1.7.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-resource-settings-v1.7.0...google-cloud-resource-settings-v1.7.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11448](https://github.com/googleapis/google-cloud-python/issues/11448)) ([4d2c35a](https://github.com/googleapis/google-cloud-python/commit/4d2c35a1cd0b68b6d481d5611ff820451273e859))

## [1.7.0](https://github.com/googleapis/python-resource-settings/compare/v1.6.1...v1.7.0) (2023-02-16)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#161](https://github.com/googleapis/python-resource-settings/issues/161)) ([6a98eb5](https://github.com/googleapis/python-resource-settings/commit/6a98eb582064c411324eb1c11e6da8e33bb14057))

## [1.6.1](https://github.com/googleapis/python-resource-settings/compare/v1.6.0...v1.6.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([1fa8c69](https://github.com/googleapis/python-resource-settings/commit/1fa8c6972f2e450e6f33d2dfe3114fb8dceca688))


### Documentation

* Add documentation for enums ([1fa8c69](https://github.com/googleapis/python-resource-settings/commit/1fa8c6972f2e450e6f33d2dfe3114fb8dceca688))

## [1.6.0](https://github.com/googleapis/python-resource-settings/compare/v1.5.0...v1.6.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#153](https://github.com/googleapis/python-resource-settings/issues/153)) ([d3e4eab](https://github.com/googleapis/python-resource-settings/commit/d3e4eab972c05e17a0a7a8b7aec289529c237b86))

## [1.5.0](https://github.com/googleapis/python-resource-settings/compare/v1.4.3...v1.5.0) (2022-12-14)


### Features

* Add support for `google.cloud.resourcesettings.__version__` ([24d1f71](https://github.com/googleapis/python-resource-settings/commit/24d1f71570281c23a995d90aae23b312ac91c4dd))
* Add typing to proto.Message based class attributes ([24d1f71](https://github.com/googleapis/python-resource-settings/commit/24d1f71570281c23a995d90aae23b312ac91c4dd))


### Bug Fixes

* Add dict typing for client_options ([24d1f71](https://github.com/googleapis/python-resource-settings/commit/24d1f71570281c23a995d90aae23b312ac91c4dd))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([78343a3](https://github.com/googleapis/python-resource-settings/commit/78343a3722e4a7c58af6fed867eeabde77b2717f))
* Drop usage of pkg_resources ([78343a3](https://github.com/googleapis/python-resource-settings/commit/78343a3722e4a7c58af6fed867eeabde77b2717f))
* Fix timeout default values ([78343a3](https://github.com/googleapis/python-resource-settings/commit/78343a3722e4a7c58af6fed867eeabde77b2717f))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([24d1f71](https://github.com/googleapis/python-resource-settings/commit/24d1f71570281c23a995d90aae23b312ac91c4dd))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([78343a3](https://github.com/googleapis/python-resource-settings/commit/78343a3722e4a7c58af6fed867eeabde77b2717f))

## [1.4.3](https://github.com/googleapis/python-resource-settings/compare/v1.4.2...v1.4.3) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#143](https://github.com/googleapis/python-resource-settings/issues/143)) ([b253cf5](https://github.com/googleapis/python-resource-settings/commit/b253cf5723a8fe5a43b350bb1d177bea34a7084a))

## [1.4.2](https://github.com/googleapis/python-resource-settings/compare/v1.4.1...v1.4.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#141](https://github.com/googleapis/python-resource-settings/issues/141)) ([9dc66a3](https://github.com/googleapis/python-resource-settings/commit/9dc66a3539283e141b8e606e91c1b28348149454))

## [1.4.1](https://github.com/googleapis/python-resource-settings/compare/v1.4.0...v1.4.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#127](https://github.com/googleapis/python-resource-settings/issues/127)) ([6455479](https://github.com/googleapis/python-resource-settings/commit/6455479446b23a0d34fe2345973efa5e876b5e06))
* **deps:** require proto-plus >= 1.22.0 ([6455479](https://github.com/googleapis/python-resource-settings/commit/6455479446b23a0d34fe2345973efa5e876b5e06))

## [1.4.0](https://github.com/googleapis/python-resource-settings/compare/v1.3.2...v1.4.0) (2022-07-16)


### Features

* add audience parameter ([0853e60](https://github.com/googleapis/python-resource-settings/commit/0853e60f4d60db073bfcd8911a840fc44211a86a))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#122](https://github.com/googleapis/python-resource-settings/issues/122)) ([e42d52a](https://github.com/googleapis/python-resource-settings/commit/e42d52ad28b7faa944496b408411777352fd111d))
* require python 3.7+ ([#120](https://github.com/googleapis/python-resource-settings/issues/120)) ([b0e5b16](https://github.com/googleapis/python-resource-settings/commit/b0e5b16d8c890c58c803de54079c53c4cdf8a47b))

## [1.3.2](https://github.com/googleapis/python-resource-settings/compare/v1.3.1...v1.3.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#110](https://github.com/googleapis/python-resource-settings/issues/110)) ([ea71f0f](https://github.com/googleapis/python-resource-settings/commit/ea71f0f039fc23e113d45d919a5841498e7d31de))


### Documentation

* fix changelog header to consistent size ([#111](https://github.com/googleapis/python-resource-settings/issues/111)) ([a1dad10](https://github.com/googleapis/python-resource-settings/commit/a1dad1003f17f533a3e8290f7a15d37b5e799547))

## [1.3.1](https://github.com/googleapis/python-resource-settings/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#89](https://github.com/googleapis/python-resource-settings/issues/89)) ([ba70731](https://github.com/googleapis/python-resource-settings/commit/ba707319f31bf65f3e120d144260b0d5d3aa742f))

## [1.3.0](https://github.com/googleapis/python-resource-settings/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#74](https://github.com/googleapis/python-resource-settings/issues/74)) ([4059c1c](https://github.com/googleapis/python-resource-settings/commit/4059c1c704803e60a7341b483ead53defa8ac39a))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([26211ca](https://github.com/googleapis/python-resource-settings/commit/26211cab0ffad79a7049b9819eba89bbc7ea2998))

## [1.2.1](https://www.github.com/googleapis/python-resource-settings/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([89c426a](https://www.github.com/googleapis/python-resource-settings/commit/89c426a76cc41c4793040cfa90daafd2bfcf75e4))
* **deps:** require google-api-core >= 1.28.0 ([89c426a](https://www.github.com/googleapis/python-resource-settings/commit/89c426a76cc41c4793040cfa90daafd2bfcf75e4))


### Documentation

* list oneofs in docstring ([89c426a](https://www.github.com/googleapis/python-resource-settings/commit/89c426a76cc41c4793040cfa90daafd2bfcf75e4))

## [1.2.0](https://www.github.com/googleapis/python-resource-settings/compare/v1.1.0...v1.2.0) (2021-10-15)


### Features

* add support for python 3.10 ([#53](https://www.github.com/googleapis/python-resource-settings/issues/53)) ([5aaa186](https://www.github.com/googleapis/python-resource-settings/commit/5aaa186d890b6b26db40f9e4390ad76e5c62e3b5))

## [1.1.0](https://www.github.com/googleapis/python-resource-settings/compare/v1.0.2...v1.1.0) (2021-10-07)


### Features

* add context manager support in client ([#49](https://www.github.com/googleapis/python-resource-settings/issues/49)) ([91201e0](https://www.github.com/googleapis/python-resource-settings/commit/91201e09bed298a96fa9e4223d454f5ac4336441))

## [1.0.2](https://www.github.com/googleapis/python-resource-settings/compare/v1.0.1...v1.0.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([801dfba](https://www.github.com/googleapis/python-resource-settings/commit/801dfba9f736136df4d8d976f6f460656bc56cd6))

## [1.0.1](https://www.github.com/googleapis/python-resource-settings/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([88a867a](https://www.github.com/googleapis/python-resource-settings/commit/88a867a1ee67ae23e2ba27f85296f494c0581c52))

## [1.0.0](https://www.github.com/googleapis/python-resource-settings/compare/v0.3.2...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#27](https://www.github.com/googleapis/python-resource-settings/issues/27)) ([ea55c97](https://www.github.com/googleapis/python-resource-settings/commit/ea55c97e88fc4222d0287d989c96f8f30426ce95))

## [0.3.2](https://www.github.com/googleapis/python-resource-settings/compare/v0.3.1...v0.3.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#23](https://www.github.com/googleapis/python-resource-settings/issues/23)) ([1d2ebf9](https://www.github.com/googleapis/python-resource-settings/commit/1d2ebf9dd19a748abc6b60944d5a4b58c22bb33e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#19](https://www.github.com/googleapis/python-resource-settings/issues/19)) ([a61c2b5](https://www.github.com/googleapis/python-resource-settings/commit/a61c2b54ccdf282dcdb227805c1da8b9b46e885c))


### Miscellaneous Chores

* release as 0.3.2 ([#24](https://www.github.com/googleapis/python-resource-settings/issues/24)) ([c0252c4](https://www.github.com/googleapis/python-resource-settings/commit/c0252c43471cf6d5c7abe62fced88121cda28c1b))

## [0.3.1](https://www.github.com/googleapis/python-resource-settings/compare/v0.3.0...v0.3.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#18](https://www.github.com/googleapis/python-resource-settings/issues/18)) ([2ea4dd4](https://www.github.com/googleapis/python-resource-settings/commit/2ea4dd42a6c8b2420a1819193bfd8d0941efe8e2))

## [0.3.0](https://www.github.com/googleapis/python-resource-settings/compare/v0.2.0...v0.3.0) (2021-07-16)


### Features

* Set retry and timeout values for Cloud ResourceSettings v1 API ([#15](https://www.github.com/googleapis/python-resource-settings/issues/15)) ([0d127ea](https://www.github.com/googleapis/python-resource-settings/commit/0d127ea2ff9288c3dc2e335d6c2dc4398842ca2d))


### Bug Fixes

* disable always_use_jwt_access ([3a2782a](https://www.github.com/googleapis/python-resource-settings/commit/3a2782aad33ab253197c4a54d04d4beae8c48c75))
* disable always_use_jwt_access ([#11](https://www.github.com/googleapis/python-resource-settings/issues/11)) ([3a2782a](https://www.github.com/googleapis/python-resource-settings/commit/3a2782aad33ab253197c4a54d04d4beae8c48c75))

## [0.2.0](https://www.github.com/googleapis/python-resource-settings/compare/v0.1.0...v0.2.0) (2021-06-22)


### Features

* add `always_use_jwt_access` ([#7](https://www.github.com/googleapis/python-resource-settings/issues/7)) ([320d9fb](https://www.github.com/googleapis/python-resource-settings/commit/320d9fbb818fbaeccbe93a6c0e46b2c278a266b8))

## 0.1.0 (2021-06-01)


### Features

* generate v1 ([137045d](https://www.github.com/googleapis/python-resource-settings/commit/137045d0937b6162cd81aed35db50172c6bc8876))
