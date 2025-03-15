# Changelog

## [0.2.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.13...google-cloud-kms-inventory-v0.2.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([e06ee32](https://github.com/googleapis/google-cloud-python/commit/e06ee325de4125cdfcaf040a77dc9ccc82843260))

## [0.2.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.12...google-cloud-kms-inventory-v0.2.13) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([908d742](https://github.com/googleapis/google-cloud-python/commit/908d7421a4adadd7407df7ec2a25e25688ff180f))
* Add support for reading selective GAPIC generation methods from service YAML ([908d742](https://github.com/googleapis/google-cloud-python/commit/908d7421a4adadd7407df7ec2a25e25688ff180f))

## [0.2.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.11...google-cloud-kms-inventory-v0.2.12) (2024-12-12)


### Features

* Add support for opt-in debug logging ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([feb5c03](https://github.com/googleapis/google-cloud-python/commit/feb5c0348d0efbe5d3c01d5470f2daaef5302842))

## [0.2.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.10...google-cloud-kms-inventory-v0.2.11) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13243](https://github.com/googleapis/google-cloud-python/issues/13243)) ([d794dec](https://github.com/googleapis/google-cloud-python/commit/d794dec5eff5f23a1ff926012bf9e6cad719e020))

## [0.2.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.9...google-cloud-kms-inventory-v0.2.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13207](https://github.com/googleapis/google-cloud-python/issues/13207)) ([ceb9be8](https://github.com/googleapis/google-cloud-python/commit/ceb9be8f89ac7355d842bac1d77b2926eb0b649c))

## [0.2.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.8...google-cloud-kms-inventory-v0.2.9) (2024-10-08)


### Bug Fixes

* **deps:** allow google-cloud-kms 3.x ([bd7ac53](https://github.com/googleapis/google-cloud-python/commit/bd7ac5328808f9aadfad08404348bc1cc473ff08))

## [0.2.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.7...google-cloud-kms-inventory-v0.2.8) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([189922a](https://github.com/googleapis/google-cloud-python/commit/189922a0fbe969dedc7b0f78a62ccb2e5d3f29a9))

## [0.2.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.6...google-cloud-kms-inventory-v0.2.7) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12867](https://github.com/googleapis/google-cloud-python/issues/12867)) ([3362176](https://github.com/googleapis/google-cloud-python/commit/33621762b989106ccf85adb538cf531c513a746c))

## [0.2.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.5...google-cloud-kms-inventory-v0.2.6) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12385](https://github.com/googleapis/google-cloud-python/issues/12385)) ([d50f4d0](https://github.com/googleapis/google-cloud-python/commit/d50f4d042774e2f12e9fe03459eae9ce91247df3))

## [0.2.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.4...google-cloud-kms-inventory-v0.2.5) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12307](https://github.com/googleapis/google-cloud-python/issues/12307)) ([be87bc4](https://github.com/googleapis/google-cloud-python/commit/be87bc4a33fe32a512448a42246c9873da88269f))
* fix ValueError in test__validate_universe_domain ([dd749df](https://github.com/googleapis/google-cloud-python/commit/dd749dfb4caf2e33f1152dfd8c4b0ac5424c381c))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.3...google-cloud-kms-inventory-v0.2.4) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.2...google-cloud-kms-inventory-v0.2.3) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12241](https://github.com/googleapis/google-cloud-python/issues/12241)) ([aae72f5](https://github.com/googleapis/google-cloud-python/commit/aae72f5e6c7d48e777fdf68d1012b2b51b912bad))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.1...google-cloud-kms-inventory-v0.2.2) (2023-12-07)


### Features

* Add support for python 3.12 ([f46b37f](https://github.com/googleapis/google-cloud-python/commit/f46b37f825f96add7b127282414346c1a1a96231))
* Introduce compatibility with native namespace packages ([f46b37f](https://github.com/googleapis/google-cloud-python/commit/f46b37f825f96add7b127282414346c1a1a96231))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([f46b37f](https://github.com/googleapis/google-cloud-python/commit/f46b37f825f96add7b127282414346c1a1a96231))
* Use `retry_async` instead of `retry` in async client ([f46b37f](https://github.com/googleapis/google-cloud-python/commit/f46b37f825f96add7b127282414346c1a1a96231))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.2.0...google-cloud-kms-inventory-v0.2.1) (2023-09-19)


### Documentation

* Minor formatting ([#11632](https://github.com/googleapis/google-cloud-python/issues/11632)) ([dbee08f](https://github.com/googleapis/google-cloud-python/commit/dbee08f2df63e1906ba13b0d3060eec5a80c79e2))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.1.1...google-cloud-kms-inventory-v0.2.0) (2023-07-17)


### Features

* add resource_types to SearchAllResources, to allow filtering by resource type ([#11484](https://github.com/googleapis/google-cloud-python/issues/11484)) ([fc26bf0](https://github.com/googleapis/google-cloud-python/commit/fc26bf06248d0459b418befe11608d6e0da2cc85))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-kms-inventory-v0.1.0...google-cloud-kms-inventory-v0.1.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11446](https://github.com/googleapis/google-cloud-python/issues/11446)) ([37682b7](https://github.com/googleapis/google-cloud-python/commit/37682b7793cfe0dcb27963fea7e474b3b85571c9))

## 0.1.0 (2023-06-22)


### Features

* add initial files for google.cloud.kms.inventory.v1 ([#11424](https://github.com/googleapis/google-cloud-python/issues/11424)) ([7e5f352](https://github.com/googleapis/google-cloud-python/commit/7e5f352a486021f901a30286394df572640b1bad))

## Changelog
