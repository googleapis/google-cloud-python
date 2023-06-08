# Changelog

## [0.8.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.7.0-alpha...v0.8.0-alpha) (2023-06-07)


### Features

* Add convert_document_to_annotate_file_json ([#124](https://github.com/googleapis/python-documentai-toolbox/issues/124)) ([a6b75fc](https://github.com/googleapis/python-documentai-toolbox/commit/a6b75fc11f07a71e436c65b8b2d6f357f18fc6a5))

## [0.7.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.6.0-alpha...v0.7.0-alpha) (2023-05-31)


### Features

* Added text_annotation to vision conversion ([#114](https://github.com/googleapis/python-documentai-toolbox/issues/114)) ([27196bb](https://github.com/googleapis/python-documentai-toolbox/commit/27196bbb6e8e90ef6ebcc5f97690b9751d70fd9b))

## [0.6.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.5.0-alpha...v0.6.0-alpha) (2023-04-17)


### Features

* Add blocks to PageWrapper ([#107](https://github.com/googleapis/python-documentai-toolbox/issues/107)) ([df7dfe7](https://github.com/googleapis/python-documentai-toolbox/commit/df7dfe7b79d39010d5addb3fa861a9c803caae45))
* Added `form_fields_to_bigquery()` method ([#104](https://github.com/googleapis/python-documentai-toolbox/issues/104)) ([96abe22](https://github.com/googleapis/python-documentai-toolbox/commit/96abe220c9909bcc5642ea146c06fd082a2f8009))

## [0.5.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.4.1-alpha...v0.5.0-alpha) (2023-04-07)


### Features

* Add Import Document from Batch Process Metadata & Operation ([#88](https://github.com/googleapis/python-documentai-toolbox/issues/88)) ([f95bbea](https://github.com/googleapis/python-documentai-toolbox/commit/f95bbeab818f37a9885f6025af04ad102e3e2b25))
* Added Export Images functionality ([#96](https://github.com/googleapis/python-documentai-toolbox/issues/96)) ([383e105](https://github.com/googleapis/python-documentai-toolbox/commit/383e1056669a07995825b4756a4100bb305bb98b))
* Update Max Files per Batch Request to 1000 ([#91](https://github.com/googleapis/python-documentai-toolbox/issues/91)) ([3bbc0f0](https://github.com/googleapis/python-documentai-toolbox/commit/3bbc0f08506be65392a19d9caec3450d68311989))

## [0.4.1-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.4.0-alpha...v0.4.1-alpha) (2023-03-21)


### Miscellaneous Chores

* Release 0.4.1-alpha ([#85](https://github.com/googleapis/python-documentai-toolbox/issues/85)) ([bc8d6c7](https://github.com/googleapis/python-documentai-toolbox/commit/bc8d6c75fdee7e3efd8138916a731a881cec8811))

## [0.4.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.3.0-alpha...v0.4.0-alpha) (2023-03-09)


### Features

* Add config based annotation converter ([#72](https://github.com/googleapis/python-documentai-toolbox/issues/72)) ([735514e](https://github.com/googleapis/python-documentai-toolbox/commit/735514e9120698487c47a7ec1107fb6f48c26ce1))
* Added Batch creation for Cloud Storage documents. ([#66](https://github.com/googleapis/python-documentai-toolbox/issues/66)) ([c32a371](https://github.com/googleapis/python-documentai-toolbox/commit/c32a371696047389b5baafe317d4c51449c6d7e9))
* Added list_gcs_document_tree ([#75](https://github.com/googleapis/python-documentai-toolbox/issues/75)) ([d18d1dc](https://github.com/googleapis/python-documentai-toolbox/commit/d18d1dc9a4c6cbd36b7a918ab26a9e229230747f))


### Bug Fixes

* Handle Edge Case where GCS Shards are out of order ([#69](https://github.com/googleapis/python-documentai-toolbox/issues/69)) ([709fe86](https://github.com/googleapis/python-documentai-toolbox/commit/709fe86dc883ee3dd2c250e1da936c9e5b77b1b9))

## [0.3.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.2.1-alpha...v0.3.0-alpha) (2023-02-27)


### Features

* Added docproto to AnnotateFile convertor ([#63](https://github.com/googleapis/python-documentai-toolbox/issues/63)) ([f6dd89a](https://github.com/googleapis/python-documentai-toolbox/commit/f6dd89ae2d12a990439358d0aa8f94566fba28bb))

## [0.2.1-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.2.0-alpha...v0.2.1-alpha) (2023-02-15)


### Documentation

* Update to README ([#58](https://github.com/googleapis/python-documentai-toolbox/issues/58)) ([4e691fa](https://github.com/googleapis/python-documentai-toolbox/commit/4e691fa8f46a24dbb2bf451f8e0d305c5c9ef607))

## [0.2.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.1.1-alpha...v0.2.0-alpha) (2023-02-15)


### Features

* Add `entities_to_dict()` and `entities_to_bigquery()` to `Document` wrapper ([#50](https://github.com/googleapis/python-documentai-toolbox/issues/50)) ([494fa86](https://github.com/googleapis/python-documentai-toolbox/commit/494fa864998b340e052f693ee963a4370128ae80))
* Add PDF Splitter ([#51](https://github.com/googleapis/python-documentai-toolbox/issues/51)) ([8359911](https://github.com/googleapis/python-documentai-toolbox/commit/8359911b55f4545421fa6ddc6f069eaf0311391d))
* Added Support for Form Fields ([#48](https://github.com/googleapis/python-documentai-toolbox/issues/48)) ([6d74548](https://github.com/googleapis/python-documentai-toolbox/commit/6d74548b471a0401b6fde66283aead507c046dd1))

## [0.1.1-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.1.0-alpha...v0.1.1-alpha) (2023-02-08)


### Bug Fixes

* Updated Pip install name in README ([#52](https://github.com/googleapis/python-documentai-toolbox/issues/52)) ([dad8c8b](https://github.com/googleapis/python-documentai-toolbox/commit/dad8c8bfb6241eaa1e24f0b239d39d1396c735c8))


### Documentation

* **samples:** Added quickstart sample ([#27](https://github.com/googleapis/python-documentai-toolbox/issues/27)) ([23a0791](https://github.com/googleapis/python-documentai-toolbox/commit/23a0791633b0c2c2fb65f3706ecb279d058239ad))

## [0.1.0-alpha](https://github.com/googleapis/python-documentai-toolbox/compare/v0.1.0-alpha...v0.1.0-alpha) (2023-01-31)


### Features

* Initial Release ([e360dce](https://github.com/googleapis/python-documentai-toolbox/commit/e360dcecca7da3191e249c4ed9cb871cd1659753))


### Miscellaneous Chores

* Set initial version to 0.1.0-alpha ([b01c38b](https://github.com/googleapis/python-documentai-toolbox/commit/b01c38b4b141cf15c7a3cee3e613a7799849ed6a))


### Documentation

* Fix docs arrangement ([#35](https://github.com/googleapis/python-documentai-toolbox/issues/35)) ([51dd7ff](https://github.com/googleapis/python-documentai-toolbox/commit/51dd7ff400f9d40b968efe7b32debd63c7c9b94c))

## 0.1.0-alpha (2022-11-24)


### Features

* Added client_info to storage client ([#10](https://github.com/googleapis/python-documentai-toolbox/issues/10)) ([b01c38b](https://github.com/googleapis/python-documentai-toolbox/commit/b01c38b4b141cf15c7a3cee3e613a7799849ed6a))
* Added get_document and list_document functions ([#7](https://github.com/googleapis/python-documentai-toolbox/issues/7)) ([b5ac4ca](https://github.com/googleapis/python-documentai-toolbox/commit/b5ac4caff9478f0b6dcb40c7cbe39747494aee2b))
* Added helper functions to DocumentWrapper ([#12](https://github.com/googleapis/python-documentai-toolbox/issues/12)) ([d103c08](https://github.com/googleapis/python-documentai-toolbox/commit/d103c0840b1cb42e7a46743ac2a02f4159b7ac16))
* Initial Release ([e360dce](https://github.com/googleapis/python-documentai-toolbox/commit/e360dcecca7da3191e249c4ed9cb871cd1659753))
* Refactor code ([#17](https://github.com/googleapis/python-documentai-toolbox/issues/17)) ([6c20e08](https://github.com/googleapis/python-documentai-toolbox/commit/6c20e0820a1f831657e951f20f53d56935082873))
* Wrapped tables ([#9](https://github.com/googleapis/python-documentai-toolbox/issues/9)) ([9e4e367](https://github.com/googleapis/python-documentai-toolbox/commit/9e4e367325d5b3ddfddfdf91c646af4b4eb91f16))
