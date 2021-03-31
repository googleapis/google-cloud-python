# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-translate/#history

## [3.1.0](https://www.github.com/googleapis/python-translate/compare/v3.0.2...v3.1.0) (2021-03-31)


### Features

* add `from_service_account_info` ([a397eff](https://www.github.com/googleapis/python-translate/commit/a397effb87f74f579605bcf261bf2b00d5e9fa5b))
* **v3beta1:** add online and batch document translation ([a397eff](https://www.github.com/googleapis/python-translate/commit/a397effb87f74f579605bcf261bf2b00d5e9fa5b))
* **v3beta1:** add online and batch document translation  ([#121](https://www.github.com/googleapis/python-translate/issues/121)) ([a397eff](https://www.github.com/googleapis/python-translate/commit/a397effb87f74f579605bcf261bf2b00d5e9fa5b))


### Bug Fixes

* moves region tags ([#103](https://www.github.com/googleapis/python-translate/issues/103)) ([e161eb5](https://www.github.com/googleapis/python-translate/commit/e161eb5e9cdc3124aa7efe2d535bae67812ae93c))
* use correct retry deadlines ([a397eff](https://www.github.com/googleapis/python-translate/commit/a397effb87f74f579605bcf261bf2b00d5e9fa5b))

### [3.0.2](https://www.github.com/googleapis/python-translate/compare/v3.0.1...v3.0.2) (2020-12-09)


### Documentation

* add w/ glossary and model ([1e030d4](https://www.github.com/googleapis/python-translate/commit/1e030d4557ee1f67bad5e5b4759d0200efd27afd))

### [3.0.1](https://www.github.com/googleapis/python-translate/compare/v3.0.0...v3.0.1) (2020-08-08)


### Bug Fixes

* update retry and timeout config ([#39](https://www.github.com/googleapis/python-translate/issues/39)) ([a334317](https://www.github.com/googleapis/python-translate/commit/a334317bc34b8927adfbc4a2559dbb71ee22c78d))

## [3.0.0](https://www.github.com/googleapis/python-translate/compare/v2.0.2...v3.0.0) (2020-08-05)


### ⚠ BREAKING CHANGES

* migrate API to microgenerator (#31)

### Features

* migrate API to microgenerator ([#31](https://www.github.com/googleapis/python-translate/issues/31)) ([1c5b6e8](https://www.github.com/googleapis/python-translate/commit/1c5b6e89a0a3b55c41c909e4ee27e0bd23e4b579))

### [2.0.2](https://www.github.com/googleapis/python-translate/compare/v2.0.1...v2.0.2) (2020-08-03)


### Bug Fixes

* refactored MP3 file creation test for Hybrid glossaries samples [([#2379](https://www.github.com/googleapis/python-translate/issues/2379))](https://github.com/GoogleCloudPlatform/python-docs-samples/issues/2379) ([b8b5101](https://www.github.com/googleapis/python-translate/commit/b8b5101be28d0d0d17a4d688eea81af6754a394c))
* translate test [([#2671](https://www.github.com/googleapis/python-translate/issues/2671))](https://github.com/GoogleCloudPlatform/python-docs-samples/issues/2671) ([a3d9f80](https://www.github.com/googleapis/python-translate/commit/a3d9f804576caeb4fdcdbbd4479caeb926efd8d0))
* update default retry config ([#15](https://www.github.com/googleapis/python-translate/issues/15)) ([dddf0bf](https://www.github.com/googleapis/python-translate/commit/dddf0bf33463968932031cc0be5bc8a0d4a96455))

### [2.0.1](https://www.github.com/googleapis/python-translate/compare/v2.0.0...v2.0.1) (2020-01-31)


### Bug Fixes

* **translate:**  add py2 deprecation warning; bump copyright year to 2020; add 3.8 unit tests (via synth) ([#9943](https://www.github.com/googleapis/python-translate/issues/9943)) ([b57f09a](https://www.github.com/googleapis/python-translate/commit/b57f09a5f804daca1a96918a29746f24ae7bc4a5))
* **translate:** update test assertion and core version pins ([#10098](https://www.github.com/googleapis/python-translate/issues/10098)) ([74b7757](https://www.github.com/googleapis/python-translate/commit/74b77579a1770c743353bdafde3e1744cbbe7842))

## 2.0.0

10-23-2019 11:13 PDT

### New Features
- Make v3 the default client. ([#9498](https://github.com/googleapis/google-cloud-python/pull/9498))

### Internal / Testing Changes
- Add VPC-SC system tests. ([#9272](https://github.com/googleapis/google-cloud-python/pull/9272))

## 1.7.0

10-07-2019 14:57 PDT

### Implementation Changes
- Update docstrings, client confg (via synth). ([#9411](https://github.com/googleapis/google-cloud-python/pull/9411))
- Remove send / receive message size limit (via synth). ([#8974](https://github.com/googleapis/google-cloud-python/pull/8974))

### New Features
- Add support for V3 of the API. ([#9020](https://github.com/googleapis/google-cloud-python/pull/9020))
- Make `parent` argument required for all client methods in v3beta1; add `labels` argument (via synth). ([#9354](https://github.com/googleapis/google-cloud-python/pull/9354))
- Add client options to translate_v2. ([#8737](https://github.com/googleapis/google-cloud-python/pull/8737))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix links to reference documentation. ([#8884](https://github.com/googleapis/google-cloud-python/pull/8884))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

### Internal / Testing Changes
- Update `ListGlossaries` method annotation (via synth)  ([#9385](https://github.com/googleapis/google-cloud-python/pull/9385))
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.6.0

07-09-2019 13:13 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8409](https://github.com/googleapis/google-cloud-python/pull/8409))
- Update service descriptions and add additional rpc bindings for Translate ([#8267](https://github.com/googleapis/google-cloud-python/pull/8267))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8527](https://github.com/googleapis/google-cloud-python/pull/8527))

### Internal / Testing Changes
- Pin black version (via synth). ([#8600](https://github.com/googleapis/google-cloud-python/pull/8600))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth).  ([#8369](https://github.com/googleapis/google-cloud-python/pull/8369))
- Add disclaimer to auto-generated template files (via synth).  ([#8333](https://github.com/googleapis/google-cloud-python/pull/8333))
- Blacken (via synth). ([#8282](https://github.com/googleapis/google-cloud-python/pull/8282))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8255](https://github.com/googleapis/google-cloud-python/pull/8255))
- Fix coverage in 'types.py' (via synth). ([#8168](https://github.com/googleapis/google-cloud-python/pull/8168))
- Blacken noxfile.py, setup.py (via synth). ([#8135](https://github.com/googleapis/google-cloud-python/pull/8135))
- Add empty lines (via synth). ([#8076](https://github.com/googleapis/google-cloud-python/pull/8076))

## 1.5.0

05-16-2019 13:05 PDT


### Implementation Changes
- Add routing header to method metadata, fix docstring (via synth). ([#7660](https://github.com/googleapis/google-cloud-python/pull/7660))

### New Features
- Add `client_info` support to client / connection. ([#7873](https://github.com/googleapis/google-cloud-python/pull/7873))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Add docs for v3beta1. ([#7681](https://github.com/googleapis/google-cloud-python/pull/7681))

### Internal / Testing Changes
- Harden system test against back-end changes. ([#7987](https://github.com/googleapis/google-cloud-python/pull/7987))
- Exclude `docs/conf.py` in synth. ([#7943](https://github.com/googleapis/google-cloud-python/pull/7943))
- Update `docs/conf.py` (via synth). ([#7837](https://github.com/googleapis/google-cloud-python/pull/7837))
- Add nox session `docs`, reorder methods (via synth). ([#7785](https://github.com/googleapis/google-cloud-python/pull/7785))

## 1.4.0

04-02-2019 14:24 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add Translate v3 ([#7637](https://github.com/googleapis/google-cloud-python/pull/7637))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 1.3.3

12-17-2018 17:07 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 1.3.2

12-10-2018 13:33 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Fix rtype for `Client.detect_language` for single values ([#5397](https://github.com/googleapis/google-cloud-python/pull/5397))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix installation package in README.rst ([#6426](https://github.com/googleapis/google-cloud-python/pull/6426))
- Fix [#6321](https://github.com/googleapis/google-cloud-python/pull/6321) Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Restore detailed usage docs. ([#5999](https://github.com/googleapis/google-cloud-python/pull/5999))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Prep translate docs for repo split. ([#5941](https://github.com/googleapis/google-cloud-python/pull/5941))

### Internal / Testing Changes
- Add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Adapt system test to updated back-end translation. ([#6427](https://github.com/googleapis/google-cloud-python/pull/6427))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier

## 1.3.1

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

## 1.3.0

### Notable Implementation Changes

- Use POST (rather than GET) for API `translate` requests (#4095,
  h/t to @Maerig)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)
- Fix example in `Config.get_variable()` (#3910)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-translate/1.3.0/
