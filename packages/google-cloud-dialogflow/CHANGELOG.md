# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/dialogflow/#history

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

### [2.1.2](https://www.github.com/googleapis/python-dialogflow/compare/v2.1.1...v2.1.2) (2021-04-13)


### Bug Fixes

* remove unused proto InputText, InputAudio ([#273](https://www.github.com/googleapis/python-dialogflow/issues/273)) ([787d064](https://www.github.com/googleapis/python-dialogflow/commit/787d0648a842b62bfc1be8dcf43c0e8cbd88618a))

### [2.1.1](https://www.github.com/googleapis/python-dialogflow/compare/v2.1.0...v2.1.1) (2021-04-12)


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

* use microgenerator. See [Migration Guide](https://github.com/googleapis/python-dialogflow/blob/master/UPGRADING.md). (#239)

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

### [0.7.2](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.7.1...v0.7.2) (2019-10-18)


### Bug Fixes

* define version once in setup.py ([#158](https://www.github.com/googleapis/dialogflow-python-client-v2/issues/158)) ([bf42fc4](https://www.github.com/googleapis/dialogflow-python-client-v2/commit/bf42fc45607b97bc040cbdacbde8ff5a4b6ad29b))

### [0.7.1](https://www.github.com/googleapis/dialogflow-python-client-v2/compare/v0.7.0...v0.7.1) (2019-10-17)


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
