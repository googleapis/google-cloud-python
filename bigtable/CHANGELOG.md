# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigtable/#history

## 1.0.0

08-28-2019 12:49 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8979](https://github.com/googleapis/google-cloud-python/pull/8979))

### Documentation
- Avoid creating table in 'list_tables' snippet; harden 'delete_instance' snippet. ([#8879](https://github.com/googleapis/google-cloud-python/pull/8879))
- Add retry for DeadlineExceeded to 'test_bigtable_create_table' snippet. ([#8889](https://github.com/googleapis/google-cloud-python/pull/8889))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Docs: Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 0.34.0

07-30-2019 10:05 PDT


### Implementation Changes
- Pick up changes to GAPIC client configuration (via synth). ([#8724](https://github.com/googleapis/google-cloud-python/pull/8724))
- Add `Cell.__repr__`. ([#8683](https://github.com/googleapis/google-cloud-python/pull/8683))
- Increase timeout for app profile update operation. ([#8417](https://github.com/googleapis/google-cloud-python/pull/8417))

### New Features
- Add methods returning Separate row types to remove confusion around return types of `row.commit`. ([#8662](https://github.com/googleapis/google-cloud-python/pull/8662))
- Add `options_` argument to clients' `get_iam_policy` (via synth). ([#8652](https://github.com/googleapis/google-cloud-python/pull/8652))
-  Add `client_options` support, update list method docstrings (via synth). ([#8500](https://github.com/googleapis/google-cloud-python/pull/8500))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for `grpc-google-iam-v1` to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))
- Allow kwargs to be passed to `create_channel` (via synth). ([#8458](https://github.com/googleapis/google-cloud-python/pull/8458))
- Add `PartialRowsData.cancel`. ([#8176](https://github.com/googleapis/google-cloud-python/pull/8176))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Add snppets illustrating use of  application profiles. ([#7033](https://github.com/googleapis/google-cloud-python/pull/7033))

### Internal / Testing Changes
- Add nox session `docs` to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Force timeout for table creation to 90 seconds (in systests). ([#8450](https://github.com/googleapis/google-cloud-python/pull/8450))
- Plug systest / snippet instance leaks. ([#8416](https://github.com/googleapis/google-cloud-python/pull/8416))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8346](https://github.com/googleapis/google-cloud-python/pull/8346))
- Add disclaimer to auto-generated template files (via synth).  ([#8308](https://github.com/googleapis/google-cloud-python/pull/8308))
- Fix coverage in `types.py` (via synth). ([#8149](https://github.com/googleapis/google-cloud-python/pull/8149))
- Integrate docstring / formatting tweaks (via synth). ([#8138](https://github.com/googleapis/google-cloud-python/pull/8138))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

## 0.33.0

05-16-2019 11:51 PDT


### Implementation Changes
- Fix typos in deprecation warnings. ([#7858](https://github.com/googleapis/google-cloud-python/pull/7858))
- Add deprecation warnings for to-be-removed features. ([#7532](https://github.com/googleapis/google-cloud-python/pull/7532))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Improve `Policy` interchange w/ JSON, gRPC payloads. ([#7378](https://github.com/googleapis/google-cloud-python/pull/7378))

### New Features
- Add support for passing `client_info` to client. ([#7876](https://github.com/googleapis/google-cloud-python/pull/7876)) and ([#7898](https://github.com/googleapis/google-cloud-python/pull/7898))
- Add `Table.mutation_timeout`, allowing override of config timeouts. ([#7424](https://github.com/googleapis/google-cloud-python/pull/7424))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Remove duplicate snippet tags for Delete cluster. ([#7860](https://github.com/googleapis/google-cloud-python/pull/7860))
- Fix rendering of instance admin snippets. ([#7797](https://github.com/googleapis/google-cloud-python/pull/7797))
- Avoid leaking instances from snippets. ([#7800](https://github.com/googleapis/google-cloud-python/pull/7800))
- Fix enum reference in documentation. ([#7724](https://github.com/googleapis/google-cloud-python/pull/7724))
- Remove duplicate snippets. ([#7528](https://github.com/googleapis/google-cloud-python/pull/7528))
- Add snippeds for Batcher, RowData, Row Operations, AppendRow. ([#7019](https://github.com/googleapis/google-cloud-python/pull/7019))
- Add column family snippets. ([#7014](https://github.com/googleapis/google-cloud-python/pull/7014))
- Add Row Set snippets. ([#7016](https://github.com/googleapis/google-cloud-python/pull/7016))
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Fix typos in Table docstrings. ([#7261](https://github.com/googleapis/google-cloud-python/pull/7261))
- Update copyright headers (via synth). ([#7139](https://github.com/googleapis/google-cloud-python/pull/7139))
- Fix linked classes in generated docstrings (via synth). ([#7060](https://github.com/googleapis/google-cloud-python/pull/7060))

### Internal / Testing Changes
- Run `instance_admin` system tests on a separate instance from `table_admin` and `data` system tests. ([#6579](https://github.com/googleapis/google-cloud-python/pull/6579))
- Re-blacken. ([#7462](https://github.com/googleapis/google-cloud-python/pull/7462))
- Copy lintified proto files (via synth). ([#7445](https://github.com/googleapis/google-cloud-python/pull/7445))
- Remove unused message exports (via synth). ([#7264](https://github.com/googleapis/google-cloud-python/pull/7264))
- Compare 0 using '!=', rather than 'is not'. ([#7312](https://github.com/googleapis/google-cloud-python/pull/7312))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Protoc-generated serialization update. ([#7077](https://github.com/googleapis/google-cloud-python/pull/7077))
- Blacken snippets. ([#7048](https://github.com/googleapis/google-cloud-python/pull/7048))
- Bigtable client snippets ([#7020](https://github.com/googleapis/google-cloud-python/pull/7020))
- Pick up order-of-enum fix from GAPIC generator. ([#6879](https://github.com/googleapis/google-cloud-python/pull/6879))
- Plug systest instance leaks ([#7004](https://github.com/googleapis/google-cloud-python/pull/7004))

## 0.32.1

12-17-2018 16:38 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Add snippets for table operations. ([#6484](https://github.com/googleapis/google-cloud-python/pull/6484))

## 0.32.0

12-10-2018 12:47 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Remove `deepcopy` from `PartialRowData.cells` property. ([#6648](https://github.com/googleapis/google-cloud-python/pull/6648))
- Pick up fixes to GAPIC generator. ([#6630](https://github.com/googleapis/google-cloud-python/pull/6630))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 0.31.1

11-02-2018 08:13 PDT

### Implementation Changes
- Fix anonymous usage under Bigtable emulator ([#6385](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6385))
- Support `DirectRow` without a `Table` ([#6336](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6336))
- Add retry parameter to `Table.read_rows()`. ([#6281](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6281))
- Fix `ConditionalRow` interaction with `check_and_mutate_row` ([#6296](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6296))
- Deprecate `channel` arg to `Client` ([#6279](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6279))

### Dependencies
- Update dependency: `google-api-core >= 1.4.1` ([#6391](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6391))
- Update IAM version in dependencies ([#6362](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6362))

### Documentation
- Add `docs/snippets.py` and test ([#6012](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6012))
- Normalize use of support level badges ([#6159](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Fix client_info bug, update docstrings and timeouts. ([#6406)](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6406))
- Remove now-spurious fixup from 'synth.py'. ([#6400](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6400))
- Fix flaky systests / snippets ([#6367](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6367))
- Add explicit coverage for `row_data._retry_read_rows_exception`. ([#6364](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6364))
- Fix instance IAM test methods ([#6343](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6343))
- Fix error from new flake8 version. ([#6309](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6309))
- Use new Nox ([#6175](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6175))

## 0.31.0

### New Features
- Upgrade support level from `alpha` to `beta`.  ([#6129](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6129))

### Implementation Changes
- Improve admin operation timeouts. ([#6010](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6010))

### Documentation
- Prepare docs for repo split. ([#6014](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6014))

### Internal / Testing Changes
- Refactor `read_row` to call `read_rows` ([#6137](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6102))
- Harden instance teardown against '429 Too Many Requests'. ([#6102](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6102))
- Add `{RowSet,RowRange}.{__eq__,.__ne__}` ([#6025](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6025))
- Regenerate low-level GAPIC code ([#6036](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6036))

## 0.30.2

### New Features
- Add iam policy implementation for an instance. (#5838)

### Implementation Changes
- Fix smart retries for 'read_rows()' when reading the full table (#5966)

### Documentation
- Replace links to `/stable/` with `/latest/`. (#5901)

### Internal / Testing Changes
- Re-generate library using bigtable/synth.py (#5974)
- Refactor `read_rows` infrastructure (#5963)

## 0.30.1

### Implementation changes

- Fix non-admin access to table data. (#5875)
- Synth bigtable and bigtable admin GAPIC clients. (#5867)

### Testing and internal changes

- Nox: use in-place installs for local packages. (#5865)

## 0.30.0

### New Features

- Improve performance and capabilities of reads.  `read_rows` now returns a generator; has automatic retries; and can read an arbitrary set of keys and ranges
  - Consolidate read_rows and yield_rows (#5840)
  - Implement row set for yield_rows  (#5506)
  - Improve read rows validation performance (#5390)
  - Add retry for yield_rows (#4882)
  - Require TimestampRanges to be milliseconds granularity (#5002)
  - Provide better access to cell values (#4908)
  - Add data app profile id  (#5369)

- Improve writes: Writes are usable in Beam
  - Create MutationBatcher for bigtable (#5651)
  - Allow DirectRow to be created without a table (#5567)
  - Add data app profile id  (#5369)

- Improve table admin: Table creation now can also create families in a single RPC.  Add an `exist()` method.  Add `get_cluster_states` for information about replication
  - Add 'Table.get_cluster_states' method (#5790)
  - Optimize 'Table.exists' performance (#5749)
  - Add column creation in 'Table.create()'. (#5576)
  - Add 'Table.exists' method (#5545)
  - Add split keys on create table - v2 (#5513)
  - Avoid sharing table names across unrelated systests. (#5421)
  - Add truncate table and drop by prefix on top of GAPIC integration (#5360)

- Improve instance admin: Instance creation allows for the creation of multiple clusters.  Instance label management is now enabled.  
  - Create app_profile_object (#5782)
  - Add 'Instance.exists' method (#5802)
  - Add 'InstanceAdminClient.list_clusters' method (#5715)
  - Add 'Instance._state' property (#5736)
  - Convert 'instance.labels' to return a dictionary (#5728)
  - Reshape cluster.py, adding cluster() factory to instance.py (#5663)
  - Convert 'Instance.update' to use 'instance.partial_instance_update' API (#5643)
  - Refactor 'InstanceAdminClient.update_app_profile' to remove update_mask argument (#5684)
  - Add the ability to create an instance with multiple clusters (#5622)
  - Add 'instance_type', 'labels' to 'Instance' ctor (#5614)
  - Add optional app profile to 'Instance.table' (#5605)
  - Clean up Instance creation. (#5542)
  - Make 'InstanceAdminClient.list_instances' return actual instance objects, not protos. (#5420)
  - Add admin app profile methods on Instance (#5315)

### Internal / Testing Changes
- Rename releases to changelog and include from CHANGELOG.md (#5191)
- Fix bad trove classifier
- Integrate new generated low-level client (#5178)
- Override gRPC max message lengths. (#5498)
- Use client properties rather than private attrs (#5398)
- Fix the broken Bigtable system test. (#5607)
- Fix Py3 breakage in new system test. (#5474)
- Modify system test for new GAPIC code (#5302)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Disable Bigtable system tests (#5381)
- Modify system tests to use prerelease versions of grpcio (#5304)
- Pass through 'session.posargs' when running Bigtable system tests. (#5418)
- Harden 'test_list_instances' against simultaneous test runs. (#5476)
- Shorten instance / cluster name to fix CI breakage. (#5641)
- Fix failing systest: 'test_create_instance_w_two_clusters'. (#5836)
- Add labels {'python-system': ISO-timestamp} to systest instances (#5729)
- Shorten cluster ID in system test (#5719)
- Harden 'test_list_instances' further. (#5696)
- Improve testing of create instance (#5544)

## 0.29.0

### New features

- Use `api_core.retry` for `mutate_row` (#4665, #4341)
- Added a row generator on a table. (#4679)

### Implementation changes

- Remove gax usage from BigTable (#4873)
- BigTable: Cell.from_pb() performance improvement (#4745)

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Minor typo (#4758)
- Row filter end points documentation error (#4667)
- Removing "rename" from bigtable table.py comments (#4526)
- Small docs/hygiene tweaks after #4256. (#4333)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Timestamp system test fix (#4765)

## 0.28.1

### Implementation Changes

- Bugfix: Distinguish between an unset column qualifier and an empty string
  column qualifier while parsing a `ReadRows` response (#4252)

### Features added

- Add a ``retry`` strategy that will be used for retry-able errors
  in ``Table.mutate_rows``. This will be used for gRPC errors of type
  ``ABORTED``, ``DEADLINE_EXCEEDED`` and ``SERVICE_UNAVAILABLE``. (#4256)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.1/

## 0.28.0

### Documentation

- Fixed referenced types in `Table.row` docstring (#3934, h/t to
  @MichaelTamm)
- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.0/
