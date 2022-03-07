# Changelog

### [1.3.1](https://github.com/googleapis/python-org-policy/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#126](https://github.com/googleapis/python-org-policy/issues/126)) ([ad3f4f4](https://github.com/googleapis/python-org-policy/commit/ad3f4f49d15f290db7ac19258960a5731a73544e))
* **deps:** require proto-plus>=1.15.0 ([ad3f4f4](https://github.com/googleapis/python-org-policy/commit/ad3f4f49d15f290db7ac19258960a5731a73544e))

## [1.3.0](https://github.com/googleapis/python-org-policy/compare/v1.2.1...v1.3.0) (2022-02-18)


### Features

* add api key support ([#113](https://github.com/googleapis/python-org-policy/issues/113)) ([90fa145](https://github.com/googleapis/python-org-policy/commit/90fa1459bfce8d8980fd8fd1767b8e83026e48a9))
* Deprecates AlternativePolicySpec ([#119](https://github.com/googleapis/python-org-policy/issues/119)) ([10dde6e](https://github.com/googleapis/python-org-policy/commit/10dde6e51311a72f29c5efe0e375d751543c0211))


### Bug Fixes

* remove tests directory from wheel ([#121](https://github.com/googleapis/python-org-policy/issues/121)) ([90439ab](https://github.com/googleapis/python-org-policy/commit/90439ab7d48c8e6cd679bee3b5fb071bb69776f4))
* resolve DuplicateCredentialArgs error when using credentials_file ([0dd6187](https://github.com/googleapis/python-org-policy/commit/0dd618763d322b9bec56fd27e62a0dfad4fc5e06))


### Documentation

* add generated snippets  ([#118](https://github.com/googleapis/python-org-policy/issues/118)) ([dae6c2c](https://github.com/googleapis/python-org-policy/commit/dae6c2cc9b3b32ddf751aabd4b0d690003f24bef))

### [1.2.1](https://www.github.com/googleapis/python-org-policy/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([1d6e752](https://www.github.com/googleapis/python-org-policy/commit/1d6e7524d8bfefd52998e887665ab3ba1b507134))
* **deps:** require google-api-core >= 1.28.0 ([1d6e752](https://www.github.com/googleapis/python-org-policy/commit/1d6e7524d8bfefd52998e887665ab3ba1b507134))


### Documentation

* list oneofs in docstring ([1d6e752](https://www.github.com/googleapis/python-org-policy/commit/1d6e7524d8bfefd52998e887665ab3ba1b507134))

## [1.2.0](https://www.github.com/googleapis/python-org-policy/compare/v1.1.0...v1.2.0) (2021-10-14)


### Features

* add support for python 3.10 ([#96](https://www.github.com/googleapis/python-org-policy/issues/96)) ([f5e795a](https://www.github.com/googleapis/python-org-policy/commit/f5e795ac66f5ecb8113f49e82baba1ffde66156f))

## [1.1.0](https://www.github.com/googleapis/python-org-policy/compare/v1.0.2...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#92](https://www.github.com/googleapis/python-org-policy/issues/92)) ([c12c571](https://www.github.com/googleapis/python-org-policy/commit/c12c571606cb7f6467479d7f3ddf7fd4f44dbbee))


### Bug Fixes

* improper types in pagers generation ([3254812](https://www.github.com/googleapis/python-org-policy/commit/3254812ce2adeb32fe44536c3859c44756bd0c89))

### [1.0.2](https://www.github.com/googleapis/python-org-policy/compare/v1.0.1...v1.0.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([c2ea337](https://www.github.com/googleapis/python-org-policy/commit/c2ea337f06189254eeaec9e60fbf273b38e9f2d8))

### [1.0.1](https://www.github.com/googleapis/python-org-policy/compare/v1.0.0...v1.0.1) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#65](https://www.github.com/googleapis/python-org-policy/issues/65)) ([f486869](https://www.github.com/googleapis/python-org-policy/commit/f486869b2c232f2c4934dab8e25637a45f577f9b))
* enable self signed jwt for grpc ([#71](https://www.github.com/googleapis/python-org-policy/issues/71)) ([26c70cd](https://www.github.com/googleapis/python-org-policy/commit/26c70cdc94326d5c312a6f601f2976e67087717b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#66](https://www.github.com/googleapis/python-org-policy/issues/66)) ([9cf6fc8](https://www.github.com/googleapis/python-org-policy/commit/9cf6fc8dbcfe6798a06f0704165dc58af2a5170a))


### Miscellaneous Chores

* release 1.0.1 ([#70](https://www.github.com/googleapis/python-org-policy/issues/70)) ([f0a76b6](https://www.github.com/googleapis/python-org-policy/commit/f0a76b66e5fe5535c01663f01b453c527b960b5f))

## [1.0.0](https://www.github.com/googleapis/python-org-policy/compare/v0.3.0...v1.0.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#59](https://www.github.com/googleapis/python-org-policy/issues/59)) ([6acf334](https://www.github.com/googleapis/python-org-policy/commit/6acf334ca0c306603b49ab64694647985b04e83b))
* bump release level to production/stable ([#50](https://www.github.com/googleapis/python-org-policy/issues/50)) ([2b1da9e](https://www.github.com/googleapis/python-org-policy/commit/2b1da9e03aa82330b0461c78abee2fa75390d238))


### Bug Fixes

* disable always_use_jwt_access ([#62](https://www.github.com/googleapis/python-org-policy/issues/62)) ([b6bf93c](https://www.github.com/googleapis/python-org-policy/commit/b6bf93c535dee1822d3b111a8e96ca6d4d30ba55))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-org-policy/issues/1127)) ([#56](https://www.github.com/googleapis/python-org-policy/issues/56)) ([540f601](https://www.github.com/googleapis/python-org-policy/commit/540f6018e9631664c0fda97ca1d0db90ab5783fd)), closes [#1126](https://www.github.com/googleapis/python-org-policy/issues/1126)

## [0.3.0](https://www.github.com/googleapis/python-org-policy/compare/v0.2.0...v0.3.0) (2021-05-16)


### Features

* add `from_service_account_info` ([#24](https://www.github.com/googleapis/python-org-policy/issues/24)) ([cb5881d](https://www.github.com/googleapis/python-org-policy/commit/cb5881dac8121617fda5a4d9df9f70c80dcc8735))
* support self-signed JWT flow for service accounts ([aade679](https://www.github.com/googleapis/python-org-policy/commit/aade679d6c04808408110292a3de805fa3364286))


### Bug Fixes

* add async client to %name_%version/init.py chore: add autogenerated snippets ([aade679](https://www.github.com/googleapis/python-org-policy/commit/aade679d6c04808408110292a3de805fa3364286))
* **deps:** add packaging requirement ([#48](https://www.github.com/googleapis/python-org-policy/issues/48)) ([3056b54](https://www.github.com/googleapis/python-org-policy/commit/3056b54822f11f0b3e2caa220a115f223bac438b))
* Fixed broken url for package. ([#38](https://www.github.com/googleapis/python-org-policy/issues/38)) ([7b27dac](https://www.github.com/googleapis/python-org-policy/commit/7b27dac39dbdda9789533502356cee6f5d9303c2)), closes [#37](https://www.github.com/googleapis/python-org-policy/issues/37)
* use correct retry deadline ([#28](https://www.github.com/googleapis/python-org-policy/issues/28)) ([5d1f86c](https://www.github.com/googleapis/python-org-policy/commit/5d1f86c3121c778f71205364af43e1f26f4c12c9))

## [0.2.0](https://www.github.com/googleapis/python-org-policy/compare/v0.1.2...v0.2.0) (2021-03-01)


### Features

* add v2 ([#21](https://www.github.com/googleapis/python-org-policy/issues/21)) ([8aaa847](https://www.github.com/googleapis/python-org-policy/commit/8aaa8472df478be10b43b34b4346084131c6e465))

### [0.1.2](https://www.github.com/googleapis/python-org-policy/compare/v0.1.1...v0.1.2) (2020-05-08)


### Bug Fixes

* add missing __init__.py ([b786474](https://www.github.com/googleapis/python-org-policy/commit/b78647490341488d3264346ef19d8c7a28f48a06))

### [0.1.1](https://www.github.com/googleapis/python-org-policy/compare/v0.1.0...v0.1.1) (2020-05-08)


### Bug Fixes

* fix setup.py ([d18203a](https://www.github.com/googleapis/python-org-policy/commit/d18203af0f7b2728ccd0695ef32cc0508fafce4c))

## 0.1.0 (2020-05-07)


### Features

* generate v1 ([51dfc91](https://www.github.com/googleapis/python-org-policy/commit/51dfc91166552ab866ee364cdf8bb6f7d0ebe41a))
