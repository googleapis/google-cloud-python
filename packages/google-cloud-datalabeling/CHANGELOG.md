# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datalabeling/#history

## [1.1.0](https://www.github.com/googleapis/python-datalabeling/compare/v1.0.0...v1.1.0) (2021-05-28)


### Features

* add common resource helper paths; expose client transport ([#49](https://www.github.com/googleapis/python-datalabeling/issues/49)) ([3d64338](https://www.github.com/googleapis/python-datalabeling/commit/3d643383e481fa22093756343bdf50eba002b1f8))
* add from_service_account_info  ([#65](https://www.github.com/googleapis/python-datalabeling/issues/65)) ([2c99e4f](https://www.github.com/googleapis/python-datalabeling/commit/2c99e4f1ff627cd8c1ddf399c81cb418b3419491))


### Bug Fixes

* **deps:** add packaging requirement ([#100](https://www.github.com/googleapis/python-datalabeling/issues/100)) ([e34e613](https://www.github.com/googleapis/python-datalabeling/commit/e34e613c1b3a7719212224094182309bd267d1bb))
* fix sphinx identifiers ([2c99e4f](https://www.github.com/googleapis/python-datalabeling/commit/2c99e4f1ff627cd8c1ddf399c81cb418b3419491))
* remove client recv msg limit fix: add enums to `types/__init__.py` ([#62](https://www.github.com/googleapis/python-datalabeling/issues/62)) ([19e8f0c](https://www.github.com/googleapis/python-datalabeling/commit/19e8f0c1a82d6b096e0787c1249a2e0cbdf5e429))
* use correct retry deadline ([2c99e4f](https://www.github.com/googleapis/python-datalabeling/commit/2c99e4f1ff627cd8c1ddf399c81cb418b3419491))

## [1.0.0](https://www.github.com/googleapis/python-datalabeling/compare/v0.4.1...v1.0.0) (2020-08-12)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#34)

### Features

* migrate to use microgen ([#34](https://www.github.com/googleapis/python-datalabeling/issues/34)) ([465eb36](https://www.github.com/googleapis/python-datalabeling/commit/465eb361d39d08029f30b36c769252c9f83e7949))

### [0.4.1](https://www.github.com/googleapis/python-datalabeling/compare/v0.4.0...v0.4.1) (2020-08-07)


### Bug Fixes

* update retry configs ([#20](https://www.github.com/googleapis/python-datalabeling/issues/20)) ([b39f497](https://www.github.com/googleapis/python-datalabeling/commit/b39f4975eceee93eec20ccfb0e301e2ff514e023))

## [0.4.0](https://www.github.com/googleapis/python-datalabeling/compare/v0.3.0...v0.4.0) (2020-01-31)


### Features

* **datalabeling:** undeprecate resource name helper methods (via synth) ([#10039](https://www.github.com/googleapis/python-datalabeling/issues/10039)) ([88f8090](https://www.github.com/googleapis/python-datalabeling/commit/88f809008ee6a709c02c78b1d93af779fab19adb))


### Bug Fixes

* **datalabeling:** deprecate resource name helper methods (via synth) ([#9832](https://www.github.com/googleapis/python-datalabeling/issues/9832)) ([e5f9021](https://www.github.com/googleapis/python-datalabeling/commit/e5f902154ebe7fcb139aa405babfe9993fd51319))

## 0.3.0

10-10-2019 11:08 PDT


### Implementation Changes
- Remove send / receive message size limit (via synth). ([#8950](https://github.com/googleapis/google-cloud-python/pull/8950))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 0.2.1

07-16-2019 10:17 PDT


### Implementation Changes
- Import operations.proto (via synth). ([#8678](https://github.com/googleapis/google-cloud-python/pull/8678))

### Documentation
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix links in README.rst. ([#8626](https://github.com/googleapis/google-cloud-python/pull/8626))

## 0.2.0

07-09-2019 12:56 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8386](https://github.com/googleapis/google-cloud-python/pull/8386))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8504](https://github.com/googleapis/google-cloud-python/pull/8504))
- [BREAKING] Remove audio type, add general_data type, blocking_resources (via synth). ([#8459](https://github.com/googleapis/google-cloud-python/pull/8459))

### Documentation
- Update index.rst ([#7764](https://github.com/googleapis/google-cloud-python/pull/7764))

### Internal / Testing Changes
- Pin black version (via synth). ([#8578](https://github.com/googleapis/google-cloud-python/pull/8578))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8348](https://github.com/googleapis/google-cloud-python/pull/8348))
- Add disclaimer to auto-generated template files (via synth). ([#8310](https://github.com/googleapis/google-cloud-python/pull/8310))
- Supress checking 'cov-fail-under' in nox default session (via synth). ([#8236](https://github.com/googleapis/google-cloud-python/pull/8236))
- Fix coverage in 'types.py' (via synth). ([#8151](https://github.com/googleapis/google-cloud-python/pull/8151))
- Blacken noxfile.py, setup.py (via synth). ([#8118](https://github.com/googleapis/google-cloud-python/pull/8118))
- Add empty lines (via synth). ([#8053](https://github.com/googleapis/google-cloud-python/pull/8053))
- Add nox session `docs`, reorder methods (via synth). ([#7767](https://github.com/googleapis/google-cloud-python/pull/7767))

## 0.1.1

04-02-2019 11:29 PDT

### Internal / Testing Changes

- Fix release classifier. ([#7643](https://github.com/googleapis/google-cloud-python/pull/7643))

## 0.1.0

04-01-2019 17:32 PDT

### New Features

- Create Data Labeling Python client. (#7635)
