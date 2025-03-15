# Changelog

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.14...google-cloud-securesourcemanager-v0.1.15) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([784a3ca](https://github.com/googleapis/google-cloud-python/commit/784a3ca7a180453320521753f5bce71de329d65c))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.13...google-cloud-securesourcemanager-v0.1.14) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([770cf0f](https://github.com/googleapis/google-cloud-python/commit/770cf0f31125586a8622e9639f6d24c1bafa9b31))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.12...google-cloud-securesourcemanager-v0.1.13) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))
* Add support for reading selective GAPIC generation methods from service YAML ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.11...google-cloud-securesourcemanager-v0.1.12) (2024-12-12)


### Features

* Add support for opt-in debug logging ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.10...google-cloud-securesourcemanager-v0.1.11) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13245](https://github.com/googleapis/google-cloud-python/issues/13245)) ([875f712](https://github.com/googleapis/google-cloud-python/commit/875f712265a36919409964f5ade218330f1d0147))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.9...google-cloud-securesourcemanager-v0.1.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13209](https://github.com/googleapis/google-cloud-python/issues/13209)) ([5f2e30d](https://github.com/googleapis/google-cloud-python/commit/5f2e30d62eea6080f5707ee18755f2bb812ad00b))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.8...google-cloud-securesourcemanager-v0.1.9) (2024-10-23)


### Features

* [google-cloud-securesourcemanager] Add field `instance` to message `.google.cloud.securesourcemanager.v1.ListRepositoriesRequest` ([#13176](https://github.com/googleapis/google-cloud-python/issues/13176)) ([18b266f](https://github.com/googleapis/google-cloud-python/commit/18b266f70010b8d233e3a3e9ce97a89caf2e0695))
* Add branch rule APIs ([e6a764b](https://github.com/googleapis/google-cloud-python/commit/e6a764b84fc0529e15c9c1a0721a50809af52369))
* Add field `psc_allowed_projects` to message `.google.cloud.securesourcemanager.v1.Instance` ([e6a764b](https://github.com/googleapis/google-cloud-python/commit/e6a764b84fc0529e15c9c1a0721a50809af52369))


### Documentation

* A comment for field `instance` in message ([18b266f](https://github.com/googleapis/google-cloud-python/commit/18b266f70010b8d233e3a3e9ce97a89caf2e0695))
* A comment for field `instance` in message `.google.cloud.securesourcemanager.v1.Repository` is changed ([e6a764b](https://github.com/googleapis/google-cloud-python/commit/e6a764b84fc0529e15c9c1a0721a50809af52369))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.7...google-cloud-securesourcemanager-v0.1.8) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([52db52e](https://github.com/googleapis/google-cloud-python/commit/52db52ea05c6883b07956d323fdd1d3029806374))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.6...google-cloud-securesourcemanager-v0.1.7) (2024-07-10)


### Features

* add constant `UNKNOWN` to field `State` in message `.google.cloud.securesourcemanager.v1.Instance` ([c3da089](https://github.com/googleapis/google-cloud-python/commit/c3da0899d77a77b9cb50e1c43e36bc191fe16687))
* add field `private_config` to message `.google.cloud.securesourcemanager.v1.Instance` ([c3da089](https://github.com/googleapis/google-cloud-python/commit/c3da0899d77a77b9cb50e1c43e36bc191fe16687))


### Documentation

* A comment for field `instance` in message `.google.cloud.securesourcemanager.v1.Repository` is updated to include data plane vs control plane behavior. ([c3da089](https://github.com/googleapis/google-cloud-python/commit/c3da0899d77a77b9cb50e1c43e36bc191fe16687))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.5...google-cloud-securesourcemanager-v0.1.6) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12869](https://github.com/googleapis/google-cloud-python/issues/12869)) ([e42edbc](https://github.com/googleapis/google-cloud-python/commit/e42edbcf7f4d8ed66b6645c96a01c55fb8cd7666))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.4...google-cloud-securesourcemanager-v0.1.5) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12387](https://github.com/googleapis/google-cloud-python/issues/12387)) ([12ce658](https://github.com/googleapis/google-cloud-python/commit/12ce658210f148eb93d9ff501568fb6f88e77f18))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.3...google-cloud-securesourcemanager-v0.1.4) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([89c1b05](https://github.com/googleapis/google-cloud-python/commit/89c1b054f321b90ab4eed0139a3a2a79c369730d))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.2...google-cloud-securesourcemanager-v0.1.3) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([9e8d039](https://github.com/googleapis/google-cloud-python/commit/9e8d0399c488cb5125d3144ad4a8e25794c123fb))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.1...google-cloud-securesourcemanager-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12243](https://github.com/googleapis/google-cloud-python/issues/12243)) ([e14d4b1](https://github.com/googleapis/google-cloud-python/commit/e14d4b13a883876a420c498a044dc34ea5122629))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-securesourcemanager-v0.1.0...google-cloud-securesourcemanager-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([e9655df](https://github.com/googleapis/google-cloud-python/commit/e9655dff9f393bf3382c668ea2a31dd3332ed192))
* Introduce compatibility with native namespace packages ([e9655df](https://github.com/googleapis/google-cloud-python/commit/e9655dff9f393bf3382c668ea2a31dd3332ed192))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([e9655df](https://github.com/googleapis/google-cloud-python/commit/e9655dff9f393bf3382c668ea2a31dd3332ed192))
* Use `retry_async` instead of `retry` in async client ([e9655df](https://github.com/googleapis/google-cloud-python/commit/e9655dff9f393bf3382c668ea2a31dd3332ed192))

## 0.1.0 (2023-10-13)


### Features

* add initial files for google.cloud.securesourcemanager.v1 ([#11809](https://github.com/googleapis/google-cloud-python/issues/11809)) ([a529c49](https://github.com/googleapis/google-cloud-python/commit/a529c49cad105407f95b7d524e0e1713f6902a85))

## Changelog
