# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-talent/#history

## [2.1.0](https://www.github.com/googleapis/python-talent/compare/v2.0.0...v2.1.0) (2021-02-11)


### Features

* add common resource helper methods; expose client transport remove gRPC send/recv limits ([#57](https://www.github.com/googleapis/python-talent/issues/57)) ([6f17871](https://www.github.com/googleapis/python-talent/commit/6f17871a73d2112b5792ad87bf4a2d0e25beb03e))

## [2.0.0](https://www.github.com/googleapis/python-talent/compare/v1.0.0...v2.0.0) (2020-10-02)


### ⚠ BREAKING CHANGES

* remove WALKING and CYCLING from v4 commute methods (#37)

### Bug Fixes

* remove WALKING and CYCLING from v4 commute methods ([#37](https://www.github.com/googleapis/python-talent/issues/37)) ([e239d24](https://www.github.com/googleapis/python-talent/commit/e239d24bdd3ff94cfc759da3e58fbf6a377af015))

## [1.0.0](https://www.github.com/googleapis/python-talent/compare/v0.6.1...v1.0.0) (2020-09-28)


### ⚠ BREAKING CHANGES

* Move API to python microgenerator (#22). See [Migration Guide](https://github.com/googleapis/python-talent/blob/master/UPGRADING.md).

### Features

* add v4 ([#29](https://www.github.com/googleapis/python-talent/issues/29)) ([80bef1f](https://www.github.com/googleapis/python-talent/commit/80bef1f07d38785aa1dc32a66e34d54d3ef04591))
* move API to python microgenerator ([#22](https://www.github.com/googleapis/python-talent/issues/22)) ([fb361bb](https://www.github.com/googleapis/python-talent/commit/fb361bbde03edc6ab0d3bc0f83d0af61c4f783d5))


### Bug Fixes

* update default retry configs ([#17](https://www.github.com/googleapis/python-talent/issues/17)) ([a0e8ddc](https://www.github.com/googleapis/python-talent/commit/a0e8ddcb5706da9b470f4f5962a7a9cf3bd09f0a))

### [0.6.1](https://www.github.com/googleapis/python-talent/compare/v0.6.0...v0.6.1) (2020-04-28)


### Bug Fixes

* increase default timeout; update templates (via synth) ([#11](https://www.github.com/googleapis/python-talent/issues/11)) ([0bf35f5](https://www.github.com/googleapis/python-talent/commit/0bf35f54ce026613fc7c2a1772d983866291d09a))

## [0.6.0](https://www.github.com/googleapis/python-talent/compare/v0.5.0...v0.6.0) (2020-03-18)


### Features

* bump library release_status to beta ([#6](https://www.github.com/googleapis/python-talent/issues/6)) ([2f1321d](https://www.github.com/googleapis/python-talent/commit/2f1321d1a9c76ca53fded6487d36e5496ed3d23c))

## [0.5.0](https://www.github.com/googleapis/python-talent/compare/v0.4.0...v0.5.0) (2020-02-03)


### Features

* **talent:** add `query_language_code` to `talent.v4beta1.JobQuery` (via synth) ([#9571](https://www.github.com/googleapis/python-talent/issues/9571)) ([fdcc4ce](https://www.github.com/googleapis/python-talent/commit/fdcc4ce17b1ba3a784984e70ec4bcd04ed5554d2))
* **talent:** undeprecate resource name helpers, add 2.7 sunset warning (via synth)  ([#10050](https://www.github.com/googleapis/python-talent/issues/10050)) ([1c6e3ee](https://www.github.com/googleapis/python-talent/commit/1c6e3eee6b4d4d0004ffb38d4fde69f147bbd969))


### Bug Fixes

* **speech:** re-add unused speaker_tag; update spacing in docs templates (via synth) ([#9766](https://www.github.com/googleapis/python-talent/issues/9766)) ([27e23ca](https://www.github.com/googleapis/python-talent/commit/27e23ca47d753983732d5a20e6fe2052c14c2a92))
* **talent:** change default timeout values; edit docstrings; bump copyright year to 2020 (via synth) ([#10239](https://www.github.com/googleapis/python-talent/issues/10239)) ([d7daa22](https://www.github.com/googleapis/python-talent/commit/d7daa2283d83ce959f010998ab2c44402f573293))
* **talent:** deprecate resource name helper methods (via synth) ([#9844](https://www.github.com/googleapis/python-talent/issues/9844)) ([56c7a87](https://www.github.com/googleapis/python-talent/commit/56c7a8796510b75242e4d5863be907b484e75578))

## 0.4.0

10-04-2019 14:29 PDT

### Implementation Changes
- Move `BatchOperationMetadata` / `JobOperationResult` messages to new protobuf files (via synth). ([#9129](https://github.com/googleapis/google-cloud-python/pull/9129))
- Import batch proto (via synth).  ([#9062](https://github.com/googleapis/google-cloud-python/pull/9062))
- Remove send / receive message size limit (via synth). ([#8970](https://github.com/googleapis/google-cloud-python/pull/8970))

### New Features
- Deprecate `candidate_availability_filter` for `availability_filters`, add `AvailabilitySignalType`, add fields to `update_profile` (via synth). ([#9256](https://github.com/googleapis/google-cloud-python/pull/9256))
- Add `applications` / `assignments` fields to `Profile` message (via synth). ([#9229](https://github.com/googleapis/google-cloud-python/pull/9229))
- Add `filter_` arg to `ProfileServiceClient.list_profiles`; docstring updates (via synth). ([#9223](https://github.com/googleapis/google-cloud-python/pull/9223))
- Deprecate job visibility (via synth). ([#9050](https://github.com/googleapis/google-cloud-python/pull/9050))
- Document additional fields allowed in profile update mask (via synth). ([#9000](https://github.com/googleapis/google-cloud-python/pull/9000))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update docstrings (via synth). ([#8986](https://github.com/googleapis/google-cloud-python/pull/8986))

### Internal / Testing Changes
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.3.0

07-24-2019 17:36 PDT


### Implementation Changes
- Return iterable of `SummarizedProfile` from `search_profiles` rather than`HistogramQueryResult` (via synth). ([#7962](https://github.com/googleapis/google-cloud-python/pull/7962))

### New Features
- Add strict keywords search, increase timeout (via synth). ([#8712](https://github.com/googleapis/google-cloud-python/pull/8712))
- Add path-construction helpers to GAPIC clients (via synth). ([#8632](https://github.com/googleapis/google-cloud-python/pull/8632))
- Add 'result_set_id' param to 'ProfileSearchClient.search_profiles'; add 'ProfileQuery.candidate_availability_filter'; pin 'black' version; dostring tweaks (via synth). ([#8597](https://github.com/googleapis/google-cloud-python/pull/8597))
- Add 'client_options' support, update list method docstrings (via synth). ([#8523](https://github.com/googleapis/google-cloud-python/pull/8523))
- Add 'batch_create_jobs' and 'batch_update_jobs' (via synth). ([#8189](https://github.com/googleapis/google-cloud-python/pull/8189))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Allow kwargs to be passed to create_channel (via synth). ([#8405](https://github.com/googleapis/google-cloud-python/pull/8405))
- Declare encoding as utf-8 in pb2 files (via synth).([#8365](https://github.com/googleapis/google-cloud-python/pull/8365))
- Add disclaimer to auto-generated template files (via synth). ([#8329](https://github.com/googleapis/google-cloud-python/pull/8329))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8253](https://github.com/googleapis/google-cloud-python/pull/8253))
- Fix coverage in 'types.py' (via synth). ([#8165](https://github.com/googleapis/google-cloud-python/pull/8165))
- Blacken noxfile.py, setup.py (via synth).([#8133](https://github.com/googleapis/google-cloud-python/pull/8133))
- Add empty lines (via synth). ([#8073](https://github.com/googleapis/google-cloud-python/pull/8073))

## 0.2.0

05-09-2019 12:25 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Regenerate talent (via synth). ([#7861](https://github.com/googleapis/google-cloud-python/pull/7861))

### Documentation
- Fixed broken talent client library documentation link ([#7546](https://github.com/googleapis/google-cloud-python/pull/7546))
- Fix link in docstring.([#7508](https://github.com/googleapis/google-cloud-python/pull/7508))
- Documentation and formatting changes. ([#7489](https://github.com/googleapis/google-cloud-python/pull/7489))

## 0.1.0

03-05-2019 12:50 PST

- Initial release of google-cloud-talent
