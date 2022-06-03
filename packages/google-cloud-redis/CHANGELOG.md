# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-redis/#history

## [2.8.0](https://github.com/googleapis/python-redis/compare/v2.7.1...v2.8.0) (2022-03-15)


### Features

* add secondary_ip_range field ([d08e3b5](https://github.com/googleapis/python-redis/commit/d08e3b5c7c6c635b7dc7277b0a455b088e94dd19))
* add support for AUTH functionality ([d08e3b5](https://github.com/googleapis/python-redis/commit/d08e3b5c7c6c635b7dc7277b0a455b088e94dd19))
* add support for TLS functionality ([d08e3b5](https://github.com/googleapis/python-redis/commit/d08e3b5c7c6c635b7dc7277b0a455b088e94dd19))
* add Support Maintenance Window ([#172](https://github.com/googleapis/python-redis/issues/172)) ([d08e3b5](https://github.com/googleapis/python-redis/commit/d08e3b5c7c6c635b7dc7277b0a455b088e94dd19))

## [2.7.1](https://github.com/googleapis/python-redis/compare/v2.7.0...v2.7.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#168](https://github.com/googleapis/python-redis/issues/168)) ([2fd9d9e](https://github.com/googleapis/python-redis/commit/2fd9d9e44b80ae9b8d66c5eb413a04c4e9a92792))
* **deps:** require proto-plus>=1.15.0 ([2fd9d9e](https://github.com/googleapis/python-redis/commit/2fd9d9e44b80ae9b8d66c5eb413a04c4e9a92792))

## [2.7.0](https://github.com/googleapis/python-redis/compare/v2.6.0...v2.7.0) (2022-02-24)


### Features

* add secondary_ip_range field ([#157](https://github.com/googleapis/python-redis/issues/157)) ([dd310d5](https://github.com/googleapis/python-redis/commit/dd310d56b6b92fecae5bc537161fd8057d82b5b5))

## [2.6.0](https://github.com/googleapis/python-redis/compare/v2.5.1...v2.6.0) (2022-02-03)


### Features

* add api key support ([#151](https://github.com/googleapis/python-redis/issues/151)) ([044d0b5](https://github.com/googleapis/python-redis/commit/044d0b577b83408e3c724817b790ff2f767be103))
* add automated RDB, also known as persistence ([#153](https://github.com/googleapis/python-redis/issues/153)) ([30d3fc6](https://github.com/googleapis/python-redis/commit/30d3fc6bb0324cba1509141bd1679850f9bda0e4))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([73a5057](https://github.com/googleapis/python-redis/commit/73a50579622e3f780cbb457a08c20402698d1b63))

## [2.5.1](https://github.com/googleapis/python-redis/compare/v2.5.0...v2.5.1) (2022-01-14)


### Bug Fixes

* Add missing fields for TLS and Maintenance Window features ([#147](https://github.com/googleapis/python-redis/issues/147)) ([f04a02e](https://github.com/googleapis/python-redis/commit/f04a02e81a8a449bdcf07f5725778425242fe16e))

## [2.5.0](https://www.github.com/googleapis/python-redis/compare/v2.4.1...v2.5.0) (2021-11-09)


### Features

* **v1beta1:** Support Multiple Read Replicas when creating Instance ([#136](https://www.github.com/googleapis/python-redis/issues/136)) ([d7146eb](https://www.github.com/googleapis/python-redis/commit/d7146eb1ed826bcd1f2bb29b4de4793ff3105573))
* **v1:** Support Multiple Read Replicas when creating Instance ([#135](https://www.github.com/googleapis/python-redis/issues/135)) ([27dfdca](https://www.github.com/googleapis/python-redis/commit/27dfdcab82c091d77f40542e6393a0a3f466bcb0))

## [2.4.1](https://www.github.com/googleapis/python-redis/compare/v2.4.0...v2.4.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([2069ea6](https://www.github.com/googleapis/python-redis/commit/2069ea6ff1dd200a9b3162fe892f425e36da1aff))
* **deps:** require google-api-core >= 1.28.0 ([2069ea6](https://www.github.com/googleapis/python-redis/commit/2069ea6ff1dd200a9b3162fe892f425e36da1aff))


### Documentation

* list oneofs in docstring ([2069ea6](https://www.github.com/googleapis/python-redis/commit/2069ea6ff1dd200a9b3162fe892f425e36da1aff))

## [2.4.0](https://www.github.com/googleapis/python-redis/compare/v2.3.0...v2.4.0) (2021-10-14)


### Features

* add support for python 3.10 ([#127](https://www.github.com/googleapis/python-redis/issues/127)) ([1b53f97](https://www.github.com/googleapis/python-redis/commit/1b53f97810a19a87d2c2a51dac855e73c5888da5))

## [2.3.0](https://www.github.com/googleapis/python-redis/compare/v2.2.4...v2.3.0) (2021-10-08)


### Features

* add context manager support in client ([#123](https://www.github.com/googleapis/python-redis/issues/123)) ([4324911](https://www.github.com/googleapis/python-redis/commit/4324911a80baaaa96065e735631bd6c446075f5c))

## [2.2.4](https://www.github.com/googleapis/python-redis/compare/v2.2.3...v2.2.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([7b93deb](https://www.github.com/googleapis/python-redis/commit/7b93debcc36cdb60bf8c17808aa1a05bad4695f6))

## [2.2.3](https://www.github.com/googleapis/python-redis/compare/v2.2.2...v2.2.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([cf0a714](https://www.github.com/googleapis/python-redis/commit/cf0a71406dfa86909099fc26553f7bf74d4d23e1))

## [2.2.2](https://www.github.com/googleapis/python-redis/compare/v2.2.1...v2.2.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#102](https://www.github.com/googleapis/python-redis/issues/102)) ([dd8b006](https://www.github.com/googleapis/python-redis/commit/dd8b0069075ee4aea18efef67f36ce045345684a))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#98](https://www.github.com/googleapis/python-redis/issues/98)) ([923f6dc](https://www.github.com/googleapis/python-redis/commit/923f6dc6497f826f80d11a4a35e5cd26b5755eac))


### Miscellaneous Chores

* release as 2.2.2 ([#103](https://www.github.com/googleapis/python-redis/issues/103)) ([6fad3b8](https://www.github.com/googleapis/python-redis/commit/6fad3b878a9e58269e5d513424ae0a36763677f8))

## [2.2.1](https://www.github.com/googleapis/python-redis/compare/v2.2.0...v2.2.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#97](https://www.github.com/googleapis/python-redis/issues/97)) ([5fcec51](https://www.github.com/googleapis/python-redis/commit/5fcec51612b8a22ceb7e121e23b9a29ece60b130))

## [2.2.0](https://www.github.com/googleapis/python-redis/compare/v2.1.1...v2.2.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#88](https://www.github.com/googleapis/python-redis/issues/88)) ([223cac0](https://www.github.com/googleapis/python-redis/commit/223cac02e172a6fe2bdee207d3b9e1973015e58c))


### Bug Fixes

* disable always_use_jwt_access ([#92](https://www.github.com/googleapis/python-redis/issues/92)) ([1f0b236](https://www.github.com/googleapis/python-redis/commit/1f0b23654a007ee62fa24fb85ba85362e9fdc9d8))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-redis/issues/1127)) ([#83](https://www.github.com/googleapis/python-redis/issues/83)) ([3a64290](https://www.github.com/googleapis/python-redis/commit/3a642900cb9b0ab6fc2dd143c1ccac6a34b30209))

## [2.1.1](https://www.github.com/googleapis/python-redis/compare/v2.1.0...v2.1.1) (2021-05-28)


### Bug Fixes

* **deps:** add packaging requirement ([#76](https://www.github.com/googleapis/python-redis/issues/76)) ([7d53117](https://www.github.com/googleapis/python-redis/commit/7d53117aa37a3a9e878cad76ed1b48ec6200b7b1))
* remove libcst from requirements ([#54](https://www.github.com/googleapis/python-redis/issues/54)) ([6a10fff](https://www.github.com/googleapis/python-redis/commit/6a10fff85baceff2061807f43350fd0a7235dcac))

## [2.1.0](https://www.github.com/googleapis/python-redis/compare/v2.0.0...v2.1.0) (2021-01-29)


### Features

* add common resource helpers; expose client transport; remove send/recv gRPC limits ([#38](https://www.github.com/googleapis/python-redis/issues/38)) ([f3f1a86](https://www.github.com/googleapis/python-redis/commit/f3f1a86a2f14ceeaf22362387b397d9b3f880684))

## [2.0.0](https://www.github.com/googleapis/python-redis/compare/v1.0.0...v2.0.0) (2020-09-14)


### ⚠ BREAKING CHANGES

* migrate to microgen (#30)

### Features

* migrate to microgen ([#30](https://www.github.com/googleapis/python-redis/issues/30)) ([a17c1a8](https://www.github.com/googleapis/python-redis/commit/a17c1a840e10ccde25df8d4305b48997e37acd51))


### Bug Fixes

* update retry config ([#24](https://www.github.com/googleapis/python-redis/issues/24)) ([0b3f2c0](https://www.github.com/googleapis/python-redis/commit/0b3f2c075728a6ec4d5d503d010de229ed1ef725))


### Documentation

* add multiprocessing note (via synth) ([#17](https://www.github.com/googleapis/python-redis/issues/17)) ([fb04673](https://www.github.com/googleapis/python-redis/commit/fb046731d325132654ce91cb5513870befd7eec4))

## [1.0.0](https://www.github.com/googleapis/python-redis/compare/v0.4.0...v1.0.0) (2020-05-12)


### Features

* set release_status to production/stable ([#11](https://www.github.com/googleapis/python-redis/issues/11)) ([effc368](https://www.github.com/googleapis/python-redis/commit/effc368f6904cb6321ec9a8100460a0df36132ab))

## [0.4.0](https://www.github.com/googleapis/python-redis/compare/v0.3.0...v0.4.0) (2020-02-12)


### Features

* **redis:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10049](https://www.github.com/googleapis/python-redis/issues/10049)) ([b8a8c24](https://www.github.com/googleapis/python-redis/commit/b8a8c242c3f8f91b4615190006f5a2da720c8f40))
* add ConnectMode and upgrade_instance ([#5](https://www.github.com/googleapis/python-redis/issues/5)) ([e55220b](https://www.github.com/googleapis/python-redis/commit/e55220b5c189bc96589abac492a490d1d99b53ff))


### Bug Fixes

* **redis:** deprecate resource name helper methods (via synth) ([#9840](https://www.github.com/googleapis/python-redis/issues/9840)) ([75342ef](https://www.github.com/googleapis/python-redis/commit/75342ef43750ec5709694ac39306e5747e01fcdc))

## 0.3.0

07-24-2019 17:15 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8400](https://github.com/googleapis/google-cloud-python/pull/8400))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7272](https://github.com/googleapis/google-cloud-python/pull/7272))
- Protoc-generated serialization update. ([#7092](https://github.com/googleapis/google-cloud-python/pull/7092))
- Pick up stub docstring fix in GAPIC generator. ([#6979](https://github.com/googleapis/google-cloud-python/pull/6979))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8519](https://github.com/googleapis/google-cloud-python/pull/8519))
- Add 'import_instance' / 'export_instance' support (via synth). ([#8220](https://github.com/googleapis/google-cloud-python/pull/8220))
- Remove v1 'import_instance' / 'export_instance'; add v1beta1 'failover_instance' (via synth). ([#7937](https://github.com/googleapis/google-cloud-python/pull/7937))
- Add support for instance import / export / failover (via synth). ([#7423](https://github.com/googleapis/google-cloud-python/pull/7423))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Pin black version (via synth). ([#8592](https://github.com/googleapis/google-cloud-python/pull/8592))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update year: 2018 -> 2019. ([#7154](https://github.com/googleapis/google-cloud-python/pull/7154))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8360](https://github.com/googleapis/google-cloud-python/pull/8360))
- Add disclaimer to auto-generated template files (via synth).  ([#8324](https://github.com/googleapis/google-cloud-python/pull/8324))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8249](https://github.com/googleapis/google-cloud-python/pull/8249))
- Fix coverage in 'types.py' (via synth). ([#8161](https://github.com/googleapis/google-cloud-python/pull/8161))
- Blacken noxfile.py, setup.py (via synth). ([#8129](https://github.com/googleapis/google-cloud-python/pull/8129))
- Add empty lines (via synth). ([#8068](https://github.com/googleapis/google-cloud-python/pull/8068))
- Finsh setup for 'docs' session in nox. ([#8101](https://github.com/googleapis/google-cloud-python/pull/8101))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))
- Copy lintified proto files (via synth).
- Add clarifying comment to blacken nox target. ([#7400](https://github.com/googleapis/google-cloud-python/pull/7400))
- Copy proto files alongside protoc versions.
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.2.1

12-18-2018 09:40 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6504](https://github.com/googleapis/google-cloud-python/pull/6504))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings. ([#6419](https://github.com/googleapis/google-cloud-python/pull/6419))
- Re-generate library using redis/synth.py ([#6016](https://github.com/googleapis/google-cloud-python/pull/6016))
- Re-generate library using redis/synth.py ([#5993](https://github.com/googleapis/google-cloud-python/pull/5993))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Don't synth 'README.rst'. ([#6262](https://github.com/googleapis/google-cloud-python/pull/6262))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.2.0

### New Features

- Add the v1 API client library. ([#5945](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5945))

### Documentation

- Docs: Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))
- Redis: Fix README.md links ([#5745](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5745))
- Add redis documentation to main index.rst ([#5405](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5405))

### Internal / Testing Changes

- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5364))
- Unit tests require grpcio. ([#5363](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5363))

## 0.1.0

### New Features
Initial version of Redis client library v1beta1.
