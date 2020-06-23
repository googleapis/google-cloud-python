# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-asset/#history

## [1.2.0](https://www.github.com/googleapis/python-asset/compare/v1.1.0...v1.2.0) (2020-06-23)


### Features

* **v1:** add support for condition in Feed ([#44](https://www.github.com/googleapis/python-asset/issues/44)) ([467ab58](https://www.github.com/googleapis/python-asset/commit/467ab58b43aa11d8d6f8087800e5d8b451984edc))

## [1.1.0](https://www.github.com/googleapis/python-asset/compare/v1.0.0...v1.1.0) (2020-06-10)

### Features

* add `search_all_resources` and `search_all_iam_policies` (via synth) ([#32](https://www.github.com/googleapis/python-asset/issues/32)) ([24a0827](https://www.github.com/googleapis/python-asset/commit/24a0827913dfa7563ea08cdf2e329626eadca4a3)), closes [#541](https://www.github.com/googleapis/python-asset/issues/541)

## [1.0.0](https://www.github.com/googleapis/python-asset/compare/v0.10.0...v1.0.0) (2020-06-10)


### Features

* release to GA ([#17](https://www.github.com/googleapis/python-asset/issues/17)) ([731e350](https://www.github.com/googleapis/python-asset/commit/731e350f6321a1b29b482ad360172754a2a255c6))

## [0.10.0](https://www.github.com/googleapis/python-asset/compare/v0.9.0...v0.10.0) (2020-05-08)


### Features

* add orgpolicy and accesscontextmanager (via synth) ([#26](https://www.github.com/googleapis/python-asset/issues/26)) ([c9d818e](https://www.github.com/googleapis/python-asset/commit/c9d818e4c53707d51395a33e6fc1b202126d6a29))

## [0.9.0](https://www.github.com/googleapis/python-asset/compare/v0.8.0...v0.9.0) (2020-03-17)


### Features

* add v1p4beta1 ([#16](https://www.github.com/googleapis/python-asset/issues/16)) ([b5771c3](https://www.github.com/googleapis/python-asset/commit/b5771c3bf6c580e414a998b63cef5400f2b3c50d))

## [0.8.0](https://www.github.com/googleapis/python-asset/compare/v0.7.0...v0.8.0) (2020-03-07)


### Features

* remove search resources and search iam policies support in v1p1beta1; remove export assets and batch get assets history from v1p2beta1 (via synth) ([#12](https://www.github.com/googleapis/python-asset/issues/12)) ([15b60a3](https://www.github.com/googleapis/python-asset/commit/15b60a349c93c928fe121dc47d44d812a0c14439))


### Bug Fixes

* **asset:** correct asset synthfile ([#10355](https://www.github.com/googleapis/python-asset/issues/10355)) ([32d9374](https://www.github.com/googleapis/python-asset/commit/32d937433109b55c8f6632d402859a38520ee153))

## 0.7.0

01-29-2020 10:53 PST

### New Features
- Add v1p1beta1, promote library to  beta. ([#10202](https://github.com/googleapis/google-cloud-python/pull/10202))
- Undeprecate resource name helper methods, add 2.7 deprecation warning (via synth).  ([#10036](https://github.com/googleapis/google-cloud-python/pull/10036))

## 0.6.0

12-12-2019 10:46 PST

### New Features
- Add real time feed support to v1 (via synth). ([#9930](https://github.com/googleapis/google-cloud-python/pull/9930))
- Deprecate resource name helper methods (via synth). ([#9827](https://github.com/googleapis/google-cloud-python/pull/9827))

### Documentation
- Change spacing in docs templates (via synth). ([#9736](https://github.com/googleapis/google-cloud-python/pull/9736))
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

### Internal / Testing Changes
- Normalize VPCSC configuration in systests. ([#9614](https://github.com/googleapis/google-cloud-python/pull/9614))

## 0.5.0

10-29-2019 14:26 PDT

### New Features
- Add `bigquery_destination` to `OutputConfig`; make `content_type` optional argument to `BatchGetAssetsHistoryRequest`; add `uri_prefix` to `GcsDestination`; add `ORG_POLICY` and `ACCESS_POLICY` content type enums ([#9555](https://github.com/googleapis/google-cloud-python/pull/9555))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages; use googleapis.dev for api_core refs ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 0.4.1

08-12-2019 13:44 PDT

### Documentation
- Fix links to googleapis.dev ([#8998](https://github.com/googleapis/google-cloud-python/pull/8998))

## 0.4.0

08-01-2019 14:24 PDT

### New Features
- Generate asset v1p2beta1. ([#8888](https://github.com/googleapis/google-cloud-python/pull/8888))

### Internal / Testing Changes
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.3.0

07-22-2019 17:42 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8382](https://github.com/googleapis/google-cloud-python/pull/8382))
- Add nox session docs, add routing header to method metadata (via synth). ([#7919](https://github.com/googleapis/google-cloud-python/pull/7919))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add 'client_options' support (via synth). ([#8498](https://github.com/googleapis/google-cloud-python/pull/8498))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Update vpcsc test settings. ([#8627](https://github.com/googleapis/google-cloud-python/pull/8627))
- Pin black version (via synth) ([#8572](https://github.com/googleapis/google-cloud-python/pull/8572))
- Add VPCSC tests. ([#8613](https://github.com/googleapis/google-cloud-python/pull/8613))
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Add disclaimer to auto-generated template files (via synth). ([#8306](https://github.com/googleapis/google-cloud-python/pull/8306))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8232](https://github.com/googleapis/google-cloud-python/pull/8232))
- Fix coverage in 'types.py'. ([#8144](https://github.com/googleapis/google-cloud-python/pull/8144))
- Blacken noxfile.py, setup.py (via synth). ([#8114](https://github.com/googleapis/google-cloud-python/pull/8114))
-  Declare encoding as utf-8 in pb2 files (via synth). ([#8343](https://github.com/googleapis/google-cloud-python/pull/8343))
- Add empty lines (via synth). ([#8047](https://github.com/googleapis/google-cloud-python/pull/8047))

## 0.2.0

03-19-2019 12:17 PDT


### Implementation Changes
- Rename 'GcsDestination.uri' -> 'object_uri', docstring changes . ([#7202](https://github.com/googleapis/google-cloud-python/pull/7202))
- Protoc-generated serialization update.. ([#7073](https://github.com/googleapis/google-cloud-python/pull/7073))

### New Features
- Generate v1. ([#7513](https://github.com/googleapis/google-cloud-python/pull/7513))

### Documentation
- Fix broken links to Cloud Asset API ([#7524](https://github.com/googleapis/google-cloud-python/pull/7524))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Pick up stub docstring fix in GAPIC generator.[#6963](https://github.com/googleapis/google-cloud-python/pull/6963))

### Internal / Testing Changes
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Add support for including protos in synth ([#7114](https://github.com/googleapis/google-cloud-python/pull/7114))

## 0.1.2

12-17-2018 16:15 PST


### Implementation Changes
- Use moved iam.policy now at google.api_core.iam.policy ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6607](https://github.com/googleapis/google-cloud-python/pull/6607))
- Pick up fixes in GAPIC generator. ([#6489](https://github.com/googleapis/google-cloud-python/pull/6489))
- Fix client_info bug, update docstrings. ([#6403](https://github.com/googleapis/google-cloud-python/pull/6403))
- Synth docstring changes generated from updated protos ([#6349](https://github.com/googleapis/google-cloud-python/pull/6349))
- Generated cloud asset client files are under asset-[version] ([#6341](https://github.com/googleapis/google-cloud-python/pull/6341))

### New Features

### Dependencies
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Fix docs build. ([#6351](https://github.com/googleapis/google-cloud-python/pull/6351))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add templating to asset synth.py ([#6606](https://github.com/googleapis/google-cloud-python/pull/6606))
- Add synth metadata. ([#6560](https://github.com/googleapis/google-cloud-python/pull/6560))
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.1.1

### Packaging
- Release as `google-cloud-asset`, rather than `google-cloud-cloudasset` ([#5998](https://github.com/googleapis/google-cloud-python/pull/5998))

## 0.1.0

Initial release.
