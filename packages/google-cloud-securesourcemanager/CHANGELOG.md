# Changelog

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
