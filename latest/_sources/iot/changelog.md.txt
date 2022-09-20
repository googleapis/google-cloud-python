# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-iot/#history

## 0.3.0

07-24-2019 16:35 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8393](https://github.com/googleapis/google-cloud-python/pull/8393))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7269](https://github.com/googleapis/google-cloud-python/pull/7269))
- Protoc-generated serialization update. ([#7085](https://github.com/googleapis/google-cloud-python/pull/7085))
- Pick up stub docstring fix in GAPIC generator. ([#6973](https://github.com/googleapis/google-cloud-python/pull/6973))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8655](https://github.com/googleapis/google-cloud-python/pull/8655))
- Add 'client_options' support, update list method docstrings (via synth). ([#8512](https://github.com/googleapis/google-cloud-python/pull/8512))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Update docstrings (via synth). ([#7867](https://github.com/googleapis/google-cloud-python/pull/7867))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright: 2018 -> 2019. ([#7147](https://github.com/googleapis/google-cloud-python/pull/7147))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). [#8354](https://github.com/googleapis/google-cloud-python/pull/8354))
- Add disclaimer to auto-generated template files (via synth). ([#8316](https://github.com/googleapis/google-cloud-python/pull/8316))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8243](https://github.com/googleapis/google-cloud-python/pull/8243))
- Fix coverage in 'types.py' (via synth). ([#8155](https://github.com/googleapis/google-cloud-python/pull/8155))
- Blacken noxfile.py, setup.py (via synth). ([#8125](https://github.com/googleapis/google-cloud-python/pull/8125))
- Add empty lines (via synth). ([#8060](https://github.com/googleapis/google-cloud-python/pull/8060))
- Exclude docs/index.rst from move in synth. ([#7835](https://github.com/googleapis/google-cloud-python/pull/7835))
- Reorder methods, add nox session `docs` (via synth). ([#7773](https://github.com/googleapis/google-cloud-python/pull/7773))
- Copy lintified proto files (via synth). ([#7448](https://github.com/googleapis/google-cloud-python/pull/7448))
- Add clarifying comment to blacken nox target. ([#7394](https://github.com/googleapis/google-cloud-python/pull/7394))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.2.0

12-18-2018 09:19 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up new methods from protos. ([#6613](https://github.com/googleapis/google-cloud-python/pull/6613))
- Pick up fixes to GAPIC generator. ([#6513](https://github.com/googleapis/google-cloud-python/pull/6513))
- Fix `client_info` bug, update docstrings. ([#6413](https://github.com/googleapis/google-cloud-python/pull/6413))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Update IAM version in dependencies ([#6362](https://github.com/googleapis/google-cloud-python/pull/6362))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

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
- Include IoT docs in build. ([#5679](https://github.com/googleapis/google-cloud-python/pull/5679))
- fix trove classifier ([#5386](https://github.com/googleapis/google-cloud-python/pull/5386))

## 0.1.0

### New Features
- Add v1 Endpoint for IoT (#5355)

