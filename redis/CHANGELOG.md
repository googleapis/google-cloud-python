# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-redis/#history

## 0.2.1

12-18-2018 09:40 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6504](https://github.com/googleapis/google-cloud-python/pull/6504))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings. ([#6419](https://github.com/googleapis/google-cloud-python/pull/6419))
- Re-generate library using redis/synth.py ([#6016](https://github.com/googleapis/google-cloud-python/pull/6016))
- Re-generate library using redis/synth.py ([#5993](https://github.com/googleapis/google-cloud-python/pull/5993))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Don't synth 'README.rst'. ([#6262](https://github.com/googleapis/google-cloud-python/pull/6262))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.2.0

### New Features

- Add the v1 API client library. ([#5945](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5945))

### Documentation

- Docs: Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))
- Redis: Fix README.md links ([#5745](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5745))
- Add redis documentation to main index.rst ([#5405](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5405))

### Internal / Testing Changes

- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5364))
- Unit tests require grpcio. ([#5363](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5363))

## 0.1.0

### New Features
Initial version of Redis client library v1beta1.

