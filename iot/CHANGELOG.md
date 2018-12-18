# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-iot/#history

## 0.2.0

12-18-2018 09:19 PST


### Implementation Changes
- Use moved iam.policy now at google.api_core.iam.policy ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up new methods from protos. ([#6613](https://github.com/googleapis/google-cloud-python/pull/6613))
- Pick up fixes to GAPIC generator. ([#6513](https://github.com/googleapis/google-cloud-python/pull/6513))
- Fix client_info bug, update docstrings. ([#6413](https://github.com/googleapis/google-cloud-python/pull/6413))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Update IAM version in dependencies ([#6362](https://github.com/googleapis/google-cloud-python/pull/6362))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6568](https://github.com/googleapis/google-cloud-python/pull/6568))
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add 'synth.py'. ([#6085](https://github.com/googleapis/google-cloud-python/pull/6085))
- fix [#5676](https://github.com/googleapis/google-cloud-python/pull/5676) by including iot docs in build ([#5679](https://github.com/googleapis/google-cloud-python/pull/5679))
- fix trove classifier ([#5386](https://github.com/googleapis/google-cloud-python/pull/5386))

## 0.1.0

### New Features
- Add v1 Endpoint for IoT (#5355)

