# Changelog

## [1.6.0](https://github.com/googleapis/python-filestore/compare/v1.5.1...v1.6.0) (2023-03-23)


### Features

* Add support for Snapshot ([fe698b2](https://github.com/googleapis/python-filestore/commit/fe698b2674491a31720e56c0f0388474362d9d61))
* Updating the client to match the latest v1 API ([fe698b2](https://github.com/googleapis/python-filestore/commit/fe698b2674491a31720e56c0f0388474362d9d61))


### Documentation

* Fix formatting of request arg in docstring ([#142](https://github.com/googleapis/python-filestore/issues/142)) ([475baaf](https://github.com/googleapis/python-filestore/commit/475baaf0d8a1218371426b2103b33d7e61aa8554))

## [1.5.1](https://github.com/googleapis/python-filestore/compare/v1.5.0...v1.5.1) (2023-02-17)


### Bug Fixes

* Add service_yaml_parameters to py_gapic_library BUILD.bazel targets ([#133](https://github.com/googleapis/python-filestore/issues/133)) ([029b59d](https://github.com/googleapis/python-filestore/commit/029b59db52734ebc120e87f64db84ce45d437304))

## [1.5.0](https://github.com/googleapis/python-filestore/compare/v1.4.1...v1.5.0) (2023-02-09)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#131](https://github.com/googleapis/python-filestore/issues/131)) ([3e2f28c](https://github.com/googleapis/python-filestore/commit/3e2f28ce47961692045700d902800cbba31e544c))

## [1.4.1](https://github.com/googleapis/python-filestore/compare/v1.4.0...v1.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([0ac5913](https://github.com/googleapis/python-filestore/commit/0ac5913b8b25f472f503198f6150f58901498461))


### Documentation

* Add documentation for enums ([0ac5913](https://github.com/googleapis/python-filestore/commit/0ac5913b8b25f472f503198f6150f58901498461))

## [1.4.0](https://github.com/googleapis/python-filestore/compare/v1.3.0...v1.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#123](https://github.com/googleapis/python-filestore/issues/123)) ([1fc907a](https://github.com/googleapis/python-filestore/commit/1fc907ae053da031faaf317c3f8bbbc2c1516f6b))

## [1.3.0](https://github.com/googleapis/python-filestore/compare/v1.2.3...v1.3.0) (2022-12-15)


### Features

* Add support for `google.cloud.filestore.__version__` ([b427d60](https://github.com/googleapis/python-filestore/commit/b427d60c1330ad22d0822b969582f3935b4a3696))
* Add typing to proto.Message based class attributes ([b427d60](https://github.com/googleapis/python-filestore/commit/b427d60c1330ad22d0822b969582f3935b4a3696))


### Bug Fixes

* Add dict typing for client_options ([b427d60](https://github.com/googleapis/python-filestore/commit/b427d60c1330ad22d0822b969582f3935b4a3696))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([e7f87de](https://github.com/googleapis/python-filestore/commit/e7f87de5e047cfe4db75f4b3a2d5ebbe53bf8221))
* Drop usage of pkg_resources ([e7f87de](https://github.com/googleapis/python-filestore/commit/e7f87de5e047cfe4db75f4b3a2d5ebbe53bf8221))
* Fix timeout default values ([e7f87de](https://github.com/googleapis/python-filestore/commit/e7f87de5e047cfe4db75f4b3a2d5ebbe53bf8221))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([b427d60](https://github.com/googleapis/python-filestore/commit/b427d60c1330ad22d0822b969582f3935b4a3696))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([e7f87de](https://github.com/googleapis/python-filestore/commit/e7f87de5e047cfe4db75f4b3a2d5ebbe53bf8221))

## [1.2.3](https://github.com/googleapis/python-filestore/compare/v1.2.2...v1.2.3) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#113](https://github.com/googleapis/python-filestore/issues/113)) ([44b1f4b](https://github.com/googleapis/python-filestore/commit/44b1f4bf289a8d10ea1012829d50953e347f221a))

## [1.2.2](https://github.com/googleapis/python-filestore/compare/v1.2.1...v1.2.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#111](https://github.com/googleapis/python-filestore/issues/111)) ([1b98932](https://github.com/googleapis/python-filestore/commit/1b9893243c2d7ec41c70ba0c80e69919b03df051))

## [1.2.1](https://github.com/googleapis/python-filestore/compare/v1.2.0...v1.2.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#96](https://github.com/googleapis/python-filestore/issues/96)) ([d53e446](https://github.com/googleapis/python-filestore/commit/d53e446405d5267de7959521aca533e9b5bce75e))
* **deps:** require proto-plus >= 1.22.0 ([d53e446](https://github.com/googleapis/python-filestore/commit/d53e446405d5267de7959521aca533e9b5bce75e))

## [1.2.0](https://github.com/googleapis/python-filestore/compare/v1.1.3...v1.2.0) (2022-07-14)


### Features

* add audience parameter ([061c4e6](https://github.com/googleapis/python-filestore/commit/061c4e66c1a5d70f5b3e087b373b5ee986ad79d3))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#86](https://github.com/googleapis/python-filestore/issues/86)) ([061c4e6](https://github.com/googleapis/python-filestore/commit/061c4e66c1a5d70f5b3e087b373b5ee986ad79d3))
* require python 3.7+ ([#88](https://github.com/googleapis/python-filestore/issues/88)) ([990fe7a](https://github.com/googleapis/python-filestore/commit/990fe7a5fac7f896ae1012b5f3b043e4769718cd))

## [1.1.3](https://github.com/googleapis/python-filestore/compare/v1.1.2...v1.1.3) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#77](https://github.com/googleapis/python-filestore/issues/77)) ([4f8b600](https://github.com/googleapis/python-filestore/commit/4f8b6009555a008d7ad483b5801e56efb948dbfa))


### Documentation

* fix changelog header to consistent size ([#76](https://github.com/googleapis/python-filestore/issues/76)) ([07f57aa](https://github.com/googleapis/python-filestore/commit/07f57aa4588f2fbacb554306b38f70970fb918b7))

## [1.1.2](https://github.com/googleapis/python-filestore/compare/v1.1.1...v1.1.2) (2022-05-06)


### Documentation

* fix type in docstring for map fields ([ce8c731](https://github.com/googleapis/python-filestore/commit/ce8c7315d9a7956a253f24ba41f94d645df5a06c))

## [1.1.1](https://github.com/googleapis/python-filestore/compare/v1.1.0...v1.1.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#43](https://github.com/googleapis/python-filestore/issues/43)) ([4f5dd38](https://github.com/googleapis/python-filestore/commit/4f5dd3862fd7dc7b9e226ed7df99623818cf156c))

## [1.1.0](https://github.com/googleapis/python-filestore/compare/v1.0.0...v1.1.0) (2022-02-26)


### Features

* add api key support ([#29](https://github.com/googleapis/python-filestore/issues/29)) ([a72a4fe](https://github.com/googleapis/python-filestore/commit/a72a4fe7f506bc3a6a43d368784b17b4e00695ff))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([314d78e](https://github.com/googleapis/python-filestore/commit/314d78e8e35f4a9cb03b372ec45428dc841e6681))

## [1.0.0](https://www.github.com/googleapis/python-filestore/compare/v0.2.1...v1.0.0) (2021-11-03)


### Features

* bump release level to production/stable ([#7](https://www.github.com/googleapis/python-filestore/issues/7)) ([7b30a52](https://www.github.com/googleapis/python-filestore/commit/7b30a5284bc8595d276af1224a32ff7c7c28e765))

## [0.2.1](https://www.github.com/googleapis/python-filestore/compare/v0.2.0...v0.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([c98e3ab](https://www.github.com/googleapis/python-filestore/commit/c98e3ab4252696f35d6d768e6a5104be0337ed04))
* **deps:** require google-api-core >= 1.28.0 ([c98e3ab](https://www.github.com/googleapis/python-filestore/commit/c98e3ab4252696f35d6d768e6a5104be0337ed04))


### Documentation

* list oneofs in docstring ([c98e3ab](https://www.github.com/googleapis/python-filestore/commit/c98e3ab4252696f35d6d768e6a5104be0337ed04))

## [0.2.0](https://www.github.com/googleapis/python-filestore/compare/v0.1.0...v0.2.0) (2021-10-08)


### Features

* add context manager support in client ([#11](https://www.github.com/googleapis/python-filestore/issues/11)) ([c1fbdff](https://www.github.com/googleapis/python-filestore/commit/c1fbdff93698f09a2e127d8dba935ffe8d9512f5))

## 0.1.0 (2021-10-02)


### Features

* generate v1 ([c95b948](https://www.github.com/googleapis/python-filestore/commit/c95b948e2ef5ed12dacf1b830013a1e5c51147ce))
