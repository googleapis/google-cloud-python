# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-phishing-protection/#history


## [1.5.2](https://github.com/googleapis/python-phishingprotection/compare/v1.5.1...v1.5.2) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#183](https://github.com/googleapis/python-phishingprotection/issues/183)) ([5706b52](https://github.com/googleapis/python-phishingprotection/commit/5706b523ce087797fead72b243ec106d3630e865))


### Documentation

* fix changelog header to consistent size ([#184](https://github.com/googleapis/python-phishingprotection/issues/184)) ([5da1123](https://github.com/googleapis/python-phishingprotection/commit/5da1123a8f8f4eb00b5813cac41a17143baad5c6))

## [1.5.1](https://github.com/googleapis/python-phishingprotection/compare/v1.5.0...v1.5.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#158](https://github.com/googleapis/python-phishingprotection/issues/158)) ([7ccbadd](https://github.com/googleapis/python-phishingprotection/commit/7ccbaddea3b3152fbe97fb08bec337578b2e6902))
* **deps:** require proto-plus>=1.15.0 ([7ccbadd](https://github.com/googleapis/python-phishingprotection/commit/7ccbaddea3b3152fbe97fb08bec337578b2e6902))

## [1.5.0](https://github.com/googleapis/python-phishingprotection/compare/v1.4.1...v1.5.0) (2022-02-26)


### Features

* add api key support ([#144](https://github.com/googleapis/python-phishingprotection/issues/144)) ([dc83a72](https://github.com/googleapis/python-phishingprotection/commit/dc83a725bfff5062193b1c29f6ee00ebddd972ba))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([f5abff9](https://github.com/googleapis/python-phishingprotection/commit/f5abff9ba017069ada02f8e65b82f1ed62c8710d))

## [1.4.1](https://www.github.com/googleapis/python-phishingprotection/compare/v1.4.0...v1.4.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([da58ec0](https://www.github.com/googleapis/python-phishingprotection/commit/da58ec0c68c39ddee99b2da483abb2a0e4a5ac5b))
* **deps:** require google-api-core >= 1.28.0 ([da58ec0](https://www.github.com/googleapis/python-phishingprotection/commit/da58ec0c68c39ddee99b2da483abb2a0e4a5ac5b))


### Documentation

* list oneofs in docstring ([da58ec0](https://www.github.com/googleapis/python-phishingprotection/commit/da58ec0c68c39ddee99b2da483abb2a0e4a5ac5b))

## [1.4.0](https://www.github.com/googleapis/python-phishingprotection/compare/v1.3.0...v1.4.0) (2021-10-14)


### Features

* add support for python 3.10 ([#124](https://www.github.com/googleapis/python-phishingprotection/issues/124)) ([a965fe4](https://www.github.com/googleapis/python-phishingprotection/commit/a965fe41e2b693dfb5d74913b4f26fd0f67d3925))

## [1.3.0](https://www.github.com/googleapis/python-phishingprotection/compare/v1.2.3...v1.3.0) (2021-10-08)


### Features

* add context manager support in client ([#120](https://www.github.com/googleapis/python-phishingprotection/issues/120)) ([2384d00](https://www.github.com/googleapis/python-phishingprotection/commit/2384d00ab4311c73fbb198963b15831d6dd14c45))

## [1.2.3](https://www.github.com/googleapis/python-phishingprotection/compare/v1.2.2...v1.2.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([a9ac832](https://www.github.com/googleapis/python-phishingprotection/commit/a9ac832c3bed179eec4f007c9e1535bf3a95aa57))

## [1.2.2](https://www.github.com/googleapis/python-phishingprotection/compare/v1.2.1...v1.2.2) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#95](https://www.github.com/googleapis/python-phishingprotection/issues/95)) ([0dab5c3](https://www.github.com/googleapis/python-phishingprotection/commit/0dab5c370cc34481227eb27ffa2c5defb816d8e0))
* enable self signed jwt for grpc ([#101](https://www.github.com/googleapis/python-phishingprotection/issues/101)) ([ac587fd](https://www.github.com/googleapis/python-phishingprotection/commit/ac587fd6d0bb6393f2c1743888c092f231b3f91d))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#96](https://www.github.com/googleapis/python-phishingprotection/issues/96)) ([c9ee6a2](https://www.github.com/googleapis/python-phishingprotection/commit/c9ee6a2838b8291a1205532b169e7fad03f1c440))


### Miscellaneous Chores

* release as 1.2.2 ([#100](https://www.github.com/googleapis/python-phishingprotection/issues/100)) ([de0503f](https://www.github.com/googleapis/python-phishingprotection/commit/de0503fffd4088d2e7d6e4b876427d79407441e8))

## [1.2.1](https://www.github.com/googleapis/python-phishingprotection/compare/v1.2.0...v1.2.1) (2021-07-14)


### Bug Fixes

* disable always_use_jwt_access ([#90](https://www.github.com/googleapis/python-phishingprotection/issues/90)) ([9725e35](https://www.github.com/googleapis/python-phishingprotection/commit/9725e35df1ed3fbe2a02a6d52207fa7e9226fbad))

## [1.2.0](https://www.github.com/googleapis/python-phishingprotection/compare/v1.1.1...v1.2.0) (2021-06-23)


### Features

* add always_use_jwt_access ([#86](https://www.github.com/googleapis/python-phishingprotection/issues/86)) ([2550523](https://www.github.com/googleapis/python-phishingprotection/commit/2550523ddd59d042b8cb1411617eee33fdddc965))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-phishingprotection/issues/1127)) ([#81](https://www.github.com/googleapis/python-phishingprotection/issues/81)) ([e8590bb](https://www.github.com/googleapis/python-phishingprotection/commit/e8590bbfa6e70d915b618ee265d7cd59cab07e98)), closes [#1126](https://www.github.com/googleapis/python-phishingprotection/issues/1126)

## [1.1.1](https://www.github.com/googleapis/python-phishingprotection/compare/v1.1.0...v1.1.1) (2021-05-28)


### Bug Fixes

* **deps:** add packaging requirement ([#74](https://www.github.com/googleapis/python-phishingprotection/issues/74)) ([23a9c0f](https://www.github.com/googleapis/python-phishingprotection/commit/23a9c0f7abc0c3385aee5c93f920a1119eb86baa))

## [1.1.0](https://www.github.com/googleapis/python-phishingprotection/compare/v1.0.0...v1.1.0) (2021-01-06)


### Features

* add from_service_account_info factory and fix sphinx identifiers  ([#46](https://www.github.com/googleapis/python-phishingprotection/issues/46)) ([8938b54](https://www.github.com/googleapis/python-phishingprotection/commit/8938b54d590753ae25213945be3764e90d4bb327))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([197a753](https://www.github.com/googleapis/python-phishingprotection/commit/197a75346252441e5a5cb5eee982e7cb64a20299))

## [1.0.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.4.0...v1.0.0) (2020-12-04)


### ⚠ BREAKING CHANGES

* Move to API to python microgenerator. See [Migration Guide](https://github.com/googleapis/python-phishingprotection/blob/main/UPGRADING.md). (#31)

### Features

* move to API to python microgenerator ([#31](https://www.github.com/googleapis/python-phishingprotection/issues/31)) ([826fabd](https://www.github.com/googleapis/python-phishingprotection/commit/826fabd0b6591a7cca7cfcdbcc16b853c067cd3d))


### Bug Fixes

* update retry config ([#27](https://www.github.com/googleapis/python-phishingprotection/issues/27)) ([c0418ae](https://www.github.com/googleapis/python-phishingprotection/commit/c0418ae2e4d13f32706d3ce6844c6260b27ca0b7))

## [0.4.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.3.0...v0.4.0) (2020-06-23)


### Features

* release as beta ([#22](https://www.github.com/googleapis/python-phishingprotection/issues/22)) ([5111f42](https://www.github.com/googleapis/python-phishingprotection/commit/5111f425eef6135a4eb4b958d0ed1c6865e6e9d7))

## [0.3.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.2.0...v0.3.0) (2020-02-05)


### Features

* **phishingprotection:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10048](https://www.github.com/googleapis/python-phishingprotection/issues/10048)) ([f96c1ed](https://www.github.com/googleapis/python-phishingprotection/commit/f96c1edfa57269b3e1ccbf3d8035e42fecb78987))


### Bug Fixes

* **phishingprotection:** deprecate resource name helper methods (via synth)  ([#9862](https://www.github.com/googleapis/python-phishingprotection/issues/9862)) ([83a9356](https://www.github.com/googleapis/python-phishingprotection/commit/83a93561695e799c8ff4a7d511fb7b6fe76d0d60))

## 0.2.0

10-10-2019 15:30 PDT

### Implementation Changes
- Use correct release status. ([#9451](https://github.com/googleapis/google-cloud-python/pull/9451))
- Remove send / receive message size limit (via synth). ([#8963](https://github.com/googleapis/google-cloud-python/pull/8963))
- Add `client_options` support, re-template / blacken files. ([#8539](https://github.com/googleapis/google-cloud-python/pull/8539))
- Fix dist name used to compute `gapic_version`. ([#8100](https://github.com/googleapis/google-cloud-python/pull/8100))
- Remove retries for `DEADLINE_EXCEEDED` (via synth). ([#7889](https://github.com/googleapis/google-cloud-python/pull/7889))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Change requests intersphinx url (via synth). ([#9407](https://github.com/googleapis/google-cloud-python/pull/9407))
- Update docstrings (via synth). ([#9350](https://github.com/googleapis/google-cloud-python/pull/9350))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

### Internal / Testing Changes
- Pin black version (via synth). ([#8590](https://github.com/googleapis/google-cloud-python/pull/8590))

## 0.1.0

04-30-2019 15:03 PDT

### New Features
- Initial release of Phishing Protection. ([#7801](https://github.com/googleapis/google-cloud-python/pull/7801))
