# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-error-reporting/#history

### [1.1.2](https://www.github.com/googleapis/python-error-reporting/compare/v1.1.1...v1.1.2) (2021-04-05)


### Dependencies

* upgrade sphinx ([#99](https://www.github.com/googleapis/python-error-reporting/issues/99)) ([a118123](https://www.github.com/googleapis/python-error-reporting/commit/a118123cbfe8b5dd2a7ba260631b248c351cb116))

### [1.1.1](https://www.github.com/googleapis/python-error-reporting/compare/v1.1.0...v1.1.1) (2021-02-25)


### Bug Fixes

* remove gRPC send/recv limit; add enums to `types/__init__.py` ([#57](https://www.github.com/googleapis/python-error-reporting/issues/57)) ([e23e5ba](https://www.github.com/googleapis/python-error-reporting/commit/e23e5ba7eba4482735d5f4897210a1ebb81bfb8a))

## [1.1.0](https://www.github.com/googleapis/python-error-reporting/compare/v1.0.0...v1.1.0) (2020-12-01)


### Features

* add common resource path helpers; expose client transport as property ([#37](https://www.github.com/googleapis/python-error-reporting/issues/37)) ([bc92bc2](https://www.github.com/googleapis/python-error-reporting/commit/bc92bc2cfa549200bf8fa87cf2f6d81ded77486c))


### Bug Fixes

* changed import path for logging client ([#43](https://www.github.com/googleapis/python-error-reporting/issues/43)) ([a09449d](https://www.github.com/googleapis/python-error-reporting/commit/a09449def35077beb85782c34a61c8f172c2f018))


### Documentation

* removed stackdriver branding ([#44](https://www.github.com/googleapis/python-error-reporting/issues/44)) ([5eea8c4](https://www.github.com/googleapis/python-error-reporting/commit/5eea8c4f533a32d2b81b1b69e48d3bb47f1bc5b4))

## [1.0.0](https://www.github.com/googleapis/python-error-reporting/compare/v0.34.0...v1.0.0) (2020-08-28)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#23)

### Features

* migrate to use microgen ([#23](https://www.github.com/googleapis/python-error-reporting/issues/23)) ([cb41e3a](https://www.github.com/googleapis/python-error-reporting/commit/cb41e3a1003cb4ef4e32efc8b5c5b5ba7d670f7d))


### Documentation

* add multiprocessing note ([#13](https://www.github.com/googleapis/python-error-reporting/issues/13)) ([840d67c](https://www.github.com/googleapis/python-error-reporting/commit/840d67c09502ae99ce4771c66bde1cefb961a367))

## [0.34.0](https://www.github.com/googleapis/python-error-reporting/compare/v0.33.0...v0.34.0) (2020-05-03)


### Features

* set release_status to beta ([#5](https://www.github.com/googleapis/python-error-reporting/issues/5)) ([e9361c5](https://www.github.com/googleapis/python-error-reporting/commit/e9361c5e0f427a4796974fd4a3da506324220e9e))

## 0.33.0

10-22-2019 12:10 PDT

### New Features
- Add `client_options` to constructor ([#9152](https://github.com/googleapis/google-cloud-python/pull/9152))

### Dependencies
- Pin `google-cloud-logging >= 1.14.0, < 2.0.0dev`. ([#9476](https://github.com/googleapis/google-cloud-python/pull/9476))

### Documentation
- Remove references to the old authentication credentials. ([#9456](https://github.com/googleapis/google-cloud-python/pull/9456))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for `gh-pages`, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

### Internal / Testing Changes
- Harden `test_report_exception` systest by increasing `max_tries`. ([#9396](https://github.com/googleapis/google-cloud-python/pull/9396))

## 0.32.1

08-23-2019 10:12 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8954](https://github.com/googleapis/google-cloud-python/pull/8954))

### Documentation
- Fix documentation links for iam and error-reporting. ([#9073](https://github.com/googleapis/google-cloud-python/pull/9073))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.32.0

07-24-2019 16:17 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8389](https://github.com/googleapis/google-cloud-python/pull/8389))
- Fix typo in non-gRPC import. ([#8028](https://github.com/googleapis/google-cloud-python/pull/8028))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8508](https://github.com/googleapis/google-cloud-python/pull/8508))

### Documentation
- Fix docs navigation issues. ([#8723](https://github.com/googleapis/google-cloud-python/pull/8723))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix mistake in documentation ([#8271](https://github.com/googleapis/google-cloud-python/pull/8271))

### Internal / Testing Changes
- Pin black version (via synth). ([#8582](https://github.com/googleapis/google-cloud-python/pull/8582))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8351](https://github.com/googleapis/google-cloud-python/pull/8351))
- Add disclaimer to auto-generated template files (via synth). ([#8313](https://github.com/googleapis/google-cloud-python/pull/8313))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8240](https://github.com/googleapis/google-cloud-python/pull/8240))
- Blacken noxfile.py, setup.py (via synth). ([#8122](https://github.com/googleapis/google-cloud-python/pull/8122))
- Add empty lines (via synth). ([#8057](https://github.com/googleapis/google-cloud-python/pull/8057))

## 0.31.0

05-17-2019 08:23 PDT

### Implementation Changes
- Add routing header to method metadata (via synth). ([#7594](https://github.com/googleapis/google-cloud-python/pull/7594))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to Client. ([#7903](https://github.com/googleapis/google-cloud-python/pull/7903))

### Dependencies
- Pin `google-cloud-logging >= 1.11.0`. ([#8015](https://github.com/googleapis/google-cloud-python/pull/8015))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes
- Add nox session `docs` (via synth). ([#7770](https://github.com/googleapis/google-cloud-python/pull/7770))
- Fix docstring replace in synth ([#7458](https://github.com/googleapis/google-cloud-python/pull/7458))
- Copy lintified proto files (via synth). ([#7447](https://github.com/googleapis/google-cloud-python/pull/7447))
- Add clarifying comment to blacken nox target (via synth). ([#7391](https://github.com/googleapis/google-cloud-python/pull/7391))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers. ([#7144](https://github.com/googleapis/google-cloud-python/pull/7144))
- Protoc-generated serialization update. ([#7082](https://github.com/googleapis/google-cloud-python/pull/7082))
- Pick up stub docstring fix in GAPIC generator. ([#6970](https://github.com/googleapis/google-cloud-python/pull/6970))
- Fix formatting ([#7002](https://github.com/googleapis/google-cloud-python/pull/7002))

## 0.30.1

12-17-2018 18:17 PST


### Implementation Changes
- Pick up fixes to GAPIC generator. ([#6522](https://github.com/googleapis/google-cloud-python/pull/6522))
- Fix `client_info` bug, update docstrings via synth. ([#6442](https://github.com/googleapis/google-cloud-python/pull/6442))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Fix [#6321](https://github.com/googleapis/google-cloud-python/pull/6321) Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Prep docs for repo split. ([#6155](https://github.com/googleapis/google-cloud-python/pull/6155))
- Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6566](https://github.com/googleapis/google-cloud-python/pull/6566))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add 'synth.py'. ([#6082](https://github.com/googleapis/google-cloud-python/pull/6082))
- Use Nox inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))

## 0.30.0

### Implementation Changes
- Make dependency on logging less restrictive in error_reporting (#5345)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Fix bad trove classifier

## 0.29.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- Fix missing extra in api-core dependency (#4764)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)

## 0.29.0

### Breaking changes

- The underlying autogenerated client library was re-generated to pick up new 
  features and resolve bugs, this may change the exceptions raised from various
  methods. (#4695)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Upgrading to `google-cloud-logging >= 1.4.0` (#4296)

PyPI: https://pypi.org/project/google-cloud-error-reporting/0.28.0/
