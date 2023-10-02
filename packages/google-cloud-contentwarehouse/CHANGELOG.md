# Changelog

## [0.7.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.7.1...google-cloud-contentwarehouse-v0.7.2) (2023-09-30)


### Features

* add matched_token_page_indices field in Document Warehouse API v1 ([030a767](https://github.com/googleapis/google-cloud-python/commit/030a76756e2ea4af464196dcae81759728231faa))

## [0.7.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.7.0...google-cloud-contentwarehouse-v0.7.1) (2023-09-19)


### Features

* add `cloud_function`fields to support new ingestion option in Document Warehouse API v1 ([61a2c29](https://github.com/googleapis/google-cloud-python/commit/61a2c2902dedd1668534310220e0e53a36718d2d))
* add `ROOT_FOLDER` field to Document Warehouse API v1 ([61a2c29](https://github.com/googleapis/google-cloud-python/commit/61a2c2902dedd1668534310220e0e53a36718d2d))


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## [0.7.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.6.0...google-cloud-contentwarehouse-v0.7.0) (2023-08-16)


### Features

* add Pipeline Service to Document Warehouse API v1 ([#11583](https://github.com/googleapis/google-cloud-python/issues/11583)) ([974cf2e](https://github.com/googleapis/google-cloud-python/commit/974cf2ec443fb1290b86e8978e8ad88dc5700278))

## [0.6.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.5.1...google-cloud-contentwarehouse-v0.6.0) (2023-08-11)


### Features

* Add `disposition_time`, `legal_hold`, `document_is_retention_folder`, `document_is_legal_hold_folder`, `question_answer`, `document_name_filter` fields ([d0432c7](https://github.com/googleapis/google-cloud-python/commit/d0432c7b7754f816c8d3d95f1ea6f9349b930717))
* Add `ON_CREATE_LINK`, `ON_DELETE_LINK` fields to support new rule engine triggers ([d0432c7](https://github.com/googleapis/google-cloud-python/commit/d0432c7b7754f816c8d3d95f1ea6f9349b930717))


### Documentation

* Deprecate DB_CLOUD_SQL_POSTGRES ([d0432c7](https://github.com/googleapis/google-cloud-python/commit/d0432c7b7754f816c8d3d95f1ea6f9349b930717))

## [0.5.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.5.0...google-cloud-contentwarehouse-v0.5.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## [0.5.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.4.1...google-cloud-contentwarehouse-v0.5.0) (2023-04-05)


### Features

* add `content_category`, `text_extraction_enabled`, `retrieval_importance`, `schema_sources`, `total_result_size` fields ([80a9ff4](https://github.com/googleapis/google-cloud-python/commit/80a9ff4a68b3c40696e95d2b1faecea7c8397a5b))
* add `DocumentCreatorDefaultRole`,  `ContentCategory`, `RetrievalImportance`, `SchemaSource`, `TotalResultSize`, `LockDocumentRequest`, `CustomWeightsMetadata`, `WeightedSchemaProperty` ([80a9ff4](https://github.com/googleapis/google-cloud-python/commit/80a9ff4a68b3c40696e95d2b1faecea7c8397a5b))
* add LockDocument service ([80a9ff4](https://github.com/googleapis/google-cloud-python/commit/80a9ff4a68b3c40696e95d2b1faecea7c8397a5b))
* deprecate `text_extraction_disabled`, `structured_content_uri`, `async_enabled` field ([80a9ff4](https://github.com/googleapis/google-cloud-python/commit/80a9ff4a68b3c40696e95d2b1faecea7c8397a5b))

## [0.4.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.4.0...google-cloud-contentwarehouse-v0.4.1) (2023-03-25)


### Documentation

* Fix formatting of request arg in docstring ([#10867](https://github.com/googleapis/google-cloud-python/issues/10867)) ([d34a425](https://github.com/googleapis/google-cloud-python/commit/d34a425f7d0f02bebaf20d24b725b8c25c699697))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.3.1...google-cloud-contentwarehouse-v0.4.0) (2023-02-09)


### Features

* enable "rest" transport in Python for services supporting numeric enums ([#10839](https://github.com/googleapis/google-cloud-python/issues/10839)) ([ad59d56](https://github.com/googleapis/google-cloud-python/commit/ad59d569bda339ed31500602e2db369afdbfcf0b))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.3.0...google-cloud-contentwarehouse-v0.3.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([900a608](https://github.com/googleapis/google-cloud-python/commit/900a6083e59bfebf215e4e469bc842d8788bba18))


### Documentation

* Add documentation for enums ([900a608](https://github.com/googleapis/google-cloud-python/commit/900a6083e59bfebf215e4e469bc842d8788bba18))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.2.1...google-cloud-contentwarehouse-v0.3.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#10812](https://github.com/googleapis/google-cloud-python/issues/10812)) ([e5f88ee](https://github.com/googleapis/google-cloud-python/commit/e5f88eebd47c677850d61ddc3774532723f5505e))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.2.0...google-cloud-contentwarehouse-v0.2.1) (2022-12-06)


### Bug Fixes

* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))
* Drop usage of pkg_resources ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))
* Fix timeout default values ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))


### Documentation

* **samples:** Snippetgen should call await on the operation coroutine before calling result ([e477ab2](https://github.com/googleapis/google-cloud-python/commit/e477ab2581f44b540051dd201b9f543a30044833))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-contentwarehouse-v0.1.0...google-cloud-contentwarehouse-v0.2.0) (2022-11-10)


### Features

* Add typing to proto.Message based class attributes ([a6cbc16](https://github.com/googleapis/google-cloud-python/commit/a6cbc167835880f9fe31b4030ec5fba69e35b383))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([a6cbc16](https://github.com/googleapis/google-cloud-python/commit/a6cbc167835880f9fe31b4030ec5fba69e35b383))

## 0.1.0 (2022-11-09)


### Features

* add initial files for google.cloud.contentwarehouse.v1 ([#10714](https://github.com/googleapis/google-cloud-python/issues/10714)) ([a0bf1dd](https://github.com/googleapis/google-cloud-python/commit/a0bf1dd8b029349092aafa47566c11e1cc1532da))
