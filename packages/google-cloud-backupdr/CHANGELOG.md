# Changelog

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.2.2...google-cloud-backupdr-v0.2.3) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([3a85796](https://github.com/googleapis/google-cloud-python/commit/3a85796774ebf728cbc9e82dc536316530ac78c1))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.2.1...google-cloud-backupdr-v0.2.2) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.2.0...google-cloud-backupdr-v0.2.1) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))
* Add support for reading selective GAPIC generation methods from service YAML ([b1c3ce8](https://github.com/googleapis/google-cloud-python/commit/b1c3ce8b271e9d22afabcde054e81dcedae6b0ef))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.7...google-cloud-backupdr-v0.2.0) (2025-01-13)


### ⚠ BREAKING CHANGES

* Update field behavior of `resource_type` field in message `BackupPlanAssociation` to `REQUIRED`

### Features

* `ignore_backup_plan_references` added to the DeleteBackupVaultRequest ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* add enum to Backup Vault Access Restriction field ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* add InitializeServiceAPI ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* Update field behavior of `networks` field in message `ManagementServer` to `OPTIONAL` ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))


### Bug Fixes

* Update field behavior of `resource_type` field in message `BackupPlanAssociation` to `REQUIRED` ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))


### Documentation

* A comment for enum value `ACCESS_RESTRICTION_UNSPECIFIED` in enum `AccessRestriction` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `access_restriction` in message `.google.cloud.backupdr.v1.BackupVault` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `backup_retention_days` in message `.google.cloud.backupdr.v1.BackupRule` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `data_source` in message `.google.cloud.backupdr.v1.BackupPlanAssociation` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `last_backup_error` in message `.google.cloud.backupdr.v1.RuleConfigInfo` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `networks` in message `.google.cloud.backupdr.v1.ManagementServer` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `requested_cancellation` in message `.google.cloud.backupdr.v1.OperationMetadata` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `resource_type` in message `.google.cloud.backupdr.v1.BackupPlan` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `resource_type` in message `.google.cloud.backupdr.v1.BackupPlanAssociation` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `rule_id` in message `.google.cloud.backupdr.v1.RuleConfigInfo` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))
* A comment for field `uid` in message `.google.cloud.backupdr.v1.BackupVault` is changed ([b5cdea3](https://github.com/googleapis/google-cloud-python/commit/b5cdea3f1d59f67ff0bd01d1891abf948a4f5582))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.6...google-cloud-backupdr-v0.1.7) (2024-12-12)


### Features

* Add support for opt-in debug logging ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([e31cbb0](https://github.com/googleapis/google-cloud-python/commit/e31cbb0e11ab2cb093411005682c2fa2c38e787c))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.5...google-cloud-backupdr-v0.1.6) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([4ed4108](https://github.com/googleapis/google-cloud-python/commit/4ed41088ab3cbadfe4de7fa170f172666015ed24))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.4...google-cloud-backupdr-v0.1.5) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13200](https://github.com/googleapis/google-cloud-python/issues/13200)) ([19dc048](https://github.com/googleapis/google-cloud-python/commit/19dc0485852406b90743297bcf257020e6012593))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.3...google-cloud-backupdr-v0.1.4) (2024-10-08)


### Features

* [google-cloud-backupdr] Client library for the backupvault api is added ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* Add backupplan proto ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* Add backupplanassociation proto ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* Add backupvault_ba proto ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* Add backupvault_gce proto ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))


### Documentation

* A comment for field `management_servers` in message `.google.cloud.backupdr.v1.ListManagementServersResponse` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* A comment for field `name` in message `.google.cloud.backupdr.v1.GetManagementServerRequest` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* A comment for field `oauth2_client_id` in message `.google.cloud.backupdr.v1.ManagementServer` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* A comment for field `parent` in message `.google.cloud.backupdr.v1.CreateManagementServerRequest` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* A comment for field `parent` in message `.google.cloud.backupdr.v1.ListManagementServersRequest` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))
* A comment for field `requested_cancellation` in message `.google.cloud.backupdr.v1.OperationMetadata` is changed ([27c262d](https://github.com/googleapis/google-cloud-python/commit/27c262d51c5d9f055152d9448f5fb6759da4bdb3))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.2...google-cloud-backupdr-v0.1.3) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.1...google-cloud-backupdr-v0.1.2) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-backupdr-v0.1.0...google-cloud-backupdr-v0.1.1) (2024-06-24)


### Features

* A new field `satisfies_pzi` is added ([9e20534](https://github.com/googleapis/google-cloud-python/commit/9e205344d6b24d6cedced1d9c177be7652f54267))
* A new field `satisfies_pzs` is added ([9e20534](https://github.com/googleapis/google-cloud-python/commit/9e205344d6b24d6cedced1d9c177be7652f54267))
* Updated documentation URI ([9e20534](https://github.com/googleapis/google-cloud-python/commit/9e205344d6b24d6cedced1d9c177be7652f54267))

## 0.1.0 (2024-04-15)


### Features

* add initial files for google.cloud.backupdr.v1 ([#12552](https://github.com/googleapis/google-cloud-python/issues/12552)) ([d9222a9](https://github.com/googleapis/google-cloud-python/commit/d9222a97786ce1badae4561410ca5e09386a3377))

## Changelog
