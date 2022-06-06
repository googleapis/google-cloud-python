# Changelog

## [1.3.2](https://github.com/googleapis/python-video-transcoder/compare/v1.3.1...v1.3.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#195](https://github.com/googleapis/python-video-transcoder/issues/195)) ([8d9c679](https://github.com/googleapis/python-video-transcoder/commit/8d9c679a2f0b460c1f34456ab2e46437c4cbdc16))


### Documentation

* fix changelog header to consistent size ([#196](https://github.com/googleapis/python-video-transcoder/issues/196)) ([04ee631](https://github.com/googleapis/python-video-transcoder/commit/04ee631bb65cd5bb0121f7dcfce9b78e67d19198))

## [1.3.1](https://github.com/googleapis/python-video-transcoder/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#153](https://github.com/googleapis/python-video-transcoder/issues/153)) ([03ba693](https://github.com/googleapis/python-video-transcoder/commit/03ba693031d605a3e61b3fd1e7e0c5529bc3c399))

## [1.3.0](https://github.com/googleapis/python-video-transcoder/compare/v1.2.1...v1.3.0) (2022-02-24)


### Features

* add api key support ([#127](https://github.com/googleapis/python-video-transcoder/issues/127)) ([ac6a403](https://github.com/googleapis/python-video-transcoder/commit/ac6a4031ac66a721d776c41885830023023f14f2)), closes [#140](https://github.com/googleapis/python-video-transcoder/issues/140)


### Bug Fixes

* **deps:** require proto-plus >= 1.20.3 ([ac6a403](https://github.com/googleapis/python-video-transcoder/commit/ac6a4031ac66a721d776c41885830023023f14f2))
* Remove deprecated v1beta1 API that is no longer available ([#138](https://github.com/googleapis/python-video-transcoder/issues/138)) ([e8a85da](https://github.com/googleapis/python-video-transcoder/commit/e8a85da130a0b688167a1474c339c66af1c6760c))
* rename mapping attribute of AudioStream to mapping_ ([c14695b](https://github.com/googleapis/python-video-transcoder/commit/c14695bc9070ec64a890c8f81af382165f5d04ea))
* resolve DuplicateCredentialArgs error when using credentials_file ([6774bd3](https://github.com/googleapis/python-video-transcoder/commit/6774bd328f235894caf7343088c25cc2809d8932))
* resolve issue where mapping attribute of AudioStream could not be set ([c14695b](https://github.com/googleapis/python-video-transcoder/commit/c14695bc9070ec64a890c8f81af382165f5d04ea))


### Documentation

* add generated snippets ([e8a85da](https://github.com/googleapis/python-video-transcoder/commit/e8a85da130a0b688167a1474c339c66af1c6760c))
* **samples:** update samples to use mapping_ attribute of AudioStream ([#142](https://github.com/googleapis/python-video-transcoder/issues/142)) ([7fbc619](https://github.com/googleapis/python-video-transcoder/commit/7fbc61917562c269439828df82b474700c95ea23))
* **samples:** add samples and tests for adding captions to a job ([#131](https://github.com/googleapis/python-video-transcoder/issues/131)) ([e30431f](https://github.com/googleapis/python-video-transcoder/commit/e30431fec7c15666afbb5bc975f7077389aac06d))

## [1.2.1](https://www.github.com/googleapis/python-video-transcoder/compare/v1.2.0...v1.2.1) (2021-11-04)


### Bug Fixes

* **deps:** drop packaging dependency ([9850614](https://www.github.com/googleapis/python-video-transcoder/commit/985061433802e6a49a23e53b77aecbaafe7bf12a))
* **deps:** require google-api-core >= 1.28.0 ([9850614](https://www.github.com/googleapis/python-video-transcoder/commit/985061433802e6a49a23e53b77aecbaafe7bf12a))


### Documentation

* list oneofs in docstring ([9850614](https://www.github.com/googleapis/python-video-transcoder/commit/985061433802e6a49a23e53b77aecbaafe7bf12a))

## [1.2.0](https://www.github.com/googleapis/python-video-transcoder/compare/v1.1.0...v1.2.0) (2021-10-14)


### Features

* add support for python 3.10 ([#108](https://www.github.com/googleapis/python-video-transcoder/issues/108)) ([e9c1c22](https://www.github.com/googleapis/python-video-transcoder/commit/e9c1c229fe88d200d0f60314814078e79e3f1524))

## [1.1.0](https://www.github.com/googleapis/python-video-transcoder/compare/v1.0.1...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#104](https://www.github.com/googleapis/python-video-transcoder/issues/104)) ([2c5f07d](https://www.github.com/googleapis/python-video-transcoder/commit/2c5f07d5d12d05c65854409f45374b846363328c))


### Bug Fixes

* remove Encryption settings that were published erroneously ([#102](https://www.github.com/googleapis/python-video-transcoder/issues/102)) ([824009a](https://www.github.com/googleapis/python-video-transcoder/commit/824009ac01700341071b50af2741ef6493dcbcf5))

## [1.0.1](https://www.github.com/googleapis/python-video-transcoder/compare/v1.0.0...v1.0.1) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([34391dc](https://www.github.com/googleapis/python-video-transcoder/commit/34391dc7fbf433278e34843d4994364f44e62b4e))

## [1.0.0](https://www.github.com/googleapis/python-video-transcoder/compare/v0.5.1...v1.0.0) (2021-09-29)


### Features

* bump release level to production/stable ([#79](https://www.github.com/googleapis/python-video-transcoder/issues/79)) ([45ba870](https://www.github.com/googleapis/python-video-transcoder/commit/45ba87048ef73c666c00248c6da3637fd418d70a))

## [0.5.1](https://www.github.com/googleapis/python-video-transcoder/compare/v0.5.0...v0.5.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([81b1273](https://www.github.com/googleapis/python-video-transcoder/commit/81b127355c37c59a36a5da45a71f8c02d64ae592))

## [0.5.0](https://www.github.com/googleapis/python-video-transcoder/compare/v0.4.1...v0.5.0) (2021-08-07)


### Features

* Add ttl_after_completion_days field to Job ([d862900](https://www.github.com/googleapis/python-video-transcoder/commit/d86290047e9464e4026c264a6dfea51936b21c2c))
* Add video cropping feature ([#81](https://www.github.com/googleapis/python-video-transcoder/issues/81)) ([d862900](https://www.github.com/googleapis/python-video-transcoder/commit/d86290047e9464e4026c264a6dfea51936b21c2c))
* Add video padding feature ([d862900](https://www.github.com/googleapis/python-video-transcoder/commit/d86290047e9464e4026c264a6dfea51936b21c2c))


### Documentation

* Indicate v1beta1 deprecation ([d862900](https://www.github.com/googleapis/python-video-transcoder/commit/d86290047e9464e4026c264a6dfea51936b21c2c))
* Update proto documentation ([d862900](https://www.github.com/googleapis/python-video-transcoder/commit/d86290047e9464e4026c264a6dfea51936b21c2c))

## [0.4.1](https://www.github.com/googleapis/python-video-transcoder/compare/v0.4.0...v0.4.1) (2021-07-27)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#70](https://www.github.com/googleapis/python-video-transcoder/issues/70)) ([37d076a](https://www.github.com/googleapis/python-video-transcoder/commit/37d076a9fba1fc995ee955528007d10c75765975))
* enable self signed jwt for grpc ([#75](https://www.github.com/googleapis/python-video-transcoder/issues/75)) ([af5ecd9](https://www.github.com/googleapis/python-video-transcoder/commit/af5ecd9295f46bc9a82bc62cd53b815ef5db10df))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#71](https://www.github.com/googleapis/python-video-transcoder/issues/71)) ([0b67055](https://www.github.com/googleapis/python-video-transcoder/commit/0b670557d0000fc891ebae7ea8f4f54959c89b79))


### Miscellaneous Chores

* release as 0.4.1 ([#76](https://www.github.com/googleapis/python-video-transcoder/issues/76)) ([4173cf3](https://www.github.com/googleapis/python-video-transcoder/commit/4173cf356a1ce84cde8ef28e0098cb8ad06f57e4))

## [0.4.0](https://www.github.com/googleapis/python-video-transcoder/compare/v0.3.1...v0.4.0) (2021-07-09)


### Features

* add always_use_jwt_access ([#62](https://www.github.com/googleapis/python-video-transcoder/issues/62)) ([d43c40e](https://www.github.com/googleapis/python-video-transcoder/commit/d43c40e9ab80c42afd25efa1c2980d23dbc50ce2))
* Add Transcoder V1 ([#67](https://www.github.com/googleapis/python-video-transcoder/issues/67)) ([721d28e](https://www.github.com/googleapis/python-video-transcoder/commit/721d28ec565bfdb41a195167a989baf042ede228))


### Bug Fixes

* disable always_use_jwt_access ([#66](https://www.github.com/googleapis/python-video-transcoder/issues/66)) ([98d8b86](https://www.github.com/googleapis/python-video-transcoder/commit/98d8b860227a9b9a8b4cecc851ec547d7789ac66))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-video-transcoder/issues/1127)) ([#58](https://www.github.com/googleapis/python-video-transcoder/issues/58)) ([1659ce8](https://www.github.com/googleapis/python-video-transcoder/commit/1659ce88ef94139a271be9719a4adaf4e3a600c0)), closes [#1126](https://www.github.com/googleapis/python-video-transcoder/issues/1126)

## [0.3.1](https://www.github.com/googleapis/python-video-transcoder/compare/v0.3.0...v0.3.1) (2021-05-28)


### Bug Fixes

* **deps:** add packaging requirement ([#52](https://www.github.com/googleapis/python-video-transcoder/issues/52)) ([7ffa13c](https://www.github.com/googleapis/python-video-transcoder/commit/7ffa13c999260f47fbeb9dcce04110a7db9fd172))

## [0.3.0](https://www.github.com/googleapis/python-video-transcoder/compare/v0.2.1...v0.3.0) (2021-03-31)


### Features

* add `from_service_account_info` ([#32](https://www.github.com/googleapis/python-video-transcoder/issues/32)) ([4076914](https://www.github.com/googleapis/python-video-transcoder/commit/4076914adfde514417b5a39a0e5fcd905e5f6e8f))

## [0.2.1](https://www.github.com/googleapis/python-video-transcoder/compare/v0.2.0...v0.2.1) (2021-02-12)


### Bug Fixes

* remove gRPC send/recv limits ([#18](https://www.github.com/googleapis/python-video-transcoder/issues/18)) ([03332a4](https://www.github.com/googleapis/python-video-transcoder/commit/03332a4287ad31d2fd41f4de27c3fea5f20e1d53))

## [0.2.0](https://www.github.com/googleapis/python-video-transcoder/compare/v0.1.0...v0.2.0) (2020-11-14)


### Features

* add create_time, start_time, and end_time to jobs ([#10](https://www.github.com/googleapis/python-video-transcoder/issues/10)) ([a5a210e](https://www.github.com/googleapis/python-video-transcoder/commit/a5a210e16420e3450200a346aaa2cd18a7270cf3))

## 0.1.0 (2020-08-24)


### Features

* generate v1beta1 ([06cfb30](https://www.github.com/googleapis/python-video-transcoder/commit/06cfb307250f3e0ef4a6ce3e54e55c3b89c73095))
