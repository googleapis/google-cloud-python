# Changelog

## [0.2.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.11...google-cloud-parallelstore-v0.2.12) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([7295cbb](https://github.com/googleapis/google-cloud-python/commit/7295cbb7c3122eeff1042c3c543bfc9b8b3ca913))

## [0.2.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.10...google-cloud-parallelstore-v0.2.11) (2025-02-18)


### Features

* Adding `deployment_type` field ([03649eb](https://github.com/googleapis/google-cloud-python/commit/03649eb7f4b41de2981b1d49e7a6fc2bf20686d1))
* deprecating `daos_version` field ([03649eb](https://github.com/googleapis/google-cloud-python/commit/03649eb7f4b41de2981b1d49e7a6fc2bf20686d1))


### Documentation

* updated `directory_stripe_level` in message `.google.cloud.parallelstore.v1.Instance` to reflect that the field is now immutable ([03649eb](https://github.com/googleapis/google-cloud-python/commit/03649eb7f4b41de2981b1d49e7a6fc2bf20686d1))
* updated documentation for field `daos_version` in message `.google.cloud.parallelstore.v1.Instance` to reflect that the field is deprecated. ([03649eb](https://github.com/googleapis/google-cloud-python/commit/03649eb7f4b41de2981b1d49e7a6fc2bf20686d1))
* Updated field `file_stripe_level` in message `.google.cloud.parallelstore.v1.Instance` to reflected that message is now immutable ([03649eb](https://github.com/googleapis/google-cloud-python/commit/03649eb7f4b41de2981b1d49e7a6fc2bf20686d1))

## [0.2.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.9...google-cloud-parallelstore-v0.2.10) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))
* Add support for reading selective GAPIC generation methods from service YAML ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))

## [0.2.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.8...google-cloud-parallelstore-v0.2.9) (2025-01-13)


### Documentation

* [google-cloud-parallelstore] fix links in documentation ([#13409](https://github.com/googleapis/google-cloud-python/issues/13409)) ([b6874a2](https://github.com/googleapis/google-cloud-python/commit/b6874a224e01ccca6f0a5b9344440a1554945920))

## [0.2.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.7...google-cloud-parallelstore-v0.2.8) (2025-01-02)


### Documentation

* fix links in documentation ([e895308](https://github.com/googleapis/google-cloud-python/commit/e895308064e35edff15c7e9ba4146a89cb272e21))

## [0.2.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.6...google-cloud-parallelstore-v0.2.7) (2024-12-12)


### Features

* A new enum `DeploymentType` is added ([d406707](https://github.com/googleapis/google-cloud-python/commit/d406707a668e2dcbc80bda91cbe08ef9bf06b5b7))
* A new field `deployment_type` is added to message `.google.cloud.parallelstore.v1beta.Instance` ([d406707](https://github.com/googleapis/google-cloud-python/commit/d406707a668e2dcbc80bda91cbe08ef9bf06b5b7))
* Add support for opt-in debug logging ([d406707](https://github.com/googleapis/google-cloud-python/commit/d406707a668e2dcbc80bda91cbe08ef9bf06b5b7))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([d406707](https://github.com/googleapis/google-cloud-python/commit/d406707a668e2dcbc80bda91cbe08ef9bf06b5b7))

## [0.2.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.5...google-cloud-parallelstore-v0.2.6) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([170e8f2](https://github.com/googleapis/google-cloud-python/commit/170e8f2dda4d42842728797f24436a98f79a7bbc))

## [0.2.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.4...google-cloud-parallelstore-v0.2.5) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13208](https://github.com/googleapis/google-cloud-python/issues/13208)) ([a019409](https://github.com/googleapis/google-cloud-python/commit/a019409a5b5a983402301f1ac175d8b7e45c3818))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.3...google-cloud-parallelstore-v0.2.4) (2024-10-08)


### Features

* [google-cloud-parallelstore] adding v1 version of our api ([7f9bc3a](https://github.com/googleapis/google-cloud-python/commit/7f9bc3a7a504956eaf6eff5b80d77a15eda9e0b6))
* add UPGRADING state to Parallelstore state ([7f9bc3a](https://github.com/googleapis/google-cloud-python/commit/7f9bc3a7a504956eaf6eff5b80d77a15eda9e0b6))


### Documentation

* [google-cloud-parallelstore] cleanup of Parallelstore API descriptions ([7f9bc3a](https://github.com/googleapis/google-cloud-python/commit/7f9bc3a7a504956eaf6eff5b80d77a15eda9e0b6))
* [google-cloud-parallelstore] minor documentation formatting fix for Parallelstore ([7f9bc3a](https://github.com/googleapis/google-cloud-python/commit/7f9bc3a7a504956eaf6eff5b80d77a15eda9e0b6))
* minor documentation formatting fix for Parallelstore ([7f9bc3a](https://github.com/googleapis/google-cloud-python/commit/7f9bc3a7a504956eaf6eff5b80d77a15eda9e0b6))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.2...google-cloud-parallelstore-v0.2.3) (2024-08-01)


### Features

* [google-cloud-parallelstore] add file_stripe_level and directory_stripe_level fields to Instance ([#12970](https://github.com/googleapis/google-cloud-python/issues/12970)) ([17f4b3a](https://github.com/googleapis/google-cloud-python/commit/17f4b3ade3a159c87acedc36b48f69125d670c74))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.1...google-cloud-parallelstore-v0.2.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([d95af77](https://github.com/googleapis/google-cloud-python/commit/d95af77248f0935a5fe3dba1fccc75124c8b1451))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.2.0...google-cloud-parallelstore-v0.2.1) (2024-07-08)


### Features

* add [iam.googleapis.com/ServiceAccount](https://www.google.com/url?sa=D&q=http%3A%2F%2Fiam.googleapis.com%2FServiceAccount) resource definition ([e357c4d](https://github.com/googleapis/google-cloud-python/commit/e357c4dc2319f30c8c705440a7e80e16fc128b60))
* Adding Import/Export BYOSA to the import Data request ([e357c4d](https://github.com/googleapis/google-cloud-python/commit/e357c4dc2319f30c8c705440a7e80e16fc128b60))


### Bug Fixes

* Allow Protobuf 5.x ([#12868](https://github.com/googleapis/google-cloud-python/issues/12868)) ([0e39c1a](https://github.com/googleapis/google-cloud-python/commit/0e39c1a0ab46757bcf80a178d9bd422f6dcb24c6))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.1.2...google-cloud-parallelstore-v0.2.0) (2024-05-16)


### ⚠ BREAKING CHANGES

* An existing field `end_time` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata`
* An existing field `source` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata`
* An existing field `destination` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata`
* [google-cloud-parallelstore] An existing field `create_time` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata`
* An existing field `destination_path` is renamed to `destination_parallelstore` in message `.google.cloud.parallelstore.v1beta.ImportDataRequest`
* An existing field `source_path` is renamed to `source_parallelstore` in message `.google.cloud.parallelstore.v1beta.ExportDataRequest`
* An existing field `destination_gcs_uri` is renamed to `destination_gcs_bucket` in message `.google.cloud.parallelstore.v1beta.ExportDataRequest`
* An existing field `source_gcs_uri` is renamed to `source_gcs_bucket` in message `.google.cloud.parallelstore.v1beta.ImportDataRequest`

### Features

* A new field `api_version` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `api_version` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `create_time` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `create_time` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `destination_gcs_bucket` is added to message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `destination_parallelstore` is added to message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `end_time` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `end_time` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `requested_cancellation` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `requested_cancellation` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `source_gcs_bucket` is added to message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `source_parallelstore` is added to message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `status_message` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `status_message` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `target` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `target` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `verb` is added to message `.google.cloud.parallelstore.v1beta.ExportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new field `verb` is added to message `.google.cloud.parallelstore.v1beta.ImportDataMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A new message `DestinationGcsBucket` is added ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* A new message `DestinationParallelstore` is added ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* A new message `SourceGcsBucket` is added ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* A new message `SourceParallelstore` is added ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))


### Bug Fixes

* [google-cloud-parallelstore] An existing field `create_time` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* An existing field `destination_gcs_uri` is renamed to `destination_gcs_bucket` in message `.google.cloud.parallelstore.v1beta.ExportDataRequest` ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* An existing field `destination_path` is renamed to `destination_parallelstore` in message `.google.cloud.parallelstore.v1beta.ImportDataRequest` ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* An existing field `destination` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* An existing field `end_time` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* An existing field `source_gcs_uri` is renamed to `source_gcs_bucket` in message `.google.cloud.parallelstore.v1beta.ImportDataRequest` ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* An existing field `source_path` is renamed to `source_parallelstore` in message `.google.cloud.parallelstore.v1beta.ExportDataRequest` ([e3c48d7](https://github.com/googleapis/google-cloud-python/commit/e3c48d7661dbbdc9ee4fcd18c1572910615389fd))
* An existing field `source` is removed from message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))


### Documentation

* A comment for field `counters` in message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` is changed ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))
* A comment for field `transfer_type` in message `.google.cloud.parallelstore.v1beta.TransferOperationMetadata` is changed ([2f57a44](https://github.com/googleapis/google-cloud-python/commit/2f57a447ca30796c1ce993a593f3fee3328ff2b0))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.1.1...google-cloud-parallelstore-v0.1.2) (2024-05-07)


### Features

* **parallelstore/v1beta:** add ImportData and ExportData RPCs ([635ee31](https://github.com/googleapis/google-cloud-python/commit/635ee31d44fffd0bfee050b685700dbb3be4d46f))


### Documentation

* fix typo in Instance.reserved_ip_range field doc ([635ee31](https://github.com/googleapis/google-cloud-python/commit/635ee31d44fffd0bfee050b685700dbb3be4d46f))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-parallelstore-v0.1.0...google-cloud-parallelstore-v0.1.1) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12386](https://github.com/googleapis/google-cloud-python/issues/12386)) ([edcad16](https://github.com/googleapis/google-cloud-python/commit/edcad1661973ae1677c69b3fc1c03c3069ec0e71))

## 0.1.0 (2024-03-04)


### Features

* add initial files for google.cloud.parallelstore.v1beta ([#12368](https://github.com/googleapis/google-cloud-python/issues/12368)) ([db14111](https://github.com/googleapis/google-cloud-python/commit/db1411133fbdd2ee333aca125dd05996c7a95f59))

## Changelog
