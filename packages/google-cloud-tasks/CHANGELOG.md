# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-tasks/#history

## [2.10.0](https://github.com/googleapis/python-tasks/compare/v2.9.1...v2.10.0) (2022-07-16)


### Features

* add audience parameter ([ad01839](https://github.com/googleapis/python-tasks/commit/ad0183951c7f1a23738004a11144b3870a91842e))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#277](https://github.com/googleapis/python-tasks/issues/277)) ([239789d](https://github.com/googleapis/python-tasks/commit/239789da46254961a27a51837441ff2035423c14))
* require python 3.7+ ([#275](https://github.com/googleapis/python-tasks/issues/275)) ([85fd179](https://github.com/googleapis/python-tasks/commit/85fd179fda7556e9a1568ff93a4b5dd22ec01036))

## [2.9.1](https://github.com/googleapis/python-tasks/compare/v2.9.0...v2.9.1) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#262](https://github.com/googleapis/python-tasks/issues/262)) ([db23558](https://github.com/googleapis/python-tasks/commit/db23558d053d56ff84a4447f7af2525ff4459309))


### Documentation

* fix changelog header to consistent size ([#263](https://github.com/googleapis/python-tasks/issues/263)) ([048d907](https://github.com/googleapis/python-tasks/commit/048d907b1929f2ced1dc1d1b3536f38265994330))

## [2.9.0](https://github.com/googleapis/python-tasks/compare/v2.8.1...v2.9.0) (2022-05-05)


### Features

* AuditConfig for IAM v1 ([7b7a294](https://github.com/googleapis/python-tasks/commit/7b7a2946a8554a06d8fdc57b13c2726c5d8a443b))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([7b7a294](https://github.com/googleapis/python-tasks/commit/7b7a2946a8554a06d8fdc57b13c2726c5d8a443b))


### Documentation

* fix type in docstring for map fields ([7b7a294](https://github.com/googleapis/python-tasks/commit/7b7a2946a8554a06d8fdc57b13c2726c5d8a443b))

## [2.8.1](https://github.com/googleapis/python-tasks/compare/v2.8.0...v2.8.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#232](https://github.com/googleapis/python-tasks/issues/232)) ([2b35888](https://github.com/googleapis/python-tasks/commit/2b3588834794ce7ac6d5c762f2d45849122ddc1b))
* **deps:** require proto-plus>=1.15.0 ([2b35888](https://github.com/googleapis/python-tasks/commit/2b3588834794ce7ac6d5c762f2d45849122ddc1b))

## [2.8.0](https://github.com/googleapis/python-tasks/compare/v2.7.2...v2.8.0) (2022-02-14)


### Features

* add api key support ([#214](https://github.com/googleapis/python-tasks/issues/214)) ([ce21598](https://github.com/googleapis/python-tasks/commit/ce215987f969cbc6347fb58cd2163394a6fc7f1c))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([8dd8aec](https://github.com/googleapis/python-tasks/commit/8dd8aec79d2302007e3f9511daeab817f05d2aa6))

## [2.7.2](https://www.github.com/googleapis/python-tasks/compare/v2.7.1...v2.7.2) (2022-01-08)


### Documentation

* fix docstring formatting ([#196](https://www.github.com/googleapis/python-tasks/issues/196)) ([e7a3461](https://www.github.com/googleapis/python-tasks/commit/e7a3461a34229c210e63590370fa6eee4d06630a))

## [2.7.1](https://www.github.com/googleapis/python-tasks/compare/v2.7.0...v2.7.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([72f150f](https://www.github.com/googleapis/python-tasks/commit/72f150fe39313173ac6c02616b6ca4466f5855fe))
* **deps:** require google-api-core >= 1.28.0 ([72f150f](https://www.github.com/googleapis/python-tasks/commit/72f150fe39313173ac6c02616b6ca4466f5855fe))


### Documentation

* list oneofs in docstring ([72f150f](https://www.github.com/googleapis/python-tasks/commit/72f150fe39313173ac6c02616b6ca4466f5855fe))

## [2.7.0](https://www.github.com/googleapis/python-tasks/compare/v2.6.0...v2.7.0) (2021-10-15)


### Features

* add support for python 3.10 ([#181](https://www.github.com/googleapis/python-tasks/issues/181)) ([0a40ab0](https://www.github.com/googleapis/python-tasks/commit/0a40ab01070018fc3ca32008f55c18e2b65aa23b))

## [2.6.0](https://www.github.com/googleapis/python-tasks/compare/v2.5.3...v2.6.0) (2021-10-08)


### Features

* add context manager support in client ([#173](https://www.github.com/googleapis/python-tasks/issues/173)) ([ceec8f1](https://www.github.com/googleapis/python-tasks/commit/ceec8f173af696d26cf367af2d969bf98987df2a))

## [2.6.0](https://www.github.com/googleapis/python-tasks/compare/v2.5.3...v2.6.0) (2021-10-07)


### Features

* add context manager support in client ([#173](https://www.github.com/googleapis/python-tasks/issues/173)) ([ceec8f1](https://www.github.com/googleapis/python-tasks/commit/ceec8f173af696d26cf367af2d969bf98987df2a))

## [2.5.3](https://www.github.com/googleapis/python-tasks/compare/v2.5.2...v2.5.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([0feec1e](https://www.github.com/googleapis/python-tasks/commit/0feec1e0d1e4847e2722920c8afdc597ecd92e3f))

## [2.5.2](https://www.github.com/googleapis/python-tasks/compare/v2.5.1...v2.5.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([42d768b](https://www.github.com/googleapis/python-tasks/commit/42d768b9f302aef3258f4abc413199070bcd2a8d))

## [2.5.1](https://www.github.com/googleapis/python-tasks/compare/v2.5.0...v2.5.1) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc chore: use gapic-generator-python 0.50.5 ([#143](https://www.github.com/googleapis/python-tasks/issues/143)) ([b8ec21e](https://www.github.com/googleapis/python-tasks/commit/b8ec21e2d3bc173249a33f34b27373e0f6c08cd2))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#135](https://www.github.com/googleapis/python-tasks/issues/135)) ([ccfc32d](https://www.github.com/googleapis/python-tasks/commit/ccfc32d56c5d0750a8f14ce244e1bc40eb4e31bd))


### Miscellaneous Chores

* release as 2.5.1 ([#144](https://www.github.com/googleapis/python-tasks/issues/144)) ([28ffe6b](https://www.github.com/googleapis/python-tasks/commit/28ffe6b149fd1267c967a8432ef41042620c314e))

## [2.5.0](https://www.github.com/googleapis/python-tasks/compare/v2.4.0...v2.5.0) (2021-07-21)


### Features

* Set `audience` field in authenticated HTTP task example ([#138](https://www.github.com/googleapis/python-tasks/issues/138)) ([7a5a0c6](https://www.github.com/googleapis/python-tasks/commit/7a5a0c6ca5372035521d5366373054a7ba95f2bd))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#134](https://www.github.com/googleapis/python-tasks/issues/134)) ([fd3cb31](https://www.github.com/googleapis/python-tasks/commit/fd3cb31bc1d36e5b6373bfa3d3bb9bb65aeb3f90))

## [2.4.0](https://www.github.com/googleapis/python-tasks/compare/v2.3.0...v2.4.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#122](https://www.github.com/googleapis/python-tasks/issues/122)) ([87c9ccc](https://www.github.com/googleapis/python-tasks/commit/87c9cccb42237eb421c72411652985a7fbe1c16a))


### Bug Fixes

* disable always_use_jwt_access ([#126](https://www.github.com/googleapis/python-tasks/issues/126)) ([54d2286](https://www.github.com/googleapis/python-tasks/commit/54d2286b153c36b7a50b5a936517aa59e10ad27c))
* update sample for task name ([#120](https://www.github.com/googleapis/python-tasks/issues/120)) ([b1be2de](https://www.github.com/googleapis/python-tasks/commit/b1be2de174fc37d0eb90bbf877851c11ddb14907))


### Documentation

* omit mention of Python 2.7 in CONTRIBUTING.rst ([#116](https://www.github.com/googleapis/python-tasks/issues/116)) ([0732ab7](https://www.github.com/googleapis/python-tasks/commit/0732ab7d726fdf564897fad009f8a5da45b5c017)), closes [#1126](https://www.github.com/googleapis/python-tasks/issues/1126)

## [2.3.0](https://www.github.com/googleapis/python-tasks/compare/v2.2.0...v2.3.0) (2021-05-28)


### Features

* add `from_service_account_info` ([#80](https://www.github.com/googleapis/python-tasks/issues/80)) ([2498225](https://www.github.com/googleapis/python-tasks/commit/2498225112ddb4b112b387dec71631c29a6db71e))
* support self-signed JWT flow for service accounts ([1acf20c](https://www.github.com/googleapis/python-tasks/commit/1acf20ca440a5396ee03205b5c2301b84e368926))


### Bug Fixes

* add async client to %name_%version/init.py ([1acf20c](https://www.github.com/googleapis/python-tasks/commit/1acf20ca440a5396ee03205b5c2301b84e368926))
* use correct retry deadlines ([2498225](https://www.github.com/googleapis/python-tasks/commit/2498225112ddb4b112b387dec71631c29a6db71e))


### Documentation

* fix grammar in documentation ([#112](https://www.github.com/googleapis/python-tasks/issues/112)) ([6f93a19](https://www.github.com/googleapis/python-tasks/commit/6f93a190311bd5468827496685072388a951e670))

## [2.2.0](https://www.github.com/googleapis/python-tasks/compare/v2.1.0...v2.2.0) (2021-02-24)


### Features

* add from_service_account_info method to clients ([e1fdc76](https://www.github.com/googleapis/python-tasks/commit/e1fdc76f5369e53067a1748aecce9fa3940d9ee1))
* **v2beta3, v2beta2:** introducing fields: ListQueuesRequest.read_mask, GetQueueRequest.read_mask, Queue.task_ttl, Queue.tombstone_ttl, Queue.stats and introducing messages: QueueStats ([e1fdc76](https://www.github.com/googleapis/python-tasks/commit/e1fdc76f5369e53067a1748aecce9fa3940d9ee1))


### Bug Fixes

* remove client recv msg limit fix: add enums to `types/__init__.py` ([#56](https://www.github.com/googleapis/python-tasks/issues/56)) ([6a5bfaf](https://www.github.com/googleapis/python-tasks/commit/6a5bfaf63b46567897c36907772b10ea4b0dff43))
* Update sample comments ([#58](https://www.github.com/googleapis/python-tasks/issues/58)) ([3eb30b3](https://www.github.com/googleapis/python-tasks/commit/3eb30b349b9092a2a2fb08116855139418ebd371))


### Documentation

* fix type references in docstrings ([e1fdc76](https://www.github.com/googleapis/python-tasks/commit/e1fdc76f5369e53067a1748aecce9fa3940d9ee1))
* **v2beta2:** updates to AppEngineHttpRequest description ([e1fdc76](https://www.github.com/googleapis/python-tasks/commit/e1fdc76f5369e53067a1748aecce9fa3940d9ee1))
* **v2beta3:** updates to max burst size description ([e1fdc76](https://www.github.com/googleapis/python-tasks/commit/e1fdc76f5369e53067a1748aecce9fa3940d9ee1))

## [2.1.0](https://www.github.com/googleapis/python-tasks/compare/v2.0.0...v2.1.0) (2020-12-07)


### Features

* add common resource helpers; expose client transport; add shebang to fixup scripts ([#34](https://www.github.com/googleapis/python-tasks/issues/34)) ([511e9f3](https://www.github.com/googleapis/python-tasks/commit/511e9f3d5da4c8b86adca8bddc65dc37a989edcf))

## [2.0.0](https://www.github.com/googleapis/python-tasks/compare/v1.5.0...v2.0.0) (2020-09-02)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#38)

### Features

* introduce field Queue.type; update default retry configs ([#29](https://www.github.com/googleapis/python-tasks/issues/29)) ([6b8ba85](https://www.github.com/googleapis/python-tasks/commit/6b8ba85de5998b0c2138bbf771fa16ba8f9bbf07))
* migrate to use microgen ([#38](https://www.github.com/googleapis/python-tasks/issues/38)) ([18e146c](https://www.github.com/googleapis/python-tasks/commit/18e146cab5e2b669538ca6b1d58603e72d58ae88))


### Documentation

* add samples from python-docs-samples/tasks ([#36](https://www.github.com/googleapis/python-tasks/issues/36)) ([9d022f7](https://www.github.com/googleapis/python-tasks/commit/9d022f736912df8a0f4d13e2a98dd53cf506f2dc)), closes [#1068](https://www.github.com/googleapis/python-tasks/issues/1068) [#1116](https://www.github.com/googleapis/python-tasks/issues/1116) [#1133](https://www.github.com/googleapis/python-tasks/issues/1133) [#1186](https://www.github.com/googleapis/python-tasks/issues/1186) [#1217](https://www.github.com/googleapis/python-tasks/issues/1217) [#1254](https://www.github.com/googleapis/python-tasks/issues/1254) [#1271](https://www.github.com/googleapis/python-tasks/issues/1271) [#1288](https://www.github.com/googleapis/python-tasks/issues/1288) [#1309](https://www.github.com/googleapis/python-tasks/issues/1309) [#1311](https://www.github.com/googleapis/python-tasks/issues/1311) [#1329](https://www.github.com/googleapis/python-tasks/issues/1329) [#1320](https://www.github.com/googleapis/python-tasks/issues/1320) [#1355](https://www.github.com/googleapis/python-tasks/issues/1355) [#1359](https://www.github.com/googleapis/python-tasks/issues/1359) [#1529](https://www.github.com/googleapis/python-tasks/issues/1529) [#1532](https://www.github.com/googleapis/python-tasks/issues/1532) [#1541](https://www.github.com/googleapis/python-tasks/issues/1541) [#1563](https://www.github.com/googleapis/python-tasks/issues/1563) [#1552](https://www.github.com/googleapis/python-tasks/issues/1552) [#1566](https://www.github.com/googleapis/python-tasks/issues/1566) [#1698](https://www.github.com/googleapis/python-tasks/issues/1698) [#2114](https://www.github.com/googleapis/python-tasks/issues/2114) [#2113](https://www.github.com/googleapis/python-tasks/issues/2113) [#2156](https://www.github.com/googleapis/python-tasks/issues/2156) [#2208](https://www.github.com/googleapis/python-tasks/issues/2208) [#2250](https://www.github.com/googleapis/python-tasks/issues/2250) [#2316](https://www.github.com/googleapis/python-tasks/issues/2316) [#2187](https://www.github.com/googleapis/python-tasks/issues/2187) [#2439](https://www.github.com/googleapis/python-tasks/issues/2439) [#2516](https://www.github.com/googleapis/python-tasks/issues/2516) [#2543](https://www.github.com/googleapis/python-tasks/issues/2543) [#2700](https://www.github.com/googleapis/python-tasks/issues/2700) [#3168](https://www.github.com/googleapis/python-tasks/issues/3168) [#3171](https://www.github.com/googleapis/python-tasks/issues/3171)

## [1.5.0](https://www.github.com/googleapis/python-tasks/compare/v1.4.0...v1.5.0) (2020-02-24)


### Features

* **tasks:** add support for stackdriver logging config; update retry config (via synth) ([#8](https://www.github.com/googleapis/python-tasks/issues/8)) ([70b597a](https://www.github.com/googleapis/python-tasks/commit/70b597a615c75976a4993ab223328d7cba3bd139))

## [1.4.0](https://www.github.com/googleapis/python-tasks/compare/v1.3.0...v1.4.0) (2020-02-06)


### Features

* **tasks:** undeprecate resource helper methods; add py2 deprecation warning; change default timeouts; add 3.8 tests; edit docstrings (via synth)([#10074](https://www.github.com/googleapis/python-tasks/issues/10074)) ([5577817](https://www.github.com/googleapis/python-tasks/commit/5577817fbe6435af03d862761fa08288b02cc69a))


### Bug Fixes

* **tasks:** change default timeout values; bump copyright year to 2020; change line breaks in docstrings (via synth) ([#10271](https://www.github.com/googleapis/python-tasks/issues/10271)) ([f68536d](https://www.github.com/googleapis/python-tasks/commit/f68536d95b6e320e4140d6720cc0c47c184dd694))
* **tasks:** deprecate resource name helper methods (via synth) ([#9864](https://www.github.com/googleapis/python-tasks/issues/9864)) ([ccf2cab](https://www.github.com/googleapis/python-tasks/commit/ccf2cabbe32d91988bd9456dc777622182beb658))

## 1.3.0

11-04-2019 10:06 PST

### Implementation Changes
- Add proto annotations (via synth) ([#9352](https://github.com/googleapis/google-cloud-python/pull/9352))

### New Features
- Add HTTP tasks, OAuth tokens, and OIDC tokens (via synth) ([#9588](https://github.com/googleapis/google-cloud-python/pull/9588))

### Documentation
- Tweak docstrings (via synth) ([#9433](https://github.com/googleapis/google-cloud-python/pull/9433))
- Disambiguate client requests from cloud task requests ([#9398](https://github.com/googleapis/google-cloud-python/pull/9398))
- Change requests intersphinx url (via synth) ([#9409](https://github.com/googleapis/google-cloud-python/pull/9409))
- Update documentation (via synth) ([#9069](https://github.com/googleapis/google-cloud-python/pull/9069))
- Remove compatibility badges from READMEs ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 1.2.1

08-12-2019 13:50 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8971](https://github.com/googleapis/google-cloud-python/pull/8971))

### Documentation
- Fix links to googleapis.dev ([#8998](https://github.com/googleapis/google-cloud-python/pull/8998))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.2.0

07-24-2019 17:41 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8406](https://github.com/googleapis/google-cloud-python/pull/8406))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8660](https://github.com/googleapis/google-cloud-python/pull/8660))
- Add 'client_options' support, update list method docstrings (via synth). ([#8524](https://github.com/googleapis/google-cloud-python/pull/8524))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation

- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix typo in README. ([#8606](https://github.com/googleapis/google-cloud-python/pull/8606))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8366](https://github.com/googleapis/google-cloud-python/pull/8366))
- Add disclaimer to auto-generated template files (via synth).  ([#8330](https://github.com/googleapis/google-cloud-python/pull/8330))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8254](https://github.com/googleapis/google-cloud-python/pull/8254))
- Fix coverage in 'types.py' (via synth). ([#8166](https://github.com/googleapis/google-cloud-python/pull/8166))
- Blacken noxfile.py, setup.py (via synth). ([#8134](https://github.com/googleapis/google-cloud-python/pull/8134))
- Add empty lines (via synth). ([#8074](https://github.com/googleapis/google-cloud-python/pull/8074))

## 1.1.0

05-14-2019 15:30 PDT

### Implementation Changes
- Remove log_sampling_ratio, add stackdriver_logging_config (via synth). ([#7950](https://github.com/googleapis/google-cloud-python/pull/7950))

### Documentation
- Update docstrings (via synth). ([#7963](https://github.com/googleapis/google-cloud-python/pull/7963))
- Update docstrings (via synth). ([#7940](https://github.com/googleapis/google-cloud-python/pull/7940))

### Internal / Testing Changes
- Add nox session `docs`, reorder methods (via synth). ([#7783](https://github.com/googleapis/google-cloud-python/pull/7783))

## 1.0.0

04-29-2019 16:35 PDT

### Documentation
- Correct docs/index.rst. ([#7808](https://github.com/googleapis/google-cloud-python/pull/7808))

### Internal / Testing Changes
- Add smoke test. ([#7808](https://github.com/googleapis/google-cloud-python/pull/7808))

## 0.7.0

04-15-2019 10:21 PDT


### New Features
- Add auth and stackdriver logging configuration (via synth). ([#7666](https://github.com/googleapis/google-cloud-python/pull/7666))

### Documentation
- Tasks: Format docstrings for enums (via synth). ([#7601](https://github.com/googleapis/google-cloud-python/pull/7601))

## 0.6.0

03-26-2019 13:35 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Generate v2. ([#7547](https://github.com/googleapis/google-cloud-python/pull/7547))

## 0.5.0

03-06-2019 15:03 PST


### Implementation Changes
- Remove unused message exports (via synth). ([#7276](https://github.com/googleapis/google-cloud-python/pull/7276))
- Protoc-generated serialization update. ([#7096](https://github.com/googleapis/google-cloud-python/pull/7096))

### New Features
- Add 'Task.http_request' and associated message type (via synth). ([#7432](https://github.com/googleapis/google-cloud-python/pull/7432))
- Add 'Task.dispatch_deadline' via synth. ([#7211](https://github.com/googleapis/google-cloud-python/pull/7211))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Restore expanded example from PR [#7025](https://github.com/googleapis/google-cloud-python/pull/7025) after synth. ([#7062](https://github.com/googleapis/google-cloud-python/pull/7062))
- Add working example for 'create_queue'. ([#7025](https://github.com/googleapis/google-cloud-python/pull/7025))
- Pick up stub docstring fix in GAPIC generator. ([#6983](https://github.com/googleapis/google-cloud-python/pull/6983))

### Internal / Testing Changes
- Copy lintified proto files (via synth). ([#7471](https://github.com/googleapis/google-cloud-python/pull/7471))
- Add clarifying comment to blacken nox target. ([#7405](https://github.com/googleapis/google-cloud-python/pull/7405))
- Copy proto files alongside protoc versions
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.4.0

12-18-2018 09:50 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6616](https://github.com/googleapis/google-cloud-python/pull/6616))
- Fix `client_info` bug, update docstrings and timeouts. ([#6422](https://github.com/googleapis/google-cloud-python/pull/6422))
- Re-generate library using tasks/synth.py ([#5980](https://github.com/googleapis/google-cloud-python/pull/5980))

### New Features
- Pick up changes to GAPIC generator, drop 'Code' enum. ([#6509](https://github.com/googleapis/google-cloud-python/pull/6509))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Separate / distinguish API docs for different API versions. ([#6306](https://github.com/googleapis/google-cloud-python/pull/6306))
- Docstring tweaks from protos. ([#6261](https://github.com/googleapis/google-cloud-python/pull/6261))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Remove autosynth / tweaks for 'README.rst' / 'setup.py'. ([#5957](https://github.com/googleapis/google-cloud-python/pull/5957))
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
- Don't update nox in 'tasks/synth.py'. ([#6232](https://github.com/googleapis/google-cloud-python/pull/6232))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.3.0

### Implementation Changes
- Regenerate tasks to fix API enablement URL (#5579)

### New Features
- Tasks: Add v2beta3 endpoint (#5880)

### Documentation
- update Task library doc link (#5708)
- tasks missing from docs (#5656)

## 0.2.0

### Implementation Changes
- regenerate tasks v2beta2 (#5469)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

## 0.1.0

### New Features
- Add v2beta2 endpoint for Tasks
