# Changelog

## [2.9.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.8.0...google-cloud-dataplex-v2.9.0) (2025-03-27)


### Features

* Add support for REST transport ([fe3dc62](https://github.com/googleapis/google-cloud-python/commit/fe3dc623808a5c40c157bf4fe55e8dd1fac39320))

## [2.8.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.7.1...google-cloud-dataplex-v2.8.0) (2025-03-15)


### Features

* [google-cloud-dataplex] Add custom BigQuery dataset location support in Auto Discovery ([#13641](https://github.com/googleapis/google-cloud-python/issues/13641)) ([90298dd](https://github.com/googleapis/google-cloud-python/commit/90298dd8ff2ab164af41848e91c789e87305f426))


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([feb5353](https://github.com/googleapis/google-cloud-python/commit/feb53532240bb70a94b359b519f0f41f95875a33))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))


### Documentation

* update the Dataplex Catalog proto to remove the info about schema ([90298dd](https://github.com/googleapis/google-cloud-python/commit/90298dd8ff2ab164af41848e91c789e87305f426))

## [2.7.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.7.0...google-cloud-dataplex-v2.7.1) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([16e14c8](https://github.com/googleapis/google-cloud-python/commit/16e14c8d547864360dcab45d90e9e55169204fc6))

## [2.7.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.6.0...google-cloud-dataplex-v2.7.0) (2025-02-12)


### Features

* Added value `NONE` to  the `SyncMode` enum ([71b9301](https://github.com/googleapis/google-cloud-python/commit/71b93012113bbaabf2ce524553342bdc52ba96dc))


### Documentation

* Modified various comments ([71b9301](https://github.com/googleapis/google-cloud-python/commit/71b93012113bbaabf2ce524553342bdc52ba96dc))

## [2.6.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.5.0...google-cloud-dataplex-v2.6.0) (2025-01-02)


### Features

* A new field `force` is added to message `.google.cloud.dataplex.v1.DeleteDataScanRequest` ([0da9e0a](https://github.com/googleapis/google-cloud-python/commit/0da9e0a01ddb9fae0df361d7cb131f2141ce5135))


### Documentation

* miscellaneous doc updates ([0da9e0a](https://github.com/googleapis/google-cloud-python/commit/0da9e0a01ddb9fae0df361d7cb131f2141ce5135))

## [2.5.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.4.0...google-cloud-dataplex-v2.5.0) (2024-12-12)


### Features

* Add support for opt-in debug logging ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))

## [2.4.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.3.1...google-cloud-dataplex-v2.4.0) (2024-11-15)


### Features

* A new enum `TableType` is added ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* A new field `datascan_id` is added to message `.google.cloud.dataplex.v1.DiscoveryEvent` ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* A new field `suspended` is added to DataScans ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* A new field `table` is added to message `.google.cloud.dataplex.v1.DiscoveryEvent` ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* A new message `TableDetails` is added ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a DATA_DISCOVERY enum type in DataScanEvent ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a DataDiscoveryAppliedConfigs message ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a TABLE_DELETED field in DiscoveryEvent ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a TABLE_IGNORED field in DiscoveryEvent ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a TABLE_PUBLISHED field in DiscoveryEvent ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add a TABLE_UPDATED field in DiscoveryEvent ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add an Issue field to DiscoveryEvent.ActionDetails to output the action message in Cloud Logs ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* add annotations in CreateMetadataJob, GetMetadataJob, ListMetaDataJobs and CancelMetadataJob for cloud audit logging ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add data_version field to AspectSource ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add new Data Discovery scan type in Datascan ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* expose create time in DataScanJobAPI ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* expose create time to customers ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* release metadata export in private preview ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* release MetadataJob APIs and related resources in GA ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))


### Documentation

* A comment for message `DataScanEvent` is changed ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add comment for field `status` in message `.google.cloud.dataplex.v1.MetadataJob` ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add comment for field `type` in message `.google.cloud.dataplex.v1.MetadataJob` ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add Identifier for `name` in message `.google.cloud.dataplex.v1.MetadataJob` ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* add info about schema changes for BigQuery metadata in Dataplex Catalog ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Add link to fully qualified names documentation ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* correct API documentation ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* correct the dimensions for data quality rules ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Dataplex Tasks do not support Dataplex Content path as a direct input anymore ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))
* Scrub descriptions for standalone discovery scans ([fffe7a5](https://github.com/googleapis/google-cloud-python/commit/fffe7a51c3b295e668426e103d523294787dff89))

## [2.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.3.0...google-cloud-dataplex-v2.3.1) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [2.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.2.2...google-cloud-dataplex-v2.3.0) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13202](https://github.com/googleapis/google-cloud-python/issues/13202)) ([5b1f2f3](https://github.com/googleapis/google-cloud-python/commit/5b1f2f3a81ed171b643812e67a7ed179b9b703ea))

## [2.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.2.1...google-cloud-dataplex-v2.2.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([ba1064f](https://github.com/googleapis/google-cloud-python/commit/ba1064fd6a63ccbe8a390c0026f32c5772c728a5))

## [2.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.2.0...google-cloud-dataplex-v2.2.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [2.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.1.0...google-cloud-dataplex-v2.2.0) (2024-06-27)


### Features

* [google-cloud-dataplex] expose data scan execution create time to customers ([#12846](https://github.com/googleapis/google-cloud-python/issues/12846)) ([2726a72](https://github.com/googleapis/google-cloud-python/commit/2726a721b0eecd05216fa018cce8d91407853187))

## [2.1.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.0.1...google-cloud-dataplex-v2.1.0) (2024-06-24)


### Features

* exposing EntrySource.location field that contains location of a resource in the source system ([9264874](https://github.com/googleapis/google-cloud-python/commit/9264874e8ab6cff0a837a3afbba33848e6100fd8))


### Documentation

* Scrub descriptions for GenerateDataQualityRules ([9264874](https://github.com/googleapis/google-cloud-python/commit/9264874e8ab6cff0a837a3afbba33848e6100fd8))

## [2.0.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v2.0.0...google-cloud-dataplex-v2.0.1) (2024-06-19)


### Documentation

* clarify DataQualityRule.sql_assertion descriptions ([74db0f8](https://github.com/googleapis/google-cloud-python/commit/74db0f812620a936fc055f49e0837aa30264fbda))
* fix links to RuleType proto references ([74db0f8](https://github.com/googleapis/google-cloud-python/commit/74db0f812620a936fc055f49e0837aa30264fbda))

## [2.0.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.13.0...google-cloud-dataplex-v2.0.0) (2024-05-16)


### ⚠ BREAKING CHANGES

* An existing field `entry` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `display_name` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `entry_type` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `modify_time` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `fully_qualified_name` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `description` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`
* An existing field `relative_resource` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult`

### Features

* updated client libraries for Dataplex Catalog: removed deprecated fields, updated comments ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))


### Bug Fixes

* An existing field `description` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `display_name` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `entry_type` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `entry` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `fully_qualified_name` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `modify_time` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* An existing field `relative_resource` is removed from message `.google.cloud.dataplex.v1.SearchEntriesResult` ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))


### Documentation

* A comment for field `aspects` in message `.google.cloud.dataplex.v1.Entry` is changed ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))
* A comment for field `filter` in message `.google.cloud.dataplex.v1.ListEntriesRequest` is changed ([fd6e39c](https://github.com/googleapis/google-cloud-python/commit/fd6e39c955877f90b63ff085be139ca2e7c5aff0))

## [1.13.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.12.3...google-cloud-dataplex-v1.13.0) (2024-03-22)


### Features

* [google-cloud-dataplex] added client side library for Unified and CRUD MetaStore APIs ([#12475](https://github.com/googleapis/google-cloud-python/issues/12475)) ([f56d7af](https://github.com/googleapis/google-cloud-python/commit/f56d7aff5caeb1fcf8f3ab421f9da83d88988241))

## [1.12.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.12.2...google-cloud-dataplex-v1.12.3) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12383](https://github.com/googleapis/google-cloud-python/issues/12383)) ([305f43f](https://github.com/googleapis/google-cloud-python/commit/305f43f7d6293e3316248f421fdc19c5d8405c21))

## [1.12.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.12.1...google-cloud-dataplex-v1.12.2) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12282](https://github.com/googleapis/google-cloud-python/issues/12282)) ([b985096](https://github.com/googleapis/google-cloud-python/commit/b985096d43add8214172ff993e00293e6c8757cb))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12305](https://github.com/googleapis/google-cloud-python/issues/12305)) ([2aa7f17](https://github.com/googleapis/google-cloud-python/commit/2aa7f17a5fd4f2249260225db91fb0414d06eaa7))

## [1.12.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.12.0...google-cloud-dataplex-v1.12.1) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))

## [1.12.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.11.0...google-cloud-dataplex-v1.12.0) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12239](https://github.com/googleapis/google-cloud-python/issues/12239)) ([8004d15](https://github.com/googleapis/google-cloud-python/commit/8004d15d9e6baa4dc5bc3f09d528e176d54d9ec5))


### Documentation

* [google-cloud-dataplex] fix typo in comment ([#12235](https://github.com/googleapis/google-cloud-python/issues/12235)) ([f8c331e](https://github.com/googleapis/google-cloud-python/commit/f8c331e24c91d8488bade3f761e26c440676f627))

## [1.11.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.10.0...google-cloud-dataplex-v1.11.0) (2024-01-04)


### Features

* [google-cloud-dataplex] added enum value EventType.GOVERNANCE_RULE_PROCESSING ([#12132](https://github.com/googleapis/google-cloud-python/issues/12132)) ([48d42fd](https://github.com/googleapis/google-cloud-python/commit/48d42fdffd8bc55346b7b560c9fdfe685b69930c))


### Documentation

* [google-cloud-dataplex] Fix the comment for `ignore_null` field to clarify its applicability on data quality rules ([#12141](https://github.com/googleapis/google-cloud-python/issues/12141)) ([ca71481](https://github.com/googleapis/google-cloud-python/commit/ca71481a3ddc9ec1bf4474c70e0512341a8adc9c))

## [1.10.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.9.0...google-cloud-dataplex-v1.10.0) (2023-12-07)


### Features

* [google-cloud-dataplex] add data quality score to DataQualityResult ([#12080](https://github.com/googleapis/google-cloud-python/issues/12080)) ([777891d](https://github.com/googleapis/google-cloud-python/commit/777891df576c55a740f3c2496263ec71dc63c123))
* Add support for python 3.12 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Introduce compatibility with native namespace packages ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Use `retry_async` instead of `retry` in async client ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))

## [1.9.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.8.1...google-cloud-dataplex-v1.9.0) (2023-11-29)


### Features

* added DataQualityResult.score, dimension_score, column_score ([b2dade2](https://github.com/googleapis/google-cloud-python/commit/b2dade2448863a9fba033030fcfbb1a03da68dd2))
* new event types GOVERNANCE_RULE_MATCHED_RESOURCES, GOVERNANCE_RULE_SEARCH_LIMIT_EXCEEDS, GOVERNANCE_RULE_ERRORS ([b2dade2](https://github.com/googleapis/google-cloud-python/commit/b2dade2448863a9fba033030fcfbb1a03da68dd2))

## [1.8.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.8.0...google-cloud-dataplex-v1.8.1) (2023-11-07)


### Documentation

* updated comments for `DataQualityResult.dimensions` field ([#11988](https://github.com/googleapis/google-cloud-python/issues/11988)) ([cf3d534](https://github.com/googleapis/google-cloud-python/commit/cf3d534856b3a5d9f56d85ba808cd3313b5a5434))

## [1.8.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.7.0...google-cloud-dataplex-v1.8.0) (2023-11-02)


### Features

* Add GovernanceEvent message ([#11939](https://github.com/googleapis/google-cloud-python/issues/11939)) ([a8e7269](https://github.com/googleapis/google-cloud-python/commit/a8e7269f87a31f57284420d575aa994f8268df92))

## [1.7.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.6.3...google-cloud-dataplex-v1.7.0) (2023-10-10)


### Features

* DataQualityDimension is now part of the DataQualityDimensionResult message ([#11791](https://github.com/googleapis/google-cloud-python/issues/11791)) ([88844db](https://github.com/googleapis/google-cloud-python/commit/88844db627026aad4be09e50ea6c9fff3573cc5b))

## [1.6.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.6.2...google-cloud-dataplex-v1.6.3) (2023-09-19)


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## [1.6.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.6.1...google-cloud-dataplex-v1.6.2) (2023-08-09)


### Bug Fixes

* remove unused annotation in results_table ([#11548](https://github.com/googleapis/google-cloud-python/issues/11548)) ([840fc36](https://github.com/googleapis/google-cloud-python/commit/840fc369045a16000ba876eebbeb1e0b5d1ee1d8))

## [1.6.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.6.0...google-cloud-dataplex-v1.6.1) (2023-08-03)


### Documentation

* Minor formatting ([#11543](https://github.com/googleapis/google-cloud-python/issues/11543)) ([8cc031e](https://github.com/googleapis/google-cloud-python/commit/8cc031e723350890b4ceb6e813f24c4bcde3d65f))

## [1.6.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.5.1...google-cloud-dataplex-v1.6.0) (2023-07-25)


### Features

* added DataQualityRule.name, description ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added DataQualitySpec.sampling_percent, row_filter ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added DataScanEvent.data_profile_configs, data_quality_configs, post_scan_actions_result ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added Job.labels, trigger, execution_spec ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added JobEvent.execution_trigger ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added ListDataScanJobsRequest.filter to filter ListDataScanJob results ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added RunTaskRequest.labels, args ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* added TopNValue.ratio ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* DataProfileSpec message with DataProfileScan related settings ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))
* new service DataTaxonomyService and related messages ([3392532](https://github.com/googleapis/google-cloud-python/commit/33925322472341319ff75e3039b109f7f34422ce))

## [1.5.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-dataplex-v1.5.0...google-cloud-dataplex-v1.5.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## [1.5.0](https://github.com/googleapis/python-dataplex/compare/v1.4.3...v1.5.0) (2023-05-25)


### Features

* Add `managed_access_identity` to `ResourceStatus` message ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))
* Add `read_access_mode` to `ResourceSpec` message ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))
* Add `resource` to `DataSource` message ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))
* Add `StorageAccess`, `RunTaskRequest`, `RunTaskResponse`, ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))
* Add `validate_only` to `CreateDataScanRequest` ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))
* Added new Dataplex APIs and new features for existing APIs (e.g. DataScans) ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))


### Documentation

* Updated comments for multiple Dataplex APIs ([17cf7f1](https://github.com/googleapis/python-dataplex/commit/17cf7f19242bfe8ca1a3b4d4348ab6d588b908ad))

## [1.4.3](https://github.com/googleapis/python-dataplex/compare/v1.4.2...v1.4.3) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#131](https://github.com/googleapis/python-dataplex/issues/131)) ([3ebb439](https://github.com/googleapis/python-dataplex/commit/3ebb439e786fecda33956c3eac2b0b3f451bedb1))

## [1.4.2](https://github.com/googleapis/python-dataplex/compare/v1.4.1...v1.4.2) (2023-02-02)


### Documentation

* Improvements to DataScan API documentation ([#123](https://github.com/googleapis/python-dataplex/issues/123)) ([a7e193f](https://github.com/googleapis/python-dataplex/commit/a7e193fb2cb0475ae1f75bb412967ec4436686e5))

## [1.4.1](https://github.com/googleapis/python-dataplex/compare/v1.4.0...v1.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([eb88024](https://github.com/googleapis/python-dataplex/commit/eb88024e41d4832ecd0e970ff7a87f57d74bba2a))


### Documentation

* Add documentation for enums ([eb88024](https://github.com/googleapis/python-dataplex/commit/eb88024e41d4832ecd0e970ff7a87f57d74bba2a))

## [1.4.0](https://github.com/googleapis/python-dataplex/compare/v1.3.0...v1.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#117](https://github.com/googleapis/python-dataplex/issues/117)) ([18c78d6](https://github.com/googleapis/python-dataplex/commit/18c78d63864fe2f7080f80d5faf3b0672e0d99d7))

## [1.3.0](https://github.com/googleapis/python-dataplex/compare/v1.2.0...v1.3.0) (2023-01-05)


### Features

* Added StorageFormat.iceberg ([16871c0](https://github.com/googleapis/python-dataplex/commit/16871c05637ef68bb99d9dc6b471dc029f368009))
* DataScans service ([16871c0](https://github.com/googleapis/python-dataplex/commit/16871c05637ef68bb99d9dc6b471dc029f368009))

## [1.2.0](https://github.com/googleapis/python-dataplex/compare/v1.1.2...v1.2.0) (2022-12-15)


### Features

* Add support for `google.cloud.dataplex.__version__` ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* Add support for notebook tasks ([#100](https://github.com/googleapis/python-dataplex/issues/100)) ([64d9c48](https://github.com/googleapis/python-dataplex/commit/64d9c481df1c2737189dcb575c69f2968c0aa034))
* Add typing to proto.Message based class attributes ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))


### Bug Fixes

* Add dict typing for client_options ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* **deps:** Allow protobuf 3.19.5 ([#103](https://github.com/googleapis/python-dataplex/issues/103)) ([65adbb3](https://github.com/googleapis/python-dataplex/commit/65adbb31c94794f27a78b309550c519734a7b030))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))
* Drop usage of pkg_resources ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))
* Fix timeout default values ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))


### Documentation

* Fix minor docstring formatting ([#113](https://github.com/googleapis/python-dataplex/issues/113)) ([0dc28b3](https://github.com/googleapis/python-dataplex/commit/0dc28b3c0f2c5be59a279c9ff859607d25906e84))
* **samples:** Snippetgen handling of repeated enum field ([18e2a32](https://github.com/googleapis/python-dataplex/commit/18e2a32c425f6a7ca0684392a796e18547ea408a))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([1e94a02](https://github.com/googleapis/python-dataplex/commit/1e94a024024638d5d7d31f7bba4408b3f0b3d5d1))

## [1.1.2](https://github.com/googleapis/python-dataplex/compare/v1.1.1...v1.1.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#98](https://github.com/googleapis/python-dataplex/issues/98)) ([1b178ce](https://github.com/googleapis/python-dataplex/commit/1b178ce8f12ed542bbe19736f9a416aa35c73828))

## [1.1.1](https://github.com/googleapis/python-dataplex/compare/v1.1.0...v1.1.1) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#84](https://github.com/googleapis/python-dataplex/issues/84)) ([747f4d9](https://github.com/googleapis/python-dataplex/commit/747f4d9fe8d4dbfeaf5576197c495edb6392a89f))
* **deps:** require proto-plus >= 1.22.0 ([747f4d9](https://github.com/googleapis/python-dataplex/commit/747f4d9fe8d4dbfeaf5576197c495edb6392a89f))

## [1.1.0](https://github.com/googleapis/python-dataplex/compare/v1.0.1...v1.1.0) (2022-07-15)


### Features

* add audience parameter ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add IAM support for Explore content APIs ([#74](https://github.com/googleapis/python-dataplex/issues/74)) ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for cross project for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for custom container for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for custom encryption key to be used for encrypt data on the PDs associated with the VMs in your Dataproc cluster for Task ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Add support for Latest job in Task resource ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* Support logging sampled file paths per partition to Cloud logging for Discovery event ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* User mode filter in Explore list sessions API ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* **deps:** require grpc-google-iam-v1 >=0.12.4 ([741f707](https://github.com/googleapis/python-dataplex/commit/741f7075723266c9c76e0cb6fc2dc720c350c819))
* require python 3.7+ ([#76](https://github.com/googleapis/python-dataplex/issues/76)) ([3cd158c](https://github.com/googleapis/python-dataplex/commit/3cd158c8a3b782683b5485d28bc14dadea852deb))

## [1.0.1](https://github.com/googleapis/python-dataplex/compare/v1.0.0...v1.0.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#66](https://github.com/googleapis/python-dataplex/issues/66)) ([0faef94](https://github.com/googleapis/python-dataplex/commit/0faef94bbd9371e41a18aa0372b1f59865010cab))


### Documentation

* fix changelog header to consistent size ([#67](https://github.com/googleapis/python-dataplex/issues/67)) ([3090fd6](https://github.com/googleapis/python-dataplex/commit/3090fd6d011e2a482e46a1c19c5e87a1aa90de35))

## [1.0.0](https://github.com/googleapis/python-dataplex/compare/v0.2.1...v1.0.0) (2022-04-26)


### Features

* bump release level to production/stable  ([b13ce8f](https://github.com/googleapis/python-dataplex/commit/b13ce8f2fda0dc60e8d1ed88e846fd8c027546e0))

## [0.2.1](https://github.com/googleapis/python-dataplex/compare/v0.2.0...v0.2.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#18](https://github.com/googleapis/python-dataplex/issues/18)) ([10b7809](https://github.com/googleapis/python-dataplex/commit/10b7809287befb914fdbe7cef3b1bded0eb7b63b))

## [0.2.0](https://github.com/googleapis/python-dataplex/compare/v0.1.0...v0.2.0) (2022-02-26)


### Features

* Added Create, Update and Delete APIs for Metadata (e.g. Entity and/or Partition). ([1333110](https://github.com/googleapis/python-dataplex/commit/13331107c96cb4d1e725eae291c9fee7316e6e72))
* Added support for Content APIs ([#8](https://github.com/googleapis/python-dataplex/issues/8)) ([1333110](https://github.com/googleapis/python-dataplex/commit/13331107c96cb4d1e725eae291c9fee7316e6e72))

## 0.1.0 (2022-01-28)


### Features

* generate v1 ([f29b530](https://github.com/googleapis/python-dataplex/commit/f29b5309dfad9df04c0dc564e065195ae33985b8))
