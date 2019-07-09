# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dlp/#history

## 0.12.0

07-09-2019 13:20 PDT

### New Features
- Add support for publishing findings to GCS; deprecate 'DetectionRule' message (via synth). ([#8610](https://github.com/googleapis/google-cloud-python/pull/8610))
- Add 'client_options' support, update list method docstrings (via synth). ([#8507](https://github.com/googleapis/google-cloud-python/pull/8507))
- Allow kwargs to be passed to create_channel; expose support for AVRO files (via synth). ([#8443](https://github.com/googleapis/google-cloud-python/pull/8443))

### Internal / Testing Changes
- Pin black version (via synth). ([#8581](https://github.com/googleapis/google-cloud-python/pull/8581))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Update docstrings, format protos, update noxfile (via synth).  ([#8239](https://github.com/googleapis/google-cloud-python/pull/8239))
- Fix coverage in 'types.py' (via synth). ([#8153](https://github.com/googleapis/google-cloud-python/pull/8153))
- Blacken noxfile.py, setup.py (via synth). ([#8121](https://github.com/googleapis/google-cloud-python/pull/8121))
- Add empty lines (via synth). ([#8056](https://github.com/googleapis/google-cloud-python/pull/8056))
- Add nox session `docs`, reorder methods (via synth). ([#7769](https://github.com/googleapis/google-cloud-python/pull/7769))

## 0.11.0

04-15-2019 15:05 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7267](https://github.com/googleapis/google-cloud-python/pull/7267))
- Protoc-generated serialization update. ([#7081](https://github.com/googleapis/google-cloud-python/pull/7081))

### New Features
- Add support for filtering job triggers; add CryptoDeterministicConfig; update docs/conf.py. (via synth). ([#7390](https://github.com/googleapis/google-cloud-python/pull/7390))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Pick up stub docstring fix in GAPIC generator. ([#6969](https://github.com/googleapis/google-cloud-python/pull/6969))

### Internal / Testing Changes
- Copy in proto files. ([#7227](https://github.com/googleapis/google-cloud-python/pull/7227))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.10.0

12-17-2018 18:07 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6611](https://github.com/googleapis/google-cloud-python/pull/6611))
- Pick up fixes in GAPIC generator. ([#6495](https://github.com/googleapis/google-cloud-python/pull/6495))
- Fix `client_info` bug, update docstrings via synth. ([#6440](https://github.com/googleapis/google-cloud-python/pull/6440))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))

### New Features
- Add `BigQueryOptions.excluded_fields`. ([#6312](https://github.com/googleapis/google-cloud-python/pull/6312))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Pick up docstring fix via synth. ([#6874](https://github.com/googleapis/google-cloud-python/pull/6874))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6565](https://github.com/googleapis/google-cloud-python/pull/6565))

## 0.9.0

10-18-2018 10:44 PDT

### New Features

- Added `stored_info_type` methods to v2. ([#6221](https://github.com/googleapis/google-cloud-python/pull/6221))

### Documentation

- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))

### Internal / Testing Changes

- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Avoid replacing/scribbling on 'setup.py' during synth. ([#6125](https://github.com/googleapis/google-cloud-python/pull/6125))

## 0.8.0

### New Features
- Add support for exclude findings. ([#6091](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6091))
- Add support for stored info type support. ([#5950](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5950))

### Documentation
- Fix docs issue in DLP generation. ([#5668](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5668), [#5815](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5815))
- Docs: Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))

## 0.7.0

### New Features
- Add StoredInfoTypes (#5809)

## 0.6.0

### New Features
- Regenerate DLP v2 endpoint (redact image, delta presence) (#5666)

### Internal / Testing Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.5.0

### New Features
- Add PublishSummaryToCscc (#5246)
- Add configurable row limit (#5246)
- Add EntityID added to risk stats (#5246)
- Add dictionaries via GCS (#5246)

## 0.4.0

### Implementation Changes

- Remove DLP client version V2Beta1 (#5155)

## 0.3.0

### Implementation changes

- The library has been regenerated to pick up changes from the API's proto definition. (#5131)

## 0.2.0

### Interface additions

- Add DLP v2 (#5059)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Normalize all setup.py files (#4909)

## 0.1.0

Initial release of the DLP (Data Loss Prevention) client library. (#4879)


