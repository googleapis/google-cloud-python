# Changelog

## [0.6.0](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.5.0...v0.6.0) (2021-06-07)


### Features

* support sentiment analysis in bot testing ([#98](https://www.github.com/googleapis/python-dialogflow-cx/issues/98)) ([db258bc](https://www.github.com/googleapis/python-dialogflow-cx/commit/db258bcc9971542e347b50f396bd51ec88520fde))

## [0.5.0](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.4.1...v0.5.0) (2021-05-28)


### Features

* add export / import flow API ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* add support for service directory webhooks ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* added API for continuous test ([#91](https://www.github.com/googleapis/python-dialogflow-cx/issues/91)) ([81d4f53](https://www.github.com/googleapis/python-dialogflow-cx/commit/81d4f53cd4a4080b21221126dacaf2e13ca2efcf))
* added API for running continuous test ([#94](https://www.github.com/googleapis/python-dialogflow-cx/issues/94)) ([cc30fa3](https://www.github.com/googleapis/python-dialogflow-cx/commit/cc30fa3e767bac2f33637ce1c29766ff41e9225b))
* added fallback option when restoring an agent ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* Expose supported languages of the agent; ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* include original user query in WebhookRequest; add GetTextCaseresult API. ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* support self-signed JWT flow for service accounts ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))


### Bug Fixes

* add async client to %name_%version/init.py ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* require google-api-core>=1.22.2 ([3440f18](https://www.github.com/googleapis/python-dialogflow-cx/commit/3440f186cd879fd4ddc9b3442bf857a4f286698e))
* **v3:** BREAKING rename `UserInput.input_` to `UserInput.input` ([#58](https://www.github.com/googleapis/python-dialogflow-cx/issues/58)) ([3440f18](https://www.github.com/googleapis/python-dialogflow-cx/commit/3440f186cd879fd4ddc9b3442bf857a4f286698e))


### Documentation

* clarified documentation for security settings docs: clarified documentation for session parameters ([#89](https://www.github.com/googleapis/python-dialogflow-cx/issues/89)) ([750a055](https://www.github.com/googleapis/python-dialogflow-cx/commit/750a055b688ebeda8e8882cdb02bdc87524a69a5))
* clarified documentation for security settings docs: clarified documentation for session parameters ([#90](https://www.github.com/googleapis/python-dialogflow-cx/issues/90)) ([c1c0fb9](https://www.github.com/googleapis/python-dialogflow-cx/commit/c1c0fb9eb9e62dc794aef1bac357bb5c20e322dc))
* clarified experiment length ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* clarify resource format for session response. ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))
* Update docs on Pages, Session, Version, etc. ([20df7c3](https://www.github.com/googleapis/python-dialogflow-cx/commit/20df7c3bfabef5da23970512a3f925f4dfe7d2f9))

### [0.4.1](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.4.0...v0.4.1) (2021-03-07)


### Documentation

* fix readme ([#52](https://www.github.com/googleapis/python-dialogflow-cx/issues/52)) ([8728ad4](https://www.github.com/googleapis/python-dialogflow-cx/commit/8728ad4018bf9c976cdc469af3d8a7ec89c04671))

## [0.4.0](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.3.0...v0.4.0) (2021-03-05)


### Features

* add from_service_account_info factory ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))
* Add new Experiment service ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))
* added support for test cases and agent validation ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))
* allow to disable webhook invocation per request ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))
* supports SentimentAnalysisResult in webhook request ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))


### Documentation

* test cases doc update ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))
* update languages link ([d9bd192](https://www.github.com/googleapis/python-dialogflow-cx/commit/d9bd192a87bc8a4462da3bdbda362b359d86dd65))

## [0.3.0](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.2.0...v0.3.0) (2021-01-29)


### Features

* add experiments API ([#36](https://www.github.com/googleapis/python-dialogflow-cx/issues/36)) ([5381512](https://www.github.com/googleapis/python-dialogflow-cx/commit/5381512872ca2492ddabcbdd7ccde5f054aed011))
* allowed custom to specify webhook headers through query parameters ([#32](https://www.github.com/googleapis/python-dialogflow-cx/issues/32)) ([09919b0](https://www.github.com/googleapis/python-dialogflow-cx/commit/09919b0e45517cedcbb1d8b5b931c7317be549b2))
* allowed custom to specify webhook headers through query parameters ([#32](https://www.github.com/googleapis/python-dialogflow-cx/issues/32)) ([09919b0](https://www.github.com/googleapis/python-dialogflow-cx/commit/09919b0e45517cedcbb1d8b5b931c7317be549b2))


### Bug Fixes

* remove gRPC send/recv limit; add enums to `types/__init__.py` ([09919b0](https://www.github.com/googleapis/python-dialogflow-cx/commit/09919b0e45517cedcbb1d8b5b931c7317be549b2))

## [0.2.0](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.1.1...v0.2.0) (2020-12-07)


### Features

* add v3 ([#21](https://www.github.com/googleapis/python-dialogflow-cx/issues/21)) ([97c7fb5](https://www.github.com/googleapis/python-dialogflow-cx/commit/97c7fb53e5f6af7d8b0fea3043c60da9ee1f549b))

### [0.1.1](https://www.github.com/googleapis/python-dialogflow-cx/compare/v0.1.0...v0.1.1) (2020-11-17)


### Bug Fixes

* corrects the repo/homepage link ([#15](https://www.github.com/googleapis/python-dialogflow-cx/issues/15)) ([c26852d](https://www.github.com/googleapis/python-dialogflow-cx/commit/c26852d8a3738eb4d67222c555d0197a854e68a9))


### Documentation

* **samples:** add initial sample codes ([#13](https://www.github.com/googleapis/python-dialogflow-cx/issues/13)) ([b590308](https://www.github.com/googleapis/python-dialogflow-cx/commit/b590308b79a230561aed776f55260a73668c8efc)), closes [#12](https://www.github.com/googleapis/python-dialogflow-cx/issues/12)

## 0.1.0 (2020-08-24)


### Features

* generate v3beta1 ([0c6e3a9](https://www.github.com/googleapis/python-dialogflow-cx/commit/0c6e3a9ff1a38f6d6c5f8c2983cbfa1f7ff7536d))
