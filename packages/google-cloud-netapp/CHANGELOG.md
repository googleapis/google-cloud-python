# Changelog

## [0.3.20](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.19...google-cloud-netapp-v0.3.20) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([c8bbf32](https://github.com/googleapis/google-cloud-python/commit/c8bbf32606e790b559b261bf96700c76b6e2bfce))

## [0.3.19](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.18...google-cloud-netapp-v0.3.19) (2025-02-12)


### Features

* add ipAddress field to MountOption ([b266867](https://github.com/googleapis/google-cloud-python/commit/b2668671a5afa4164ff9be4a24888c63256e6b1b))
* Add REST Interceptors which support reading metadata ([b266867](https://github.com/googleapis/google-cloud-python/commit/b2668671a5afa4164ff9be4a24888c63256e6b1b))

## [0.3.18](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.17...google-cloud-netapp-v0.3.18) (2025-01-13)


### Features

* Add ValidateDirectoryService API for testing AD connection of a storage pool ([b45a11d](https://github.com/googleapis/google-cloud-python/commit/b45a11db722f709f055d703f4ef7fd4cbf8655fa))


### Documentation

* Remove the format for `replication` in message `google.cloud.netapp.v1.HybridReplicationParameters` ([b45a11d](https://github.com/googleapis/google-cloud-python/commit/b45a11db722f709f055d703f4ef7fd4cbf8655fa))

## [0.3.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.16...google-cloud-netapp-v0.3.17) (2024-12-12)


### Features

* Add EstablishPeering API for Onprem Migration ([2b05355](https://github.com/googleapis/google-cloud-python/commit/2b053555536107335ff5ea08b37fdfbeed864e6a))
* Add new Active Directory state for AD Diagnostics support ([2b05355](https://github.com/googleapis/google-cloud-python/commit/2b053555536107335ff5ea08b37fdfbeed864e6a))
* Add support for opt-in debug logging ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))
* Add Sync API for Replications ([2b05355](https://github.com/googleapis/google-cloud-python/commit/2b053555536107335ff5ea08b37fdfbeed864e6a))
* Enable creation of Onprem Migration in CreateVolume ([2b05355](https://github.com/googleapis/google-cloud-python/commit/2b053555536107335ff5ea08b37fdfbeed864e6a))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))


### Documentation

* Docs now do not allow underscore in IDs of various Resources ([2b05355](https://github.com/googleapis/google-cloud-python/commit/2b053555536107335ff5ea08b37fdfbeed864e6a))

## [0.3.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.15...google-cloud-netapp-v0.3.16) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13244](https://github.com/googleapis/google-cloud-python/issues/13244)) ([ae1f471](https://github.com/googleapis/google-cloud-python/commit/ae1f47175bf3354f78cb558a844a9cab00317b95))

## [0.3.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.14...google-cloud-netapp-v0.3.15) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13207](https://github.com/googleapis/google-cloud-python/issues/13207)) ([ceb9be8](https://github.com/googleapis/google-cloud-python/commit/ceb9be8f89ac7355d842bac1d77b2926eb0b649c))

## [0.3.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.13...google-cloud-netapp-v0.3.14) (2024-09-16)


### Features

* A new field 'allow_auto_tiering' in message 'google.cloud.netapp.v1.StoragePool' is added ([5e3f4ae](https://github.com/googleapis/google-cloud-python/commit/5e3f4aebeb2f79efb1992ae623eb1aea86de2b0c))
* A new field 'cold_tier_size_gib' in message 'google.cloud.netapp.v1.Volume' is added ([5e3f4ae](https://github.com/googleapis/google-cloud-python/commit/5e3f4aebeb2f79efb1992ae623eb1aea86de2b0c))
* A new message 'google.cloud.netapp.v1.SwitchActiveReplicaZoneRequest' is added ([5e3f4ae](https://github.com/googleapis/google-cloud-python/commit/5e3f4aebeb2f79efb1992ae623eb1aea86de2b0c))
* **api:** [google-cloud-netapp] A new rpc 'SwitchActiveReplicaZone' is added to service 'google.cloud.netapp.v1.NetApp' ([5e3f4ae](https://github.com/googleapis/google-cloud-python/commit/5e3f4aebeb2f79efb1992ae623eb1aea86de2b0c))

## [0.3.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.12...google-cloud-netapp-v0.3.13) (2024-07-31)


### Features

* A new field `administrators` is added to message `.google.cloud.netapp.v1.ActiveDirectory` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `large_capacity` is added to message `.google.cloud.netapp.v1.Volume` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `multiple_endpoints` is added to message `.google.cloud.netapp.v1.Volume` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `replica_zone` is added to message `.google.cloud.netapp.v1.StoragePool` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `replica_zone` is added to message `.google.cloud.netapp.v1.Volume` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `zone` is added to message `.google.cloud.netapp.v1.StoragePool` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A new field `zone` is added to message `.google.cloud.netapp.v1.Volume` ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))


### Documentation

* [google-cloud-netapp] A comment for field `active_directory_id` in message `.google.cloud.netapp.v1.CreateActiveDirectoryRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for enum value `TRANSFERRING` in enum `MirrorState` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `backup_id` in message `.google.cloud.netapp.v1.CreateBackupRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `backup_policy_id` in message `.google.cloud.netapp.v1.CreateBackupPolicyRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `backup_vault_id` in message `.google.cloud.netapp.v1.CreateBackupVaultRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `kms_config_id` in message `.google.cloud.netapp.v1.CreateKmsConfigRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `replication_id` in message `.google.cloud.netapp.v1.CreateReplicationRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `snapshot_id` in message `.google.cloud.netapp.v1.CreateSnapshotRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `storage_pool_id` in message `.google.cloud.netapp.v1.CreateStoragePoolRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `total_transfer_duration` in message `.google.cloud.netapp.v1.TransferStats` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `transfer_bytes` in message `.google.cloud.netapp.v1.TransferStats` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))
* A comment for field `volume_id` in message `.google.cloud.netapp.v1.CreateVolumeRequest` is changed ([d3c6970](https://github.com/googleapis/google-cloud-python/commit/d3c6970029a98849c1a1db885fe55ca79c823c9d))

## [0.3.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.11...google-cloud-netapp-v0.3.12) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([d95af77](https://github.com/googleapis/google-cloud-python/commit/d95af77248f0935a5fe3dba1fccc75124c8b1451))

## [0.3.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.10...google-cloud-netapp-v0.3.11) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12868](https://github.com/googleapis/google-cloud-python/issues/12868)) ([0e39c1a](https://github.com/googleapis/google-cloud-python/commit/0e39c1a0ab46757bcf80a178d9bd422f6dcb24c6))

## [0.3.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.9...google-cloud-netapp-v0.3.10) (2024-05-17)


### Features

* Add a new Service Level FLEX ([74a7e9c](https://github.com/googleapis/google-cloud-python/commit/74a7e9c313c2d6301982eded0e46bc5176d2737b))
* Add backup chain bytes to BackupConfig in Volume ([74a7e9c](https://github.com/googleapis/google-cloud-python/commit/74a7e9c313c2d6301982eded0e46bc5176d2737b))
* Add Location metadata support ([74a7e9c](https://github.com/googleapis/google-cloud-python/commit/74a7e9c313c2d6301982eded0e46bc5176d2737b))
* Add Tiering Policy to Volume ([74a7e9c](https://github.com/googleapis/google-cloud-python/commit/74a7e9c313c2d6301982eded0e46bc5176d2737b))

## [0.3.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.8...google-cloud-netapp-v0.3.9) (2024-03-22)


### Documentation

* [google-cloud-netapp] Rephrase comment on psa_range ([#12476](https://github.com/googleapis/google-cloud-python/issues/12476)) ([585a7e8](https://github.com/googleapis/google-cloud-python/commit/585a7e86058c5beff9fefe3945d3efc0b17f9412))

## [0.3.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.7...google-cloud-netapp-v0.3.8) (2024-03-07)


### Documentation

* change comments of the psa_range field to note it is currently not implemented ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))
* mark optional fields explicitly in Storage Pool ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))
* update comments of ServiceLevel and EncryptionType ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))

## [0.3.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.6...google-cloud-netapp-v0.3.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12385](https://github.com/googleapis/google-cloud-python/issues/12385)) ([d50f4d0](https://github.com/googleapis/google-cloud-python/commit/d50f4d042774e2f12e9fe03459eae9ce91247df3))

## [0.3.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.5...google-cloud-netapp-v0.3.6) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12307](https://github.com/googleapis/google-cloud-python/issues/12307)) ([be87bc4](https://github.com/googleapis/google-cloud-python/commit/be87bc4a33fe32a512448a42246c9873da88269f))
* fix ValueError in test__validate_universe_domain ([7c2f2c2](https://github.com/googleapis/google-cloud-python/commit/7c2f2c29d74c9584efc42ddfe8bc098a594391a2))

## [0.3.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.4...google-cloud-netapp-v0.3.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))

## [0.3.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.3...google-cloud-netapp-v0.3.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12241](https://github.com/googleapis/google-cloud-python/issues/12241)) ([aae72f5](https://github.com/googleapis/google-cloud-python/commit/aae72f5e6c7d48e777fdf68d1012b2b51b912bad))

## [0.3.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.2...google-cloud-netapp-v0.3.3) (2024-01-04)


### Features

* Add singular and plural annotations ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))
* Enable Backup, Backup Vault, and Backup Policy ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))
* Set field_behavior to IDENTIFIER on the "name" fields ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))


### Documentation

* Comments are updated for several fields/enums ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))

## [0.3.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.1...google-cloud-netapp-v0.3.2) (2023-12-07)


### Features

* Add support for python 3.12 ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))
* Introduce compatibility with native namespace packages ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))
* Use `retry_async` instead of `retry` in async client ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.0...google-cloud-netapp-v0.3.1) (2023-09-19)


### Documentation

* Minor formatting ([1ae610b](https://github.com/googleapis/google-cloud-python/commit/1ae610bb3b321ceac7bd23a455a002e39645d84f))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.2.0...google-cloud-netapp-v0.3.0) (2023-08-09)


### Features

* add actions for Operations and Locations ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))
* add RestrictedAction to Volume ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))


### Documentation

* add comments to a few messages ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.1.0...google-cloud-netapp-v0.2.0) (2023-08-03)


### Features

* add initial version of NetApp v1 APIs ([de53f0e](https://github.com/googleapis/google-cloud-python/commit/de53f0efe25e71d0aa5b57b0989c4f0a491fa2ec))


### Bug Fixes

* remove netapp_v1beta1 client ([#11534](https://github.com/googleapis/google-cloud-python/issues/11534)) ([e7b16ed](https://github.com/googleapis/google-cloud-python/commit/e7b16ed17e06fa42858e5fdd35953805b8ca7e90))
* update the default import to use `netapp_v1` ([de53f0e](https://github.com/googleapis/google-cloud-python/commit/de53f0efe25e71d0aa5b57b0989c4f0a491fa2ec))

## 0.1.0 (2023-07-20)


### Features

* add initial files for google.cloud.netapp.v1beta1 ([#11490](https://github.com/googleapis/google-cloud-python/issues/11490)) ([719a2d5](https://github.com/googleapis/google-cloud-python/commit/719a2d5d6e792b3d96dc72a1743dc7b4b4321edc))

## Changelog
