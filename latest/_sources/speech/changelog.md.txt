# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-speech/#history

## 1.0.0

03-18-2019 08:05 PDT


### Implementation Changes
- Remove unused message exports. ([#7275](https://github.com/googleapis/google-cloud-python/pull/7275))

### New Features
- Promote google-cloud-speech to GA ([#7525](https://github.com/googleapis/google-cloud-python/pull/7525))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes
- Speech: copy lintified proto files (via synth).
- Add clarifying comment to blacken nox target. ([#7404](https://github.com/googleapis/google-cloud-python/pull/7404))
- Copy proto files alongside protoc versions. Remove unneeded utf-8 header.

## 0.36.3

01-31-2019 09:57 PST


### New Features
- Add 'RecognitionConfig.audio_channel_count' field via synth. ([#7240](https://github.com/googleapis/google-cloud-python/pull/7240))

### Documentation
- Modify file headers. ([#7158](https://github.com/googleapis/google-cloud-python/pull/7158))

### Internal / Testing Changes
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.36.2

01-10-2019 15:36 PST

### Implementation Changes
- Protoc-generated serialization update. ([#7106](https://github.com/googleapis/google-cloud-python/pull/7106))

### Documentation
- Regenerate speech to change quote chars in docstr.
- Pick up stub docstring fix in GAPIC generator. ([#6982](https://github.com/googleapis/google-cloud-python/pull/6982))

## 0.36.1

12-18-2018 09:46 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAIPC generator. ([#6508](https://github.com/googleapis/google-cloud-python/pull/6508))
- Add `result_end_time`, docstring changes via synth. ([#6462](https://github.com/googleapis/google-cloud-python/pull/6462))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings and timeouts. ([#6421](https://github.com/googleapis/google-cloud-python/pull/6421))
- Re-generate library using speech/synth.py ([#5979](https://github.com/googleapis/google-cloud-python/pull/5979))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Clarify passed arguments in speech examples. ([#6857](https://github.com/googleapis/google-cloud-python/pull/6857))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Fix client library URL. ([#6052](https://github.com/googleapis/google-cloud-python/pull/6052))
- Prep docs for repo split. ([#6017](https://github.com/googleapis/google-cloud-python/pull/6017))

### Internal / Testing Changes
- Synth.metadata. ([#6868](https://github.com/googleapis/google-cloud-python/pull/6868))
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.36.0

### New Features

- Re-generate the library to pick up changes and new features in the underlying API. ([#5915](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5915))

### Documentation

- Fix broken links to description of 'Beta' ([#5917](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5917))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))

## 0.35.0

### Implementation Changes

- Re-generated the library to pick up new API features. (#5577)

### Internal / Testing Changes

- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.34.0

### Implementation Changes
- Regenerate GAPIC to account for the removal of GoogleDataCollectionConfig and google_data_collection_opt_in  (#5235)

## 0.33.0

### New Features

- Add Audio Logging and Recognition Metadata. (#5123)

### Internal / Testing Changes

- Fix bad trove classifier

## 0.32.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)

## 0.31.1

### Bugfixes

- Fix speech helpers to properly pass retry and timeout args. (#4828, #4830)

## 0.31.0

This is the (hopefully) final release candidate before 1.0.

### Breaking Changes

- The deprecated Speech layer (deprecated since 0.27.0) has been removed. If you are still using  it, the [migration guide](https://cloud.google.com/speech/docs/python-client-migration) is still available.
- The following changes are _technically_ breaking but very unlikely to affect you directly:
  * `google.cloud.gapic.speech.v1` moved to `google.cloud.speech_v1.gapic`, in accordance with more recent clients.
  * `google.cloud.proto.speech.v1` moved to `google.cloud.speech_v1.proto`, in accordance with more recent clients.

### Dependencies

  * Removed dependency on `google-gax`.
  * Added dependency on `google-api-core`, its replacement.

## 0.30.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-speech/0.30.0/
