# Changelog

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.13...google-cloud-support-v0.1.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([4757dae](https://github.com/googleapis/google-cloud-python/commit/4757daede978618382ba46f4aa91bb9cfd9b937b))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.12...google-cloud-support-v0.1.13) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))
* Add support for reading selective GAPIC generation methods from service YAML ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.11...google-cloud-support-v0.1.12) (2024-12-12)


### Features

* Add support for opt-in debug logging ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.10...google-cloud-support-v0.1.11) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13246](https://github.com/googleapis/google-cloud-python/issues/13246)) ([bcad563](https://github.com/googleapis/google-cloud-python/commit/bcad563acea541bb51f9fbd005f18e9f32e381f0))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.9...google-cloud-support-v0.1.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13210](https://github.com/googleapis/google-cloud-python/issues/13210)) ([0b62ac6](https://github.com/googleapis/google-cloud-python/commit/0b62ac6aa99bd3259a088097630f2bd1f06825e6))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.8...google-cloud-support-v0.1.9) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([9cdac77](https://github.com/googleapis/google-cloud-python/commit/9cdac77b20a8c9720aa668639e3ca6d1e759a2de))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.7...google-cloud-support-v0.1.8) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12870](https://github.com/googleapis/google-cloud-python/issues/12870)) ([4d16761](https://github.com/googleapis/google-cloud-python/commit/4d16761640dd8e35410b3219b7d675d7668d2f88))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.6...google-cloud-support-v0.1.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12387](https://github.com/googleapis/google-cloud-python/issues/12387)) ([12ce658](https://github.com/googleapis/google-cloud-python/commit/12ce658210f148eb93d9ff501568fb6f88e77f18))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.5...google-cloud-support-v0.1.6) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12310](https://github.com/googleapis/google-cloud-python/issues/12310)) ([41821da](https://github.com/googleapis/google-cloud-python/commit/41821da1fe08cc2aeeefc8c8f516023e4b0d0700))
* fix ValueError in test__validate_universe_domain ([2451e88](https://github.com/googleapis/google-cloud-python/commit/2451e88f302bc582b3f6d01a6ec6aceba7646252))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.4...google-cloud-support-v0.1.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([e16032f](https://github.com/googleapis/google-cloud-python/commit/e16032ffe9b15dfd008b51f046dbb10211356998))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([e16032f](https://github.com/googleapis/google-cloud-python/commit/e16032ffe9b15dfd008b51f046dbb10211356998))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([e16032f](https://github.com/googleapis/google-cloud-python/commit/e16032ffe9b15dfd008b51f046dbb10211356998))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.3...google-cloud-support-v0.1.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12243](https://github.com/googleapis/google-cloud-python/issues/12243)) ([e14d4b1](https://github.com/googleapis/google-cloud-python/commit/e14d4b13a883876a420c498a044dc34ea5122629))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.2...google-cloud-support-v0.1.3) (2023-12-07)


### Features

* Add support for python 3.12 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Introduce compatibility with native namespace packages ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Use `retry_async` instead of `retry` in async client ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.1...google-cloud-support-v0.1.2) (2023-09-19)


### Documentation

* Minor formatting ([025219f](https://github.com/googleapis/google-cloud-python/commit/025219f5c04803651e20eae4c0186b87608f4db4))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-support-v0.1.0...google-cloud-support-v0.1.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11449](https://github.com/googleapis/google-cloud-python/issues/11449)) ([3885820](https://github.com/googleapis/google-cloud-python/commit/388582082828e22a517c4f794901ee5dcbc31bd9))

## 0.1.0 (2023-05-12)


### Features

* add initial files for google.cloud.support.v2 ([#11176](https://github.com/googleapis/google-cloud-python/issues/11176)) ([84d9653](https://github.com/googleapis/google-cloud-python/commit/84d9653eb3fb4c22c039934a94e39d19b8c8705c))

## Changelog
