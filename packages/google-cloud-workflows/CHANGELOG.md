# Changelog

## [1.7.0](https://github.com/googleapis/python-workflows/compare/v1.6.3...v1.7.0) (2022-07-06)


### Features

* add audience parameter ([c4a8a8d](https://github.com/googleapis/python-workflows/commit/c4a8a8d5109b91a2a0af176044ab79b20f2bcf60))


### Bug Fixes

* **deps:** require google-api-core >= 2.8.0 ([c4a8a8d](https://github.com/googleapis/python-workflows/commit/c4a8a8d5109b91a2a0af176044ab79b20f2bcf60))
* require python >= 3.7 ([#195](https://github.com/googleapis/python-workflows/issues/195)) ([6315169](https://github.com/googleapis/python-workflows/commit/6315169c0696cc8807c13c89c992d60ad8970f2e))

## [1.6.3](https://github.com/googleapis/python-workflows/compare/v1.6.2...v1.6.3) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf>=3.19.0, <4.0.0dev ([#183](https://github.com/googleapis/python-workflows/issues/183)) ([d58f508](https://github.com/googleapis/python-workflows/commit/d58f508d0efc171ccb0dc6354360e6ac8f234c87))


### Documentation

* fix changelog header to consistent size ([#184](https://github.com/googleapis/python-workflows/issues/184)) ([0578027](https://github.com/googleapis/python-workflows/commit/0578027fc1d034f2706987324eb9cd9988b3b8b1))

## [1.6.2](https://github.com/googleapis/python-workflows/compare/v1.6.1...v1.6.2) (2022-05-05)


### Documentation

* fix type in docstring for map fields ([f3ec9da](https://github.com/googleapis/python-workflows/commit/f3ec9dadea8a3574a5413c635288242014b1a5ae))

## [1.6.1](https://github.com/googleapis/python-workflows/compare/v1.6.0...v1.6.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >2.3.0 ([#142](https://github.com/googleapis/python-workflows/issues/142)) ([0a0280a](https://github.com/googleapis/python-workflows/commit/0a0280aa9fa93faadb1e69a0808c680f40972d24))
* **deps:** require proto-plus>=1.15.0 ([0a0280a](https://github.com/googleapis/python-workflows/commit/0a0280aa9fa93faadb1e69a0808c680f40972d24))

## [1.6.0](https://github.com/googleapis/python-workflows/compare/v1.5.0...v1.6.0) (2022-02-15)


### Features

* add api key support ([#127](https://github.com/googleapis/python-workflows/issues/127)) ([9db415f](https://github.com/googleapis/python-workflows/commit/9db415fdcc3ac7372e07b060a06751d0c8804ba8))


### Bug Fixes

* **deps:** remove unused dependency libcst ([#133](https://github.com/googleapis/python-workflows/issues/133)) ([bfadb79](https://github.com/googleapis/python-workflows/commit/bfadb7946d7960996a7d371c5b60b47057009eb5))
* resolve DuplicateCredentialArgs error when using credentials_file ([57614ee](https://github.com/googleapis/python-workflows/commit/57614eeac59b09bcbbb8bdf50369934c73802ae3))

## [1.5.0](https://www.github.com/googleapis/python-workflows/compare/v1.4.1...v1.5.0) (2021-11-05)


### Features

* add a stack_trace field to the Error messages specifying where the error occurred ([#113](https://www.github.com/googleapis/python-workflows/issues/113)) ([22f55d3](https://www.github.com/googleapis/python-workflows/commit/22f55d30c57d31bf8d0839bd7289e1392ff65a18))
* add call_log_level field to Execution messages ([22f55d3](https://www.github.com/googleapis/python-workflows/commit/22f55d30c57d31bf8d0839bd7289e1392ff65a18))

## [1.4.1](https://www.github.com/googleapis/python-workflows/compare/v1.4.0...v1.4.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([a294177](https://www.github.com/googleapis/python-workflows/commit/a294177e4d23f35e60fdcaa2023efea9bce366a4))
* **deps:** require google-api-core >= 1.28.0 ([a294177](https://www.github.com/googleapis/python-workflows/commit/a294177e4d23f35e60fdcaa2023efea9bce366a4))


### Documentation

* list oneofs in docstring ([a294177](https://www.github.com/googleapis/python-workflows/commit/a294177e4d23f35e60fdcaa2023efea9bce366a4))

## [1.4.0](https://www.github.com/googleapis/python-workflows/compare/v1.3.0...v1.4.0) (2021-10-19)


### Features

* add support for python 3.10 ([#106](https://www.github.com/googleapis/python-workflows/issues/106)) ([7eac117](https://www.github.com/googleapis/python-workflows/commit/7eac117640b08704291d561370630aad388efb0c))

## [1.3.0](https://www.github.com/googleapis/python-workflows/compare/v1.2.3...v1.3.0) (2021-10-08)


### Features

* add context manager support in client ([#102](https://www.github.com/googleapis/python-workflows/issues/102)) ([090c723](https://www.github.com/googleapis/python-workflows/commit/090c723e249c62fa29a519fd1aebdf205d12b03e))

## [1.2.3](https://www.github.com/googleapis/python-workflows/compare/v1.2.2...v1.2.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([f33a1b9](https://www.github.com/googleapis/python-workflows/commit/f33a1b902c6d66222b2bd217f81f42188de24e65))

## [1.2.2](https://www.github.com/googleapis/python-workflows/compare/v1.2.1...v1.2.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([8e778a3](https://www.github.com/googleapis/python-workflows/commit/8e778a39b1a655867d129df4dbd573ac4763cd19))

## [1.2.1](https://www.github.com/googleapis/python-workflows/compare/v1.2.0...v1.2.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#75](https://www.github.com/googleapis/python-workflows/issues/75)) ([cd2684f](https://www.github.com/googleapis/python-workflows/commit/cd2684fd73e7bf68ce413370aec5819a9c5e35a1))
* enable self signed jwt for grpc ([#81](https://www.github.com/googleapis/python-workflows/issues/81)) ([5abf2bc](https://www.github.com/googleapis/python-workflows/commit/5abf2bca6fff87008386e1505aba86765c318fec))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#76](https://www.github.com/googleapis/python-workflows/issues/76)) ([8eb851b](https://www.github.com/googleapis/python-workflows/commit/8eb851b40624f56fc805fec00b0731c60ec3b568))


### Miscellaneous Chores

* release as 1.2.1 ([#80](https://www.github.com/googleapis/python-workflows/issues/80)) ([b3ece19](https://www.github.com/googleapis/python-workflows/commit/b3ece19a7b671846ef49ade9a54d1b01f8ff2b69))

## [1.2.0](https://www.github.com/googleapis/python-workflows/compare/v1.1.0...v1.2.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#68](https://www.github.com/googleapis/python-workflows/issues/68)) ([a88f246](https://www.github.com/googleapis/python-workflows/commit/a88f2466a906fdec0ebf4d772967cdf334b8ac91))


### Bug Fixes

* disable always_use_jwt_access ([#72](https://www.github.com/googleapis/python-workflows/issues/72)) ([2085463](https://www.github.com/googleapis/python-workflows/commit/20854636d22eefd738872ef4fa8b280a2f6989ec))
* exclude docs and tests from package ([#63](https://www.github.com/googleapis/python-workflows/issues/63)) ([ff68d16](https://www.github.com/googleapis/python-workflows/commit/ff68d16bb68960dbee188771f6f334ab69a98b23))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-workflows/issues/1127)) ([#65](https://www.github.com/googleapis/python-workflows/issues/65)) ([10341d6](https://www.github.com/googleapis/python-workflows/commit/10341d6b7adf284507d5f99dc68bae34e4360be9))

## [1.1.0](https://www.github.com/googleapis/python-workflows/compare/v1.0.0...v1.1.0) (2021-06-16)


### Features

* support self-signed JWT flow for service accounts ([1165c47](https://www.github.com/googleapis/python-workflows/commit/1165c47754c62c4538e254c59909aaa50190dbde))


### Bug Fixes

* add async client to %name_%version/init.py ([1165c47](https://www.github.com/googleapis/python-workflows/commit/1165c47754c62c4538e254c59909aaa50190dbde))

## [1.0.0](https://www.github.com/googleapis/python-workflows/compare/v0.3.0...v1.0.0) (2021-06-02)


### Features

* bump release level to production/stable ([#54](https://www.github.com/googleapis/python-workflows/issues/54)) ([3cd61a5](https://www.github.com/googleapis/python-workflows/commit/3cd61a5670707e56a67749a31805e091e0ab87b2))

## [0.3.0](https://www.github.com/googleapis/python-workflows/compare/v0.2.0...v0.3.0) (2021-04-30)


### Features

* add v1 ([#36](https://www.github.com/googleapis/python-workflows/issues/36)) ([a843aae](https://www.github.com/googleapis/python-workflows/commit/a843aaed7e295f951650b81ce3da5cbece4ebab7))

## [0.2.0](https://www.github.com/googleapis/python-workflows/compare/v0.1.0...v0.2.0) (2021-01-21)


### Features

* add 'from_service_account_info' factory to clients ([887df00](https://www.github.com/googleapis/python-workflows/commit/887df0046f4350cb515036fba4df608d8adec687))
* add common resource path helpers; expose client transport; remove gRPC send/recv limit ([#12](https://www.github.com/googleapis/python-workflows/issues/12)) ([672d821](https://www.github.com/googleapis/python-workflows/commit/672d8218d27238bfbe7443355accebde6e9ae6da))


### Bug Fixes

* fix sphinx identifiers ([887df00](https://www.github.com/googleapis/python-workflows/commit/887df0046f4350cb515036fba4df608d8adec687))


### Documentation

* fix type annotations ([#4](https://www.github.com/googleapis/python-workflows/issues/4)) ([60d3930](https://www.github.com/googleapis/python-workflows/commit/60d393078c39eec8756c65338860e46aa641d31d))
* remove note on editable installs ([#5](https://www.github.com/googleapis/python-workflows/issues/5)) ([4dddd59](https://www.github.com/googleapis/python-workflows/commit/4dddd59e87b788c3feb6a8cc3441a0105f5d5aad))

## 0.1.0 (2020-09-24)


### Features

* add workflows v1beta ([8ec2882](https://www.github.com/googleapis/python-workflows/commit/8ec28824c2b3d7ff7dab1b14c22cca0ab7da0370))
