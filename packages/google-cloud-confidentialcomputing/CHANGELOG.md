# Changelog

## [0.4.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.16...google-cloud-confidentialcomputing-v0.4.17) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([1e43e75](https://github.com/googleapis/google-cloud-python/commit/1e43e75e99445373785b11381e0e859fa14bb485))

## [0.4.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.15...google-cloud-confidentialcomputing-v0.4.16) (2025-02-24)


### Features

* [google-cloud-confidentialcomputing] A new field `attester` is added to message `.google.cloud.confidentialcomputing.v1.VerifyAttestationRequest` ([#13543](https://github.com/googleapis/google-cloud-python/issues/13543)) ([6e892e0](https://github.com/googleapis/google-cloud-python/commit/6e892e0aeac1975a3fd592bca1087c5c7e043ccc))


### Documentation

* Fixed a typo in `VerifyAttestationRequest` comment ([6e892e0](https://github.com/googleapis/google-cloud-python/commit/6e892e0aeac1975a3fd592bca1087c5c7e043ccc))

## [0.4.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.14...google-cloud-confidentialcomputing-v0.4.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))
* Add support for reading selective GAPIC generation methods from service YAML ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))

## [0.4.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.13...google-cloud-confidentialcomputing-v0.4.14) (2024-12-12)


### Features

* Add a token_type options proto to allow for customization of specific token types ([f8900f4](https://github.com/googleapis/google-cloud-python/commit/f8900f40bb825b25a0cf5727f6992397662bb6a2))
* Add support for opt-in debug logging ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))
* Added the first token type option to hold principal tag token options ([f8900f4](https://github.com/googleapis/google-cloud-python/commit/f8900f40bb825b25a0cf5727f6992397662bb6a2))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))

## [0.4.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.12...google-cloud-confidentialcomputing-v0.4.13) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [0.4.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.11...google-cloud-confidentialcomputing-v0.4.12) (2024-10-24)


### Features

* Add support for  Python 3.13 ([6252476](https://github.com/googleapis/google-cloud-python/commit/6252476e5938352fb2417d098a1edcc08558fe10))

## [0.4.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.10...google-cloud-confidentialcomputing-v0.4.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([a6f7356](https://github.com/googleapis/google-cloud-python/commit/a6f7356f1549721f9fab83d4dcfa226cec1965d0))

## [0.4.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.9...google-cloud-confidentialcomputing-v0.4.10) (2024-07-10)


### Features

* [google-cloud-confidentialcomputing] Add a new field `tee_attestation` to `VerifyAttestationRequest` message proto for SEV SNP and TDX attestations ([#12894](https://github.com/googleapis/google-cloud-python/issues/12894)) ([8e75da8](https://github.com/googleapis/google-cloud-python/commit/8e75da8f04b5c1e6442517949581a9424f90bb18))

## [0.4.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.8...google-cloud-confidentialcomputing-v0.4.9) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [0.4.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.7...google-cloud-confidentialcomputing-v0.4.8) (2024-03-27)


### Features

* [google-cloud-confidentialcomputing] Add additional `TokenType` options (`TOKEN_TYPE_PKI` and `TOKEN_TYPE_LIMITED_AWS`) ([#12515](https://github.com/googleapis/google-cloud-python/issues/12515)) ([60d87fa](https://github.com/googleapis/google-cloud-python/commit/60d87fab39cf9b19fee1679b52100310a42f19e5))

## [0.4.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.6...google-cloud-confidentialcomputing-v0.4.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12383](https://github.com/googleapis/google-cloud-python/issues/12383)) ([305f43f](https://github.com/googleapis/google-cloud-python/commit/305f43f7d6293e3316248f421fdc19c5d8405c21))

## [0.4.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.5...google-cloud-confidentialcomputing-v0.4.6) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12282](https://github.com/googleapis/google-cloud-python/issues/12282)) ([b985096](https://github.com/googleapis/google-cloud-python/commit/b985096d43add8214172ff993e00293e6c8757cb))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12305](https://github.com/googleapis/google-cloud-python/issues/12305)) ([2aa7f17](https://github.com/googleapis/google-cloud-python/commit/2aa7f17a5fd4f2249260225db91fb0414d06eaa7))

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.4...google-cloud-confidentialcomputing-v0.4.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.3...google-cloud-confidentialcomputing-v0.4.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12239](https://github.com/googleapis/google-cloud-python/issues/12239)) ([8004d15](https://github.com/googleapis/google-cloud-python/commit/8004d15d9e6baa4dc5bc3f09d528e176d54d9ec5))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.2...google-cloud-confidentialcomputing-v0.4.3) (2023-12-07)


### Features

* Add support for python 3.12 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Introduce compatibility with native namespace packages ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Use `retry_async` instead of `retry` in async client ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))

## [0.4.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.1...google-cloud-confidentialcomputing-v0.4.2) (2023-11-13)


### Features

* [google-cloud-confidentialcomputing] Add a new field `token_type` to `TokenOptions` message proto ([#12011](https://github.com/googleapis/google-cloud-python/issues/12011)) ([37b1ae9](https://github.com/googleapis/google-cloud-python/commit/37b1ae9e3a03e246d74da6cb3276d2b2d0d9135c))

## [0.4.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.4.0...google-cloud-confidentialcomputing-v0.4.1) (2023-09-19)


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.3.0...google-cloud-confidentialcomputing-v0.4.0) (2023-08-10)


### Features

* Add a new field `partial_errors` to `VerifyAttestationResponse` proto ([#11559](https://github.com/googleapis/google-cloud-python/issues/11559)) ([0c9b83a](https://github.com/googleapis/google-cloud-python/commit/0c9b83abfad6c66bc91008991b760118d1b70a01))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.2.0...google-cloud-confidentialcomputing-v0.3.0) (2023-08-09)


### Features

* Mark all fields `Optional` for `ContainerImageSignagure` proto ([#11547](https://github.com/googleapis/google-cloud-python/issues/11547)) ([f6a6175](https://github.com/googleapis/google-cloud-python/commit/f6a617587e1591c6b3aaa6b41a901f40b95b0f73))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.1.1...google-cloud-confidentialcomputing-v0.2.0) (2023-08-03)


### Features

* Added support for signed container image and custom audience and nonce requests ([#11525](https://github.com/googleapis/google-cloud-python/issues/11525)) ([58158d3](https://github.com/googleapis/google-cloud-python/commit/58158d397f71f41a3e7fd84203d2a859f9ec462a))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-confidentialcomputing-v0.1.0...google-cloud-confidentialcomputing-v0.1.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## 0.1.0 (2023-04-19)


### Features

* add initial files for google.cloud.confidentialcomputing.v1 ([#11102](https://github.com/googleapis/google-cloud-python/issues/11102)) ([816cd75](https://github.com/googleapis/google-cloud-python/commit/816cd752bd8a354d82c19ec75dbb5f3056e2d480))

## Changelog
