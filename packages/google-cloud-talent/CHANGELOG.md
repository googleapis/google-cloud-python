# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-talent/#history

## [2.7.0](https://github.com/googleapis/python-talent/compare/v2.6.0...v2.7.0) (2022-07-17)


### Features

* add audience parameter ([37e649c](https://github.com/googleapis/python-talent/commit/37e649cbec6bcc87f71cf4dbb347fa3f3f9e1f87))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#254](https://github.com/googleapis/python-talent/issues/254)) ([37e649c](https://github.com/googleapis/python-talent/commit/37e649cbec6bcc87f71cf4dbb347fa3f3f9e1f87))
* require python 3.7+ ([#264](https://github.com/googleapis/python-talent/issues/264)) ([40cb6db](https://github.com/googleapis/python-talent/commit/40cb6dbb4e7e733d813c0cd77d28e6c9ea5ffc90))
* **v4beta1:** remove Application and Profile services and and related protos, enums, and messages ([37e649c](https://github.com/googleapis/python-talent/commit/37e649cbec6bcc87f71cf4dbb347fa3f3f9e1f87))

## [2.6.0](https://github.com/googleapis/python-talent/compare/v2.5.2...v2.6.0) (2022-06-06)


### Features

* Add a new operator on companyDisplayNames filter to further support fuzzy match by treating input value as a multi word token ([#248](https://github.com/googleapis/python-talent/issues/248)) ([aeab3a0](https://github.com/googleapis/python-talent/commit/aeab3a023ae19f313f7ea8e75d7e48fbb784fbcc))
* Add a new option TELECOMMUTE_JOBS_EXCLUDED under enum TelecommutePreference to completely filter out the telecommute jobs in response ([aeab3a0](https://github.com/googleapis/python-talent/commit/aeab3a023ae19f313f7ea8e75d7e48fbb784fbcc))


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#251](https://github.com/googleapis/python-talent/issues/251)) ([75b11a6](https://github.com/googleapis/python-talent/commit/75b11a6cbb8a872d6766d0aa31d97efc765318cd))


### Documentation

* Deprecate option TELECOMMUTE_EXCLUDED under enum TelecommutePreference ([aeab3a0](https://github.com/googleapis/python-talent/commit/aeab3a023ae19f313f7ea8e75d7e48fbb784fbcc))

### [2.5.2](https://github.com/googleapis/python-talent/compare/v2.5.1...v2.5.2) (2022-03-29)


### Documentation

* Added functionality in the companyDisplayNames filter to support fuzzy matching ([#221](https://github.com/googleapis/python-talent/issues/221)) ([985508c](https://github.com/googleapis/python-talent/commit/985508ce1cdd1050f5d6a7c7b6919408946e4c1d))

### [2.5.1](https://github.com/googleapis/python-talent/compare/v2.5.0...v2.5.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#213](https://github.com/googleapis/python-talent/issues/213)) ([bca14ed](https://github.com/googleapis/python-talent/commit/bca14ed0c94d91dfdf1d4c14715cdb8e8834cebd))

## [2.5.0](https://github.com/googleapis/python-talent/compare/v2.4.0...v2.5.0) (2022-02-11)


### Features

* add api key support ([#197](https://github.com/googleapis/python-talent/issues/197)) ([8109720](https://github.com/googleapis/python-talent/commit/810972062fd7dfbd495a510cfcbe738eb0acc70d))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([#200](https://github.com/googleapis/python-talent/issues/200)) ([36a4f52](https://github.com/googleapis/python-talent/commit/36a4f52b2fc149a8792d90a42c655f7490844d31))

## [2.4.0](https://www.github.com/googleapis/python-talent/compare/v2.3.0...v2.4.0) (2021-11-04)


### Features

* add context manager support in client ([#168](https://www.github.com/googleapis/python-talent/issues/168)) ([04dd991](https://www.github.com/googleapis/python-talent/commit/04dd991f185380bafa81a68e90be19f7bef9e3bc))
* Add new commute methods in Search APIs feat: Add new histogram type 'publish_time_in_day' feat: Support filtering by requisitionId is ListJobs API ([#148](https://www.github.com/googleapis/python-talent/issues/148)) ([3e72647](https://www.github.com/googleapis/python-talent/commit/3e72647c6cf9b69a157bd790a26e5dd915e2056e))
* Added a new `KeywordMatchMode` field to support more keyword matching options feat: Added more `DiversificationLevel` configuration options ([#159](https://www.github.com/googleapis/python-talent/issues/159)) ([4626497](https://www.github.com/googleapis/python-talent/commit/4626497c55596d876f7a63314bc55e2b9330361c))


### Bug Fixes

* add 'dict' annotation type to 'request' ([c0945eb](https://www.github.com/googleapis/python-talent/commit/c0945ebabb75f0cc53c09ce30dce46fd424fa0d4))
* **deps:** drop packaging dependency ([84914d5](https://www.github.com/googleapis/python-talent/commit/84914d54499f677f0db3ee44c74030d5afaead32))
* **deps:** require google-api-core >= 1.28.0 ([84914d5](https://www.github.com/googleapis/python-talent/commit/84914d54499f677f0db3ee44c74030d5afaead32))
* improper types in pagers generation ([31f3a51](https://www.github.com/googleapis/python-talent/commit/31f3a516a1f778dca07ba91dfa14f6010d3f66f1))


### Documentation

* list oneofs in docstring ([84914d5](https://www.github.com/googleapis/python-talent/commit/84914d54499f677f0db3ee44c74030d5afaead32))

## [2.3.0](https://www.github.com/googleapis/python-talent/compare/v2.2.1...v2.3.0) (2021-08-09)


### Features

* bump release level to production/stable ([#102](https://www.github.com/googleapis/python-talent/issues/102)) ([2e63f9b](https://www.github.com/googleapis/python-talent/commit/2e63f9bf6aa2275fdf4d44c4ec8e7135add8df66))

### [2.2.1](https://www.github.com/googleapis/python-talent/compare/v2.2.0...v2.2.1) (2021-07-28)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#133](https://www.github.com/googleapis/python-talent/issues/133)) ([9032d52](https://www.github.com/googleapis/python-talent/commit/9032d52e1f69f1e58e867aa8968d63af1398d36f))
* enable self signed jwt for grpc ([#138](https://www.github.com/googleapis/python-talent/issues/138)) ([95fbb59](https://www.github.com/googleapis/python-talent/commit/95fbb597e2a4b9aac0b0bb0fc920e69b5e04f22b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#134](https://www.github.com/googleapis/python-talent/issues/134)) ([4a4c133](https://www.github.com/googleapis/python-talent/commit/4a4c1337be504d7b45c1a1ec000302472787d409))


### Miscellaneous Chores

* release 2.2.1 ([#139](https://www.github.com/googleapis/python-talent/issues/139)) ([9c15373](https://www.github.com/googleapis/python-talent/commit/9c15373aa362220b20836b6a8fade858f8d41e31))

## [2.2.0](https://www.github.com/googleapis/python-talent/compare/v2.1.0...v2.2.0) (2021-06-30)


### Features

* add `from_service_account_info` ([095747e](https://www.github.com/googleapis/python-talent/commit/095747e8b517769a9caa2df6babf96fd526d0a22))
* add always_use_jwt_access ([#112](https://www.github.com/googleapis/python-talent/issues/112)) ([01c8095](https://www.github.com/googleapis/python-talent/commit/01c8095182503fa8d7ca593f4701f87fe00621ff))


### Bug Fixes

* **deps:** add packaging requirement ([#99](https://www.github.com/googleapis/python-talent/issues/99)) ([c00ab57](https://www.github.com/googleapis/python-talent/commit/c00ab5750a4062b7de24fcba5798171be174f131))
* disable always_use_jwt_access ([a422ac0](https://www.github.com/googleapis/python-talent/commit/a422ac00d270bef6f66d6d29b674505c3a152e33))
* disable always_use_jwt_access ([#115](https://www.github.com/googleapis/python-talent/issues/115)) ([a422ac0](https://www.github.com/googleapis/python-talent/commit/a422ac00d270bef6f66d6d29b674505c3a152e33))
* fix retry deadlines ([#73](https://www.github.com/googleapis/python-talent/issues/73)) ([095747e](https://www.github.com/googleapis/python-talent/commit/095747e8b517769a9caa2df6babf96fd526d0a22))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-talent/issues/1127)) ([#109](https://www.github.com/googleapis/python-talent/issues/109)) ([fe89307](https://www.github.com/googleapis/python-talent/commit/fe89307a7288e02aaeadb4d582a4b0bd7aa1d221)), closes [#1126](https://www.github.com/googleapis/python-talent/issues/1126)

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

* Move API to python microgenerator (#22). See [Migration Guide](https://github.com/googleapis/python-talent/blob/main/UPGRADING.md).

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
