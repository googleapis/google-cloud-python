# Changelog

### [1.3.2](https://github.com/googleapis/python-shell/compare/v1.3.1...v1.3.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#85](https://github.com/googleapis/python-shell/issues/85)) ([b3271c5](https://github.com/googleapis/python-shell/commit/b3271c5f07fc1326a614ab8fb365cc9b7c46c897))

### [1.3.1](https://github.com/googleapis/python-shell/compare/v1.3.0...v1.3.1) (2022-02-11)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([b660c07](https://github.com/googleapis/python-shell/commit/b660c07d2f42673a85dd596590c82e2f972530fd))

## [1.3.0](https://github.com/googleapis/python-shell/compare/v1.2.2...v1.3.0) (2022-01-25)


### Features

* add api key support ([#70](https://github.com/googleapis/python-shell/issues/70)) ([3e91fb8](https://github.com/googleapis/python-shell/commit/3e91fb8bacf28a19e167a357829ffcbb9e0e02c9))

### [1.2.2](https://www.github.com/googleapis/python-shell/compare/v1.2.1...v1.2.2) (2022-01-07)


### Bug Fixes

* provide appropriate mock values for message body fields ([24cf144](https://www.github.com/googleapis/python-shell/commit/24cf144d17b64dc71a5182d1ccbc44444bd68450))

### [1.2.1](https://www.github.com/googleapis/python-shell/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([ff43aa0](https://www.github.com/googleapis/python-shell/commit/ff43aa0900e4fc626ab3243621f1ccc763878616))
* **deps:** require google-api-core >= 1.28.0 ([ff43aa0](https://www.github.com/googleapis/python-shell/commit/ff43aa0900e4fc626ab3243621f1ccc763878616))


### Documentation

* list oneofs in docstring ([ff43aa0](https://www.github.com/googleapis/python-shell/commit/ff43aa0900e4fc626ab3243621f1ccc763878616))

## [1.2.0](https://www.github.com/googleapis/python-shell/compare/v1.1.0...v1.2.0) (2021-10-18)


### Features

* add support for python 3.10 ([#45](https://www.github.com/googleapis/python-shell/issues/45)) ([c8d6c7e](https://www.github.com/googleapis/python-shell/commit/c8d6c7ecf22d929963de5433f9d7abe7c7c402fd))

## [1.1.0](https://www.github.com/googleapis/python-shell/compare/v1.0.1...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#41](https://www.github.com/googleapis/python-shell/issues/41)) ([33eb545](https://www.github.com/googleapis/python-shell/commit/33eb545715c52bb3e8e04cba07ee84466ace672e))

### [1.0.1](https://www.github.com/googleapis/python-shell/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([c07f6c9](https://www.github.com/googleapis/python-shell/commit/c07f6c900b41a7513fa73a36544f62d429d1a36d))

## [1.0.0](https://www.github.com/googleapis/python-shell/compare/v0.2.2...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#25](https://www.github.com/googleapis/python-shell/issues/25)) ([9a1a44e](https://www.github.com/googleapis/python-shell/commit/9a1a44e65f4c9adc16bce134046752e10d04ce4b))

### [0.2.2](https://www.github.com/googleapis/python-shell/compare/v0.2.1...v0.2.2) (2021-07-30)


### Features

* add Samples section to CONTRIBUTING.rst ([#17](https://www.github.com/googleapis/python-shell/issues/17)) ([ce23d47](https://www.github.com/googleapis/python-shell/commit/ce23d475183fa3baa561f23c30d28cac09f6794d))


### Bug Fixes

* enable self signed jwt for grpc ([#21](https://www.github.com/googleapis/python-shell/issues/21)) ([0dafd2f](https://www.github.com/googleapis/python-shell/commit/0dafd2fbb839fcca38d6dc27b9fffff182f2add0))


### Miscellaneous Chores

* release as 0.2.2 ([#22](https://www.github.com/googleapis/python-shell/issues/22)) ([d3b208a](https://www.github.com/googleapis/python-shell/commit/d3b208aa33932c1008c5627d61bcd8dcf67aa85a))

### [0.2.1](https://www.github.com/googleapis/python-shell/compare/v0.2.0...v0.2.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#16](https://www.github.com/googleapis/python-shell/issues/16)) ([61b6123](https://www.github.com/googleapis/python-shell/commit/61b61231accd865e69f3a3b097e1c1c1a755f3bc))

## [0.2.0](https://www.github.com/googleapis/python-shell/compare/v0.1.0...v0.2.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#9](https://www.github.com/googleapis/python-shell/issues/9)) ([13ce7ba](https://www.github.com/googleapis/python-shell/commit/13ce7bab4613f287a73743d80d1bbbee5c59969a))


### Bug Fixes

* disable always_use_jwt_access ([b447260](https://www.github.com/googleapis/python-shell/commit/b4472606f4eb050b9135d5dd948d65ae065a1e04))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-shell/issues/1127)) ([#4](https://www.github.com/googleapis/python-shell/issues/4)) ([0150a5d](https://www.github.com/googleapis/python-shell/commit/0150a5d71e22b6aeb194cd2992d58ed03683d1ca)), closes [#1126](https://www.github.com/googleapis/python-shell/issues/1126)

## 0.1.0 (2021-06-13)


### Features

* generate v1 ([311a15b](https://www.github.com/googleapis/python-shell/commit/311a15b0a8ee3a4695e3922b549e534be5d019ab))
