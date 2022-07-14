# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-kms/#history

## [2.12.0](https://github.com/googleapis/python-kms/compare/v2.11.2...v2.12.0) (2022-07-14)


### Features

* add audience parameter ([06a4096](https://github.com/googleapis/python-kms/commit/06a4096a61c8b2ed14ccbf88f386203e2c8dc54e))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#315](https://github.com/googleapis/python-kms/issues/315)) ([82ab556](https://github.com/googleapis/python-kms/commit/82ab556b8aec33d75e99c151f01b7e2c4aa6a719))
* require python 3.7+ ([#313](https://github.com/googleapis/python-kms/issues/313)) ([28d244f](https://github.com/googleapis/python-kms/commit/28d244f1347337f9294a9c3445df426c28b7d1d3))

## [2.11.2](https://github.com/googleapis/python-kms/compare/v2.11.1...v2.11.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#299](https://github.com/googleapis/python-kms/issues/299)) ([45b97e8](https://github.com/googleapis/python-kms/commit/45b97e8cd0443c090c28b348af1e3ccddf2dbf29))


### Documentation

* fix changelog header to consistent size ([#298](https://github.com/googleapis/python-kms/issues/298)) ([d3f7a5b](https://github.com/googleapis/python-kms/commit/d3f7a5b9abe6828f84d45df570845d3be16f5411))

## [2.11.1](https://github.com/googleapis/python-kms/compare/v2.11.0...v2.11.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#247](https://github.com/googleapis/python-kms/issues/247)) ([ef54503](https://github.com/googleapis/python-kms/commit/ef54503efc02d178e1294f3550693208082d256f))
* **deps:** require proto-plus>=1.15.0 ([ef54503](https://github.com/googleapis/python-kms/commit/ef54503efc02d178e1294f3550693208082d256f))


### Documentation

* add generated snippets ([#236](https://github.com/googleapis/python-kms/issues/236)) ([314485f](https://github.com/googleapis/python-kms/commit/314485f55904eb9e914380b627d3a80fc65712b3))
* **samples:** updated var name to avoid shadowing built-in ([#238](https://github.com/googleapis/python-kms/issues/238)) ([5bbf2c3](https://github.com/googleapis/python-kms/commit/5bbf2c36b99c5f547cda5806f803d06cef17c627))

## [2.11.0](https://github.com/googleapis/python-kms/compare/v2.10.1...v2.11.0) (2022-02-03)


### Features

* add a new EkmService API ([#233](https://github.com/googleapis/python-kms/issues/233)) ([eb532f5](https://github.com/googleapis/python-kms/commit/eb532f5c84907c12356e549c694c0210e5ad585b))
* add api key support ([#230](https://github.com/googleapis/python-kms/issues/230)) ([fdf62ae](https://github.com/googleapis/python-kms/commit/fdf62ae3b3209a1215e0f2f2440add1f01d40907))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([97f7ea5](https://github.com/googleapis/python-kms/commit/97f7ea50a30d1dc1133d7703e6bd90ad209f75a1))


### Documentation

* **samples:** fix typo in verify_asymmetric_ec.py ([#227](https://github.com/googleapis/python-kms/issues/227)) ([3817d73](https://github.com/googleapis/python-kms/commit/3817d7390fddebd137c99865455f0ae145dbcf63))

## [2.10.1](https://www.github.com/googleapis/python-kms/compare/v2.10.0...v2.10.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([6d7b8c1](https://www.github.com/googleapis/python-kms/commit/6d7b8c1043e59f3749c58b032f3fe800293c03f5))
* **deps:** require google-api-core >= 1.28.0 ([6d7b8c1](https://www.github.com/googleapis/python-kms/commit/6d7b8c1043e59f3749c58b032f3fe800293c03f5))


### Documentation

* list oneofs in docstring ([6d7b8c1](https://www.github.com/googleapis/python-kms/commit/6d7b8c1043e59f3749c58b032f3fe800293c03f5))

## [2.10.0](https://www.github.com/googleapis/python-kms/compare/v2.9.0...v2.10.0) (2021-10-18)


### Features

* add support for Raw PKCS[#1](https://www.github.com/googleapis/python-kms/issues/1) signing keys ([#195](https://www.github.com/googleapis/python-kms/issues/195)) ([9c4f997](https://www.github.com/googleapis/python-kms/commit/9c4f997d09e9a83141eda767cd2bb63a0bf58a37))

## [2.9.0](https://www.github.com/googleapis/python-kms/compare/v2.8.0...v2.9.0) (2021-10-08)


### Features

* add context manager support in client ([#190](https://www.github.com/googleapis/python-kms/issues/190)) ([6707e79](https://www.github.com/googleapis/python-kms/commit/6707e7950f9ebcedaa22d2e1d12aa0af6e35581d))

## [2.8.0](https://www.github.com/googleapis/python-kms/compare/v2.7.0...v2.8.0) (2021-09-30)


### Features

* add RPC retry information for MacSign, MacVerify, and GenerateRandomBytes ([#186](https://www.github.com/googleapis/python-kms/issues/186)) ([62591c8](https://www.github.com/googleapis/python-kms/commit/62591c8ead85c33fa5a5c4cc7c2a26779cbd1075))

## [2.7.0](https://www.github.com/googleapis/python-kms/compare/v2.6.1...v2.7.0) (2021-09-30)


### Features

* add OAEP+SHA1 to the list of supported algorithms ([#181](https://www.github.com/googleapis/python-kms/issues/181)) ([65b2c97](https://www.github.com/googleapis/python-kms/commit/65b2c975d2635cd562a0e4b7ff8f1989643929ee))


### Bug Fixes

* improper types in pagers generation ([8ff7501](https://www.github.com/googleapis/python-kms/commit/8ff75018aeacd87bd00abb4a12a130f3e28604f5))

## [2.6.1](https://www.github.com/googleapis/python-kms/compare/v2.6.0...v2.6.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([728e5e0](https://www.github.com/googleapis/python-kms/commit/728e5e08738e4954c3f1f9eecda5c1d1753501c3))

## [2.6.0](https://www.github.com/googleapis/python-kms/compare/v2.5.0...v2.6.0) (2021-08-30)


### Features

* add support for Key Reimport ([#167](https://www.github.com/googleapis/python-kms/issues/167)) ([1aaaea9](https://www.github.com/googleapis/python-kms/commit/1aaaea9405109a2f226f3d6a9631eb5f110349ab))


### Documentation

* **kms:** add samples for new hmac and rng apis ([#161](https://www.github.com/googleapis/python-kms/issues/161)) ([558b740](https://www.github.com/googleapis/python-kms/commit/558b740f0491311ebcaf3c62d7117ec15883150a))

## [2.5.0](https://www.github.com/googleapis/python-kms/compare/v2.4.3...v2.5.0) (2021-08-07)


### Features

* add support for HMAC, Variable Key Destruction, and GenerateRandom ([#157](https://www.github.com/googleapis/python-kms/issues/157)) ([4b7c9f9](https://www.github.com/googleapis/python-kms/commit/4b7c9f96a73fba8b825f8c7cfabc748728c0eb62))

## [2.4.3](https://www.github.com/googleapis/python-kms/compare/v2.4.2...v2.4.3) (2021-07-29)


### Documentation

* update README for attestation verification scripts ([#151](https://www.github.com/googleapis/python-kms/issues/151)) ([a1a111d](https://www.github.com/googleapis/python-kms/commit/a1a111d67017b89235c18455512658514ce65140))

## [2.4.2](https://www.github.com/googleapis/python-kms/compare/v2.4.1...v2.4.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#149](https://www.github.com/googleapis/python-kms/issues/149)) ([211fe79](https://www.github.com/googleapis/python-kms/commit/211fe797d8847675390af67691d7296bbf150a02))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#144](https://www.github.com/googleapis/python-kms/issues/144)) ([88fee3a](https://www.github.com/googleapis/python-kms/commit/88fee3ab24acca72d2bade56e471d60cc893d97f))


### Miscellaneous Chores

* release as 2.4.2 ([#150](https://www.github.com/googleapis/python-kms/issues/150)) ([6663190](https://www.github.com/googleapis/python-kms/commit/66631903dc8c32eea1af0bd0265893e6bdffd55f))

## [2.4.1](https://www.github.com/googleapis/python-kms/compare/v2.4.0...v2.4.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#143](https://www.github.com/googleapis/python-kms/issues/143)) ([c1f33e1](https://www.github.com/googleapis/python-kms/commit/c1f33e1844dfe2bca4b03d9ad29195381b5c0fd8))

## [2.4.0](https://www.github.com/googleapis/python-kms/compare/v2.3.0...v2.4.0) (2021-07-12)


### Features

* add always_use_jwt_access ([#129](https://www.github.com/googleapis/python-kms/issues/129)) ([cfa0802](https://www.github.com/googleapis/python-kms/commit/cfa08022db3e096e2414418b63482606af8d46cb))


### Bug Fixes

* disable always_use_jwt_access ([#133](https://www.github.com/googleapis/python-kms/issues/133)) ([8007b81](https://www.github.com/googleapis/python-kms/commit/8007b810f11ebf49cd24edd77867abac174841e9))


### Documentation

* Include verify_attestation_chains.py help text to attestations README ([#134](https://www.github.com/googleapis/python-kms/issues/134)) ([2f2bb49](https://www.github.com/googleapis/python-kms/commit/2f2bb49adca244031d584ffbb27e32585e64ed42))
* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-kms/issues/1127)) ([#124](https://www.github.com/googleapis/python-kms/issues/124)) ([5c3e273](https://www.github.com/googleapis/python-kms/commit/5c3e27391c4771b4a03c87e21a5260ed8d61b9c4)), closes [#1126](https://www.github.com/googleapis/python-kms/issues/1126)

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

## [2.0.1](https://www.github.com/googleapis/python-kms/compare/v2.0.0...v2.0.1) (2020-08-24)


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
