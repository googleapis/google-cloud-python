# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dlp/#history

## 0.10.0

11-14-2018 11:34 PST


### Implementation Changes
- Pick up fixes in GAPIC generator. ([#6495](https://github.com/googleapis/google-cloud-python/pull/6495))
- Fix `client_info` bug, update docstrings via synth. ([#6440](https://github.com/googleapis/google-cloud-python/pull/6440))
- Add `BigQueryOptions.excluded_fields` via synth ([#6312](https://github.com/googleapis/google-cloud-python/pull/6312))

### Dependencies
- Bump minimum `api_core` version to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Internal / Testing Changes
- Remove now-spurious fixup from `synth.py` ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))

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


