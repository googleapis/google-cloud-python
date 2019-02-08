# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-texttospeech/#history

## 0.4.0

02-07-2019 15:21 PST


### Implementation Changes
- Pick up stub docstring fix in GAPIC generator. ([#6984](https://github.com/googleapis/google-cloud-python/pull/6984))

### New Features
- Protoc updates to include effects_profile_id. ([#7097](https://github.com/googleapis/google-cloud-python/pull/7097))

### Documentation
- Fix `Client Library Documentation` link ([#7109](https://github.com/googleapis/google-cloud-python/pull/7109))

### Internal / Testing Changes
- Copy proto files alongside protoc versions.
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers and docstring quoting

## 0.3.0

12-18-2018 09:54 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6510](https://github.com/googleapis/google-cloud-python/pull/6510))
- Fix `client_info` bug, update docstrings. ([#6423](https://github.com/googleapis/google-cloud-python/pull/6423))
- Re-generate library using texttospeech/synth.py ([#5981](https://github.com/googleapis/google-cloud-python/pull/5981))
- Add gRPC Transport layer. ([#5959](https://github.com/googleapis/google-cloud-python/pull/5959))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Docs: Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))
- Fix docs links for TTS. ([#5483](https://github.com/googleapis/google-cloud-python/pull/5483))

### Internal / Testing Changes
- Add synth.metadata. ([#6870](https://github.com/googleapis/google-cloud-python/pull/6870))
- Update noxfile.
- blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.2.0

### New Features

- Add the text-to-speech v1 API surface. (#5468)
- Re-generate the text-to-speech v1beta1 API surface. (#5468)

### Documentation

- Rename releases to changelog and include from CHANGELOG.md (#5191)

### Internal / Testing Changes

- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 0.1.0

### Interface additions

- Added text-to-speech v1beta1. (#5049)

