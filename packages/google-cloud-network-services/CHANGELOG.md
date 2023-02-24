# Changelog

## [0.5.0](https://github.com/googleapis/python-network-services/compare/v0.4.1...v0.5.0) (2023-02-09)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#70](https://github.com/googleapis/python-network-services/issues/70)) ([ccfdcec](https://github.com/googleapis/python-network-services/commit/ccfdcecec0f5d187260d3753039ddb0090b39346))

## [0.4.1](https://github.com/googleapis/python-network-services/compare/v0.4.0...v0.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([2e8534f](https://github.com/googleapis/python-network-services/commit/2e8534f860d789225a27497223f0edf17befc5dd))


### Documentation

* Add documentation for enums ([2e8534f](https://github.com/googleapis/python-network-services/commit/2e8534f860d789225a27497223f0edf17befc5dd))

## [0.4.0](https://github.com/googleapis/python-network-services/compare/v0.3.0...v0.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#61](https://github.com/googleapis/python-network-services/issues/61)) ([9fece25](https://github.com/googleapis/python-network-services/commit/9fece25c41d10677764ef70286786bb90f535842))

## [0.3.0](https://github.com/googleapis/python-network-services/compare/v0.2.2...v0.3.0) (2022-12-15)


### Features

* Add support for `google.cloud.network_services.__version__` ([9b6c478](https://github.com/googleapis/python-network-services/commit/9b6c478c95590aac6602217e80e346895e99ecf4))
* Add typing to proto.Message based class attributes ([9b6c478](https://github.com/googleapis/python-network-services/commit/9b6c478c95590aac6602217e80e346895e99ecf4))


### Bug Fixes

* Add dict typing for client_options ([9b6c478](https://github.com/googleapis/python-network-services/commit/9b6c478c95590aac6602217e80e346895e99ecf4))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([c0ecbf1](https://github.com/googleapis/python-network-services/commit/c0ecbf1430820b0415cb8ae02e18d4a687e6fd45))
* Drop usage of pkg_resources ([c0ecbf1](https://github.com/googleapis/python-network-services/commit/c0ecbf1430820b0415cb8ae02e18d4a687e6fd45))
* Fix timeout default values ([c0ecbf1](https://github.com/googleapis/python-network-services/commit/c0ecbf1430820b0415cb8ae02e18d4a687e6fd45))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([9b6c478](https://github.com/googleapis/python-network-services/commit/9b6c478c95590aac6602217e80e346895e99ecf4))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([c0ecbf1](https://github.com/googleapis/python-network-services/commit/c0ecbf1430820b0415cb8ae02e18d4a687e6fd45))

## [0.2.2](https://github.com/googleapis/python-network-services/compare/v0.2.1...v0.2.2) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#50](https://github.com/googleapis/python-network-services/issues/50)) ([c05d701](https://github.com/googleapis/python-network-services/commit/c05d7015b39317876ec7d63819345ef63431a3cc))

## [0.2.1](https://github.com/googleapis/python-network-services/compare/v0.2.0...v0.2.1) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#48](https://github.com/googleapis/python-network-services/issues/48)) ([9f82686](https://github.com/googleapis/python-network-services/commit/9f826865f03ad0a29910b94e0fbbc184e57b5695))

## [0.2.0](https://github.com/googleapis/python-network-services/compare/v0.1.1...v0.2.0) (2022-08-11)


### Features

* add audience parameter ([42ab6e0](https://github.com/googleapis/python-network-services/commit/42ab6e04f356f1b65a805944ef07a780b95a02a9))
* Add Service Directory Service API ([42ab6e0](https://github.com/googleapis/python-network-services/commit/42ab6e04f356f1b65a805944ef07a780b95a02a9))
* Add traffic director API ([#22](https://github.com/googleapis/python-network-services/issues/22)) ([42ab6e0](https://github.com/googleapis/python-network-services/commit/42ab6e04f356f1b65a805944ef07a780b95a02a9))


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#31](https://github.com/googleapis/python-network-services/issues/31)) ([2ec0e05](https://github.com/googleapis/python-network-services/commit/2ec0e054b18243b7b157e0a59ac5acfe6864ae3c))
* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([42ab6e0](https://github.com/googleapis/python-network-services/commit/42ab6e04f356f1b65a805944ef07a780b95a02a9))
* **deps:** require grpc-google-iam-v1 >=0.12.4 ([42ab6e0](https://github.com/googleapis/python-network-services/commit/42ab6e04f356f1b65a805944ef07a780b95a02a9))
* **deps:** require proto-plus >= 1.22.0 ([2ec0e05](https://github.com/googleapis/python-network-services/commit/2ec0e054b18243b7b157e0a59ac5acfe6864ae3c))
* require python 3.7+ ([#24](https://github.com/googleapis/python-network-services/issues/24)) ([86b9b43](https://github.com/googleapis/python-network-services/commit/86b9b43f15fbe341c6f9eddfa7a520185c2d2668))

## [0.1.1](https://github.com/googleapis/python-network-services/compare/v0.1.0...v0.1.1) (2022-06-07)


### Bug Fixes

* **deps:** require protobuf>=3.19.0,<4.0.0 ([#16](https://github.com/googleapis/python-network-services/issues/16)) ([dea0f13](https://github.com/googleapis/python-network-services/commit/dea0f136a38d10de086985878ed3676e40b1444c))

## 0.1.0 (2022-04-15)


### Features

* generate v1 ([7a064d3](https://github.com/googleapis/python-network-services/commit/7a064d306d46663e1284a77411d2404576a4a5e7))
