# Changelog

### [1.4.1](https://github.com/googleapis/python-eventarc/compare/v1.4.0...v1.4.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#84](https://github.com/googleapis/python-eventarc/issues/84)) ([988eff8](https://github.com/googleapis/python-eventarc/commit/988eff8b621c91bb0e6b3844e36d5b918b9056b6))

## [1.4.0](https://github.com/googleapis/python-eventarc/compare/v1.3.0...v1.4.0) (2022-02-04)


### Features

* Add Channel and ChannelConnection resources ([#72](https://github.com/googleapis/python-eventarc/issues/72)) ([4d89018](https://github.com/googleapis/python-eventarc/commit/4d8901835ea498cf9ba3fd289f5c078f1eafe7a7))

## [1.3.0](https://github.com/googleapis/python-eventarc/compare/v1.2.1...v1.3.0) (2022-02-03)


### Features

* add api key support ([#68](https://github.com/googleapis/python-eventarc/issues/68)) ([96e07bb](https://github.com/googleapis/python-eventarc/commit/96e07bbbfbb75aa16d33ee9e0984144949e5adc3))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([6bffd75](https://github.com/googleapis/python-eventarc/commit/6bffd757478617fe6ffff905f42fc702a0cb1262))

### [1.2.1](https://www.github.com/googleapis/python-eventarc/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([f509558](https://www.github.com/googleapis/python-eventarc/commit/f509558fe1967d7b0fc65c27a1a0f498bddaa915))
* **deps:** require google-api-core >= 1.28.0 ([f509558](https://www.github.com/googleapis/python-eventarc/commit/f509558fe1967d7b0fc65c27a1a0f498bddaa915))


### Documentation

* list oneofs in docstring ([f509558](https://www.github.com/googleapis/python-eventarc/commit/f509558fe1967d7b0fc65c27a1a0f498bddaa915))

## [1.2.0](https://www.github.com/googleapis/python-eventarc/compare/v1.1.0...v1.2.0) (2021-10-14)


### Features

* add support for python 3.10 ([#47](https://www.github.com/googleapis/python-eventarc/issues/47)) ([987360c](https://www.github.com/googleapis/python-eventarc/commit/987360ceded2027693e3ba148453f0ccfd50d2ce))

## [1.1.0](https://www.github.com/googleapis/python-eventarc/compare/v1.0.2...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#44](https://www.github.com/googleapis/python-eventarc/issues/44)) ([d732a44](https://www.github.com/googleapis/python-eventarc/commit/d732a44510336c7725809b797d082e4fc58c444c))

### [1.0.2](https://www.github.com/googleapis/python-eventarc/compare/v1.0.1...v1.0.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([406ac83](https://www.github.com/googleapis/python-eventarc/commit/406ac83dc4f568500c87ce8ff7b6aa61000252b3))

### [1.0.1](https://www.github.com/googleapis/python-eventarc/compare/v1.0.0...v1.0.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([d940eea](https://www.github.com/googleapis/python-eventarc/commit/d940eeadf232c1c4e74e4f86a65367a2bf37f428))

## [1.0.0](https://www.github.com/googleapis/python-eventarc/compare/v0.2.2...v1.0.0) (2021-08-03)


### Features

* bump release level to production/stable ([#25](https://www.github.com/googleapis/python-eventarc/issues/25)) ([bf70c36](https://www.github.com/googleapis/python-eventarc/commit/bf70c364be632440d3af774e7ddbdf83661a9432))

### [0.2.2](https://www.github.com/googleapis/python-eventarc/compare/v0.2.1...v0.2.2) (2021-07-30)


### Features

* add Samples section to CONTRIBUTING.rst ([#17](https://www.github.com/googleapis/python-eventarc/issues/17)) ([7e2cd4a](https://www.github.com/googleapis/python-eventarc/commit/7e2cd4a1fb857e9992425726bbc93ff2827fea49))


### Bug Fixes

* enable self signed jwt for grpc ([#21](https://www.github.com/googleapis/python-eventarc/issues/21)) ([c9af910](https://www.github.com/googleapis/python-eventarc/commit/c9af9101a3d16395b6ccdecdfd6676394741f686))


### Miscellaneous Chores

* release as 0.2.2 ([#22](https://www.github.com/googleapis/python-eventarc/issues/22)) ([0b26e99](https://www.github.com/googleapis/python-eventarc/commit/0b26e9953c2690f2c71d87681523afd6299af638))

### [0.2.1](https://www.github.com/googleapis/python-eventarc/compare/v0.2.0...v0.2.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#16](https://www.github.com/googleapis/python-eventarc/issues/16)) ([74277de](https://www.github.com/googleapis/python-eventarc/commit/74277dee9067a109e0a76c5fd9fbfd7cac696c80))

## [0.2.0](https://www.github.com/googleapis/python-eventarc/compare/v0.1.0...v0.2.0) (2021-07-14)


### Features

* add always_use_jwt_access ([#9](https://www.github.com/googleapis/python-eventarc/issues/9)) ([2ce20e8](https://www.github.com/googleapis/python-eventarc/commit/2ce20e89a2d15b43e6f72bdcec1741013d1442f2))


### Bug Fixes

* disable always_use_jwt_access ([#13](https://www.github.com/googleapis/python-eventarc/issues/13)) ([d4db355](https://www.github.com/googleapis/python-eventarc/commit/d4db35506e0e0ef4feec76260b3eda4e6ebb8b38))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-eventarc/issues/1127)) ([#4](https://www.github.com/googleapis/python-eventarc/issues/4)) ([18a491d](https://www.github.com/googleapis/python-eventarc/commit/18a491de894bede3d1d675c0bbc884def6eaaf6d))

## 0.1.0 (2021-06-15)


### Features

* generate v1 ([bb2fbd0](https://www.github.com/googleapis/python-eventarc/commit/bb2fbd08b73879699d2c2df13693e15bafde7f65))
