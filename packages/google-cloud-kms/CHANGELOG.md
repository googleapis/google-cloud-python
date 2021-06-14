# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-kms/#history

## [2.3.0](https://www.github.com/googleapis/python-kms/compare/v2.2.0...v2.3.0) (2021-06-14)


### Features

* add `from_service_account_info` ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))
* add common resource path helpers ([#74](https://www.github.com/googleapis/python-kms/issues/74)) ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))
* add ECDSA secp256k1 to the list of supported algorithms ([#120](https://www.github.com/googleapis/python-kms/issues/120)) ([65a453f](https://www.github.com/googleapis/python-kms/commit/65a453f3a2adb71ea82a96d769d748ad0dc721b4))
* add script to verify attestations with certificate chains ([#99](https://www.github.com/googleapis/python-kms/issues/99)) ([7b0799f](https://www.github.com/googleapis/python-kms/commit/7b0799f4e1b52b359862e97ea2b89befafe92713))
* expose client transport ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))


### Bug Fixes

* **deps:** add packaging requirement ([#114](https://www.github.com/googleapis/python-kms/issues/114)) ([a6a894f](https://www.github.com/googleapis/python-kms/commit/a6a894f0c49fb1774d74aa26441e7525f0c0d138))
* fix retryable errors ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))
* remove grpc send/recv limits ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))
* use correct retry deadline ([6d115ce](https://www.github.com/googleapis/python-kms/commit/6d115ce1902e4306ba3e1d80de64a2424e47ef52))

## [2.2.0](https://www.github.com/googleapis/python-kms/compare/v2.1.0...v2.2.0) (2020-09-16)


### Features

* regenerate client lib to pick up new mtls env ([#55](https://www.github.com/googleapis/python-kms/issues/55)) ([4d62c19](https://www.github.com/googleapis/python-kms/commit/4d62c19d2f0f7c597214f2b39dfecb85f9d75a58))


### Documentation

* add crypto_key_path_path method rename to UPGRADING.md ([#45](https://www.github.com/googleapis/python-kms/issues/45)) ([81db5d9](https://www.github.com/googleapis/python-kms/commit/81db5d90112092772b83aec57e2358088ed88e0d)), closes [#43](https://www.github.com/googleapis/python-kms/issues/43)

## [2.1.0](https://www.github.com/googleapis/python-kms/compare/v2.0.1...v2.1.0) (2020-08-27)


### Features

* accept custom client_info ([#41](https://www.github.com/googleapis/python-kms/issues/41)) ([6688e80](https://www.github.com/googleapis/python-kms/commit/6688e80aa4db74980d4a6194519c814a22cde177))

### [2.0.1](https://www.github.com/googleapis/python-kms/compare/v2.0.0...v2.0.1) (2020-08-24)


### Bug Fixes

* add system test back ([#39](https://www.github.com/googleapis/python-kms/issues/39)) ([fc5a720](https://www.github.com/googleapis/python-kms/commit/fc5a720d93ba41cd2616c7c9c8012d9a3e8f4a9c))


### Documentation

* Generate using new common.py_samples() synthtool functionality ([#35](https://www.github.com/googleapis/python-kms/issues/35)) ([90097bc](https://www.github.com/googleapis/python-kms/commit/90097bca7660f148f36e009f70d108404efa5308))

## [2.0.0](https://www.github.com/googleapis/python-kms/compare/v1.4.0...v2.0.0) (2020-07-30)


### ⚠ BREAKING CHANGES

* migrate to microgenerator. (#16)

### Features

* migrate to microgenerator. See [Migration Guide](https://github.com/googleapis/python-kms/blob/release-v2.0.0/UPGRADING.md). ([#16](https://www.github.com/googleapis/python-kms/issues/16)) ([605f757](https://www.github.com/googleapis/python-kms/commit/605f7577a9a9f1a2b39fa69da7e250b5f70e945e))


## [1.4.0](https://www.github.com/googleapis/python-kms/compare/v1.3.0...v1.4.0) (2020-04-14)


### Features

* add support for external key manager (via synth) ([#8](https://www.github.com/googleapis/python-kms/issues/8)) ([4077fc8](https://www.github.com/googleapis/python-kms/commit/4077fc89943cc09d489d44c05efcf9cab61cdbaf))

## [1.3.0](https://www.github.com/googleapis/python-kms/compare/v1.2.1...v1.3.0) (2020-02-12)


### Features

* **kms:** add `ProtectionLevel.External` enum; standardize use of 'optional' and 'required' in docstrings (via synth) ([#10070](https://www.github.com/googleapis/python-kms/issues/10070)) ([add232f](https://www.github.com/googleapis/python-kms/commit/add232fb657505264300ff37b07dc47fcdbbeede))
* **kms:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10045](https://www.github.com/googleapis/python-kms/issues/10045)) ([23dca59](https://www.github.com/googleapis/python-kms/commit/23dca598dbfef86460d1a16e5a4386ab2714cfd3))


### Bug Fixes

* **kms:** deprecate resource name helper methods (via synth) ([#9836](https://www.github.com/googleapis/python-kms/issues/9836)) ([a3eca00](https://www.github.com/googleapis/python-kms/commit/a3eca000de2518080e4a960be731fb2be08c90da))

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
