# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/grafeas/#history

## [1.5.0](https://github.com/googleapis/python-grafeas/compare/v1.4.5...v1.5.0) (2022-07-14)


### Features

* Add `Digest`, `FileLocation` and `License` ([#186](https://github.com/googleapis/python-grafeas/issues/186)) ([69b5e8b](https://github.com/googleapis/python-grafeas/commit/69b5e8b7fe9162f93a2141a30a94e0bf637af433))
* add audience parameter ([59cb75d](https://github.com/googleapis/python-grafeas/commit/59cb75d9b2beeaaa25ab4cd057bcbd5efc5796d7))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#196](https://github.com/googleapis/python-grafeas/issues/196)) ([61bc475](https://github.com/googleapis/python-grafeas/commit/61bc475542fec60ed8a8ff6b4aecf66e61b5a53a))
* require python 3.7+ ([#195](https://github.com/googleapis/python-grafeas/issues/195)) ([08f46fd](https://github.com/googleapis/python-grafeas/commit/08f46fdaf38d76c31f97616e3f9e379e496b189a))

## [1.4.5](https://github.com/googleapis/python-grafeas/compare/v1.4.4...v1.4.5) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#182](https://github.com/googleapis/python-grafeas/issues/182)) ([d20665c](https://github.com/googleapis/python-grafeas/commit/d20665c84379e260cd2d4470ba8b000f0336a8d2))


### Documentation

* fix changelog header to consistent size ([#181](https://github.com/googleapis/python-grafeas/issues/181)) ([ac19dbf](https://github.com/googleapis/python-grafeas/commit/ac19dbf79e1d29205ecd36d8ef185c615ee7a691))

## [1.4.4](https://github.com/googleapis/python-grafeas/compare/v1.4.3...v1.4.4) (2022-05-05)


### Documentation

* fix type in docstring for map fields ([30b3cba](https://github.com/googleapis/python-grafeas/commit/30b3cba74aec079cd7ac29d08b55dae7caaf8018))

## [1.4.3](https://github.com/googleapis/python-grafeas/compare/v1.4.2...v1.4.3) (2022-03-04)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#150](https://github.com/googleapis/python-grafeas/issues/150)) ([86c3ea1](https://github.com/googleapis/python-grafeas/commit/86c3ea1f23d518a56c350cb5f26b8c651d38c1e4))
* **deps:** require proto-plus>=1.15.0 ([86c3ea1](https://github.com/googleapis/python-grafeas/commit/86c3ea1f23d518a56c350cb5f26b8c651d38c1e4))

## [1.4.2](https://github.com/googleapis/python-grafeas/compare/v1.4.1...v1.4.2) (2022-02-26)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([71ab2a6](https://github.com/googleapis/python-grafeas/commit/71ab2a6719a1ff50ba13dc521dfee54f238b7dc3))


### Documentation

* add generated snippets ([#147](https://github.com/googleapis/python-grafeas/issues/147)) ([6fcc520](https://github.com/googleapis/python-grafeas/commit/6fcc52016e3feca62b171ea4e6c70644302263c9))

## [1.4.1](https://github.com/googleapis/python-grafeas/compare/v1.4.0...v1.4.1) (2022-01-11)


### Bug Fixes

* include the compliance protos ([#134](https://github.com/googleapis/python-grafeas/issues/134)) ([6a8f2d1](https://github.com/googleapis/python-grafeas/commit/6a8f2d151d6e207e2005ee21b7e0ba34e58b0e09))

## [1.4.0](https://www.github.com/googleapis/python-grafeas/compare/v1.3.1...v1.4.0) (2021-11-03)


### Features

* Add compliance and intoto attestation protos ([#123](https://www.github.com/googleapis/python-grafeas/issues/123)) ([ff88a63](https://www.github.com/googleapis/python-grafeas/commit/ff88a6388c1117d17f5e33e28aa1c7e090b34659))

## [1.3.1](https://www.github.com/googleapis/python-grafeas/compare/v1.3.0...v1.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([b90b6fe](https://www.github.com/googleapis/python-grafeas/commit/b90b6fe80fe7358a245109b8c331bddba6f68e7e))
* **deps:** require google-api-core >= 1.28.0 ([b90b6fe](https://www.github.com/googleapis/python-grafeas/commit/b90b6fe80fe7358a245109b8c331bddba6f68e7e))


### Documentation

* list oneofs in docstring ([b90b6fe](https://www.github.com/googleapis/python-grafeas/commit/b90b6fe80fe7358a245109b8c331bddba6f68e7e))

## [1.3.0](https://www.github.com/googleapis/python-grafeas/compare/v1.2.0...v1.3.0) (2021-10-14)


### Features

* add support for python 3.10 ([#117](https://www.github.com/googleapis/python-grafeas/issues/117)) ([ef1fa8e](https://www.github.com/googleapis/python-grafeas/commit/ef1fa8e13cdadcd8b41cbb84313b472bc313f7ea))

## [1.2.0](https://www.github.com/googleapis/python-grafeas/compare/v1.1.4...v1.2.0) (2021-10-08)


### Features

* add context manager support in client ([#114](https://www.github.com/googleapis/python-grafeas/issues/114)) ([13240ae](https://www.github.com/googleapis/python-grafeas/commit/13240ae230782816916edda9e665c9457620a094))

## [1.1.4](https://www.github.com/googleapis/python-grafeas/compare/v1.1.3...v1.1.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([ce7afa0](https://www.github.com/googleapis/python-grafeas/commit/ce7afa03c39588832beaa9a0307b79ba1fac88f6))

## [1.1.3](https://www.github.com/googleapis/python-grafeas/compare/v1.1.2...v1.1.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([594f8d1](https://www.github.com/googleapis/python-grafeas/commit/594f8d19b3515c1cadab9fdacbba4317d4b43b29))

## [1.1.2](https://www.github.com/googleapis/python-grafeas/compare/v1.1.1...v1.1.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#88](https://www.github.com/googleapis/python-grafeas/issues/88)) ([81a0635](https://www.github.com/googleapis/python-grafeas/commit/81a06350840a854631ea9997d1c851aa62883d4b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#84](https://www.github.com/googleapis/python-grafeas/issues/84)) ([2849415](https://www.github.com/googleapis/python-grafeas/commit/28494150a4f0f4fbf1d70161e494ad3faf511412))


### Miscellaneous Chores

* release as 1.1.2 ([#89](https://www.github.com/googleapis/python-grafeas/issues/89)) ([508aa4d](https://www.github.com/googleapis/python-grafeas/commit/508aa4dc1c61dfc4cb12ed16c062977ed3f324ba))

## [1.1.1](https://www.github.com/googleapis/python-grafeas/compare/v1.1.0...v1.1.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#83](https://www.github.com/googleapis/python-grafeas/issues/83)) ([1ada5bc](https://www.github.com/googleapis/python-grafeas/commit/1ada5bceefcbe750d40613614fccf5ad3a94fec5))

## [1.1.0](https://www.github.com/googleapis/python-grafeas/compare/v1.0.1...v1.1.0) (2021-05-20)


### Features

* bump release level to production/stable ([#71](https://www.github.com/googleapis/python-grafeas/issues/71)) ([53bd8a5](https://www.github.com/googleapis/python-grafeas/commit/53bd8a50ab731cf43d0c789198d221c7fbff6fb6))

## [1.0.1](https://www.github.com/googleapis/python-grafeas/compare/v1.0.0...v1.0.1) (2020-08-12)


### Bug Fixes

* remove gapic surface ([#42](https://www.github.com/googleapis/python-grafeas/issues/42)) ([aed68fe](https://www.github.com/googleapis/python-grafeas/commit/aed68fe9a83f041097d8a34f95eb89a1042b7b14))

## [1.0.0](https://www.github.com/googleapis/python-grafeas/compare/v0.4.1...v1.0.0) (2020-08-11)


### ⚠ BREAKING CHANGES

* generate with microgenerator (#36)

### Features

* generate with microgenerator ([#36](https://www.github.com/googleapis/python-grafeas/issues/36)) ([2785cc2](https://www.github.com/googleapis/python-grafeas/commit/2785cc23c3c59457d9f42a9ef1321c2ad0fade47))

## [0.4.1](https://www.github.com/googleapis/python-grafeas/compare/v0.4.0...v0.4.1) (2020-06-25)


### Bug Fixes

* update retry config ([#24](https://www.github.com/googleapis/python-grafeas/issues/24)) ([122ec6a](https://www.github.com/googleapis/python-grafeas/commit/122ec6a2fdf93ad745b6c275defa0bb809f1d005))

## [0.4.0](https://www.github.com/googleapis/python-grafeas/compare/v0.3.0...v0.4.0) (2020-02-07)


### Features

* **grafeas:** add support for upgrade notes; add `cpe` and `last_scan_time` to `DiscoveryOccurrence`; add `source_update_time` to `VulnerabilityNote` (via synth) ([#10084](https://www.github.com/googleapis/python-grafeas/issues/10084)) ([2ee967b](https://www.github.com/googleapis/python-grafeas/commit/2ee967b916e663bacbda8c391528cdca3a1117fd))


### Bug Fixes

* **grafeas:** deprecate resource name helper methods (via synth) ([#9835](https://www.github.com/googleapis/python-grafeas/issues/9835)) ([a2c26d9](https://www.github.com/googleapis/python-grafeas/commit/a2c26d9b60194d305f8cb2b8ec4a4a33d7bf3686))

## 0.3.0

10-10-2019 11:28 PDT


### Implementation Changes
- Remove send / receive message size limit (via synth). ([#8981](https://github.com/googleapis/google-cloud-python/pull/8981))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 0.2.0

07-12-2019 17:04 PDT


### Implementation Changes
- replace `min_affected_version` w/ `affected_version_{start,end}` (via synth).  ([#8465](https://github.com/googleapis/google-cloud-python/pull/8465))
- Allow kwargs to be passed to create_channel, update templates (via synth). ([#8391](https://github.com/googleapis/google-cloud-python/pull/8391))

### New Features
- Update list method docstrings (via synth). ([#8510](https://github.com/googleapis/google-cloud-python/pull/8510))

### Documentation
- Update READMEs. ([#8456](https://github.com/googleapis/google-cloud-python/pull/8456))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.1.0

06-17-2019 10:44 PDT

### New Features
- Initial release of the Grafeas client library. ([#8186](https://github.com/googleapis/google-cloud-python/pull/8186))
