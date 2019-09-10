# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery/#history

## 1.19.0

09-03-2019 14:33 PDT

### Implementation Changes

- Raise when unexpected fields are present in the `LoadJobConfig.schema` when calling `load_table_from_dataframe`. ([#9096](https://github.com/googleapis/google-cloud-python/pull/9096))
- Determine the schema in `load_table_from_dataframe` based on dtypes. ([#9049](https://github.com/googleapis/google-cloud-python/pull/9049))
- Raise helpful error when loading table from dataframe with `STRUCT` columns. ([#9053](https://github.com/googleapis/google-cloud-python/pull/9053))
- Fix schema recognition of struct field types. ([#9001](https://github.com/googleapis/google-cloud-python/pull/9001))
- Fix deserializing `None` in `QueryJob` for queries with parameters. ([#9029](https://github.com/googleapis/google-cloud-python/pull/9029))

### New Features

- Include indexes in table written by `load_table_from_dataframe`, only if
  fields corresponding to indexes are present in `LoadJobConfig.schema`.
  ([#9084](https://github.com/googleapis/google-cloud-python/pull/9084))
- Add `client_options` to constructor. ([#8999](https://github.com/googleapis/google-cloud-python/pull/8999))
- Add `--dry_run` option to `%%bigquery` magic. ([#9067](https://github.com/googleapis/google-cloud-python/pull/9067))
- Add `load_table_from_json()` method to create a table from a list of dictionaries. ([#9076](https://github.com/googleapis/google-cloud-python/pull/9076))
- Allow subset of schema to be passed into `load_table_from_dataframe`. ([#9064](https://github.com/googleapis/google-cloud-python/pull/9064))
- Add support for unsetting `LoadJobConfig.schema`. ([#9077](https://github.com/googleapis/google-cloud-python/pull/9077))
- Add support to `Dataset` for project IDs containing an org prefix. ([#8877](https://github.com/googleapis/google-cloud-python/pull/8877))
- Add enum with SQL type names allowed to be used in `SchemaField`. ([#9040](https://github.com/googleapis/google-cloud-python/pull/9040))

### Documentation

- Fix the reference URL for `Client.create_dataset()`. ([#9149](https://github.com/googleapis/google-cloud-python/pull/9149))
- Update code samples to use strings for table names instead of `client.dataset()`. ([#9032](https://github.com/googleapis/google-cloud-python/pull/9032))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Fix Pandas DataFrame load example under Python 2.7. ([#9022](https://github.com/googleapis/google-cloud-python/pull/9022))

### Internal / Testing Changes

- Disable failing snippets test for copying CMEK-protected tables. ([#9156](https://github.com/googleapis/google-cloud-python/pull/9156))
- Fix BigQuery client unit test assertions ([#9112](https://github.com/googleapis/google-cloud-python/pull/9112))
- Replace avro with arrow schemas in `test_table.py` ([#9056](https://github.com/googleapis/google-cloud-python/pull/9056))

## 1.18.0

08-08-2019 12:28 PDT

### New Features

- Add `bqstorage_client` param to `QueryJob.to_arrow()` ([#8693](https://github.com/googleapis/google-cloud-python/pull/8693))
- Include SQL query and job ID in exception messages. ([#8748](https://github.com/googleapis/google-cloud-python/pull/8748))
- Allow using TableListItem to construct a Table object. ([#8738](https://github.com/googleapis/google-cloud-python/pull/8738))
- Add StandardSqlDataTypes enum to BigQuery ([#8782](https://github.com/googleapis/google-cloud-python/pull/8782))
- Add `to_standard_sql()` method to SchemaField ([#8880](https://github.com/googleapis/google-cloud-python/pull/8880))
- Add debug logging statements to track when BQ Storage API is used. ([#8838](https://github.com/googleapis/google-cloud-python/pull/8838))
- Hide error traceback in BigQuery cell magic ([#8808](https://github.com/googleapis/google-cloud-python/pull/8808))
- Allow choice of compression when loading from dataframe ([#8938](https://github.com/googleapis/google-cloud-python/pull/8938))
- Additional clustering metrics for BQML K-means models (via synth). ([#8945](https://github.com/googleapis/google-cloud-python/pull/8945))

### Documentation

- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Remove redundant service account key code sample. ([#8891](https://github.com/googleapis/google-cloud-python/pull/8891))

### Internal / Testing Changes

- Fix several pytest "skip if" markers ([#8694](https://github.com/googleapis/google-cloud-python/pull/8694))
- Update tests to support conversion of NaN as NULL in pyarrow `0.14.*`. ([#8785](https://github.com/googleapis/google-cloud-python/pull/8785))
- Mock external calls in one of BigQuery unit tests ([#8727](https://github.com/googleapis/google-cloud-python/pull/8727))
- Set IPython user agent when running queries with IPython cell magic ([#8713](https://github.com/googleapis/google-cloud-python/pull/8713))
- Use configurable bucket name for GCS samples data in systems tests. ([#8783](https://github.com/googleapis/google-cloud-python/pull/8783))
- Move `maybe_fail_import()` to top level test utils ([#8840](https://github.com/googleapis/google-cloud-python/pull/8840))
- Set BQ Storage client user-agent when in Jupyter cell ([#8734](https://github.com/googleapis/google-cloud-python/pull/8734))

## 1.17.0

07-12-2019 07:56 PDT

### New Features

- Support faster Arrow data format in `to_dataframe` when using BigQuery Storage API. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))
- Add `to_arrow` to get a `pyarrow.Table` from query results. ([#8609](https://github.com/googleapis/google-cloud-python/pull/8609))

### Dependencies

- Exclude bad 0.14.0 `pyarrow` release. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))

## 1.16.0

07-01-2019 10:22 PDT

### New Features

- Add Routines API. ([#8491](https://github.com/googleapis/google-cloud-python/pull/8491))
- Add more stats to Models API, such as `optimization_strategy` (via synth). ([#8344](https://github.com/googleapis/google-cloud-python/pull/8344))

### Documentation

- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Add sample demonstrating how to create a job. ([#8422](https://github.com/googleapis/google-cloud-python/pull/8422))
- Use autodetected location in code samples. ([#8340](https://github.com/googleapis/google-cloud-python/pull/8340), [#8341](https://github.com/googleapis/google-cloud-python/pull/8341))

### Internal / Testing Changes

- Refactor `to_dataframe` to deterministicly update progress bar. ([#8303](https://github.com/googleapis/google-cloud-python/pull/8303))

## 1.15.0

06-14-2019 10:10 PDT

### Implementation Changes

- Fix bug where `load_table_from_dataframe` could not append to REQUIRED fields. ([#8230](https://github.com/googleapis/google-cloud-python/pull/8230))

### New Features

- Add `page_size` parameter to `QueryJob.result`. ([#8206](https://github.com/googleapis/google-cloud-python/pull/8206))

## 1.14.0

06-04-2019 11:11 PDT


### New Features
- Add `maximum_bytes_billed` argument and `context.default_query_job_config` property to magics. ([#8179](https://github.com/googleapis/google-cloud-python/pull/8179))

### Dependencies
- Don't pin `google-api-core` in libs using `google-cloud-core`. ([#8213](https://github.com/googleapis/google-cloud-python/pull/8213))

## 1.13.0

05-31-2019 10:22 PDT

### New Features

- Use `job_config.schema` for data type conversion if specified in `load_table_from_dataframe`. ([#8105](https://github.com/googleapis/google-cloud-python/pull/8105))

### Internal / Testing Changes

- Adds private `_connection` object to magics context. ([#8192](https://github.com/googleapis/google-cloud-python/pull/8192))
- Fix coverage in 'types.py' (via synth). ([#8146](https://github.com/googleapis/google-cloud-python/pull/8146))

## 1.12.1

05-21-2019 11:16 PDT

### Implementation Changes

- Don't raise error when encountering unknown fields in Models API. ([#8083](https://github.com/googleapis/google-cloud-python/pull/8083))

### Documentation

- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

### Internal / Testing Changes

- Add empty lines (via synth). ([#8049](https://github.com/googleapis/google-cloud-python/pull/8049))

## 1.12.0

05-16-2019 11:25 PDT

### Implementation Changes
- Remove duplicates from index on pandas DataFrames returned by `to_dataframe()`. ([#7953](https://github.com/googleapis/google-cloud-python/pull/7953))
- Prevent error when time partitioning is populated with empty dict ([#7904](https://github.com/googleapis/google-cloud-python/pull/7904))
- Preserve order in `to_dataframe` with BQ Storage from queries containing `ORDER BY` ([#7793](https://github.com/googleapis/google-cloud-python/pull/7793))
- Respect `progress_bar_type` in `to_dataframe` when used with BQ Storage API ([#7697](https://github.com/googleapis/google-cloud-python/pull/7697))
- Refactor QueryJob.query to read from resource dictionary ([#7763](https://github.com/googleapis/google-cloud-python/pull/7763))
- Close the `to_dataframe` progress bar when finished. ([#7757](https://github.com/googleapis/google-cloud-python/pull/7757))
- Ensure that `KeyboardInterrupt` during `to_dataframe`no longer hangs. ([#7698](https://github.com/googleapis/google-cloud-python/pull/7698))
- Raise ValueError when BQ Storage is required but missing ([#7726](https://github.com/googleapis/google-cloud-python/pull/7726))
- Make `total_rows` available on RowIterator before iteration ([#7622](https://github.com/googleapis/google-cloud-python/pull/7622))
- Avoid masking auth errors in `to_dataframe` with BQ Storage API ([#7674](https://github.com/googleapis/google-cloud-python/pull/7674))

### New Features
- Add support for passing `client_info`. ([#7849](https://github.com/googleapis/google-cloud-python/pull/7849) and ([#7806](https://github.com/googleapis/google-cloud-python/pull/7806))
- Phase 1 for storing schemas for later use. ([#7761](https://github.com/googleapis/google-cloud-python/pull/7761))
- Add `destination` and related properties to LoadJob. ([#7710](https://github.com/googleapis/google-cloud-python/pull/7710))
- Add `clustering_fields` property to TableListItem ([#7692](https://github.com/googleapis/google-cloud-python/pull/7692))
- Add `created` and `expires` properties to TableListItem ([#7684](https://github.com/googleapis/google-cloud-python/pull/7684))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))
- Add `[all]` extras to install all extra dependencies ([#7610](https://github.com/googleapis/google-cloud-python/pull/7610))

### Documentation
- Move table and dataset snippets to samples/ directory ([#7683](https://github.com/googleapis/google-cloud-python/pull/7683))

### Internal / Testing Changes
- Blacken unit tests. ([#7960](https://github.com/googleapis/google-cloud-python/pull/7960))
- Cleanup client tests with method to create minimal table resource ([#7802](https://github.com/googleapis/google-cloud-python/pull/7802))

## 1.11.2

04-05-2019 08:16 PDT

### Dependencies

- Add dependency on protobuf. ([#7668](https://github.com/googleapis/google-cloud-python/pull/7668))

## 1.11.1

04-04-2019 09:19 PDT

### Internal / Testing Changes

- Increment version number in `setup.py`.

## 1.11.0

04-03-2019 19:33 PDT

### Implementation Changes

- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features

- Enable fastparquet support by using temporary file in `load_table_from_dataframe` ([#7545](https://github.com/googleapis/google-cloud-python/pull/7545))
- Allow string for copy sources, query destination, and default dataset ([#7560](https://github.com/googleapis/google-cloud-python/pull/7560))
- Add `progress_bar_type` argument to `to_dataframe` to use `tqdm` to display a progress bar ([#7552](https://github.com/googleapis/google-cloud-python/pull/7552))
- Call `get_table` in `list_rows` if the schema is not available ([#7621](https://github.com/googleapis/google-cloud-python/pull/7621))
- Fallback to BQ API when there are problems reading from BQ Storage. ([#7633](https://github.com/googleapis/google-cloud-python/pull/7633))
- Add methods for Models API ([#7562](https://github.com/googleapis/google-cloud-python/pull/7562))
- Add option to use BigQuery Storage API from IPython magics ([#7640](https://github.com/googleapis/google-cloud-python/pull/7640))

### Documentation

- Remove typo in `Table.from_api_repr` docstring. ([#7509](https://github.com/googleapis/google-cloud-python/pull/7509))
- Add docs session to nox configuration for BigQuery ([#7541](https://github.com/googleapis/google-cloud-python/pull/7541))

### Internal / Testing Changes

- Refactor `table()` methods into shared implementation. ([#7516](https://github.com/googleapis/google-cloud-python/pull/7516))
- Blacken noxfile and setup file in nox session ([#7619](https://github.com/googleapis/google-cloud-python/pull/7619))
- Actually use the `progress_bar_type` argument in `QueryJob.to_dataframe()`. ([#7616](https://github.com/googleapis/google-cloud-python/pull/7616))

## 1.10.0

03-06-2019 15:20 PST

### Implementation Changes

- Harden 'ArrayQueryParameter.from_api_repr' against missing 'parameterValue'. ([#7311](https://github.com/googleapis/google-cloud-python/pull/7311))
- Allow nested records w/ null values. ([#7297](https://github.com/googleapis/google-cloud-python/pull/7297))

### New Features

- Add options to ignore errors when creating/deleting datasets/tables. ([#7491](https://github.com/googleapis/google-cloud-python/pull/7491))
- Accept a string in Table and Dataset constructors. ([#7483](https://github.com/googleapis/google-cloud-python/pull/7483))

### Documentation

- Update docstring of RowIterator's to_dataframe ([#7306](https://github.com/googleapis/google-cloud-python/pull/7306))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes

- Fix lint. ([#7383](https://github.com/googleapis/google-cloud-python/pull/7383))

## 1.9.0

02-04-2019 13:28 PST

### New Features

- Add arguments to select `dtypes` and use BQ Storage API to `QueryJob.to_dataframe()`. ([#7241](https://github.com/googleapis/google-cloud-python/pull/7241))

### Documentation

- Add sample for fetching `total_rows` from query results. ([#7217](https://github.com/googleapis/google-cloud-python/pull/7217))

## 1.8.1

12-17-2018 17:53 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for 'page_size' / 'max_results' / 'page_token' ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 1.8.0

12-10-2018 12:39 PST


### Implementation Changes
- Add option to use BQ Storage API with `to_dataframe` ([#6854](https://github.com/googleapis/google-cloud-python/pull/6854))
- Fix exception type in comment ([#6847](https://github.com/googleapis/google-cloud-python/pull/6847))
- Add `to_bqstorage` to convert from Table[Reference] google-cloud-bigquery-storage reference ([#6840](https://github.com/googleapis/google-cloud-python/pull/6840))
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Add avro logical type control for load jobs. ([#6827](https://github.com/googleapis/google-cloud-python/pull/6827))
- Allow setting partition expiration to 'None'. ([#6823](https://github.com/googleapis/google-cloud-python/pull/6823))
- Add `retry` argument to `_AsyncJob.result`. ([#6302](https://github.com/googleapis/google-cloud-python/pull/6302))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))

### Documentation
- Add avro load samples ([#6832](https://github.com/googleapis/google-cloud-python/pull/6832))

### Internal / Testing Changes
- Blacken libraries ([#6794](https://github.com/googleapis/google-cloud-python/pull/6794))
- Fix copy/paste typos in noxfile comments ([#6831](https://github.com/googleapis/google-cloud-python/pull/6831))

## 1.7.0

11-05-2018 16:41 PST

### Implementation Changes

- Add destination table properties to `LoadJobConfig`. ([#6202](https://github.com/googleapis/google-cloud-python/pull/6202))
- Allow strings or references in `create_dataset` and `create_table` ([#6199](https://github.com/googleapis/google-cloud-python/pull/6199))
- Fix swallowed error message ([#6168](https://github.com/googleapis/google-cloud-python/pull/6168))

### New Features

- Add `--params option` to `%%bigquery` magic ([#6277](https://github.com/googleapis/google-cloud-python/pull/6277))
- Expose `to_api_repr` method for jobs. ([#6176](https://github.com/googleapis/google-cloud-python/pull/6176))
- Allow string in addition to DatasetReference / TableReference in Client methods. ([#6164](https://github.com/googleapis/google-cloud-python/pull/6164))
- Add keyword arguments to job config constructors for setting properties ([#6397](https://github.com/googleapis/google-cloud-python/pull/6397))

### Documentation

- Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Move usage guides to their own docs. ([#6238](https://github.com/googleapis/google-cloud-python/pull/6238))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes

- Deprecation cleanups ([#6304](https://github.com/googleapis/google-cloud-python/pull/6304))
- Use `_get_sub_prop` helper so missing load stats don't raise. ([#6269](https://github.com/googleapis/google-cloud-python/pull/6269))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Harden snippets against transient GCS errors. ([#6184](https://github.com/googleapis/google-cloud-python/pull/6184))

## 1.6.0

### New Features
- Add support for `GEOGRAPHY` type ([#6147](https://github.com/googleapis/google-cloud-python/pull/6147))
- Add default QueryJobConfig to Client ([#6088](https://github.com/googleapis/google-cloud-python/pull/6088))

### Documentation
- Remove unused "append" samples ([#6100](https://github.com/googleapis/google-cloud-python/pull/6100))

### Internal / Testing Changes
- Address dataset leaks, conflicts in systests ([#6099](https://github.com/googleapis/google-cloud-python/pull/6099))
- Harden bucket teardown against `429 Too Many Requests`. ([#6101](https://github.com/googleapis/google-cloud-python/pull/6101))

## 1.5.1

### Implementation Changes

- Retry '502 Bad Gateway' errors by default. (#5930)
- Avoid pulling entire result set into memory when constructing dataframe. (#5870)
- Add support for retrying unstructured 429 / 500 / 502 responses. (#6011)
- Populate the jobReference from the API response. (#6044)

### Documentation

- Prepare documentation for repo split (#5955)
- Fix leakage of bigquery/spanner sections into sidebar menu. (#5986)

### Internal / Testing Changes

- Test pandas support under Python 3.7. (#5857)
- Nox: use inplace installs (#5865)
- Update system test to use test data in bigquery-public-data. (#5965)

## 1.5.0

### Implementation Changes

- Make 'Table.location' read-only. (#5687)

### New Features

- Add 'clustering_fields' properties. (#5630)
- Add support for job labels (#5654)
- Add 'QueryJob.estimated_bytes_processed' property (#5655)
- Add support/tests for loading tables from 'gzip.GzipFile'. (#5711)
- Add 'ExternalSourceFormat' enum. (#5674)
- Add default location to client (#5678)

### Documentation

- Fix typo in CopyJob sources docstring (#5690)

### Internal / Testing Changes

- Add/refactor snippets for managing BigQuery jobs (#5631)
- Reenable systests for 'dataset.update'/'table.update'. (#5732)

## 1.4.0

### Implementation Changes

- Add 'internalError' to retryable error reasons. (#5599)
- Don't raise exception if viewing CREATE VIEW DDL results (#5602)

### New Features

- Add Orc source format support and samples (#5500)
- Move 'DEFAULT_RETRY' (w/ its predicate) to a new public 'retry' module. (#5552)
- Allow listing rows on an empty table. (#5584)

### Documentation

- Add load_table_from_dataframe() to usage docs and changelog and dedents snippets in usage page (#5501)
- Add samples for query external data sources (GCS & Sheets) (#5491)
- Add BigQuery authorized view samples (#5515)
- Update docs to show pyarrow as the only dependency of load_table_from_dataframe() (#5582)

### Internal / Testing Changes

- Add missing explict coverage for '_helpers' (#5550)
- Skip update_table and update_dataset tests until etag issue is resolved. (#5590)

## 1.3.0

### New Features

- NUMERIC type support (#5331)
- Add timeline and top-level slot-millis to query statistics. (#5312)
- Add additional statistics to query plan stages. (#5307)
- Add `client.load_table_from_dataframe()` (#5387)

### Documentation

- Use autosummary to split up API reference docs (#5340)
- Fix typo in Client docstrings (#5342)

### Internal / Testing Changes

- Prune systests identified as reduntant to snippets. (#5365)
- Modify system tests to use prerelease versions of grpcio (#5304)
- Improve system test performance (#5319)

## 1.2.0

### Implementation Changes
- Switch `list_partitions` helper to a direct metatable read (#5273)
- Fix typo in `Encoding.ISO_8859_1` enum value (#5211)

### New Features
- Add UnknownJob type for redacted jobs. (#5281)
- Add project parameter to `list_datasets` and `list_jobs` (#5217)
- Add from_string factory methods to Dataset and Table (#5255)
- Add column based time partitioning (#5267)

### Documentation
- Standardize docstrings for constants (#5289)
- Fix docstring / impl of `ExtractJob.destination_uri_file_counts`. (#5245)

### Internal / Testing Changes
- Add testing support for Python 3.7; remove testing support for Python 3.4. (#5295)

## 1.1.0

### New Features
- Add `client.get_service_account_email` (#5203)

### Documentation
- Update samples and standardize region tags (#5195)

### Internal / Testing Changes
- Fix trove classifier to be Production/Stable
- Don't suppress 'dots' output on test (#5202)

## 1.0.0

### Implementation Changes
- Remove deprecated Client methods (#5182)

## 0.32.0

### :warning: Interface changes

- Use `job.configuration` resource for XXXJobConfig classes (#5036)

### Interface additions

- Add `page_size` parameter for `list_rows` and use in DB-API for `arraysize` (#4931)
- Add IPython magics for running queries (#4983)

### Documentation

- Add job string constant parameters in init and snippets documentation (#4987)

### Internal / Testing changes

- Specify IPython version 5.5 when running Python 2.7 tests (#5145)
- Move all Dataset property conversion logic into properties (#5130)
- Remove unnecessary _Table class from test_job.py (#5126)
- Use explicit bytes to initialize 'BytesIO'. (#5116)
- Make SchemaField be able to include description via from_api_repr method (#5114)
- Remove _ApiResourceProperty class (#5107)
- Add dev version for 0.32.0 release (#5105)
- StringIO to BytesIO (#5101)
- Shorten snippets test name (#5091)
- Don't use `selected_fields` for listing query result rows (#5072)
- Add location property to job classes. (#5071)
- Use autospec for Connection in tests. (#5066)
- Add Parquet SourceFormat and samples (#5057)
- Remove test_load_table_from_uri_w_autodetect_schema_then_get_job because of duplicate test in snippets (#5004)
- Fix encoding variable and strings UTF-8 and ISO-8859-1 difference documentation (#4990)

## 0.31.0

### Interface additions

- Add support for `EncryptionConfiguration` (#4845)

### Implementation changes

- Allow listing/getting jobs even when there is an "invalid" job. (#4786)

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Documentation

- Update format in `Table.full_table_id` and `TableListItem.full_table_id` docstrings. (#4906)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Remove unnecessary debug print from tests (#4907)
- Use constant strings for job properties in tests (#4833)

## 0.30.0

This is the release candidate for v1.0.0.

### Interface changes / additions

- Add `delete_contents` to `delete_dataset`. (#4724)

### Bugfixes

- Add handling of missing properties in `SchemaField.from_api_repr()`. (#4754)
- Fix missing return value in `LoadJobConfig.from_api_repr`. (#4727)

### Documentation

- Minor documentation and typo fixes. (#4782, #4718, #4784, #4835, #4836)

## 0.29.0

### Interface changes / additions

-   Add `to_dataframe()` method to row iterators. When Pandas is installed this
    method returns a `DataFrame` containing the query's or table's rows.
    ([#4354](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4354))
-   Iterate over a `QueryJob` to wait for and get the query results.
    ([#4350](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4350))
-   Add `Table.reference` and `Dataset.reference` properties to get the
    `TableReference` or `DatasetReference` corresponding to that `Table` or
    `Dataset`, respectively.
    ([#4405](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4405))
-   Add `Row.keys()`, `Row.items()`, and `Row.get()`. This makes `Row` act
    more like a built-in dictionary.
    ([#4393](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4393),
    [#4413](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4413))

### Interface changes / breaking changes

-   Add `Client.insert_rows()` and `Client.insert_rows_json()`, deprecate
    `Client.create_rows()` and `Client.create_rows_json()`.
    ([#4657](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4657))
-   Add `Client.list_tables`, deprecate `Client.list_dataset_tables`.
    ([#4653](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4653))
-   `Client.list_tables` returns an iterators of `TableListItem`. The API
    only returns a subset of properties of a table when listing.
    ([#4427](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4427))
-   Remove `QueryJob.query_results()`. Use `QueryJob.result()` instead.
    ([#4652](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4652))
-   Remove `Client.query_rows()`. Use `Client.query()` instead.
    ([#4429](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4429))
-   `Client.list_datasets` returns an iterator of `DatasetListItem`. The API
    only returns a subset of properties of a dataset when listing.
    ([#4439](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4439))

## 0.28.0

**0.28.0 significantly changes the interface for this package.** For examples
of the differences between 0.28.0 and previous versions, see
[Migrating to the BigQuery Python client library 0.28][2].
These changes can be summarized as follows:

-   Query and view operations default to the standard SQL dialect. (#4192)
-   Client functions related to
    [jobs](https://cloud.google.com/bigquery/docs/jobs-overview), like running
    queries, immediately start the job.
-   Functions to create, get, update, delete datasets and tables moved to the
    client class.

[2]: https://cloud.google.com/bigquery/docs/python-client-migration

### Fixes

- Populate timeout parameter correctly for queries (#4209)
- Automatically retry idempotent RPCs (#4148, #4178)
- Parse timestamps in query parameters using canonical format (#3945)
- Parse array parameters that contain a struct type. (#4040)
- Support Sub Second Datetimes in row data (#3901, #3915, #3926), h/t @page1

### Interface changes / additions

- Support external table configuration (#4182) in query jobs (#4191) and
  tables (#4193).
- New `Row` class allows for access by integer index like a tuple, string
  index like a dictionary, or attribute access like an object. (#4149)
- Add option for job ID generation with user-supplied prefix (#4198)
- Add support for update of dataset access entries (#4197)
- Add support for atomic read-modify-write of a dataset using etag (#4052)
- Add support for labels to `Dataset` (#4026)
- Add support for labels to `Table` (#4207)
- Add `Table.streaming_buffer` property (#4161)
- Add `TableReference` class (#3942)
- Add `DatasetReference` class (#3938, #3942, #3993)
- Add `ExtractJob.destination_uri_file_counts` property. (#3803)
- Add `client.create_rows_json()` to bypass conversions on streaming writes.
  (#4189)
- Add `client.get_job()` to get arbitrary jobs. (#3804, #4213)
- Add filter to `client.list_datasets()` (#4205)
- Add `QueryJob.undeclared_query_parameters` property. (#3802)
- Add `QueryJob.referenced_tables` property. (#3801)
- Add new scalar statistics properties to `QueryJob` (#3800)
- Add `QueryJob.query_plan` property. (#3799)

### Interface changes / breaking changes

- Remove `client.run_async_query()`, use `client.query()` instead. (#4130)
- Remove `client.run_sync_query()`, use `client.query_rows()` instead. (#4065, #4248)
- Make `QueryResults` read-only. (#4094, #4144)
- Make `get_query_results` private. Return rows for `QueryJob.result()` (#3883)
- Move `*QueryParameter` and `UDFResource` classes to `query` module (also
  exposed in `bigquery` module). (#4156)

#### Changes to tables

- Remove `client` from `Table` class (#4159)
- Remove `table.exists()` (#4145)
- Move `table.list_parations` to `client.list_partitions` (#4146)
- Move `table.upload_from_file` to `client.load_table_from_file` (#4136)
- Move `table.update()` and `table.patch()` to `client.update_table()` (#4076)
- Move `table.insert_data()` to `client.create_rows()`. Automatically
  generates row IDs if not supplied. (#4151, #4173)
- Move `table.fetch_data()` to `client.list_rows()` (#4119, #4143)
- Move `table.delete()` to `client.delete_table()` (#4066)
- Move `table.create()` to `client.create_table()` (#4038, #4043)
- Move `table.reload()` to `client.get_table()` (#4004)
- Rename `Table.name` attribute to `Table.table_id` (#3959)
- `Table` constructor takes a `TableReference` as parameter (#3997)

#### Changes to datasets

- Remove `client` from `Dataset` class (#4018)
- Remove `dataset.exists()` (#3996)
- Move `dataset.list_tables()` to `client.list_dataset_tables()` (#4013)
- Move `dataset.delete()` to `client.delete_dataset()` (#4012)
- Move `dataset.patch()` and `dataset.update()` to `client.update_dataset()` (#4003)
- Move `dataset.create()` to `client.create_dataset()` (#3982)
- Move `dataset.reload()` to `client.get_dataset()` (#3973)
- Rename `Dataset.name` attribute to `Dataset.dataset_id` (#3955)
- `client.dataset()` returns a `DatasetReference` instead of `Dataset`. (#3944)
- Rename class: `dataset.AccessGrant -> dataset.AccessEntry`. (#3798)
- `dataset.table()` returns a `TableReference` instead of a `Table` (#4014)
- `Dataset` constructor takes a DatasetReference (#4036)

#### Changes to jobs

- Make `job.begin()` method private. (#4242)
- Add `LoadJobConfig` class and modify `LoadJob` (#4103, #4137)
- Add `CopyJobConfig` class and modify `CopyJob` (#4051, #4059)
- Type of Job's and Query's `default_dataset` changed from `Dataset` to
  `DatasetReference` (#4037)
- Rename `client.load_table_from_storage()` to `client.load_table_from_uri()`
  (#4235)
- Rename `client.extract_table_to_storage` to `client.extract_table()`.
  Method starts the extract job immediately. (#3991, #4177)
- Rename `XJob.name` to `XJob.job_id`. (#3962)
- Rename job classes. `LoadTableFromStorageJob -> LoadJob` and
  `ExtractTableToStorageJob -> jobs.ExtractJob` (#3797)

### Dependencies

- Updating to `google-cloud-core ~= 0.28`, in particular, the
  `google-api-core` package has been moved out of `google-cloud-core`. (#4221)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.28.0/


## 0.27.0

- Remove client-side enum validation. (#3735)
- Add `Table.row_from_mapping` helper. (#3425)
- Move `google.cloud.future` to `google.api.core` (#3764)
- Fix `__eq__` and `__ne__`. (#3765)
- Move `google.cloud.iterator` to `google.api.core.page_iterator` (#3770)
- `nullMarker` support for BigQuery Load Jobs (#3777), h/t @leondealmeida
- Allow `job_id` to be explicitly specified in DB-API. (#3779)
- Add support for a custom null marker. (#3776)
- Add `SchemaField` serialization and deserialization. (#3786)
- Add `get_query_results` method to the client. (#3838)
- Poll for query completion via `getQueryResults` method. (#3844)
- Allow fetching more than the first page when `max_results` is set. (#3845)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.27.0/

## 0.26.0

### Notable implementation changes

- Using the `requests` transport attached to a Client for for resumable media
  (i.e. downloads and uploads) (#3705) (this relates to the `httplib2` to
  `requests` switch)

### Interface changes / additions

- Adding `autodetect` property on `LoadTableFromStorageJob` to enable schema
  autodetection. (#3648)
- Implementing the Python Futures interface for Jobs. Call `job.result()` to
  wait for jobs to complete instead of polling manually on the job status.
  (#3626)
- Adding `is_nullable` property on `SchemaField`. Can be used to check if a
  column is nullable. (#3620)
- `job_name` argument added to `Table.upload_from_file` for setting the job
  ID. (#3605)
- Adding `google.cloud.bigquery.dbapi` package, which implements PEP-249
  DB-API specification. (#2921)
- Adding `Table.view_use_legacy_sql` property. Can be used to create views
  with legacy or standard SQL. (#3514)

### Interface changes / breaking changes

- Removing `results()` method from the `QueryJob` class. Use
  `query_results()` instead. (#3661)
- `SchemaField` is now immutable. It is also hashable so that it can be used
  in sets. (#3601)

### Dependencies

- Updating to `google-cloud-core ~= 0.26`, in particular, the underlying HTTP
  transport switched from `httplib2` to `requests` (#3654, #3674)
- Adding dependency on `google-resumable-media` for loading BigQuery tables
  from local files. (#3555)

### Packaging

- Fix inclusion of `tests` (vs. `unit_tests`) in `MANIFEST.in` (#3552)
- Updating `author_email` in `setup.py` to `googleapis-publisher@google.com`.
  (#3598)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.26.0/
