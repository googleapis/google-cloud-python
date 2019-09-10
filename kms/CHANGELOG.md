# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-kms/#history

## 1.2.1

08-12-2019 13:44 PDT


### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8959](https://github.com/googleapis/google-cloud-python/pull/8959))

### Documentation
- Fix links to googleapis.dev ([#8998](https://github.com/googleapis/google-cloud-python/pull/8998))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.2.0

07-24-2019 16:42 PDT


### Implementation Changes
- Accomodate new location of 'IAMPolicyStub' (via synth). ([#8679](https://github.com/googleapis/google-cloud-python/pull/8679))

### New Features
- Add 'options_' argument to client's 'get_iam_policy'; pin black version (via synth). ([#8656](https://github.com/googleapis/google-cloud-python/pull/8656))
- Add 'client_options' support, update list method docstrings (via synth). ([#8514](https://github.com/googleapis/google-cloud-python/pull/8514))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

## 1.1.0

06-27-2019 12:32 PDT

### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8395](https://github.com/googleapis/google-cloud-python/pull/8395))
- Add empty lines (via synth). ([#8062](https://github.com/googleapis/google-cloud-python/pull/8062))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add ability to create keys via import, add crypto algorithms (via synth).  ([#8356](https://github.com/googleapis/google-cloud-python/pull/8356))
- Retry idempotent codes for Encyrpt, Decrypt, Asymmetric Decrypt, Asymmetric Sign (via synth). ([#7715](https://github.com/googleapis/google-cloud-python/pull/7715))
- Add CAVIUM_V2_COMPRESSED option to KeyOperationAttestation (via synth). ([#7396](https://github.com/googleapis/google-cloud-python/pull/7396))

### Documentation
- Update docstrings. ([#7868](https://github.com/googleapis/google-cloud-python/pull/7868))
- Update information in READMEs to indicate KMS is GA. ([#7840](https://github.com/googleapis/google-cloud-python/pull/7840))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Add disclaimer to auto-generated template files (via synth). ([#8318](https://github.com/googleapis/google-cloud-python/pull/8318))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8245](https://github.com/googleapis/google-cloud-python/pull/8245))
- Fix coverage in 'types.py'; blacken 'noxfile.py' / 'setup.py' (via synth). ([#8157](https://github.com/googleapis/google-cloud-python/pull/8157))
- Add nox session `docs`, reorder methods (via synth). ([#7775](https://github.com/googleapis/google-cloud-python/pull/7775))
- Copy lintified proto files (via synth). ([#7449](https://github.com/googleapis/google-cloud-python/pull/7449))

## 1.0.0

02-13-2019 10:53 PST

### Implementation Changes
- Remove unused message exports. ([#7270](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7270))
- Pick up stub docstring fix in GAPIC generator. ([#6974](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6974))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7307))

### Internal / Testing Changes
- Add KMS system test ([#7304](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7304))
- Add protos as an artifact to library ([#7205](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7205))
- Update copyright headers
- Protoc-generated serialization update. ([#7086](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7086))

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

