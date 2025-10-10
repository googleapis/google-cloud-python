# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-geminidataanalytics/#history

## [0.5.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-geminidataanalytics-v0.4.0...google-cloud-geminidataanalytics-v0.5.0) (2025-10-10)


### Features

* Add support for Python 3.14  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))


### Bug Fixes

* Deprecate credentials_file argument  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-geminidataanalytics-v0.3.0...google-cloud-geminidataanalytics-v0.4.0) (2025-09-24)


### ⚠ BREAKING CHANGES

* An existing message `RetrieveBigQueryTableContextsRequest` is removed
* An existing message `RetrieveBigQueryTableContextsResponse` is removed
* An existing message `RetrieveBigQueryTableContextsFromRecentTablesRequest` is removed
* An existing message `RetrieveBigQueryTableContextsFromRecentTablesResponse` is removed
* An existing message `RetrieveBigQueryTableSuggestedDescriptionsRequest` is removed
* An existing message `RetrieveBigQueryTableSuggestedDescriptionsResponse` is removed
* An existing message `RetrieveBigQueryTableSuggestedExamplesRequest` is removed
* An existing message `RetrieveBigQueryTableSuggestedExamplesResponse` is removed
* An existing message `RetrieveBigQueryRecentRelevantTablesRequest` is removed
* An existing message `RetrieveBigQueryRecentRelevantTablesResponse` is removed
* An existing message `DirectLookup` is removed
* An existing message `TableCandidate` is removed
* An existing service `ContextRetrievalService` is removed

### Bug Fixes

* An existing message `DirectLookup` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryRecentRelevantTablesRequest` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryRecentRelevantTablesResponse` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableContextsFromRecentTablesRequest` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableContextsFromRecentTablesResponse` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableContextsRequest` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableContextsResponse` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableSuggestedDescriptionsRequest` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableSuggestedDescriptionsResponse` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableSuggestedExamplesRequest` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `RetrieveBigQueryTableSuggestedExamplesResponse` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing message `TableCandidate` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* An existing service `ContextRetrievalService` is removed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))


### Documentation

* A comment for field `description` in message `.google.cloud.geminidataanalytics.v1alpha.Schema` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `example_queries` in message `.google.cloud.geminidataanalytics.v1alpha.Context` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `filter` in message `.google.cloud.geminidataanalytics.v1alpha.ListConversationsRequest` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `name` in message `.google.cloud.geminidataanalytics.v1alpha.Conversation` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `name` in message `.google.cloud.geminidataanalytics.v1alpha.DataAgent` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `synonyms` in message `.google.cloud.geminidataanalytics.v1alpha.Field` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `synonyms` in message `.google.cloud.geminidataanalytics.v1alpha.Schema` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `tags` in message `.google.cloud.geminidataanalytics.v1alpha.Field` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for field `tags` in message `.google.cloud.geminidataanalytics.v1alpha.Schema` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))
* A comment for message `ExampleQuery` is changed ([a336184](https://github.com/googleapis/google-cloud-python/commit/a336184b9e2f327251ff1785283b3eebf1a36b6d))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-geminidataanalytics-v0.2.0...google-cloud-geminidataanalytics-v0.3.0) (2025-08-29)


### ⚠ BREAKING CHANGES

* An existing method `RetrieveBigQueryTableContext` is removed from service `ContextRetrievalService`
* An existing message `RetrieveBigQueryTableContextRequest` is removed
* An existing message `RetrieveBigQueryTableContextResponse` is removed
* An existing service `ContextRetrievalService` is removed

### Features

* A new enum `DataFilterType` is added ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `description` is added to message `.google.cloud.geminidataanalytics.v1alpha.Schema` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `example_queries` is added to message `.google.cloud.geminidataanalytics.v1alpha.Context` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `filters` is added to message `.google.cloud.geminidataanalytics.v1alpha.Schema` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `schema` is added to message `.google.cloud.geminidataanalytics.v1alpha.BigQueryTableReference` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `synonyms` is added to message `.google.cloud.geminidataanalytics.v1alpha.Field` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `synonyms` is added to message `.google.cloud.geminidataanalytics.v1alpha.Schema` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `tags` is added to message `.google.cloud.geminidataanalytics.v1alpha.Field` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `tags` is added to message `.google.cloud.geminidataanalytics.v1alpha.Schema` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new field `value_format` is added to message `.google.cloud.geminidataanalytics.v1alpha.Field` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new message `DataFilter` is added ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* A new message `ExampleQuery` is added ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))


### Bug Fixes

* An existing message `RetrieveBigQueryTableContextRequest` is removed ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* An existing message `RetrieveBigQueryTableContextResponse` is removed ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* An existing method `RetrieveBigQueryTableContext` is removed from service `ContextRetrievalService` ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))
* An existing service `ContextRetrievalService` is removed ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))


### Documentation

* many comment updates ([25504f3](https://github.com/googleapis/google-cloud-python/commit/25504f3752d1e2c63d4f3f56114b7529c5f10b2e))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-geminidataanalytics-v0.1.0...google-cloud-geminidataanalytics-v0.2.0) (2025-07-16)


### ⚠ BREAKING CHANGES

* Correct the resource reference type for the parent field in data_chat_service proto

### Features

* Add `setIAM` and `getIAM` methods for managing agent sharing ([b803c39](https://github.com/googleapis/google-cloud-python/commit/b803c3910c141e39d8982947b11c7ebc5ac8c3fe))


### Bug Fixes

* Correct the resource reference type for the parent field in data_chat_service proto ([b803c39](https://github.com/googleapis/google-cloud-python/commit/b803c3910c141e39d8982947b11c7ebc5ac8c3fe))


### Documentation

* Update comments for multiple fields in Gemini Data Analytics API ([b803c39](https://github.com/googleapis/google-cloud-python/commit/b803c3910c141e39d8982947b11c7ebc5ac8c3fe))

## 0.1.0 (2025-06-19)


### Features

* add initial files for google.cloud.geminidataanalytics.v1alpha ([#14008](https://github.com/googleapis/google-cloud-python/issues/14008)) ([4aee4e3](https://github.com/googleapis/google-cloud-python/commit/4aee4e3740d988e73aff2f613df66020f1657b24))

## Changelog
