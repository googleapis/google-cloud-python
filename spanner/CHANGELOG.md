# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-spanner/#history

## 1.13.0

11-11-2019 15:59 PST


### Implementation Changes
Fix TransactionPingingPool to stop thowing ''NoneType' object is not callable' error. ([#9609](https://github.com/googleapis/google-cloud-python/pull/9609))
Return sessions from pool in LIFO order. ([#9454](https://github.com/googleapis/google-cloud-python/pull/9454))

### Documentation
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Update description of the `timeout_secs` parameter. ([#9381](https://github.com/googleapis/google-cloud-python/pull/9381))

### Internal / Testing Changes
- Harden `test_transaction_batch_update*` systests against partial success + abort. ([#9579](https://github.com/googleapis/google-cloud-python/pull/9579))

## 1.12.0

10-23-2019 19:09 PDT


### Implementation Changes
- Add `batch_create_session` calls to session pools. ([#9488](https://github.com/googleapis/google-cloud-python/pull/9488))

### New Features
- Add `client_options` to client constructor. ([#9151](https://github.com/googleapis/google-cloud-python/pull/9151))

### Internal / Testing Changes
- Harden 'test_reload_instance' systest against eventual consistency failures. ([#9394](https://github.com/googleapis/google-cloud-python/pull/9394))
- Harden 'test_transaction_batch_update_w_syntax_error' systest. ([#9395](https://github.com/googleapis/google-cloud-python/pull/9395))
- Propagate errors from 'Transaction.batch_update' in systest. ([#9393](https://github.com/googleapis/google-cloud-python/pull/9393))

## 1.11.0

10-15-2019 06:55 PDT


### Implementation Changes
- Adjust gRPC timeouts (via synth). ([#9330](https://github.com/googleapis/google-cloud-python/pull/9330))
- Make `session_count` optional for `SpannerClient.batch_create_sessions` (via synth). ([#9280](https://github.com/googleapis/google-cloud-python/pull/9280))
- Remove send / receive message size limit, update docstrings (via synth). ([#8968](https://github.com/googleapis/google-cloud-python/pull/8968))

### New Features
- Add `batch_create_sessions` method to generated client (via synth). ([#9087](https://github.com/googleapis/google-cloud-python/pull/9087))

### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

### Documentation
- Remove references to old authentication credentials in docs. ([#9456](https://github.com/googleapis/google-cloud-python/pull/9456))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Fix `run_in_transaction` return value docs. ([#9264](https://github.com/googleapis/google-cloud-python/pull/9264))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Add DML insert and update examples to README. ([#8698](https://github.com/googleapis/google-cloud-python/pull/8698))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.10.0

07-24-2019 17:32 PDT


### Implementation Changes
- Add backoff for `run_in_transaction' when backend does not provide 'RetryInfo' in response. ([#8461](https://github.com/googleapis/google-cloud-python/pull/8461))
- Adjust gRPC timeouts (via synth). ([#8445](https://github.com/googleapis/google-cloud-python/pull/8445))
- Allow kwargs to be passed to create_channel (via synth). ([#8403](https://github.com/googleapis/google-cloud-python/pull/8403))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8659](https://github.com/googleapis/google-cloud-python/pull/8659))
- Add 'client_options' support, update list method docstrings (via synth). ([#8522](https://github.com/googleapis/google-cloud-python/pull/8522))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Fixes [#8545](https://github.com/googleapis/google-cloud-python/pull/8545) by removing typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8363](https://github.com/googleapis/google-cloud-python/pull/8363))
- Add disclaimer to auto-generated template files (via synth). ([#8327](https://github.com/googleapis/google-cloud-python/pull/8327))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8251](https://github.com/googleapis/google-cloud-python/pull/8251))
- Blacken noxfile.py, setup.py (via synth). ([#8131](https://github.com/googleapis/google-cloud-python/pull/8131))
- Harden synth replacement against template adding whitespace. ([#8103](https://github.com/googleapis/google-cloud-python/pull/8103))

## 1.9.0

05-16-2019 12:54 PDT


### Implementation Changes
- Add routing header to method metadata (via synth). ([#7750](https://github.com/googleapis/google-cloud-python/pull/7750))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to client. ([#7878](https://github.com/googleapis/google-cloud-python/pull/7878))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Expand API reference for snapshot / transaction. ([#7618](https://github.com/googleapis/google-cloud-python/pull/7618))

### Internal / Testing Changes
- Add nox session `docs`, remove retries for DEADLINE_EXCEEDED (via synth). ([#7781](https://github.com/googleapis/google-cloud-python/pull/7781))
- Added matching END tags to Spanner Tests ([#7529](https://github.com/googleapis/google-cloud-python/pull/7529))

## 1.8.0

03-05-2019 12:57 PST


### Implementation Changes
- Protoc-generated serialization update. ([#7095](https://github.com/googleapis/google-cloud-python/pull/7095))
- Fix typo in exported param type name. ([#7295](https://github.com/googleapis/google-cloud-python/pull/7295))

### New Features
- Add Batch DML support. ([#7485](https://github.com/googleapis/google-cloud-python/pull/7485))

### Documentation
- Copy lintified proto files, update docstrings (via synth). ([#7453](https://github.com/googleapis/google-cloud-python/pull/7453))
- Fix Batch object creation instructions. ([#7341](https://github.com/googleapis/google-cloud-python/pull/7341))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Fix README to install spanner instead of datastore. ([#7301](https://github.com/googleapis/google-cloud-python/pull/7301))

### Internal / Testing Changes
- Add clarifying comment to blacken nox target. ([#7403](https://github.com/googleapis/google-cloud-python/pull/7403))
- Ensure that GRPC config file is included in MANIFEST.in after templating. ([#7046](https://github.com/googleapis/google-cloud-python/pull/7046))
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers.

## 1.7.1

12-14-2018 15:18 PST


### Documentation
- Announce Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize documentation for 'page_size' / 'max_results' / 'page_token' ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

### Internal / Testing Changes
- Include grpc config in manifest ([#6928](https://github.com/googleapis/google-cloud-python/pull/6928))

## 1.7.0

12-10-2018 13:10 PST


### Implementation Changes
- Add PingingPool and TransactionPingingPool to toplevel module ([#6886](https://github.com/googleapis/google-cloud-python/pull/6886))
- Add `operation_id` parameter to `Database.update_ddl`. ([#6825](https://github.com/googleapis/google-cloud-python/pull/6825))
- Pick up changes to GAPIC method configuration ([#6615](https://github.com/googleapis/google-cloud-python/pull/6615))
- Add timeout + retry settings to Sessions/Snapshots ([#6536](https://github.com/googleapis/google-cloud-python/pull/6536))
- Pick up fixes to GAPIC generator. ([#6576](https://github.com/googleapis/google-cloud-python/pull/6576))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Blacken. ([#6846](https://github.com/googleapis/google-cloud-python/pull/6846))
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add tags to DML system tests ([#6580](https://github.com/googleapis/google-cloud-python/pull/6580))

## 1.6.1

11-09-2018 14:49 PST

### Implementation Changes
- Fix client_info bug, update docstrings. ([#6420](https://github.com/googleapis/google-cloud-python/pull/6420))

### Documentation
- Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Fix typo in spanner usage documentation ([#6209](https://github.com/googleapis/google-cloud-python/pull/6209))

### Internal / Testing Changes
- Rationalize 'all_types' round-trip systest ([#6379](https://github.com/googleapis/google-cloud-python/pull/6379))
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Add systest for returning empty array struct ([#4449](https://github.com/googleapis/google-cloud-python/pull/4449))
- Add systests not needing tables ([#6308](https://github.com/googleapis/google-cloud-python/pull/6308))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 1.6.0

10-08-2018 08:25 PDT

### New Features
- Add support for DML/PDML. ([#6151](https://github.com/googleapis/google-cloud-python/pull/6151))

### Implementation Changes
- Add 'synth.py' and regen GAPIC code. ([#6040](https://github.com/googleapis/google-cloud-python/pull/6040))

### Documentation
- Remove invalid examples of `database.transaction()`. ([#6032](https://github.com/googleapis/google-cloud-python/pull/6032))
- Redirect renamed `usage.html`/`client.html` -> `index.html`. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Fix leakage of sections into sidebar menu. ([#5986](https://github.com/googleapis/google-cloud-python/pull/5986))
- Prepare documentation for repo split. ([#5938](https://github.com/googleapis/google-cloud-python/pull/5938))

### Internal / Testing Changes
- Remove extra `grpc_gcp` system tests. ([#6049](https://github.com/googleapis/google-cloud-python/pull/6049))

## 1.5.0

### New Features

- Add support for session / pool labels ([#5734](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5734))
- Add support for gRPC connection management ([#5553](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5553))

### Dependencies

- Add `grpcio-gcp` dependency for Cloud Spanner ([#5904](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5904))

### Internal / Testing Changes

- Don't hardcode endpoint URL in grpc_gcp unit tests. ([#5893](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5893))
- Run `grpc_gcp` unit tests only with Python 2.7 / 3.6. ([#5871](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5871))
- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))
- Benchmarks: print() is a function in Python 3 ([#5862](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5862))
- Retry `test_transaction_read_and_insert_then_rollback` when aborted. ([#5737](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5737))
- Skip the flaky `test_update_database_ddl` systest. ([#5704](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5704))

## 1.4.0

### Implementation Changes
- Ensure that initial resume token is bytes, not text. (#5450)
- Prevent process_read_batch from mutating params (#5416)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Add support for Python 3.7 (#5288)
- Add support for Spanner struct params. (#5463)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)

## 1.3.0

### Interface additions

- Added `spanner_v1.COMMIT_TIMESTAMP`. (#5102)

## 1.2.0

### New features

- Added batch query support (#4938)

### Implementation changes

- Removed custom timestamp class in favor of the one in google-api-core. (#4980)

### Dependencies

- Update minimum version for google-api-core to 1.1.0 (#5030)

### Documentation

- Update package metadata release status to 'Stable' (#5031)

## 1.1.0

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Testing and internal changes

- Fix load_keys() in YCSB-like benchmark for cloud spanner. (#4919)
- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix system test util to populate streaming (#4888)
- Retry conflict errors in system test (#4850)

## 1.0.0

### Breaking Changes

- `to_pb` has now been made private (`_to_pb`) in `KeySet`
  and `KeyRange` (#4740)

### Documentation Changes
- Database update_ddl missing param in documentation (#4749)

## 0.30.0

### Breaking Changes

- The underlying autogenerated client library was re-generated to pick up new 
  features and resolve bugs, this may change the exceptions raised from various
  methods. (#4695)
- Made `StreamedResultSet`'s `row`, `consume_all`, and `consume_next` members
  private (#4492)

### Implementation Changes

- `Keyset` can now infer defaults to `start_closed` or `end_closed` when only one argument is specified. (#4735)

### Documentation

- Brought Spanner README more in line with others. (#4306, #4317)

### Testing

- Added several new system tests and fixed minor issues with existing tests. (
  #4631, #4569, #4573, #4572, #4416, #4411, #4407, #4386, #4419, #4489,
  #4678, #4620, #4418, #4403, #4397, #4383, #4371, #4372, #4374, #4370, #4285,
  #4321)
- Excluded generated code from linting. (#4375)
- Added a `nox -s default` session for all packages. (#4324)

## 0.29.0

### Implementation Changes

- **Bugfix**: Clear `session._transaction` before calling
  `_delay_until_retry` (#4185)
- **Bugfix**: Be permissive about merging an empty list. (#4170,
  fixes #4164)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-spanner/0.29.0/
