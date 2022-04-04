# Changelog

## [2.10.0](https://github.com/googleapis/python-secret-manager/compare/v2.9.2...v2.10.0) (2022-04-04)


### Features

* Added support for accessing secret versions by alias ([#281](https://github.com/googleapis/python-secret-manager/issues/281)) ([6c5cd29](https://github.com/googleapis/python-secret-manager/commit/6c5cd296c888d1839ffdac1a8d09ca568c99d36d))

### [2.9.2](https://github.com/googleapis/python-secret-manager/compare/v2.9.1...v2.9.2) (2022-03-13)


### Documentation

* **samples:** add checksum snippets ([#255](https://github.com/googleapis/python-secret-manager/issues/255)) ([2095a04](https://github.com/googleapis/python-secret-manager/commit/2095a04e73f2437cc4ccbaa272b1998422d18fe3))

### [2.9.1](https://github.com/googleapis/python-secret-manager/compare/v2.9.0...v2.9.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#260](https://github.com/googleapis/python-secret-manager/issues/260)) ([b6b800b](https://github.com/googleapis/python-secret-manager/commit/b6b800bbb26fbe08dd86ff0d876a70fe67274491))
* **deps:** require proto-plus>=1.15.0 ([b6b800b](https://github.com/googleapis/python-secret-manager/commit/b6b800bbb26fbe08dd86ff0d876a70fe67274491))

## [2.9.0](https://github.com/googleapis/python-secret-manager/compare/v2.8.0...v2.9.0) (2022-02-26)


### Features

* add api key support ([#240](https://github.com/googleapis/python-secret-manager/issues/240)) ([4056e97](https://github.com/googleapis/python-secret-manager/commit/4056e97028a638934de9deea68d29e523fa45a1f))
* add checksums in Secret Manager  ([#244](https://github.com/googleapis/python-secret-manager/issues/244)) ([6c24f70](https://github.com/googleapis/python-secret-manager/commit/6c24f70276333e74b32ba0992e77e24f5f453de5))


### Bug Fixes

* **deps:** move libcst to extras ([#248](https://github.com/googleapis/python-secret-manager/issues/248)) ([9acb791](https://github.com/googleapis/python-secret-manager/commit/9acb7913adc01f41928b85641aea184ffccdf121))
* resolve DuplicateCredentialArgs error when using credentials_file ([6c24f70](https://github.com/googleapis/python-secret-manager/commit/6c24f70276333e74b32ba0992e77e24f5f453de5))


### Documentation

* add generated snippets ([#247](https://github.com/googleapis/python-secret-manager/issues/247)) ([a84c252](https://github.com/googleapis/python-secret-manager/commit/a84c2520b522c8c5d60d7fa32050fe917a30dff2))

## [2.8.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.7.3...v2.8.0) (2021-11-08)


### Features

* add context manager support in client ([#210](https://www.github.com/googleapis/python-secret-manager/issues/210)) ([8d247d4](https://www.github.com/googleapis/python-secret-manager/commit/8d247d4b7f96faa61532ac09ef95e2599c523702))
* add support for python 3.10 ([#214](https://www.github.com/googleapis/python-secret-manager/issues/214)) ([5e3cc7e](https://www.github.com/googleapis/python-secret-manager/commit/5e3cc7ef9a0e3660c9734f989d5b1e82a18d336c))


### Bug Fixes

* **deps:** drop packaging dependency ([6aac11f](https://www.github.com/googleapis/python-secret-manager/commit/6aac11f08d396835f7c4ca71c7a2f2a2a48e96db))
* **deps:** require google-api-core >= 1.28.0 ([6aac11f](https://www.github.com/googleapis/python-secret-manager/commit/6aac11f08d396835f7c4ca71c7a2f2a2a48e96db))


### Documentation

* list oneofs in docstring ([6aac11f](https://www.github.com/googleapis/python-secret-manager/commit/6aac11f08d396835f7c4ca71c7a2f2a2a48e96db))
* **samples:** Add filtered listing samples ([#209](https://www.github.com/googleapis/python-secret-manager/issues/209)) ([316de2d](https://www.github.com/googleapis/python-secret-manager/commit/316de2d68283e4c1da7f4fdc24fc7e6d65adbfd0))

### [2.7.3](https://www.github.com/googleapis/python-secret-manager/compare/v2.7.2...v2.7.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([59c557f](https://www.github.com/googleapis/python-secret-manager/commit/59c557f5acd5de9e12dfa7308fa9fb9e89833fe6))

### [2.7.2](https://www.github.com/googleapis/python-secret-manager/compare/v2.7.1...v2.7.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([b5e0c81](https://www.github.com/googleapis/python-secret-manager/commit/b5e0c818eeca22cae59406693f435595d2b92f8d))

### [2.7.1](https://www.github.com/googleapis/python-secret-manager/compare/v2.7.0...v2.7.1) (2021-09-13)


### Bug Fixes

* add 'dict' type annotation to 'request' ([#193](https://www.github.com/googleapis/python-secret-manager/issues/193)) ([1d5fee4](https://www.github.com/googleapis/python-secret-manager/commit/1d5fee4fe825096947bb125ebcba72fdb6d463c6))

## [2.7.0](https://www.github.com/googleapis/python-secret-manager/compare/v2.6.0...v2.7.0) (2021-08-03)


### Features

* add filter to customize the output of ListSecrets/ListSecretVersions calls ([#161](https://www.github.com/googleapis/python-secret-manager/issues/161)) ([c09615c](https://www.github.com/googleapis/python-secret-manager/commit/c09615c328782f0a15201cb4f2c7387b0a6ce51d))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#153](https://www.github.com/googleapis/python-secret-manager/issues/153)) ([1e8a4aa](https://www.github.com/googleapis/python-secret-manager/commit/1e8a4aae06badda947717217c224366963664bdc))
* enable self signed jwt for grpc ([#158](https://www.github.com/googleapis/python-secret-manager/issues/158)) ([9ebe2b3](https://www.github.com/googleapis/python-secret-manager/commit/9ebe2b3a683de1d710ec3e91b444eb71b2ef0f6b))


### Documentation

* **secretmanager:** add sample code for receiving a Pub/Sub message ([#138](https://www.github.com/googleapis/python-secret-manager/issues/138)) ([51f743d](https://www.github.com/googleapis/python-secret-manager/commit/51f743dfe2de41ef0378fff08c92c506dd11fc2b))


### Miscellaneous Chores

* release as 2.6.1 ([#159](https://www.github.com/googleapis/python-secret-manager/issues/159)) ([b686310](https://www.github.com/googleapis/python-secret-manager/commit/b686310643ec5fbd090a5d58d8a7694bdc6eebb9))
* release as 2.7.0 ([#163](https://www.github.com/googleapis/python-secret-manager/issues/163)) ([b1c148b](https://www.github.com/googleapis/python-secret-manager/commit/b1c148bba25374bd9a62a6b823bf10ffd6215e9e))

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
