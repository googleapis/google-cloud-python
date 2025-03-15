# Changelog

## [0.1.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.16...google-cloud-quotas-v0.1.17) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([7295cbb](https://github.com/googleapis/google-cloud-python/commit/7295cbb7c3122eeff1042c3c543bfc9b8b3ca913))


### Documentation

* [google-cloud-quotas] improved comment clarity ([#13647](https://github.com/googleapis/google-cloud-python/issues/13647)) ([3edc52a](https://github.com/googleapis/google-cloud-python/commit/3edc52a999e96c931b126ef1be20140bb4042089))

## [0.1.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.15...google-cloud-quotas-v0.1.16) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([c8e0760](https://github.com/googleapis/google-cloud-python/commit/c8e0760e8088950c62279335216ad1d17716ce59))
* Add support for reading selective GAPIC generation methods from service YAML ([c8e0760](https://github.com/googleapis/google-cloud-python/commit/c8e0760e8088950c62279335216ad1d17716ce59))

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.14...google-cloud-quotas-v0.1.15) (2025-01-13)


### Features

* Add v1beta client libraries for cloudquotas API ([#13408](https://github.com/googleapis/google-cloud-python/issues/13408)) ([c757c44](https://github.com/googleapis/google-cloud-python/commit/c757c441cd4f2c830062717d35595840d111a977))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.13...google-cloud-quotas-v0.1.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([8e6b0cc](https://github.com/googleapis/google-cloud-python/commit/8e6b0cca8709ae8c7f0c722c5ebf0707358d3359))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8e6b0cc](https://github.com/googleapis/google-cloud-python/commit/8e6b0cca8709ae8c7f0c722c5ebf0707358d3359))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.12...google-cloud-quotas-v0.1.13) (2024-11-14)


### Features

* A new value `NOT_ENOUGH_USAGE_HISTORY` is added to enum `IneligibilityReason` ([1c9fcd9](https://github.com/googleapis/google-cloud-python/commit/1c9fcd9b38bc2f217bf6298c62c2c2a8ff4fdf16))
* A new value `NOT_SUPPORTED` is added to enum `IneligibilityReason` ([1c9fcd9](https://github.com/googleapis/google-cloud-python/commit/1c9fcd9b38bc2f217bf6298c62c2c2a8ff4fdf16))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.11...google-cloud-quotas-v0.1.12) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([59c4287](https://github.com/googleapis/google-cloud-python/commit/59c42878386ee08d1717b73e47d33d76cfb38ba0))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-quotas-v0.1.10...google-cloud-quotas-v0.1.11) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13202](https://github.com/googleapis/google-cloud-python/issues/13202)) ([5b1f2f3](https://github.com/googleapis/google-cloud-python/commit/5b1f2f3a81ed171b643812e67a7ed179b9b703ea))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.9...google-cloud-cloudquotas-v0.1.10) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([a6f7356](https://github.com/googleapis/google-cloud-python/commit/a6f7356f1549721f9fab83d4dcfa226cec1965d0))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.8...google-cloud-cloudquotas-v0.1.9) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.7...google-cloud-cloudquotas-v0.1.8) (2024-04-18)


### Documentation

* [google-cloud-cloudquotas] Update contact_email doc to not check permission of the email account ([#12592](https://github.com/googleapis/google-cloud-python/issues/12592)) ([a4c8d03](https://github.com/googleapis/google-cloud-python/commit/a4c8d03a01a102761b6aaf066cc96273fd903c9c))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.6...google-cloud-cloudquotas-v0.1.7) (2024-04-03)


### Features

* Add `rollout_info` field to `QuotaDetails` message ([0b8728c](https://github.com/googleapis/google-cloud-python/commit/0b8728ccd8072c0f761a119971fb0dfe20207cf5))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.5...google-cloud-cloudquotas-v0.1.6) (2024-03-27)


### Documentation

* update comment of `contact_email` to make it optional as opposed to required ([763c119](https://github.com/googleapis/google-cloud-python/commit/763c1199b9c5d6c9a6297bed6bb815e4c80432e3))
* update sample URL in field for `service_request_quota_uri` ([763c119](https://github.com/googleapis/google-cloud-python/commit/763c1199b9c5d6c9a6297bed6bb815e4c80432e3))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.4...google-cloud-cloudquotas-v0.1.5) (2024-03-22)


### Documentation

* A comment for field `filter` in message `.google.api.cloudquotas.v1.ListQuotaPreferencesRequest` is changed ([55bf59f](https://github.com/googleapis/google-cloud-python/commit/55bf59ffe7d96c747b4b2c47cbcebe31e4bc0183))
* A comment for field `order_by` in message `.google.api.cloudquotas.v1.ListQuotaPreferencesRequest` is changed ([55bf59f](https://github.com/googleapis/google-cloud-python/commit/55bf59ffe7d96c747b4b2c47cbcebe31e4bc0183))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.3...google-cloud-cloudquotas-v0.1.4) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12383](https://github.com/googleapis/google-cloud-python/issues/12383)) ([305f43f](https://github.com/googleapis/google-cloud-python/commit/305f43f7d6293e3316248f421fdc19c5d8405c21))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.2...google-cloud-cloudquotas-v0.1.3) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12305](https://github.com/googleapis/google-cloud-python/issues/12305)) ([2aa7f17](https://github.com/googleapis/google-cloud-python/commit/2aa7f17a5fd4f2249260225db91fb0414d06eaa7))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.1...google-cloud-cloudquotas-v0.1.2) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudquotas-v0.1.0...google-cloud-cloudquotas-v0.1.1) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## 0.1.0 (2024-01-12)


### Features

* add initial files for google.api.cloudquotas.v1 ([#12193](https://github.com/googleapis/google-cloud-python/issues/12193)) ([797c302](https://github.com/googleapis/google-cloud-python/commit/797c302fcc475657959488a5db503a874d910c21))

## Changelog
