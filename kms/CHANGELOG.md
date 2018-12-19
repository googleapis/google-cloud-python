# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-kms/#history

## 0.2.1

12-18-2018 09:24 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up changes in GAPIC generator. ([#6499](https://github.com/googleapis/google-cloud-python/pull/6499))
- Fix `client_info` bug, update docstrings. ([#6414](https://github.com/googleapis/google-cloud-python/pull/6414))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Update IAM version in dependencies ([#6362](https://github.com/googleapis/google-cloud-python/pull/6362))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6569](https://github.com/googleapis/google-cloud-python/pull/6569))
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Don't update nox in 'kms/synth.py'. ([#6233](https://github.com/googleapis/google-cloud-python/pull/6233))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Don't scribble on setup.py harder. ([#6064](https://github.com/googleapis/google-cloud-python/pull/6064))
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6021](https://github.com/googleapis/google-cloud-python/pull/6021))
- Exclude 'setup.py' from synth. ([#6038](https://github.com/googleapis/google-cloud-python/pull/6038))

## 0.2.0

### Documentation
- Docs: Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Re-generate library using kms/synth.py ([#5977](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5977))
- Re-generate library using kms/synth.py ([#5951](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5951))
- Remove synth fix for replacing `iam_policy_pb2_grpc` ([#5755](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5755))

## 0.1.0

### New Features
- KMS v1

