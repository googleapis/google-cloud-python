# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-core/#history

## [2.2.0](https://www.github.com/googleapis/python-cloud-core/compare/v2.1.0...v2.2.0) (2021-11-09)


### Features

* add mypy checking + 'py.typed' files ([#149](https://www.github.com/googleapis/python-cloud-core/issues/149)) ([f20ef60](https://www.github.com/googleapis/python-cloud-core/commit/f20ef60abaff13520d2e7b9719741746bd0d1c7b))
## [2.1.0](https://www.github.com/googleapis/python-cloud-core/compare/v2.0.0...v2.1.0) (2021-10-05)


### Features

* add support for Python 3.10 ([#145](https://www.github.com/googleapis/python-cloud-core/issues/145)) ([c9370b9](https://www.github.com/googleapis/python-cloud-core/commit/c9370b9598ae337abf1d9f9c02fdc5390ca83ff7))

## [2.0.0](https://www.github.com/googleapis/python-cloud-core/compare/v2.0.0-b1...v2.0.0) (2021-08-18)

### ⚠ BREAKING CHANGES

* drop python 2.7 support ([#103](https://www.github.com/googleapis/python-cloud-core/issues/103)) ([181d706](https://www.github.com/googleapis/python-cloud-core/commit/181d706e5b44d9d4189c21782551ce85c720d733)), closes [#102](https://www.github.com/googleapis/python-cloud-core/issues/102)


### Miscellaneous Chores

* trigger 2.0.0 release ([#128](https://www.github.com/googleapis/python-cloud-core/issues/128)) ([aead67a](https://www.github.com/googleapis/python-cloud-core/commit/aead67a1244306d518b8ab150e143e5a29e1ab6f))

## [2.0.0b1](https://www.github.com/googleapis/python-cloud-core/compare/v1.7.2...v2.0.0b1) (2021-08-02)


### ⚠ BREAKING CHANGES

* drop python 2.7 support ([#103](https://www.github.com/googleapis/python-cloud-core/issues/103)) ([181d706](https://www.github.com/googleapis/python-cloud-core/commit/181d706e5b44d9d4189c21782551ce85c720d733)), closes [#102](https://www.github.com/googleapis/python-cloud-core/issues/102)

### [1.7.2](https://www.github.com/googleapis/python-cloud-core/compare/v1.7.1...v1.7.2) (2021-07-27)


### Documentation

* add Samples section to CONTRIBUTING.rst ([#119](https://www.github.com/googleapis/python-cloud-core/issues/119)) ([5c3959b](https://www.github.com/googleapis/python-cloud-core/commit/5c3959b3870b8c6ccaf321cc030f4b0cba7ce2ba))

## [1.7.1](https://www.github.com/googleapis/python-cloud-core/compare/v1.7.0...v1.7.1) (2021-06-25)


### Bug Fixes

* pass kwargs through in 'from_service_account_json' ([#109](https://www.github.com/googleapis/python-cloud-core/issues/109)) ([efc4bbf](https://www.github.com/googleapis/python-cloud-core/commit/efc4bbfd377e64763c60500407f5c191c03ef85c))

## [1.7.0](https://www.github.com/googleapis/python-cloud-core/compare/v1.6.0...v1.7.0) (2021-06-14)


### Features

* add 'Client.close' ([#100](https://www.github.com/googleapis/python-cloud-core/issues/100)) ([7387fc8](https://www.github.com/googleapis/python-cloud-core/commit/7387fc87186defff74612cf85909c7d456155d47))
* add 'Client.from_service_account_info' factory ([#54](https://www.github.com/googleapis/python-cloud-core/issues/54)) ([7e59360](https://www.github.com/googleapis/python-cloud-core/commit/7e59360a43418947cbbb7608aa23ef5d566c964c))


### Documentation

* update python contributing guide ([#80](https://www.github.com/googleapis/python-cloud-core/issues/80)) ([58deef8](https://www.github.com/googleapis/python-cloud-core/commit/58deef8ce2e90415a4c38022e88fdfe25bc666b6))

## [1.6.0](https://www.github.com/googleapis/python-cloud-core/compare/v1.5.0...v1.6.0) (2021-02-02)


### Features

* add mtls support ([#75](https://www.github.com/googleapis/python-cloud-core/issues/75)) ([a93129b](https://www.github.com/googleapis/python-cloud-core/commit/a93129bf2fa6fabda3de8b8a342f31a328ccbaf0))
* infer project from explicit service account creds ([#51](https://www.github.com/googleapis/python-cloud-core/issues/51)) ([2bd41a1](https://www.github.com/googleapis/python-cloud-core/commit/2bd41a177864c7d577155ee3c7e4a1dfd24601dc)), closes [#27](https://www.github.com/googleapis/python-cloud-core/issues/27)


### Documentation

* **python:** document adding Python 3.9 support, dropping 3.5 support ([#65](https://www.github.com/googleapis/python-cloud-core/issues/65)) ([860f345](https://www.github.com/googleapis/python-cloud-core/commit/860f345d1f912ffb9a41003159f34ddbebfbd110)), closes [#787](https://www.github.com/googleapis/python-cloud-core/issues/787)

## [1.5.0](https://www.github.com/googleapis/python-cloud-core/compare/v1.4.4...v1.5.0) (2020-12-14)


### Features

* add support for Python 3.9, drop support for Python 3.5 ([#55](https://www.github.com/googleapis/python-cloud-core/issues/55)) ([ddf7ce5](https://www.github.com/googleapis/python-cloud-core/commit/ddf7ce5cc1be78e580d6450043bace71e789e933))

### [1.4.4](https://www.github.com/googleapis/python-cloud-core/compare/v1.4.3...v1.4.4) (2020-11-30)


### Dependencies

* require `six>=1.12.0` and `google-api-core>=1.21.0` ([#46](https://www.github.com/googleapis/python-cloud-core/issues/46)) ([a97b9ca](https://www.github.com/googleapis/python-cloud-core/commit/a97b9cae6d3b8f0c723dfa825f1b76efc2318f80))

### [1.4.3](https://www.github.com/googleapis/python-cloud-core/compare/v1.4.2...v1.4.3) (2020-10-06)


### Bug Fixes

* avoid using 'pkg_resources' to determine version ([#40](https://www.github.com/googleapis/python-cloud-core/issues/40)) ([568578d](https://www.github.com/googleapis/python-cloud-core/commit/568578d33f71117564ee9212daad72d4e2b739a6)), closes [#39](https://www.github.com/googleapis/python-cloud-core/issues/39)

### [1.4.2](https://www.github.com/googleapis/python-cloud-core/compare/v1.4.1...v1.4.2) (2020-09-29)


### Bug Fixes

* handle query_params tuples in JSONConnection.build_api_url ([#34](https://www.github.com/googleapis/python-cloud-core/issues/34)) ([6a9adb3](https://www.github.com/googleapis/python-cloud-core/commit/6a9adb3dddd5f6d82032aba5efd673ea0641593c))


### Performance Improvements

* use prettyPrint=false by default ([#28](https://www.github.com/googleapis/python-cloud-core/issues/28)) ([c407b5d](https://www.github.com/googleapis/python-cloud-core/commit/c407b5d617c04affbdb4f444c188edffb25d4336))

### [1.4.1](https://www.github.com/googleapis/python-cloud-core/compare/v1.4.0...v1.4.1) (2020-08-06)


### Bug Fixes

* **deps:** fix missing scopes attribute in client_options ([#24](https://www.github.com/googleapis/python-cloud-core/issues/24)) ([a0e7730](https://www.github.com/googleapis/python-cloud-core/commit/a0e773057a59b573a760d38710c52a8747fceb1f)), closes [/github.com/googleapis/python-cloud-core/issues/23#issuecomment-669504557](https://www.github.com/googleapis//github.com/googleapis/python-cloud-core/issues/23/issues/issuecomment-669504557)


### Documentation

* update docs build (via synth) ([#14](https://www.github.com/googleapis/python-cloud-core/issues/14)) ([f1a95ce](https://www.github.com/googleapis/python-cloud-core/commit/f1a95ce89c25f5297470299ca1ef7e1e05a9e99f))


## 1.4.2rc2

09-24-2020 09:29 PDT

### Implementation Changes

- fix: handle query_params tuples in JSONConnection.build_api_url ([#34](https://github.com/googleapis/python-cloud-core/pull/34))

### Internal / Testing Changes

- chore: add default CODEOWNERS ([#33](https://github.com/googleapis/python-cloud-core/pull/33))


## 1.4.2rc1

09-21-2020 14:45 PDT


### Implementation Changes

- perf: use prettyPrint=false by default ([#28](https://github.com/googleapis/python-cloud-core/pull/28))

### Internal / Testing Changes

- test: fix mock credentials to allow for quota projects ([#29](https://github.com/googleapis/python-cloud-core/pull/29))

## [1.4.0](https://www.github.com/googleapis/python-cloud-core/compare/v1.3.0...v1.4.0) (2020-08-04)


### Features

* add quota_project, credentials file, and scopes options ([#15](https://www.github.com/googleapis/python-cloud-core/issues/15)) ([a1e11e1](https://www.github.com/googleapis/python-cloud-core/commit/a1e11e1f81a2a7e17b87fe4321eb497f7f3ccdc5))
* add support for Python 3.8 ([#17](https://www.github.com/googleapis/python-cloud-core/issues/17)) ([f727aba](https://www.github.com/googleapis/python-cloud-core/commit/f727aba432d4726cce72da5f74e8be6adb945a80)), closes [#16](https://www.github.com/googleapis/python-cloud-core/issues/16)

## 1.3.0

01-31-2020 13:30 PST

### New Features
- Change default api_request() timeout to non-None ([#10219](https://github.com/googleapis/google-cloud-python/pull/10219))

## 1.2.0

01-14-2020 13:22 PST

### Dependencies

- chores(core): bump api-core dependency to 1.16.0 ([#10111](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/10111))

## 1.1.0

12-04-2019 13:56 PST


### New Features

- Add timeout param to `JSONConnection.api_request()`. ([#9915](https://github.com/googleapis/google-cloud-python/pull/9915))


### Documentation

- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Fix Google Auth Credentials help link now. ([#9260](https://github.com/googleapis/google-cloud-python/pull/9260))
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.0.3

07-26-2019 10:34 PDT


### Implementation Changes
- Make `Client.build_api_url` an instance method. ([#8747](https://github.com/googleapis/google-cloud-python/pull/8747))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Linkify the PR in the change log. ([#8790](https://github.com/googleapis/google-cloud-python/pull/8790))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Removing typing information for `**kwargs` in order to not conflict with type checkers. ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))

### Internal / Testing Changes
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 1.0.2

06/11/2019 15:19 PDT

### Internal Changes
- Prevent requests from hanging on SSL handshake issue by adding a max timeout of 5 minutes. ([#8207](https://github.com/googleapis/google-cloud-python/pull/8207))

## 1.0.1

05-28-2019 11:22 PDT

### Dependencies
- Pin `grpcio < 2.0dev`. ([#8182](https://github.com/googleapis/google-cloud-python/pull/8182))

## 1.0.0

05-15-2019 13:09 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Refactor `client_info` support. ([#7849](https://github.com/googleapis/google-cloud-python/pull/7849))

### Dependencies
- Update dep on `api_core` >= 1.11.0. ([#7986](https://github.com/googleapis/google-cloud-python/pull/7986))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 0.29.1

12-17-2018 16:35 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 0.29.0

12-03-2018 15:54 PST

### Breaking Changes
- Remove iam module from core. This module is now available as part of google-api-core. ([#6775](https://github.com/googleapis/google-cloud-python/pull/6775))

### Implementation Changes
- Fix `_time_from_iso8601_time_naive` for values with micros. ([#5756](https://github.com/googleapis/google-cloud-python/pull/5756))
- Import stdlib ABCs from `collections.abc` rather than `collections`. ([#6451](https://github.com/googleapis/google-cloud-python/pull/6451))

### Dependencies
- Bump minimum `api_core` version to 1.0.0. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Internal / Testing Changes
- Blacken api_core and core. ([#6668](https://github.com/googleapis/google-cloud-python/pull/6668))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox. ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Use inplace installs for nox ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Fix bad trove classifier.
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))

## 0.28.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- Requiring 'grpcio >= 1.8.2'. (#4642)

### Documentation

- DefaultCredentialsError could be raised if credentials not supplied (#4688)
- Unreachable links in the readme files have been fixed. (#4406)
- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Notable Implementation Changes

- A large portion of the implementation has moved into
  [`google-api-core`][2] (#4022, #4041, #4057, #4067,
  #4069, #4079, #4081, #4166, #4221)

### Dependencies

- Explicit depending on `google-api-core` and upgrading to
  `grpcio >= 1.7.0` (see #4096, #4280 and
  https://github.com/grpc/grpc/issues/12455)

### Interface changes / additions

- Rename `google.cloud.obselete` module to
  `obsolete` (#3913, h/t to @dimaqq)

PyPI: https://pypi.org/project/google-cloud-core/0.28.0/

[2]: https://pypi.org/project/google-api-core/
