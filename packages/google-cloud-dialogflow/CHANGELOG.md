# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/dialogflow/#history

## [2.15.0](https://github.com/googleapis/python-dialogflow/compare/v2.14.1...v2.15.0) (2022-07-16)


### Features

* add audience parameter ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* Add AudioInput to analysis requests ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* Add filter field to ListAnswerRecordsRequest ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* deprecated the filter field and add resource_definition ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* provide new parameter cx_current_page, the unique identifier of the CX page to override the `current_page` in the session ([#533](https://github.com/googleapis/python-dialogflow/issues/533)) ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* require python 3.7+ ([#535](https://github.com/googleapis/python-dialogflow/issues/535)) ([912518b](https://github.com/googleapis/python-dialogflow/commit/912518b3d119f38115a255d26bd11397d483dddb))


### Documentation

* add more meaningful comments ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* add more meaningful comments ([4377f2a](https://github.com/googleapis/python-dialogflow/commit/4377f2a61a829cb4fc402f7090d0082b838c8bfe))
* Update region_tag: dialogflow_detect_intent_text --> dialogflow_es_detect_intent_text ([#536](https://github.com/googleapis/python-dialogflow/issues/536)) ([c20dcf7](https://github.com/googleapis/python-dialogflow/commit/c20dcf788211796d23ed630a0f7259ac02ef6781))

## [2.14.1](https://github.com/googleapis/python-dialogflow/compare/v2.14.0...v2.14.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#523](https://github.com/googleapis/python-dialogflow/issues/523)) ([d444383](https://github.com/googleapis/python-dialogflow/commit/d44438335af3488cec8d973b3329cea1161bc5eb))


### Documentation

* fix changelog header to consistent size ([#524](https://github.com/googleapis/python-dialogflow/issues/524)) ([75977e8](https://github.com/googleapis/python-dialogflow/commit/75977e823d5e569494da81fbb8de4f0395bf6990))

## [2.14.0](https://github.com/googleapis/python-dialogflow/compare/v2.13.0...v2.14.0) (2022-05-09)


### Features

* added HUMAN_INTERVENTION_NEEDED type in ConversationEvent ([#488](https://github.com/googleapis/python-dialogflow/issues/488)) ([fa5fd8b](https://github.com/googleapis/python-dialogflow/commit/fa5fd8ba4356051776b8828cef2bae59da5b4993))
* **v2beta1:** add the API of StreamingAnalyzeContent ([#520](https://github.com/googleapis/python-dialogflow/issues/520)) ([0d3b413](https://github.com/googleapis/python-dialogflow/commit/0d3b41353e7171783a44bbd996de95c9bdb1ae34))


### Bug Fixes

* correct broken ConversationModelEvaluation resource pattern ([#509](https://github.com/googleapis/python-dialogflow/issues/509)) ([cd4a93b](https://github.com/googleapis/python-dialogflow/commit/cd4a93b44b9b09d0a7cb71e32686337f504ef0ce))


### Documentation

* add the fields for setting CX virtual agent session parameters ([#519](https://github.com/googleapis/python-dialogflow/issues/519)) ([347e03f](https://github.com/googleapis/python-dialogflow/commit/347e03f07b55216dd1cc62ee3e3c04b509968c5b))
* added explanation for SuggestionResult ([#490](https://github.com/googleapis/python-dialogflow/issues/490)) ([0c210be](https://github.com/googleapis/python-dialogflow/commit/0c210bef1dec9c7014f1ae791523f6b60aa8034e))

## [2.13.0](https://github.com/googleapis/python-dialogflow/compare/v2.12.0...v2.13.0) (2022-03-08)


### Features

* added ConversationDataset resource and its APIs ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* added ConversationModel resource and its APIs ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* added metadata for the Knowledge operation ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* added new knowledge type of Document content ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* added SetSuggestionFeatureConfig and ClearSuggestionFeatureConfig APIs for ConversationProfile ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* added states of Document ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#479](https://github.com/googleapis/python-dialogflow/issues/479)) ([4a62e80](https://github.com/googleapis/python-dialogflow/commit/4a62e80e045639061779bb097dacab744276973a))
* **deps:** require proto-plus>=1.15.0 ([4a62e80](https://github.com/googleapis/python-dialogflow/commit/4a62e80e045639061779bb097dacab744276973a))


### Documentation

* added a new resource name pattern for ConversationModel ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* clarified the behavior of language_code in EventInput ([#475](https://github.com/googleapis/python-dialogflow/issues/475)) ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* clarified wording around Cloud Storage usage ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))
* updated copyright ([bd93557](https://github.com/googleapis/python-dialogflow/commit/bd935578a57d7738796bf8d3c02dfca126bfdfbb))

## [2.12.0](https://github.com/googleapis/python-dialogflow/compare/v2.11.0...v2.12.0) (2022-02-11)


### Features

* add api key support ([#468](https://github.com/googleapis/python-dialogflow/issues/468)) ([0d6bebd](https://github.com/googleapis/python-dialogflow/commit/0d6bebd2c28d46bfd06d42da30778d3b55a1878e))
* **v2:** add conversation process config ([#464](https://github.com/googleapis/python-dialogflow/issues/464)) ([921861a](https://github.com/googleapis/python-dialogflow/commit/921861a46b48ce16d87308ee96f9ab58171489e6))
* **v2:** add ImportDocument ([921861a](https://github.com/googleapis/python-dialogflow/commit/921861a46b48ce16d87308ee96f9ab58171489e6))
* **v2:** add SuggestSmartReplies ([921861a](https://github.com/googleapis/python-dialogflow/commit/921861a46b48ce16d87308ee96f9ab58171489e6))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([74a54c6](https://github.com/googleapis/python-dialogflow/commit/74a54c6fd9d6e03741206ff1e95939123362cab9))


### Documentation

* add generated snippets ([#473](https://github.com/googleapis/python-dialogflow/issues/473)) ([c0c7789](https://github.com/googleapis/python-dialogflow/commit/c0c7789e58af7206493fdef99341367ab16f95bd))
* fix typos in UPGRADING.md ([#472](https://github.com/googleapis/python-dialogflow/issues/472)) ([62bbb7f](https://github.com/googleapis/python-dialogflow/commit/62bbb7fa38889380501eda4f8b6ccfe96fde0db5))

## [2.11.0](https://github.com/googleapis/python-dialogflow/compare/v2.10.0...v2.11.0) (2022-01-13)


### Features

* support document metadata filter in article suggestion ([#442](https://github.com/googleapis/python-dialogflow/issues/442)) ([6f615f9](https://github.com/googleapis/python-dialogflow/commit/6f615f997dfa4e8e4d3e734a94ee0c81012a5a6d))
* **v2:** added export documentation method ([#449](https://github.com/googleapis/python-dialogflow/issues/449)) ([a43d1e9](https://github.com/googleapis/python-dialogflow/commit/a43d1e92c86c87645c73a91a5c1593412bd3018d))
* **v2:** added filter in list documentations request ([a43d1e9](https://github.com/googleapis/python-dialogflow/commit/a43d1e92c86c87645c73a91a5c1593412bd3018d))
* **v2:** added filter in list knowledge bases request ([a43d1e9](https://github.com/googleapis/python-dialogflow/commit/a43d1e92c86c87645c73a91a5c1593412bd3018d))
* **v2:** added option to apply partial update to the smart messaging allowlist in reload document request ([a43d1e9](https://github.com/googleapis/python-dialogflow/commit/a43d1e92c86c87645c73a91a5c1593412bd3018d))
* **v2:** added option to import custom metadata from Google Cloud Storage in reload document request ([a43d1e9](https://github.com/googleapis/python-dialogflow/commit/a43d1e92c86c87645c73a91a5c1593412bd3018d))
* **v2beta1:** add support for knowledge_base in knowledge operation metadata ([0f60629](https://github.com/googleapis/python-dialogflow/commit/0f606297c75cdf601fc8ea1c1906fe6ac4939c43))
* **v2beta1:** added option to configure the number of sentences in the suggestion context ([#453](https://github.com/googleapis/python-dialogflow/issues/453)) ([e48ea00](https://github.com/googleapis/python-dialogflow/commit/e48ea001b7c8a4a5c1fe4b162bad49ea397458e9))
* **v2beta1:** removed OPTIONAL for speech model variant ([#448](https://github.com/googleapis/python-dialogflow/issues/448)) ([0f60629](https://github.com/googleapis/python-dialogflow/commit/0f606297c75cdf601fc8ea1c1906fe6ac4939c43))
* **v2:** removed OPTIONAL for speech model variant ([#447](https://github.com/googleapis/python-dialogflow/issues/447)) ([56efd10](https://github.com/googleapis/python-dialogflow/commit/56efd1047f146bab52d59db29b04211326118cf3))

## [2.10.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.9.1...v2.10.0) (2021-11-12)


### Features

* add context manager support in client ([#416](https://www.github.com/googleapis/python-dialogflow/issues/416)) ([317187c](https://www.github.com/googleapis/python-dialogflow/commit/317187cbaacc6889d6fff5d7ea483fe1bc2cd9ee))
* add document metadata filter in article suggestion ([#437](https://www.github.com/googleapis/python-dialogflow/issues/437)) ([56a6e11](https://www.github.com/googleapis/python-dialogflow/commit/56a6e11622f73c6d302a5f43142ceb289b334fd1))
* add smart reply model in human agent assistant ([56a6e11](https://www.github.com/googleapis/python-dialogflow/commit/56a6e11622f73c6d302a5f43142ceb289b334fd1))
* add support for python 3.10 ([#422](https://www.github.com/googleapis/python-dialogflow/issues/422)) ([652e2e8](https://www.github.com/googleapis/python-dialogflow/commit/652e2e8d860f369b62e7866d6cf220204740ade8))
* **v2:** added support to configure security settings, language code and time zone on conversation profile ([#431](https://www.github.com/googleapis/python-dialogflow/issues/431)) ([6296673](https://www.github.com/googleapis/python-dialogflow/commit/629667367d7098cfb62bae1b6e48cc11a72b9fbc))


### Bug Fixes

* **deps:** drop packaging dependency ([fd06e9f](https://www.github.com/googleapis/python-dialogflow/commit/fd06e9fe8626ac3d86175518c52ff14efebc0f7b))
* **deps:** require google-api-core >= 1.28.0 ([fd06e9f](https://www.github.com/googleapis/python-dialogflow/commit/fd06e9fe8626ac3d86175518c52ff14efebc0f7b))


### Documentation

* clarified meaning of the legacy editions ([#426](https://www.github.com/googleapis/python-dialogflow/issues/426)) ([d7a7544](https://www.github.com/googleapis/python-dialogflow/commit/d7a7544ce69cb357d7cad13e9a44afe26c6d3cf5))
* clarified semantic of the streaming APIs ([d7a7544](https://www.github.com/googleapis/python-dialogflow/commit/d7a7544ce69cb357d7cad13e9a44afe26c6d3cf5))
* list oneofs in docstring ([fd06e9f](https://www.github.com/googleapis/python-dialogflow/commit/fd06e9fe8626ac3d86175518c52ff14efebc0f7b))
* **samples:** Added comments ([#425](https://www.github.com/googleapis/python-dialogflow/issues/425)) ([f5d40dc](https://www.github.com/googleapis/python-dialogflow/commit/f5d40dc9b4bb57b8830dcd6541a2a1189a6c9780))
* **v2beta1:** clarified meaning of the legacy editions ([fd06e9f](https://www.github.com/googleapis/python-dialogflow/commit/fd06e9fe8626ac3d86175518c52ff14efebc0f7b))
* **v2beta1:** clarified semantic of the streaming APIs ([fd06e9f](https://www.github.com/googleapis/python-dialogflow/commit/fd06e9fe8626ac3d86175518c52ff14efebc0f7b))
* **v2beta1:** recommend AnalyzeContent for future users ([#420](https://www.github.com/googleapis/python-dialogflow/issues/420)) ([1afdab3](https://www.github.com/googleapis/python-dialogflow/commit/1afdab3b50c98cc082b150ff408d0f07f11f9cf3))
* **v2:** recommend AnalyzeContent for future users ([#421](https://www.github.com/googleapis/python-dialogflow/issues/421)) ([c6940a9](https://www.github.com/googleapis/python-dialogflow/commit/c6940a9f974af95037616bd1affb34d8db4405c9))

## [2.9.1](https://www.github.com/googleapis/python-dialogflow/compare/v2.9.0...v2.9.1) (2021-10-04)


### Documentation

* **samples:** adds training phrases sample ([#404](https://www.github.com/googleapis/python-dialogflow/issues/404)) ([9d98f9b](https://www.github.com/googleapis/python-dialogflow/commit/9d98f9b47208cbbdee13f678000c2970387c716e))

## [2.9.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.8.1...v2.9.0) (2021-09-30)


### Features

* added support for TelephonyTransferCall in Participant ResponseMessage ([#406](https://www.github.com/googleapis/python-dialogflow/issues/406)) ([814055d](https://www.github.com/googleapis/python-dialogflow/commit/814055d2f6d7948f832b8cc0ae0573fea163ace1))


### Bug Fixes

* improper types in pagers generation ([814055d](https://www.github.com/googleapis/python-dialogflow/commit/814055d2f6d7948f832b8cc0ae0573fea163ace1))


### Documentation

* **samples:** added webhook code snippet ([#401](https://www.github.com/googleapis/python-dialogflow/issues/401)) ([9e279c8](https://www.github.com/googleapis/python-dialogflow/commit/9e279c86136543432cc218c2b1876bbb96f24240))

## [2.8.1](https://www.github.com/googleapis/python-dialogflow/compare/v2.8.0...v2.8.1) (2021-09-29)


### Bug Fixes

* add 'dict' annotation type to 'request' ([12b4f60](https://www.github.com/googleapis/python-dialogflow/commit/12b4f6050d0b5f741f106798643bef6ebbbe1e28))

## [2.8.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.7.1...v2.8.0) (2021-09-08)


### Features

* add language code to streaming recognition result ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* add time zone and security settings to conversation profile ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* expose `Locations` service to get/list avaliable locations of Dialogflow products ([#364](https://www.github.com/googleapis/python-dialogflow/issues/364)) ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))


### Documentation

* clarified some LRO types ([#387](https://www.github.com/googleapis/python-dialogflow/issues/387)) ([3ca0f58](https://www.github.com/googleapis/python-dialogflow/commit/3ca0f5871ff8a7f28048f719f49145331ec21871))
* fix validation result docs ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* **samples:** add region tags to update intent sample ([#382](https://www.github.com/googleapis/python-dialogflow/issues/382)) ([8497101](https://www.github.com/googleapis/python-dialogflow/commit/849710195387337a7d5b13817d5c7478d09c9a28))
* **samples:** add set agent code sample ([#370](https://www.github.com/googleapis/python-dialogflow/issues/370)) ([f997336](https://www.github.com/googleapis/python-dialogflow/commit/f9973364562243a757db5c61f0ec05771751e1eb))
* **samples:** add update intent code sample ([#357](https://www.github.com/googleapis/python-dialogflow/issues/357)) ([fab916f](https://www.github.com/googleapis/python-dialogflow/commit/fab916f1f239b7425371abb224b65965913c0481))
* update agent docs ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* update entity type docs ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* update environment docs ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))
* update intent docs ([ad896f7](https://www.github.com/googleapis/python-dialogflow/commit/ad896f7401feb3f38b57612cb1bb865f1d3fc371))

## [2.7.1](https://www.github.com/googleapis/python-dialogflow/compare/v2.7.0...v2.7.1) (2021-07-26)


### Bug Fixes

* enable self signed jwt for grpc ([#345](https://www.github.com/googleapis/python-dialogflow/issues/345)) ([ae434ed](https://www.github.com/googleapis/python-dialogflow/commit/ae434edc46c5e9c3243b928674727ea91cdf0145))


### Documentation

* fix typos ([#347](https://www.github.com/googleapis/python-dialogflow/issues/347)) ([1aa9a7a](https://www.github.com/googleapis/python-dialogflow/commit/1aa9a7a67d2997d87735666ecdcc55c8f8442cdf))

## [2.7.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.6.0...v2.7.0) (2021-07-22)


### Features

* add Samples section to CONTRIBUTING.rst ([#340](https://www.github.com/googleapis/python-dialogflow/issues/340)) ([25217a3](https://www.github.com/googleapis/python-dialogflow/commit/25217a385a315a3f209039e82141f0bd153e43a0))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#339](https://www.github.com/googleapis/python-dialogflow/issues/339)) ([3bfe5b6](https://www.github.com/googleapis/python-dialogflow/commit/3bfe5b6c4c2d81ec3f1cb5e1b7aa96c60a269eb4))

## [2.6.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.5.0...v2.6.0) (2021-07-10)


### Features

* add always_use_jwt_access ([#320](https://www.github.com/googleapis/python-dialogflow/issues/320)) ([9bf371d](https://www.github.com/googleapis/python-dialogflow/commit/9bf371d38a4c55bbb349cc59c7fd7e9d49847560))


### Bug Fixes

* disable always_use_jwt_access ([9bf371d](https://www.github.com/googleapis/python-dialogflow/commit/9bf371d38a4c55bbb349cc59c7fd7e9d49847560))

## [2.5.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.4.0...v2.5.0) (2021-06-26)


### Features

* added Automated agent reply type and allow cancellation flag for partial response feature ([#314](https://www.github.com/googleapis/python-dialogflow/issues/314)) ([5dfd375](https://www.github.com/googleapis/python-dialogflow/commit/5dfd375c389e41e8d87055a6479cfb9c0b5f2e37))
* **v2beta1:** added Automated agent reply type and allow cancellation flag for partial response feature ([#311](https://www.github.com/googleapis/python-dialogflow/issues/311)) ([1d34763](https://www.github.com/googleapis/python-dialogflow/commit/1d34763b13902162f567fac7768d08619f77f81e))


### Documentation

* added notes to train agent prior to sending queries ([#319](https://www.github.com/googleapis/python-dialogflow/issues/319)) ([37dece2](https://www.github.com/googleapis/python-dialogflow/commit/37dece29c4f2b852f5d5426fb10c6c8b55d9bff6))
* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-dialogflow/issues/1127)) ([#316](https://www.github.com/googleapis/python-dialogflow/issues/316)) ([55fcb9d](https://www.github.com/googleapis/python-dialogflow/commit/55fcb9d366a27318e7f044f15984df8f3fb32f8e))
* update comment in ListSuggestions to use absolute URL for /apis/design/design_patterns ([#313](https://www.github.com/googleapis/python-dialogflow/issues/313)) ([99d8897](https://www.github.com/googleapis/python-dialogflow/commit/99d8897a9a576bcf1d3887c5d40ec86efd8e3ec4))

## [2.4.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.3.0...v2.4.0) (2021-05-25)


### Features

* add a field to indicate whether slot filling is cancelled ([#304](https://www.github.com/googleapis/python-dialogflow/issues/304)) ([3343504](https://www.github.com/googleapis/python-dialogflow/commit/33435048c05a8897297032415ccfefd171140529))
* **v2beta1:** add a field to indicate whether slot filling is cancelled ([#306](https://www.github.com/googleapis/python-dialogflow/issues/306)) ([05be019](https://www.github.com/googleapis/python-dialogflow/commit/05be0196ff2998278f174ba076498327180a63f9))

## [2.3.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.2.0...v2.3.0) (2021-05-19)


### Features

* added location-aware HTTP path binding for ListIntents feat: exposed match confidence and parameter in AnalyzeContentResponse feat: added DTMF and PARTIAL DTMF type in recognition result ([#298](https://www.github.com/googleapis/python-dialogflow/issues/298)) ([e52e9c0](https://www.github.com/googleapis/python-dialogflow/commit/e52e9c001c9830e24286e0251f3a639aaeaa32fd))

## [2.2.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.1.2...v2.2.0) (2021-05-16)


### Features

* added Fulfillment service ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* added location in some resource patterns ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* added location-aware HTTP path binding for ListIntents ([#294](https://www.github.com/googleapis/python-dialogflow/issues/294)) ([1f71e77](https://www.github.com/googleapis/python-dialogflow/commit/1f71e7788eb996e118767b83818227931750902e))
* added more Environment RPCs ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* added TextToSpeechSettings. ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* added Versions service ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* support self-signed JWT flow for service accounts ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))


### Bug Fixes

* add async client to %name_%version/init.py ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))
* **deps:** add packaging requirement ([#293](https://www.github.com/googleapis/python-dialogflow/issues/293)) ([a9f970c](https://www.github.com/googleapis/python-dialogflow/commit/a9f970c98e62c362f8aa71c26b14d68eaeccbbbd))
* removed incorrect resource annotation for UpdateEnvironmentRequest. ([1b39fc0](https://www.github.com/googleapis/python-dialogflow/commit/1b39fc00108af7b00cd8fbc3975a2bcf403b5749))

## [2.1.2](https://www.github.com/googleapis/python-dialogflow/compare/v2.1.1...v2.1.2) (2021-04-13)


### Bug Fixes

* remove unused proto InputText, InputAudio ([#273](https://www.github.com/googleapis/python-dialogflow/issues/273)) ([787d064](https://www.github.com/googleapis/python-dialogflow/commit/787d0648a842b62bfc1be8dcf43c0e8cbd88618a))

## [2.1.1](https://www.github.com/googleapis/python-dialogflow/compare/v2.1.0...v2.1.1) (2021-04-12)


### Bug Fixes

* remove `input_audio` field from AnalyzeContentRequest from v2/v2beta1 ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))
* remove proto message CreateCallMatcherRequest, CreateCallMatcherResponse, ListCallMatchersRequest, ListCallMatchersResponse, DeleteCallMatcherRequest, DeleteCallMatcherResponse, CallMatcher, StreamingAnalyzeContentRequest, StreamingAnalyzeContentResponse, AudioInput from v2/v2beta1, TelephonyDtmfEvents, TelephonyDtmf from v2 ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))
* remove resource_reference for invisible resources ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))
* Remove resource_reference from UpdateAnswerRecord ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))
* remove rpc or fields that are unintended to release ([#264](https://www.github.com/googleapis/python-dialogflow/issues/264)) ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))
* remove StreamingAnalyzeContent, CreateCallMatcher, ListCallMatchers, DeleteCallMatcher rpc from v2/v2beta1 ([06381fc](https://www.github.com/googleapis/python-dialogflow/commit/06381fcc965669e1b3dc8bec22aa567dceb6f935))


### Documentation

* **samples:** add Agent Assist code samples ([#267](https://www.github.com/googleapis/python-dialogflow/issues/267)) ([0a8cfb9](https://www.github.com/googleapis/python-dialogflow/commit/0a8cfb9ac71870df9f69ae518e32a920d08bd170))

## [2.1.0](https://www.github.com/googleapis/python-dialogflow/compare/v2.0.0...v2.1.0) (2021-03-10)


### Features

* add sample code for using regional Dialogflow endpoint ([#254](https://www.github.com/googleapis/python-dialogflow/issues/254)) ([230bb4e](https://www.github.com/googleapis/python-dialogflow/commit/230bb4e5e5b0bee5426c0cb07ea162e92bc75639))
* Add CCAI API ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))
* add additional_bindings to Dialogflow v2beta1 ListIntents API ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))
* add additional_bindings to Dialogflow v2 ListIntents API ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))
* Add from_service_account_info factory ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))


### Bug Fixes

* remove gRPC send/recv limits ([#245](https://www.github.com/googleapis/python-dialogflow/issues/245)) ([ceba454](https://www.github.com/googleapis/python-dialogflow/commit/ceba454ee98f51803415a1fe3235e3f3402d6523))

### Documentation

* clarified voice selection params names ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))
* update comments on parameters and validation result. ([#259](https://www.github.com/googleapis/python-dialogflow/issues/259)) ([f383bb9](https://www.github.com/googleapis/python-dialogflow/commit/f383bb98356e7e4c29838d8888cd0a3cf80fbd6a))


## [2.0.0](https://www.github.com/googleapis/python-dialogflow/compare/v1.1.0...v2.0.0) (2020-12-14)


### ⚠ BREAKING CHANGES

* use microgenerator. See [Migration Guide](https://github.com/googleapis/python-dialogflow/blob/main/UPGRADING.md). (#239)

### Features

* use microgenerator ([#239](https://www.github.com/googleapis/python-dialogflow/issues/239)) ([57c90a5](https://www.github.com/googleapis/python-dialogflow/commit/57c90a5b72668e599047b358f634f939d70a051f))

## [1.1.0](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v1.0.0...v1.1.0) (2020-08-26)


### Features

* add environments client ([#217](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/217)) ([7bf5926](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/7bf592684b4d5df0cd1f66dd414efe2350d0461e))


### Documentation

* move to googleapisdotdev ([#155](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/155)) ([89d071c](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/89d071c55c5bf9c7f766c5b49de7ce33b75222d6))

## [1.0.0](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.8.0...v1.0.0) (2020-05-13)


### Features

* release 1.0.0 ([#192](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/192)) ([33a7263](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/33a7263c18ae72d89263e790f76eb1682fe69c9f)), closes [#189](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/189)
* release_status to production/stable ([#189](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/189)) ([8b995dc](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/8b995dc0dd883e4980a492a67d9c76b7f2603f00))

## [0.8.0](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.7.2...v0.8.0) (2020-03-26)


### Features

* **dialogflow:** add `MediaContent`,  `BrowseCarouselCard`, `ColumnProperties`in v2; add `SpeechContext`, `SpeechWordInfo`in v2; add `enable_word_info`, `speech_contexts`,`model` to InputAudioConfig in v2; add `subtitles` to `Intent.Message.ListSelect` in `v2beta1`; add `language_code` to `ListKnowledgeBase` in v2beta1; add `webhook_headers` to `QueryParameters` in v2beta1 ([#175](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/175)) ([713846b](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/713846b7ed99eaf78cdf383aa9d39b43731b9a0d))
* add validation support to v2; add `output_audio_config_mask` to `detect_intent` method in v2beta1 and v2; add sub agent to v2beta1 (via synth) ([#179](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/179)) ([5a6f18e](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/5a6f18e362b5dd87affbe75e0d0bfc0c21ab87a9))

## [0.7.2](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.7.1...v0.7.2) (2019-10-18)


### Bug Fixes

* define version once in setup.py ([#158](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/158)) ([bf42fc4](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/bf42fc45607b97bc040cbdacbde8ff5a4b6ad29b))

## [0.7.1](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.7.0...v0.7.1) (2019-10-17)


### Bug Fixes

* pin google-api-core>=1.14.0, update format ([#156](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/156)) ([69951d0](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/69951d013b7c99966848565e30d5ab1bad7229fb))

## [0.7.0](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.6.0...v0.7.0) (2019-10-16)


### Features

* regenerate ([#151](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/151)) ([6222277](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/6222277a5332011e9cc2e80bb5b26692a12fad36))
  #### v2 and v2beta1
  * Add `set_agent` and `delete_agent` methods to  `AgentsClient`
  * Add `api_version` and `tier` to `Agents`
  * Add `session_entity_types` to `WebhookResponse`
  * Add `model_variant` and `single_utterance` to `InputAudioConfig`
  * Add `SpeechModelVariant` enum
  * Add `enable_fuzzy_extraction` to `EntityType`
  * Add `KIND_REGEXP` to `EntityType.Kind` enum
  * Add `client_options` to clients
  * Allow kwargs to be passed to transport `create_channel` methods
  * Deprecate `single_utterance` attribute in `StreamingDetectIntentRequest`. Please use `InputAudioConfig.single_utterance`

  #### v2
  * Add Google Hangouts to `Message.Platform` enum

  #### v2beta1 
  * Add `get_validation_result` method to `AgentsClient`
  * Add `gcs_source` and `source` to `reload_document` method in `DocumentsClient`
  * Add Rich Business Messaging (RBM) support, `table_card`, and `media_content` to intent messages
  * Add `enable_word_info`, `speech_contexts` to `InputAudioConfig`
  * `update_document` returns `_OperationFuture` rather than `Operation`
  * Deprecate `projects.agent.knowledgeBases`. Please use `projects.knowledgeBases`.
  * Add `stability`, `speech_word_info` and `speech_end_offset` to `StreamingRecognitionResult`

## 0.6.0

05-06-2019 1:34 PST

### Implementation Changes

- Add routing header to method metadata.([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Warn when deprecated client_config argument is used. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add https://www.googleapis.com/auth/dialogflow OAuth scope. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add channel to gRPC transport classes. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Features

- Add argument output_audio_config to detect_intent. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add update_knowledge_base method. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add update_document and reload_document methods. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Documentation:
- Change copyright year to 2019. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Internal / Testing Changes
- Use mock to patch create_channel in unit tests. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

## 0.5.2

12-18-2018 10:50 PST

### Documentation
- Add notice of Python 2.7 deprecation ([#112](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Fix typo in samples ([#52](https://github.com/googleapis/dialogflow-python-client-v2/pull/52))
- Update README.rst ([#27](https://github.com/googleapis/dialogflow-python-client-v2/pull/27))
- Updating README per ask from Product ([#81](https://github.com/googleapis/dialogflow-python-client-v2/pull/81))
- Add v2beta1 samples for dialogflow and update v2 sample formatting. ([#72](https://github.com/googleapis/dialogflow-python-client-v2/pull/72))

### Internal / Testing Changes
- Update github issue templates ([#103](https://github.com/googleapis/dialogflow-python-client-v2/pull/103))
- Strip dynamic badges from README ([#99](https://github.com/googleapis/dialogflow-python-client-v2/pull/99))
- Correct the repository name in samples README. ([#83](https://github.com/googleapis/dialogflow-python-client-v2/pull/83))
- Fix [#76](https://github.com/googleapis/dialogflow-python-client-v2/pull/76) by adding replacement patterns to dialogflow ([#79](https://github.com/googleapis/dialogflow-python-client-v2/pull/79))

## 0.4.0
- Regenerate v2beta1 endpoint

## 0.3.0
- Regenerate v2 endpoint
- Update documentation comments

## 0.2.0

### New Features
- Add v2 Endpoint (#38)

### Documentation
- Add sample readme, and sample agent (#15)

### Internal / Testing Changes
- Fix typo (#16)
