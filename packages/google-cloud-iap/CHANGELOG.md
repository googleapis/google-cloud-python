# Changelog

## [1.4.0](https://github.com/googleapis/python-iap/compare/v1.3.1...v1.4.0) (2022-05-19)


### Features

* add ReauthSettings to the UpdateIapSettingsRequest ([36c1866](https://github.com/googleapis/python-iap/commit/36c1866e605e4e880e65eb44a7d4dc49389f92f3))
* add the TunnelDestGroup-related methods and types ([#93](https://github.com/googleapis/python-iap/issues/93)) ([36c1866](https://github.com/googleapis/python-iap/commit/36c1866e605e4e880e65eb44a7d4dc49389f92f3))
* AuditConfig for IAM v1 ([49dc9c7](https://github.com/googleapis/python-iap/commit/49dc9c7162e956c684892bdf866f20b47e3b27d2))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([49dc9c7](https://github.com/googleapis/python-iap/commit/49dc9c7162e956c684892bdf866f20b47e3b27d2))

### [1.3.1](https://github.com/googleapis/python-iap/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#71](https://github.com/googleapis/python-iap/issues/71)) ([0e00d6a](https://github.com/googleapis/python-iap/commit/0e00d6a489ee97707bb733387a951e48e1f415dc))

## [1.3.0](https://github.com/googleapis/python-iap/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#57](https://github.com/googleapis/python-iap/issues/57)) ([1787cb0](https://github.com/googleapis/python-iap/commit/1787cb00158f111915d0f9bb948abeceab75a6f4))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([18f725d](https://github.com/googleapis/python-iap/commit/18f725d81007e02d2054538087d7567029b2d179))


### Documentation

* add generated snippets ([#62](https://github.com/googleapis/python-iap/issues/62)) ([27c14d2](https://github.com/googleapis/python-iap/commit/27c14d24ce50d6bb80f09218bcf0ebc1db9ceabd))

### [1.2.1](https://www.github.com/googleapis/python-iap/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([30b353c](https://www.github.com/googleapis/python-iap/commit/30b353c9296d37f8792759a5ee997b3f50572f19))
* **deps:** require google-api-core >= 1.28.0 ([30b353c](https://www.github.com/googleapis/python-iap/commit/30b353c9296d37f8792759a5ee997b3f50572f19))


### Documentation

* list oneofs in docstring ([30b353c](https://www.github.com/googleapis/python-iap/commit/30b353c9296d37f8792759a5ee997b3f50572f19))

## [1.2.0](https://www.github.com/googleapis/python-iap/compare/v1.1.0...v1.2.0) (2021-10-18)


### Features

* add support for python 3.10 ([#37](https://www.github.com/googleapis/python-iap/issues/37)) ([7716426](https://www.github.com/googleapis/python-iap/commit/7716426b83a457a3206fae1dee66c46cf35bd7e7))

## [1.1.0](https://www.github.com/googleapis/python-iap/compare/v1.0.2...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#34](https://www.github.com/googleapis/python-iap/issues/34)) ([a985591](https://www.github.com/googleapis/python-iap/commit/a985591b016e768a5a172ab5f8de873319b1e7e0))

### [1.0.2](https://www.github.com/googleapis/python-iap/compare/v1.0.1...v1.0.2) (2021-10-05)


### Bug Fixes

* improper types in pagers generation ([242d445](https://www.github.com/googleapis/python-iap/commit/242d44516fe55141a26024653158ea94fa93e525))

### [1.0.1](https://www.github.com/googleapis/python-iap/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([a5b27d2](https://www.github.com/googleapis/python-iap/commit/a5b27d26e4bc845aeede7281959a81f693ee52c2))

## [1.0.0](https://www.github.com/googleapis/python-iap/compare/v0.1.2...v1.0.0) (2021-08-09)


### Features

* bump release level to production/stable ([#13](https://www.github.com/googleapis/python-iap/issues/13)) ([9d0a9f8](https://www.github.com/googleapis/python-iap/commit/9d0a9f84554b98fd2b1829532c9c13b16432b0af))

### [0.1.2](https://www.github.com/googleapis/python-iap/compare/v0.1.1...v0.1.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#9](https://www.github.com/googleapis/python-iap/issues/9)) ([51304a3](https://www.github.com/googleapis/python-iap/commit/51304a327207a233e40308a8b49c9fdeda87c28b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#5](https://www.github.com/googleapis/python-iap/issues/5)) ([2ba31c5](https://www.github.com/googleapis/python-iap/commit/2ba31c5a2ea2e52c4a79410548a252bf8fc0522e))


### Miscellaneous Chores

* release as 0.1.2 ([#10](https://www.github.com/googleapis/python-iap/issues/10)) ([4499ba5](https://www.github.com/googleapis/python-iap/commit/4499ba5ccd90edc882fbda73e4d792074ff44e6d))

### [0.1.1](https://www.github.com/googleapis/python-iap/compare/v0.1.0...v0.1.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#4](https://www.github.com/googleapis/python-iap/issues/4)) ([21e9e57](https://www.github.com/googleapis/python-iap/commit/21e9e57451a87d9f9dd1137142d138cb73aa746c))

## 0.1.0 (2021-07-06)


### Features

* generate v1 ([6fdf055](https://www.github.com/googleapis/python-iap/commit/6fdf055c835adf6715bf43e9255d02abcd2affd4))
