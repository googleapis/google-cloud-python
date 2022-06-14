# Changelog

## [1.20.6](https://github.com/googleapis/proto-plus-python/compare/v1.20.5...v1.20.6) (2022-06-13)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#324](https://github.com/googleapis/proto-plus-python/issues/324)) ([af4f56e](https://github.com/googleapis/proto-plus-python/commit/af4f56edb0bfbfa808f7def37e19b24bd27d4b40))


### Documentation

* fix changelog header to consistent size ([#319](https://github.com/googleapis/proto-plus-python/issues/319)) ([27d2003](https://github.com/googleapis/proto-plus-python/commit/27d2003571342e24aa74d29a45fa49d2328ff76d))

## [1.20.5](https://github.com/googleapis/proto-plus-python/compare/v1.20.4...v1.20.5) (2022-05-26)


### Bug Fixes

* **deps:** require google-api-core[grpc] >= 1.31.5 ([1d13c41](https://github.com/googleapis/proto-plus-python/commit/1d13c415df457a87153a6fca202003fa83e56093))
* **deps:** require protobuf>= 3.15.0, <4.0.0dev ([#315](https://github.com/googleapis/proto-plus-python/issues/315)) ([1d13c41](https://github.com/googleapis/proto-plus-python/commit/1d13c415df457a87153a6fca202003fa83e56093))

## [1.20.4](https://github.com/googleapis/proto-plus-python/compare/v1.20.3...v1.20.4) (2022-05-02)


### Bug Fixes

* default proto package name is the module name, not "" ([#309](https://github.com/googleapis/proto-plus-python/issues/309)) ([3148a1c](https://github.com/googleapis/proto-plus-python/commit/3148a1c287eb69b397c940119cd44e5067357e17))
* lookup attribute instead of performing a deepcopy ([#226](https://github.com/googleapis/proto-plus-python/issues/226)) ([e469059](https://github.com/googleapis/proto-plus-python/commit/e469059d70bab4c2b0a38dd52c4451b3c61bf470))

## [1.20.3](https://github.com/googleapis/proto-plus-python/compare/v1.20.2...v1.20.3) (2022-02-18)


### Bug Fixes

* additional logic to mitigate collisions with reserved terms ([#301](https://github.com/googleapis/proto-plus-python/issues/301)) ([c9a77df](https://github.com/googleapis/proto-plus-python/commit/c9a77df58e93a87952470d809538a08103644364))

## [1.20.2](https://github.com/googleapis/proto-plus-python/compare/v1.20.1...v1.20.2) (2022-02-17)


### Bug Fixes

* dir(proto.Message) does not raise ([#302](https://github.com/googleapis/proto-plus-python/issues/302)) ([80dcce9](https://github.com/googleapis/proto-plus-python/commit/80dcce9099e630a6217792b6b3a14213add690e6))

## [1.20.1](https://github.com/googleapis/proto-plus-python/compare/v1.20.0...v1.20.1) (2022-02-14)


### Bug Fixes

* mitigate collisions in field names ([#295](https://github.com/googleapis/proto-plus-python/issues/295)) ([158ae99](https://github.com/googleapis/proto-plus-python/commit/158ae995aa4fdf6239c864a41f5df5575a3c30b3))

## [1.20.0](https://github.com/googleapis/proto-plus-python/compare/v1.19.9...v1.20.0) (2022-02-07)


### Features

* add custom __dir__ for messages and message classes ([#289](https://github.com/googleapis/proto-plus-python/issues/289)) ([35e019e](https://github.com/googleapis/proto-plus-python/commit/35e019eb8155c1e4067b326804e3e7e86f85b6a8))


### Bug Fixes

* workaround for buggy pytest ([#291](https://github.com/googleapis/proto-plus-python/issues/291)) ([28aa3b2](https://github.com/googleapis/proto-plus-python/commit/28aa3b2b325d2ba262f35cfc8d20e1f5fbdcf883))

## [1.19.9](https://github.com/googleapis/proto-plus-python/compare/v1.19.8...v1.19.9) (2022-01-25)


### Bug Fixes

* add pickling support to proto messages ([#280](https://github.com/googleapis/proto-plus-python/issues/280)) ([2b7be35](https://github.com/googleapis/proto-plus-python/commit/2b7be3563f9fc2a4649a5e14d7653b85020c566f))

## [1.19.8](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.7...v1.19.8) (2021-11-09)


### Documentation

* fix typos ([#277](https://www.github.com/googleapis/proto-plus-python/issues/277)) ([e3b71e8](https://www.github.com/googleapis/proto-plus-python/commit/e3b71e8b2a81a5abb5af666c9625facb1814a609))

## [1.19.7](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.6...v1.19.7) (2021-10-27)


### Bug Fixes

* restore allowing None as value for stringy ints ([#272](https://www.github.com/googleapis/proto-plus-python/issues/272)) ([a8991d7](https://www.github.com/googleapis/proto-plus-python/commit/a8991d71ff455093fbfef142f9140d3f2928195f))

## [1.19.6](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.5...v1.19.6) (2021-10-25)


### Bug Fixes

* setting 64bit fields from strings supported ([#267](https://www.github.com/googleapis/proto-plus-python/issues/267)) ([ea7b911](https://www.github.com/googleapis/proto-plus-python/commit/ea7b91100114f5c3d40d41320b045568ac9a68f9))

## [1.19.5](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.4...v1.19.5) (2021-10-11)


### Documentation

* Clarify semantics of multiple oneof variants passed to msg ctor ([#263](https://www.github.com/googleapis/proto-plus-python/issues/263)) ([6f8a5b2](https://www.github.com/googleapis/proto-plus-python/commit/6f8a5b2098e4f6748945c53bda3d5821e62e5a0a))

## [1.19.4](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.3...v1.19.4) (2021-10-08)


### Documentation

* clarify that proto plus messages are not pickleable ([#260](https://www.github.com/googleapis/proto-plus-python/issues/260)) ([6e691dc](https://www.github.com/googleapis/proto-plus-python/commit/6e691dc27b1e540ef0661597fd89ece8f0155c97))

## [1.19.3](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.2...v1.19.3) (2021-10-07)


### Bug Fixes

* setting bytes field from python string base64 decodes before assignment ([#255](https://www.github.com/googleapis/proto-plus-python/issues/255)) ([b6f3eb6](https://www.github.com/googleapis/proto-plus-python/commit/b6f3eb6575484748126170997b8c98512763ea66))

## [1.19.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.1...v1.19.2) (2021-09-29)


### Bug Fixes

* ensure enums are hashable ([#252](https://www.github.com/googleapis/proto-plus-python/issues/252)) ([232341b](https://www.github.com/googleapis/proto-plus-python/commit/232341b4f4902fba1b3597bb1e1618b8f320374b))

## [1.19.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.19.0...v1.19.1) (2021-09-29)


### Bug Fixes

* ensure enums are incomparable w other enum types ([#248](https://www.github.com/googleapis/proto-plus-python/issues/248)) ([5927c14](https://www.github.com/googleapis/proto-plus-python/commit/5927c1400f400b3213c9b92e7a37c3c3a1abd681))

## [1.19.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.18.1...v1.19.0) (2021-06-29)


### Features

* pass 'including_default_value_fields' through to 'Message.to_dict' method ([#232](https://www.github.com/googleapis/proto-plus-python/issues/232)) ([15c2f47](https://www.github.com/googleapis/proto-plus-python/commit/15c2f479f81f0f80d451ca9b043e42cecfe7184e))

## [1.18.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.18.0...v1.18.1) (2021-03-19)


### Bug Fixes

* Add arm64 support for PY3.6 ([#219](https://www.github.com/googleapis/proto-plus-python/issues/219)) ([c9667c2](https://www.github.com/googleapis/proto-plus-python/commit/c9667c22d0b8f6026dbf69d502eb8eb972279891))

## [1.18.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.17.0...v1.18.0) (2021-03-16)


### Features

* add copy_from method for field assignment ([#215](https://www.github.com/googleapis/proto-plus-python/issues/215)) ([11c3e58](https://www.github.com/googleapis/proto-plus-python/commit/11c3e58a9ba59f0d7d808a26597dab735ca982ba))

## [1.17.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.16.0...v1.17.0) (2021-03-12)


### Features

* add preserving_proto_field_name to to_json ([#213](https://www.github.com/googleapis/proto-plus-python/issues/213)) ([b2c245b](https://www.github.com/googleapis/proto-plus-python/commit/b2c245bf044b964897f4e7423ff4944ae915e469))

## [1.16.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.15.0...v1.16.0) (2021-03-12)


### Features

* add preserving_proto_field_name passthrough in MessageMeta.to_dict ([#211](https://www.github.com/googleapis/proto-plus-python/issues/211)) ([7675a0c](https://www.github.com/googleapis/proto-plus-python/commit/7675a0c8d1004f2727d64100527f2b208d305017))

## [1.15.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.14.3...v1.15.0) (2021-03-10)


### Features

* allow_alias for enums ([#207](https://www.github.com/googleapis/proto-plus-python/issues/207)) ([6d4d713](https://www.github.com/googleapis/proto-plus-python/commit/6d4d71399f494b9f3bd47b6f3ef0b6d3c0c547b5))

## [1.14.3](https://www.github.com/googleapis/proto-plus-python/compare/v1.14.2...v1.14.3) (2021-03-04)


### Bug Fixes

* adding enums to a repeated field does not raise a TypeError ([#202](https://www.github.com/googleapis/proto-plus-python/issues/202)) ([2a10bbe](https://www.github.com/googleapis/proto-plus-python/commit/2a10bbecaf8955c7bf1956086aef42630112788b))

## [1.14.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.14.1...v1.14.2) (2021-02-26)


### Bug Fixes

* use the correct environment for uploading to pypi ([#199](https://www.github.com/googleapis/proto-plus-python/issues/199)) ([babdc5c](https://www.github.com/googleapis/proto-plus-python/commit/babdc5cddf08235cac3cda66200babab44204688))

## [1.14.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.14.0...v1.14.1) (2021-02-26)


### Bug Fixes

* install the wheel dependency ([#197](https://www.github.com/googleapis/proto-plus-python/issues/197)) ([923ab31](https://www.github.com/googleapis/proto-plus-python/commit/923ab31e4685b47acae793198be55335e5eeae38))

## [1.14.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.13.1...v1.14.0) (2021-02-24)


### Features

* Pypi publish ghub actions ([#189](https://www.github.com/googleapis/proto-plus-python/issues/189)) ([4c967b0](https://www.github.com/googleapis/proto-plus-python/commit/4c967b0bb2ead29156bcc53c1f3b227b3afb2e8b))


### Bug Fixes

* proper __setitem__ and insert for RepeatedComposite ([#178](https://www.github.com/googleapis/proto-plus-python/issues/178)) ([1157a76](https://www.github.com/googleapis/proto-plus-python/commit/1157a76bb608d72389f46dc4d8e9aa00cc14ccc6))
* proper native marshal for repeated enumeration fields ([#180](https://www.github.com/googleapis/proto-plus-python/issues/180)) ([30265d6](https://www.github.com/googleapis/proto-plus-python/commit/30265d654d7f3589cbd0994d2ac564db1fd44265))

## [1.13.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.13.0...v1.13.1) (2021-02-09)


### Bug Fixes

* update docstring to match type hint ([#172](https://www.github.com/googleapis/proto-plus-python/issues/172)) ([14dad5b](https://www.github.com/googleapis/proto-plus-python/commit/14dad5bf6c5967a720e9d3095d621dbfe208b614))

## [1.13.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.12.0...v1.13.0) (2020-12-04)


### Features

* add 3.9 support and drop 3.5 ([#167](https://www.github.com/googleapis/proto-plus-python/issues/167)) ([6d17195](https://www.github.com/googleapis/proto-plus-python/commit/6d171956e14b398aece931b9dde1013be9644b74))

## [1.12.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.11.0...v1.12.0) (2020-11-20)


### Features

* add default values parameter to to_json ([#164](https://www.github.com/googleapis/proto-plus-python/issues/164)) ([691f1b2](https://www.github.com/googleapis/proto-plus-python/commit/691f1b24454502c4ac49a88a09d1c9fbc287b2bd))

## [1.11.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.2...v1.11.0) (2020-10-19)


### Features

* provide a to_dict method ([#154](https://www.github.com/googleapis/proto-plus-python/issues/154)) ([ccf903e](https://www.github.com/googleapis/proto-plus-python/commit/ccf903e3cddfcb1ff539e853594b4342914b7d61)), closes [#153](https://www.github.com/googleapis/proto-plus-python/issues/153) [#151](https://www.github.com/googleapis/proto-plus-python/issues/151)

## [1.10.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.1...v1.10.2) (2020-10-14)


### Documentation

* explain how to use repeated struct.Value ([#148](https://www.github.com/googleapis/proto-plus-python/issues/148)) ([9634ea8](https://www.github.com/googleapis/proto-plus-python/commit/9634ea8fa464c0d34f13469016f23cc2e986d973)), closes [#104](https://www.github.com/googleapis/proto-plus-python/issues/104)

## [1.10.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.10.0...v1.10.1) (2020-10-08)


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


## [1.9.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.9.0...v1.9.1) (2020-09-08)


### Reverts

* Revert "feat: json serialization and deserialization support stringy enums (#112)" (#116) ([91c6d7b](https://www.github.com/googleapis/proto-plus-python/commit/91c6d7bb27d198439bb323d2454fb94e197bf3dd)), closes [#112](https://www.github.com/googleapis/proto-plus-python/issues/112) [#116](https://www.github.com/googleapis/proto-plus-python/issues/116)


### Documentation

* update README ([#120](https://www.github.com/googleapis/proto-plus-python/issues/120)) ([2077390](https://www.github.com/googleapis/proto-plus-python/commit/2077390d614acb278ab94077f131a895d7184881))

## [1.9.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.8.1...v1.9.0) (2020-09-02)


### Features

* json serialization and deserialization support stringy enums ([#112](https://www.github.com/googleapis/proto-plus-python/issues/112)) ([8d2e3a3](https://www.github.com/googleapis/proto-plus-python/commit/8d2e3a3439650dab9ca7c6ff49ed067838a02a45)), closes [#107](https://www.github.com/googleapis/proto-plus-python/issues/107)

## [1.8.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.8.0...v1.8.1) (2020-08-28)


### Bug Fixes

* revert "feat: allow enum strings in json serialization and deserialization" ([#110](https://www.github.com/googleapis/proto-plus-python/issues/110)) ([bd3d50e](https://www.github.com/googleapis/proto-plus-python/commit/bd3d50e6b4d4574a21592f51adf7b248ededd545)), closes [#107](https://www.github.com/googleapis/proto-plus-python/issues/107)

## [1.8.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.7.1...v1.8.0) (2020-08-28)


### Features

* allow enum strings in json serialization and deserialization ([#107](https://www.github.com/googleapis/proto-plus-python/issues/107)) ([a082f85](https://www.github.com/googleapis/proto-plus-python/commit/a082f85ffcb72e2c53c0e33e40e6df2927a41259))

## [1.7.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.7.0...v1.7.1) (2020-08-17)


### Bug Fixes

* revert algorithm for RepeatedComposite insertion. ([#101](https://www.github.com/googleapis/proto-plus-python/issues/101)) ([ae946aa](https://www.github.com/googleapis/proto-plus-python/commit/ae946aa2a3b394fa31590224fcf50593bde0ccaa))

## [1.7.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.6.0...v1.7.0) (2020-08-07)


### Features

* optimize insert for class RepeatedComposite. ([#95](https://www.github.com/googleapis/proto-plus-python/issues/95)) ([86790e3](https://www.github.com/googleapis/proto-plus-python/commit/86790e3f7d891e13835699a4e1f50aec6140fa6e))

## [1.6.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.3...v1.6.0) (2020-08-05)


### Features

* more performance optimizations ([#92](https://www.github.com/googleapis/proto-plus-python/issues/92)) ([19b1519](https://www.github.com/googleapis/proto-plus-python/commit/19b151960de7c83ac82e670b06cb47d6e885f627))

## [1.5.3](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.2...v1.5.3) (2020-08-04)


### Bug Fixes

* yet more perf tweaks ([#90](https://www.github.com/googleapis/proto-plus-python/issues/90)) ([eb7891c](https://www.github.com/googleapis/proto-plus-python/commit/eb7891cf05124803352b2f4fd719937356bf9167))

## [1.5.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.1...v1.5.2) (2020-08-03)


### Bug Fixes

* tweak to_python ([#88](https://www.github.com/googleapis/proto-plus-python/issues/88)) ([5459ede](https://www.github.com/googleapis/proto-plus-python/commit/5459ede75597b06df5a211b0e317fb2c1f4b034e))

## [1.5.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.5.0...v1.5.1) (2020-07-30)


### Bug Fixes

* numerous small performance tweaks ([#85](https://www.github.com/googleapis/proto-plus-python/issues/85)) ([7b5faf2](https://www.github.com/googleapis/proto-plus-python/commit/7b5faf2e2c20c8022c83d6a99656505aa669200b))

## [1.5.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.2...v1.5.0) (2020-07-29)


### Features

* support fixed filename salt to allow proto-plus use with schema registry tools ([#61](https://www.github.com/googleapis/proto-plus-python/issues/61)) ([ea86eb9](https://www.github.com/googleapis/proto-plus-python/commit/ea86eb9ac694ed1f0e711698429449f41ecfedfc))

## [1.4.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.1...v1.4.2) (2020-07-23)


### Bug Fixes

* getattr on an invalid field raises AttributeError ([#73](https://www.github.com/googleapis/proto-plus-python/issues/73)) ([74ea8f0](https://www.github.com/googleapis/proto-plus-python/commit/74ea8f0cd9083939e53d1de2450b649500281b9a)), closes [#31](https://www.github.com/googleapis/proto-plus-python/issues/31)

## [1.4.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.4.0...v1.4.1) (2020-07-23)


### Bug Fixes

* tweak publish ci task ([#65](https://www.github.com/googleapis/proto-plus-python/issues/65)) ([983189c](https://www.github.com/googleapis/proto-plus-python/commit/983189c5effa25fb9365eb63caddb425d3cfb2b5))

## [1.4.0](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.2...v1.4.0) (2020-07-23)


### Features

* prevent unnecessary copies when deserializing proto ([#63](https://www.github.com/googleapis/proto-plus-python/issues/63)) ([5e1c061](https://www.github.com/googleapis/proto-plus-python/commit/5e1c0619b5f4c5d2a6a75ae6d45a53fef2e58823))

## [1.3.2](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.1...v1.3.2) (2020-07-22)


### Bug Fixes

* correctly handle passed in vanilla datetime.datetime ([#57](https://www.github.com/googleapis/proto-plus-python/issues/57)) ([a770816](https://www.github.com/googleapis/proto-plus-python/commit/a770816197cbce60ee023bd5b6ee6bd2d970ded8)), closes [googleapis/gapic-generator-python#544](https://www.github.com/googleapis/gapic-generator-python/issues/544)
* update encrypted pypi passwd ([#58](https://www.github.com/googleapis/proto-plus-python/issues/58)) ([d985233](https://www.github.com/googleapis/proto-plus-python/commit/d9852336d83717cb9ff24b6bec3ef1463239fea1))

## [1.3.1](https://www.github.com/googleapis/proto-plus-python/compare/v1.3.0...v1.3.1) (2020-07-21)


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
