# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-logging/#history

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
