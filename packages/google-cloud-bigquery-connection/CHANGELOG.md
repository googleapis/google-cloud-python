# Changelog

## [1.5.1](https://github.com/googleapis/python-bigquery-connection/compare/v1.5.0...v1.5.1) (2022-06-07)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#218](https://github.com/googleapis/python-bigquery-connection/issues/218)) ([f842925](https://github.com/googleapis/python-bigquery-connection/commit/f842925ac025647b2959f60443b1b22326f8f9bc))


### Documentation

* fix changelog header to consistent size ([#219](https://github.com/googleapis/python-bigquery-connection/issues/219)) ([33c376f](https://github.com/googleapis/python-bigquery-connection/commit/33c376f7f1df8825dfdf1697512e42754b988075))

## [1.5.0](https://github.com/googleapis/python-bigquery-connection/compare/v1.4.0...v1.5.0) (2022-05-05)


### Features

* AuditConfig for IAM v1 ([#194](https://github.com/googleapis/python-bigquery-connection/issues/194)) ([d350b94](https://github.com/googleapis/python-bigquery-connection/commit/d350b947b3cfbb1aede8638c518eac2e8ba5495d))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([d350b94](https://github.com/googleapis/python-bigquery-connection/commit/d350b947b3cfbb1aede8638c518eac2e8ba5495d))
* region tags in create_mysql_connection.py ([#205](https://github.com/googleapis/python-bigquery-connection/issues/205)) ([f082fd2](https://github.com/googleapis/python-bigquery-connection/commit/f082fd246495cd6f874e6ac85655d27d594ab786))


### Documentation

* **samples:** create connection sample for MySQL instance ([#147](https://github.com/googleapis/python-bigquery-connection/issues/147)) ([8e664be](https://github.com/googleapis/python-bigquery-connection/commit/8e664bea488183d1132a61cb1ab7a912dde48b43))

## [1.4.0](https://github.com/googleapis/python-bigquery-connection/compare/v1.3.4...v1.4.0) (2022-03-08)


### Features

* Add Cloud_Resource Connection Support ([#181](https://github.com/googleapis/python-bigquery-connection/issues/181)) ([1be012a](https://github.com/googleapis/python-bigquery-connection/commit/1be012a7d7f585365cfd6c1e499188784838965a))

## [1.3.4](https://github.com/googleapis/python-bigquery-connection/compare/v1.3.3...v1.3.4) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#176](https://github.com/googleapis/python-bigquery-connection/issues/176)) ([a6cfa8f](https://github.com/googleapis/python-bigquery-connection/commit/a6cfa8f0c27ffa507305618d16a7ae5fb6fb15f9))
* **deps:** require proto-plus>=1.15.0 ([a6cfa8f](https://github.com/googleapis/python-bigquery-connection/commit/a6cfa8f0c27ffa507305618d16a7ae5fb6fb15f9))

## [1.3.3](https://github.com/googleapis/python-bigquery-connection/compare/v1.3.2...v1.3.3) (2022-02-26)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([d1e6767](https://github.com/googleapis/python-bigquery-connection/commit/d1e676705826962072919c51d881f22d540377b5))


### Documentation

* add generated snippets ([#165](https://github.com/googleapis/python-bigquery-connection/issues/165)) ([53edc14](https://github.com/googleapis/python-bigquery-connection/commit/53edc14b8f976985549856ac0823565b88a1a4ee))

## [1.3.2](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.3.1...v1.3.2) (2022-01-08)


### Documentation

* add python quickstart sample ([#141](https://www.github.com/googleapis/python-bigquery-connection/issues/141)) ([8b85fb6](https://www.github.com/googleapis/python-bigquery-connection/commit/8b85fb6784ba9bf51123e9185f276391326dd54a))

## [1.3.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.3.0...v1.3.1) (2021-11-02)


### Bug Fixes

* **deps:** drop packaging dependency ([826da22](https://www.github.com/googleapis/python-bigquery-connection/commit/826da22f591ab1c16eadf3a53cc8476e04577f40))
* **deps:** require google-api-core >= 1.28.0 ([826da22](https://www.github.com/googleapis/python-bigquery-connection/commit/826da22f591ab1c16eadf3a53cc8476e04577f40))


### Documentation

* list oneofs in docstring ([826da22](https://www.github.com/googleapis/python-bigquery-connection/commit/826da22f591ab1c16eadf3a53cc8476e04577f40))

## [1.3.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.3...v1.3.0) (2021-10-08)


### Features

* add context manager support in client ([#125](https://www.github.com/googleapis/python-bigquery-connection/issues/125)) ([bf9cc26](https://www.github.com/googleapis/python-bigquery-connection/commit/bf9cc268363a2a6e115b6af65ab6b50c05bbde28))

## [1.2.3](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.2...v1.2.3) (2021-10-05)


### Bug Fixes

* add 'dict' annotation type to 'request' ([87b77ee](https://www.github.com/googleapis/python-bigquery-connection/commit/87b77ee76e3abcce5428230a6884c66843353440))
* improper types in pagers generation ([47d1b68](https://www.github.com/googleapis/python-bigquery-connection/commit/47d1b68b74dda036b64979e4c7aab589046822ba))

## [1.2.2](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.1...v1.2.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#102](https://www.github.com/googleapis/python-bigquery-connection/issues/102)) ([d3d00a5](https://www.github.com/googleapis/python-bigquery-connection/commit/d3d00a5ba2e4521217b09a53c279dc2134d20e48))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#98](https://www.github.com/googleapis/python-bigquery-connection/issues/98)) ([842e239](https://www.github.com/googleapis/python-bigquery-connection/commit/842e239cbde9f041a5d2d9a8785c94682bc9140b))


### Miscellaneous Chores

* release as 1.2.2 ([#103](https://www.github.com/googleapis/python-bigquery-connection/issues/103)) ([2d6b168](https://www.github.com/googleapis/python-bigquery-connection/commit/2d6b168a7fce539383e72c9ea00d93fffe233607))

## [1.2.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.0...v1.2.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#97](https://www.github.com/googleapis/python-bigquery-connection/issues/97)) ([11e1214](https://www.github.com/googleapis/python-bigquery-connection/commit/11e12147753b04f68811ec9144d59c0fc8b15530))

## [1.2.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.1.1...v1.2.0) (2021-07-13)


### Features

* add cloud spanner connection support ([#93](https://www.github.com/googleapis/python-bigquery-connection/issues/93)) ([3ae2369](https://www.github.com/googleapis/python-bigquery-connection/commit/3ae236928f0ac923367d5379daa59f366299397b))

## [1.1.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.1.0...v1.1.1) (2021-06-30)


### Bug Fixes

* disable always_use_jwt_access ([37f28c5](https://www.github.com/googleapis/python-bigquery-connection/commit/37f28c5112d9b8f180a8cf754d474ac74f5f92d9))
* disable always_use_jwt_access ([#91](https://www.github.com/googleapis/python-bigquery-connection/issues/91)) ([37f28c5](https://www.github.com/googleapis/python-bigquery-connection/commit/37f28c5112d9b8f180a8cf754d474ac74f5f92d9))

## [1.1.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.0.1...v1.1.0) (2021-06-23)


### Features

* add always_use_jwt_access ([#88](https://www.github.com/googleapis/python-bigquery-connection/issues/88)) ([821fffc](https://www.github.com/googleapis/python-bigquery-connection/commit/821fffcc3f9ecdb222e4a5a2c94ad9c5d3325681))
* support self-signed JWT flow for service accounts ([2f1db84](https://www.github.com/googleapis/python-bigquery-connection/commit/2f1db842b16cf2c3981c61b503482fa7df85bdfe))


### Bug Fixes

* add async client to %name_%version/init.py ([2f1db84](https://www.github.com/googleapis/python-bigquery-connection/commit/2f1db842b16cf2c3981c61b503482fa7df85bdfe))
* **deps:** add packaging requirement ([#77](https://www.github.com/googleapis/python-bigquery-connection/issues/77)) ([2ab8403](https://www.github.com/googleapis/python-bigquery-connection/commit/2ab84031d3f46b5ccd1acaefe5b744679b43e140))
* exclude docs and tests from package ([#83](https://www.github.com/googleapis/python-bigquery-connection/issues/83)) ([3ef23e5](https://www.github.com/googleapis/python-bigquery-connection/commit/3ef23e5b9e8f4a0bcef24dbe79773ca92a336ef0))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-bigquery-connection/issues/1127)) ([#85](https://www.github.com/googleapis/python-bigquery-connection/issues/85)) ([715e04b](https://www.github.com/googleapis/python-bigquery-connection/commit/715e04b77dc352b17e508288a7268c6c2ce46e10)), closes [#1126](https://www.github.com/googleapis/python-bigquery-connection/issues/1126)
* Update the README to reflect that this library is GA ([#79](https://www.github.com/googleapis/python-bigquery-connection/issues/79)) ([f737861](https://www.github.com/googleapis/python-bigquery-connection/commit/f7378614002697ed5c7dc9217fbe8b48ba7c7410))

## [1.0.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.0.0...v1.0.1) (2021-02-03)


### Bug Fixes

* remove gRPC send/recv limits ([#37](https://www.github.com/googleapis/python-bigquery-connection/issues/37)) ([c8d639a](https://www.github.com/googleapis/python-bigquery-connection/commit/c8d639a23d1800c37c2db1cf9f0fc41b51ac07b8))


### Documentation

* **python:** update intersphinx for grpc and auth ([#32](https://www.github.com/googleapis/python-bigquery-connection/issues/32)) ([f3ce3aa](https://www.github.com/googleapis/python-bigquery-connection/commit/f3ce3aa826173bf61b3b79803d0231c27f89e6fa))

## [1.0.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v0.3.0...v1.0.0) (2020-10-29)


### ⚠ BREAKING CHANGES

* update package names to avoid conflict with google-cloud-bigquery (#27)

### Bug Fixes

* update package names to avoid conflict with google-cloud-bigquery ([#27](https://www.github.com/googleapis/python-bigquery-connection/issues/27)) ([741121c](https://www.github.com/googleapis/python-bigquery-connection/commit/741121c44786ac78e5750aa5383b6da918c3230c))

## [0.3.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v0.2.0...v0.3.0) (2020-10-28)


### Features

* add AWS connection type ([#19](https://www.github.com/googleapis/python-bigquery-connection/issues/19)) ([3d1a41a](https://www.github.com/googleapis/python-bigquery-connection/commit/3d1a41ad208274448604a0a17d072f6fcb36535a))

## [0.2.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v0.1.0...v0.2.0) (2020-08-10)


### Features

* add async client ([#12](https://www.github.com/googleapis/python-bigquery-connection/issues/12)) ([58eb861](https://www.github.com/googleapis/python-bigquery-connection/commit/58eb8615e1858b50a9727db7a56cec3610959d4f))


### Documentation

* **readme:** adds link to BQ external data sources docs ([#5](https://www.github.com/googleapis/python-bigquery-connection/issues/5)) ([4a740d0](https://www.github.com/googleapis/python-bigquery-connection/commit/4a740d0beba471bd5646a0c69045f69c9b158639))

## 0.1.0 (2020-05-19)


### Features

* generate v1 ([73b89dc](https://www.github.com/googleapis/python-bigquery-connection/commit/73b89dcb423026c4b4e537ff728d22be2cb5ff3f))
