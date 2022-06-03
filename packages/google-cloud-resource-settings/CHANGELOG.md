# Changelog

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
