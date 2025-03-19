# Changelog

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.4.4...google-cloud-alloydb-v0.4.5) (2025-03-19)


### Features

* **v1beta:** A new message `ExportClusterRequest` is added ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A new message `ExportClusterResponse` is added ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A new message `GcsDestination` is added ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A new method `ExportCluster` is added to service `AlloyDBAdmin` ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))


### Documentation

* **v1beta:** A comment for field `database_flags` in message `.google.cloud.alloydb.v1beta.Instance` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A comment for field `id` in message `.google.cloud.alloydb.v1beta.Instance` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A comment for field `ip` in message `.google.cloud.alloydb.v1beta.Instance` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A comment for field `requested_cancellation` in message `.google.cloud.alloydb.v1beta.OperationMetadata` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A comment for field `state` in message `.google.cloud.alloydb.v1beta.Instance` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))
* **v1beta:** A comment for field `zone_id` in message `.google.cloud.alloydb.v1beta.Instance` is changed ([923f33e](https://github.com/googleapis/google-cloud-python/commit/923f33e2b49d602ee66cf4914bf8ce6cb6ca0e7f))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.4.3...google-cloud-alloydb-v0.4.4) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.4.2...google-cloud-alloydb-v0.4.3) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.4.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.4.1...google-cloud-alloydb-v0.4.2) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.4.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.4.0...google-cloud-alloydb-v0.4.1) (2024-12-12)


### Features

* Add support for opt-in debug logging ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.16...google-cloud-alloydb-v0.4.0) (2024-11-11)


### ⚠ BREAKING CHANGES

* deprecated various PSC instance configuration fields

### Features

* add more observability options on the Instance level ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new API to execute SQL statements ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new API to perform a promotion or switchover on secondary instances ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new API to upgrade a cluster ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new CloudSQL backup resource ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new cluster and instance level configurations to interact with Gemini ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add new PSC instance configuration setting and output the PSC DNS name ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add optional field to keep extra roles on a user if it already exists ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add support for Free Trials ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* add support to schedule maintenance ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* additional field to set tags on a backup or cluster ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))
* support for obtaining the public ip addresses of an instance and enabling outbound public ip ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))


### Bug Fixes

* deprecated various PSC instance configuration fields ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))


### Documentation

* various typo fixes, correcting the formatting, and clarifications on the request_id and validate_only fields in API requests and on the page_size when listing the database ([68a04ad](https://github.com/googleapis/google-cloud-python/commit/68a04ad07c42eb9f64861feb55018922be7963da))

## [0.3.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.15...google-cloud-alloydb-v0.3.16) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.3.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.14...google-cloud-alloydb-v0.3.15) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.3.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.13...google-cloud-alloydb-v0.3.14) (2024-10-23)


### Features

* add more observability options on the Instance level ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add new API to execute SQL statements ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add new API to list the databases in a project and location ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add new API to perform a promotion or switchover on secondary instances ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add new PSC instance configuration setting and output the PSC DNS name ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add optional field to keep extra roles on a user if it already exists ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add support for Free Trials ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* add support to schedule maintenance ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* additional field to set tags on a backup or cluster ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))
* support for obtaining the public ip addresses of an instance and enabling either inbound or outbound public ip ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))


### Documentation

* various typo fixes, correcting the formatting, and clarifications on the request_id and validate_only fields in API requests and on the page_size when listing the database ([e729f1e](https://github.com/googleapis/google-cloud-python/commit/e729f1e7718a0a99dfa29df1fc707b9766637961))

## [0.3.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.12...google-cloud-alloydb-v0.3.13) (2024-09-03)


### Features

* support for enabling outbound public IP on an instance ([4f468fa](https://github.com/googleapis/google-cloud-python/commit/4f468fa598c51426ef31ef878f9c3b61f79802f9))
* support for getting maintenance schedule of a cluster ([4f468fa](https://github.com/googleapis/google-cloud-python/commit/4f468fa598c51426ef31ef878f9c3b61f79802f9))
* support for getting outbound public IP addresses of an instance ([4f468fa](https://github.com/googleapis/google-cloud-python/commit/4f468fa598c51426ef31ef878f9c3b61f79802f9))
* support for setting maintenance update policy on a cluster ([4f468fa](https://github.com/googleapis/google-cloud-python/commit/4f468fa598c51426ef31ef878f9c3b61f79802f9))

## [0.3.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.11...google-cloud-alloydb-v0.3.12) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.3.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.10...google-cloud-alloydb-v0.3.11) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([04ec204](https://github.com/googleapis/google-cloud-python/commit/04ec2046ed11c690273912e1bb6220823c7dd7c0))
* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))

## [0.3.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.9...google-cloud-alloydb-v0.3.10) (2024-03-05)


### Features

* Add new API to list the databases in a project and location ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))
* Add PSC cluster and instance configuration settings to enable/disable PSC and obtain the PSC endpoint name ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))
* Add support for getting PSC DNS name from the GetConnectionInfo API ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))
* Add support for obtaining the public IP address of an Instance ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))


### Documentation

* Clarified read pool config is for read pool type instances ([3f2a93c](https://github.com/googleapis/google-cloud-python/commit/3f2a93c4892bd5995a87c152f2d54e26aa6cf138))

## [0.3.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.8...google-cloud-alloydb-v0.3.9) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12280](https://github.com/googleapis/google-cloud-python/issues/12280)) ([2d75d0e](https://github.com/googleapis/google-cloud-python/commit/2d75d0e67ca4cccddc688bd37c14ac80564a2e65))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12303](https://github.com/googleapis/google-cloud-python/issues/12303)) ([fbb80c3](https://github.com/googleapis/google-cloud-python/commit/fbb80c32f7db91e25bd1cc30966f630728ff6d6a))

## [0.3.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.7...google-cloud-alloydb-v0.3.8) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))

## [0.3.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.6...google-cloud-alloydb-v0.3.7) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([a0392ee](https://github.com/googleapis/google-cloud-python/commit/a0392eeb59fcc6ea7c55283110b92aa24a4d40a0))

## [0.3.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.5...google-cloud-alloydb-v0.3.6) (2024-01-04)


### Features

* added instance network config ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))
* added ListDatabases API and Database object ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))
* added PSC config, PSC interface config, PSC instance config ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))
* added two boolean fields satisfies_pzi and satisfies_pzs ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))
* changed field network in NetworkConfig from required to optional ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))


