# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-logging/#history

### [1.15.1](https://www.github.com/googleapis/python-logging/compare/v1.15.0...v1.15.1) (2020-07-01)


### Documentation

* add initialization of LogEntry instance in the v2 example ([#46](https://www.github.com/googleapis/python-logging/issues/46)) ([251ac93](https://www.github.com/googleapis/python-logging/commit/251ac9355b192121572552c1c9cfd4df94a42802)), closes [#44](https://www.github.com/googleapis/python-logging/issues/44)
* change descriptions for virtual environment ([#48](https://www.github.com/googleapis/python-logging/issues/48)) ([c5c3c15](https://www.github.com/googleapis/python-logging/commit/c5c3c153d1ae91f44c4104279baae9d9e4f88d03)), closes [#47](https://www.github.com/googleapis/python-logging/issues/47)

## [1.15.0](https://www.github.com/googleapis/python-logging/compare/v1.14.0...v1.15.0) (2020-02-26)


### Features

* add support for cmek settings; undeprecate resource name helper methods; bump copyright year to 2020 ([#22](https://www.github.com/googleapis/python-logging/issues/22)) ([1c687c1](https://www.github.com/googleapis/python-logging/commit/1c687c168cdc1f5ebc74d2380ad87335a42209a2))


### Bug Fixes

* **logging:** deprecate resource name helper methods (via synth) ([#9837](https://www.github.com/googleapis/python-logging/issues/9837)) ([335af9e](https://www.github.com/googleapis/python-logging/commit/335af9e909eb7fb4696ba906a82176611653531d))
* **logging:** update test assertion and core version pins ([#10087](https://www.github.com/googleapis/python-logging/issues/10087)) ([4aedea8](https://www.github.com/googleapis/python-logging/commit/4aedea80e2bccb5ba3c41fae7a0ee46cc07eefa9))
* replace unsafe six.PY3 with PY2 for better future compatibility with Python 4 ([#10081](https://www.github.com/googleapis/python-logging/issues/10081)) ([c6eb601](https://www.github.com/googleapis/python-logging/commit/c6eb60179d674dfd5137d90d209094c9369b3581))

## 1.14.0

10-15-2019 06:50 PDT


### Implementation Changes
- Fix proto copy. ([#9420](https://github.com/googleapis/google-cloud-python/pull/9420))

### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

## 1.13.0

09-23-2019 10:00 PDT

### Implementation Changes
- Pass 'stream' argument to super in 'ContainerEngineHandler.__init__'. ([#9166](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9166))

### New Features
- Add LoggingV2Servicer, LogSinks, logging_metrics, and log_entry. Add LogSeverity and HttpRequest types (via synth). ([#9262](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9262))
- Add client_options to logging v1 ([#9046](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9046))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Docs: Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9085))
- Delete custom synth removing gRPC send/recv msg size limits. ([#8939](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8939))

## 1.12.1

08-01-2019 09:45 PDT


### Implementation Changes
- Remove gRPC size restrictions (4MB default) ([#8860](https://github.com/googleapis/google-cloud-python/pull/8860))
- Map stdlib loglevels to Cloud Logging severity enum values. ([#8837](https://github.com/googleapis/google-cloud-python/pull/8837))

### Documentation
- Fix 'list_entries' example with projects. ([#8858](https://github.com/googleapis/google-cloud-python/pull/8858))

### Internal / Testing Changes
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.12.0

07-24-2019 16:47 PDT


### Implementation Changes
- Set the 'timestamp' on log records created by handler. ([#8227](https://github.com/googleapis/google-cloud-python/pull/8227))
- Clarify worker thread implementation. ([#8228](https://github.com/googleapis/google-cloud-python/pull/8228))

### New Features
- Add path-construction helpers to GAPIC clients (via synth). ([#8631](https://github.com/googleapis/google-cloud-python/pull/8631))
- Add 'client_options' support, update list method docstrings (via synth). ([#8535](https://github.com/googleapis/google-cloud-python/pull/8535))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Re-add "generated" markers (via synth). ([#8538](https://github.com/googleapis/google-cloud-python/pull/8538))
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Fix tests broken in PR [#8227](https://github.com/googleapis/google-cloud-python/pull/8227). ([#8273](https://github.com/googleapis/google-cloud-python/pull/8273))
- Add empty lines. ([#8064](https://github.com/googleapis/google-cloud-python/pull/8064))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

## 1.11.0

05-16-2019 12:27 PDT


### Implementation Changes
- Add routing header to method metadata (via synth). ([#7598](https://github.com/googleapis/google-cloud-python/pull/7598))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Use FQDN for GCE metadata endpoint. ([#7520](https://github.com/googleapis/google-cloud-python/pull/7520))

### New Features
- Add `client_info` support to client. ([#7874](https://github.com/googleapis/google-cloud-python/pull/7874)) and ([#7901](https://github.com/googleapis/google-cloud-python/pull/7901))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Reformat snippet (via synth). ([#7216](https://github.com/googleapis/google-cloud-python/pull/7216))
- Add snippet for logging a resource. ([#7212](https://github.com/googleapis/google-cloud-python/pull/7212))

### Internal / Testing Changes
- Reorder methods in file (via synth). ([#7810](https://github.com/googleapis/google-cloud-python/pull/7810))
- Copy lintified proto files (via synth). ([#7450](https://github.com/googleapis/google-cloud-python/pull/7450))
- Trivial gapic-generator change. ([#7230](https://github.com/googleapis/google-cloud-python/pull/7230))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 1.10.0

01-17-2019 15:37 PST


### Implementation Changes
- Change WriteLogEntries retry policy.
- Protoc-generated serialization update. ([#7088](https://github.com/googleapis/google-cloud-python/pull/7088))
- GAPIC generation fixes. ([#7061](https://github.com/googleapis/google-cloud-python/pull/7061))

### Internal / Testing Changes
- Update copyright headers.
- Use 'python-3.6' for 'blacken' run. ([#7064](https://github.com/googleapis/google-cloud-python/pull/7064))

## 1.9.1

12-17-2018 16:49 PST


### Implementation Changes
- Allow setting name, args on default handler (post-blacken) ([#6828](https://github.com/googleapis/google-cloud-python/pull/6828))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 1.9.0

12-10-2018 12:55 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6631](https://github.com/googleapis/google-cloud-python/pull/6631))
- Fix `client_info` bug, update docstrings via synth. ([#6435](https://github.com/googleapis/google-cloud-python/pull/6435))
- Revert "Allow turning on JSON Detection in StackDriver" ([#6352](https://github.com/googleapis/google-cloud-python/pull/6352))
- Allow turning on JSON Detection in StackDriver ([#6293](https://github.com/googleapis/google-cloud-python/pull/6293))

### New Features
- Add support for additional 'LogEntry' fields ([#6229](https://github.com/googleapis/google-cloud-python/pull/6229))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))


### Internal / Testing Changes
- Change the url to the canonical one ([#6843](https://github.com/googleapis/google-cloud-python/pull/6843))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Logging: add 'synth.py'. ([#6081](https://github.com/googleapis/google-cloud-python/pull/6081))

## 1.8.0

10-17-2018 14:23 PDT

### Implementation Changes

- Logging:  allow more tries on inner retry for '_list_entries'. ([#6179](https://github.com/googleapis/google-cloud-python/pull/6179))
- Accommodate payload-less log entries. ([#6103](https://github.com/googleapis/google-cloud-python/pull/6103))

### New Features

- Logging: support request-correlated logging in App Engine standard python37 runtime ([#6118](https://github.com/googleapis/google-cloud-python/pull/6118))

### Documentation

- Logging: fix class reference in docstring ([#6153](https://github.com/googleapis/google-cloud-python/pull/6153))
- Translate / Logging / Language: restore detailed usage docs. ([#5999](https://github.com/googleapis/google-cloud-python/pull/5999))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))

### Internal / Testing Changes

- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Logging: harden systest teardown against 'DeadlineExceeded' retry errors. ([#6182](https://github.com/googleapis/google-cloud-python/pull/6182))
- Logging: fix lint errors. ([#6183](https://github.com/googleapis/google-cloud-python/pull/6183))
- Harden sink / metric creation against transient errors. ([#6180](https://github.com/googleapis/google-cloud-python/pull/6180))
- Logging: test both GCLOUD_PROJECT and GOOGLE_CLOUD_PROJECT env vars ([#6138](https://github.com/googleapis/google-cloud-python/pull/6138))
- Harden 'test_list_entry_with_unregistered' against 429 errors. ([#6181](https://github.com/googleapis/google-cloud-python/pull/6181))
- Prep logging docs for repo split. ([#5943](https://github.com/googleapis/google-cloud-python/pull/5943))

## 1.7.0

### Implementation Changes
- Print to stderr instead of stdout when exiting the program ([#5569](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5569))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5364))
- Support older Django versions in request middleware [#5024](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5024)
- Fix bad trove classifier [#5386](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5386)

### New Features
- Add support for `trace` and `span_id` to logging async API ([#5908](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5908))
- Add support for `span_id` attribute of log entries ([#5885](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5885))
- Add support for `trace` attribute of log entries ([#5878](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5878))
- Add support for Python 3.7 and remove 3.4 ([#5295](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5295))

### Documentation
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))
- Unflake logging systests ([#5698](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5698))
- Harden `_list_entries` system test further against backoff failure. ([#5551](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5551))
- Harden logging systests ([#5496](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5496))
- Harden system tests against 'ResourceExhausted' quota errors. ([#5486](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5486))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5304))
- Plug leaky sink in systests. ([#5247](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5247))

## 1.6.0

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)

## 1.5.0

### New features

- Added `max_latency` to `BackgroundThreadTransport`. (#4762)
- Added support for unique writer identity in `Sink`. (#4595, #4708, #4704, #4706)

### Implementation changes

- The underlying auto-generated client library was re-generated to pick up new features and bugfixes. (#4759)
- Moved the code path of `get_gae_labels()` to `emit()`. (#4824)
- Removed a debug print statement. (#4838)
- `LogSink.create` captures the server-generated `writerIdentity`. (#4707)
- Accomodated a back-end change making `Sink.filter` optional. (#4699)

### Testing

- Fixed system tests (#4768)
- Hardened test for `retrieve_metadata_server` against transparent DNS proxies. (#4698)
- Added cleanup for Pub / Sub topic in logging system test. (#4532)
- Added another check for Python 2.7 in Logging `nox -s default`. (#4523)
- Pinned `django` test dependency to `< 2.0` in Python 2.7. (#4519)
- Maked a `nox -s default` session for all packages. (#4324)
- Shortened test names. (#4321)

### Documentation

- Added doc to highlight missing `uniqueWriterIdentity` field. (#4579)
- Fixing "Fore" -> "For" typo in README docs. (#4317)

## 1.4.0

### Implementation Changes

- Remove `deepcopy` of `Client._http` in background transport (#3954)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-logging/1.4.0/
