# Changelog

## [0.1.21](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.20...google-cloud-securitycentermanagement-v0.1.21) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([784a3ca](https://github.com/googleapis/google-cloud-python/commit/784a3ca7a180453320521753f5bce71de329d65c))

## [0.1.20](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.19...google-cloud-securitycentermanagement-v0.1.20) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([770cf0f](https://github.com/googleapis/google-cloud-python/commit/770cf0f31125586a8622e9639f6d24c1bafa9b31))

## [0.1.19](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.18...google-cloud-securitycentermanagement-v0.1.19) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))
* Add support for reading selective GAPIC generation methods from service YAML ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))

## [0.1.18](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.17...google-cloud-securitycentermanagement-v0.1.18) (2024-12-12)


### Features

* Add support for opt-in debug logging ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))

## [0.1.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.16...google-cloud-securitycentermanagement-v0.1.17) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13245](https://github.com/googleapis/google-cloud-python/issues/13245)) ([875f712](https://github.com/googleapis/google-cloud-python/commit/875f712265a36919409964f5ade218330f1d0147))

## [0.1.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.15...google-cloud-securitycentermanagement-v0.1.16) (2024-10-31)


### Documentation

* update documentation ([f611927](https://github.com/googleapis/google-cloud-python/commit/f61192719e42218a751e30ad9aca4c40d795c63a))

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.14...google-cloud-securitycentermanagement-v0.1.15) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13209](https://github.com/googleapis/google-cloud-python/issues/13209)) ([5f2e30d](https://github.com/googleapis/google-cloud-python/commit/5f2e30d62eea6080f5707ee18755f2bb812ad00b))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.13...google-cloud-securitycentermanagement-v0.1.14) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([42c4d04](https://github.com/googleapis/google-cloud-python/commit/42c4d04ee1362ba0ed0f1b6a134ac8e409875b63))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.12...google-cloud-securitycentermanagement-v0.1.13) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12869](https://github.com/googleapis/google-cloud-python/issues/12869)) ([e42edbc](https://github.com/googleapis/google-cloud-python/commit/e42edbcf7f4d8ed66b6645c96a01c55fb8cd7666))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.11...google-cloud-securitycentermanagement-v0.1.12) (2024-06-24)


### Features

* add `show_eligible_modules_only` field to `GetSecurityCenterServiceRequest` message ([2e0f94e](https://github.com/googleapis/google-cloud-python/commit/2e0f94e0f96054a884af7fe8ae80612e04faa91a))
* add `TOXIC_COMBINATION` to `FindingClass` enum ([2e0f94e](https://github.com/googleapis/google-cloud-python/commit/2e0f94e0f96054a884af7fe8ae80612e04faa91a))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.10...google-cloud-securitycentermanagement-v0.1.11) (2024-06-19)


### Features

* add an INGEST_ONLY EnablementState ([5363fa3](https://github.com/googleapis/google-cloud-python/commit/5363fa34a5c2bb524321d0b09c5f467e784ddb3c))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.9...google-cloud-securitycentermanagement-v0.1.10) (2024-06-10)


### Documentation

* minor docs formatting in `UpdateSecurityCenterServiceRequest.validate_only` ([01e36a7](https://github.com/googleapis/google-cloud-python/commit/01e36a7b4a7e58ff48fcf4dc1098f4447a7e70f6))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.8...google-cloud-securitycentermanagement-v0.1.9) (2024-05-27)


### Features

* add support for new Security Center Management APIs ([9896255](https://github.com/googleapis/google-cloud-python/commit/98962551bbe4c8901950a9769c7d5fd4369f2ef5))


### Documentation

* update comment formatting throughout API ([9896255](https://github.com/googleapis/google-cloud-python/commit/98962551bbe4c8901950a9769c7d5fd4369f2ef5))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.7...google-cloud-securitycentermanagement-v0.1.8) (2024-03-22)


### Bug Fixes

* annotate EffectiveEventThreatDetectionCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate EffectiveSecurityHealthAnalyticsCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate EventThreatDetectionCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))
* annotate SecurityHealthAnalyticsCustomModule.name as IDENTIFIER ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))


### Documentation

* updated comments ([9360249](https://github.com/googleapis/google-cloud-python/commit/93602495cf8265cedd188c042c6b45275971980e))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.6...google-cloud-securitycentermanagement-v0.1.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0  ([add6a6d](https://github.com/googleapis/google-cloud-python/commit/add6a6d5198c81e35e5edf8997eb9fde2cc9c81b))


### Documentation

* Clarify documentation for ListDescendantSecurityHealthAnalyticsCustomModules RPC and CustomConfig message ([add6a6d](https://github.com/googleapis/google-cloud-python/commit/add6a6d5198c81e35e5edf8997eb9fde2cc9c81b))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.5...google-cloud-securitycentermanagement-v0.1.6) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([89c1b05](https://github.com/googleapis/google-cloud-python/commit/89c1b054f321b90ab4eed0139a3a2a79c369730d))


### Documentation

* [google-cloud-securitycentermanagement] Finish a sentence with a period ([#12300](https://github.com/googleapis/google-cloud-python/issues/12300)) ([833998a](https://github.com/googleapis/google-cloud-python/commit/833998a27193f6d9c95d054a352702439c596165))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.4...google-cloud-securitycentermanagement-v0.1.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.3...google-cloud-securitycentermanagement-v0.1.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12243](https://github.com/googleapis/google-cloud-python/issues/12243)) ([e14d4b1](https://github.com/googleapis/google-cloud-python/commit/e14d4b13a883876a420c498a044dc34ea5122629))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.2...google-cloud-securitycentermanagement-v0.1.3) (2024-01-19)


### Documentation

* [google-cloud-securitycentermanagement] update documentation for UpdateSecurityHealthAnalyticsCustomModule update_mask field ([#12196](https://github.com/googleapis/google-cloud-python/issues/12196)) ([c7cf0a1](https://github.com/googleapis/google-cloud-python/commit/c7cf0a1c754091fb5b141dd7a9238c63f9d1f36e))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.1...google-cloud-securitycentermanagement-v0.1.2) (2024-01-08)


### Documentation

* [google-cloud-securitycentermanagement] updates on multiple comments, syncing terminology and clarifying some aspects ([#12151](https://github.com/googleapis/google-cloud-python/issues/12151)) ([461c76b](https://github.com/googleapis/google-cloud-python/commit/461c76bbc6bd7cda3ef6da0a0ec7e2418c1532aa))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securitycentermanagement-v0.1.0...google-cloud-securitycentermanagement-v0.1.1) (2024-01-04)


### Documentation

* [google-cloud-securitycentermanagement] clarify several RPC descriptions ([#12146](https://github.com/googleapis/google-cloud-python/issues/12146)) ([a7e4920](https://github.com/googleapis/google-cloud-python/commit/a7e492084f88c72d77127d6adf9feb537362ca18))

## 0.1.0 (2023-12-07)


### Features

* add initial files for google.cloud.securitycentermanagement.v1 ([#12089](https://github.com/googleapis/google-cloud-python/issues/12089)) ([48e7c5f](https://github.com/googleapis/google-cloud-python/commit/48e7c5f9b3747f7ccf85733a99666a3df7206c94))

## Changelog
