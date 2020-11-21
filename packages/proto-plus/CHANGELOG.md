# Changelog

## [1.12.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.11.0...v1.12.0) (2020-11-20)


### Features

* add default values parameter to to_json ([#164](https://www.github.com/googleapis/proto-plus-python/issues/164)) ([691f1b2](https://www.github.com/googleapis/proto-plus-python/commit/691f1b24454502c4ac49a88a09d1c9fbc287b2bd))

## [1.11.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.2...v1.11.0) (2020-10-19)


### Features

* provide a to_dict method ([#154](https://www.github.com/googleapis/proto-plus-python/issues/154)) ([ccf903e](https://www.github.com/googleapis/proto-plus-python/commit/ccf903e3cddfcb1ff539e853594b4342914b7d61)), closes [#153](https://www.github.com/googleapis/proto-plus-python/issues/153) [#151](https://www.github.com/googleapis/proto-plus-python/issues/151)

### [1.10.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.1...v1.10.2) (2020-10-14)


### Documentation

* explain how to use repeated struct.Value ([#148](https://www.github.com/googleapis/proto-plus-python/issues/148)) ([9634ea8](https://www.github.com/googleapis/proto-plus-python/commit/9634ea8fa464c0d34f13469016f23cc2e986d973)), closes [#104](https://www.github.com/googleapis/proto-plus-python/issues/104)

### [1.10.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.0...v1.10.1) (2020-10-08)


### Bug Fixes

* accessing an unset struct_pb2.Value field does not raise ([#140](https://www.github.com/googleapis/proto-plus-python/issues/140)) ([d045cbf](https://www.github.com/googleapis/proto-plus-python/commit/d045cbf058cbb8f4ca98dd06741270fcaee865be))
* add LICENSE and tests to package ([#146](https://www.github.com/googleapis/proto-plus-python/issues/146)) ([815c943](https://www.github.com/googleapis/proto-plus-python/commit/815c9439a1dadb2d4111784eb18ba673ce6e6cc2))

## [1.10.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.9.1...v1.10.0) (2020-09-24)


### Bug Fixes

* loosen tag match for publish_package ([#123](https://www.github.com/googleapis/proto-plus-python/issues/123)) ([67441c9](https://www.github.com/googleapis/proto-plus-python/commit/67441c931b5f00b2e1084ce2539784ae9d9c31e6))
* third party enums don't break first class enums ([#118](https://www.github.com/googleapis/proto-plus-python/issues/118)) ([50b87af](https://www.github.com/googleapis/proto-plus-python/commit/50b87af481bb1f19d10d64e88dc9ee39c2d5b6f8)), closes [#103](https://www.github.com/googleapis/proto-plus-python/issues/103)


## [1.10.0-dev2](https://www.github.com/googleapis/proto-plus-python/compare/v1.9.1...v1.10.0-dev2) (2020-09-21)


### Bug Fixes

* loosen tag match for publish_package ([#123](https://www.github.com/googleapis/proto-plus-python/issues/123)) ([67441c9](https://www.github.com/googleapis/proto-plus-python/commit/67441c931b5f00b2e1084ce2539784ae9d9c31e6))
* third party enums don't break first class enums ([#118](https://www.github.com/googleapis/proto-plus-python/issues/118)) ([50b87af](https://www.github.com/googleapis/proto-plus-python/commit/50b87af481bb1f19d10d64e88dc9ee39c2d5b6f8)), closes [#103](https://www.github.com/googleapis/proto-plus-python/issues/103)


### [1.9.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.9.0...v1.9.1) (2020-09-08)


### Reverts

* Revert "feat: json serialization and deserialization support stringy enums (#112)" (#116) ([91c6d7b](https://www.github.com/googleapis/proto-plus-python/commit/91c6d7bb27d198439bb323d2454fb94e197bf3dd)), closes [#112](https://www.github.com/googleapis/proto-plus-python/issues/112) [#116](https://www.github.com/googleapis/proto-plus-python/issues/116)


### Documentation

* update README ([#120](https://www.github.com/googleapis/proto-plus-python/issues/120)) ([2077390](https://www.github.com/googleapis/proto-plus-python/commit/2077390d614acb278ab94077f131a895d7184881))

## [1.9.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.8.1...v1.9.0) (2020-09-02)


### Features

* json serialization and deserialization support stringy enums ([#112](https://www.github.com/googleapis/proto-plus-python/issues/112)) ([8d2e3a3](https://www.github.com/googleapis/proto-plus-python/commit/8d2e3a3439650dab9ca7c6ff49ed067838a02a45)), closes [#107](https://www.github.com/googleapis/proto-plus-python/issues/107)

### [1.8.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.8.0...v1.8.1) (2020-08-28)


### Bug Fixes

* revert "feat: allow enum strings in json serialization and deserialization" ([#110](https://www.github.com/googleapis/proto-plus-python/issues/110)) ([bd3d50e](https://www.github.com/googleapis/proto-plus-python/commit/bd3d50e6b4d4574a21592f51adf7b248ededd545)), closes [#107](https://www.github.com/googleapis/proto-plus-python/issues/107)

## [1.8.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.7.1...v1.8.0) (2020-08-28)


### Features

* allow enum strings in json serialization and deserialization ([#107](https://www.github.com/googleapis/proto-plus-python/issues/107)) ([a082f85](https://www.github.com/googleapis/proto-plus-python/commit/a082f85ffcb72e2c53c0e33e40e6df2927a41259))

### [1.7.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.7.0...v1.7.1) (2020-08-17)


### Bug Fixes

* revert algorithm for RepeatedComposite insertion. ([#101](https://www.github.com/googleapis/proto-plus-python/issues/101)) ([ae946aa](https://www.github.com/googleapis/proto-plus-python/commit/ae946aa2a3b394fa31590224fcf50593bde0ccaa))

## [1.7.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.6.0...v1.7.0) (2020-08-07)


### Features

* optimize insert for class RepeatedComposite. ([#95](https://www.github.com/googleapis/proto-plus-python/issues/95)) ([86790e3](https://www.github.com/googleapis/proto-plus-python/commit/86790e3f7d891e13835699a4e1f50aec6140fa6e))

## [1.6.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.3...v1.6.0) (2020-08-05)


### Features

* more performance optimizations ([#92](https://www.github.com/googleapis/proto-plus-python/issues/92)) ([19b1519](https://www.github.com/googleapis/proto-plus-python/commit/19b151960de7c83ac82e670b06cb47d6e885f627))

### [1.5.3](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.2...v1.5.3) (2020-08-04)


### Bug Fixes

* yet more perf tweaks ([#90](https://www.github.com/googleapis/proto-plus-python/issues/90)) ([eb7891c](https://www.github.com/googleapis/proto-plus-python/commit/eb7891cf05124803352b2f4fd719937356bf9167))

### [1.5.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.1...v1.5.2) (2020-08-03)


### Bug Fixes

* tweak to_python ([#88](https://www.github.com/googleapis/proto-plus-python/issues/88)) ([5459ede](https://www.github.com/googleapis/proto-plus-python/commit/5459ede75597b06df5a211b0e317fb2c1f4b034e))

### [1.5.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.0...v1.5.1) (2020-07-30)


### Bug Fixes

* numerous small performance tweaks ([#85](https://www.github.com/googleapis/proto-plus-python/issues/85)) ([7b5faf2](https://www.github.com/googleapis/proto-plus-python/commit/7b5faf2e2c20c8022c83d6a99656505aa669200b))

## [1.5.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.2...v1.5.0) (2020-07-29)


### Features

* support fixed filename salt to allow proto-plus use with schema registry tools ([#61](https://www.github.com/googleapis/proto-plus-python/issues/61)) ([ea86eb9](https://www.github.com/googleapis/proto-plus-python/commit/ea86eb9ac694ed1f0e711698429449f41ecfedfc))

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
