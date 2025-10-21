# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-memorystore/#history

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-memorystore-v0.1.3...google-cloud-memorystore-v0.2.0) (2025-10-20)


### Features

* Add support for Python 3.14  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))


### Bug Fixes

* Deprecate credentials_file argument  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-memorystore-v0.1.2...google-cloud-memorystore-v0.1.3) (2025-05-08)


### Features

* A new field `async_instance_endpoints_deletion_enabled` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `automated_backup_config` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `backup_collection` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `cross_instance_replication_config` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `gcs_source` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `maintenance_policy` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `maintenance_schedule` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `managed_backup_source` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `ondemand_maintenance` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `port` is added to message `.google.cloud.memorystore.v1.PscConnection` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `psc_attachment_details` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `target_engine_version` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new field `target_node_type` is added to message `.google.cloud.memorystore.v1.Instance` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `AutomatedBackupConfig` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `Backup` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `BackupCollection` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `BackupFile` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `BackupInstanceRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `CrossInstanceReplicationConfig` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `DeleteBackupRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ExportBackupRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `GcsBackupSource` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `GetBackupCollectionRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `GetBackupRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ListBackupCollectionsRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ListBackupCollectionsResponse` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ListBackupsRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ListBackupsResponse` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `MaintenancePolicy` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `MaintenanceSchedule` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `ManagedBackupSource` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `PscAttachmentDetail` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `RescheduleMaintenanceRequest` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new message `WeeklyMaintenanceWindow` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `BackupInstance` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `DeleteBackup` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `ExportBackup` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `GetBackup` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `GetBackupCollection` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `ListBackupCollections` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `ListBackups` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new method `RescheduleMaintenance` is added to service `Memorystore` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new resource_definition `cloudkms.googleapis.com/CryptoKey` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new resource_definition `memorystore.googleapis.com/Backup` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A new resource_definition `memorystore.googleapis.com/BackupCollection` is added ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))


### Bug Fixes

* Changed field behavior for an existing field `psc_connection_id` in message `.google.cloud.memorystore.v1.PscConnection` ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))


### Documentation

* A comment for field `discovery_endpoints` in message `.google.cloud.memorystore.v1.Instance` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `engine_version` in message `.google.cloud.memorystore.v1.Instance` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `node_type` in message `.google.cloud.memorystore.v1.Instance` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `port` in message `.google.cloud.memorystore.v1.PscAutoConnection` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `psc_auto_connection` in message `.google.cloud.memorystore.v1.Instance` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `psc_auto_connections` in message `.google.cloud.memorystore.v1.Instance` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))
* A comment for field `psc_connection_id` in message `.google.cloud.memorystore.v1.PscConnection` is changed ([6e3836f](https://github.com/googleapis/google-cloud-python/commit/6e3836f72a3335d75fb912d4e39963c57da47979))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-memorystore-v0.1.1...google-cloud-memorystore-v0.1.2) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([c8bbf32](https://github.com/googleapis/google-cloud-python/commit/c8bbf32606e790b559b261bf96700c76b6e2bfce))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-memorystore-v0.1.0...google-cloud-memorystore-v0.1.1) (2025-02-12)


### Features

* add Instance.Mode.CLUSTER_DISABLED value, and deprecate STANDALONE ([3f8ab82](https://github.com/googleapis/google-cloud-python/commit/3f8ab82aa97dd47b79bcf52343e6764ff159e961))
* Add REST Interceptors which support reading metadata ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))
* Add support for reading selective GAPIC generation methods from service YAML ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))


### Documentation

* A comment for enum value `STANDALONE` in enum `Mode` is changed ([3f8ab82](https://github.com/googleapis/google-cloud-python/commit/3f8ab82aa97dd47b79bcf52343e6764ff159e961))

## 0.1.0 (2024-12-12)


### Features

* add initial files for google.cloud.memorystore.v1 ([6ef2cae](https://github.com/googleapis/google-cloud-python/commit/6ef2caeb89e7476fce4c2e1c9c8bde8e9e4b98a8))
* add initial files for google.cloud.memorystore.v1beta ([6ef2cae](https://github.com/googleapis/google-cloud-python/commit/6ef2caeb89e7476fce4c2e1c9c8bde8e9e4b98a8))
* Add support for opt-in debug logging ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))

## Changelog
