# Changelog

## [1.5.1](https://github.com/googleapis/python-dataproc-metastore/compare/v1.5.0...v1.5.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#147](https://github.com/googleapis/python-dataproc-metastore/issues/147)) ([776fe97](https://github.com/googleapis/python-dataproc-metastore/commit/776fe97db292998b8bb68e13953c2ca057502b2f))


### Documentation

* fix changelog header to consistent size ([#148](https://github.com/googleapis/python-dataproc-metastore/issues/148)) ([0f93c4e](https://github.com/googleapis/python-dataproc-metastore/commit/0f93c4e5ab1a663c2b8350b5b2827eacced8548d))

## [1.5.0](https://github.com/googleapis/python-dataproc-metastore/compare/v1.4.1...v1.5.0) (2022-03-21)


### Features

* Added additional endTime field for MetadataImports ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added AuxiliaryVersionConfig for configuring the auxiliary hive versions during creation or update of the DPMS instance ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added AVRO DatabaseDumpSpec for importing and exporting Avro files ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added configuration for Dataplex integration ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added DatabaseType field for the type of backing store used ([#122](https://github.com/googleapis/python-dataproc-metastore/issues/122)) ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added EncryptionConfig which contains information used to configure the Dataproc Metastore service to encrypt customer data at rest (CMEK) ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added NetworkConfig for exposing the DPMS endpoint in multiple subnetworks using PSC (this skips the need for VPC peering) ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added RESTORING status on Backups ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added support for IAM management for metadata resources ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))
* Added support to record the services that are restoring the backup ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))


### Documentation

* formatting improvements ([0a768dd](https://github.com/googleapis/python-dataproc-metastore/commit/0a768dd7f9541231f124d7ff6cd1c9c8a497c1ed))

## [1.4.1](https://github.com/googleapis/python-dataproc-metastore/compare/v1.4.0...v1.4.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#119](https://github.com/googleapis/python-dataproc-metastore/issues/119)) ([e079039](https://github.com/googleapis/python-dataproc-metastore/commit/e079039025a92e686e9348a0f06241fcd3cd50b5))
* **deps:** require proto-plus>=1.15.0 ([e079039](https://github.com/googleapis/python-dataproc-metastore/commit/e079039025a92e686e9348a0f06241fcd3cd50b5))

## [1.4.0](https://github.com/googleapis/python-dataproc-metastore/compare/v1.3.1...v1.4.0) (2022-02-26)


### Features

* add api key support ([#105](https://github.com/googleapis/python-dataproc-metastore/issues/105)) ([f8d7bb8](https://github.com/googleapis/python-dataproc-metastore/commit/f8d7bb845079cb98a1f4d18ad68a6b3958541d51))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([61baf5c](https://github.com/googleapis/python-dataproc-metastore/commit/61baf5c79541ce85a8012bf8ada5127381a4c813))


### Documentation

* add generated snippets ([#110](https://github.com/googleapis/python-dataproc-metastore/issues/110)) ([30373ff](https://github.com/googleapis/python-dataproc-metastore/commit/30373ffee9aa49c4c23a421ad36da141bf06156d))

## [1.3.1](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.3.0...v1.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([7abadeb](https://www.github.com/googleapis/python-dataproc-metastore/commit/7abadeb6de0d3e7e45f6d38eeac7abc9a76bca24))
* **deps:** require google-api-core >= 1.28.0 ([7abadeb](https://www.github.com/googleapis/python-dataproc-metastore/commit/7abadeb6de0d3e7e45f6d38eeac7abc9a76bca24))


### Documentation

* list oneofs in docstring ([7abadeb](https://www.github.com/googleapis/python-dataproc-metastore/commit/7abadeb6de0d3e7e45f6d38eeac7abc9a76bca24))

## [1.3.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.2.0...v1.3.0) (2021-10-13)


### Features

* add support for python 3.10 ([#86](https://www.github.com/googleapis/python-dataproc-metastore/issues/86)) ([1ef7b30](https://www.github.com/googleapis/python-dataproc-metastore/commit/1ef7b30871217713eb7be9294044ebe5fa72909a))

## [1.2.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.1.2...v1.2.0) (2021-10-08)


### Features

* add context manager support in client ([#83](https://www.github.com/googleapis/python-dataproc-metastore/issues/83)) ([d6b8569](https://www.github.com/googleapis/python-dataproc-metastore/commit/d6b85696e21df07a63c93f5e993972fba157aa77))

## [1.1.2](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.1.1...v1.1.2) (2021-10-05)


### Bug Fixes

* improper types in pagers generation ([fd7978b](https://www.github.com/googleapis/python-dataproc-metastore/commit/fd7978b1e2552dd47ea4ecf109d6266d165766b9))

## [1.1.1](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.1.0...v1.1.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([63a6c45](https://www.github.com/googleapis/python-dataproc-metastore/commit/63a6c4551c9e68502379a1efdd0d00cfab529633))

## [1.1.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v1.0.0...v1.1.0) (2021-08-17)


### Features

* Added the Backup resource and Backup resource GetIamPolicy/SetIamPolicy to V1 feat: Added the RestoreService method to V1 ([#63](https://www.github.com/googleapis/python-dataproc-metastore/issues/63)) ([483cc6e](https://www.github.com/googleapis/python-dataproc-metastore/commit/483cc6e90eff74e746adcb2e5ea67decc64aa217))

## [1.0.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.3.1...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#59](https://www.github.com/googleapis/python-dataproc-metastore/issues/59)) ([434ca20](https://www.github.com/googleapis/python-dataproc-metastore/commit/434ca203c9ffad48f96d6a8c45de81a5ec74bd2b))

## [0.3.1](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.3.0...v0.3.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#50](https://www.github.com/googleapis/python-dataproc-metastore/issues/50)) ([091ff2f](https://www.github.com/googleapis/python-dataproc-metastore/commit/091ff2fa0cc9413c99cb3c17a18af9de131bca01))
* enable self signed jwt for grpc ([#56](https://www.github.com/googleapis/python-dataproc-metastore/issues/56)) ([3f94f5a](https://www.github.com/googleapis/python-dataproc-metastore/commit/3f94f5adb30d4e9a6e28424259a9a26b78429740))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#51](https://www.github.com/googleapis/python-dataproc-metastore/issues/51)) ([c093c12](https://www.github.com/googleapis/python-dataproc-metastore/commit/c093c1282e832f3d7a027d63be1b55017bcec9ff))


### Miscellaneous Chores

* release 0.3.1 ([#55](https://www.github.com/googleapis/python-dataproc-metastore/issues/55)) ([2a846dd](https://www.github.com/googleapis/python-dataproc-metastore/commit/2a846ddef298a09baf7ff27331cd438f8f7113ee))

## [0.3.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.2.2...v0.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#43](https://www.github.com/googleapis/python-dataproc-metastore/issues/43)) ([75cf2ee](https://www.github.com/googleapis/python-dataproc-metastore/commit/75cf2ee2204211be6f43d94bf78cfa7f02ba1976))


### Bug Fixes

* disable always_use_jwt_access ([#47](https://www.github.com/googleapis/python-dataproc-metastore/issues/47)) ([903b08e](https://www.github.com/googleapis/python-dataproc-metastore/commit/903b08e9436691a92f5557d3e8a0a49612d4d8db))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-dataproc-metastore/issues/1127)) ([#38](https://www.github.com/googleapis/python-dataproc-metastore/issues/38)) ([9b8c147](https://www.github.com/googleapis/python-dataproc-metastore/commit/9b8c14739b9cb5d02f9372d952acf099712f9826)), closes [#1126](https://www.github.com/googleapis/python-dataproc-metastore/issues/1126)

## [0.2.2](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.2.1...v0.2.2) (2021-06-16)


### Bug Fixes

* **deps:** add packaging requirement ([#35](https://www.github.com/googleapis/python-dataproc-metastore/issues/35)) ([922536c](https://www.github.com/googleapis/python-dataproc-metastore/commit/922536c93fe70eb0052843c6cb9f9a7c91046a81))

## [0.2.1](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.2.0...v0.2.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#33](https://www.github.com/googleapis/python-dataproc-metastore/issues/33)) ([dfaec68](https://www.github.com/googleapis/python-dataproc-metastore/commit/dfaec68833ded607fd0514d73b10e0d33dc26c72))

## [0.2.0](https://www.github.com/googleapis/python-dataproc-metastore/compare/v0.1.0...v0.2.0) (2021-06-02)


### Features

* add v1 ([#28](https://www.github.com/googleapis/python-dataproc-metastore/issues/28)) ([4d054d9](https://www.github.com/googleapis/python-dataproc-metastore/commit/4d054d92fed4296883e5ae09b99d57bd74d68fb4))

## 0.1.0 (2021-03-15)


### Features

* generate v1alpha ([2c025f8](https://www.github.com/googleapis/python-dataproc-metastore/commit/2c025f80c7791ef864ce2bf655429e1ecf40d288))
* generate v1beta ([942ddcd](https://www.github.com/googleapis/python-dataproc-metastore/commit/942ddcd6ddd18bd6d79cf2c57685a743ea35a376))
