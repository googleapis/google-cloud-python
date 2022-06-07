# Changelog

## [1.4.2](https://github.com/googleapis/python-managed-identities/compare/v1.4.1...v1.4.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#146](https://github.com/googleapis/python-managed-identities/issues/146)) ([fb8eaf8](https://github.com/googleapis/python-managed-identities/commit/fb8eaf8ee5f16bffeb4335fd52134a313c98eef9))


### Documentation

* fix changelog header to consistent size ([#145](https://github.com/googleapis/python-managed-identities/issues/145)) ([5549f26](https://github.com/googleapis/python-managed-identities/commit/5549f264cce65c9ff59e859690ee76f1a96c2c05))

## [1.4.1](https://github.com/googleapis/python-managed-identities/compare/v1.4.0...v1.4.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#118](https://github.com/googleapis/python-managed-identities/issues/118)) ([72e501f](https://github.com/googleapis/python-managed-identities/commit/72e501f2739087c5f43e631608a0bdb4c2222c87))
* **deps:** require proto-plus>=1.15.0 ([72e501f](https://github.com/googleapis/python-managed-identities/commit/72e501f2739087c5f43e631608a0bdb4c2222c87))

## [1.4.0](https://github.com/googleapis/python-managed-identities/compare/v1.3.1...v1.4.0) (2022-02-26)


### Features

* add api key support ([#103](https://github.com/googleapis/python-managed-identities/issues/103)) ([91b316a](https://github.com/googleapis/python-managed-identities/commit/91b316a5da34c8ecec852d811c2e7a9bd5254379))


### Bug Fixes

* **deps:** remove unused dependency libcst ([#109](https://github.com/googleapis/python-managed-identities/issues/109)) ([8d92706](https://github.com/googleapis/python-managed-identities/commit/8d9270668ae4f9ee090d84559e45f6ba4d1756eb))
* resolve DuplicateCredentialArgs error when using credentials_file ([ed0bec5](https://github.com/googleapis/python-managed-identities/commit/ed0bec5588b9e0809d37e7902a375ce776ecdfc5))

## [1.3.1](https://www.github.com/googleapis/python-managed-identities/compare/v1.3.0...v1.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([0e325ae](https://www.github.com/googleapis/python-managed-identities/commit/0e325ae6f338fed1d7f815a4ecda87a9c9998412))
* **deps:** require google-api-core >= 1.28.0 ([0e325ae](https://www.github.com/googleapis/python-managed-identities/commit/0e325ae6f338fed1d7f815a4ecda87a9c9998412))


### Documentation

* list oneofs in docstring ([0e325ae](https://www.github.com/googleapis/python-managed-identities/commit/0e325ae6f338fed1d7f815a4ecda87a9c9998412))

## [1.3.0](https://www.github.com/googleapis/python-managed-identities/compare/v1.2.0...v1.3.0) (2021-10-21)


### Features

* add support for python 3.10 ([#82](https://www.github.com/googleapis/python-managed-identities/issues/82)) ([c17da66](https://www.github.com/googleapis/python-managed-identities/commit/c17da66423d67daca0166289f033dfecba09a5bf))

## [1.2.0](https://www.github.com/googleapis/python-managed-identities/compare/v1.1.3...v1.2.0) (2021-10-08)


### Features

* add context manager support in client ([#78](https://www.github.com/googleapis/python-managed-identities/issues/78)) ([9cad312](https://www.github.com/googleapis/python-managed-identities/commit/9cad312b3673009f8bcd6b51c8a24fe5dda468f0))

## [1.1.3](https://www.github.com/googleapis/python-managed-identities/compare/v1.1.2...v1.1.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([4d42021](https://www.github.com/googleapis/python-managed-identities/commit/4d4202106eb7ed5af809a96f823e4b8067709f6e))

## [1.1.2](https://www.github.com/googleapis/python-managed-identities/compare/v1.1.1...v1.1.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([9da978a](https://www.github.com/googleapis/python-managed-identities/commit/9da978af7a5e95cbc6edae861978ed492797a0c9))

## [1.1.1](https://www.github.com/googleapis/python-managed-identities/compare/v1.1.0...v1.1.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#51](https://www.github.com/googleapis/python-managed-identities/issues/51)) ([43e3ce1](https://www.github.com/googleapis/python-managed-identities/commit/43e3ce1df7c59f9d33d1afeb4e440ae8103dfb4b))
* enable self signed jwt for grpc ([#57](https://www.github.com/googleapis/python-managed-identities/issues/57)) ([d79eaa7](https://www.github.com/googleapis/python-managed-identities/commit/d79eaa732ea33f601cb5f9a37b2f788e6f3fd9f2))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#52](https://www.github.com/googleapis/python-managed-identities/issues/52)) ([a3e352c](https://www.github.com/googleapis/python-managed-identities/commit/a3e352c80a3e2984d0c767ec32d08e1524a69949))


### Miscellaneous Chores

* release 1.1.1 ([#56](https://www.github.com/googleapis/python-managed-identities/issues/56)) ([0a67d24](https://www.github.com/googleapis/python-managed-identities/commit/0a67d242c1d41a09aab0e0b32f5effb2aae384f3))

## [1.1.0](https://www.github.com/googleapis/python-managed-identities/compare/v1.0.0...v1.1.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#44](https://www.github.com/googleapis/python-managed-identities/issues/44)) ([1fd37ac](https://www.github.com/googleapis/python-managed-identities/commit/1fd37ac71b3d0b4106d87bcf527bf0bd8dada27d))


### Bug Fixes

* disable always_use_jwt_access ([#48](https://www.github.com/googleapis/python-managed-identities/issues/48)) ([c3dda3f](https://www.github.com/googleapis/python-managed-identities/commit/c3dda3f68b5c2a4320a046852c4f218d04075326))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-managed-identities/issues/1127)) ([#39](https://www.github.com/googleapis/python-managed-identities/issues/39)) ([4c82d41](https://www.github.com/googleapis/python-managed-identities/commit/4c82d419bd18f6361d9ebc134dc3c7cebf473cac))

## [1.0.0](https://www.github.com/googleapis/python-managed-identities/compare/v0.2.0...v1.0.0) (2021-06-16)


### Features

* bump release level to production/stable ([#32](https://www.github.com/googleapis/python-managed-identities/issues/32)) ([ab0fdc2](https://www.github.com/googleapis/python-managed-identities/commit/ab0fdc2df4dd10dc605bb869a88a95d68359f3fc))

## [0.2.0](https://www.github.com/googleapis/python-managed-identities/compare/v0.1.0...v0.2.0) (2021-05-16)


### Features

* support self-signed JWT flow for service accounts ([cf6f145](https://www.github.com/googleapis/python-managed-identities/commit/cf6f1456a626433753dafff5700f182497d9b18d))


### Bug Fixes

* add async client to %name_%version/init.py ([cf6f145](https://www.github.com/googleapis/python-managed-identities/commit/cf6f1456a626433753dafff5700f182497d9b18d))
* **deps:** add packaging requirement ([#30](https://www.github.com/googleapis/python-managed-identities/issues/30)) ([e618271](https://www.github.com/googleapis/python-managed-identities/commit/e618271758f0c9a8ed2c2ae8b057f9fc83491724))

## 0.1.0 (2021-03-15)


### Features

* generate v1 ([39e51df](https://www.github.com/googleapis/python-managed-identities/commit/39e51dff89c1577548ea08b6163c0de5c6f7d923))
