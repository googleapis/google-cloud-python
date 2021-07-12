# Changelog

## [2.6.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.5.0...v2.6.0) (2021-07-09)


### Features

* add always_use_jwt_access ([#137](https://www.github.com/googleapis/python-secret-manager/issues/137)) ([e1ee4c7](https://www.github.com/googleapis/python-secret-manager/commit/e1ee4c76ba5eb12b3fdd54eed1b2498eac386030))
* Tune Secret Manager auto retry parameters ([#144](https://www.github.com/googleapis/python-secret-manager/issues/144)) ([494f3f6](https://www.github.com/googleapis/python-secret-manager/commit/494f3f638203fd683e36bdf882d8a29b9b303dc5))


### Bug Fixes

* disable always_use_jwt_access ([#143](https://www.github.com/googleapis/python-secret-manager/issues/143)) ([47cdda9](https://www.github.com/googleapis/python-secret-manager/commit/47cdda91a0962805f8553ec9f2ac779d99c3e291))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-secret-manager/issues/1127)) ([#132](https://www.github.com/googleapis/python-secret-manager/issues/132)) ([6a10592](https://www.github.com/googleapis/python-secret-manager/commit/6a105926ec39939398deca5b6fbfb05290615bfd)), closes [#1126](https://www.github.com/googleapis/python-secret-manager/issues/1126)

## [2.5.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.4.0...v2.5.0) (2021-06-07)


### Features

* Etags in Secret Manager ([#116](https://www.github.com/googleapis/python-secret-manager/issues/116)) ([6ec898e](https://www.github.com/googleapis/python-secret-manager/commit/6ec898e4d671344a3f4a8322417d38c8cf606f1b))


### Bug Fixes

* **deps:** add packaging requirement ([#119](https://www.github.com/googleapis/python-secret-manager/issues/119)) ([0937207](https://www.github.com/googleapis/python-secret-manager/commit/0937207c59753e0b6b595f2ff708826ee3a2c4bd))

## [2.4.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.3.0...v2.4.0) (2021-03-31)


### Features

* Rotation for Secrets ([#95](https://www.github.com/googleapis/python-secret-manager/issues/95)) ([c0aea0f](https://www.github.com/googleapis/python-secret-manager/commit/c0aea0f4f932a2c78c3f5e747092279290611a65))


### Bug Fixes

* use correct retry deadline ([#92](https://www.github.com/googleapis/python-secret-manager/issues/92)) ([5f57e66](https://www.github.com/googleapis/python-secret-manager/commit/5f57e6615b2bf0793626dc574de94d76915f7489))

## [2.3.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.2.0...v2.3.0) (2021-03-11)


### Features

* add topic field to Secret ([#80](https://www.github.com/googleapis/python-secret-manager/issues/80)) ([f83c035](https://www.github.com/googleapis/python-secret-manager/commit/f83c03517a7d32f5f53ea5511c41b855ab955eae))

## [2.2.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.1.0...v2.2.0) (2021-01-20)


### Features

* added expire_time and ttl fields to Secret ([#70](https://www.github.com/googleapis/python-secret-manager/issues/70)) ([92c4a98](https://www.github.com/googleapis/python-secret-manager/commit/92c4a983bcfb127eb4eb37a1a25e8c773a5fdcbf))


### Bug Fixes

* remove client side recv limits ([#65](https://www.github.com/googleapis/python-secret-manager/issues/65)) ([383bde5](https://www.github.com/googleapis/python-secret-manager/commit/383bde5a7552ab62dc7c1d36a533401ec9430609))

## [2.1.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.0.0...v2.1.0) (2020-12-03)


### Features

* add common resource helper methods; expose client transport; add shebang to fixup scripts ([#57](https://www.github.com/googleapis/python-secret-manager/issues/57)) ([b5c022b](https://www.github.com/googleapis/python-secret-manager/commit/b5c022bebd36f82bb538d4d8467f25685f84f8bc))

## [2.0.0](https://www.github.com/googleapis/python-secret-manager/compare/v1.0.0...v2.0.0) (2020-09-15)


### ⚠ BREAKING CHANGES

* migrate to use microgen. See [Migration Guide](https://googleapis.dev/python/secretmanager/latest/UPGRADING.html) (#44)

### Features

* migrate to use microgen ([#44](https://www.github.com/googleapis/python-secret-manager/issues/44)) ([4196032](https://www.github.com/googleapis/python-secret-manager/commit/41960323415701f3b358be201857fe04f58652be))


### Bug Fixes

* update default retry configs ([#31](https://www.github.com/googleapis/python-secret-manager/issues/31)) ([5f8689c](https://www.github.com/googleapis/python-secret-manager/commit/5f8689c9a1d6001d2873158c13cbb9a95b33fb97))

## [1.0.0](https://www.github.com/googleapis/python-secret-manager/compare/v0.2.0...v1.0.0) (2020-05-20)


### Features

* release as production/stable ([#24](https://www.github.com/googleapis/python-secret-manager/issues/24)) ([39a8cc8](https://www.github.com/googleapis/python-secret-manager/commit/39a8cc8f631569c82d1cbffc6a9bbb440d380683))

## [0.2.0](https://www.github.com/googleapis/python-secret-manager/compare/v0.1.1...v0.2.0) (2020-03-06)


### Features

* add support for v1 ([#15](https://www.github.com/googleapis/python-secret-manager/issues/15)) ([cc97391](https://www.github.com/googleapis/python-secret-manager/commit/cc973912f40166c2574caad5a8266eddff6ae7a6))

### [0.1.1](https://www.github.com/googleapis/python-secret-manager/compare/v0.1.0...v0.1.1) (2020-01-06)


### Bug Fixes

* remove deprecations from path helpers ([#9](https://www.github.com/googleapis/python-secret-manager/issues/9)) ([723ef9f](https://www.github.com/googleapis/python-secret-manager/commit/723ef9fb59f86e434fb6c9fcb5857bdd492358f6))

## 0.1.0 (2019-12-20)


### Features

* initial generation of secret manager ([1c193f8](https://www.github.com/googleapis/python-secret-manager/commit/1c193f815dcb2a2093b467576d3704e637ae0091))
