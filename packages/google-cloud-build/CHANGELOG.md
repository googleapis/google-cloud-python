# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-build/#history

### [3.8.1](https://github.com/googleapis/python-cloudbuild/compare/v3.8.0...v3.8.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#239](https://github.com/googleapis/python-cloudbuild/issues/239)) ([d2d9c83](https://github.com/googleapis/python-cloudbuild/commit/d2d9c83c76472afe992a4019306397f0584c3151))
* **deps:** require proto-plus>=1.15.0 ([d2d9c83](https://github.com/googleapis/python-cloudbuild/commit/d2d9c83c76472afe992a4019306397f0584c3151))

## [3.8.0](https://github.com/googleapis/python-cloudbuild/compare/v3.7.1...v3.8.0) (2022-02-14)


### Features

* add api key support ([#222](https://github.com/googleapis/python-cloudbuild/issues/222)) ([9c62e7e](https://github.com/googleapis/python-cloudbuild/commit/9c62e7e60b57ac213e98d6df05f9d9a748134f57))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([2af2b18](https://github.com/googleapis/python-cloudbuild/commit/2af2b18e87de591b72ee9279a8a3cd54171cb725))

### [3.7.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.7.0...v3.7.1) (2021-11-05)


### Bug Fixes

* **deps:** require google-api-core >= 1.28.0, drop packaging dep ([f3fb436](https://www.github.com/googleapis/python-cloudbuild/commit/f3fb4367ba598506d4cdd296870b61a8ffad75ef))


### Documentation

* list oneofs in docstring ([f3fb436](https://www.github.com/googleapis/python-cloudbuild/commit/f3fb4367ba598506d4cdd296870b61a8ffad75ef))

## [3.7.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.6.0...v3.7.0) (2021-10-13)


### Features

* add support for python 3.10 ([#189](https://www.github.com/googleapis/python-cloudbuild/issues/189)) ([0f2e580](https://www.github.com/googleapis/python-cloudbuild/commit/0f2e58035a046dd4a50fcc45ce20b36c05bb5724))

## [3.6.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.5.2...v3.6.0) (2021-10-11)


### Features

* add context manager support in client ([#184](https://www.github.com/googleapis/python-cloudbuild/issues/184)) ([7ac092c](https://www.github.com/googleapis/python-cloudbuild/commit/7ac092ce44f5884bdf2990a7dbd61dd72e1991d3))

### [3.5.2](https://www.github.com/googleapis/python-cloudbuild/compare/v3.5.1...v3.5.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([f56eed5](https://www.github.com/googleapis/python-cloudbuild/commit/f56eed5376f66a9ce5f9c1ca21f2b5b9b6d5779b))

### [3.5.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.5.0...v3.5.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([925a436](https://www.github.com/googleapis/python-cloudbuild/commit/925a436ebc38266e04ad694243b60dbf0af9ad2a))

## [3.5.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.4.0...v3.5.0) (2021-08-27)


### Features

* add script field to BuildStep message ([#154](https://www.github.com/googleapis/python-cloudbuild/issues/154)) ([8336413](https://www.github.com/googleapis/python-cloudbuild/commit/83364130c4e216724094c88bf57fe6ecf3d1e50d))
* Update cloudbuild proto with the service_account for BYOSA Triggers. ([#155](https://www.github.com/googleapis/python-cloudbuild/issues/155)) ([e18dbee](https://www.github.com/googleapis/python-cloudbuild/commit/e18dbeedda72f2e2bac5138e0068c80cb5eba5d1))

## [3.4.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.3.2...v3.4.0) (2021-08-20)


### Features

* Add ability to configure BuildTriggers to create Builds that require approval before executing and ApproveBuild API to approve or reject pending Builds ([#147](https://www.github.com/googleapis/python-cloudbuild/issues/147)) ([0ba4e0d](https://www.github.com/googleapis/python-cloudbuild/commit/0ba4e0d5f44897abf70427d54d152fe265698d91))

### [3.3.2](https://www.github.com/googleapis/python-cloudbuild/compare/v3.3.1...v3.3.2) (2021-07-28)


### Documentation

* Add a new build phase `SETUPBUILD` for timing information ([#142](https://www.github.com/googleapis/python-cloudbuild/issues/142)) ([eb23c8d](https://www.github.com/googleapis/python-cloudbuild/commit/eb23c8dbc35dc45b228a1536f8143b8a291bcd87))

### [3.3.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.3.0...v3.3.1) (2021-07-24)


### Features

* add a WorkerPools API ([#129](https://www.github.com/googleapis/python-cloudbuild/issues/129)) ([2ea98bd](https://www.github.com/googleapis/python-cloudbuild/commit/2ea98bddbfafd5e728b99f8bcae6b7dc2a741e60))
* add Samples section to CONTRIBUTING.rst ([#131](https://www.github.com/googleapis/python-cloudbuild/issues/131)) ([7593c96](https://www.github.com/googleapis/python-cloudbuild/commit/7593c96f3b3276c3b5432bbe1fbbf6c3bb3a358a))
* Implementation of Build Failure Info: - Added message FailureInfo field ([#132](https://www.github.com/googleapis/python-cloudbuild/issues/132)) ([76564e8](https://www.github.com/googleapis/python-cloudbuild/commit/76564e85da5e3a1e66d64720cf47ce5e80b1fc22))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#130](https://www.github.com/googleapis/python-cloudbuild/issues/130)) ([e92b7a2](https://www.github.com/googleapis/python-cloudbuild/commit/e92b7a21ce2115461ff7884885a88118731d56ef))
* enable self signed jwt for grpc ([#139](https://www.github.com/googleapis/python-cloudbuild/issues/139)) ([89f7931](https://www.github.com/googleapis/python-cloudbuild/commit/89f7931e9f33d823e31a0e997dfc22d728f55008))


### Miscellaneous Chores

* release as 3.3.1 ([#136](https://www.github.com/googleapis/python-cloudbuild/issues/136)) ([5d6e342](https://www.github.com/googleapis/python-cloudbuild/commit/5d6e342a6c6c3d163b61f6ffa05a551519c1f461))

## [3.3.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.2.1...v3.3.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#118](https://www.github.com/googleapis/python-cloudbuild/issues/118)) ([6414a3b](https://www.github.com/googleapis/python-cloudbuild/commit/6414a3bcc27baa4e60b2bf7cf2f7d9f776ad6843))


### Bug Fixes

* disable always_use_jwt_access ([#123](https://www.github.com/googleapis/python-cloudbuild/issues/123)) ([c1c9608](https://www.github.com/googleapis/python-cloudbuild/commit/c1c960894dc401b0a125801b08ef1a4fee659abe))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-cloudbuild/issues/1127)) ([#112](https://www.github.com/googleapis/python-cloudbuild/issues/112)) ([e2420f8](https://www.github.com/googleapis/python-cloudbuild/commit/e2420f8ad5630aedff0d52e3cc4facbb11300b72)), closes [#1126](https://www.github.com/googleapis/python-cloudbuild/issues/1126)

### [3.2.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.2.0...v3.2.1) (2021-05-16)


### Bug Fixes

* **deps:** add packaging requirement ([#101](https://www.github.com/googleapis/python-cloudbuild/issues/101)) ([9563889](https://www.github.com/googleapis/python-cloudbuild/commit/956388912b5aab80375c1a2439d934f211627e3a))

## [3.2.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.1.1...v3.2.0) (2021-04-01)


### Features

* Add `COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY` for corresponding comment control behavior with triggered builds. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))
* Add `E2_HIGHCPU_8` and `E2_HIGHCPU_32` machine types. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))
* Add `ReceiveTriggerWebhook` for webhooks activating specific triggers. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))
* Add `SecretManager`-related resources and messages for corresponding integration. ([#73](https://www.github.com/googleapis/python-cloudbuild/issues/73)) ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))


### Bug Fixes

* Specify `build` as the body of a `CreateBuild` call. The Cloud Build API has always assumed this, but now we are actually specifying it. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))


### Documentation

* Add `$PROJECT_NUMBER` as a substitution variable. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))
* Clarify lifetime/expiration behavior around `ListBuilds` page tokens. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))
* Update field docs on required-ness behavior and fix typos. ([df8ddd0](https://www.github.com/googleapis/python-cloudbuild/commit/df8ddd0e691101077784a5272fd27b9d7bd86938))

### [3.1.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.1.0...v3.1.1) (2021-03-26)


### Documentation

* Adding samples ([#69](https://www.github.com/googleapis/python-cloudbuild/issues/69)) ([9f35e43](https://www.github.com/googleapis/python-cloudbuild/commit/9f35e432271bfccc2bbd4a1e025efaa5b04a9f68))

## [3.1.0](https://www.github.com/googleapis/python-cloudbuild/compare/v3.0.2...v3.1.0) (2021-03-23)


### Features

* add `from_service_account_info` ([#52](https://www.github.com/googleapis/python-cloudbuild/issues/52)) ([580a959](https://www.github.com/googleapis/python-cloudbuild/commit/580a95925651c8478a47fd588540088104bb9a12))

### [3.0.2](https://www.github.com/googleapis/python-cloudbuild/compare/v3.0.1...v3.0.2) (2021-02-19)


### Documentation

* update python contributing guide ([#63](https://www.github.com/googleapis/python-cloudbuild/issues/63)) ([f199171](https://www.github.com/googleapis/python-cloudbuild/commit/f199171267bcec8cbddf5aa5be420647370dadee))

### [3.0.1](https://www.github.com/googleapis/python-cloudbuild/compare/v3.0.0...v3.0.1) (2021-02-08)


### Bug Fixes

* remove client recv msg limit  ([a1727c3](https://www.github.com/googleapis/python-cloudbuild/commit/a1727c393b14a919884b52aa1ba1f3f332a4b204))

## [3.0.0](https://www.github.com/googleapis/python-cloudbuild/compare/v2.0.0...v3.0.0) (2020-11-04)


### ⚠ BREAKING CHANGES

* rename fields that conflict with builtins ([#29](https://www.github.com/googleapis/python-cloudbuild/issues/29)) ([3b27cc3](https://www.github.com/googleapis/python-cloudbuild/commit/3b27cc311d697d881e26c1f1196f0a1fdeb4bb21))
  * `StorageSource.object` -> `StorageSource.object_`
  * `RepoSource.dir` -> `RepoSource.dir_`
  * `BuildStep.dir` -> `BuildStep.dir_`
  * `Hash.type` -> `Hash.type_`

### Features

* add new build message fields ([#29](https://www.github.com/googleapis/python-cloudbuild/issues/29)) ([3b27cc3](https://www.github.com/googleapis/python-cloudbuild/commit/3b27cc311d697d881e26c1f1196f0a1fdeb4bb21))
  * `service_account`, which is available to members of our closed alpha
  * `STACKDRIVER_ONLY` and `CLOUD_LOGGING_ONLY` logging modes
  * `dynamic_substitutions` option

## [2.0.0](https://www.github.com/googleapis/python-cloudbuild/compare/v1.1.0...v2.0.0) (2020-07-23)


### ⚠ BREAKING CHANGES

* migrate to use microgenerator (#23)

### Features

* migrate to use microgenerator ([#23](https://www.github.com/googleapis/python-cloudbuild/issues/23)) ([f52a799](https://www.github.com/googleapis/python-cloudbuild/commit/f52a79930e621c46dea574917549f9ed37771149))

## [1.1.0](https://www.github.com/googleapis/python-cloudbuild/compare/v1.0.0...v1.1.0) (2020-06-30)


### Features

* add time-to-live in a queue for builds ([#19](https://www.github.com/googleapis/python-cloudbuild/issues/19)) ([d30aba7](https://www.github.com/googleapis/python-cloudbuild/commit/d30aba73e7026089d4e3f9b51ce71d262698d510))

## [1.0.0](https://www.github.com/googleapis/python-cloudbuild/compare/v0.1.0...v1.0.0) (2020-02-28)


### Features

* bump library release level to GA ([#8](https://www.github.com/googleapis/python-cloudbuild/issues/8)) ([f6e5c3b](https://www.github.com/googleapis/python-cloudbuild/commit/f6e5c3bccb86b3900fde848404f64b1d38eca99d))

## 0.1.0

11-07-2019 10:48 PST

**Note**:  This library is incompatible with `google-cloud-containeranalysis<0.3.1`. Please upgrade to `google-cloud-containeranalysis>=0.3.1` to use this library.

### New Features
- Initial generation of Cloud Build v1 ([#9510](https://github.com/googleapis/google-cloud-python/pull/9510)).
