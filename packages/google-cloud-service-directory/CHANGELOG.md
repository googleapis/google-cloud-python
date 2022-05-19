# Changelog

## [1.4.0](https://github.com/googleapis/python-service-directory/compare/v1.3.1...v1.4.0) (2022-05-05)


### Features

* AuditConfig for IAM v1 ([ab48a2a](https://github.com/googleapis/python-service-directory/commit/ab48a2a2f2dddfaf9bc18b53f99b379ad66098d2))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([ab48a2a](https://github.com/googleapis/python-service-directory/commit/ab48a2a2f2dddfaf9bc18b53f99b379ad66098d2))


### Documentation

* fix type in docstring for map fields ([ab48a2a](https://github.com/googleapis/python-service-directory/commit/ab48a2a2f2dddfaf9bc18b53f99b379ad66098d2))

### [1.3.1](https://github.com/googleapis/python-service-directory/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#162](https://github.com/googleapis/python-service-directory/issues/162)) ([8cf5f69](https://github.com/googleapis/python-service-directory/commit/8cf5f6950ccb302aac014a539855206403a50baf))
* **deps:** require proto-plus>=1.15.0 ([8cf5f69](https://github.com/googleapis/python-service-directory/commit/8cf5f6950ccb302aac014a539855206403a50baf))

## [1.3.0](https://github.com/googleapis/python-service-directory/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#148](https://github.com/googleapis/python-service-directory/issues/148)) ([a562a5d](https://github.com/googleapis/python-service-directory/commit/a562a5d8f530b41078062612b9916bc76882f211))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([55c52b5](https://github.com/googleapis/python-service-directory/commit/55c52b5b67891ac723a34fae22040feb5b5fcf15))

### [1.2.1](https://www.github.com/googleapis/python-service-directory/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([809bcd7](https://www.github.com/googleapis/python-service-directory/commit/809bcd7ee993eba50cb3be1cf70658beb008db5b))
* **deps:** require google-api-core >= 1.28.0 ([809bcd7](https://www.github.com/googleapis/python-service-directory/commit/809bcd7ee993eba50cb3be1cf70658beb008db5b))


### Documentation

* list oneofs in docstring ([809bcd7](https://www.github.com/googleapis/python-service-directory/commit/809bcd7ee993eba50cb3be1cf70658beb008db5b))

## [1.2.0](https://www.github.com/googleapis/python-service-directory/compare/v1.1.0...v1.2.0) (2021-10-20)


### Features

* add support for python 3.10 ([#126](https://www.github.com/googleapis/python-service-directory/issues/126)) ([3d3847c](https://www.github.com/googleapis/python-service-directory/commit/3d3847cd14542934a4b992ab789bbc5f1bffe2ef))


### Documentation

* fix docstring formatting ([#130](https://www.github.com/googleapis/python-service-directory/issues/130)) ([a440a30](https://www.github.com/googleapis/python-service-directory/commit/a440a307044cb58c301111df7491ce59778abaac))

## [1.1.0](https://www.github.com/googleapis/python-service-directory/compare/v1.0.4...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#122](https://www.github.com/googleapis/python-service-directory/issues/122)) ([59229eb](https://www.github.com/googleapis/python-service-directory/commit/59229ebe9f17be35cb39119cbae2e19e7a4c8732))

### [1.0.4](https://www.github.com/googleapis/python-service-directory/compare/v1.0.3...v1.0.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([1b0841d](https://www.github.com/googleapis/python-service-directory/commit/1b0841dec49d193c777601ff16ee0706395349b3))

### [1.0.3](https://www.github.com/googleapis/python-service-directory/compare/v1.0.2...v1.0.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([b1982e1](https://www.github.com/googleapis/python-service-directory/commit/b1982e1e3d9214c93b59dbbb1f9ff00532fc6120))

### [1.0.2](https://www.github.com/googleapis/python-service-directory/compare/v1.0.1...v1.0.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#101](https://www.github.com/googleapis/python-service-directory/issues/101)) ([b81c721](https://www.github.com/googleapis/python-service-directory/commit/b81c721ccebd363b078f4c6acbe6deef6a70ff7e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#97](https://www.github.com/googleapis/python-service-directory/issues/97)) ([195861c](https://www.github.com/googleapis/python-service-directory/commit/195861c821be6a3ba853074d07a609ef67a48bcf))


### Miscellaneous Chores

* release as 1.0.2 ([#102](https://www.github.com/googleapis/python-service-directory/issues/102)) ([47caf13](https://www.github.com/googleapis/python-service-directory/commit/47caf1346029bc6d017a1498f3a9b97e396ef667))

### [1.0.1](https://www.github.com/googleapis/python-service-directory/compare/v1.0.0...v1.0.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#96](https://www.github.com/googleapis/python-service-directory/issues/96)) ([ec30558](https://www.github.com/googleapis/python-service-directory/commit/ec30558ee8b89b951509e3f7b9cea6f548b69fe6))

## [1.0.0](https://www.github.com/googleapis/python-service-directory/compare/v0.5.0...v1.0.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#87](https://www.github.com/googleapis/python-service-directory/issues/87)) ([6104fe4](https://www.github.com/googleapis/python-service-directory/commit/6104fe4e8ee660031562291ac216d6376b33cb73))
* bump release level to production/stable ([#77](https://www.github.com/googleapis/python-service-directory/issues/77)) ([b267e2f](https://www.github.com/googleapis/python-service-directory/commit/b267e2f326b5247c84800c8f23e47b53540b663a))
* support self-signed JWT flow for service accounts ([a0387dd](https://www.github.com/googleapis/python-service-directory/commit/a0387dd9d4fd8303e96f2d028b5c450546e26ec0))
* Update Service Directory v1beta1 protos to include VPC Network field, and create/modify timestamp fields. ([#88](https://www.github.com/googleapis/python-service-directory/issues/88)) ([e7fba11](https://www.github.com/googleapis/python-service-directory/commit/e7fba11e53b85ff25620ba92e8859206fd7884d8))


### Bug Fixes

* add async client to %name_%version/init.py ([a0387dd](https://www.github.com/googleapis/python-service-directory/commit/a0387dd9d4fd8303e96f2d028b5c450546e26ec0))
* disable always_use_jwt_access ([1df4a39](https://www.github.com/googleapis/python-service-directory/commit/1df4a3918f59264f1b3b3041ae7c8a51460ed80f))
* disable always_use_jwt_access ([#91](https://www.github.com/googleapis/python-service-directory/issues/91)) ([1df4a39](https://www.github.com/googleapis/python-service-directory/commit/1df4a3918f59264f1b3b3041ae7c8a51460ed80f))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-service-directory/issues/1127)) ([#84](https://www.github.com/googleapis/python-service-directory/issues/84)) ([d9c20bb](https://www.github.com/googleapis/python-service-directory/commit/d9c20bb7dc9f393d0383e69367f5e1ec703ac416))


### Miscellaneous Chores

* release as 1.0.0 ([#82](https://www.github.com/googleapis/python-service-directory/issues/82)) ([a3eaeff](https://www.github.com/googleapis/python-service-directory/commit/a3eaeff0750200a53969c2be0b2d41129e8c194a))

## [0.5.0](https://www.github.com/googleapis/python-service-directory/compare/v0.4.1...v0.5.0) (2021-03-31)


### Features

* add `from_service_account_info` ([#45](https://www.github.com/googleapis/python-service-directory/issues/45)) ([db77e88](https://www.github.com/googleapis/python-service-directory/commit/db77e88a44ffdabd284d61775960079309071617))

### [0.4.1](https://www.github.com/googleapis/python-service-directory/compare/v0.4.0...v0.4.1) (2021-02-11)


### Bug Fixes

* remove gRPC send/recv limits ([#39](https://www.github.com/googleapis/python-service-directory/issues/39)) ([07908c0](https://www.github.com/googleapis/python-service-directory/commit/07908c009307485955886fc042c1c2b18b43adbd))

## [0.4.0](https://www.github.com/googleapis/python-service-directory/compare/v0.3.0...v0.4.0) (2020-12-03)


### Features

* add v1; add async client ([#30](https://www.github.com/googleapis/python-service-directory/issues/30)) ([7a771b1](https://www.github.com/googleapis/python-service-directory/commit/7a771b12d61e47e1cd341f3bd2d2fc8d221e07c0))

## [0.3.0](https://www.github.com/googleapis/python-service-directory/compare/v0.2.0...v0.3.0) (2020-06-11)


### Features

* add mTLS support, fix missing routing header issue  ([#15](https://www.github.com/googleapis/python-service-directory/issues/15)) ([b983735](https://www.github.com/googleapis/python-service-directory/commit/b98373544181ecc55104230fc1e53b206c2e23ac))

## [0.2.0](https://www.github.com/googleapis/python-service-directory/compare/v0.1.1...v0.2.0) (2020-05-19)


### Features

* add mTLS support (via synth) ([#4](https://www.github.com/googleapis/python-service-directory/issues/4)) ([25e0fcf](https://www.github.com/googleapis/python-service-directory/commit/25e0fcfb32d100be0cba3799d62543569dd2d2c6))


### Bug Fixes

* fix docs link ([#9](https://www.github.com/googleapis/python-service-directory/issues/9)) ([0f73da9](https://www.github.com/googleapis/python-service-directory/commit/0f73da9722e3e0c943b67063af4a7f9d0fc1f9e4))

### [0.1.1](https://www.github.com/googleapis/python-service-directory/compare/v0.1.0...v0.1.1) (2020-04-17)


### Bug Fixes

* fix link to client library documentation ([#3](https://www.github.com/googleapis/python-service-directory/issues/3)) ([8e9e602](https://www.github.com/googleapis/python-service-directory/commit/8e9e6020ffdeb2e012ef93fb466658da9fbac8df))

## 0.1.0 (2020-03-13)


### Features

* generate v1beta1 ([c2b8b99](https://www.github.com/googleapis/python-service-directory/commit/c2b8b99579a866ec7701e8ed95e6d05069593fb0))
