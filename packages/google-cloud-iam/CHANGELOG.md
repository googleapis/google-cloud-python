# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-iam/#history

## [2.1.0](https://www.github.com/googleapis/python-iam/compare/v2.0.0...v2.1.0) (2021-01-25)


### Features

* add 'from_service_account_info' factory to clients ([29746e1](https://www.github.com/googleapis/python-iam/commit/29746e1984fc3942d830f54a9e921151d4d720c1))
* add common resource helpers; expose client transport ([da9e307](https://www.github.com/googleapis/python-iam/commit/da9e307cec6e2d38ef3c42a67ebdb6ab915b09f5))
* add from_service_account_info factory and fix sphinx identifiers  ([#48](https://www.github.com/googleapis/python-iam/issues/48)) ([29746e1](https://www.github.com/googleapis/python-iam/commit/29746e1984fc3942d830f54a9e921151d4d720c1))


### Bug Fixes

* fix sphinx identifiers ([29746e1](https://www.github.com/googleapis/python-iam/commit/29746e1984fc3942d830f54a9e921151d4d720c1))
* remove client recv msg limit fix: add enums to `types/__init__.py` ([#43](https://www.github.com/googleapis/python-iam/issues/43)) ([8f5023d](https://www.github.com/googleapis/python-iam/commit/8f5023dbb24a8151bfcd967261904797d8d74b5b))


### Documentation

* link to migration guide ([#28](https://www.github.com/googleapis/python-iam/issues/28)) ([f895427](https://www.github.com/googleapis/python-iam/commit/f895427f7e59820931de194af42a10f44c5e9ae6))

## [2.0.0](https://www.github.com/googleapis/python-iam/compare/v1.0.1...v2.0.0) (2020-07-27)


### ⚠ BREAKING CHANGES

* migrate to microgenerator (#26). See the [migration guide](https://github.com/googleapis/python-iam/blob/master/UPGRADING.md).

### Features

* migrate to microgenerator ([#26](https://www.github.com/googleapis/python-iam/issues/26)) ([60e221b](https://www.github.com/googleapis/python-iam/commit/60e221b010c18f12b156c2e282edc647d178a0f2))

### [1.0.1](https://www.github.com/googleapis/python-iam/compare/v1.0.0...v1.0.1) (2020-06-29)


### Bug Fixes

* update default retry config ([#21](https://www.github.com/googleapis/python-iam/issues/21)) ([840de7e](https://www.github.com/googleapis/python-iam/commit/840de7e974f1214d420d7ff9fc990cd9710baa66))


### Documentation

* fix a tiny typo in the README ([#20](https://www.github.com/googleapis/python-iam/issues/20)) ([ef36fe8](https://www.github.com/googleapis/python-iam/commit/ef36fe8eac9b0ff6bd57132c71135718c3c55f9d))

## [1.0.0](https://www.github.com/googleapis/python-iam/compare/v0.3.0...v1.0.0) (2020-05-19)


### Features

* release as production/stable ([#14](https://www.github.com/googleapis/python-iam/issues/14)) ([4ccb185](https://www.github.com/googleapis/python-iam/commit/4ccb185e968ce1a35e8c7a9795d8e418bafc1dcb)), closes [#6](https://www.github.com/googleapis/python-iam/issues/6) [#13](https://www.github.com/googleapis/python-iam/issues/13)

## [0.3.0](https://www.github.com/googleapis/python-iam/compare/v0.2.1...v0.3.0) (2020-02-03)


### Features

* **iam:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10043](https://www.github.com/googleapis/python-iam/issues/10043)) ([0a23a84](https://www.github.com/googleapis/python-iam/commit/0a23a84142c45922726c3a0718a5993c5ad01604))


### Bug Fixes

* **iam:** bump copyright year to 2020 (via synth) ([#10231](https://www.github.com/googleapis/python-iam/issues/10231)) ([872cc13](https://www.github.com/googleapis/python-iam/commit/872cc1335599384a8f354749dd3fb12d9a130ac5))
* **iam:** deprecate resource name helper methods (via synth) ([#9858](https://www.github.com/googleapis/python-iam/issues/9858)) ([d546df1](https://www.github.com/googleapis/python-iam/commit/d546df13d876eb41ba88e4f4106409638e2a3768))

## 0.2.1

08-23-2019 10:10 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8936](https://github.com/googleapis/google-cloud-python/pull/8936))

### Documentation
- Fix documentation links for iam and error-reporting. ([#9073](https://github.com/googleapis/google-cloud-python/pull/9073))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.2.0

07-24-2019 16:22 PDT


### Implementation Changes
- Remove generate_identity_binding_access_token (via synth). ([#8486](https://github.com/googleapis/google-cloud-python/pull/8486))
- Allow kwargs to be passed to create_channel (via synth). ([#8392](https://github.com/googleapis/google-cloud-python/pull/8392))
- Add routing header to method metadata, format docstrings, update docs configuration (via synth). ([#7595](https://github.com/googleapis/google-cloud-python/pull/7595))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7268](https://github.com/googleapis/google-cloud-python/pull/7268))
- Protoc-generated serialization update. ([#7084](https://github.com/googleapis/google-cloud-python/pull/7084))
- Protoc-generated serialization update. ([#7052](https://github.com/googleapis/google-cloud-python/pull/7052))
- Pick up stub docstring fix in GAPIC generator. ([#6972](https://github.com/googleapis/google-cloud-python/pull/6972))

### New Features
- Add 'client_options' support (via synth).  ([#8511](https://github.com/googleapis/google-cloud-python/pull/8511))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix client lib docs link in README. ([#7813](https://github.com/googleapis/google-cloud-python/pull/7813))
- Update copyright: 2018 -> 2019. ([#7146](https://github.com/googleapis/google-cloud-python/pull/7146))

### Internal / Testing Changes
- Pin black version (via synth). ([#8584](https://github.com/googleapis/google-cloud-python/pull/8584))
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). [#8353](https://github.com/googleapis/google-cloud-python/pull/8353))
- Add disclaimer to auto-generated template files (via synth). ([#8315](https://github.com/googleapis/google-cloud-python/pull/8315))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8242](https://github.com/googleapis/google-cloud-python/pull/8242))
- Fix coverage in 'types.py' (via synth). ([#8154](https://github.com/googleapis/google-cloud-python/pull/8154))
- Blacken noxfile.py, setup.py (via synth). ([#8124](https://github.com/googleapis/google-cloud-python/pull/8124))
- Add empty lines (via synth). ([#8059](https://github.com/googleapis/google-cloud-python/pull/8059))
- Add nox session `docs` (via synth). ([#7772](https://github.com/googleapis/google-cloud-python/pull/7772))
- Copy lintified proto files (via synth). ([#7467](https://github.com/googleapis/google-cloud-python/pull/7467))
- Add clarifying comment to blacken nox target. ([#7393](https://github.com/googleapis/google-cloud-python/pull/7393))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.0

12-13-2018 10:55 PST


### New Features
- Add Client Library for IAM ([#6905](https://github.com/googleapis/google-cloud-python/pull/6905))

### Documentation
- Fix docs build ([#6913](https://github.com/googleapis/google-cloud-python/pull/6913))

### Internal / Testing Changes
- trove classifier fix ([#6922](https://github.com/googleapis/google-cloud-python/pull/6922))
