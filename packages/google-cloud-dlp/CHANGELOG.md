# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dlp/#history

## [3.8.0](https://github.com/googleapis/python-dlp/compare/v3.7.1...v3.8.0) (2022-07-16)


### Features

* add audience parameter ([6a3d7ec](https://github.com/googleapis/python-dlp/commit/6a3d7ec17783fd6b3486b2bd5a04cb33d65acb3e))
* InfoType categories were added to built-in infoTypes ([#409](https://github.com/googleapis/python-dlp/issues/409)) ([6a3d7ec](https://github.com/googleapis/python-dlp/commit/6a3d7ec17783fd6b3486b2bd5a04cb33d65acb3e))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([6a3d7ec](https://github.com/googleapis/python-dlp/commit/6a3d7ec17783fd6b3486b2bd5a04cb33d65acb3e))
* require python 3.7+ ([#411](https://github.com/googleapis/python-dlp/issues/411)) ([232001d](https://github.com/googleapis/python-dlp/commit/232001d2c15731c20d2b98f837906799b35309b6))

## [3.7.1](https://github.com/googleapis/python-dlp/compare/v3.7.0...v3.7.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#395](https://github.com/googleapis/python-dlp/issues/395)) ([d8760a1](https://github.com/googleapis/python-dlp/commit/d8760a12f4d566cb64df4e4aec3641cb6aa8e588))
* drop dependency pytz ([d8760a1](https://github.com/googleapis/python-dlp/commit/d8760a12f4d566cb64df4e4aec3641cb6aa8e588))


### Documentation

* fix changelog header to consistent size ([#396](https://github.com/googleapis/python-dlp/issues/396)) ([d09ac69](https://github.com/googleapis/python-dlp/commit/d09ac693f6b356bf5da1e26e522168bc2376872e))

## [3.7.0](https://github.com/googleapis/python-dlp/compare/v3.6.2...v3.7.0) (2022-05-12)


### Features

* add DataProfilePubSubMessage supporting pub/sub integration ([#363](https://github.com/googleapis/python-dlp/issues/363)) ([15a4653](https://github.com/googleapis/python-dlp/commit/15a4653426b2a614a22152ca0a4b457fd8696d3a))
* new Bytes and File types POWERPOINT and EXCEL ([#355](https://github.com/googleapis/python-dlp/issues/355)) ([be8c8b1](https://github.com/googleapis/python-dlp/commit/be8c8b145d8ecad24a9c56f4ab26520700b157a8))

## [3.6.2](https://github.com/googleapis/python-dlp/compare/v3.6.1...v3.6.2) (2022-03-05)


### Bug Fixes

* **deps:** require proto-plus>=1.15.0 ([#342](https://github.com/googleapis/python-dlp/issues/342)) ([81ae7b6](https://github.com/googleapis/python-dlp/commit/81ae7b6c25071f18c356b62d2df4234f43fe1fec))

## [3.6.1](https://github.com/googleapis/python-dlp/compare/v3.6.0...v3.6.1) (2022-02-26)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([#325](https://github.com/googleapis/python-dlp/issues/325)) ([676f1d7](https://github.com/googleapis/python-dlp/commit/676f1d76158c6c0951e75362d5eb34f57d901712))


### Documentation

* **dlp-samples:** modified region tags and fixed comment ([#330](https://github.com/googleapis/python-dlp/issues/330)) ([6375f90](https://github.com/googleapis/python-dlp/commit/6375f90805c5e30c995c47d1538fb08882afb518))

## [3.6.0](https://github.com/googleapis/python-dlp/compare/v3.5.0...v3.6.0) (2022-01-26)


### Features

* add api key support ([#320](https://github.com/googleapis/python-dlp/issues/320)) ([ac2fe87](https://github.com/googleapis/python-dlp/commit/ac2fe8702b31f687935938b9fb089953e9a3af48))


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >2.3.0 ([#322](https://github.com/googleapis/python-dlp/issues/322)) ([24d07e3](https://github.com/googleapis/python-dlp/commit/24d07e3af30b694b4b73b40fb2a5f19c276d6d98))

## [3.5.0](https://github.com/googleapis/python-dlp/compare/v3.4.0...v3.5.0) (2022-01-16)


### Features

* add support for Python 3.9 / 3.10 ([#300](https://github.com/googleapis/python-dlp/issues/300)) ([ac58bde](https://github.com/googleapis/python-dlp/commit/ac58bde1f9d361f56ecf942319d1c427159a02e9))

## [3.4.0](https://www.github.com/googleapis/python-dlp/compare/v3.3.1...v3.4.0) (2021-12-03)


### Features

* added deidentify replacement dictionaries ([#296](https://www.github.com/googleapis/python-dlp/issues/296)) ([63e9661](https://www.github.com/googleapis/python-dlp/commit/63e96614ba72e4ae8e0eafe4139d5329e75a3c18))
* added field for BigQuery inspect template inclusion lists ([63e9661](https://www.github.com/googleapis/python-dlp/commit/63e96614ba72e4ae8e0eafe4139d5329e75a3c18))
* added field to support infotype versioning ([63e9661](https://www.github.com/googleapis/python-dlp/commit/63e96614ba72e4ae8e0eafe4139d5329e75a3c18))

## [3.3.1](https://www.github.com/googleapis/python-dlp/compare/v3.3.0...v3.3.1) (2021-11-05)


### Bug Fixes

* **deps:** drop packaging dependency ([84181e9](https://www.github.com/googleapis/python-dlp/commit/84181e971ee04b46a603119d44410816fd7f04be))
* **deps:** require google-api-core >= 1.28.0 ([84181e9](https://www.github.com/googleapis/python-dlp/commit/84181e971ee04b46a603119d44410816fd7f04be))
* fix extras_require typo in setup.py ([84181e9](https://www.github.com/googleapis/python-dlp/commit/84181e971ee04b46a603119d44410816fd7f04be))


### Documentation

* list oneofs in docstring ([84181e9](https://www.github.com/googleapis/python-dlp/commit/84181e971ee04b46a603119d44410816fd7f04be))

## [3.3.0](https://www.github.com/googleapis/python-dlp/compare/v3.2.4...v3.3.0) (2021-10-26)


### Features

* add context manager support in client ([#272](https://www.github.com/googleapis/python-dlp/issues/272)) ([c0ba4eb](https://www.github.com/googleapis/python-dlp/commit/c0ba4eb27304c4e216864f6707693b27dc22c214))

## [3.2.4](https://www.github.com/googleapis/python-dlp/compare/v3.2.3...v3.2.4) (2021-10-05)


### Bug Fixes

* improper types in pagers generation ([164977f](https://www.github.com/googleapis/python-dlp/commit/164977fda1fff85a245869ff197c3ca9f200f544))

## [3.2.3](https://www.github.com/googleapis/python-dlp/compare/v3.2.2...v3.2.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([ff98215](https://www.github.com/googleapis/python-dlp/commit/ff98215e7dc3fc6a2e8b04e3b8e570cd72556f4f))

## [3.2.2](https://www.github.com/googleapis/python-dlp/compare/v3.2.1...v3.2.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#218](https://www.github.com/googleapis/python-dlp/issues/218)) ([584a887](https://www.github.com/googleapis/python-dlp/commit/584a887ac2bb648ebac439d4044f3fd8f12a01f4))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#210](https://www.github.com/googleapis/python-dlp/issues/210)) ([566827b](https://www.github.com/googleapis/python-dlp/commit/566827ba4cead4a5237fed370da132dd6fb55602))


### Miscellaneous Chores

* release as 3.2.2 ([#219](https://www.github.com/googleapis/python-dlp/issues/219)) ([5618115](https://www.github.com/googleapis/python-dlp/commit/56181152dbc1e48a70583e81dbe0fc089725f463))

## [3.2.1](https://www.github.com/googleapis/python-dlp/compare/v3.2.0...v3.2.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#209](https://www.github.com/googleapis/python-dlp/issues/209)) ([a016e6b](https://www.github.com/googleapis/python-dlp/commit/a016e6bd69a04b1e68efe48dd77493bd5267fbe5))

## [3.2.0](https://www.github.com/googleapis/python-dlp/compare/v3.1.1...v3.2.0) (2021-07-12)


### Features

* add always_use_jwt_access ([#172](https://www.github.com/googleapis/python-dlp/issues/172)) ([fb86805](https://www.github.com/googleapis/python-dlp/commit/fb8680580a16b088fd680355e85f12593372b9a4))


### Bug Fixes

* disable always_use_jwt_access ([#177](https://www.github.com/googleapis/python-dlp/issues/177)) ([15f189f](https://www.github.com/googleapis/python-dlp/commit/15f189fdbbb8f9445bd88e3675c3f1e65da84aad))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-dlp/issues/1127)) ([#166](https://www.github.com/googleapis/python-dlp/issues/166)) ([e2e1c90](https://www.github.com/googleapis/python-dlp/commit/e2e1c90d65a2e2e9c1be1ed7921e138059401519))

## [3.1.1](https://www.github.com/googleapis/python-dlp/compare/v3.1.0...v3.1.1) (2021-06-16)


### Bug Fixes

* **deps:** add packaging requirement ([#162](https://www.github.com/googleapis/python-dlp/issues/162)) ([e857e15](https://www.github.com/googleapis/python-dlp/commit/e857e1522d9fd59c1b4c5d9936c7371ddf8018b1))

## [3.1.0](https://www.github.com/googleapis/python-dlp/compare/v3.0.1...v3.1.0) (2021-05-28)


### Features

* crypto_deterministic_config ([#108](https://www.github.com/googleapis/python-dlp/issues/108)) ([#119](https://www.github.com/googleapis/python-dlp/issues/119)) ([396804d](https://www.github.com/googleapis/python-dlp/commit/396804d65e40c1ae9ced16aa0f04ef4bdffa54c5))
* support self-signed JWT flow for service accounts ([cdea974](https://www.github.com/googleapis/python-dlp/commit/cdea9744d0bc7244a42894acc1446080a16b2dab))


### Bug Fixes

* add async client ([cdea974](https://www.github.com/googleapis/python-dlp/commit/cdea9744d0bc7244a42894acc1446080a16b2dab))
* require google-api-core>=1.22.2 ([d146cf5](https://www.github.com/googleapis/python-dlp/commit/d146cf59db14b3c3afbef72d7a86419532ad347e))
* use correct retry deadlines ([#96](https://www.github.com/googleapis/python-dlp/issues/96)) ([d146cf5](https://www.github.com/googleapis/python-dlp/commit/d146cf59db14b3c3afbef72d7a86419532ad347e))

## [3.0.1](https://www.github.com/googleapis/python-dlp/compare/v3.0.0...v3.0.1) (2021-01-28)


### Bug Fixes

* remove gRPC send/recv limits;  add enums to `types/__init__.py` ([#89](https://www.github.com/googleapis/python-dlp/issues/89)) ([76e0439](https://www.github.com/googleapis/python-dlp/commit/76e0439b3acfdacf9303595107c03c1d49eac8b6))

## [3.0.0](https://www.github.com/googleapis/python-dlp/compare/v2.0.0...v3.0.0) (2020-12-02)


### ⚠ BREAKING CHANGES
* rename fields that collide with builtins (#75)
  * `ByteContentItem.type` -> `ByteContentItem.type_`
  * `MetadataLocation.type` -> `MetadataLocation.type_`
  * `Container.type` -> `Container.type_`
  * `Bucket.min` -> `Bucket.min_`
  * `Bucket.max `-> `Bucket.max_`
  * `DlpJob.type` -> `DlpJob.type_`
  * `GetDlpJobRequest.type` -> `GetDlpJobRequest.type_`

### Bug Fixes

* rename fields that collide with builtins; retrieve job config for risk analysis jobs ([#75](https://www.github.com/googleapis/python-dlp/issues/75)) ([4f3148e](https://www.github.com/googleapis/python-dlp/commit/4f3148e93ec3dfc9395aa38a3afc62498500a055))


### Documentation

* **samples:** fix README to accurately reflect the new repo after the move ([#72](https://www.github.com/googleapis/python-dlp/issues/72)) ([dc56806](https://www.github.com/googleapis/python-dlp/commit/dc56806b47f92227e396969d8a583b881aa41fd1))

## [2.0.0](https://www.github.com/googleapis/python-dlp/compare/v1.0.0...v2.0.0) (2020-08-18)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#34)

### Features

* migrate to use microgen ([#34](https://www.github.com/googleapis/python-dlp/issues/34)) ([c6001e2](https://www.github.com/googleapis/python-dlp/commit/c6001e20facb0bba957794c674c7b1121dc1774a))

## [1.0.0](https://www.github.com/googleapis/python-dlp/compare/v0.15.0...v1.0.0) (2020-06-10)


### Features

* set release_status to production/stable ([#9](https://www.github.com/googleapis/python-dlp/issues/9)) ([a7f22a5](https://www.github.com/googleapis/python-dlp/commit/a7f22a5c29d2393ed89a65c3423c590f4454d1c9))

## [0.15.0](https://www.github.com/googleapis/python-dlp/compare/v0.14.0...v0.15.0) (2020-05-14)


### Features

* add file types and metadata location enums (via synth) ([#16](https://www.github.com/googleapis/python-dlp/issues/16)) ([442bd9f](https://www.github.com/googleapis/python-dlp/commit/442bd9f57fdc7f186e34958ac422fa39eadf03c2))
* add support for hybrid jobs (via synth) ([#10](https://www.github.com/googleapis/python-dlp/issues/10)) ([ffad36e](https://www.github.com/googleapis/python-dlp/commit/ffad36ec37e62648f81830ecabbccb1d57e49036))

## [0.14.0](https://www.github.com/googleapis/python-dlp/compare/v0.13.0...v0.14.0) (2020-02-21)


### Features

* **dlp:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth)  ([#10040](https://www.github.com/googleapis/python-dlp/issues/10040)) ([b30d7c1](https://www.github.com/googleapis/python-dlp/commit/b30d7c1cd48fba47fdddb7b9232e421261108a52))

## 0.13.0

12-06-2019 14:29 PST


### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8953](https://github.com/googleapis/google-cloud-python/pull/8953))

### New Features
- Add `location_id` in preparation for regionalization; deprecate resource name helper functions (via synth). ([#9856](https://github.com/googleapis/google-cloud-python/pull/9856))

### Documentation
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Change requests intersphinx ref (via synth). ([#9403](https://github.com/googleapis/google-cloud-python/pull/9403))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

### Internal / Testing Changes
- Normalize VPCSC configuration in systests. ([#9608](https://github.com/googleapis/google-cloud-python/pull/9608))
- Ensure env is always set; fix typo in `test_deidentify_content`. ([#9479](https://github.com/googleapis/google-cloud-python/pull/9479))
- Exclude 'noxfile.py' from synth. ([#9284](https://github.com/googleapis/google-cloud-python/pull/9284))
- Ensure `GOOGLE_CLOUD_TESTS_IN_VPCSC` is down cast for env variables. ([#9274](https://github.com/googleapis/google-cloud-python/pull/9274))
- Add VPCSC tests. ([#9249](https://github.com/googleapis/google-cloud-python/pull/9249))

## 0.12.1

07-24-2019 16:16 PDT

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix docs navigation issues. ([#8723](https://github.com/googleapis/google-cloud-python/pull/8723))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

## 0.12.0

07-09-2019 13:20 PDT

### New Features
- Add support for publishing findings to GCS; deprecate 'DetectionRule' message (via synth). ([#8610](https://github.com/googleapis/google-cloud-python/pull/8610))
- Add 'client_options' support, update list method docstrings (via synth). ([#8507](https://github.com/googleapis/google-cloud-python/pull/8507))
- Allow kwargs to be passed to create_channel; expose support for AVRO files (via synth). ([#8443](https://github.com/googleapis/google-cloud-python/pull/8443))

### Internal / Testing Changes
- Pin black version (via synth). ([#8581](https://github.com/googleapis/google-cloud-python/pull/8581))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Update docstrings, format protos, update noxfile (via synth).  ([#8239](https://github.com/googleapis/google-cloud-python/pull/8239))
- Fix coverage in 'types.py' (via synth). ([#8153](https://github.com/googleapis/google-cloud-python/pull/8153))
- Blacken noxfile.py, setup.py (via synth). ([#8121](https://github.com/googleapis/google-cloud-python/pull/8121))
- Add empty lines (via synth). ([#8056](https://github.com/googleapis/google-cloud-python/pull/8056))
- Add nox session `docs`, reorder methods (via synth). ([#7769](https://github.com/googleapis/google-cloud-python/pull/7769))

## 0.11.0

04-15-2019 15:05 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7267](https://github.com/googleapis/google-cloud-python/pull/7267))
- Protoc-generated serialization update. ([#7081](https://github.com/googleapis/google-cloud-python/pull/7081))

### New Features
- Add support for filtering job triggers; add CryptoDeterministicConfig; update docs/conf.py. (via synth). ([#7390](https://github.com/googleapis/google-cloud-python/pull/7390))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Pick up stub docstring fix in GAPIC generator. ([#6969](https://github.com/googleapis/google-cloud-python/pull/6969))

### Internal / Testing Changes
- Copy in proto files. ([#7227](https://github.com/googleapis/google-cloud-python/pull/7227))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.10.0

12-17-2018 18:07 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6611](https://github.com/googleapis/google-cloud-python/pull/6611))
- Pick up fixes in GAPIC generator. ([#6495](https://github.com/googleapis/google-cloud-python/pull/6495))
- Fix `client_info` bug, update docstrings via synth. ([#6440](https://github.com/googleapis/google-cloud-python/pull/6440))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))

### New Features
- Add `BigQueryOptions.excluded_fields`. ([#6312](https://github.com/googleapis/google-cloud-python/pull/6312))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Pick up docstring fix via synth. ([#6874](https://github.com/googleapis/google-cloud-python/pull/6874))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6565](https://github.com/googleapis/google-cloud-python/pull/6565))

## 0.9.0

10-18-2018 10:44 PDT

### New Features

- Added `stored_info_type` methods to v2. ([#6221](https://github.com/googleapis/google-cloud-python/pull/6221))

### Documentation

- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))

### Internal / Testing Changes

- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Avoid replacing/scribbling on 'setup.py' during synth. ([#6125](https://github.com/googleapis/google-cloud-python/pull/6125))

## 0.8.0

### New Features
- Add support for exclude findings. ([#6091](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6091))
- Add support for stored info type support. ([#5950](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5950))

### Documentation
- Fix docs issue in DLP generation. ([#5668](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5668), [#5815](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5815))
- Docs: Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))

## 0.7.0

### New Features
- Add StoredInfoTypes (#5809)

## 0.6.0

### New Features
- Regenerate DLP v2 endpoint (redact image, delta presence) (#5666)

### Internal / Testing Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.5.0

### New Features
- Add PublishSummaryToCscc (#5246)
- Add configurable row limit (#5246)
- Add EntityID added to risk stats (#5246)
- Add dictionaries via GCS (#5246)

## 0.4.0

### Implementation Changes

- Remove DLP client version V2Beta1 (#5155)

## 0.3.0

### Implementation changes

- The library has been regenerated to pick up changes from the API's proto definition. (#5131)

## 0.2.0

### Interface additions

- Add DLP v2 (#5059)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Normalize all setup.py files (#4909)

## 0.1.0

Initial release of the DLP (Data Loss Prevention) client library. (#4879)
