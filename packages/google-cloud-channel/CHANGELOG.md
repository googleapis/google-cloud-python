# Changelog

## [1.8.0](https://github.com/googleapis/python-channel/compare/v1.7.1...v1.8.0) (2022-04-27)


### Features

* Add API definitions for Cloud Channel Repricing APIs ([#169](https://github.com/googleapis/python-channel/issues/169)) ([18db43c](https://github.com/googleapis/python-channel/commit/18db43c21a935ab9bc52539edf8f97556aa05819))
* Add filter in ListCustomersRequest ([#167](https://github.com/googleapis/python-channel/issues/167)) ([2a88151](https://github.com/googleapis/python-channel/commit/2a881514bb8ecfbcbdec9dac15663f4caa00bd00))

### [1.7.1](https://github.com/googleapis/python-channel/compare/v1.7.0...v1.7.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#149](https://github.com/googleapis/python-channel/issues/149)) ([5c2908e](https://github.com/googleapis/python-channel/commit/5c2908e5f02336d3457d9625b54c73d02745e47d))
* **deps:** require proto-plus>=1.15.0 ([5c2908e](https://github.com/googleapis/python-channel/commit/5c2908e5f02336d3457d9625b54c73d02745e47d))

## [1.7.0](https://github.com/googleapis/python-channel/compare/v1.6.3...v1.7.0) (2022-02-26)


### Features

* add api key support ([#133](https://github.com/googleapis/python-channel/issues/133)) ([df6f6d7](https://github.com/googleapis/python-channel/commit/df6f6d723d507cb332b70c343c92468b90298327))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([f57605e](https://github.com/googleapis/python-channel/commit/f57605ec93277a32f88d33967b704c45e3fc060a))


### Documentation

* clarify language for provisioning_id ([#140](https://github.com/googleapis/python-channel/issues/140)) ([a925354](https://github.com/googleapis/python-channel/commit/a925354a36a6587219a6525da100afbd36f48a68))
* Update description for ProvisionedService.provisioning_id ([#137](https://github.com/googleapis/python-channel/issues/137)) ([9b24071](https://github.com/googleapis/python-channel/commit/9b24071c8701355bf29916c0a35cc1d8f067d12e))

### [1.6.3](https://www.github.com/googleapis/python-channel/compare/v1.6.2...v1.6.3) (2021-11-13)


### Documentation

* clarify entitlement parameter `assigned_units` ([#122](https://www.github.com/googleapis/python-channel/issues/122)) ([7bb783e](https://www.github.com/googleapis/python-channel/commit/7bb783ef1ba20506f35fed649a079a7b153eddb4))

### [1.6.2](https://www.github.com/googleapis/python-channel/compare/v1.6.1...v1.6.2) (2021-11-04)


### Documentation

* clarified usage of entitlement parameters ([#116](https://www.github.com/googleapis/python-channel/issues/116)) ([20fb1ff](https://www.github.com/googleapis/python-channel/commit/20fb1ffdf922875d420266c9a761c184fe19d671))

### [1.6.1](https://www.github.com/googleapis/python-channel/compare/v1.6.0...v1.6.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([339c62c](https://www.github.com/googleapis/python-channel/commit/339c62c4a1b491bd86bb70530376b65183a2b7d4))
* **deps:** require google-api-core >= 1.28.0 ([339c62c](https://www.github.com/googleapis/python-channel/commit/339c62c4a1b491bd86bb70530376b65183a2b7d4))


### Documentation

* list oneofs in docstring ([339c62c](https://www.github.com/googleapis/python-channel/commit/339c62c4a1b491bd86bb70530376b65183a2b7d4))

## [1.6.0](https://www.github.com/googleapis/python-channel/compare/v1.5.0...v1.6.0) (2021-10-27)


### Features

* add resource type to ChannelPartnerLink ([#112](https://www.github.com/googleapis/python-channel/issues/112)) ([76433c4](https://www.github.com/googleapis/python-channel/commit/76433c4869cdbaec4c43f2a85632a9e2a272f207))

## [1.5.0](https://www.github.com/googleapis/python-channel/compare/v1.4.0...v1.5.0) (2021-10-18)


### Features

* add trove classifier for python 3.9 and python 3.10 ([#105](https://www.github.com/googleapis/python-channel/issues/105)) ([8c4eb48](https://www.github.com/googleapis/python-channel/commit/8c4eb48881d99dbc6a642a7cb771c69b2c6e6242))

## [1.4.0](https://www.github.com/googleapis/python-channel/compare/v1.3.2...v1.4.0) (2021-10-08)


### Features

* add context manager support in client ([#102](https://www.github.com/googleapis/python-channel/issues/102)) ([acf8bb2](https://www.github.com/googleapis/python-channel/commit/acf8bb2ce65cf64a9bee20362b49c207f17ffe91))

### [1.3.2](https://www.github.com/googleapis/python-channel/compare/v1.3.1...v1.3.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([dae83af](https://www.github.com/googleapis/python-channel/commit/dae83af170d1d5734ba3b1b72ffc9710adfd2a67))

### [1.3.1](https://www.github.com/googleapis/python-channel/compare/v1.3.0...v1.3.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([2e959cc](https://www.github.com/googleapis/python-channel/commit/2e959cc025ddb9677796bc87707f82132333f59d))

## [1.3.0](https://www.github.com/googleapis/python-channel/compare/v1.2.3...v1.3.0) (2021-09-23)


### Features

* add ImportCustomer ([#90](https://www.github.com/googleapis/python-channel/issues/90)) ([2bb2d89](https://www.github.com/googleapis/python-channel/commit/2bb2d8987da8a6138bef45c5fd278cb25235cfa7))

### [1.2.3](https://www.github.com/googleapis/python-channel/compare/v1.2.2...v1.2.3) (2021-08-31)


### Bug Fixes

* disable self signed jwt if users provide their own credential ([#86](https://www.github.com/googleapis/python-channel/issues/86)) ([d7c07f8](https://www.github.com/googleapis/python-channel/commit/d7c07f8d579ce55ea86520e6a7b7a268befae92d))

### [1.2.2](https://www.github.com/googleapis/python-channel/compare/v1.2.1...v1.2.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#76](https://www.github.com/googleapis/python-channel/issues/76)) ([016111e](https://www.github.com/googleapis/python-channel/commit/016111ee4750d047c44324bf3dca752560840376))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#72](https://www.github.com/googleapis/python-channel/issues/72)) ([b70a090](https://www.github.com/googleapis/python-channel/commit/b70a0900ab7b820e623a286cbd6f0e5c29ad9256))


### Miscellaneous Chores

* release as 1.2.2 ([#77](https://www.github.com/googleapis/python-channel/issues/77)) ([2e950a4](https://www.github.com/googleapis/python-channel/commit/2e950a41e5099facad90b884fe24f43e00b59255))

### [1.2.1](https://www.github.com/googleapis/python-channel/compare/v1.2.0...v1.2.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#71](https://www.github.com/googleapis/python-channel/issues/71)) ([36ba3c3](https://www.github.com/googleapis/python-channel/commit/36ba3c36d9ffb37c1f156fd69f7216c331f55f87))

## [1.2.0](https://www.github.com/googleapis/python-channel/compare/v1.1.1...v1.2.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#64](https://www.github.com/googleapis/python-channel/issues/64)) ([45621e5](https://www.github.com/googleapis/python-channel/commit/45621e5eabad6ff6979b89d619dcbf979ed78d63))


### Bug Fixes

* disable always_use_jwt_access ([2f8fa52](https://www.github.com/googleapis/python-channel/commit/2f8fa52e232e5468e6797d2b14166c7f319a0ca1))
* disable always_use_jwt_access ([#68](https://www.github.com/googleapis/python-channel/issues/68)) ([2f8fa52](https://www.github.com/googleapis/python-channel/commit/2f8fa52e232e5468e6797d2b14166c7f319a0ca1))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-channel/issues/1127)) ([#59](https://www.github.com/googleapis/python-channel/issues/59)) ([f358de3](https://www.github.com/googleapis/python-channel/commit/f358de3eb94fc9c870a899e3d94d93c5f14b5b0d)), closes [#1126](https://www.github.com/googleapis/python-channel/issues/1126)

### [1.1.1](https://www.github.com/googleapis/python-channel/compare/v1.1.0...v1.1.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#55](https://www.github.com/googleapis/python-channel/issues/55)) ([7747953](https://www.github.com/googleapis/python-channel/commit/7747953eb02ae952108cc9d2dcd66f939e60e115))

## [1.1.0](https://www.github.com/googleapis/python-channel/compare/v1.0.0...v1.1.0) (2021-06-10)


### Features

* Add a new enum value LICENSE_CAP_CHANGED to enum EntitlementEvent.Type. ([164539d](https://www.github.com/googleapis/python-channel/commit/164539dc0892481a739bfe4372c35be8d74480d9))
* Add a new LookupOffer RPC and LookupOfferRequest proto. ([164539d](https://www.github.com/googleapis/python-channel/commit/164539dc0892481a739bfe4372c35be8d74480d9))
* Add additional_bindings to HTTP annotations of Customer related APIs (list/create/get/update/delete). ([164539d](https://www.github.com/googleapis/python-channel/commit/164539dc0892481a739bfe4372c35be8d74480d9))
* Add/Update API definitions for Cloud Channel API ([#53](https://www.github.com/googleapis/python-channel/issues/53)) ([164539d](https://www.github.com/googleapis/python-channel/commit/164539dc0892481a739bfe4372c35be8d74480d9))
* Update descriptions of APIs. ([164539d](https://www.github.com/googleapis/python-channel/commit/164539dc0892481a739bfe4372c35be8d74480d9))

## [1.0.0](https://www.github.com/googleapis/python-channel/compare/v0.3.0...v1.0.0) (2021-06-02)


### Features

* bump release level to production/stable ([#46](https://www.github.com/googleapis/python-channel/issues/46)) ([3460f68](https://www.github.com/googleapis/python-channel/commit/3460f683a4e8f1a2f94a1eeb92af7eae1dcdb02b))


### Miscellaneous Chores

* release as 1.0.0 ([#51](https://www.github.com/googleapis/python-channel/issues/51)) ([00710b6](https://www.github.com/googleapis/python-channel/commit/00710b6566540ba111c5bb3705f892e8f743b1c2))

## [0.3.0](https://www.github.com/googleapis/python-channel/compare/v0.2.1...v0.3.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([c218e2e](https://www.github.com/googleapis/python-channel/commit/c218e2efeef2f2e4cf1646644a8d4c38be021bdf))


### Bug Fixes

* add async client to %name_%version/init.py ([c218e2e](https://www.github.com/googleapis/python-channel/commit/c218e2efeef2f2e4cf1646644a8d4c38be021bdf))
* **deps:** add packaging requirement ([#43](https://www.github.com/googleapis/python-channel/issues/43)) ([e368062](https://www.github.com/googleapis/python-channel/commit/e36806211b8b3392811eb5ee1047517f840265c7))

### [0.2.1](https://www.github.com/googleapis/python-channel/compare/v0.2.0...v0.2.1) (2021-04-07)


### Bug Fixes

* BREAKING deprecate TransferableSkus fields ([#14](https://www.github.com/googleapis/python-channel/issues/14)) ([0d3b493](https://www.github.com/googleapis/python-channel/commit/0d3b4939cdae196ea9b0edc00e13f61d7d71777d))

## [0.2.0](https://www.github.com/googleapis/python-channel/compare/v0.1.0...v0.2.0) (2021-02-11)


### Features

* add Pub/Sub endpoints for Cloud Channnel API ([#9](https://www.github.com/googleapis/python-channel/issues/9)) ([2c483c8](https://www.github.com/googleapis/python-channel/commit/2c483c8ec24bba25fdea7a1f46d3d5396fe2076a))

## 0.1.0 (2021-01-14)


### Features

* generate v1 ([a95c9cf](https://www.github.com/googleapis/python-channel/commit/a95c9cf86cc9188c1e3eb8535c62367d141658cc))
