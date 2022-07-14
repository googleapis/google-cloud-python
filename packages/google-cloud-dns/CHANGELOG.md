# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dns/#history

## [0.34.1](https://github.com/googleapis/python-dns/compare/v0.34.0...v0.34.1) (2022-07-14)


### Bug Fixes

* require python 3.7+ ([#163](https://github.com/googleapis/python-dns/issues/163)) ([6882da5](https://github.com/googleapis/python-dns/commit/6882da56f7ef44b2ccd337ac4d48bd8093cb146e))

## [0.34.0](https://www.github.com/googleapis/python-dns/compare/v0.33.1...v0.34.0) (2021-10-08)


### Features

* add support for Python 3.10 ([#121](https://www.github.com/googleapis/python-dns/issues/121)) ([af8be30](https://www.github.com/googleapis/python-dns/commit/af8be306e5c8512602e739471c016d84b4b46759))

### [0.33.1](https://www.github.com/googleapis/python-dns/compare/v0.33.0...v0.33.1) (2021-09-20)


### Bug Fixes

* remove six ([#115](https://www.github.com/googleapis/python-dns/issues/115)) ([95f94ef](https://www.github.com/googleapis/python-dns/commit/95f94ef4d75273deae56dc8ecfcc708e2be84d03))

## [0.33.0](https://www.github.com/googleapis/python-dns/compare/v0.32.3...v0.33.0) (2021-07-23)


### Features

* require python 3.6 ([#61](https://www.github.com/googleapis/python-dns/issues/61)) ([56ab29f](https://www.github.com/googleapis/python-dns/commit/56ab29f35e0fda4f290f7cf2697466928080bd2f))

### [0.32.3](https://www.github.com/googleapis/python-dns/compare/v0.32.2...v0.32.3) (2021-05-27)


### Bug Fixes

* require google-cloud-core >= 1.3.0 ([#38](https://www.github.com/googleapis/python-dns/issues/38)) ([3ba0456](https://www.github.com/googleapis/python-dns/commit/3ba0456e6df34845c8d601d6d359eed98bfc17cf))

### [0.32.2](https://www.github.com/googleapis/python-dns/compare/v0.32.1...v0.32.2) (2021-02-11)


### Documentation

* **python:** update intersphinx for grpc and auth ([#30](https://www.github.com/googleapis/python-dns/issues/30)) ([142d2e7](https://www.github.com/googleapis/python-dns/commit/142d2e777ccaf857d5455c4640f6d0502fad89e0))

### [0.32.1](https://www.github.com/googleapis/python-dns/compare/v0.32.0...v0.32.1) (2020-10-12)


### Bug Fixes

* fix client.quotas() method ([#24](https://www.github.com/googleapis/python-dns/issues/24)) ([9d97955](https://www.github.com/googleapis/python-dns/commit/9d979552512c633366e5ff34d155b5550ec7f6f3))


### Documentation

* remove samples in library docs ([#17](https://www.github.com/googleapis/python-dns/issues/17)) ([51d4d10](https://www.github.com/googleapis/python-dns/commit/51d4d10884d3e13bb9051114537a1a6eddab0086))
* update README.rst ([#25](https://www.github.com/googleapis/python-dns/issues/25)) ([3e511cb](https://www.github.com/googleapis/python-dns/commit/3e511cb0b4c6496d310365aeb326cf720a8d5609))

## [0.32.0](https://www.github.com/googleapis/python-dns/compare/v0.31.0...v0.32.0) (2020-02-11)


### Features

* **dns:** add 'client_options' argument to client ctor ([#9516](https://www.github.com/googleapis/python-dns/issues/9516)) ([ab31add](https://www.github.com/googleapis/python-dns/commit/ab31add5be9c49d441e0b5cdf48c5fb3cfc6fc19)), closes [#8475](https://www.github.com/googleapis/python-dns/issues/8475)


### Bug Fixes

* **dns:** update test assertion and core version pins ([#10096](https://www.github.com/googleapis/python-dns/issues/10096)) ([b6e7b49](https://www.github.com/googleapis/python-dns/commit/b6e7b49d1a5d30362eddec48b7e5f800c26bc59c))

## 0.31.0

10-15-2019 06:42 PDT


### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

### Documentation
- Fix intersphinx reference to `requests`. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Fix broken links in docs. ([#9148](https://github.com/googleapis/google-cloud-python/pull/9148))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 0.30.2

07-11-2019 10:09 PDT

### Implementation Changes
- Change base url to dns.googleapis.com ([#8641](https://github.com/googleapis/google-cloud-python/pull/8641))

### Internal / Testing Changes
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.30.1

06-04-2019 11:13 PDT


### Dependencies
- Don't pin 'google-api-core' in libs using 'google-cloud-core'. ([#8213](https://github.com/googleapis/google-cloud-python/pull/8213))

## 0.30.0

05-16-2019 12:23 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to client / connection. ([#7869](https://github.com/googleapis/google-cloud-python/pull/7869))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 0.29.2

12-17-2018 16:47 PST


### Implementation Changes
- Ensure that `ManagedZone:exists()` does not misreport `True` result. ([#6884](https://github.com/googleapis/google-cloud-python/pull/6884))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docs/fixit: normalize docs for `page_size` / `max_results` / `page_token` ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 0.29.1

12-10-2018 12:50 PST


### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix 'Datastore' in text as well as examples / links

### Internal / Testing Changes
- Add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Fix copy-pasta from datastore README. ([#6208](https://github.com/googleapis/google-cloud-python/pull/6208))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Prep dns docs for repo split. ([#6020](https://github.com/googleapis/google-cloud-python/pull/6020))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier

## 0.29.0

### Implementation changes

- Renaming `makeResource` -> `make_resource`. (#4355)

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

PyPI: https://pypi.org/project/google-cloud-dns/0.28.0/
