# Changelog

## [0.4.0](https://www.github.com/googleapis/python-contact-center-insights/compare/v0.3.1...v0.4.0) (2021-09-29)


### Features

* add metadata from dialogflow related to transcript segment ([#54](https://www.github.com/googleapis/python-contact-center-insights/issues/54)) ([ef575cf](https://www.github.com/googleapis/python-contact-center-insights/commit/ef575cf076376261c784b9c3332ef2befa1a11d9))
* add obfuscated if from dialogflow ([ef575cf](https://www.github.com/googleapis/python-contact-center-insights/commit/ef575cf076376261c784b9c3332ef2befa1a11d9))
* add sentiment data for transcript segment ([ef575cf](https://www.github.com/googleapis/python-contact-center-insights/commit/ef575cf076376261c784b9c3332ef2befa1a11d9))

### [0.3.1](https://www.github.com/googleapis/python-contact-center-insights/compare/v0.3.0...v0.3.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([94e64ac](https://www.github.com/googleapis/python-contact-center-insights/commit/94e64acc866eeed789768c2e216dad3f561c81e3))

## [0.3.0](https://www.github.com/googleapis/python-contact-center-insights/compare/v0.2.0...v0.3.0) (2021-09-20)


### Features

* add new issue model API methods ([#25](https://www.github.com/googleapis/python-contact-center-insights/issues/25)) ([16a9bdd](https://www.github.com/googleapis/python-contact-center-insights/commit/16a9bdd90987c82300cf5f3ff03aac05a27e61e9))
* display_name is the display name for the assigned issue ([#32](https://www.github.com/googleapis/python-contact-center-insights/issues/32)) ([5b0fa8e](https://www.github.com/googleapis/python-contact-center-insights/commit/5b0fa8e4047f1f5f7115393b9f7fd1aeaa7ac74d))
* filter is used to filter conversations used for issue model training feat: update_time is used to indicate when the phrase matcher was updated ([#48](https://www.github.com/googleapis/python-contact-center-insights/issues/48)) ([92b9f30](https://www.github.com/googleapis/python-contact-center-insights/commit/92b9f30b3231a8b5ca7c3a9e9da6e5b4db40c568))
* support Dialogflow and user-specified participant IDs ([16a9bdd](https://www.github.com/googleapis/python-contact-center-insights/commit/16a9bdd90987c82300cf5f3ff03aac05a27e61e9))


### Documentation

* update pubsub_notification_settings docs ([16a9bdd](https://www.github.com/googleapis/python-contact-center-insights/commit/16a9bdd90987c82300cf5f3ff03aac05a27e61e9))

## [0.2.0](https://www.github.com/googleapis/python-contact-center-insights/compare/v0.1.1...v0.2.0) (2021-07-24)


### Features

* update contact center insights v1 prior to launch ([#8](https://www.github.com/googleapis/python-contact-center-insights/issues/8)) ([1df2eff](https://www.github.com/googleapis/python-contact-center-insights/commit/1df2eff788db7ed1a867202000af396065d67b9b))


### Bug Fixes

* change nesting of Conversation.Transcript.Participant to ConversationParticipant ([1df2eff](https://www.github.com/googleapis/python-contact-center-insights/commit/1df2eff788db7ed1a867202000af396065d67b9b))
* enable self signed jwt for grpc ([#9](https://www.github.com/googleapis/python-contact-center-insights/issues/9)) ([b1d5d2f](https://www.github.com/googleapis/python-contact-center-insights/commit/b1d5d2f9dba913fd0489fa287dd6c6d2fc7c3213))
* remove AnnotationBoundary.time_offset ([1df2eff](https://www.github.com/googleapis/python-contact-center-insights/commit/1df2eff788db7ed1a867202000af396065d67b9b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#4](https://www.github.com/googleapis/python-contact-center-insights/issues/4)) ([6dcbc56](https://www.github.com/googleapis/python-contact-center-insights/commit/6dcbc567aad97661de34237c8e96f4412bb18223))


### [0.1.1](https://www.github.com/googleapis/python-contact-center-insights/compare/v0.1.0...v0.1.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#3](https://www.github.com/googleapis/python-contact-center-insights/issues/3)) ([3c5be83](https://www.github.com/googleapis/python-contact-center-insights/commit/3c5be834b37e036441b74e2d3464e2367d59e4d6))

## 0.1.0 (2021-07-16)


### Features

* generate v1 ([612875b](https://www.github.com/googleapis/python-contact-center-insights/commit/612875be69712f7571c6ae5d7677ac90c0f36b3c))


### Miscellaneous Chores

* release as 0.1.0 ([#1](https://www.github.com/googleapis/python-contact-center-insights/issues/1)) ([efc26a6](https://www.github.com/googleapis/python-contact-center-insights/commit/efc26a64242cb6a46600858f8229ea805d407d8a))
