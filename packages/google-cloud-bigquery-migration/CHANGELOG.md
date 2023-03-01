# Changelog

## [0.10.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.9.1...v0.10.0) (2023-03-01)


### Features

* **v2alpha:** Add SQL translation service ([#170](https://github.com/googleapis/python-bigquery-migration/issues/170)) ([533d1d8](https://github.com/googleapis/python-bigquery-migration/commit/533d1d87e3bfb917488550a979b35994ebe293ed))

## [0.9.1](https://github.com/googleapis/python-bigquery-migration/compare/v0.9.0...v0.9.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([970281e](https://github.com/googleapis/python-bigquery-migration/commit/970281ecea66632b651f8346166509e0e7160168))


### Documentation

* Add documentation for enums ([970281e](https://github.com/googleapis/python-bigquery-migration/commit/970281ecea66632b651f8346166509e0e7160168))

## [0.9.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.8.0...v0.9.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#157](https://github.com/googleapis/python-bigquery-migration/issues/157)) ([d9b27e4](https://github.com/googleapis/python-bigquery-migration/commit/d9b27e4519d47b5cc95a04336100f7fcaf7235c7))

## [0.8.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.7.2...v0.8.0) (2022-12-15)


### Features

* Add support for `google.cloud.bigquery_migration.__version__` ([8f180ec](https://github.com/googleapis/python-bigquery-migration/commit/8f180ec2c2dec24d73982d5af2f9af8f8f7dfa8f))
* Add typing to proto.Message based class attributes ([8f180ec](https://github.com/googleapis/python-bigquery-migration/commit/8f180ec2c2dec24d73982d5af2f9af8f8f7dfa8f))


### Bug Fixes

* Add dict typing for client_options ([8f180ec](https://github.com/googleapis/python-bigquery-migration/commit/8f180ec2c2dec24d73982d5af2f9af8f8f7dfa8f))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([61bc618](https://github.com/googleapis/python-bigquery-migration/commit/61bc618abf8ced62fea472b9ceb25a6c5fe24e6d))
* Drop usage of pkg_resources ([61bc618](https://github.com/googleapis/python-bigquery-migration/commit/61bc618abf8ced62fea472b9ceb25a6c5fe24e6d))
* Fix timeout default values ([61bc618](https://github.com/googleapis/python-bigquery-migration/commit/61bc618abf8ced62fea472b9ceb25a6c5fe24e6d))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([8f180ec](https://github.com/googleapis/python-bigquery-migration/commit/8f180ec2c2dec24d73982d5af2f9af8f8f7dfa8f))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([61bc618](https://github.com/googleapis/python-bigquery-migration/commit/61bc618abf8ced62fea472b9ceb25a6c5fe24e6d))

## [0.7.2](https://github.com/googleapis/python-bigquery-migration/compare/v0.7.1...v0.7.2) (2022-10-08)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#139](https://github.com/googleapis/python-bigquery-migration/issues/139)) ([5258fa6](https://github.com/googleapis/python-bigquery-migration/commit/5258fa6112f7f47ec0b3351f45dd90f18eaa5181))

## [0.7.1](https://github.com/googleapis/python-bigquery-migration/compare/v0.7.0...v0.7.1) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#136](https://github.com/googleapis/python-bigquery-migration/issues/136)) ([f69ed02](https://github.com/googleapis/python-bigquery-migration/commit/f69ed025709bf30d4dca51d09a9fd9b3a3d964cd))

## [0.7.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.6.0...v0.7.0) (2022-08-11)


### Features

* **v2:** Add MySQL dialect ([#116](https://github.com/googleapis/python-bigquery-migration/issues/116)) ([9f66ca4](https://github.com/googleapis/python-bigquery-migration/commit/9f66ca4c1e8b1438a8f11919c24fb6506a5790ea))


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#118](https://github.com/googleapis/python-bigquery-migration/issues/118)) ([b217543](https://github.com/googleapis/python-bigquery-migration/commit/b2175431fd5b2391f9490a5900977c5768d6712a))
* **deps:** require proto-plus >= 1.22.0 ([b217543](https://github.com/googleapis/python-bigquery-migration/commit/b2175431fd5b2391f9490a5900977c5768d6712a))

## [0.6.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.5.0...v0.6.0) (2022-07-16)


### Features

* add audience parameter ([77e4c52](https://github.com/googleapis/python-bigquery-migration/commit/77e4c52d597e62956e2349dfff2f1b88df013450))
* Add Presto and Postgresql dialects ([#103](https://github.com/googleapis/python-bigquery-migration/issues/103)) ([77e4c52](https://github.com/googleapis/python-bigquery-migration/commit/77e4c52d597e62956e2349dfff2f1b88df013450))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([77e4c52](https://github.com/googleapis/python-bigquery-migration/commit/77e4c52d597e62956e2349dfff2f1b88df013450))
* require python 3.7+ ([#105](https://github.com/googleapis/python-bigquery-migration/issues/105)) ([13f50a7](https://github.com/googleapis/python-bigquery-migration/commit/13f50a7b845f5d4ce0aa03821578b730ea37dbb2))

## [0.5.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.4.3...v0.5.0) (2022-06-15)


### Features

* Add SQL Server dialect to bigquerymigration v2 client library ([#99](https://github.com/googleapis/python-bigquery-migration/issues/99)) ([35a1099](https://github.com/googleapis/python-bigquery-migration/commit/35a10990d6d9019511d9c1813f4f6d5889004189))

## [0.4.3](https://github.com/googleapis/python-bigquery-migration/compare/v0.4.2...v0.4.3) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#95](https://github.com/googleapis/python-bigquery-migration/issues/95)) ([0b93e8d](https://github.com/googleapis/python-bigquery-migration/commit/0b93e8d0332269cf837d146106d8d5fbdcd42cc4))


### Documentation

* fix changelog header to consistent size ([#96](https://github.com/googleapis/python-bigquery-migration/issues/96)) ([e95f0fc](https://github.com/googleapis/python-bigquery-migration/commit/e95f0fcad0f6c3366ade1637b51295a89d2bc1b2))

## [0.4.2](https://github.com/googleapis/python-bigquery-migration/compare/v0.4.1...v0.4.2) (2022-05-22)


### Documentation

* **samples:** add create_migration_workflow snippet ([#71](https://github.com/googleapis/python-bigquery-migration/issues/71)) ([761b5f5](https://github.com/googleapis/python-bigquery-migration/commit/761b5f5045edbe8c81a31f501bf3b14de7dffe20))

## [0.4.1](https://github.com/googleapis/python-bigquery-migration/compare/v0.4.0...v0.4.1) (2022-05-05)


### Documentation

* fix type in docstring for map fields ([6c5982b](https://github.com/googleapis/python-bigquery-migration/commit/6c5982bf2fcc0d90d6a6951a7dd676e9b7974627))

## [0.4.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.3.1...v0.4.0) (2022-04-03)


### Features

* Add bigquery_migration v2 client library  ([#54](https://github.com/googleapis/python-bigquery-migration/issues/54)) ([776ea61](https://github.com/googleapis/python-bigquery-migration/commit/776ea6189f6a94c5daa5af6b4fa7e0e3b21015ec))


### Bug Fixes

* set bigquery_migration_v2 as the default import ([776ea61](https://github.com/googleapis/python-bigquery-migration/commit/776ea6189f6a94c5daa5af6b4fa7e0e3b21015ec))

## [0.3.1](https://github.com/googleapis/python-bigquery-migration/compare/v0.3.0...v0.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#48](https://github.com/googleapis/python-bigquery-migration/issues/48)) ([2d8b0b5](https://github.com/googleapis/python-bigquery-migration/commit/2d8b0b5845573d2784b6bfa925285c6ddac5c1e7))

## [0.3.0](https://github.com/googleapis/python-bigquery-migration/compare/v0.2.1...v0.3.0) (2022-02-14)


### Features

* add api key support ([#34](https://github.com/googleapis/python-bigquery-migration/issues/34)) ([124de81](https://github.com/googleapis/python-bigquery-migration/commit/124de81e97b39694433820678704b3f6079ce1e2))
* Add task details and orchestration result details ([#32](https://github.com/googleapis/python-bigquery-migration/issues/32)) ([44c10e1](https://github.com/googleapis/python-bigquery-migration/commit/44c10e17767135b7a5c9a5e22b82260be75459b1))


### Bug Fixes

* **deps:** remove unused dependency libcst ([#39](https://github.com/googleapis/python-bigquery-migration/issues/39)) ([496abc7](https://github.com/googleapis/python-bigquery-migration/commit/496abc7854985c6f1bfd8463330f2f07a0f3048c))
* resolve DuplicateCredentialArgs error when using credentials_file ([b3b1ee2](https://github.com/googleapis/python-bigquery-migration/commit/b3b1ee2c0075adadedeef28a5853a440fc1e6535))


### Documentation

* add generated snippets ([#38](https://github.com/googleapis/python-bigquery-migration/issues/38)) ([13b7ac7](https://github.com/googleapis/python-bigquery-migration/commit/13b7ac71ace1cc226d6fa5b43dde345c3ac3e489))

## [0.2.1](https://www.github.com/googleapis/python-bigquery-migration/compare/v0.2.0...v0.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([70ec0c5](https://www.github.com/googleapis/python-bigquery-migration/commit/70ec0c5da7cf18ed632bfb19c5f2d6bfb8d2334a))
* **deps:** require google-api-core >= 1.28.0 ([70ec0c5](https://www.github.com/googleapis/python-bigquery-migration/commit/70ec0c5da7cf18ed632bfb19c5f2d6bfb8d2334a))


### Documentation

* list oneofs in docstring ([70ec0c5](https://www.github.com/googleapis/python-bigquery-migration/commit/70ec0c5da7cf18ed632bfb19c5f2d6bfb8d2334a))

## [0.2.0](https://www.github.com/googleapis/python-bigquery-migration/compare/v0.1.0...v0.2.0) (2021-10-08)


### Features

* add context manager support in client ([#8](https://www.github.com/googleapis/python-bigquery-migration/issues/8)) ([d9dbb32](https://www.github.com/googleapis/python-bigquery-migration/commit/d9dbb32edeffee1e559f979300713a4a10cd9806))

## 0.1.0 (2021-09-30)


### Features

* generate v2alpha ([ccb7ca8](https://www.github.com/googleapis/python-bigquery-migration/commit/ccb7ca8473252da1eeab1ba4338c65a5ff0e6e8e))


### Bug Fixes

* address testing failures from initial generation ([#1](https://www.github.com/googleapis/python-bigquery-migration/issues/1)) ([85284a7](https://www.github.com/googleapis/python-bigquery-migration/commit/85284a7f1f7ed39cd2de61ecae5ed40656283533))
* correct python namespace for migration API ([#3](https://www.github.com/googleapis/python-bigquery-migration/issues/3)) ([3dda870](https://www.github.com/googleapis/python-bigquery-migration/commit/3dda8702d54ee39897322215c2a551921356ae61))
