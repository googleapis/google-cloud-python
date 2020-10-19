# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history

## [2.0.0](https://www.github.com/googleapis/python-language/compare/v1.3.0...v2.0.0) (2020-10-16)


### Features

* Migrate API to use python micro-generator ([#41](https://www.github.com/googleapis/python-language/issues/41)) ([b408b14](https://www.github.com/googleapis/python-language/commit/b408b1431194d8e1373b5d986d476add639f7e87))


### Documentation

* add multiprocessing note ([#26](https://www.github.com/googleapis/python-language/issues/26)) ([a489102](https://www.github.com/googleapis/python-language/commit/a489102ca0f5ab302ec8974728a52065f2ea8857))
* add spacing for readability ([#22](https://www.github.com/googleapis/python-language/issues/22)) ([7dff809](https://www.github.com/googleapis/python-language/commit/7dff809b94b5a1d001aeb1e7763dbbe624865600))
* fix small typo ([#5](https://www.github.com/googleapis/python-language/issues/5)) ([7a9d4dd](https://www.github.com/googleapis/python-language/commit/7a9d4ddf676f2a77e1bd83e02b8d7987a72c6525))
* **language:** change docstring formatting; bump copyright year to 2020 (via synth) ([#10234](https://www.github.com/googleapis/python-language/issues/10234)) ([b68b216](https://www.github.com/googleapis/python-language/commit/b68b2166d8e4d81a7e51e701f8facdfd7fb82a26))
* **language:** edit hyphenation of "part-of-speech" (via synth) ([#9954](https://www.github.com/googleapis/python-language/issues/9954)) ([6246ef9](https://www.github.com/googleapis/python-language/commit/6246ef904871405334c0b3bd6c2490b79ffe56fa))
* **language:** fixes typo in Natural Language samples ([#10134](https://www.github.com/googleapis/python-language/issues/10134)) ([223d614](https://www.github.com/googleapis/python-language/commit/223d6140145dcf5c48af206212db58a062a7937b))
* add python 2 sunset banner to documentation ([#9036](https://www.github.com/googleapis/python-language/issues/9036)) ([1fe4105](https://www.github.com/googleapis/python-language/commit/1fe4105e078f84f1d4ea713550c26bdf91096d4a))
* fix intersphinx reference to requests ([#9294](https://www.github.com/googleapis/python-language/issues/9294)) ([e97a0ae](https://www.github.com/googleapis/python-language/commit/e97a0ae6c2e3a26afc9b3af7d91118ac3c0aa1f7))
* Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://www.github.com/googleapis/python-language/issues/9085)) ([6b15df6](https://www.github.com/googleapis/python-language/commit/6b15df6091378ed444642fc813d49d8bbbb6365d))

## 1.3.0

07-24-2019 16:44 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel  ([#8396](https://github.com/googleapis/google-cloud-python/pull/8396))

### New Features
- Add 'client_options' support (via synth). ([#8515](https://github.com/googleapis/google-cloud-python/pull/8515))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Add google.api proto annotations, update docstrings (via synth). ([#7659](https://github.com/googleapis/google-cloud-python/pull/7659))

### Internal / Testing Changes
- Pin black version (via synth). ([#8588](https://github.com/googleapis/google-cloud-python/pull/8588))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8357](https://github.com/googleapis/google-cloud-python/pull/8357))
- Add disclaimer to auto-generated template files (via synth).  ([#8319](https://github.com/googleapis/google-cloud-python/pull/8319))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8246](https://github.com/googleapis/google-cloud-python/pull/8246))
- Blacken 'noxfile.py' / 'setup.py' (via synth). ([#8158](https://github.com/googleapis/google-cloud-python/pull/8158))
- Add empty lines (via synth). ([#8063](https://github.com/googleapis/google-cloud-python/pull/8063))
- Add nox session `docs` (via synth). ([#7776](https://github.com/googleapis/google-cloud-python/pull/7776))

## 1.2.0

03-29-2019 09:53 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Protoc-generated serialization update. ([#7087](https://github.com/googleapis/google-cloud-python/pull/7087))

### New Features
- Add new entity types (via synth). ([#7510](https://github.com/googleapis/google-cloud-python/pull/7510))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Pick up stub docstring fix in GAPIC generator. ([#6975](https://github.com/googleapis/google-cloud-python/pull/6975))

### Internal / Testing Changes
- Copy lintified proto files (via synth). ([#7468](https://github.com/googleapis/google-cloud-python/pull/7468))
- Add clarifying comment to blacken nox target. ([#7397](https://github.com/googleapis/google-cloud-python/pull/7397))
- Copy in correct proto versions via synth. [#7257](https://github.com/googleapis/google-cloud-python/pull/7257))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 1.1.1

12-18-2018 09:34 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6521](https://github.com/googleapis/google-cloud-python/pull/6521))
- Fix `client_info` bug, update docstrings. ([#6415](https://github.com/googleapis/google-cloud-python/pull/6415))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Fix usage docs example for entity extraction ([#6193](https://github.com/googleapis/google-cloud-python/pull/6193))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6570](https://github.com/googleapis/google-cloud-python/pull/6570))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 1.1.0

10-05-2018 13:52 PDT

### Implementation Changes

- The library has been regenerated to pick up changes in the underlying API.
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))

### Documentation

- Translate / Logging / Language: restore detailed usage docs. ([#5999](https://github.com/googleapis/google-cloud-python/pull/5999))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Prep language docs for repo split. ([#5932](https://github.com/googleapis/google-cloud-python/pull/5932))

### Internal / Testing Changes

- Language: add 'synth.py'. ([#6080](https://github.com/googleapis/google-cloud-python/pull/6080))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))

## 1.0.2

### Packaging
- Update setuptools before packaging (#5265)
- Update setup.py to use recommended method for python-verson specific dependencies (#5266)
- Fix bad trove classifier

## 1.0.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix coveragerc to correctly omit generated files (#4843)

## 1.0.0

[![release level](https://img.shields.io/badge/release%20level-general%20availability%20%28GA%29-brightgreen.svg?style&#x3D;flat)](https://cloud.google.com/terms/launch-stages)

### Features

##### General Availability

The `google-cloud-language` package is now supported at the **general availability** quality level. This means it is stable; the code and API surface will not change in backwards-incompatible ways unless absolutely necessary (e.g. because of critical security issues) or with an extensive deprecation period.

One exception to this: We will remove beta endpoints (as a semver-minor update) at whatever point the underlying endpoints go away.

## 0.31.0

### Release Candidate

  * This update is considered a final "release candidate", and
    the `google-cloud-language` package is preparing for a GA release
    in the near future.

### :warning: Breaking Changes!

  * Some rarely-used arguments to the `LanguageServiceClient` constructor
    have been removed (in favor of a subclass or a custom gRPC channel).
    It is unlikely that you used these, but if you did, then this update
    will represent a breaking change.
      * The removed arguments are: `client_config`, `lib_name`, `lib_version`
        `metrics_headers`, `ssl_credentials`, and `scopes`.

### Features

  * Added the `classify_text` method on the primary (`v1`) endpoint. (#4283)

## 0.30.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-language/0.30.0/