### Documentation

* clarified read pool config is for read pool type instances ([bea1a52](https://github.com/googleapis/google-cloud-python/commit/bea1a52adf0717b7656764ac0f0f6f5fa13d0338))

## [0.3.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.4...google-cloud-alloydb-v0.3.5) (2023-12-07)


### Features

* Add support for python 3.12 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Introduce compatibility with native namespace packages ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Use `retry_async` instead of `retry` in async client ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))

## [0.3.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.3...google-cloud-alloydb-v0.3.4) (2023-11-02)


### Features

* Add new field in `GenerateClientCertificate` v1 API to allow AlloyDB connectors request client certs with metadata exchange support ([c915e94](https://github.com/googleapis/google-cloud-python/commit/c915e94f26dbbacafed1256fe9c35a7b0590c166))


### Documentation

* Clarify that `readPoolConfig` is required under certain circumstances, and fix doc formatting on `allocatedIpRange`. ([c915e94](https://github.com/googleapis/google-cloud-python/commit/c915e94f26dbbacafed1256fe9c35a7b0590c166))

## [0.3.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.2...google-cloud-alloydb-v0.3.3) (2023-09-30)


### Features

* Add support to generate client certificate and get connection info ([0f72d58](https://github.com/googleapis/google-cloud-python/commit/0f72d586cebe5d6bb7e127aded5eb49dcc2ca8d9))
* Add support to generate client certificate and get connection info for auth proxy in AlloyDB v1 ([#11764](https://github.com/googleapis/google-cloud-python/issues/11764)) ([0f72d58](https://github.com/googleapis/google-cloud-python/commit/0f72d586cebe5d6bb7e127aded5eb49dcc2ca8d9))

## [0.3.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.1...google-cloud-alloydb-v0.3.2) (2023-09-19)


### Features

* **v1alpha:** Added ClientConnectionConfig ([899c388](https://github.com/googleapis/google-cloud-python/commit/899c388ff5cc6986c4e18fa82babb57f66bb38ce))
* **v1alpha:** Added DatabaseVersion ([899c388](https://github.com/googleapis/google-cloud-python/commit/899c388ff5cc6986c4e18fa82babb57f66bb38ce))
* **v1alpha:** Added enum value for PG15 ([899c388](https://github.com/googleapis/google-cloud-python/commit/899c388ff5cc6986c4e18fa82babb57f66bb38ce))
* **v1alpha:** Deprecate network field in favor of network_config.network ([899c388](https://github.com/googleapis/google-cloud-python/commit/899c388ff5cc6986c4e18fa82babb57f66bb38ce))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.0...google-cloud-alloydb-v0.3.1) (2023-09-19)


### Features

* Added ClientConnectionConfig ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))
* Added DatabaseVersion ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))
* Added enum value for PG15 ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))
* Added QuantityBasedExpiry ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))
* Changed description for recovery_window_days in ContinuousBackupConfig ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))
* Deprecate network field in favor of network_config.network ([c76e881](https://github.com/googleapis/google-cloud-python/commit/c76e88194ea5ae3851cdd61071bc9e8106ae1571))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.2.1...google-cloud-alloydb-v0.3.0) (2023-07-17)


### Features

* add metadata exchange support for AlloyDB connectors ([6b47f7a](https://github.com/googleapis/google-cloud-python/commit/6b47f7af5edb5db7a9e909e3c7ebd0d34296facb))
* adds metadata field describing an AlloyDB backup's quantity based retention ([6b47f7a](https://github.com/googleapis/google-cloud-python/commit/6b47f7af5edb5db7a9e909e3c7ebd0d34296facb))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.2.0...google-cloud-alloydb-v0.2.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.1.1...google-cloud-alloydb-v0.2.0) (2023-06-13)


### Features

* Added cluster network config ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added ClusterView supporting more granular view of continuous backups ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added fault injection API ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added instance update policy ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added new SSL modes ALLOW_UNENCRYPTED_AND_ENCRYPTED, ENCRYPTED_ONLY ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added support for continuous backups ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added support for cross-region replication (secondary clusters/instances and promotion) ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))
* Added users API ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))


### Bug Fixes

* Deprecated SSL modes SSL_MODE_ALLOW, SSL_MODE_REQUIRE, SSL_MODE_VERIFY_CA ([32760f9](https://github.com/googleapis/google-cloud-python/commit/32760f95a3bee3571a5cb5b22ffd7e8f666663f1))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.1.0...google-cloud-alloydb-v0.1.1) (2023-03-25)


### Documentation

* Fix formatting of request arg in docstring ([#10867](https://github.com/googleapis/google-cloud-python/issues/10867)) ([d34a425](https://github.com/googleapis/google-cloud-python/commit/d34a425f7d0f02bebaf20d24b725b8c25c699697))

## 0.1.0 (2023-03-06)


### Features

* add initial files for google.cloud.alloydb.v1 ([#10847](https://github.com/googleapis/google-cloud-python/issues/10847)) ([c9ebf82](https://github.com/googleapis/google-cloud-python/commit/c9ebf8298d0164d382c278a1a8c95cccc3dd7491))

## Changelog
