# Changelog

## [1.4.3](https://github.com/googleapis/python-dataplex/compare/v1.4.2...v1.4.3) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#131](https://github.com/googleapis/python-dataplex/issues/131)) ([3ebb439](https://github.com/googleapis/python-dataplex/commit/3ebb439e786fecda33956c3eac2b0b3f451bedb1))

## [1.4.2](https://github.com/googleapis/python-dataplex/compare/v1.4.1...v1.4.2) (2023-02-02)


### Documentation

* Improvements to DataScan API documentation ([#123](https://github.com/googleapis/python-dataplex/issues/123)) ([a7e193f](https://github.com/googleapis/python-dataplex/commit/a7e193fb2cb0475ae1f75bb412967ec4436686e5))

## [1.4.1](https://github.com/googleapis/python-dataplex/compare/v1.4.0...v1.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([eb88024](https://github.com/googleapis/python-dataplex/commit/eb88024e41d4832ecd0e970ff7a87f57d74bba2a))


### Documentation

* Add documentation for enums ([eb88024](https://github.com/googleapis/python-dataplex/commit/eb88024e41d4832ecd0e970ff7a87f57d74bba2a))

## [1.4.0](https://github.com/googleapis/python-dataplex/compare/v1.3.0...v1.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#117](https://github.com/googleapis/python-dataplex/issues/117)) ([18c78d6](https://github.com/googleapis/python-dataplex/commit/18c78d63864fe2f7080f80d5faf3b0672e0d99d7))

## [1.3.0](https://github.com/googleapis/python-dataplex/compare/v1.2.0...v1.3.0) (2023-01-05)


### Features

* Added StorageFormat.iceberg ([16871c0](https://github.com/googleapis/python-dataplex/commit/16871c05637ef68bb99d9dc6b471dc029f368009))
* DataScans service ([16871c0](https://github.com/googleapis/python-dataplex/commit/16871c05637ef68bb99d9dc6b471dc029f368009))

## [1.2.0](https://github.com/googleapis/python-dataplex/compare/v1.1.2...v1.2.0) (2022-12-15)


### Features

* Add support for `google.cloud.dataplex.__version__` ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* Add support for notebook tasks ([#100](https://github.com/googleapis/python-dataplex/issues/100)) ([64d9c48](https://github.com/googleapis/python-dataplex/commit/64d9c481df1c2737189dcb575c69f2968c0aa034))
* Add typing to proto.Message based class attributes ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))


### Bug Fixes

* Add dict typing for client_options ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* **deps:** Allow protobuf 3.19.5 ([#103](https://github.com/googleapis/python-dataplex/issues/103)) ([65adbb3](https://github.com/googleapis/python-dataplex/commit/65adbb31c94794f27a78b309550c519734a7b030))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))
* Drop usage of pkg_resources ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))
* Fix timeout default values ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))


### Documentation

* Fix minor docstring formatting ([#113](https://github.com/googleapis/python-dataplex/issues/113)) ([0dc28b3](https://github.com/googleapis/python-dataplex/commit/0dc28b3c0f2c5be59a279c9ff859607d25906e84))
* **samples:** Snippetgen handling of repeated enum field ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))

## [1.1.2](https://github.com/googleapis/python-dataplex/compare/v1.1.1...v1.1.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#98](https://github.com/googleapis/python-dataplex/issues/98)) ([1b178ce](https://github.com/googleapis/python-dataplex/commit/1b178ce8f12ed542bbe19736f9a416aa35c73828))

## [1.1.1](https://github.com/googleapis/python-dataplex/compare/v1.1.0...v1.1.1) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#84](https://github.com/googleapis/python-dataplex/issues/84)) ([747f4d9](https://github.com/googleapis/python-dataplex/commit/747f4d9fe8d4dbfeaf5576197c495edb6392a89f))
* **deps:** require proto-plus >= 1.22.0 ([747f4d9](https://github.com/googleapis/python-dataplex/commit/747f4d9fe8d4dbfeaf5576197c495edb6392a89f))

## [1.1.0](https://github.com/googleapis/python-dataplex/compare/v1.0.1...v1.1.0) (2022-07-15)


### Features

* add audience parameter ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add IAM support for Explore content APIs ([#74](https://github.com/googleapis/python-dataplex/issues/74)) ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for cross project for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for custom container for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for custom encryption key to be used for encrypt data on the PDs associated with the VMs in your Dataproc cluster for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for Latest job in Task resource ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Support logging sampled file paths per partition to Cloud logging for Discovery event ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* User mode filter in Explore list sessions API ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* **deps:** require grpc-google-iam-v1 >=0.12.4 ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* require python 3.7+ ([#76](https://github.com/googleapis/python-dataplex/issues/76)) ([3cd158c](https://github.com/googleapis/python-dataplex/commit/3cd158c8a3b782683b5485d28bc14dadea852deb))

## [1.0.1](https://github.com/googleapis/python-dataplex/compare/v1.0.0...v1.0.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#66](https://github.com/googleapis/python-dataplex/issues/66)) ([0faef94](https://github.com/googleapis/python-dataplex/commit/0faef94bbd9371e41a18aa0372b1f59865010cab))


### Documentation

* fix changelog header to consistent size ([#67](https://github.com/googleapis/python-dataplex/issues/67)) ([3090fd6](https://github.com/googleapis/python-dataplex/commit/3090fd6d011e2a482e46a1c19c5e87a1aa90de35))

## [1.0.0](https://github.com/googleapis/python-dataplex/compare/v0.2.1...v1.0.0) (2022-04-26)


### Features

* bump release level to production/stable  ([b13ce8f](https://github.com/googleapis/python-dataplex/commit/b13ce8f2fda0dc60e8d1ed88e846fd8c027546e0))

## [0.2.1](https://github.com/googleapis/python-dataplex/compare/v0.2.0...v0.2.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#18](https://github.com/googleapis/python-dataplex/issues/18)) ([10b7809](https://github.com/googleapis/python-dataplex/commit/10b7809287befb914fdbe7cef3b1bded0eb7b63b))

## [0.2.0](https://github.com/googleapis/python-dataplex/compare/v0.1.0...v0.2.0) (2022-02-26)


### Features

* Added Create, Update and Delete APIs for Metadata (e.g. Entity and/or Partition). ([1333110](https://github.com/googleapis/python-dataplex/commit/13331107c96cb4d1e725eae291c9fee7316e6e72))
* Added support for Content APIs ([#8](https://github.com/googleapis/python-dataplex/issues/8)) ([1333110](https://github.com/googleapis/python-dataplex/commit/13331107c96cb4d1e725eae291c9fee7316e6e72))

## 0.1.0 (2022-01-28)


### Features

* generate v1 ([f29b530](https://github.com/googleapis/python-dataplex/commit/f29b5309dfad9df04c0dc564e065195ae33985b8))
