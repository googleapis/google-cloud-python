# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-iam/#history

### [2.6.1](https://github.com/googleapis/python-iam/compare/v2.6.0...v2.6.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#161](https://github.com/googleapis/python-iam/issues/161)) ([9b8fb54](https://github.com/googleapis/python-iam/commit/9b8fb5467236ed61a301a2a86cec860abd0847ff))
* **deps:** require proto-plus>=1.15.0 ([9b8fb54](https://github.com/googleapis/python-iam/commit/9b8fb5467236ed61a301a2a86cec860abd0847ff))

## [2.6.0](https://github.com/googleapis/python-iam/compare/v2.5.1...v2.6.0) (2022-02-26)


### Features

* add api key support ([#147](https://github.com/googleapis/python-iam/issues/147)) ([8145ace](https://github.com/googleapis/python-iam/commit/8145ace353fe863117cf35bd28df1e3dbcd9ba6d))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([4e6e3fc](https://github.com/googleapis/python-iam/commit/4e6e3fca6f4bc1e3764cd2ce2d1a0c760cac0d5f))


### Documentation

* add generated snippets ([#152](https://github.com/googleapis/python-iam/issues/152)) ([a213fdc](https://github.com/googleapis/python-iam/commit/a213fdc92f4feb7777692ad918cb99acaf064b1a))

### [2.5.1](https://www.github.com/googleapis/python-iam/compare/v2.5.0...v2.5.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([ffde276](https://www.github.com/googleapis/python-iam/commit/ffde276b9cc7f988044bed897b30cad957d9ce93))
* **deps:** require google-api-core >= 1.28.0 ([ffde276](https://www.github.com/googleapis/python-iam/commit/ffde276b9cc7f988044bed897b30cad957d9ce93))


### Documentation

* list oneofs in docstring ([ffde276](https://www.github.com/googleapis/python-iam/commit/ffde276b9cc7f988044bed897b30cad957d9ce93))

## [2.5.0](https://www.github.com/googleapis/python-iam/compare/v2.4.0...v2.5.0) (2021-10-14)


### Features

* add support for python 3.10 ([#128](https://www.github.com/googleapis/python-iam/issues/128)) ([28d5a6a](https://www.github.com/googleapis/python-iam/commit/28d5a6aca688f5b59753c95666fafb1cf97f60e2))

## [2.4.0](https://www.github.com/googleapis/python-iam/compare/v2.3.2...v2.4.0) (2021-10-08)


### Features

* add context manager support in client ([#125](https://www.github.com/googleapis/python-iam/issues/125)) ([070897f](https://www.github.com/googleapis/python-iam/commit/070897fd1656ec23bc7da85ef44781d7861f4559))

### [2.3.2](https://www.github.com/googleapis/python-iam/compare/v2.3.1...v2.3.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([96b0b6a](https://www.github.com/googleapis/python-iam/commit/96b0b6ad8af89e0ab2803325f9ff595ce5e3b5b4))

### [2.3.1](https://www.github.com/googleapis/python-iam/compare/v2.3.0...v2.3.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#98](https://www.github.com/googleapis/python-iam/issues/98)) ([4d37f49](https://www.github.com/googleapis/python-iam/commit/4d37f496d529d60443dab2f8812d0859abed3979))
* enable self signed jwt for grpc ([#104](https://www.github.com/googleapis/python-iam/issues/104)) ([d40d70e](https://www.github.com/googleapis/python-iam/commit/d40d70e84a35e00f946a8b30591869a7829b7398))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#99](https://www.github.com/googleapis/python-iam/issues/99)) ([8c0c465](https://www.github.com/googleapis/python-iam/commit/8c0c465225aa7398caa31f50a2ed0788cbc7140e))


### Miscellaneous Chores

* release as 2.3.1 ([#103](https://www.github.com/googleapis/python-iam/issues/103)) ([e5a3d4b](https://www.github.com/googleapis/python-iam/commit/e5a3d4b3951e413db7be208ce853c779ff3d4571))

## [2.3.0](https://www.github.com/googleapis/python-iam/compare/v2.2.0...v2.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#89](https://www.github.com/googleapis/python-iam/issues/89)) ([cc322f9](https://www.github.com/googleapis/python-iam/commit/cc322f9642b8afe847e42ece1cd778ab27c94b72))


### Bug Fixes

* disable always_use_jwt_access ([#93](https://www.github.com/googleapis/python-iam/issues/93)) ([0880d9a](https://www.github.com/googleapis/python-iam/commit/0880d9adc2a7737edae905e3f11b4bd9b6ad5331))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-iam/issues/1127)) ([#84](https://www.github.com/googleapis/python-iam/issues/84)) ([b30f69e](https://www.github.com/googleapis/python-iam/commit/b30f69eec8ade3087652d34013e7a55c05bbe6dd))

## [2.2.0](https://www.github.com/googleapis/python-iam/compare/v2.1.0...v2.2.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([50ca9be](https://www.github.com/googleapis/python-iam/commit/50ca9becf959a2872e8a33b9afc00766dbfaa196))


### Bug Fixes

* add async client to %name_%version/init.py ([50ca9be](https://www.github.com/googleapis/python-iam/commit/50ca9becf959a2872e8a33b9afc00766dbfaa196))
* require google-api-core>=1.22.2 ([#61](https://www.github.com/googleapis/python-iam/issues/61)) ([959b03d](https://www.github.com/googleapis/python-iam/commit/959b03d7c557881e586b29960d3aaaba75b3adbc))
* use correct retry deadlines ([#63](https://www.github.com/googleapis/python-iam/issues/63)) ([1fbdece](https://www.github.com/googleapis/python-iam/commit/1fbdeceee5eba78233b913885be2cbffc3ca7904))

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

* migrate to microgenerator (#26). See the [migration guide](https://github.com/googleapis/python-iam/blob/main/UPGRADING.md).

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
