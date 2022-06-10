# Changelog


## [1.0.1](https://github.com/googleapis/gapic-generator-python/compare/v1.0.0...v1.0.1) (2022-06-10)


### Bug Fixes

* add missing metadata. ([#1335](https://github.com/googleapis/gapic-generator-python/issues/1335)) ([228efda](https://github.com/googleapis/gapic-generator-python/commit/228efdab198dd18de82df2be1b8d858b78811a89))

## [1.0.0](https://github.com/googleapis/gapic-generator-python/compare/v0.65.3...v1.0.0) (2022-05-24)


### Features

* adds LRO mixin. ([#1304](https://github.com/googleapis/gapic-generator-python/issues/1304)) ([18af90a](https://github.com/googleapis/gapic-generator-python/commit/18af90a8b51159da85f3f93bd37248a58ede4ab3))
* release as stable ([767aaba](https://github.com/googleapis/gapic-generator-python/commit/767aaba6d623fab2af972140ffd4de3b43a92439))

### [0.65.3](https://github.com/googleapis/gapic-generator-python/compare/v0.65.2...v0.65.3) (2022-05-03)


### Bug Fixes

* don't use stale session in rest transport ([#1291](https://github.com/googleapis/gapic-generator-python/issues/1291)) ([a96ef9e](https://github.com/googleapis/gapic-generator-python/commit/a96ef9ef3f99b0114f1d5630ee6e8907dd24bec2))

### [0.65.2](https://github.com/googleapis/gapic-generator-python/compare/v0.65.1...v0.65.2) (2022-04-21)


### Bug Fixes

* disambiguate method names ([#1282](https://github.com/googleapis/gapic-generator-python/issues/1282)) ([efe7216](https://github.com/googleapis/gapic-generator-python/commit/efe7216d8d59d945b4ea90ad109248b9eecc33e5))
* fixes bug when an annotation path in an http rule does not have =. ([#1284](https://github.com/googleapis/gapic-generator-python/issues/1284)) ([6dcb97c](https://github.com/googleapis/gapic-generator-python/commit/6dcb97cfb60d7d81dc205c20c762dfd5e74659e1))
* use async snippet in async client method docstring ([#1280](https://github.com/googleapis/gapic-generator-python/issues/1280)) ([b72e1e0](https://github.com/googleapis/gapic-generator-python/commit/b72e1e063d587a93b65aa77dd222341bcc87ba39))

### [0.65.1](https://github.com/googleapis/gapic-generator-python/compare/v0.65.0...v0.65.1) (2022-04-13)


### Bug Fixes

* correct import for request message type ([#1273](https://github.com/googleapis/gapic-generator-python/issues/1273)) ([3406d9e](https://github.com/googleapis/gapic-generator-python/commit/3406d9e0336d2fe698b90a95e20f6aacec79763b))
* use google-api-core==2.7.2 ([#1276](https://github.com/googleapis/gapic-generator-python/issues/1276)) ([5ab8eb5](https://github.com/googleapis/gapic-generator-python/commit/5ab8eb5a36c64e521b475cb0c045f507400d8f27))

## [0.65.0](https://github.com/googleapis/gapic-generator-python/compare/v0.64.0...v0.65.0) (2022-04-09)


### Features

* adds support for MixIns. ([#1240](https://github.com/googleapis/gapic-generator-python/issues/1240)) ([856af2e](https://github.com/googleapis/gapic-generator-python/commit/856af2ef406e0ea380fcfaa5d505435124330c25))

## [0.64.0](https://github.com/googleapis/gapic-generator-python/compare/v0.63.8...v0.64.0) (2022-04-08)


### Features

* full LRO for Extended Operations ([#1234](https://github.com/googleapis/gapic-generator-python/issues/1234)) ([4d1bccc](https://github.com/googleapis/gapic-generator-python/commit/4d1bccc965a6908e9b1aeaebf1327918f3e2042a))


### Bug Fixes

* add missing import for Mapping ([#1267](https://github.com/googleapis/gapic-generator-python/issues/1267)) ([f416622](https://github.com/googleapis/gapic-generator-python/commit/f416622c753a56036cf9ac1fa6eb818a6e557018))

### [0.63.8](https://github.com/googleapis/gapic-generator-python/compare/v0.63.7...v0.63.8) (2022-04-04)


### Bug Fixes

* **deps:** exclude click 8.1.0 ([#1255](https://github.com/googleapis/gapic-generator-python/issues/1255)) ([daf63eb](https://github.com/googleapis/gapic-generator-python/commit/daf63ebe2392fd6fde65326fffc5519cd126c2ae))
* fix docstring for map fields ([#1249](https://github.com/googleapis/gapic-generator-python/issues/1249)) ([3100464](https://github.com/googleapis/gapic-generator-python/commit/310046478092b4fc4ef9dfdd1e50363ca6fc72c5))
* sanitize file names ([#1236](https://github.com/googleapis/gapic-generator-python/issues/1236)) ([3072ffb](https://github.com/googleapis/gapic-generator-python/commit/3072ffb6000983ecb06d8dd7b44f77da61cc992e))

### [0.63.7](https://github.com/googleapis/gapic-generator-python/compare/v0.63.6...v0.63.7) (2022-03-08)


### Bug Fixes

* resolve issue where rest transport is not used in certain tests ([#1231](https://github.com/googleapis/gapic-generator-python/issues/1231)) ([90ab41a](https://github.com/googleapis/gapic-generator-python/commit/90ab41ab1f1b058ec0eb4a96b973031898f64df0))

### [0.63.6](https://github.com/googleapis/gapic-generator-python/compare/v0.63.5...v0.63.6) (2022-03-04)


### Bug Fixes

* **deps:** require google-api-core >=2.3.2 ([#1225](https://github.com/googleapis/gapic-generator-python/issues/1225)) ([f59917f](https://github.com/googleapis/gapic-generator-python/commit/f59917fdbdf5ee4091e35d721811dcd7f4b9a3f3))

### [0.63.5](https://github.com/googleapis/gapic-generator-python/compare/v0.63.4...v0.63.5) (2022-02-25)


### Bug Fixes

* update license year to 2022 ([#1199](https://github.com/googleapis/gapic-generator-python/issues/1199)) ([31292d5](https://github.com/googleapis/gapic-generator-python/commit/31292d59c8d08695f3e2dfa75861c86d723a9d35))

### [0.63.4](https://github.com/googleapis/gapic-generator-python/compare/v0.63.3...v0.63.4) (2022-02-22)


### Bug Fixes

* fix snippet region tag format ([#1210](https://github.com/googleapis/gapic-generator-python/issues/1210)) ([e895106](https://github.com/googleapis/gapic-generator-python/commit/e8951064827c726bb651801336b86188e2628386))

### [0.63.3](https://github.com/googleapis/gapic-generator-python/compare/v0.63.2...v0.63.3) (2022-02-16)


### Bug Fixes

* disambiguate field headers whose names are reserved python words ([#1178](https://github.com/googleapis/gapic-generator-python/issues/1178)) ([98aa690](https://github.com/googleapis/gapic-generator-python/commit/98aa6906031276dcad899fdb88f47cbafc651ae4))
* fix docstring code block formatting ([#1206](https://github.com/googleapis/gapic-generator-python/issues/1206)) ([500dfe7](https://github.com/googleapis/gapic-generator-python/commit/500dfe7e401888b3bea6488d6e6fee9955f1a2ab))
* HTTP body field messages with enums or recursive fields ([#1201](https://github.com/googleapis/gapic-generator-python/issues/1201)) ([246bfe2](https://github.com/googleapis/gapic-generator-python/commit/246bfe2948362bc8f6035aafc0dbd9e65f5acc2b))

### [0.63.2](https://github.com/googleapis/gapic-generator-python/compare/v0.63.1...v0.63.2) (2022-02-09)


### Bug Fixes

* fix lint sessions on generated samples ([#1192](https://github.com/googleapis/gapic-generator-python/issues/1192)) ([4d0ea18](https://github.com/googleapis/gapic-generator-python/commit/4d0ea182aa5500eee0f5485e88e14043974ae78b))

### [0.63.1](https://github.com/googleapis/gapic-generator-python/compare/v0.63.0...v0.63.1) (2022-02-03)


### Bug Fixes

* disambiguate method names that are reserved in transport classes ([#1187](https://github.com/googleapis/gapic-generator-python/issues/1187)) ([78626d8](https://github.com/googleapis/gapic-generator-python/commit/78626d89665128ef7d078ee12b49480475cce9e2))

## [0.63.0](https://github.com/googleapis/gapic-generator-python/compare/v0.62.1...v0.63.0) (2022-02-03)


### Features

* adds dynamic routing files. ([8c191a5](https://github.com/googleapis/gapic-generator-python/commit/8c191a5475f208213806fff81c0efa1d26216cd9))
* adds dynamic routing. ([#1135](https://github.com/googleapis/gapic-generator-python/issues/1135)) ([8c191a5](https://github.com/googleapis/gapic-generator-python/commit/8c191a5475f208213806fff81c0efa1d26216cd9))
* enable snippetgen for default templates ([#1171](https://github.com/googleapis/gapic-generator-python/issues/1171)) ([c1af051](https://github.com/googleapis/gapic-generator-python/commit/c1af051743dde2fb40e028c51de85dfea47a793d))

### [0.62.1](https://github.com/googleapis/gapic-generator-python/compare/v0.62.0...v0.62.1) (2022-02-02)


### Bug Fixes

* **deps:** require setuptools<=60.5.0 ([#1179](https://github.com/googleapis/gapic-generator-python/issues/1179)) ([fb56af7](https://github.com/googleapis/gapic-generator-python/commit/fb56af7cd33931f6747b5ce1fb8502bcbc74dcc7))

## [0.62.0](https://github.com/googleapis/gapic-generator-python/compare/v0.61.0...v0.62.0) (2022-01-28)


### Features

* adds REST server-streaming support. ([#1120](https://github.com/googleapis/gapic-generator-python/issues/1120)) ([812cf3e](https://github.com/googleapis/gapic-generator-python/commit/812cf3e0d11b67f7ecd60b9c643b032370bb9400))
* expose extended operations annotations within generator ([#1145](https://github.com/googleapis/gapic-generator-python/issues/1145)) ([e7bee70](https://github.com/googleapis/gapic-generator-python/commit/e7bee702e92612f88efca782a68d8884b9c71feb))


### Bug Fixes

* add special method parameters to set of reserved module names ([#1168](https://github.com/googleapis/gapic-generator-python/issues/1168)) ([8078961](https://github.com/googleapis/gapic-generator-python/commit/8078961f68d2f34fff6403d318bf95c844889d78))
* fix snippetgen golden file ([#1170](https://github.com/googleapis/gapic-generator-python/issues/1170)) ([13b2028](https://github.com/googleapis/gapic-generator-python/commit/13b2028df5193f11aee40ae42ea5186aeb25eef3))
* **snippetgen:** remove special handling for resource paths ([#1134](https://github.com/googleapis/gapic-generator-python/issues/1134)) ([4ea2d11](https://github.com/googleapis/gapic-generator-python/commit/4ea2d114b670c2f2adb43cd87e5f0cf7750e5407))

## [0.61.0](https://github.com/googleapis/gapic-generator-python/compare/v0.60.0...v0.61.0) (2022-01-28)


### Features

* add interceptor-like functionality to REST transport ([#1142](https://github.com/googleapis/gapic-generator-python/issues/1142)) ([fe57eb2](https://github.com/googleapis/gapic-generator-python/commit/fe57eb26badb596fd9bd8a0b8b65f00f060b009d))


### Bug Fixes

* preserve hyperlinks with hyphens ([#1140](https://github.com/googleapis/gapic-generator-python/issues/1140)) ([b091bfc](https://github.com/googleapis/gapic-generator-python/commit/b091bfc523ee40af4ef0b28abfc0c26dcdf09ebe)), closes [#1131](https://github.com/googleapis/gapic-generator-python/issues/1131)
* resolve DuplicateCredentialArgs when using credentials_file ([#1159](https://github.com/googleapis/gapic-generator-python/issues/1159)) ([fccd2ba](https://github.com/googleapis/gapic-generator-python/commit/fccd2ba4f67c92bce5d9f7a2d59d5f1ea28829b5))

## [0.60.0](https://github.com/googleapis/gapic-generator-python/compare/v0.59.1...v0.60.0) (2022-01-19)


### Features

* add api key support ([#969](https://github.com/googleapis/gapic-generator-python/issues/969)) ([7c72739](https://github.com/googleapis/gapic-generator-python/commit/7c7273919193f321e0dc2d4156b35be1b4733458))
* generate snippet metadata  ([#1129](https://github.com/googleapis/gapic-generator-python/issues/1129)) ([9e46031](https://github.com/googleapis/gapic-generator-python/commit/9e46031d01edc3a461140fe3b29d8d400f5ddf86))


### Bug Fixes

* only set unset fields if they are query params ([#1130](https://github.com/googleapis/gapic-generator-python/issues/1130)) ([9ad98ca](https://github.com/googleapis/gapic-generator-python/commit/9ad98ca6833f1b280bf3c04c858f92276d59ffbe))

### [0.59.1](https://github.com/googleapis/gapic-generator-python/compare/v0.59.0...v0.59.1) (2022-01-10)


### Bug Fixes

* refactor mtls logic to standalone method ([#1123](https://github.com/googleapis/gapic-generator-python/issues/1123)) ([d528223](https://github.com/googleapis/gapic-generator-python/commit/d528223e3221487f86a3d82c92cd2e2cf04bec4a))

## [0.59.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.58.4...v0.59.0) (2022-01-10)


### Features

* add snippet index ([#1121](https://www.github.com/googleapis/gapic-generator-python/issues/1121)) ([55d2bc6](https://www.github.com/googleapis/gapic-generator-python/commit/55d2bc6580e5db0f837de1b245533a8f1f2e9beb))

### [0.58.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.58.3...v0.58.4) (2021-12-30)


### Bug Fixes

* handle message bodies ([#1117](https://www.github.com/googleapis/gapic-generator-python/issues/1117)) ([36e3236](https://github.com/googleapis/gapic-generator-python/commit/36e3236b3832993331d8d99c10e72797a8851390))


### [0.58.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.58.2...v0.58.3) (2021-12-28)


### Bug Fixes

* add additional reserved names for disambiguation ([#1114](https://www.github.com/googleapis/gapic-generator-python/issues/1114)) ([1cffd8d](https://www.github.com/googleapis/gapic-generator-python/commit/1cffd8d99936cd10649faf05e0288b693e718f81))

### [0.58.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.58.1...v0.58.2) (2021-12-13)


### Bug Fixes

* fix case for expected field names in required fields test. ([#1107](https://www.github.com/googleapis/gapic-generator-python/issues/1107)) ([6a593f9](https://www.github.com/googleapis/gapic-generator-python/commit/6a593f9807141aaf6c13a8843804e9fa9b300c91))
* non-string required fields provide correct values ([#1108](https://www.github.com/googleapis/gapic-generator-python/issues/1108)) ([bc5f729](https://www.github.com/googleapis/gapic-generator-python/commit/bc5f729cf777d30e1053e23a1d115460952478af))
* syntax fix and test for multiple required fields ([#1105](https://www.github.com/googleapis/gapic-generator-python/issues/1105)) ([4e5fe2d](https://www.github.com/googleapis/gapic-generator-python/commit/4e5fe2db9d0d81929cc1559d3a134c9a38ae595c))

### [0.58.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.58.0...v0.58.1) (2021-12-09)


### Bug Fixes

* syntax fix for required_fields struct in rest transport ([#1103](https://www.github.com/googleapis/gapic-generator-python/issues/1103)) ([3d7128c](https://www.github.com/googleapis/gapic-generator-python/commit/3d7128ce8f55523b9aff2e44e2c000450e712ac2))

## [0.58.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.57.0...v0.58.0) (2021-12-07)


### Features

* add support for long-running operations with rest transport. ([#1094](https://www.github.com/googleapis/gapic-generator-python/issues/1094)) ([e89fd23](https://www.github.com/googleapis/gapic-generator-python/commit/e89fd23609625c5aa49acd6c6ee67f87fce324fd))


### Bug Fixes

* ensure rest unit tests have complete coverage ([#1098](https://www.github.com/googleapis/gapic-generator-python/issues/1098)) ([0705d9c](https://www.github.com/googleapis/gapic-generator-python/commit/0705d9c5dbbea793867551e64991be37d8339c6b))
* fix resource path args for paths with =** ([#1089](https://www.github.com/googleapis/gapic-generator-python/issues/1089)) ([309cc66](https://www.github.com/googleapis/gapic-generator-python/commit/309cc66e880e07940866864b03c744310ef56762))
* **snippetgen:** don't create duplicate requests for required oneofs ([#1088](https://www.github.com/googleapis/gapic-generator-python/issues/1088)) ([5531795](https://www.github.com/googleapis/gapic-generator-python/commit/55317956397370a91b1a06ecd476e55f58789807))

## [0.57.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.56.2...v0.57.0) (2021-11-17)


### Features

* forward compatible diregapic LRO support ([#1085](https://www.github.com/googleapis/gapic-generator-python/issues/1085)) ([aa7f4d5](https://www.github.com/googleapis/gapic-generator-python/commit/aa7f4d568f7f43738ab3489fc84ce6bc5d6bda18))

### [0.56.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.56.1...v0.56.2) (2021-11-08)


### Bug Fixes

* don't enable snippetgen by default ([#1078](https://www.github.com/googleapis/gapic-generator-python/issues/1078)) ([8bdb709](https://www.github.com/googleapis/gapic-generator-python/commit/8bdb70931a9ecb1c89fda9608697b0762770bc12))

### [0.56.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.56.0...v0.56.1) (2021-11-08)


### Bug Fixes

* **snippetgen:** fix client streaming samples ([#1061](https://www.github.com/googleapis/gapic-generator-python/issues/1061)) ([64b9ad6](https://www.github.com/googleapis/gapic-generator-python/commit/64b9ad6e417a15cfbddf0e7a1b57036b8abfc829))

## [0.56.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.55.1...v0.56.0) (2021-11-05)


### Features

* **snippetgen:** turn resource path strings into f-strings ([#1012](https://www.github.com/googleapis/gapic-generator-python/issues/1012)) ([a110e1d](https://www.github.com/googleapis/gapic-generator-python/commit/a110e1d8387ea37b85ab0621bacd30da175fe85b))


### Bug Fixes

* fix rest unit test ([#1074](https://www.github.com/googleapis/gapic-generator-python/issues/1074)) ([3b2918e](https://www.github.com/googleapis/gapic-generator-python/commit/3b2918ecaeb90229f22834438dc31755498ee2d0))

### [0.55.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.55.0...v0.55.1) (2021-11-04)


### Bug Fixes

* fix missing http schema (http/https) for REST clients ([#1063](https://www.github.com/googleapis/gapic-generator-python/issues/1063)) ([e3aa7a0](https://www.github.com/googleapis/gapic-generator-python/commit/e3aa7a0b23bc4bfd5170753f74bdeac219902d1a))
* handle required fields properly in query_params ([#1068](https://www.github.com/googleapis/gapic-generator-python/issues/1068)) ([0e379ca](https://www.github.com/googleapis/gapic-generator-python/commit/0e379ca6c0aee9d79d11a14074b7e9343e9e6af2))
* leave a newline between field description and oneof line ([#1071](https://www.github.com/googleapis/gapic-generator-python/issues/1071)) ([4d0e365](https://www.github.com/googleapis/gapic-generator-python/commit/4d0e36528a8eb23ea3893b0bbcca10b679867445))
* suppress type error for fallback def of OptionalRetry ([#1065](https://www.github.com/googleapis/gapic-generator-python/issues/1065)) ([e47faa6](https://www.github.com/googleapis/gapic-generator-python/commit/e47faa6c59a1fadf7dfebc965c962aa05ca30f74))
* unignore 'google.api_core' imports ([#1066](https://www.github.com/googleapis/gapic-generator-python/issues/1066)) ([13f764c](https://www.github.com/googleapis/gapic-generator-python/commit/13f764c6513b91e7143a4a4a0bcc661cd19be0d8))
* use (new) typing for 'gapic_v1.method.DEFAULT' ([#1032](https://www.github.com/googleapis/gapic-generator-python/issues/1032)) ([d85dfad](https://www.github.com/googleapis/gapic-generator-python/commit/d85dfadc180e5f218ad582a306c1c441a6c668db))

## [0.55.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.54.0...v0.55.0) (2021-11-01)


### Features

* add fragment tests ([#1056](https://www.github.com/googleapis/gapic-generator-python/issues/1056)) ([9d9b33d](https://www.github.com/googleapis/gapic-generator-python/commit/9d9b33dadf587a6d0b09031edeea597d6d2eae62))

## [0.54.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.53.4...v0.54.0) (2021-10-29)


### Features

* generate code snippets by default ([#1044](https://www.github.com/googleapis/gapic-generator-python/issues/1044)) ([e46f443](https://www.github.com/googleapis/gapic-generator-python/commit/e46f443dbeffe16b63f97668801b06189769e972))

### [0.53.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.53.3...v0.53.4) (2021-10-29)


### Bug Fixes

* add 'dict' type annotation to 'request' for async_client ([#1051](https://www.github.com/googleapis/gapic-generator-python/issues/1051)) ([08cc2c4](https://www.github.com/googleapis/gapic-generator-python/commit/08cc2c4c85297759892782e307bcaa63dff41212))
* fix tests generation logic ([#1049](https://www.github.com/googleapis/gapic-generator-python/issues/1049)) ([8f213ad](https://www.github.com/googleapis/gapic-generator-python/commit/8f213add4cb02366bb370ef46a686c6f0c37a575))
* methods returning Operation w/o operation_info are now allowed. ([#1047](https://www.github.com/googleapis/gapic-generator-python/issues/1047)) ([6b640af](https://www.github.com/googleapis/gapic-generator-python/commit/6b640afbd93ea8c861b902211dc34e188234d072))

### [0.53.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.53.2...v0.53.3) (2021-10-27)


### Bug Fixes

* more fixes for rest transport ([#1042](https://www.github.com/googleapis/gapic-generator-python/issues/1042)) ([13d5f77](https://www.github.com/googleapis/gapic-generator-python/commit/13d5f77f8b6d4ce1181b29f2335d7584783be753))

### [0.53.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.53.1...v0.53.2) (2021-10-27)


### Bug Fixes

* Adjust Field Names in URI Templates ([#1041](https://www.github.com/googleapis/gapic-generator-python/issues/1041)) ([06cd7b6](https://www.github.com/googleapis/gapic-generator-python/commit/06cd7b66f0f303b066f7f1f510332ae19aa9de8e))
* Fix rest transport logic ([#1039](https://www.github.com/googleapis/gapic-generator-python/issues/1039)) ([50d61af](https://www.github.com/googleapis/gapic-generator-python/commit/50d61afd30b021835fe898e41b783f4d04acff09))
* list oneofs in docstring ([#1030](https://www.github.com/googleapis/gapic-generator-python/issues/1030)) ([a0e25c8](https://www.github.com/googleapis/gapic-generator-python/commit/a0e25c8c00391b99a351e667eddc8b4fecad30d8))

### [0.53.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.53.0...v0.53.1) (2021-10-13)


### Bug Fixes

* use correct typing for retries / operations_client ([#1026](https://www.github.com/googleapis/gapic-generator-python/issues/1026)) ([acb3ea8](https://www.github.com/googleapis/gapic-generator-python/commit/acb3ea83becf6bf85c142739dede556cae2cebae))

## [0.53.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.52.0...v0.53.0) (2021-10-04)


### Features

* add support for context manager in client ([#987](https://www.github.com/googleapis/gapic-generator-python/issues/987)) ([4edabcf](https://www.github.com/googleapis/gapic-generator-python/commit/4edabcf6791cfb0874a951b695b39672036760d4))
* enable self signed jwt for http ([#1000](https://www.github.com/googleapis/gapic-generator-python/issues/1000)) ([5f87973](https://www.github.com/googleapis/gapic-generator-python/commit/5f8797396a2477b772b7bfb827499db32e28710e))
* implement grpc transcode for rest transport and complete generated tests ([#999](https://www.github.com/googleapis/gapic-generator-python/issues/999)) ([ccdd17d](https://www.github.com/googleapis/gapic-generator-python/commit/ccdd17d6133274a34dd727fab0576e6c63238833))
* implement grpc transcode for rest transport and complete generated tests. ([ccdd17d](https://www.github.com/googleapis/gapic-generator-python/commit/ccdd17d6133274a34dd727fab0576e6c63238833))


### Bug Fixes

* fix docstring for first attribute of protos ([#1004](https://www.github.com/googleapis/gapic-generator-python/issues/1004)) ([383f655](https://www.github.com/googleapis/gapic-generator-python/commit/383f6555a1d850889b2aa74be28c8d06465399e5))

## [0.52.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.51.2...v0.52.0) (2021-09-29)


### Features

* Support alternative http bindings in the gapic schema. ([#993](https://www.github.com/googleapis/gapic-generator-python/issues/993)) ([041a726](https://www.github.com/googleapis/gapic-generator-python/commit/041a726b818cd67812d689c23757f31ec9964d66))


### Bug Fixes

* improper types in pagers generation ([#970](https://www.github.com/googleapis/gapic-generator-python/issues/970)) ([bba3eea](https://www.github.com/googleapis/gapic-generator-python/commit/bba3eea5d45fe57c0395ceef30402ad7880013d7))

### [0.51.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.51.1...v0.51.2) (2021-09-13)


### Bug Fixes

* add a separate DEFAULT_CLIENT_INFO for rest clients ([#988](https://www.github.com/googleapis/gapic-generator-python/issues/988)) ([22ac400](https://www.github.com/googleapis/gapic-generator-python/commit/22ac40097ab50bb2d3a7f1a2d35d659c391e0927))
* **snippetgen:** use f-strings in print statements ([#975](https://www.github.com/googleapis/gapic-generator-python/issues/975)) ([122e85c](https://www.github.com/googleapis/gapic-generator-python/commit/122e85c37ff6aa0a99f64361397eb3df5495a3b4))

### [0.51.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.51.0...v0.51.1) (2021-08-20)


### Bug Fixes

* timeouts are handled by rest clients, retries silently ignored ([#976](https://www.github.com/googleapis/gapic-generator-python/issues/976)) ([a62463c](https://www.github.com/googleapis/gapic-generator-python/commit/a62463cadee0cdaf861e93998faa27e6a82adab4))

## [0.51.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.5...v0.51.0) (2021-08-18)


### Features

* **snippetgen:** generate mock input for required fields ([#941](https://www.github.com/googleapis/gapic-generator-python/issues/941)) ([b2149da](https://www.github.com/googleapis/gapic-generator-python/commit/b2149da5e6873e1f71871bfecd899bb9aa0b6439))


### Bug Fixes

* add 'dict' type annotation to 'request' ([#966](https://www.github.com/googleapis/gapic-generator-python/issues/966)) ([49205d9](https://www.github.com/googleapis/gapic-generator-python/commit/49205d99dd440690b838c8eb3f6a695f35b061c2))

### [0.50.5](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.4...v0.50.5) (2021-07-22)


### Bug Fixes

* enable self signed jwt for grpc ([#958](https://www.github.com/googleapis/gapic-generator-python/issues/958)) ([af02a9c](https://www.github.com/googleapis/gapic-generator-python/commit/af02a9cae522ff2cdc8e97cfffe2ba2bb84d6b6a))
* fix rest transport unit test and required query prams handling ([#951](https://www.github.com/googleapis/gapic-generator-python/issues/951)) ([b793017](https://www.github.com/googleapis/gapic-generator-python/commit/b7930177da9a8be556bf6485febcc0a9bdef897b))

### [0.50.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.3...v0.50.4) (2021-06-30)


### Bug Fixes

* fix syntax for Deprecationwarning ([#942](https://www.github.com/googleapis/gapic-generator-python/issues/942)) ([82dbddb](https://www.github.com/googleapis/gapic-generator-python/commit/82dbddb6a9caf1227c4b335345f365dd01025794))

### [0.50.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.2...v0.50.3) (2021-06-29)


### Bug Fixes

* disable always_use_jwt_access ([#939](https://www.github.com/googleapis/gapic-generator-python/issues/939)) ([1302352](https://www.github.com/googleapis/gapic-generator-python/commit/130235220849987df572c1840735b3c199b85dfc))

### [0.50.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.1...v0.50.2) (2021-06-28)


### Bug Fixes

* fix wrong scopes for self signed jwt ([#935](https://www.github.com/googleapis/gapic-generator-python/issues/935)) ([e033acd](https://www.github.com/googleapis/gapic-generator-python/commit/e033acd44763f7cf65eabb6b35f66093022b1bcb))
* import warnings when needed ([#930](https://www.github.com/googleapis/gapic-generator-python/issues/930)) ([d4270ae](https://www.github.com/googleapis/gapic-generator-python/commit/d4270ae5805f44ab8ee30bb11fe42a0da6d79755))

### [0.50.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.50.0...v0.50.1) (2021-06-24)


### Bug Fixes

* **bazel:** Re-enable Python µgen integration tests post monolith rule removal ([#926](https://www.github.com/googleapis/gapic-generator-python/issues/926)) ([13a6b3a](https://www.github.com/googleapis/gapic-generator-python/commit/13a6b3aed35b5af85aea047922aa219258460a58))

## [0.50.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.49.0...v0.50.0) (2021-06-21)


### Features

* enable self signed jwt for grpc ([#920](https://www.github.com/googleapis/gapic-generator-python/issues/920)) ([da119c7](https://www.github.com/googleapis/gapic-generator-python/commit/da119c72c82d04e168c4b41e5bf910a0c1609ce3))


### Bug Fixes

* **bazel:** Remove monolith imports from Python µgen Bazel rules ([#923](https://www.github.com/googleapis/gapic-generator-python/issues/923)) ([4a2afa7](https://www.github.com/googleapis/gapic-generator-python/commit/4a2afa78455817e7e6c058d21857326867fe3f21))
* temporarily disable code coverage in showcase_unit tests ([#925](https://www.github.com/googleapis/gapic-generator-python/issues/925)) ([0dfac03](https://www.github.com/googleapis/gapic-generator-python/commit/0dfac03bd3ef8c12b33e6c03e62eab3e7bf2cd69))

## [0.49.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.48.1...v0.49.0) (2021-06-11)


### Features

* add async samples ([#861](https://www.github.com/googleapis/gapic-generator-python/issues/861)) ([e385ffd](https://www.github.com/googleapis/gapic-generator-python/commit/e385ffd7f012c6a38c9fcd7c5f36ce090311032b))

### [0.48.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.48.0...v0.48.1) (2021-06-09)


### Bug Fixes

* samplegen always produces sample dicts with "response" ([#914](https://www.github.com/googleapis/gapic-generator-python/issues/914)) ([0b168f2](https://www.github.com/googleapis/gapic-generator-python/commit/0b168f20f4cbf419131fcc512141fccca8186681))

## [0.48.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.47.0...v0.48.0) (2021-05-27)


### Features

* Add `x-goog-api-client` header to rest clients ([#888](https://www.github.com/googleapis/gapic-generator-python/issues/888)) ([2d1d3ae](https://www.github.com/googleapis/gapic-generator-python/commit/2d1d3ae135a75bbfff13df7703de5d0dad44695c))
* **dev:** Add Git pre-commit hooks [gapic-generator-python] ([#908](https://www.github.com/googleapis/gapic-generator-python/issues/908)) ([298db39](https://www.github.com/googleapis/gapic-generator-python/commit/298db39064e29de764537f25dc38f9e5ac301390))
* Raise GoogleAPICallError on REST response errors ([#891](https://www.github.com/googleapis/gapic-generator-python/issues/891)) ([edb8c63](https://www.github.com/googleapis/gapic-generator-python/commit/edb8c63e8a331f5e08ea19202d8de42de7051299))
* **tests:** Add integration test framework, goldens for 4 APIs [gapic-generator-python] ([#905](https://www.github.com/googleapis/gapic-generator-python/issues/905)) ([48db1e6](https://www.github.com/googleapis/gapic-generator-python/commit/48db1e644badc2180253e11d9a3d3657e8f9aeed))


### Bug Fixes

* fix datetime comparison unit tests ([#898](https://www.github.com/googleapis/gapic-generator-python/issues/898)) ([81932a2](https://www.github.com/googleapis/gapic-generator-python/commit/81932a2b71e6ca5f424ddc5c52933ad1d452583a))
* remove support for google-api-core<1.26.0 ([#893](https://www.github.com/googleapis/gapic-generator-python/issues/893)) ([ce558ac](https://www.github.com/googleapis/gapic-generator-python/commit/ce558acef9ec9c9bcc54243cddb708ef168c05f0))


### Documentation

* Add DEVELOPMENT.md ([#876](https://www.github.com/googleapis/gapic-generator-python/issues/876)) ([592ec06](https://www.github.com/googleapis/gapic-generator-python/commit/592ec061d4eec35e35633c5a9e62cf1e598a8461))

## [0.47.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.46.3...v0.47.0) (2021-05-13)


### Features

* support protobuf method deprecation option [gapic-generator-python] ([#875](https://www.github.com/googleapis/gapic-generator-python/issues/875)) ([5a5a839](https://www.github.com/googleapis/gapic-generator-python/commit/5a5a839b99d78ec5a5c52452e57c289b55ad1db5))

### [0.46.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.46.2...v0.46.3) (2021-05-12)


### Bug Fixes

* consistently use _pb2 identifier ([#883](https://www.github.com/googleapis/gapic-generator-python/issues/883)) ([d789c84](https://www.github.com/googleapis/gapic-generator-python/commit/d789c84d0d686bdb2d88179041b4c04cc32a3e66))

### [0.46.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.46.1...v0.46.2) (2021-05-12)


### Bug Fixes

* fix incorrectly referenced exceptions, add missing port to tests ([#873](https://www.github.com/googleapis/gapic-generator-python/issues/873)) ([40078c4](https://www.github.com/googleapis/gapic-generator-python/commit/40078c46b21a0dfa489d4cd80ed7d95bb542f3c3)), closes [#872](https://www.github.com/googleapis/gapic-generator-python/issues/872)

### [0.46.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.46.0...v0.46.1) (2021-05-07)


### Bug Fixes

* also add the async client to __all__ ([#869](https://www.github.com/googleapis/gapic-generator-python/issues/869)) ([09c90fa](https://www.github.com/googleapis/gapic-generator-python/commit/09c90fa48515cb7da1d0ebf1d93a0d49fc6448e8))

## [0.46.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.45.2...v0.46.0) (2021-05-07)


### Features

* Support field presence for query parameters in REST clients ([#866](https://www.github.com/googleapis/gapic-generator-python/issues/866)) ([5339db1](https://www.github.com/googleapis/gapic-generator-python/commit/5339db1308326d91a05a34d38e31cf91b79a9225))


### Bug Fixes

* Check for default value presence for non-optional fields in REST ([#868](https://www.github.com/googleapis/gapic-generator-python/issues/868)) ([5748001](https://www.github.com/googleapis/gapic-generator-python/commit/57480019c3e77c6b3a85bdaf8441334170b318e8))

### [0.45.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.45.1...v0.45.2) (2021-05-06)


### Bug Fixes

* remove extra space before_pb_options ([#863](https://www.github.com/googleapis/gapic-generator-python/issues/863)) ([f0532e7](https://www.github.com/googleapis/gapic-generator-python/commit/f0532e7a88479aeb805c1509239008bdd19e9d85))

### [0.45.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.45.0...v0.45.1) (2021-05-04)


### Bug Fixes

* add async client to %name_%version/__init__.py ([#859](https://www.github.com/googleapis/gapic-generator-python/issues/859)) ([391fdb8](https://www.github.com/googleapis/gapic-generator-python/commit/391fdb84b13c5628c21d81ad311c689da8971f6a))

## [0.45.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.44.3...v0.45.0) (2021-05-03)


### Features

* add autogenerated snippets ([#845](https://www.github.com/googleapis/gapic-generator-python/issues/845)) ([abdf5ec](https://www.github.com/googleapis/gapic-generator-python/commit/abdf5ec00261e5500dbdd190c23b0b2b05836799))

### [0.44.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.44.2...v0.44.3) (2021-05-03)


### Performance Improvements

* reduce unnecessary copies, optimize Address comparison ([#855](https://www.github.com/googleapis/gapic-generator-python/issues/855)) ([e843540](https://www.github.com/googleapis/gapic-generator-python/commit/e8435400257707458e83424019c9b1a16fac9a99))

### [0.44.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.44.1...v0.44.2) (2021-04-30)


### Bug Fixes

* remove auth, policy, and options from the reserved names list ([#851](https://www.github.com/googleapis/gapic-generator-python/issues/851)) ([d3f31a0](https://www.github.com/googleapis/gapic-generator-python/commit/d3f31a0d33411b3248871ddbe51135e83b699a73))

### [0.44.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.44.0...v0.44.1) (2021-04-28)


### Bug Fixes

* fix syntax errors and failing unit tests ([#849](https://www.github.com/googleapis/gapic-generator-python/issues/849)) ([9046261](https://www.github.com/googleapis/gapic-generator-python/commit/90462617e3e2b90eb8684210b6a70e890bdc0d96)), closes [#848](https://www.github.com/googleapis/gapic-generator-python/issues/848)

## [0.44.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.43.3...v0.44.0) (2021-04-23)


### Features

* support self-signed JWT flow for service accounts ([#774](https://www.github.com/googleapis/gapic-generator-python/issues/774)) ([89d6f35](https://www.github.com/googleapis/gapic-generator-python/commit/89d6f35c54b0a9b81c9b5f580d2e9eb87352ed93))


### Bug Fixes

* enable GAPIC metadata generation ([#843](https://www.github.com/googleapis/gapic-generator-python/issues/843)) ([697816c](https://www.github.com/googleapis/gapic-generator-python/commit/697816ce7d5b201d6ced85fadd89f9140da67b37))

### [0.43.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.43.2...v0.43.3) (2021-04-12)


### Bug Fixes

* sort subpackages in %namespace/%name/__init__.py ([#836](https://www.github.com/googleapis/gapic-generator-python/issues/836)) ([90cf882](https://www.github.com/googleapis/gapic-generator-python/commit/90cf882b20f430499f692e6b9b23497b3555e928))

### [0.43.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.43.1...v0.43.2) (2021-03-24)


### Bug Fixes

* add certain raw imports to RESERVED_NAMES ([#824](https://www.github.com/googleapis/gapic-generator-python/issues/824)) ([04bd8aa](https://www.github.com/googleapis/gapic-generator-python/commit/04bd8aaf0fc2c2c0615105cab39dc33266b66775))
* Update module alias to resolve naming conflict ([#820](https://www.github.com/googleapis/gapic-generator-python/issues/820)) ([f5e9f36](https://www.github.com/googleapis/gapic-generator-python/commit/f5e9f367ec6a72b4272f559a93f6fbb3d7e54b8b)), closes [#819](https://www.github.com/googleapis/gapic-generator-python/issues/819)

### [0.43.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.43.0...v0.43.1) (2021-03-19)


### Bug Fixes

* use correct retry deadline in publisher methods ([#814](https://www.github.com/googleapis/gapic-generator-python/issues/814)) ([92a2cfc](https://www.github.com/googleapis/gapic-generator-python/commit/92a2cfc47b24c4b1a041d5bbb944d69a67a962a2))

## [0.43.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.42.2...v0.43.0) (2021-03-11)


### Features

* add bazel support for gapic metadata ([#811](https://www.github.com/googleapis/gapic-generator-python/issues/811)) ([7ced24a](https://www.github.com/googleapis/gapic-generator-python/commit/7ced24a0b20cb6505587b946c03b1b038eef4b4a))
* update templates to permit enum aliases ([#809](https://www.github.com/googleapis/gapic-generator-python/issues/809)) ([2e7ea11](https://www.github.com/googleapis/gapic-generator-python/commit/2e7ea11f80210459106f9780e5f013e2a0381d29))

### [0.42.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.42.1...v0.42.2) (2021-03-05)


### Bug Fixes

* s/grpcAsync/grpc-async for gapic metadata ([#803](https://www.github.com/googleapis/gapic-generator-python/issues/803)) ([96f7864](https://www.github.com/googleapis/gapic-generator-python/commit/96f78640d90cf50c6b525924d14c6afe31874be6))

### [0.42.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.42.0...v0.42.1) (2021-03-04)


### Bug Fixes

* corner case fix for empty request generated test ([#801](https://www.github.com/googleapis/gapic-generator-python/issues/801)) ([039dc71](https://www.github.com/googleapis/gapic-generator-python/commit/039dc713fed291142058741e1138da5a4bec542f))

## [0.42.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.41.0...v0.42.0) (2021-03-03)


### Features

* add flag for gapic metadata ([#795](https://www.github.com/googleapis/gapic-generator-python/issues/795)) ([9cd7664](https://www.github.com/googleapis/gapic-generator-python/commit/9cd7664141835edcd8970629d9cf3abe4b7fd7c4))

## [0.41.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.12...v0.41.0) (2021-03-02)


### Features

* add gapic metadata file ([#781](https://www.github.com/googleapis/gapic-generator-python/issues/781)) ([5dd8fcc](https://www.github.com/googleapis/gapic-generator-python/commit/5dd8fccf6b4da57edef0347beb07102634daa992))

### [0.40.12](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.11...v0.40.12) (2021-02-26)


### Bug Fixes

* exclude 'input' from reserved names list ([#788](https://www.github.com/googleapis/gapic-generator-python/issues/788)) ([da2ff71](https://www.github.com/googleapis/gapic-generator-python/commit/da2ff717b82357359baeeafad9a3e48a70e194cb))

### [0.40.11](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.10...v0.40.11) (2021-02-24)


### Bug Fixes

* remove duplicate field entries ([#786](https://www.github.com/googleapis/gapic-generator-python/issues/786)) ([9f4dfa4](https://www.github.com/googleapis/gapic-generator-python/commit/9f4dfa46cb6a67081563ce096452fedd9e35051d))

### [0.40.10](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.9...v0.40.10) (2021-02-17)


### Bug Fixes

* ignore unknown fields returned from server for REST ([#777](https://www.github.com/googleapis/gapic-generator-python/issues/777)) ([a70b078](https://www.github.com/googleapis/gapic-generator-python/commit/a70b0787f7e3d40642a4f68574f0cc493cc4e054))

### [0.40.9](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.8...v0.40.9) (2021-02-10)


### Bug Fixes

* fix rest transport tests ([#772](https://www.github.com/googleapis/gapic-generator-python/issues/772)) ([ce110a3](https://www.github.com/googleapis/gapic-generator-python/commit/ce110a35894aa1a838649f9782294b3b8446be5c))

### [0.40.8](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.7...v0.40.8) (2021-02-05)


### Bug Fixes

* body encoding for rest transport ([#768](https://www.github.com/googleapis/gapic-generator-python/issues/768)) ([cc55a18](https://www.github.com/googleapis/gapic-generator-python/commit/cc55a182b878d78f92aba259c067d47ab1d01e5b))
* update paging implementation to handle unconventional pagination ([#750](https://www.github.com/googleapis/gapic-generator-python/issues/750)) ([eaac3e6](https://www.github.com/googleapis/gapic-generator-python/commit/eaac3e69d366b610ae7551d94d4f546819e24bc2))

### [0.40.7](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.6...v0.40.7) (2021-02-03)


### Bug Fixes

* don't use integer for enums in json encoding ([#761](https://www.github.com/googleapis/gapic-generator-python/issues/761)) ([6d37a73](https://www.github.com/googleapis/gapic-generator-python/commit/6d37a7388995b90428ee6293bcce5d48cd9a48f8))

### [0.40.6](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.5...v0.40.6) (2021-02-02)


### Bug Fixes

* remove duplicate assignment of certain flattened, repeated fields ([#760](https://www.github.com/googleapis/gapic-generator-python/issues/760)) ([cdbc221](https://www.github.com/googleapis/gapic-generator-python/commit/cdbc22130a176e733c529f60a6b8b1d224e82e89))

### [0.40.5](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.4...v0.40.5) (2021-02-01)


### Bug Fixes

* Fix namespace packages conflict issue ([#757](https://www.github.com/googleapis/gapic-generator-python/issues/757)) ([8035662](https://www.github.com/googleapis/gapic-generator-python/commit/8035662bdcfbdffd1c294c5d28479733358407ca))

### [0.40.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.3...v0.40.4) (2021-01-28)


### Bug Fixes

* Make gapic-generator-python compatible with protobuf 3.14.0 (packaged as native namespace package) ([#753](https://www.github.com/googleapis/gapic-generator-python/issues/753)) ([45212af](https://www.github.com/googleapis/gapic-generator-python/commit/45212afb9f523a416d86272798d71ce05dc292f0))
* mypy 0.800 update errors ([#754](https://www.github.com/googleapis/gapic-generator-python/issues/754)) ([608275a](https://www.github.com/googleapis/gapic-generator-python/commit/608275aa923f495520dea8ebddb94a99f26e27a5))

### [0.40.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.2...v0.40.3) (2021-01-21)


### Bug Fixes

* stabilize order of query_params ([#742](https://www.github.com/googleapis/gapic-generator-python/issues/742)) ([2835ddb](https://www.github.com/googleapis/gapic-generator-python/commit/2835ddbe62b520e2e4c84f02810b1ac936c9cbb9))

### [0.40.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.1...v0.40.2) (2021-01-21)


### Bug Fixes

* fix rest transport unit test template ([#741](https://www.github.com/googleapis/gapic-generator-python/issues/741)) ([54b9806](https://www.github.com/googleapis/gapic-generator-python/commit/54b98060f881c8f0424c7e146488d3adc19fec7a))

### [0.40.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.40.0...v0.40.1) (2021-01-20)


### Bug Fixes

* raise for rest transport http error ([#738](https://www.github.com/googleapis/gapic-generator-python/issues/738)) ([7d24f3d](https://www.github.com/googleapis/gapic-generator-python/commit/7d24f3d81499ad714e57c7c9562b842c09e49d20))

## [0.40.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.39.1...v0.40.0) (2021-01-19)


### Features

* add mtls feature to rest transport ([#731](https://www.github.com/googleapis/gapic-generator-python/issues/731)) ([524dbab](https://www.github.com/googleapis/gapic-generator-python/commit/524dbab16d248198ca10a08ecede4600fd36cefc))

### [0.39.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.39.0...v0.39.1) (2021-01-05)


### Bug Fixes

* fix missing .coveragerc and the broken bazel build ([#723](https://www.github.com/googleapis/gapic-generator-python/issues/723)) ([7f8235f](https://www.github.com/googleapis/gapic-generator-python/commit/7f8235f6dfbd309a879895701aeb5e73c6425483))
* Update gapic-generator-python to gracefully handle internal google inconsistencies ([#721](https://www.github.com/googleapis/gapic-generator-python/issues/721)) ([b984295](https://www.github.com/googleapis/gapic-generator-python/commit/b9842952433924a1d8de4ef9cc3ea9e7fa91c01a))
* updating testing, rest-only generation, & minor bug-fixes ([#716](https://www.github.com/googleapis/gapic-generator-python/issues/716)) ([56c31de](https://www.github.com/googleapis/gapic-generator-python/commit/56c31de4a9f661e3d69b52e19c9a28dddfe9d7dc))

## [0.39.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.38.0...v0.39.0) (2020-12-22)


### Features

* allow warehouse name to be customized ([#717](https://www.github.com/googleapis/gapic-generator-python/issues/717)) ([7c185e8](https://www.github.com/googleapis/gapic-generator-python/commit/7c185e87cb4252b1f99ed121515814595f9492c4)), closes [#605](https://www.github.com/googleapis/gapic-generator-python/issues/605)


### Bug Fixes

* fix sphinx identifiers ([#714](https://www.github.com/googleapis/gapic-generator-python/issues/714)) ([39be474](https://www.github.com/googleapis/gapic-generator-python/commit/39be474b4419dfa521ef51927fd36dbf257d68e3)), closes [#625](https://www.github.com/googleapis/gapic-generator-python/issues/625) [#604](https://www.github.com/googleapis/gapic-generator-python/issues/604)

## [0.38.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.37.1...v0.38.0) (2020-12-16)


### Features

* add 'from_service_account_info' factory to clients ([#706](https://www.github.com/googleapis/gapic-generator-python/issues/706)) ([94d5f0c](https://www.github.com/googleapis/gapic-generator-python/commit/94d5f0c11b8041cbae8e4a89bb504d6c6e200a95)), closes [#705](https://www.github.com/googleapis/gapic-generator-python/issues/705)

### [0.37.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.37.0...v0.37.1) (2020-12-10)


### Bug Fixes

* remove client recv msg limit ([#704](https://www.github.com/googleapis/gapic-generator-python/issues/704)) ([80147ce](https://www.github.com/googleapis/gapic-generator-python/commit/80147ce177ce435dcb1b611181e80dc35f915293))

## [0.37.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.36.0...v0.37.0) (2020-12-08)


### Features

* add proper handling of query/path/body parameters for rest transport ([#702](https://www.github.com/googleapis/gapic-generator-python/issues/702)) ([6b2de5d](https://www.github.com/googleapis/gapic-generator-python/commit/6b2de5dd9fbf15e6b0a42b428b01eb03f1a3820a))

## [0.36.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.11...v0.36.0) (2020-11-14)


### Features

* add rest transport generation for clients with optional transport flag ([#688](https://www.github.com/googleapis/gapic-generator-python/issues/688)) ([af59c2c](https://www.github.com/googleapis/gapic-generator-python/commit/af59c2c3c3d6b7e1f626c3fbc2c03f99ca31b4a4))

### [0.35.11](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.10...v0.35.11) (2020-11-12)


### Bug Fixes

* add enums to types/__init__.py ([#695](https://www.github.com/googleapis/gapic-generator-python/issues/695)) ([e1d4a4a](https://www.github.com/googleapis/gapic-generator-python/commit/e1d4a4ae768a631f6e6dc28f2acfde8be8dc4a8f))
* update protobuf version [gapic-generator-python] ([#696](https://www.github.com/googleapis/gapic-generator-python/issues/696)) ([ea3e519](https://www.github.com/googleapis/gapic-generator-python/commit/ea3e5198862881f5b142638df6ea604654f81f82))

### [0.35.10](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.9...v0.35.10) (2020-11-09)


### Documentation

* fix a few typos ([#690](https://www.github.com/googleapis/gapic-generator-python/issues/690)) ([2716838](https://www.github.com/googleapis/gapic-generator-python/commit/2716838fb739c9350eee2c95b5cf207c4d83423d))

### [0.35.9](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.8...v0.35.9) (2020-10-27)


### Performance Improvements

* collisions don't contain reserved names by default ([#684](https://www.github.com/googleapis/gapic-generator-python/issues/684)) ([2ec6ea6](https://www.github.com/googleapis/gapic-generator-python/commit/2ec6ea6835256c0d7b252e035cf4eac1ff442647))

### [0.35.8](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.7...v0.35.8) (2020-10-21)


### Documentation

* generated message types reference proto-plus ([#680](https://www.github.com/googleapis/gapic-generator-python/issues/680)) ([23327b2](https://www.github.com/googleapis/gapic-generator-python/commit/23327b275fb5a3fefe6c47cb15b9d9ecb02aac1f))

### [0.35.7](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.6...v0.35.7) (2020-10-21)


### Bug Fixes

* expose ssl credentials from transport ([#677](https://www.github.com/googleapis/gapic-generator-python/issues/677)) ([da0ee3e](https://www.github.com/googleapis/gapic-generator-python/commit/da0ee3eab4f80bf3d70fa5e06a2dcef7e1d4d22e))

### [0.35.6](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.5...v0.35.6) (2020-10-20)


### Bug Fixes

* unknown resources do not cause a generator crash ([#675](https://www.github.com/googleapis/gapic-generator-python/issues/675)) ([2d23d7d](https://www.github.com/googleapis/gapic-generator-python/commit/2d23d7d202099ccf145c01aeb9a03ae46b4e1b00))

### [0.35.5](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.4...v0.35.5) (2020-10-19)


### Bug Fixes

* numerous small fixes to allow bigtable-admin ([#660](https://www.github.com/googleapis/gapic-generator-python/issues/660)) ([09692c4](https://www.github.com/googleapis/gapic-generator-python/commit/09692c4e889ccde3b0ca31a5e8476c1679804beb))

### [0.35.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.3...v0.35.4) (2020-10-16)


### Bug Fixes

* minor typo in ads template ([#664](https://www.github.com/googleapis/gapic-generator-python/issues/664)) ([816f965](https://www.github.com/googleapis/gapic-generator-python/commit/816f965c8560bf65d8043bd67672c660a2b1300b))

### [0.35.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.2...v0.35.3) (2020-10-13)


### Documentation

* remove references to pipsi ([#656](https://www.github.com/googleapis/gapic-generator-python/issues/656)) ([39c612b](https://www.github.com/googleapis/gapic-generator-python/commit/39c612b545bc93c7c738a78f074672ee66365efb))

### [0.35.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.1...v0.35.2) (2020-10-13)


### Bug Fixes

* modules referenced in MapField message type are properly aliased ([#654](https://www.github.com/googleapis/gapic-generator-python/issues/654)) ([2c79349](https://www.github.com/googleapis/gapic-generator-python/commit/2c79349e7b89435bc45e499885f7b12ac0bc2d9f)), closes [#618](https://www.github.com/googleapis/gapic-generator-python/issues/618)

### [0.35.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.35.0...v0.35.1) (2020-10-09)


### Bug Fixes

* the common resources are not targets for lookup ([#650](https://www.github.com/googleapis/gapic-generator-python/issues/650)) ([8e1b384](https://www.github.com/googleapis/gapic-generator-python/commit/8e1b384e812ef519c421c8c288d5118961d8b4cf))

## [0.35.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.34.4...v0.35.0) (2020-10-09)


### Features

* file_level and indirectly used resources generate helper methods ([#642](https://www.github.com/googleapis/gapic-generator-python/issues/642)) ([42e224c](https://www.github.com/googleapis/gapic-generator-python/commit/42e224cb100f6e2aa9370bc6a5179d62979b5c4d)), closes [#637](https://www.github.com/googleapis/gapic-generator-python/issues/637)

### [0.34.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.34.3...v0.34.4) (2020-10-09)


### Bug Fixes

* expose transport property for clients ([#645](https://www.github.com/googleapis/gapic-generator-python/issues/645)) ([13cddda](https://www.github.com/googleapis/gapic-generator-python/commit/13cddda0623bd4d24ae7973752b1be0eaa40523a)), closes [#640](https://www.github.com/googleapis/gapic-generator-python/issues/640)

### [0.34.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.34.2...v0.34.3) (2020-10-08)


### Bug Fixes

* fix types on server and bidi streaming callables ([#641](https://www.github.com/googleapis/gapic-generator-python/issues/641)) ([d92c202](https://www.github.com/googleapis/gapic-generator-python/commit/d92c2029398c969ebf2a68a5bf77c5eb4fff7b31))

### [0.34.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.34.1...v0.34.2) (2020-09-30)


### Bug Fixes

* resource messages in method response types generate helpers ([#629](https://www.github.com/googleapis/gapic-generator-python/issues/629)) ([52bfd6d](https://www.github.com/googleapis/gapic-generator-python/commit/52bfd6d5d5821b33e78e6b9867a3be2865cdbc74))

### [0.34.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.34.0...v0.34.1) (2020-09-30)


### Bug Fixes

* fix typo attribue -> attribute ([#627](https://www.github.com/googleapis/gapic-generator-python/issues/627)) ([729146f](https://www.github.com/googleapis/gapic-generator-python/commit/729146fd53edf1e4ae4d3c9a90640a7520b1ba9d)), closes [#626](https://www.github.com/googleapis/gapic-generator-python/issues/626)

## [0.34.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.8...v0.34.0) (2020-09-29)


### Features

* add support for common resource paths ([#622](https://www.github.com/googleapis/gapic-generator-python/issues/622)) ([15a7fde](https://www.github.com/googleapis/gapic-generator-python/commit/15a7fdeb966cb64a742b6305d2c71dd3d485d0f9))

### [0.33.8](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.7...v0.33.8) (2020-09-25)


### Bug Fixes

* handle repeated fields in method signatures ([#445](https://www.github.com/googleapis/gapic-generator-python/issues/445)) ([3aae799](https://www.github.com/googleapis/gapic-generator-python/commit/3aae799f62a1f5d3b0506d919cc6080ee417f14b))

### [0.33.7](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.6...v0.33.7) (2020-09-24)


### Bug Fixes

* retriable exceptions are deterministically ordered in GAPICs ([#619](https://www.github.com/googleapis/gapic-generator-python/issues/619)) ([f7b1164](https://www.github.com/googleapis/gapic-generator-python/commit/f7b11640b74d8c64747b33783976d6e0ab9c61c4))

### [0.33.6](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.5...v0.33.6) (2020-09-22)


### Bug Fixes

* operation module is properly aliased if necessary ([#615](https://www.github.com/googleapis/gapic-generator-python/issues/615)) ([8f92fd9](https://www.github.com/googleapis/gapic-generator-python/commit/8f92fd9999286ef3f916119be78dbeb838a15550)), closes [#610](https://www.github.com/googleapis/gapic-generator-python/issues/610)

### [0.33.5](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.4...v0.33.5) (2020-09-22)


### Bug Fixes

* remove 'property' from reserved names ([#613](https://www.github.com/googleapis/gapic-generator-python/issues/613)) ([8338a51](https://www.github.com/googleapis/gapic-generator-python/commit/8338a51a81f5f5b8ebacf68c8e46d3e1804d3f8b))

### [0.33.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.3...v0.33.4) (2020-09-17)


### Bug Fixes

* 'id' should not be a reserved name ([#602](https://www.github.com/googleapis/gapic-generator-python/issues/602)) ([c43c574](https://www.github.com/googleapis/gapic-generator-python/commit/c43c5740db099be19c5f6e52b3a917a631003411))

### [0.33.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.2...v0.33.3) (2020-09-15)


### Bug Fixes

* module names can no longer collide with keywords or builtins ([#595](https://www.github.com/googleapis/gapic-generator-python/issues/595)) ([960d550](https://www.github.com/googleapis/gapic-generator-python/commit/960d550c4a8fd09b052cce785d76243a5d4525d7))

### [0.33.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.1...v0.33.2) (2020-09-15)


### Bug Fixes

* ignore types for imports generated from 'google.api_core' ([#597](https://www.github.com/googleapis/gapic-generator-python/issues/597)) ([8440e09](https://www.github.com/googleapis/gapic-generator-python/commit/8440e09855d399d647b62238a9697e04ea4d0d41)), closes [#596](https://www.github.com/googleapis/gapic-generator-python/issues/596)

### [0.33.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.33.0...v0.33.1) (2020-09-15)


### Bug Fixes

* Fix client template type hints ([#593](https://www.github.com/googleapis/gapic-generator-python/issues/593)) ([93f34e8](https://www.github.com/googleapis/gapic-generator-python/commit/93f34e8a2a351a24a49424c1722baec2893dc764))

## [0.33.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.32.4...v0.33.0) (2020-09-10)


### Features

* support mtls env variables ([#589](https://www.github.com/googleapis/gapic-generator-python/issues/589)) ([b19026d](https://www.github.com/googleapis/gapic-generator-python/commit/b19026d9cca26ebd1cd0c3e73f738c4d1870d987))

### [0.32.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.32.3...v0.32.4) (2020-09-03)


### Bug Fixes

* rendering mock values for recursive messages no longer crashes ([#587](https://www.github.com/googleapis/gapic-generator-python/issues/587)) ([c2a83e5](https://www.github.com/googleapis/gapic-generator-python/commit/c2a83e561bf46b4af21e9008c7d67a1c609d7d06))

### [0.32.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.32.2...v0.32.3) (2020-08-28)


### Bug Fixes

* stabilize the order of resource helper methods and ([#582](https://www.github.com/googleapis/gapic-generator-python/issues/582)) ([7d2adde](https://www.github.com/googleapis/gapic-generator-python/commit/7d2adde3a1ae81ac88ced822d6dfdfb26ffbfdf0))

### [0.32.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.32.1...v0.32.2) (2020-08-20)


### Bug Fixes

* add 'type: ignore' comment for 'google.auth' ([#579](https://www.github.com/googleapis/gapic-generator-python/issues/579)) ([af17501](https://www.github.com/googleapis/gapic-generator-python/commit/af17501d258c7c37fc1081fcad5fe18f7629f4c3))

### [0.32.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.32.0...v0.32.1) (2020-08-19)


### Bug Fixes

* rename local var page in generated tests ([#577](https://www.github.com/googleapis/gapic-generator-python/issues/577)) ([075f9e8](https://www.github.com/googleapis/gapic-generator-python/commit/075f9e8d50b02ffb5f2f042b84f27a9f634636e2))

## [0.32.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.31.1...v0.32.0) (2020-08-17)


### Features

* allow user-provided client info ([#573](https://www.github.com/googleapis/gapic-generator-python/issues/573)) ([b2e5274](https://www.github.com/googleapis/gapic-generator-python/commit/b2e52746c7ce4b983482fb776224b30767978c79)), closes [googleapis/python-kms#37](https://www.github.com/googleapis/python-kms/issues/37) [#566](https://www.github.com/googleapis/gapic-generator-python/issues/566)

### [0.31.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.31.0...v0.31.1) (2020-08-17)


### Bug Fixes

* install gcc by hand ([#571](https://www.github.com/googleapis/gapic-generator-python/issues/571)) ([e224a03](https://www.github.com/googleapis/gapic-generator-python/commit/e224a0365a2d3ed20d69cf4d1298a3f022f8da76))

## [0.31.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.30.0...v0.31.0) (2020-07-28)


### Features

* bypass request copying in method calls ([#557](https://www.github.com/googleapis/gapic-generator-python/issues/557)) ([3a23143](https://www.github.com/googleapis/gapic-generator-python/commit/3a2314318de229a3353c984a8cb2766ae95cc968))


### Bug Fixes

* add google.api_core.retry import to base.py ([#555](https://www.github.com/googleapis/gapic-generator-python/issues/555)) ([1d08e60](https://www.github.com/googleapis/gapic-generator-python/commit/1d08e60cea4c5b3fa2555a4952161b0115d686f2))

## [0.30.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.29.2...v0.30.0) (2020-07-27)


### Features

* precache wrapped rpcs ([#553](https://www.github.com/googleapis/gapic-generator-python/issues/553)) ([2f2fb5d](https://www.github.com/googleapis/gapic-generator-python/commit/2f2fb5d3d9472a79c80be6d052129d07d2bbb835))

### [0.29.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.29.1...v0.29.2) (2020-07-23)


### Bug Fixes

* rename __init__.py to __init__.py.j2 ([#550](https://www.github.com/googleapis/gapic-generator-python/issues/550)) ([71a7062](https://www.github.com/googleapis/gapic-generator-python/commit/71a7062b918136b916cc5bfc7dbdf64f870edf6a)), closes [#437](https://www.github.com/googleapis/gapic-generator-python/issues/437)

### [0.29.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.29.0...v0.29.1) (2020-07-23)


### Bug Fixes

* use context manager for mtls env var ([#548](https://www.github.com/googleapis/gapic-generator-python/issues/548)) ([d19e180](https://www.github.com/googleapis/gapic-generator-python/commit/d19e1808df9cd2884ae7a449977a479b4829bc1d))

## [0.29.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.28.1...v0.29.0) (2020-07-22)


### Features

* add iam methods to templates ([#545](https://www.github.com/googleapis/gapic-generator-python/issues/545)) ([3f42c3c](https://www.github.com/googleapis/gapic-generator-python/commit/3f42c3cf8aae432a9bda0953fbabd7f0c8d774de))
* support quota project override via client options ([#496](https://www.github.com/googleapis/gapic-generator-python/issues/496)) ([bbc6b36](https://www.github.com/googleapis/gapic-generator-python/commit/bbc6b367f50526312e8320f0fc668ef88f230dbd))


### Bug Fixes

* make # after alpha/beta optional ([#540](https://www.github.com/googleapis/gapic-generator-python/issues/540)) ([f86a47b](https://www.github.com/googleapis/gapic-generator-python/commit/f86a47b6431e374ae1797061511b49fe6bf22daf))

### [0.28.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.28.0...v0.28.1) (2020-07-16)


### Bug Fixes

* remove typo from py_gapic.bzl ([#532](https://www.github.com/googleapis/gapic-generator-python/issues/532)) ([2975c2d](https://www.github.com/googleapis/gapic-generator-python/commit/2975c2d76e08b5ee5324730707707d9dd6ced8ae))

## [0.28.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.27.0...v0.28.0) (2020-07-16)


### Features

* add retry config passed to bazel rule ([#526](https://www.github.com/googleapis/gapic-generator-python/issues/526)) ([9e96151](https://www.github.com/googleapis/gapic-generator-python/commit/9e96151d702786912fcf033f7535efad8ae754ee))


### Bug Fixes

* paged code and templates are no longer message centric ([#527](https://www.github.com/googleapis/gapic-generator-python/issues/527)) ([00ba77c](https://www.github.com/googleapis/gapic-generator-python/commit/00ba77c3d27ef9a0b8742db3660983b80a68c672))

## [0.27.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.6...v0.27.0) (2020-07-13)


### Features

* support for proto3 optional fields ([#519](https://www.github.com/googleapis/gapic-generator-python/issues/519)) ([1aa729c](https://www.github.com/googleapis/gapic-generator-python/commit/1aa729cc8d2f7f0de25c8348fdbf9d6dd96f5847))

### [0.26.6](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.5...v0.26.6) (2020-07-10)


### Bug Fixes

* primitive repeated fields are now correctly auto paginated ([#517](https://www.github.com/googleapis/gapic-generator-python/issues/517)) ([61a2cc0](https://www.github.com/googleapis/gapic-generator-python/commit/61a2cc0d4c08064d442fd4d7aa4b1b9e56158eaa))

### [0.26.5](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.4...v0.26.5) (2020-07-10)


### Bug Fixes

* convert datetime back to proto for unit tests ([#511](https://www.github.com/googleapis/gapic-generator-python/issues/511)) ([e1c787d](https://www.github.com/googleapis/gapic-generator-python/commit/e1c787d3b6fe09dc0b4e00f07a7bd77fb5f1e6a3))

### [0.26.4](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.3...v0.26.4) (2020-07-10)


### Bug Fixes

* require min google-api-core version of 1.21.0 ([#506](https://www.github.com/googleapis/gapic-generator-python/issues/506)) ([bf787bd](https://www.github.com/googleapis/gapic-generator-python/commit/bf787bd36198288d6a40e45e44e43f0098cfec7c)), closes [#461](https://www.github.com/googleapis/gapic-generator-python/issues/461)
* tweak oneof detection ([#505](https://www.github.com/googleapis/gapic-generator-python/issues/505)) ([1632e25](https://www.github.com/googleapis/gapic-generator-python/commit/1632e250cfc01a17ccad128c3e065008b334473a))

### [0.26.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.2...v0.26.3) (2020-07-08)


### Bug Fixes

* fix wrong unit test ([#502](https://www.github.com/googleapis/gapic-generator-python/issues/502)) ([c95bd45](https://www.github.com/googleapis/gapic-generator-python/commit/c95bd45506df7973758b9e1249586597d8214985))

### [0.26.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.1...v0.26.2) (2020-07-07)


### Bug Fixes

* add oneof fields to generated protoplus init ([#485](https://www.github.com/googleapis/gapic-generator-python/issues/485)) ([be5a847](https://www.github.com/googleapis/gapic-generator-python/commit/be5a847aeff6687679f7bca46308362d588f5c77)), closes [#484](https://www.github.com/googleapis/gapic-generator-python/issues/484)

### [0.26.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.0...v0.26.1) (2020-07-07)


### Bug Fixes

* pass metadata to pagers ([#470](https://www.github.com/googleapis/gapic-generator-python/issues/470)) ([c43c6d9](https://www.github.com/googleapis/gapic-generator-python/commit/c43c6d943fa99f202014bf4bba795df25d314a63)), closes [#469](https://www.github.com/googleapis/gapic-generator-python/issues/469)

## [0.26.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.25.2...v0.26.0) (2020-06-30)


### Features

* add `credentials_file` and `scopes` via `client_options` ([#461](https://www.github.com/googleapis/gapic-generator-python/issues/461)) ([b5e1b1e](https://www.github.com/googleapis/gapic-generator-python/commit/b5e1b1e8991159dc176da889e9bdf12e3eebdb1e))


### Bug Fixes

* add name and version info to fixup script name ([#490](https://www.github.com/googleapis/gapic-generator-python/issues/490)) ([16fe7e7](https://www.github.com/googleapis/gapic-generator-python/commit/16fe7e7885b7e17bf16b4f1f8f8844b9f5d0bdfe))
* Temporarily define a fixed testing event loop ([#493](https://www.github.com/googleapis/gapic-generator-python/issues/493)) ([2d22d91](https://www.github.com/googleapis/gapic-generator-python/commit/2d22d919bc8c08e03f501ff2f23152b761467c80))

### [0.25.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.25.1...v0.25.2) (2020-06-23)


### Bug Fixes

* always use dataclasses 0.6 ([#481](https://www.github.com/googleapis/gapic-generator-python/issues/481)) ([066d04e](https://www.github.com/googleapis/gapic-generator-python/commit/066d04e7d53301024106f244280502f16af46b79))

### [0.25.1](https://www.github.com/googleapis/gapic-generator-python/compare/0.25.0...v0.25.1) (2020-06-23)


### Bug Fixes

* only require dataclases if python<3.7 ([#475](https://www.github.com/googleapis/gapic-generator-python/issues/475)) ([9597695](https://www.github.com/googleapis/gapic-generator-python/commit/959769518ea47df383b23b6e48c5da148f69029e))

## [0.25.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.24.2...v0.25.0) (2020-06-17)


### Features

* provide AsyncIO support for generated code ([#365](https://www.github.com/googleapis/gapic-generator-python/issues/365)) ([305ed34](https://www.github.com/googleapis/gapic-generator-python/commit/305ed34cfc1607c990f2f88b27f53358da25c366))

### [0.24.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.24.1...v0.24.2) (2020-06-13)


### Bug Fixes

* generated unit tests live in the 'tests/gapic' subdir ([#456](https://www.github.com/googleapis/gapic-generator-python/issues/456)) ([1ed7c9d](https://www.github.com/googleapis/gapic-generator-python/commit/1ed7c9d6fe9595c390387d72113d741ebf28538d)), closes [#454](https://www.github.com/googleapis/gapic-generator-python/issues/454)

### [0.24.1](https://www.github.com/googleapis/gapic-generator-python/compare/0.24.0...v0.24.1) (2020-06-12)


### Bug Fixes

* update GOOGLE_API_USE_MTLS value ([#453](https://www.github.com/googleapis/gapic-generator-python/issues/453)) ([7449ad5](https://www.github.com/googleapis/gapic-generator-python/commit/7449ad5aad4a1fbbf9ca3796e097512fc80991e3))
