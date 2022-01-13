# Changelog

### [2.6.3](https://github.com/googleapis/python-containeranalysis/compare/v2.6.2...v2.6.3) (2022-01-13)


### Bug Fixes

* **deps:** require grafeas 1.4.1 ([16d27f7](https://github.com/googleapis/python-containeranalysis/commit/16d27f73742d969a62394cf1de4cce85849ea92a))
* include the compliance protos ([#222](https://github.com/googleapis/python-containeranalysis/issues/222)) ([16d27f7](https://github.com/googleapis/python-containeranalysis/commit/16d27f73742d969a62394cf1de4cce85849ea92a))

### [2.6.2](https://www.github.com/googleapis/python-containeranalysis/compare/v2.6.1...v2.6.2) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([5de0b09](https://www.github.com/googleapis/python-containeranalysis/commit/5de0b093d7495f9d46c332463aa68a7a5995e317))
* **deps:** require google-api-core >= 1.28.0 ([5de0b09](https://www.github.com/googleapis/python-containeranalysis/commit/5de0b093d7495f9d46c332463aa68a7a5995e317))


### Documentation

* list oneofs in docstring ([5de0b09](https://www.github.com/googleapis/python-containeranalysis/commit/5de0b093d7495f9d46c332463aa68a7a5995e317))

### [2.6.1](https://www.github.com/googleapis/python-containeranalysis/compare/v2.6.0...v2.6.1) (2021-10-28)


### Bug Fixes

* fix extra_require typo ([#202](https://www.github.com/googleapis/python-containeranalysis/issues/202)) ([2948965](https://www.github.com/googleapis/python-containeranalysis/commit/2948965ecf269e97244c5388c389cf351d6abd1a))

## [2.6.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.5.0...v2.6.0) (2021-10-20)


### Features

* add support for python 3.10 ([#197](https://www.github.com/googleapis/python-containeranalysis/issues/197)) ([26f516c](https://www.github.com/googleapis/python-containeranalysis/commit/26f516ce4c78a3189b436dd8292dba66d2e3baa7))

## [2.5.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.4.2...v2.5.0) (2021-10-11)


### Features

* add context manager support in client ([#192](https://www.github.com/googleapis/python-containeranalysis/issues/192)) ([5274a93](https://www.github.com/googleapis/python-containeranalysis/commit/5274a933bd7abec9528168fa0530388536269c4c))

### [2.4.2](https://www.github.com/googleapis/python-containeranalysis/compare/v2.4.1...v2.4.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([42c8c64](https://www.github.com/googleapis/python-containeranalysis/commit/42c8c646630810189a971796c921b30a2d2b419f))

### [2.4.1](https://www.github.com/googleapis/python-containeranalysis/compare/v2.4.0...v2.4.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#156](https://www.github.com/googleapis/python-containeranalysis/issues/156)) ([e1ff96f](https://www.github.com/googleapis/python-containeranalysis/commit/e1ff96faa545e22358b5a0d62e005ca9dfac0105))
* enable self signed jwt for grpc ([#162](https://www.github.com/googleapis/python-containeranalysis/issues/162)) ([071eac6](https://www.github.com/googleapis/python-containeranalysis/commit/071eac6c5c0e6b0f48b75db3f2257f174dd7cbe4))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#157](https://www.github.com/googleapis/python-containeranalysis/issues/157)) ([16f4eff](https://www.github.com/googleapis/python-containeranalysis/commit/16f4eff9cdf2e5122d623eb05c1e155062822f12))


### Miscellaneous Chores

* release 2.4.1 ([#163](https://www.github.com/googleapis/python-containeranalysis/issues/163)) ([c49ad98](https://www.github.com/googleapis/python-containeranalysis/commit/c49ad9854b4ce1f3a6a28ec4035d5b0edb390cfd))

## [2.4.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.3.0...v2.4.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#147](https://www.github.com/googleapis/python-containeranalysis/issues/147)) ([1f55871](https://www.github.com/googleapis/python-containeranalysis/commit/1f558713a683e3b48d9d7fba2c015e92818850fd))


### Bug Fixes

* disable always_use_jwt_access ([#151](https://www.github.com/googleapis/python-containeranalysis/issues/151)) ([7768ae1](https://www.github.com/googleapis/python-containeranalysis/commit/7768ae1ce4a32fa25ef5c0fb86f8981fed038297))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-containeranalysis/issues/1127)) ([#141](https://www.github.com/googleapis/python-containeranalysis/issues/141)) ([a588841](https://www.github.com/googleapis/python-containeranalysis/commit/a58884154f23caf453040ad314c0a2d4416952f2))

## [2.3.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.2.3...v2.3.0) (2021-05-25)


### Features

* support self-signed JWT flow for service accounts ([b427e90](https://www.github.com/googleapis/python-containeranalysis/commit/b427e9091d4afc482c8d9fd6ff4510ad3b740820))


### Bug Fixes

* add async client to %name_%version/init.py ([b427e90](https://www.github.com/googleapis/python-containeranalysis/commit/b427e9091d4afc482c8d9fd6ff4510ad3b740820))
* **deps:** add packaging requirement ([#135](https://www.github.com/googleapis/python-containeranalysis/issues/135)) ([3f0bd3a](https://www.github.com/googleapis/python-containeranalysis/commit/3f0bd3af9d809150a81933601bee5b9de0ff834a))

### [2.2.3](https://www.github.com/googleapis/python-containeranalysis/compare/v2.2.2...v2.2.3) (2021-04-02)


### Bug Fixes

* require google-api-core >= 1.22.2 ([#103](https://www.github.com/googleapis/python-containeranalysis/issues/103)) ([74be886](https://www.github.com/googleapis/python-containeranalysis/commit/74be8869363254d3551a58634c299abcfb18e682))

### [2.2.2](https://www.github.com/googleapis/python-containeranalysis/compare/v2.2.1...v2.2.2) (2021-03-25)


### Bug Fixes

* effective severity attribute error ([#104](https://www.github.com/googleapis/python-containeranalysis/issues/104)) ([913251a](https://www.github.com/googleapis/python-containeranalysis/commit/913251aa5535612460cd7ed6139c3cb5b7c7cc3f))

### [2.2.1](https://www.github.com/googleapis/python-containeranalysis/compare/v2.2.0...v2.2.1) (2021-02-09)


### Documentation

* update python contributing guide ([#89](https://www.github.com/googleapis/python-containeranalysis/issues/89)) ([fd356af](https://www.github.com/googleapis/python-containeranalysis/commit/fd356afb7010186559ebdd621c6c2e7012826a81))

## [2.2.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.1.0...v2.2.0) (2021-01-06)


### Features

* add from_service_account_info factory and fix sphinx identifiers  ([#74](https://www.github.com/googleapis/python-containeranalysis/issues/74)) ([7a87c41](https://www.github.com/googleapis/python-containeranalysis/commit/7a87c4115b15ccd42ccf0836ed62d663601720f7))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([#68](https://www.github.com/googleapis/python-containeranalysis/issues/68)) ([77d47d3](https://www.github.com/googleapis/python-containeranalysis/commit/77d47d3efaceb30ed5952935a056229a960dc964))

## [2.1.0](https://www.github.com/googleapis/python-containeranalysis/compare/v2.0.0...v2.1.0) (2020-11-18)


### Features

* add GetVulnerabilityOccurrencesSummary ([#42](https://www.github.com/googleapis/python-containeranalysis/issues/42)) ([7f3e8b3](https://www.github.com/googleapis/python-containeranalysis/commit/7f3e8b3357bdce56aa1cf362b60f02717365c421))

## [2.0.0](https://www.github.com/googleapis/python-containeranalysis/compare/v1.0.3...v2.0.0) (2020-08-12)


### ⚠ BREAKING CHANGES

* move to microgen. See the [Migration Guide](https://github.com/googleapis/python-containeranalysis/blob/release-v2.0.0/UPGRADING.md) for details. (#33)

### Features

* move to microgen. See the [Migration Guide](https://github.com/googleapis/python-containeranalysis/blob/release-v2.0.0/UPGRADING.md) for details. ([#33](https://www.github.com/googleapis/python-containeranalysis/issues/33)) ([6098905](https://www.github.com/googleapis/python-containeranalysis/commit/60989058883a0ae35f3b913d6a06741c73186203))

### [1.0.3](https://www.github.com/googleapis/python-containeranalysis/compare/v1.0.2...v1.0.3) (2020-08-11)


### Bug Fixes

* Use different versions of pytest for python 2 and python3 [([#2558](https://www.github.com/googleapis/python-containeranalysis/issues/2558))](https://github.com/GoogleCloudPlatform/python-docs-samples/issues/2558) ([7d21641](https://www.github.com/googleapis/python-containeranalysis/commit/7d21641eb50f574784ae7dfbb1d25a0d0af14699))
* **deps:** add upper bound for grafeas ([#30](https://www.github.com/googleapis/python-containeranalysis/issues/30)) ([5ca8f79](https://www.github.com/googleapis/python-containeranalysis/commit/5ca8f7981349ed86438185f02681225f059cc9d9))

### [1.0.2](https://www.github.com/googleapis/python-containeranalysis/compare/v1.0.1...v1.0.2) (2020-07-16)


### Bug Fixes

* update retry config ([#23](https://www.github.com/googleapis/python-containeranalysis/issues/23)) ([ddf9585](https://www.github.com/googleapis/python-containeranalysis/commit/ddf95852778c0e60961516ecd77b793e6af3295b))


### Documentation

* add multiprocessing note ([#21](https://www.github.com/googleapis/python-containeranalysis/issues/21)) ([be29088](https://www.github.com/googleapis/python-containeranalysis/commit/be290885cef76ffdd27afb44cd858c6a89d4f280))

### [1.0.1](https://www.github.com/googleapis/python-containeranalysis/compare/v1.0.0...v1.0.1) (2020-06-16)


### Bug Fixes

* fix `release_status` in `setup.py` ([#17](https://www.github.com/googleapis/python-containeranalysis/issues/17)) ([2de847c](https://www.github.com/googleapis/python-containeranalysis/commit/2de847c1cf0e3e9a4f09f35d7abb5004dcee6bad))

## [1.0.0](https://www.github.com/googleapis/python-containeranalysis/compare/v0.3.1...v1.0.0) (2020-06-16)


### Features

* release as production/stable ([#15](https://www.github.com/googleapis/python-containeranalysis/issues/15)) ([b81e207](https://www.github.com/googleapis/python-containeranalysis/commit/b81e2074eb86c015c781b79a68839cbaeb40e5b2))
* remove `note_path` and `occurence_path` (via synth) ([#7](https://www.github.com/googleapis/python-containeranalysis/issues/7)) ([656b11e](https://www.github.com/googleapis/python-containeranalysis/commit/656b11eee22f11d1109e288190fc63b6c8ff20b7))

## 0.3.1

11-07-2019 11:08 PST

**NOTE**: Please upgrade to this version if you will also be using `google-cloud-build`. 

### Implementation Changes
- Make google.cloud.devtools a namespace ([#9606](https://github.com/googleapis/google-cloud-python/pull/9606))

### Documentation
- Change requests intersphinx ref (via synth)
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 0.3.0

08-12-2019 13:53 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8948](https://github.com/googleapis/google-cloud-python/pull/8948))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.2.0

07-12-2019 16:56 PDT

### New Features
- Add 'client_options' support (via synth). ([#8502](https://github.com/googleapis/google-cloud-python/pull/8502))
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8653](https://github.com/googleapis/google-cloud-python/pull/8653))

### Dependencies
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Update READMEs. ([#8456](https://github.com/googleapis/google-cloud-python/pull/8456))

### Internal / Testing Changes
- Fix language in repo metadata. ([#8537](https://github.com/googleapis/google-cloud-python/pull/8537))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.1.0

06-19-2019 11:02 PDT

### New Features
- Initial release of Container Analysis client library. ([#8381](https://github.com/googleapis/google-cloud-python/pull/8381))
