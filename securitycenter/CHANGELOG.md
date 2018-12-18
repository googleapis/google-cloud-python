# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-securitycenter/#history

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

