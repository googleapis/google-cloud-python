# Changelog

## [1.6.1](https://github.com/googleapis/python-billing/compare/v1.6.0...v1.6.1) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#185](https://github.com/googleapis/python-billing/issues/185)) ([2542e90](https://github.com/googleapis/python-billing/commit/2542e902b8c23cbb9b84d2e6e266689e80102884))


### Documentation

* fix changelog header to consistent size ([#186](https://github.com/googleapis/python-billing/issues/186)) ([0b7c05e](https://github.com/googleapis/python-billing/commit/0b7c05ea4038a68b8648e0594f5cd0c05255f381))

## [1.6.0](https://github.com/googleapis/python-billing/compare/v1.5.1...v1.6.0) (2022-05-05)


### Features

* AuditConfig for IAM v1 ([6ce587c](https://github.com/googleapis/python-billing/commit/6ce587c58fb76d0f2f2ff5c9bcfc25a8f307071d))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([6ce587c](https://github.com/googleapis/python-billing/commit/6ce587c58fb76d0f2f2ff5c9bcfc25a8f307071d))


### Documentation

* fix type in docstring for map fields ([6ce587c](https://github.com/googleapis/python-billing/commit/6ce587c58fb76d0f2f2ff5c9bcfc25a8f307071d))

## [1.5.1](https://github.com/googleapis/python-billing/compare/v1.5.0...v1.5.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#159](https://github.com/googleapis/python-billing/issues/159)) ([d5511db](https://github.com/googleapis/python-billing/commit/d5511dbae66858b39f95ab989a1049d84ea57e49))
* **deps:** require proto-plus>=1.15.0 ([d5511db](https://github.com/googleapis/python-billing/commit/d5511dbae66858b39f95ab989a1049d84ea57e49))

## [1.5.0](https://github.com/googleapis/python-billing/compare/v1.4.1...v1.5.0) (2022-02-26)


### Features

* add api key support ([#145](https://github.com/googleapis/python-billing/issues/145)) ([a434c2e](https://github.com/googleapis/python-billing/commit/a434c2eb1ec6a79c36409c6039f05501c9cfc113))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([7b94621](https://github.com/googleapis/python-billing/commit/7b94621dafbcda8a549dd849337ba51fa5305f56))

## [1.4.1](https://www.github.com/googleapis/python-billing/compare/v1.4.0...v1.4.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([11ee1bf](https://www.github.com/googleapis/python-billing/commit/11ee1bfd84cfddcdc60ee2500273f5016919eba1))
* **deps:** require google-api-core >= 1.28.0 ([11ee1bf](https://www.github.com/googleapis/python-billing/commit/11ee1bfd84cfddcdc60ee2500273f5016919eba1))


### Documentation

* list oneofs in docstring ([11ee1bf](https://www.github.com/googleapis/python-billing/commit/11ee1bfd84cfddcdc60ee2500273f5016919eba1))

## [1.4.0](https://www.github.com/googleapis/python-billing/compare/v1.3.4...v1.4.0) (2021-10-11)


### Features

* add context manager support in client ([#122](https://www.github.com/googleapis/python-billing/issues/122)) ([9ec2297](https://www.github.com/googleapis/python-billing/commit/9ec229702b9a116e2572dd10c3e40887dfd70f93))
* add trove classifier for python 3.10 ([#125](https://www.github.com/googleapis/python-billing/issues/125)) ([6b93726](https://www.github.com/googleapis/python-billing/commit/6b93726fba956a41edf7d71f4950c649bc87f96f))

## [1.3.4](https://www.github.com/googleapis/python-billing/compare/v1.3.3...v1.3.4) (2021-10-04)


### Bug Fixes

* improper types in pagers generation ([578aeef](https://www.github.com/googleapis/python-billing/commit/578aeefcde72f12063e54e86208e3c6c4b135885))

## [1.3.3](https://www.github.com/googleapis/python-billing/compare/v1.3.2...v1.3.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([51f7055](https://www.github.com/googleapis/python-billing/commit/51f7055f3a992902f60342de389ec261147e98af))

## [1.3.2](https://www.github.com/googleapis/python-billing/compare/v1.3.1...v1.3.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#101](https://www.github.com/googleapis/python-billing/issues/101)) ([261507e](https://www.github.com/googleapis/python-billing/commit/261507e86d5e14a435fa74dea96feff187cd4f87))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#97](https://www.github.com/googleapis/python-billing/issues/97)) ([05b63b3](https://www.github.com/googleapis/python-billing/commit/05b63b3f88cb7cbc77db9daedf34db5617f93ca8))


### Miscellaneous Chores

* release as 1.3.2 ([#102](https://www.github.com/googleapis/python-billing/issues/102)) ([da74027](https://www.github.com/googleapis/python-billing/commit/da74027594f06705a9f6c2fe33241514e71379b4))

## [1.3.1](https://www.github.com/googleapis/python-billing/compare/v1.3.0...v1.3.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#96](https://www.github.com/googleapis/python-billing/issues/96)) ([a9e5368](https://www.github.com/googleapis/python-billing/commit/a9e536849aea8fe4ba513cd5503c275c4a7db880))

## [1.3.0](https://www.github.com/googleapis/python-billing/compare/v1.2.1...v1.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#86](https://www.github.com/googleapis/python-billing/issues/86)) ([7ff02d6](https://www.github.com/googleapis/python-billing/commit/7ff02d68336e9a5d51dba0e03e6e9332d6080cf9))


### Bug Fixes

* disable always_use_jwt_access ([cff1d3e](https://www.github.com/googleapis/python-billing/commit/cff1d3e7d191321914003bc1d677954bfea49304))
* disable always_use_jwt_access ([#93](https://www.github.com/googleapis/python-billing/issues/93)) ([cff1d3e](https://www.github.com/googleapis/python-billing/commit/cff1d3e7d191321914003bc1d677954bfea49304))


### Documentation

* include client library documentation in README.rst ([#91](https://www.github.com/googleapis/python-billing/issues/91)) ([3a6999d](https://www.github.com/googleapis/python-billing/commit/3a6999d6196f8d5ea1a92f4304c60fd3c2cc549c))
* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-billing/issues/1127)) ([#82](https://www.github.com/googleapis/python-billing/issues/82)) ([634d7b0](https://www.github.com/googleapis/python-billing/commit/634d7b01fba7d834b0acfd3a2ee1357260f0b695))

## [1.2.1](https://www.github.com/googleapis/python-billing/compare/v1.2.0...v1.2.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#79](https://www.github.com/googleapis/python-billing/issues/79)) ([f2fc441](https://www.github.com/googleapis/python-billing/commit/f2fc4412c677c5648cbe12a86f01699118279a56))

## [1.2.0](https://www.github.com/googleapis/python-billing/compare/v1.1.1...v1.2.0) (2021-05-28)


### Features

* add from_service_account_info factory and fix sphinx identifiers ([#42](https://www.github.com/googleapis/python-billing/issues/42)) ([95ba269](https://www.github.com/googleapis/python-billing/commit/95ba26961090dc76e75064cba10c21ca4897675e))
* support self-signed JWT flow for service accounts ([a2a6aaf](https://www.github.com/googleapis/python-billing/commit/a2a6aaf71864cd1a9e093fd77f6426e2a39ebe25))


### Bug Fixes

* add async client to %name_%version/init.py ([a2a6aaf](https://www.github.com/googleapis/python-billing/commit/a2a6aaf71864cd1a9e093fd77f6426e2a39ebe25))
* **deps:** add packaging requirement ([#75](https://www.github.com/googleapis/python-billing/issues/75)) ([73d8957](https://www.github.com/googleapis/python-billing/commit/73d895725d396d7f930c8259dfbec269897a5b62))

## [1.1.1](https://www.github.com/googleapis/python-billing/compare/v1.1.0...v1.1.1) (2021-02-11)


### Bug Fixes

* update retry and timeout settings ([#38](https://www.github.com/googleapis/python-billing/issues/38)) ([8dbad86](https://www.github.com/googleapis/python-billing/commit/8dbad869521924fc3f7d7dc2d4f5d7e9100874b3))

## [1.1.0](https://www.github.com/googleapis/python-billing/compare/v1.0.0...v1.1.0) (2020-11-17)


### Features

* add async client, support credentials_file and scopes client options ([#29](https://www.github.com/googleapis/python-billing/issues/29)) ([4177eb5](https://www.github.com/googleapis/python-billing/commit/4177eb53544392931a17a6fc8e51b24c69698969))
* add mtls support ([#19](https://www.github.com/googleapis/python-billing/issues/19)) ([fef622a](https://www.github.com/googleapis/python-billing/commit/fef622a0dddf005d8af329ee001ec41f03850427))

## [1.0.0](https://www.github.com/googleapis/python-billing/compare/v0.1.0...v1.0.0) (2020-05-18)


### Features

* release as production/stable ([#15](https://www.github.com/googleapis/python-billing/issues/15)) ([80a4fed](https://www.github.com/googleapis/python-billing/commit/80a4fed5aea4349b4f6d4e2b4a387c6cb8136295))


### Bug Fixes

* correct link to docs ([#5](https://www.github.com/googleapis/python-billing/issues/5)) ([3d87965](https://www.github.com/googleapis/python-billing/commit/3d879653ad5e1b45aadb856796c6db68145c51f4))

## 0.1.0 (2020-02-28)


### Features

* generate v1 ([61db762](https://www.github.com/googleapis/python-billing/commit/61db76297352fc61f65130dfbf50e3dfa7620fd8))
