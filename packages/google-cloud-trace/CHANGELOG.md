# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-trace/#history

## [1.7.0](https://github.com/googleapis/python-trace/compare/v1.6.2...v1.7.0) (2022-07-16)


### Features

* add audience parameter ([9fbef80](https://github.com/googleapis/python-trace/commit/9fbef80b978ae5a2dba2fa08e0a92dd18c3267ca))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#244](https://github.com/googleapis/python-trace/issues/244)) ([aa3229c](https://github.com/googleapis/python-trace/commit/aa3229c8866bf68a7069ec19f01e049836ff0b05))
* require python 3.7+ ([#242](https://github.com/googleapis/python-trace/issues/242)) ([c24ff5e](https://github.com/googleapis/python-trace/commit/c24ff5ee0511172b48f3df0755a8bde4a981f92f))

## [1.6.2](https://github.com/googleapis/python-trace/compare/v1.6.1...v1.6.2) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#229](https://github.com/googleapis/python-trace/issues/229)) ([6074f64](https://github.com/googleapis/python-trace/commit/6074f646b6bac5b6e106b86dc44c0d3132d67712))


### Documentation

* fix changelog header to consistent size ([#230](https://github.com/googleapis/python-trace/issues/230)) ([4994bb7](https://github.com/googleapis/python-trace/commit/4994bb7bf34f9e2c4afa7c4c38947bdeab76598a))

## [1.6.1](https://github.com/googleapis/python-trace/compare/v1.6.0...v1.6.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#193](https://github.com/googleapis/python-trace/issues/193)) ([cef4d52](https://github.com/googleapis/python-trace/commit/cef4d524dcc06216e8d32d738f698b21082ae50f))
* **deps:** require proto-plus>=1.15.0 ([cef4d52](https://github.com/googleapis/python-trace/commit/cef4d524dcc06216e8d32d738f698b21082ae50f))

## [1.6.0](https://github.com/googleapis/python-trace/compare/v1.5.1...v1.6.0) (2022-02-11)


### Features

* add api key support ([#176](https://github.com/googleapis/python-trace/issues/176)) ([5c1ea85](https://github.com/googleapis/python-trace/commit/5c1ea8505ba5dbbf9d0d544db95e14bd63e1be53))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([e0294af](https://github.com/googleapis/python-trace/commit/e0294af5d06c22a8739e9d50f514e4bbe85e8463))

## [1.5.1](https://www.github.com/googleapis/python-trace/compare/v1.5.0...v1.5.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([755b803](https://www.github.com/googleapis/python-trace/commit/755b8033a5e43490eda443e8ac6817f0d14ecc85))
* **deps:** require google-api-core >= 1.28.0 ([755b803](https://www.github.com/googleapis/python-trace/commit/755b8033a5e43490eda443e8ac6817f0d14ecc85))


### Documentation

* list oneofs in docstring ([755b803](https://www.github.com/googleapis/python-trace/commit/755b8033a5e43490eda443e8ac6817f0d14ecc85))

## [1.5.0](https://www.github.com/googleapis/python-trace/compare/v1.4.0...v1.5.0) (2021-10-14)


### Features

* add support for python 3.10 ([#146](https://www.github.com/googleapis/python-trace/issues/146)) ([11d2d9e](https://www.github.com/googleapis/python-trace/commit/11d2d9ec1a615600caca6c3e03a28ceac567452f))

## [1.4.0](https://www.github.com/googleapis/python-trace/compare/v1.3.4...v1.4.0) (2021-10-07)


### Features

* add context manager support in client ([#141](https://www.github.com/googleapis/python-trace/issues/141)) ([2bf8ab7](https://www.github.com/googleapis/python-trace/commit/2bf8ab7c0ac288feb63cbd84ed1826f996136200))

## [1.3.4](https://www.github.com/googleapis/python-trace/compare/v1.3.3...v1.3.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([cb38c20](https://www.github.com/googleapis/python-trace/commit/cb38c2000d9edf20943cb8c6a5ed98e6aa2a57b6))

## [1.3.3](https://www.github.com/googleapis/python-trace/compare/v1.3.2...v1.3.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([4a5ed62](https://www.github.com/googleapis/python-trace/commit/4a5ed6283a9ed3ed7732117023d362c20d031c16))

## [1.3.2](https://www.github.com/googleapis/python-trace/compare/v1.3.1...v1.3.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#113](https://www.github.com/googleapis/python-trace/issues/113)) ([99eba56](https://www.github.com/googleapis/python-trace/commit/99eba56da96bf968036e1eb3af0e9fee056db0ca))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#109](https://www.github.com/googleapis/python-trace/issues/109)) ([6aa9d7a](https://www.github.com/googleapis/python-trace/commit/6aa9d7a80e88be1210a60cd802ba682ae20839cc))


### Miscellaneous Chores

* release as 1.3.2 ([#114](https://www.github.com/googleapis/python-trace/issues/114)) ([57d63cd](https://www.github.com/googleapis/python-trace/commit/57d63cdb6b6e2eae77d4bda07749546c1ab65611))

## [1.3.1](https://www.github.com/googleapis/python-trace/compare/v1.3.0...v1.3.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#108](https://www.github.com/googleapis/python-trace/issues/108)) ([63a9999](https://www.github.com/googleapis/python-trace/commit/63a9999ee62a956c3df5516bccaa942e53f999db))

## [1.3.0](https://www.github.com/googleapis/python-trace/compare/v1.2.0...v1.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#96](https://www.github.com/googleapis/python-trace/issues/96)) ([e88837d](https://www.github.com/googleapis/python-trace/commit/e88837d7bc7ac180f87f4a5bb8a4cbd71f6e3449))


### Bug Fixes

* disable always_use_jwt_access ([#100](https://www.github.com/googleapis/python-trace/issues/100)) ([110f692](https://www.github.com/googleapis/python-trace/commit/110f692dace7b321d92033b1ccc1330deb859395))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-trace/issues/1127)) ([#91](https://www.github.com/googleapis/python-trace/issues/91)) ([5dcc16c](https://www.github.com/googleapis/python-trace/commit/5dcc16ca802dc2a8895389fabecd82e4ec739e54))

## [1.2.0](https://www.github.com/googleapis/python-trace/compare/v1.1.0...v1.2.0) (2021-05-27)


### Features

* add `from_service_account_info` ([e097a64](https://www.github.com/googleapis/python-trace/commit/e097a643c9584a50ae91b823f8dbd8df705001f6))
* add common resource path helpers ([#70](https://www.github.com/googleapis/python-trace/issues/70)) ([e097a64](https://www.github.com/googleapis/python-trace/commit/e097a643c9584a50ae91b823f8dbd8df705001f6))
* support self-signed JWT flow for service accounts ([1055668](https://www.github.com/googleapis/python-trace/commit/105566818fe8f8930a8393ebfc827ef151b695df))


### Bug Fixes

* add async client ([1055668](https://www.github.com/googleapis/python-trace/commit/105566818fe8f8930a8393ebfc827ef151b695df))
* **deps:** add packaging requirement ([#84](https://www.github.com/googleapis/python-trace/issues/84)) ([792599f](https://www.github.com/googleapis/python-trace/commit/792599fc0e21f3e0d71acdaf9f0d4d6e3afabc5f))
* use correct retry deadlines ([e097a64](https://www.github.com/googleapis/python-trace/commit/e097a643c9584a50ae91b823f8dbd8df705001f6))

## [1.1.0](https://www.github.com/googleapis/python-trace/compare/v1.0.0...v1.1.0) (2020-10-13)


### Features

* bump to GA ([#51](https://www.github.com/googleapis/python-trace/issues/51)) ([1985fef](https://www.github.com/googleapis/python-trace/commit/1985feff307ee117d552e1c13c1ef8b2b86278e0))


### Documentation

* state >=3.6 requirement in README ([#42](https://www.github.com/googleapis/python-trace/issues/42)) ([c162047](https://www.github.com/googleapis/python-trace/commit/c162047a779478a43561a7e1f1b8687dda5ecc89))


### Dependencies

* remove unused google-cloud-core dependency ([#50](https://www.github.com/googleapis/python-trace/issues/50)) ([e748cb4](https://www.github.com/googleapis/python-trace/commit/e748cb4d27fdc6c7cdde2d63417f7892820c75dd))

## [1.0.0](https://www.github.com/googleapis/python-trace/compare/v0.24.0...v1.0.0) (2020-09-14)


### ⚠ BREAKING CHANGES

* migrate to microgenerator. See [Migration Guide](https://github.com/googleapis/python-trace/blob/main/UPGRADING.md) (#29)

### Features

* migrate to microgenerator ([#29](https://www.github.com/googleapis/python-trace/issues/29)) ([f0d9d91](https://www.github.com/googleapis/python-trace/commit/f0d9d9161d7aee344ad1765c477947cd04505bf5))

## [0.24.0](https://www.github.com/googleapis/python-trace/compare/v0.23.0...v0.24.0) (2020-08-06)


### ⚠ BREAKING CHANGES

* **trace:** remove `span_path` resource helper method from v2; modify retry configs; standardize usage of 'optional' and 'required' for args in docstrings; add 2.7 deprecation warning (via synth)  (#10075)

### Features

* **trace:** add `client_options` to constructor ([#9154](https://www.github.com/googleapis/python-trace/issues/9154)) ([a5b4f7a](https://www.github.com/googleapis/python-trace/commit/a5b4f7aa4575364868ba80aa0a3b1289dc7f0c3e))
* added support for span kind ([#28](https://www.github.com/googleapis/python-trace/issues/28)) ([23ba194](https://www.github.com/googleapis/python-trace/commit/23ba194fdc59c34bfa5f66aba89a6baa8d7bb527))


### Bug Fixes

* **trace:** remove `span_path` resource helper method from v2; modify retry configs; standardize usage of 'optional' and 'required' for args in docstrings; add 2.7 deprecation warning (via synth)  ([#10075](https://www.github.com/googleapis/python-trace/issues/10075)) ([4c02194](https://www.github.com/googleapis/python-trace/commit/4c02194a8c1390b2a382e1f3aaef8138baf02f07))


### Documentation

* add python 2 sunset banner to documentation ([#9036](https://www.github.com/googleapis/python-trace/issues/9036)) ([52f3ab5](https://www.github.com/googleapis/python-trace/commit/52f3ab5db26a2b49d1e292ea9b349c1b698fa695))

## 0.23.0

10-15-2019 06:59 PDT


### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

### Documentation
- Change requests intersphinx url (via synth). ([#9410](https://github.com/googleapis/google-cloud-python/pull/9410))
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

## 0.22.1

08-12-2019 13:51 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8973](https://github.com/googleapis/google-cloud-python/pull/8973))

### Documentation
- Fix links to googleapis.dev ([#8998](https://github.com/googleapis/google-cloud-python/pull/8998))
- Fix pip / usage examples in README.rst. ([#8833](https://github.com/googleapis/google-cloud-python/pull/8833))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.22.0

07-24-2019 17:50 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8408](https://github.com/googleapis/google-cloud-python/pull/8408))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8526](https://github.com/googleapis/google-cloud-python/pull/8526))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8368](https://github.com/googleapis/google-cloud-python/pull/8368))
- Add disclaimer to auto-generated template files (via synth). ([#8332](https://github.com/googleapis/google-cloud-python/pull/8332))
- Fix coverage in 'types.py' (via synth). ([#8167](https://github.com/googleapis/google-cloud-python/pull/8167))
- Add empty lines (via synth). ([#8075](https://github.com/googleapis/google-cloud-python/pull/8075))

## 0.21.0

05-16-2019 12:58 PDT


### Implementation Changes
- Add routing header to method metadata (via synth).  ([#7602](https://github.com/googleapis/google-cloud-python/pull/7602))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to clients. ([#7899](https://github.com/googleapis/google-cloud-python/pull/7899))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Update docstring for `page_size` (via synth). ([#7688](https://github.com/googleapis/google-cloud-python/pull/7688))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Pick up stub docstring fix in GAPIC generator. ([#6985](https://github.com/googleapis/google-cloud-python/pull/6985))

### Internal / Testing Changes
- Add nox session `docs`, reorder methods (via synth). ([#7783](https://github.com/googleapis/google-cloud-python/pull/7783)) and ([#7784](https://github.com/googleapis/google-cloud-python/pull/7784))
- Copy lintified proto files (via synth). ([#7455](https://github.com/googleapis/google-cloud-python/pull/7455))
- Add clarifying comment to blacken nox target. ([#7406](https://github.com/googleapis/google-cloud-python/pull/7406))
- Remove unused message exports (via synth). ([#7278](https://github.com/googleapis/google-cloud-python/pull/7278))
- Copy proto files alongside protoc versions ([#7254](https://github.com/googleapis/google-cloud-python/pull/7254))
- Trivial gapic-generator change. ([#7236](https://github.com/googleapis/google-cloud-python/pull/7236))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers (via synth). ([#7161](https://github.com/googleapis/google-cloud-python/pull/7161))
- Protoc-generated serialization update. ([#7098](https://github.com/googleapis/google-cloud-python/pull/7098))

## 0.20.2

12-17-2018 17:06 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 0.20.1

12-07-2018 16:06 PST

### Implementation Changes
- Fix trace client memory leak ([#6856](https://github.com/googleapis/google-cloud-python/pull/6856))

### Dependencies
- Update version of google-cloud-core ([#6858](https://github.com/googleapis/google-cloud-python/pull/6858))

### Internal / Testing Changes
- Add baseline for synth.metadata

## 0.20.0

12-05-2018 13:16 PST


### Implementation Changes
- Use moved iam.policy now at google.api_core.iam.policy ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6577](https://github.com/googleapis/google-cloud-python/pull/6577))
- Fix client_info bug, update docstrings and timeouts. ([#6424](https://github.com/googleapis/google-cloud-python/pull/6424))
- Pass credentials into TraceServiceClient ([#5596](https://github.com/googleapis/google-cloud-python/pull/5596))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))

### New Features
- Add 'synth.py'. ([#6083](https://github.com/googleapis/google-cloud-python/pull/6083))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add static HTML redirect page for 'trace/starting.html'. ([#6142](https://github.com/googleapis/google-cloud-python/pull/6142))
- Prep docs for repo split. ([#6024](https://github.com/googleapis/google-cloud-python/pull/6024))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Updates to noxfile and other templates. Start Blackening. ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792)),
  ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701)),
  ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698)),
  ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666)),
  ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add kokoro for trace, remove trace from CircleCI ([#6112](https://github.com/googleapis/google-cloud-python/pull/6112))
- Use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier
- Move unit test from gax to gapic ([#4988](https://github.com/googleapis/google-cloud-python/pull/4988))

## 0.19.0

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)

## 0.18.0

### Breaking changes

- The underlying autogenerated client library was re-generated to pick up new 
  features and resolve bugs, this may change the exceptions raised from various
  methods. (#4799)

## 0.17.0

### Notable Implementation Changes

- Default to use Stackdriver Trace V2 API if calling `from google.cloud import trace`.
  Using V1 API needs to be explicitly specified in the import.(#4437)

PyPI: https://pypi.org/project/google-cloud-trace/0.17.0/

## 0.16.0

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-trace/0.16.0/
