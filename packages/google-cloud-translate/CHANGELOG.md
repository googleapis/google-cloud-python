# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-translate/#history

### [3.7.3](https://github.com/googleapis/python-translate/compare/v3.7.2...v3.7.3) (2022-05-19)


### Documentation

* fix type in docstring for map fields ([3b845d6](https://github.com/googleapis/python-translate/commit/3b845d68eddd852c2d65bb852de6c5c4b4d096ad))

### [3.7.2](https://github.com/googleapis/python-translate/compare/v3.7.1...v3.7.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#348](https://github.com/googleapis/python-translate/issues/348)) ([fe3ac1e](https://github.com/googleapis/python-translate/commit/fe3ac1e68cf50147fcb0aecf01aec17f5e598425))
* **deps:** require proto-plus>=1.15.0 ([fe3ac1e](https://github.com/googleapis/python-translate/commit/fe3ac1e68cf50147fcb0aecf01aec17f5e598425))

### [3.7.1](https://github.com/googleapis/python-translate/compare/v3.7.0...v3.7.1) (2022-02-26)


### Documentation

* add generated snippets ([#336](https://github.com/googleapis/python-translate/issues/336)) ([36c4483](https://github.com/googleapis/python-translate/commit/36c4483e9fac4933fc024fcae24ae8fbbdb470a0))

## [3.7.0](https://github.com/googleapis/python-translate/compare/v3.6.1...v3.7.0) (2022-02-03)


### Features

* add api key support ([#329](https://github.com/googleapis/python-translate/issues/329)) ([4b08cd5](https://github.com/googleapis/python-translate/commit/4b08cd56ce230b843ced78a3f81c2e6511ac2a4f))


### Bug Fixes

* 290 added a create glossary line before each call using bistro-glossary ([#302](https://github.com/googleapis/python-translate/issues/302)) ([742e414](https://github.com/googleapis/python-translate/commit/742e414ad8ac83e4116c67740a42e264a63e3287))
* resolve DuplicateCredentialArgs error when using credentials_file ([26791c2](https://github.com/googleapis/python-translate/commit/26791c251e851f921d23316e6ca5adab648c63c0))

### [3.6.1](https://www.github.com/googleapis/python-translate/compare/v3.6.0...v3.6.1) (2021-11-04)


### Bug Fixes

* **deps:** drop packaging dependency ([7924322](https://www.github.com/googleapis/python-translate/commit/79243222e5e16e1b7cb50b9d69862ddf6023ad4f))
* **deps:** require google-api-core >= 1.28.0 ([7924322](https://www.github.com/googleapis/python-translate/commit/79243222e5e16e1b7cb50b9d69862ddf6023ad4f))


### Documentation

* list oneofs in docstring ([7924322](https://www.github.com/googleapis/python-translate/commit/79243222e5e16e1b7cb50b9d69862ddf6023ad4f))
* **samples:** Add Cloud Code tags for API Explorer pilot ([#282](https://www.github.com/googleapis/python-translate/issues/282)) ([3e8df68](https://www.github.com/googleapis/python-translate/commit/3e8df6836f0508fb4c6cd1c4a9f2f39192a01cea))

## [3.6.0](https://www.github.com/googleapis/python-translate/compare/v3.5.0...v3.6.0) (2021-10-18)


### Features

* add support for python 3.10 ([#275](https://www.github.com/googleapis/python-translate/issues/275)) ([381fc15](https://www.github.com/googleapis/python-translate/commit/381fc15cd920252edbc280b7623125955ee68347))


### Bug Fixes

* add model signature for batch document translation ([#276](https://www.github.com/googleapis/python-translate/issues/276)) ([be0b01b](https://www.github.com/googleapis/python-translate/commit/be0b01bb5b21cec9910967305784fc02c7ce83ff))

## [3.5.0](https://www.github.com/googleapis/python-translate/compare/v3.4.1...v3.5.0) (2021-10-11)


### Features

* add context manager support in client ([#267](https://www.github.com/googleapis/python-translate/issues/267)) ([6e750e8](https://www.github.com/googleapis/python-translate/commit/6e750e8d655cc6ae7967ff5e105b6f64dd05c4c3))


### Bug Fixes

* [#254](https://www.github.com/googleapis/python-translate/issues/254) by increasing timeout, use backoff module instead of flaky ([#271](https://www.github.com/googleapis/python-translate/issues/271)) ([0cff0f2](https://www.github.com/googleapis/python-translate/commit/0cff0f2d6c1a6509f03e18a5a3dbd8377f864b27))

### [3.4.1](https://www.github.com/googleapis/python-translate/compare/v3.4.0...v3.4.1) (2021-09-30)


### Bug Fixes

* add 'dict' annotation type to 'request' ([6bbf390](https://www.github.com/googleapis/python-translate/commit/6bbf39038f37a3d16018d9ee9f356145a50f987c))
* improper types in pagers generation ([cd70523](https://www.github.com/googleapis/python-translate/commit/cd70523d9a628684515a8d910e7e5158817b3e61))

## [3.4.0](https://www.github.com/googleapis/python-translate/compare/v3.3.2...v3.4.0) (2021-08-29)


### Features

* add translate_document and batch_translate_document ([#234](https://www.github.com/googleapis/python-translate/issues/234)) ([b5962d6](https://www.github.com/googleapis/python-translate/commit/b5962d68051d7dc6e4213c78d21ab3bbea1411f5))
* **v3beta1:** add format_conversions ([b5962d6](https://www.github.com/googleapis/python-translate/commit/b5962d68051d7dc6e4213c78d21ab3bbea1411f5))


### Bug Fixes

* add missing annotation for batch document translation ([#231](https://www.github.com/googleapis/python-translate/issues/231)) ([a1297ba](https://www.github.com/googleapis/python-translate/commit/a1297ba6079524f82588c3fe79ec3f5c433a7606))

### [3.3.2](https://www.github.com/googleapis/python-translate/compare/v3.3.1...v3.3.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#215](https://www.github.com/googleapis/python-translate/issues/215)) ([2f1bc32](https://www.github.com/googleapis/python-translate/commit/2f1bc327fd436f2f7e86c676cbbf1e7d7cc61921))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#206](https://www.github.com/googleapis/python-translate/issues/206)) ([6f1df67](https://www.github.com/googleapis/python-translate/commit/6f1df6794394bcbedb18199793aaebb9c095ccf5))


### Miscellaneous Chores

* release as 3.3.2 ([#218](https://www.github.com/googleapis/python-translate/issues/218)) ([e14de99](https://www.github.com/googleapis/python-translate/commit/e14de99d9d3480274ba92ef36c93f0b626a2bd91))

### [3.3.1](https://www.github.com/googleapis/python-translate/compare/v3.3.0...v3.3.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#205](https://www.github.com/googleapis/python-translate/issues/205)) ([3a11025](https://www.github.com/googleapis/python-translate/commit/3a1102560ab70f8a7021f3b4f024e3e9feb134fe))

## [3.3.0](https://www.github.com/googleapis/python-translate/compare/v3.2.1...v3.3.0) (2021-07-19)


### Features

* add always_use_jwt_access ([778878d](https://www.github.com/googleapis/python-translate/commit/778878d7aeb70a3da249c91b8a2bd36c675b1e4b))


### Bug Fixes

* disable always_use_jwt_access ([#186](https://www.github.com/googleapis/python-translate/issues/186)) ([778878d](https://www.github.com/googleapis/python-translate/commit/778878d7aeb70a3da249c91b8a2bd36c675b1e4b))

### [3.2.1](https://www.github.com/googleapis/python-translate/compare/v3.2.0...v3.2.1) (2021-06-21)


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-translate/issues/1127)) ([#175](https://www.github.com/googleapis/python-translate/issues/175)) ([7ef5f04](https://www.github.com/googleapis/python-translate/commit/7ef5f04cdb80198472bdc376364db9cc0a91fd9e))

## [3.2.0](https://www.github.com/googleapis/python-translate/compare/v3.1.0...v3.2.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([959a35c](https://www.github.com/googleapis/python-translate/commit/959a35c85e32867ed63c63d96593a240a5e8a1c4))


### Bug Fixes

* add async client to %name_%version/init.py ([959a35c](https://www.github.com/googleapis/python-translate/commit/959a35c85e32867ed63c63d96593a240a5e8a1c4))
* **deps:** add packaging requirement ([959a35c](https://www.github.com/googleapis/python-translate/commit/959a35c85e32867ed63c63d96593a240a5e8a1c4))


### Documentation

* connect Python Translate client library to nebulous serverless example ([#162](https://www.github.com/googleapis/python-translate/issues/162)) ([2986864](https://www.github.com/googleapis/python-translate/commit/2986864db391e5216dbead83eb822fd1fb2c19d0))

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
