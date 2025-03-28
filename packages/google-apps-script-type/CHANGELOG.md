# Changelog

## [0.3.14](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.13...google-apps-script-type-v0.3.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))

## [0.3.13](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.12...google-apps-script-type-v0.3.13) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.3.12](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.11...google-apps-script-type-v0.3.12) (2025-01-27)


### Documentation

* [google-apps-script-type] Minor documentation edits ([#13464](https://github.com/googleapis/google-cloud-python/issues/13464)) ([c45e8e9](https://github.com/googleapis/google-cloud-python/commit/c45e8e9bb4efbeeb2e1ffb1b4e9847364c33d76a))

## [0.3.11](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.10...google-apps-script-type-v0.3.11) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.3.10](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.9...google-apps-script-type-v0.3.10) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.3.9](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.8...google-apps-script-type-v0.3.9) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([04ec204](https://github.com/googleapis/google-cloud-python/commit/04ec2046ed11c690273912e1bb6220823c7dd7c0))

## [0.3.8](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.7...google-apps-script-type-v0.3.8) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12381](https://github.com/googleapis/google-cloud-python/issues/12381)) ([48ae8ab](https://github.com/googleapis/google-cloud-python/commit/48ae8aba7ec71a382e001b3a659022f942c3b436))

## [0.3.7](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.6...google-apps-script-type-v0.3.7) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12303](https://github.com/googleapis/google-cloud-python/issues/12303)) ([fbb80c3](https://github.com/googleapis/google-cloud-python/commit/fbb80c32f7db91e25bd1cc30966f630728ff6d6a))

## [0.3.6](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.5...google-apps-script-type-v0.3.6) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))

## [0.3.5](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.4...google-apps-script-type-v0.3.5) (2023-12-07)


### Features

* Add support for python 3.12 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Introduce compatibility with native namespace packages ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Use `retry_async` instead of `retry` in async client ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))

## [0.3.4](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.3...google-apps-script-type-v0.3.4) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.3.3](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.2...google-apps-script-type-v0.3.3) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.3.2](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.1...google-apps-script-type-v0.3.2) (2023-06-03)


### Documentation

* fix broken client library documentation links ([#11192](https://github.com/googleapis/google-cloud-python/issues/11192)) ([5e17f7a](https://github.com/googleapis/google-cloud-python/commit/5e17f7a901bbbae8ff9a44ed62f1abd2386da2c8))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.3.0...google-apps-script-type-v0.3.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([900a608](https://github.com/googleapis/google-cloud-python/commit/900a6083e59bfebf215e4e469bc842d8788bba18))


### Documentation

* Add documentation for enums ([900a608](https://github.com/googleapis/google-cloud-python/commit/900a6083e59bfebf215e4e469bc842d8788bba18))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.2.1...google-apps-script-type-v0.3.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#10812](https://github.com/googleapis/google-cloud-python/issues/10812)) ([e5f88ee](https://github.com/googleapis/google-cloud-python/commit/e5f88eebd47c677850d61ddc3774532723f5505e))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.2.0...google-apps-script-type-v0.2.1) (2022-12-06)


### Bug Fixes

* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))
* Drop usage of pkg_resources ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))
* Fix timeout default values ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))


### Documentation

* **samples:** Snippetgen should call await on the operation coroutine before calling result ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-script-type-v0.1.0...google-apps-script-type-v0.2.0) (2022-11-12)


### Features

* add types for google.apps.script.type.calendar ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))
* add types for google.apps.script.type.docs ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))
* add types for google.apps.script.type.drive ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))
* add types for google.apps.script.type.gmail ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))
* add types for google.apps.script.type.sheets ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))
* add types for google.apps.script.type.slides ([4c22dd2](https://github.com/googleapis/google-cloud-python/commit/4c22dd204ea1bafd54d61fbfd353fc9848d76503))

## 0.1.0 (2022-11-10)


### Features

* add initial files for google.apps.script.type ([#10778](https://github.com/googleapis/google-cloud-python/issues/10778)) ([3814477](https://github.com/googleapis/google-cloud-python/commit/3814477a7ecc04e68c631601a6b2820868aacba1))

## Changelog
