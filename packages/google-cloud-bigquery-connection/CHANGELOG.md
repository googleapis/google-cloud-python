# Changelog

### [1.2.2](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.1...v1.2.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#102](https://www.github.com/googleapis/python-bigquery-connection/issues/102)) ([d3d00a5](https://www.github.com/googleapis/python-bigquery-connection/commit/d3d00a5ba2e4521217b09a53c279dc2134d20e48))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#98](https://www.github.com/googleapis/python-bigquery-connection/issues/98)) ([842e239](https://www.github.com/googleapis/python-bigquery-connection/commit/842e239cbde9f041a5d2d9a8785c94682bc9140b))


### Miscellaneous Chores

* release as 1.2.2 ([#103](https://www.github.com/googleapis/python-bigquery-connection/issues/103)) ([2d6b168](https://www.github.com/googleapis/python-bigquery-connection/commit/2d6b168a7fce539383e72c9ea00d93fffe233607))

### [1.2.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.2.0...v1.2.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#97](https://www.github.com/googleapis/python-bigquery-connection/issues/97)) ([11e1214](https://www.github.com/googleapis/python-bigquery-connection/commit/11e12147753b04f68811ec9144d59c0fc8b15530))

## [1.2.0](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.1.1...v1.2.0) (2021-07-13)


### Features

* add cloud spanner connection support ([#93](https://www.github.com/googleapis/python-bigquery-connection/issues/93)) ([3ae2369](https://www.github.com/googleapis/python-bigquery-connection/commit/3ae236928f0ac923367d5379daa59f366299397b))

### [1.1.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.1.0...v1.1.1) (2021-06-30)


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

### [1.0.1](https://www.github.com/googleapis/python-bigquery-connection/compare/v1.0.0...v1.0.1) (2021-02-03)


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
