# Changelog

## [1.3.2](https://github.com/googleapis/python-memcache/compare/v1.3.1...v1.3.2) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#184](https://github.com/googleapis/python-memcache/issues/184)) ([acc06a7](https://github.com/googleapis/python-memcache/commit/acc06a7c8564d272617a66456ac2a002b463443f))


### Documentation

* fix changelog header to consistent size ([#183](https://github.com/googleapis/python-memcache/issues/183)) ([3647e5f](https://github.com/googleapis/python-memcache/commit/3647e5f70d1d43e388d25f11fee9d730c453732d))

## [1.3.1](https://github.com/googleapis/python-memcache/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#150](https://github.com/googleapis/python-memcache/issues/150)) ([fba1303](https://github.com/googleapis/python-memcache/commit/fba130344bb07512d8fc0355c2c2da158d9be8ff))
* **deps:** require proto-plus>=1.15.0 ([fba1303](https://github.com/googleapis/python-memcache/commit/fba130344bb07512d8fc0355c2c2da158d9be8ff))

## [1.3.0](https://github.com/googleapis/python-memcache/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#135](https://github.com/googleapis/python-memcache/issues/135)) ([ef5104e](https://github.com/googleapis/python-memcache/commit/ef5104e0922d980c0023b65665f29f27c14cddcc))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([5f8a2b4](https://github.com/googleapis/python-memcache/commit/5f8a2b4fe5fcc0c4a2be6b9f8529f4ceacbf6421))

## [1.2.1](https://www.github.com/googleapis/python-memcache/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([5159fe9](https://www.github.com/googleapis/python-memcache/commit/5159fe99b200979b54ce76633a7b8cda87931eee))
* **deps:** require google-api-core >= 1.28.0 ([5159fe9](https://www.github.com/googleapis/python-memcache/commit/5159fe99b200979b54ce76633a7b8cda87931eee))


### Documentation

* list oneofs in docstring ([5159fe9](https://www.github.com/googleapis/python-memcache/commit/5159fe99b200979b54ce76633a7b8cda87931eee))

## [1.2.0](https://www.github.com/googleapis/python-memcache/compare/v1.1.3...v1.2.0) (2021-10-12)


### Features

* add context manager support in client ([#111](https://www.github.com/googleapis/python-memcache/issues/111)) ([a385b99](https://www.github.com/googleapis/python-memcache/commit/a385b993b2473a01256042cc2c560f872c6b8c13))

## [1.1.3](https://www.github.com/googleapis/python-memcache/compare/v1.1.2...v1.1.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([3680bac](https://www.github.com/googleapis/python-memcache/commit/3680bac8c702cc0313b06dbec3c0c6512ac4a58a))

## [1.1.2](https://www.github.com/googleapis/python-memcache/compare/v1.1.1...v1.1.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([c56fbee](https://www.github.com/googleapis/python-memcache/commit/c56fbee0ffedac37a80bca5ca3028c53753ada5a))

## [1.1.1](https://www.github.com/googleapis/python-memcache/compare/v1.1.0...v1.1.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#82](https://www.github.com/googleapis/python-memcache/issues/82)) ([d4f2c96](https://www.github.com/googleapis/python-memcache/commit/d4f2c965c13c28f97bda9aa8ab570529747bd68d))
* enable self signed jwt for grpc ([#88](https://www.github.com/googleapis/python-memcache/issues/88)) ([0ddd8eb](https://www.github.com/googleapis/python-memcache/commit/0ddd8eb6c91b799d443e4d09a20adcd25d9ef70a))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#83](https://www.github.com/googleapis/python-memcache/issues/83)) ([9471485](https://www.github.com/googleapis/python-memcache/commit/94714851060def4b68ec065ae435b71ce94f41bc))


### Miscellaneous Chores

* release as 1.1.1 ([#87](https://www.github.com/googleapis/python-memcache/issues/87)) ([3182207](https://www.github.com/googleapis/python-memcache/commit/31822078c9a27c26f303f51106ccb0af587a35e4))

## [1.1.0](https://www.github.com/googleapis/python-memcache/compare/v1.0.0...v1.1.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#79](https://www.github.com/googleapis/python-memcache/issues/79)) ([e7f03bb](https://www.github.com/googleapis/python-memcache/commit/e7f03bb915eb523afcb72ec0d2dd275739f485e5))
* support self-signed JWT flow for service accounts ([2d1aaf4](https://www.github.com/googleapis/python-memcache/commit/2d1aaf439d096857a727752ae129852b279c3658))


### Bug Fixes

* add async client to %name_%version/init.py ([2d1aaf4](https://www.github.com/googleapis/python-memcache/commit/2d1aaf439d096857a727752ae129852b279c3658))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-memcache/issues/1127)) ([#70](https://www.github.com/googleapis/python-memcache/issues/70)) ([f273025](https://www.github.com/googleapis/python-memcache/commit/f273025fedad32be0b766e40ab99b445f529cd13))

## [1.0.0](https://www.github.com/googleapis/python-memcache/compare/v0.3.0...v1.0.0) (2021-05-28)


### Features

* bump release level to production/stable ([#59](https://www.github.com/googleapis/python-memcache/issues/59)) ([b8d9394](https://www.github.com/googleapis/python-memcache/commit/b8d9394dd34b97ddd68f8c73a5f516ba5294a70c))
* support self-signed JWT flow for service accounts ([2ad1bfb](https://www.github.com/googleapis/python-memcache/commit/2ad1bfbee1f847c1b150b0e1595faba63f42d768))


### Bug Fixes

* add async client to %name_%version/init.py ([2ad1bfb](https://www.github.com/googleapis/python-memcache/commit/2ad1bfbee1f847c1b150b0e1595faba63f42d768))


### Miscellaneous Chores

* release 1.0.0 ([#62](https://www.github.com/googleapis/python-memcache/issues/62)) ([829a7b7](https://www.github.com/googleapis/python-memcache/commit/829a7b7b0cfedb3a18a61158d7aa949b178ae4fe))

## [0.3.0](https://www.github.com/googleapis/python-memcache/compare/v0.2.0...v0.3.0) (2021-02-10)


### Features

* add async client ([#26](https://www.github.com/googleapis/python-memcache/issues/26)) ([0bbc337](https://www.github.com/googleapis/python-memcache/commit/0bbc337594e2a44c51a5b372670d72499592e2e0))
* generate v1 ([#37](https://www.github.com/googleapis/python-memcache/issues/37)) ([7945daf](https://www.github.com/googleapis/python-memcache/commit/7945dafbbee1b21efc733e079044db77e880a10a))

## [0.2.0](https://www.github.com/googleapis/python-memcache/compare/v0.1.0...v0.2.0) (2020-05-28)


### Features

* add mtls support ([#7](https://www.github.com/googleapis/python-memcache/issues/7)) ([669d2a9](https://www.github.com/googleapis/python-memcache/commit/669d2a985877971fb6c1eb0ad97806fbcfcc7399))

## 0.1.0 (2020-03-03)


### Features

* generate v1beta2 ([8b4b6d8](https://www.github.com/googleapis/python-memcache/commit/8b4b6d888b5181deedc87436165e1ed327fe26f5))
