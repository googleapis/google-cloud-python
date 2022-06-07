# Changelog

## [1.4.3](https://github.com/googleapis/python-gke-hub/compare/v1.4.2...v1.4.3) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#174](https://github.com/googleapis/python-gke-hub/issues/174)) ([f061842](https://github.com/googleapis/python-gke-hub/commit/f061842b7dfd93e63e46209820c8c8aceeb175a6))


### Documentation

* fix changelog header to consistent size ([#173](https://github.com/googleapis/python-gke-hub/issues/173)) ([396111b](https://github.com/googleapis/python-gke-hub/commit/396111b2d29a682611ac90172fe4ed6fe79e8e26))

## [1.4.2](https://github.com/googleapis/python-gke-hub/compare/v1.4.1...v1.4.2) (2022-05-05)


### Documentation

* fix type in docstring for map fields ([d6acb71](https://github.com/googleapis/python-gke-hub/commit/d6acb71fd8763ab581cc698713e0dc188a333bd6))

## [1.4.1](https://github.com/googleapis/python-gke-hub/compare/v1.4.0...v1.4.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#127](https://github.com/googleapis/python-gke-hub/issues/127)) ([169b080](https://github.com/googleapis/python-gke-hub/commit/169b080afd7c1c89ccda6e0499b00f5e37c8e539))
* **deps:** require proto-plus>=1.15.0 ([169b080](https://github.com/googleapis/python-gke-hub/commit/169b080afd7c1c89ccda6e0499b00f5e37c8e539))

## [1.4.0](https://github.com/googleapis/python-gke-hub/compare/v1.3.0...v1.4.0) (2022-02-24)


### Features

* added support for k8s_version field ([#117](https://github.com/googleapis/python-gke-hub/issues/117)) ([5228f98](https://github.com/googleapis/python-gke-hub/commit/5228f988f8ac27db790db42366301e2d3c62385a))

## [1.3.0](https://github.com/googleapis/python-gke-hub/compare/v1.2.0...v1.3.0) (2022-02-11)


### Features

* add `kubernetes_resource` field ([#107](https://github.com/googleapis/python-gke-hub/issues/107)) ([a887e18](https://github.com/googleapis/python-gke-hub/commit/a887e1897ef34f0bb701b4ad9ecd9559f523648a))
* add api key support ([#110](https://github.com/googleapis/python-gke-hub/issues/110)) ([e2f7a2c](https://github.com/googleapis/python-gke-hub/commit/e2f7a2ca422d9f14964eff8794ee000c4a1efaee))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([2e4c08f](https://github.com/googleapis/python-gke-hub/commit/2e4c08f3fc9b6217b24f380cc5cc4a4bf2fb3e60))


### Documentation

* update API annotation ([a887e18](https://github.com/googleapis/python-gke-hub/commit/a887e1897ef34f0bb701b4ad9ecd9559f523648a))

## [1.2.0](https://www.github.com/googleapis/python-gke-hub/compare/v1.1.0...v1.2.0) (2021-10-14)


### Features

* add support for python 3.10 ([#90](https://www.github.com/googleapis/python-gke-hub/issues/90)) ([5b929d6](https://www.github.com/googleapis/python-gke-hub/commit/5b929d6845b30719e16c71705e861431e83fed3e))

## [1.1.0](https://www.github.com/googleapis/python-gke-hub/compare/v1.0.0...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#87](https://www.github.com/googleapis/python-gke-hub/issues/87)) ([e32a6f6](https://www.github.com/googleapis/python-gke-hub/commit/e32a6f677368bd0637267aea058b344325ddb678))


### Bug Fixes

* improper types in pagers generation ([80c87ba](https://www.github.com/googleapis/python-gke-hub/commit/80c87baf1ce13e9c4377a2fb5d59f0776580758e))

## [1.0.0](https://www.github.com/googleapis/python-gke-hub/compare/v0.2.2...v1.0.0) (2021-09-29)


### Features

* bump release level to production/stable ([#60](https://www.github.com/googleapis/python-gke-hub/issues/60)) ([5877ee6](https://www.github.com/googleapis/python-gke-hub/commit/5877ee64f259cfdae46f2606e0cb1d9ef5fcc5ea))

## [0.2.2](https://www.github.com/googleapis/python-gke-hub/compare/v0.2.1...v0.2.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([7b07616](https://www.github.com/googleapis/python-gke-hub/commit/7b07616c8da7dc504a917634c3749c03e3445148))

## [0.2.1](https://www.github.com/googleapis/python-gke-hub/compare/v0.2.0...v0.2.1) (2021-08-20)


### Bug Fixes

* resolve issue importing library ([#64](https://www.github.com/googleapis/python-gke-hub/issues/64)) ([cfa166e](https://www.github.com/googleapis/python-gke-hub/commit/cfa166e9b9024920bd00b5994d2638ab7716c2d1))

## [0.2.0](https://www.github.com/googleapis/python-gke-hub/compare/v0.1.2...v0.2.0) (2021-07-24)


### Features

* add always_use_jwt_access ([f11dcfd](https://www.github.com/googleapis/python-gke-hub/commit/f11dcfdf34ce4fa26de2fc4779b5b4f46a5c52bd))
* add always_use_jwt_access ([#45](https://www.github.com/googleapis/python-gke-hub/issues/45)) ([225d132](https://www.github.com/googleapis/python-gke-hub/commit/225d13235789a5d778658c2938e2c07df847a0cd))
* add v1 ([#51](https://www.github.com/googleapis/python-gke-hub/issues/51)) ([f11dcfd](https://www.github.com/googleapis/python-gke-hub/commit/f11dcfdf34ce4fa26de2fc4779b5b4f46a5c52bd))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#55](https://www.github.com/googleapis/python-gke-hub/issues/55)) ([7035364](https://www.github.com/googleapis/python-gke-hub/commit/703536465a766c452a8c27a6ee951dec35cf3c4f))
* enable self signed jwt for grpc ([#58](https://www.github.com/googleapis/python-gke-hub/issues/58)) ([66f14c9](https://www.github.com/googleapis/python-gke-hub/commit/66f14c93978f97f8180ca8f0a02856d4d633a2bf))
* **v1beta1:** disable always_use_jwt_access ([#52](https://www.github.com/googleapis/python-gke-hub/issues/52)) ([100f72e](https://www.github.com/googleapis/python-gke-hub/commit/100f72e7181f4faeb04a76e106888ffd766ed9ef))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-gke-hub/issues/1127)) ([#40](https://www.github.com/googleapis/python-gke-hub/issues/40)) ([8f703d7](https://www.github.com/googleapis/python-gke-hub/commit/8f703d74ad3d9b3ea31b2136ed4e97594b52f832)), closes [#1126](https://www.github.com/googleapis/python-gke-hub/issues/1126)
* add Samples section to CONTRIBUTING.rst ([#56](https://www.github.com/googleapis/python-gke-hub/issues/56)) ([b08cf7e](https://www.github.com/googleapis/python-gke-hub/commit/b08cf7e5f2dbb1f3615f5b652c2d69f991d8aa69))

## [0.1.2](https://www.github.com/googleapis/python-gke-hub/compare/v0.1.1...v0.1.2) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#37](https://www.github.com/googleapis/python-gke-hub/issues/37)) ([65eee87](https://www.github.com/googleapis/python-gke-hub/commit/65eee87a7f48cce25cc89fdedaf383de0fdc4247))

## [0.1.1](https://www.github.com/googleapis/python-gke-hub/compare/v0.1.0...v0.1.1) (2021-05-27)


### Bug Fixes

* **deps:** add packaging requirement ([#31](https://www.github.com/googleapis/python-gke-hub/issues/31)) ([71eb607](https://www.github.com/googleapis/python-gke-hub/commit/71eb607254ce524cf47765fd3e9fb2427d139dc8))

## 0.1.0 (2021-03-16)


### Features

* generate v1beta1 ([655d649](https://www.github.com/googleapis/python-gke-hub/commit/655d64963fcdc7a3102b1b025ba967eab26a3ff3))
