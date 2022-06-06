# Changelog

## [1.3.2](https://github.com/googleapis/python-vpc-access/compare/v1.3.1...v1.3.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#111](https://github.com/googleapis/python-vpc-access/issues/111)) ([b0dd3f8](https://github.com/googleapis/python-vpc-access/commit/b0dd3f8ad278067188fdc736fb047a747c410ec7))


### Documentation

* fix changelog header to consistent size ([#112](https://github.com/googleapis/python-vpc-access/issues/112)) ([02034f0](https://github.com/googleapis/python-vpc-access/commit/02034f0c11d0b5352d74b1b327b6795185aa26b1))

## [1.3.1](https://github.com/googleapis/python-vpc-access/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#90](https://github.com/googleapis/python-vpc-access/issues/90)) ([cde4f5b](https://github.com/googleapis/python-vpc-access/commit/cde4f5b590cb7bfc02fb13d6ff56c9f27e580f95))

## [1.3.0](https://github.com/googleapis/python-vpc-access/compare/v1.2.1...v1.3.0) (2022-02-11)


### Features

* add api key support ([#76](https://github.com/googleapis/python-vpc-access/issues/76)) ([ff52eb5](https://github.com/googleapis/python-vpc-access/commit/ff52eb59ead8c561e057d29d15b6592033b65258))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([6d4115c](https://github.com/googleapis/python-vpc-access/commit/6d4115c40217796cc5797be421889704777edb8d))

## [1.2.1](https://www.github.com/googleapis/python-vpc-access/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([cd6b816](https://www.github.com/googleapis/python-vpc-access/commit/cd6b816ece0ea0de28619d2072d980678e82c414))
* **deps:** require google-api-core >= 1.28.0 ([cd6b816](https://www.github.com/googleapis/python-vpc-access/commit/cd6b816ece0ea0de28619d2072d980678e82c414))


### Documentation

* list oneofs in docstring ([cd6b816](https://www.github.com/googleapis/python-vpc-access/commit/cd6b816ece0ea0de28619d2072d980678e82c414))

## [1.2.0](https://www.github.com/googleapis/python-vpc-access/compare/v1.1.0...v1.2.0) (2021-10-18)


### Features

* add support for python 3.10 ([#55](https://www.github.com/googleapis/python-vpc-access/issues/55)) ([dc33d72](https://www.github.com/googleapis/python-vpc-access/commit/dc33d72ba0de607a9fdf5d978b6daf52c6cfcefa))

## [1.1.0](https://www.github.com/googleapis/python-vpc-access/compare/v1.0.2...v1.1.0) (2021-10-07)


### Features

* add context manager support in client ([#51](https://www.github.com/googleapis/python-vpc-access/issues/51)) ([f031d91](https://www.github.com/googleapis/python-vpc-access/commit/f031d910e7924ae6db9ac20bf26a38b74e36597f))

## [1.0.2](https://www.github.com/googleapis/python-vpc-access/compare/v1.0.1...v1.0.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([294b2da](https://www.github.com/googleapis/python-vpc-access/commit/294b2da2a2161b7e84ce011780e7f25bc8bd7184))

## [1.0.1](https://www.github.com/googleapis/python-vpc-access/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([be61638](https://www.github.com/googleapis/python-vpc-access/commit/be616386c0a9db4c49f8f319498411ab969542a3))


## [1.0.0](https://www.github.com/googleapis/python-vpc-access/compare/v0.2.1...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#29](https://www.github.com/googleapis/python-vpc-access/issues/29)) ([6e8f2b1](https://www.github.com/googleapis/python-vpc-access/commit/6e8f2b1a5abd697da122854f8fee4c8d3cb00383))

## [0.2.1](https://www.github.com/googleapis/python-vpc-access/compare/v0.2.0...v0.2.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#20](https://www.github.com/googleapis/python-vpc-access/issues/20)) ([46a4eaf](https://www.github.com/googleapis/python-vpc-access/commit/46a4eaf7814d69edb7b5ecb1767805088e3e82f9))
* enable self signed jwt for grpc ([#26](https://www.github.com/googleapis/python-vpc-access/issues/26)) ([aca8358](https://www.github.com/googleapis/python-vpc-access/commit/aca8358bf75e76a49508688507aba3d73ec8d95c))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#21](https://www.github.com/googleapis/python-vpc-access/issues/21)) ([d1fc404](https://www.github.com/googleapis/python-vpc-access/commit/d1fc404fd34d69b70c925bf3af2a022c116a5a11))


### Miscellaneous Chores

* release 0.2.1 ([#25](https://www.github.com/googleapis/python-vpc-access/issues/25)) ([8ded00a](https://www.github.com/googleapis/python-vpc-access/commit/8ded00a39a9f151376e1060b617805222aef78c9))

## [0.2.0](https://www.github.com/googleapis/python-vpc-access/compare/v0.1.0...v0.2.0) (2021-07-14)


### Features

* add always_use_jwt_access ([#11](https://www.github.com/googleapis/python-vpc-access/issues/11)) ([6f1f049](https://www.github.com/googleapis/python-vpc-access/commit/6f1f0499f661625e77c71543f9b70f60b4478338))


### Bug Fixes

* disable always_use_jwt_access ([#15](https://www.github.com/googleapis/python-vpc-access/issues/15)) ([25a9da1](https://www.github.com/googleapis/python-vpc-access/commit/25a9da1e9b7761632befd3b0e7646f7e45f2ebc2))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-vpc-access/issues/1127)) ([#6](https://www.github.com/googleapis/python-vpc-access/issues/6)) ([36a763a](https://www.github.com/googleapis/python-vpc-access/commit/36a763acbccf7641efc4d57fcb7ebddf3322d66a))

## 0.1.0 (2021-06-14)


### Features

* generate v1 ([2f99f6f](https://www.github.com/googleapis/python-vpc-access/commit/2f99f6f08c23ac14df17deef6c1d131e396a8e2c))
