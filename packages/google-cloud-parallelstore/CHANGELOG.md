# Changelog

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
