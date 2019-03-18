# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-securitycenter/#history

## 0.2.0

03-12-2019 17:09 PDT


### Implementation Changes
- Remove 'having' filter arguments from query methods (via synth). [#7511](https://github.com/googleapis/google-cloud-python/pull/7511))
- Remove unused message exports. ([#7274](https://github.com/googleapis/google-cloud-python/pull/7274))
- Trivial gapic-generator change. ([#7233](https://github.com/googleapis/google-cloud-python/pull/7233))
- Protoc-generated serialization update, docstring tweak. ([#7094](https://github.com/googleapis/google-cloud-python/pull/7094))

### New Features
- Add support for `v1` API. ([#7495](https://github.com/googleapis/google-cloud-python/pull/7495))

### Documentation
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Docstring update from .proto file. ([#7056](https://github.com/googleapis/google-cloud-python/pull/7056))
- Fix 404 for 'Client Library Documentation' link. ([#7041](https://github.com/googleapis/google-cloud-python/pull/7041))
- Pick up stub docstring fix in GAPIC generator. ([#6981](https://github.com/googleapis/google-cloud-python/pull/6981))

### Internal / Testing Changes
- Proto file housekeeping FBO C# (via synth). ([#7502](https://github.com/googleapis/google-cloud-python/pull/7502))
- Copy lintified proto files (via synth). ([#7470](https://github.com/googleapis/google-cloud-python/pull/7470))
- Add clarifying comment to blacken nox target. ([#7402](https://github.com/googleapis/google-cloud-python/pull/7402))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.1

12-18-2018 09:45 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up changes to GAPIC generator. ([#6506](https://github.com/googleapis/google-cloud-python/pull/6506))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings via synth. ([#6438](https://github.com/googleapis/google-cloud-python/pull/6438))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docstring changes via synth. ([#6473](https://github.com/googleapis/google-cloud-python/pull/6473))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Overlooked synth changes. ([#6439](https://github.com/googleapis/google-cloud-python/pull/6439))

## 0.1.0

11-01-2018 15:12 PDT

### New Features
- Generate Security Center Client Library ([#6356](https://github.com/googleapis/google-cloud-python/pull/6356))

