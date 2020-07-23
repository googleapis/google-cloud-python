# Changelog

### [1.4.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.1...v1.4.2) (2020-07-23)


### Bug Fixes

* getattr on an invalid field raises AttributeError ([#73](https://www.github.com/googleapis/proto-plus-python/issues/73)) ([74ea8f0](https://www.github.com/googleapis/proto-plus-python/commit/74ea8f0cd9083939e53d1de2450b649500281b9a)), closes [#31](https://www.github.com/googleapis/proto-plus-python/issues/31)

### [1.4.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.0...v1.4.1) (2020-07-23)


### Bug Fixes

* tweak publish ci task ([#65](https://www.github.com/googleapis/proto-plus-python/issues/65)) ([983189c](https://www.github.com/googleapis/proto-plus-python/commit/983189c5effa25fb9365eb63caddb425d3cfb2b5))

## [1.4.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.2...v1.4.0) (2020-07-23)


### Features

* prevent unnecessary copies when deserializing proto ([#63](https://www.github.com/googleapis/proto-plus-python/issues/63)) ([5e1c061](https://www.github.com/googleapis/proto-plus-python/commit/5e1c0619b5f4c5d2a6a75ae6d45a53fef2e58823))

### [1.3.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.1...v1.3.2) (2020-07-22)


### Bug Fixes

* correctly handle passed in vanilla datetime.datetime ([#57](https://www.github.com/googleapis/proto-plus-python/issues/57)) ([a770816](https://www.github.com/googleapis/proto-plus-python/commit/a770816197cbce60ee023bd5b6ee6bd2d970ded8)), closes [googleapis/gapic-generator-python#544](https://www.github.com/googleapis/gapic-generator-python/issues/544)
* update encrypted pypi passwd ([#58](https://www.github.com/googleapis/proto-plus-python/issues/58)) ([d985233](https://www.github.com/googleapis/proto-plus-python/commit/d9852336d83717cb9ff24b6bec3ef1463239fea1))

### [1.3.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.0...v1.3.1) (2020-07-21)


### Bug Fixes

* tweak pypi circleci task ([#54](https://www.github.com/googleapis/proto-plus-python/issues/54)) ([89c49d7](https://www.github.com/googleapis/proto-plus-python/commit/89c49d700d4b6e9a434fbfced8ca39d430dd22f9))


### Documentation

* linkify pypi badge ([#50](https://www.github.com/googleapis/proto-plus-python/issues/50)) ([8ff08e2](https://www.github.com/googleapis/proto-plus-python/commit/8ff08e21e75570aad71c5e62f4c78b43139b5df2))

## [1.3.0](https://www.github.com/googleapis/proto-plus-python/compare/1.2.0...v1.3.0) (2020-07-16)


### Features

* add convenience methods to convert to/from json ([#39](https://www.github.com/googleapis/proto-plus-python/issues/39)) ([2868946](https://www.github.com/googleapis/proto-plus-python/commit/286894609843f568c9ff367ab79542783642b801))
* add DatetimeWithNanoseconds class to maintain Timestamp pb precision. ([#40](https://www.github.com/googleapis/proto-plus-python/issues/40)) ([a17ccd5](https://www.github.com/googleapis/proto-plus-python/commit/a17ccd52c7fa3609ce79fde84b931c0693f53171)), closes [#38](https://www.github.com/googleapis/proto-plus-python/issues/38)
* add support for proto3 optional fields ([#35](https://www.github.com/googleapis/proto-plus-python/issues/35)) ([0eb5762](https://www.github.com/googleapis/proto-plus-python/commit/0eb5762681e315635db1dffd583d91a4f32cba43))


### Bug Fixes

* Modify setup.py to indicate this is google maintained ([#45](https://www.github.com/googleapis/proto-plus-python/issues/45)) ([96b3b00](https://www.github.com/googleapis/proto-plus-python/commit/96b3b00dd6712fe44e71dedf8080b20544e95416))
