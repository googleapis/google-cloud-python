# Changelog

### [1.3.1](https://github.com/googleapis/python-service-usage/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#88](https://github.com/googleapis/python-service-usage/issues/88)) ([bee9ae0](https://github.com/googleapis/python-service-usage/commit/bee9ae00c8dd77fcc423ceb4b0023b0041d6c395))

## [1.3.0](https://github.com/googleapis/python-service-usage/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#74](https://github.com/googleapis/python-service-usage/issues/74)) ([c9cf774](https://github.com/googleapis/python-service-usage/commit/c9cf774ba8082ce7026acd582817e84b63d39fbe))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([27fb0c2](https://github.com/googleapis/python-service-usage/commit/27fb0c270dc776862f282159c9a637aa5900ced7))


### Documentation

* add generated snippets ([#79](https://github.com/googleapis/python-service-usage/issues/79)) ([dee08f1](https://github.com/googleapis/python-service-usage/commit/dee08f1d654cb5e04955ca51c824f77b13c000b9))

### [1.2.1](https://www.github.com/googleapis/python-service-usage/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([57a982c](https://www.github.com/googleapis/python-service-usage/commit/57a982c7cafb2f91a9c2d2f0f8b85be1502f14be))
* **deps:** require google-api-core >= 1.28.0 ([57a982c](https://www.github.com/googleapis/python-service-usage/commit/57a982c7cafb2f91a9c2d2f0f8b85be1502f14be))


### Documentation

* list oneofs in docstring ([57a982c](https://www.github.com/googleapis/python-service-usage/commit/57a982c7cafb2f91a9c2d2f0f8b85be1502f14be))

## [1.2.0](https://www.github.com/googleapis/python-service-usage/compare/v1.1.0...v1.2.0) (2021-10-18)


### Features

* add support for python 3.10 ([#53](https://www.github.com/googleapis/python-service-usage/issues/53)) ([9f235a8](https://www.github.com/googleapis/python-service-usage/commit/9f235a84d01b84a598f5af4bdd6203f4d752f31a))

## [1.1.0](https://www.github.com/googleapis/python-service-usage/compare/v1.0.1...v1.1.0) (2021-10-07)


### Features

* add context manager support in client ([#49](https://www.github.com/googleapis/python-service-usage/issues/49)) ([b50e7cb](https://www.github.com/googleapis/python-service-usage/commit/b50e7cbbf53e0efb6809bce5c25cdc7369e65f5d))


### Bug Fixes

* improper types in pagers generation ([b230f5f](https://www.github.com/googleapis/python-service-usage/commit/b230f5fd83f21b7ac86bb01dac85ce403d694228))

### [1.0.1](https://www.github.com/googleapis/python-service-usage/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([172ba0d](https://www.github.com/googleapis/python-service-usage/commit/172ba0dd5ca2d1d6ffee0cccce45ee28c822704b))

## [1.0.0](https://www.github.com/googleapis/python-service-usage/compare/v0.2.2...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#28](https://www.github.com/googleapis/python-service-usage/issues/28)) ([6627d2d](https://www.github.com/googleapis/python-service-usage/commit/6627d2dddf686a6ecc355891989928ca33003f00))

### [0.2.2](https://www.github.com/googleapis/python-service-usage/compare/v0.2.1...v0.2.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#24](https://www.github.com/googleapis/python-service-usage/issues/24)) ([cb9bed0](https://www.github.com/googleapis/python-service-usage/commit/cb9bed079e5ab4316ae79d44c8cf4bee1b4c3ae7))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#20](https://www.github.com/googleapis/python-service-usage/issues/20)) ([394ed1a](https://www.github.com/googleapis/python-service-usage/commit/394ed1a75dcfa2c70f8bbac6aaea1150a6d90052))


### Miscellaneous Chores

* release as 0.2.2 ([#25](https://www.github.com/googleapis/python-service-usage/issues/25)) ([4f1ab38](https://www.github.com/googleapis/python-service-usage/commit/4f1ab3848cf43ae7385ebf5c4dcb5f1b9057f14d))

### [0.2.1](https://www.github.com/googleapis/python-service-usage/compare/v0.2.0...v0.2.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#19](https://www.github.com/googleapis/python-service-usage/issues/19)) ([599eee0](https://www.github.com/googleapis/python-service-usage/commit/599eee0fe0f92efa4a19835691a9216c8804349f))

## [0.2.0](https://www.github.com/googleapis/python-service-usage/compare/v0.1.0...v0.2.0) (2021-07-14)


### Features

* add always_use_jwt_access ([#10](https://www.github.com/googleapis/python-service-usage/issues/10)) ([87d2c40](https://www.github.com/googleapis/python-service-usage/commit/87d2c40eb4989b94229984f22e461fdc56a4f122))


### Bug Fixes

* disable always_use_jwt_access ([#14](https://www.github.com/googleapis/python-service-usage/issues/14)) ([2f90720](https://www.github.com/googleapis/python-service-usage/commit/2f907209d1199c5a9cec210495845775ae630ccf))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-service-usage/issues/1127)) ([#5](https://www.github.com/googleapis/python-service-usage/issues/5)) ([c8bbbcb](https://www.github.com/googleapis/python-service-usage/commit/c8bbbcbd939b421fa0b243f6003de54afc2107e1))

## 0.1.0 (2021-06-14)


### Features

* generate v1 ([b468d1b](https://www.github.com/googleapis/python-service-usage/commit/b468d1b447c30994d9266b5e0ff4c34ec0d19d80))
