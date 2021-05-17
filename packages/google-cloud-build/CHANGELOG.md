# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-build/#history

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
