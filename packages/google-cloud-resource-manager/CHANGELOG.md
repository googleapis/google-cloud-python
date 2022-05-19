# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-resource-manager/#history

## [1.5.0](https://github.com/googleapis/python-resource-manager/compare/v1.4.1...v1.5.0) (2022-05-05)


### Features

* AuditConfig for IAM v1 ([8f4c7ff](https://github.com/googleapis/python-resource-manager/commit/8f4c7ffdb19ab14c47b8bdf3b421c1a7efdbbc36))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([8f4c7ff](https://github.com/googleapis/python-resource-manager/commit/8f4c7ffdb19ab14c47b8bdf3b421c1a7efdbbc36))
* don't package tests ([#193](https://github.com/googleapis/python-resource-manager/issues/193)) ([be8ecab](https://github.com/googleapis/python-resource-manager/commit/be8ecab98554b00567659b94adb912336f6cc943))


### Documentation

* fix type in docstring for map fields ([8f4c7ff](https://github.com/googleapis/python-resource-manager/commit/8f4c7ffdb19ab14c47b8bdf3b421c1a7efdbbc36))

### [1.4.1](https://github.com/googleapis/python-resource-manager/compare/v1.4.0...v1.4.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#168](https://github.com/googleapis/python-resource-manager/issues/168)) ([36d05bb](https://github.com/googleapis/python-resource-manager/commit/36d05bbb9646dbcc389976fc7eea6174f572e518))

## [1.4.0](https://github.com/googleapis/python-resource-manager/compare/v1.3.3...v1.4.0) (2022-02-26)


### Features

* add api key support ([#154](https://github.com/googleapis/python-resource-manager/issues/154)) ([6d8c5bd](https://github.com/googleapis/python-resource-manager/commit/6d8c5bd867af5cfd6939373388769b57203a1138))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([e335369](https://github.com/googleapis/python-resource-manager/commit/e3353691b9c066a52b451c97438b389589760724))

### [1.3.3](https://www.github.com/googleapis/python-resource-manager/compare/v1.3.2...v1.3.3) (2021-11-13)


### Documentation

* fix docstring formatting ([#140](https://www.github.com/googleapis/python-resource-manager/issues/140)) ([57bf037](https://www.github.com/googleapis/python-resource-manager/commit/57bf037175f6015b24d9b45ffb74e13dc0d37872))

### [1.3.2](https://www.github.com/googleapis/python-resource-manager/compare/v1.3.1...v1.3.2) (2021-11-05)


### Documentation

* fix docstring formatting ([#135](https://www.github.com/googleapis/python-resource-manager/issues/135)) ([c703958](https://www.github.com/googleapis/python-resource-manager/commit/c7039587d072cea4a655b20b882c6ed5934d9ec6))

### [1.3.1](https://www.github.com/googleapis/python-resource-manager/compare/v1.3.0...v1.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([a6a9231](https://www.github.com/googleapis/python-resource-manager/commit/a6a9231410e73d89b98f3a031bb465a2cc3a672b))
* **deps:** require google-api-core >= 1.28.0 ([a6a9231](https://www.github.com/googleapis/python-resource-manager/commit/a6a9231410e73d89b98f3a031bb465a2cc3a672b))


### Documentation

* list oneofs in docstring ([a6a9231](https://www.github.com/googleapis/python-resource-manager/commit/a6a9231410e73d89b98f3a031bb465a2cc3a672b))

## [1.3.0](https://www.github.com/googleapis/python-resource-manager/compare/v1.2.0...v1.3.0) (2021-10-14)


### Features

* add support for python 3.10 ([#125](https://www.github.com/googleapis/python-resource-manager/issues/125)) ([061edf3](https://www.github.com/googleapis/python-resource-manager/commit/061edf3af5eff2d68e29ed5a898a6a28ce8edf04))

## [1.2.0](https://www.github.com/googleapis/python-resource-manager/compare/v1.1.2...v1.2.0) (2021-10-07)


### Features

* add context manager support in client ([#120](https://www.github.com/googleapis/python-resource-manager/issues/120)) ([49df2ea](https://www.github.com/googleapis/python-resource-manager/commit/49df2eaef49e1f844a65f2b499a172e1e4b37b61))

## [1.2.0](https://www.github.com/googleapis/python-resource-manager/compare/v1.1.2...v1.2.0) (2021-10-07)


### Features

* add context manager support in client ([#120](https://www.github.com/googleapis/python-resource-manager/issues/120)) ([49df2ea](https://www.github.com/googleapis/python-resource-manager/commit/49df2eaef49e1f844a65f2b499a172e1e4b37b61))

### [1.1.2](https://www.github.com/googleapis/python-resource-manager/compare/v1.1.1...v1.1.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([e48478b](https://www.github.com/googleapis/python-resource-manager/commit/e48478b64d66a54b4ff283a071b6492cb2961330))

### [1.1.1](https://www.github.com/googleapis/python-resource-manager/compare/v1.1.0...v1.1.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([e322b1e](https://www.github.com/googleapis/python-resource-manager/commit/e322b1e183bb7edf5a24a60e36e177a63f54ce86))

## [1.1.0](https://www.github.com/googleapis/python-resource-manager/compare/v1.0.2...v1.1.0) (2021-08-19)


### Features

* bump release level to production/stable ([#96](https://www.github.com/googleapis/python-resource-manager/issues/96)) ([aac0a24](https://www.github.com/googleapis/python-resource-manager/commit/aac0a240843846ccb228c8d4223cfd2dbdf03f7d))

### [1.0.2](https://www.github.com/googleapis/python-resource-manager/compare/v1.0.1...v1.0.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#92](https://www.github.com/googleapis/python-resource-manager/issues/92)) ([9df35b3](https://www.github.com/googleapis/python-resource-manager/commit/9df35b32a75fe4c6c5e427b42d49222303f8ee5f))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#85](https://www.github.com/googleapis/python-resource-manager/issues/85)) ([d0f63b8](https://www.github.com/googleapis/python-resource-manager/commit/d0f63b8201cbd19938cb021e9457c421b19e9c78))


### Miscellaneous Chores

* release as 1.0.2 ([#93](https://www.github.com/googleapis/python-resource-manager/issues/93)) ([4135c6c](https://www.github.com/googleapis/python-resource-manager/commit/4135c6c7a97c4bf6edab632509618330c00230d6))

### [1.0.1](https://www.github.com/googleapis/python-resource-manager/compare/v1.0.0...v1.0.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#84](https://www.github.com/googleapis/python-resource-manager/issues/84)) ([92c3ec8](https://www.github.com/googleapis/python-resource-manager/commit/92c3ec8ef175430daf18657a212638c56a382c2b))

## [1.0.0](https://www.github.com/googleapis/python-resource-manager/compare/v0.30.3...v1.0.0) (2021-07-18)


### Features

* add always_use_jwt_access ([#73](https://www.github.com/googleapis/python-resource-manager/issues/73)) ([9c0bc88](https://www.github.com/googleapis/python-resource-manager/commit/9c0bc888c685f2dbcbc66ca73e7fd4f27d5be47e))
* add v3 ([#62](https://www.github.com/googleapis/python-resource-manager/issues/62)) ([72f69f0](https://www.github.com/googleapis/python-resource-manager/commit/72f69f0f3a2205ef3bb49ca3e3ae670fd103f6cb))


### Bug Fixes

* disable always_use_jwt_access ([#76](https://www.github.com/googleapis/python-resource-manager/issues/76)) ([9f36514](https://www.github.com/googleapis/python-resource-manager/commit/9f365141716b2acc90bb16132dba48b38e470a9b))
* remove v1beta1 ([72f69f0](https://www.github.com/googleapis/python-resource-manager/commit/72f69f0f3a2205ef3bb49ca3e3ae670fd103f6cb))
* require google-cloud-core >= 1.3.0 ([#43](https://www.github.com/googleapis/python-resource-manager/issues/43)) ([16df2d0](https://www.github.com/googleapis/python-resource-manager/commit/16df2d064b25ac75234cbbd736b16fba53a51f2d))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-resource-manager/issues/1127)) ([#68](https://www.github.com/googleapis/python-resource-manager/issues/68)) ([d6e699e](https://www.github.com/googleapis/python-resource-manager/commit/d6e699eb0492c979871ed69f6badbec8ab3427f4)), closes [#1126](https://www.github.com/googleapis/python-resource-manager/issues/1126)


### Miscellaneous Chores

* release as 1.0.0 ([#78](https://www.github.com/googleapis/python-resource-manager/issues/78)) ([fc852aa](https://www.github.com/googleapis/python-resource-manager/commit/fc852aa0b0e42a37324ca94901c34015e6127df2))
* release as 1.0.0-rc1 ([#64](https://www.github.com/googleapis/python-resource-manager/issues/64)) ([cce4608](https://www.github.com/googleapis/python-resource-manager/commit/cce46083be8cd73cbe921ee8ac917806507b6084))

## [1.0.0-rc1](https://www.github.com/googleapis/python-resource-manager/compare/v0.30.3...v1.0.0-rc1) (2021-06-14)


### Features

* add v3 ([#62](https://www.github.com/googleapis/python-resource-manager/issues/62)) ([72f69f0](https://www.github.com/googleapis/python-resource-manager/commit/72f69f0f3a2205ef3bb49ca3e3ae670fd103f6cb))


### Bug Fixes

* remove v1beta1 ([72f69f0](https://www.github.com/googleapis/python-resource-manager/commit/72f69f0f3a2205ef3bb49ca3e3ae670fd103f6cb))
* require google-cloud-core >= 1.3.0 ([#43](https://www.github.com/googleapis/python-resource-manager/issues/43)) ([16df2d0](https://www.github.com/googleapis/python-resource-manager/commit/16df2d064b25ac75234cbbd736b16fba53a51f2d))


### Miscellaneous Chores

* release as 1.0.0-rc1 ([#64](https://www.github.com/googleapis/python-resource-manager/issues/64)) ([cce4608](https://www.github.com/googleapis/python-resource-manager/commit/cce46083be8cd73cbe921ee8ac917806507b6084))

### [0.30.3](https://www.github.com/googleapis/python-resource-manager/compare/v0.30.2...v0.30.3) (2020-12-10)


### Documentation

* update intersphinx for grpc and auth ([#35](https://www.github.com/googleapis/python-resource-manager/issues/35)) ([e98319c](https://www.github.com/googleapis/python-resource-manager/commit/e98319c7096a8101d47ec8f026050f866f59830c))
* update language of py2 admonition ([#26](https://www.github.com/googleapis/python-resource-manager/issues/26)) ([07bdc02](https://www.github.com/googleapis/python-resource-manager/commit/07bdc0215663fc8e3a35bd353aefbdcb4d3a5d30))

### [0.30.2](https://www.github.com/googleapis/python-resource-manager/compare/v0.30.1...v0.30.2) (2020-05-19)


### Bug Fixes

* fix list_projects behavior for multiple filter params ([#20](https://www.github.com/googleapis/python-resource-manager/issues/20)) ([26a708a](https://www.github.com/googleapis/python-resource-manager/commit/26a708a2628877e78b180ba3fae0b5d21f44fd7e))

### [0.30.1](https://www.github.com/googleapis/python-resource-manager/compare/v0.30.0...v0.30.1) (2020-02-20)


### Bug Fixes

* **resourcemanager:** update test assertion and core version pin ([#10095](https://www.github.com/googleapis/python-resource-manager/issues/10095)) ([9269dbc](https://www.github.com/googleapis/python-resource-manager/commit/9269dbc963abb46a3031b93cb53abe5bb03fe0f8))

## 0.30.0

10-10-2019 11:38 PDT


### New Features
- Add `client_options` support. ([#9043](https://github.com/googleapis/google-cloud-python/pull/9043))

### Dependencies
- Pin minimum version of `google-cloud-core` to 1.0.3. ([#9043](https://github.com/googleapis/google-cloud-python/pull/9043))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.29.2

07-24-2019 17:25 PDT

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.29.1

06-04-2019 11:14 PDT


### Dependencies
- Don't pin `google-api-core` in libs using `google-cloud-core`. ([#8213](https://github.com/googleapis/google-cloud-python/pull/8213))

## 0.29.0

05-16-2019 12:31 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to client / connection. ([#7870](https://github.com/googleapis/google-cloud-python/pull/7870))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 0.28.3

12-17-2018 16:59 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docs/fixit: normalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 0.28.2

12-10-2018 13:00 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Fix `filter_params` argument in `list_projects` ([#5383](https://github.com/googleapis/google-cloud-python/pull/5383))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Prep docs for repo split. ([#6022](https://github.com/googleapis/google-cloud-python/pull/6022))
- Declutter sidebar by supplying explict short titles. ([#5939](https://github.com/googleapis/google-cloud-python/pull/5939))

### Internal / Testing Changes
- Add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier

## 0.28.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-resource-manager/0.28.0/
