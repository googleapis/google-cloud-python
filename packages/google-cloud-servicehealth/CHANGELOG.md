# Changelog

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.9...google-cloud-servicehealth-v0.1.10) (2025-01-02)


### Documentation

* [google-cloud-servicehealth] update documentation for various messages ([#13374](https://github.com/googleapis/google-cloud-python/issues/13374)) ([8e53145](https://github.com/googleapis/google-cloud-python/commit/8e531455b2ea2ecaf19981ad7871bdba0389afaa))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.8...google-cloud-servicehealth-v0.1.9) (2024-12-12)


### Features

* [google-cloud-servicehealth] A new field `id` is added to message `.google.cloud.servicehealth.v1.Product` ([#13307](https://github.com/googleapis/google-cloud-python/issues/13307)) ([b84e0a9](https://github.com/googleapis/google-cloud-python/commit/b84e0a95eb06877d431090bf29d13803b241f975))
* Add support for opt-in debug logging ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.7...google-cloud-servicehealth-v0.1.8) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13245](https://github.com/googleapis/google-cloud-python/issues/13245)) ([875f712](https://github.com/googleapis/google-cloud-python/commit/875f712265a36919409964f5ade218330f1d0147))


### Documentation

* [google-cloud-servicehealth] add missing doc comments ([#13254](https://github.com/googleapis/google-cloud-python/issues/13254)) ([483d1cd](https://github.com/googleapis/google-cloud-python/commit/483d1cd5445638a80cd5752fd61400e54f036f74))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.6...google-cloud-servicehealth-v0.1.7) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13209](https://github.com/googleapis/google-cloud-python/issues/13209)) ([5f2e30d](https://github.com/googleapis/google-cloud-python/commit/5f2e30d62eea6080f5707ee18755f2bb812ad00b))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.5...google-cloud-servicehealth-v0.1.6) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([42c4d04](https://github.com/googleapis/google-cloud-python/commit/42c4d04ee1362ba0ed0f1b6a134ac8e409875b63))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.4...google-cloud-servicehealth-v0.1.5) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12869](https://github.com/googleapis/google-cloud-python/issues/12869)) ([e42edbc](https://github.com/googleapis/google-cloud-python/commit/e42edbcf7f4d8ed66b6645c96a01c55fb8cd7666))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.3...google-cloud-servicehealth-v0.1.4) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12387](https://github.com/googleapis/google-cloud-python/issues/12387)) ([12ce658](https://github.com/googleapis/google-cloud-python/commit/12ce658210f148eb93d9ff501568fb6f88e77f18))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.2...google-cloud-servicehealth-v0.1.3) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([2451e88](https://github.com/googleapis/google-cloud-python/commit/2451e88f302bc582b3f6d01a6ec6aceba7646252))


### Documentation

* [google-cloud-servicehealth] update proto comments ([#12320](https://github.com/googleapis/google-cloud-python/issues/12320)) ([db4e692](https://github.com/googleapis/google-cloud-python/commit/db4e6925f454d3c402989bec3dda043d07153896))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.1...google-cloud-servicehealth-v0.1.2) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-servicehealth-v0.1.0...google-cloud-servicehealth-v0.1.1) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12243](https://github.com/googleapis/google-cloud-python/issues/12243)) ([e14d4b1](https://github.com/googleapis/google-cloud-python/commit/e14d4b13a883876a420c498a044dc34ea5122629))

## 0.1.0 (2024-01-12)


### Features

* add initial files for google.cloud.servicehealth.v1 ([#12189](https://github.com/googleapis/google-cloud-python/issues/12189)) ([6ca7fa2](https://github.com/googleapis/google-cloud-python/commit/6ca7fa209b79f57fce901e049bf2251b2b41e9c1))

## Changelog
