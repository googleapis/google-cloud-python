# Changelog

## [0.3.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-alloydb-v0.3.7...google-cloud-alloydb-v0.3.8) (2024-02-05)


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
