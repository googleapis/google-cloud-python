# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-resource-manager/#history

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
