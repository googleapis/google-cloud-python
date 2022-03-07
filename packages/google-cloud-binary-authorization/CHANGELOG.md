# Changelog

### [1.2.2](https://github.com/googleapis/python-binary-authorization/compare/v1.2.1...v1.2.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#126](https://github.com/googleapis/python-binary-authorization/issues/126)) ([2b7e982](https://github.com/googleapis/python-binary-authorization/commit/2b7e982e09b85570af842acba3ca6c48831a49e2))

### [1.2.1](https://github.com/googleapis/python-binary-authorization/compare/v1.2.0...v1.2.1) (2022-02-11)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([1f500f5](https://github.com/googleapis/python-binary-authorization/commit/1f500f506715e9028b98e7c42048aacc276fb9b4))

## [1.2.0](https://github.com/googleapis/python-binary-authorization/compare/v1.1.0...v1.2.0) (2022-01-25)


### Features

* add api key support ([#110](https://github.com/googleapis/python-binary-authorization/issues/110)) ([e4b39f0](https://github.com/googleapis/python-binary-authorization/commit/e4b39f0c78e2a8775deac76444c4bc350ec6cc1f))

## [1.1.0](https://www.github.com/googleapis/python-binary-authorization/compare/v1.0.1...v1.1.0) (2021-11-09)


### Features

* **v1beta1:** add new admission rule types to Policy ([#95](https://www.github.com/googleapis/python-binary-authorization/issues/95)) ([f25d17a](https://www.github.com/googleapis/python-binary-authorization/commit/f25d17abaefe4a2d317161ec15b867b33eb3e8ba))
* **v1beta1:** add SystemPolicyV1Beta1 service ([f25d17a](https://www.github.com/googleapis/python-binary-authorization/commit/f25d17abaefe4a2d317161ec15b867b33eb3e8ba))
* **v1beta1:** update SignatureAlgorithm enum to match algorithm names in KMS ([f25d17a](https://www.github.com/googleapis/python-binary-authorization/commit/f25d17abaefe4a2d317161ec15b867b33eb3e8ba))

### [1.0.1](https://www.github.com/googleapis/python-binary-authorization/compare/v1.0.0...v1.0.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([d02c2fd](https://www.github.com/googleapis/python-binary-authorization/commit/d02c2fdbc52d4dc5f8ca333e99d7e7160dcd23e8))
* **deps:** require google-api-core >= 1.28.0 ([d02c2fd](https://www.github.com/googleapis/python-binary-authorization/commit/d02c2fdbc52d4dc5f8ca333e99d7e7160dcd23e8))


### Documentation

* list oneofs in docstring ([d02c2fd](https://www.github.com/googleapis/python-binary-authorization/commit/d02c2fdbc52d4dc5f8ca333e99d7e7160dcd23e8))

## [1.0.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.6.0...v1.0.0) (2021-10-22)


### Features

* bump release level to production/stable ([#77](https://www.github.com/googleapis/python-binary-authorization/issues/77)) ([f893ce0](https://www.github.com/googleapis/python-binary-authorization/commit/f893ce0fac64aa9ab153cfff1c9323f235cb4a27))

## [0.6.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.5.0...v0.6.0) (2021-10-13)


### Features

* add trove classifier for python 3.9 and python 3.10 ([#87](https://www.github.com/googleapis/python-binary-authorization/issues/87)) ([73acd98](https://www.github.com/googleapis/python-binary-authorization/commit/73acd98ae81bf43591f7599e70e7f1b264eafceb))

## [0.5.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.4.1...v0.5.0) (2021-10-08)


### Features

* add context manager support in client ([#84](https://www.github.com/googleapis/python-binary-authorization/issues/84)) ([0991f56](https://www.github.com/googleapis/python-binary-authorization/commit/0991f564af01dc8b0172693290a9aba566035848))

### [0.4.1](https://www.github.com/googleapis/python-binary-authorization/compare/v0.4.0...v0.4.1) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([789e8c5](https://www.github.com/googleapis/python-binary-authorization/commit/789e8c5e459bf6a2eafada84fe586ba9524efc05))

## [0.4.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.3.1...v0.4.0) (2021-09-24)


### Features

* add binaryauthorization v1 ([#74](https://www.github.com/googleapis/python-binary-authorization/issues/74)) ([cd828ec](https://www.github.com/googleapis/python-binary-authorization/commit/cd828ec45edb5a297607ea7e9f94c39e68ef2d7d))
* set binaryauthorization_v1 as the default version ([cd828ec](https://www.github.com/googleapis/python-binary-authorization/commit/cd828ec45edb5a297607ea7e9f94c39e68ef2d7d))


### Bug Fixes

* add 'dict' annotation type to 'request' ([7045df0](https://www.github.com/googleapis/python-binary-authorization/commit/7045df0313b0c6f05662745e90c28626d292d64e))
* require grafeas>=1.1.2, proto-plus>=1.15.0 ([cd828ec](https://www.github.com/googleapis/python-binary-authorization/commit/cd828ec45edb5a297607ea7e9f94c39e68ef2d7d))


### Documentation

* fix broken links in README ([cd828ec](https://www.github.com/googleapis/python-binary-authorization/commit/cd828ec45edb5a297607ea7e9f94c39e68ef2d7d))

### [0.3.1](https://www.github.com/googleapis/python-binary-authorization/compare/v0.3.0...v0.3.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#55](https://www.github.com/googleapis/python-binary-authorization/issues/55)) ([0ca0dc2](https://www.github.com/googleapis/python-binary-authorization/commit/0ca0dc2671bb8920f56bcbd057b9a13d7b23bf7f))
* enable self signed jwt for grpc ([#61](https://www.github.com/googleapis/python-binary-authorization/issues/61)) ([1a65f17](https://www.github.com/googleapis/python-binary-authorization/commit/1a65f171f677b7ca659ffe98051f432bed342209))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#56](https://www.github.com/googleapis/python-binary-authorization/issues/56)) ([c641b6c](https://www.github.com/googleapis/python-binary-authorization/commit/c641b6c148779e1952149e5ce5edf62fa0a1c642))


### Miscellaneous Chores

* release 0.3.1 ([#60](https://www.github.com/googleapis/python-binary-authorization/issues/60)) ([e2b54b5](https://www.github.com/googleapis/python-binary-authorization/commit/e2b54b5a97f23c6a01bce151b4fb5809f089f1d6))

## [0.3.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.2.2...v0.3.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#48](https://www.github.com/googleapis/python-binary-authorization/issues/48)) ([63a3c9a](https://www.github.com/googleapis/python-binary-authorization/commit/63a3c9a8f8c9ab97436882adc7658260aa66df9d))


### Bug Fixes

* disable always_use_jwt_access ([#52](https://www.github.com/googleapis/python-binary-authorization/issues/52)) ([b840980](https://www.github.com/googleapis/python-binary-authorization/commit/b84098014328d14531caafe30585a5bd55c216f4))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-binary-authorization/issues/1127)) ([#43](https://www.github.com/googleapis/python-binary-authorization/issues/43)) ([726d589](https://www.github.com/googleapis/python-binary-authorization/commit/726d58920de4e97a70cbbe1fd88ac427224ba1ea)), closes [#1126](https://www.github.com/googleapis/python-binary-authorization/issues/1126)

### [0.2.2](https://www.github.com/googleapis/python-binary-authorization/compare/v0.2.1...v0.2.2) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#39](https://www.github.com/googleapis/python-binary-authorization/issues/39)) ([a90d7f4](https://www.github.com/googleapis/python-binary-authorization/commit/a90d7f46ca54c3bf805208bff157cfbc48a14234))

### [0.2.1](https://www.github.com/googleapis/python-binary-authorization/compare/v0.2.0...v0.2.1) (2021-05-25)


### Bug Fixes

* **deps:** add packaging requirement ([#34](https://www.github.com/googleapis/python-binary-authorization/issues/34)) ([59752a5](https://www.github.com/googleapis/python-binary-authorization/commit/59752a57cd6fb9a9e4d4caeb0b27793ce829d37c))

## [0.2.0](https://www.github.com/googleapis/python-binary-authorization/compare/v0.1.1...v0.2.0) (2021-05-20)


### Features

* Publish Binary Authorization ContinuousValidationEvent proto ([#31](https://www.github.com/googleapis/python-binary-authorization/issues/31)) ([d3d2abe](https://www.github.com/googleapis/python-binary-authorization/commit/d3d2abeb22bad714de0591916c1065fda7305a92))

### [0.1.1](https://www.github.com/googleapis/python-binary-authorization/compare/v0.1.0...v0.1.1) (2021-04-01)


### Bug Fixes

* use correct retry deadline ([#7](https://www.github.com/googleapis/python-binary-authorization/issues/7)) ([3f9bfc2](https://www.github.com/googleapis/python-binary-authorization/commit/3f9bfc2b1c5b6d520716b194daf175e1030135b0))


### Documentation

* update python contributing guide ([#9](https://www.github.com/googleapis/python-binary-authorization/issues/9)) ([b6e095f](https://www.github.com/googleapis/python-binary-authorization/commit/b6e095ff6a1f7422e9f1ce9132d32871f800aab7))

## 0.1.0 (2021-01-08)


### Features

* generate v1beta1 ([06c43f2](https://www.github.com/googleapis/python-binary-authorization/commit/06c43f24701da8f301be5bc04a6ec83a25edc41f))
