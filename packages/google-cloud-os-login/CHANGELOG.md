# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-oslogin/#history

### [2.2.1](https://www.github.com/googleapis/python-oslogin/compare/v2.2.0...v2.2.1) (2021-06-02)


### Documentation

* Fix broken links in README ([#75](https://www.github.com/googleapis/python-oslogin/issues/75)) ([d01d15f](https://www.github.com/googleapis/python-oslogin/commit/d01d15f034178e6bc9e36c80d0c0b1cf6cfd2f17))

## [2.2.0](https://www.github.com/googleapis/python-oslogin/compare/v2.1.0...v2.2.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([857db06](https://www.github.com/googleapis/python-oslogin/commit/857db06e1b777e62eba0180655d059e2729ba898))


### Bug Fixes

* add async client to %name_%version/init.py ([857db06](https://www.github.com/googleapis/python-oslogin/commit/857db06e1b777e62eba0180655d059e2729ba898))
* use correct retry deadline ([#56](https://www.github.com/googleapis/python-oslogin/issues/56)) ([a226955](https://www.github.com/googleapis/python-oslogin/commit/a22695516e8e89ccce2c500ade38c29451432b14))

## [2.1.0](https://www.github.com/googleapis/python-oslogin/compare/v2.0.0...v2.1.0) (2021-01-06)


### Features

* add common resource helpers, expose client transport, remove client side recv limit ([#41](https://www.github.com/googleapis/python-oslogin/issues/41)) ([ed84bb1](https://www.github.com/googleapis/python-oslogin/commit/ed84bb127eac218e845468d5d07a476af410ce71))
* add from_service_account_info factory and fix sphinx identifiers  ([#46](https://www.github.com/googleapis/python-oslogin/issues/46)) ([36d488c](https://www.github.com/googleapis/python-oslogin/commit/36d488cd552cdfd11401d7090adf4ef9d1b01f61))

## [2.0.0](https://www.github.com/googleapis/python-oslogin/compare/v1.0.0...v2.0.0) (2020-09-30)


### ⚠ BREAKING CHANGES

* move to microgen (#33). See [Migration Guide](https://github.com/googleapis/python-oslogin/blob/master/UPGRADING.md).

### Features

* move to microgen ([#33](https://www.github.com/googleapis/python-oslogin/issues/33)) ([97de222](https://www.github.com/googleapis/python-oslogin/commit/97de2223423162e39d25bb793c660a9ed5c30a2c))


### Bug Fixes

* update retry configs ([#24](https://www.github.com/googleapis/python-oslogin/issues/24)) ([13b6e8d](https://www.github.com/googleapis/python-oslogin/commit/13b6e8ddd1fbcf6f215ae706706bc44eb3e286c5))

## [1.0.0](https://www.github.com/googleapis/python-oslogin/compare/v0.3.0...v1.0.0) (2020-06-03)


### Features

* set release_status to production/stable ([#11](https://www.github.com/googleapis/python-oslogin/issues/11)) ([b695e81](https://www.github.com/googleapis/python-oslogin/commit/b695e81b4f9a45af162d04d68a1c588ea0aa3de7))

## [0.3.0](https://www.github.com/googleapis/python-oslogin/compare/v0.2.0...v1.0.0) (2020-04-21)


### ⚠ BREAKING CHANGES

* **oslogin:** rename `fingerprint_path` to `ssh_public_key_path`; rename `project_path` to `posix_account_path`; add `OperatingSystemType` enum; make `ssh_public_key` optional param to `import_ssh_public_key`; annotate protos (via synth) (#9431)

### Features

* **oslogin:** rename `fingerprint_path` to `ssh_public_key_path`; rename `project_path` to `posix_account_path`; add `OperatingSystemType` enum; make `ssh_public_key` optional param to `import_ssh_public_key`; annotate protos (via synth) ([#9431](https://www.github.com/googleapis/python-oslogin/issues/9431)) ([f903af4](https://www.github.com/googleapis/python-oslogin/commit/f903af460761fd4e259e8ba122df9f1fcd38adb2))


### Bug Fixes

* **oslogin:** add py2 deprecation warning; bump copyright year to 2020; add 3.8 unit tests (via synth) ([#10071](https://www.github.com/googleapis/python-oslogin/issues/10071)) ([3085490](https://www.github.com/googleapis/python-oslogin/commit/30854901bde0a2dbe25872f8e332fee4d425bcab))

## 0.2.0

07-24-2019 17:10 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel. ([#8398](https://github.com/googleapis/google-cloud-python/pull/8398))
- Reorder class methods, add routing header to method metadata, add nox session docs (via synth). ([#7934](https://github.com/googleapis/google-cloud-python/pull/7934))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Protoc-generated serialization update. ([#7090](https://github.com/googleapis/google-cloud-python/pull/7090))
- Pick up stub docstring fix in GAPIC generator. ([#6977](https://github.com/googleapis/google-cloud-python/pull/6977))

### New Features
- Add 'client_options' support (via synth). ([#8517](https://github.com/googleapis/google-cloud-python/pull/8517))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers

### Internal / Testing Changes
- Pin black version (via synth). ([#8589](https://github.com/googleapis/google-cloud-python/pull/8589))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
-  Declare encoding as utf-8 in pb2 files (via synth). ([#8359](https://github.com/googleapis/google-cloud-python/pull/8359))
- Add disclaimer to auto-generated template files (via synth). ([#8322](https://github.com/googleapis/google-cloud-python/pull/8322))
-  Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8247](https://github.com/googleapis/google-cloud-python/pull/8247))
- Fix coverage in 'types.py' (via synth). ([#8160](https://github.com/googleapis/google-cloud-python/pull/8160))
- Blacken noxfile.py, setup.py (via synth). ([#8127](https://github.com/googleapis/google-cloud-python/pull/8127))
- Add empty lines (via synth). ([#8066](https://github.com/googleapis/google-cloud-python/pull/8066))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.2

12-18-2018 09:36 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6575](https://github.com/googleapis/google-cloud-python/pull/6575))
- Fix `client_info` bug, update docstrings. ([#6417](https://github.com/googleapis/google-cloud-python/pull/6417))
- Avoid overwriting `__module__` of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add 'synth.py'. ([#6086](https://github.com/googleapis/google-cloud-python/pull/6086))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Rename releases to changelog and include from CHANGELOG.md ([#5191](https://github.com/googleapis/google-cloud-python/pull/5191))
- Fix bad trove classifier

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Normalize all setup.py files (#4909)
