# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dataproc/#history

## [0.8.0](https://www.github.com/googleapis/python-dataproc/compare/v0.7.0...v0.8.0) (2020-05-19)


### Features

* add SparkR and Presto jobs to WorkflowTemplates; add new optional components; add submit_job_as_operation to v1 (via synth) ([#21](https://www.github.com/googleapis/python-dataproc/issues/21)) ([1cf10b6](https://www.github.com/googleapis/python-dataproc/commit/1cf10b6b127a63dbeb34958771c2cc8d8cb37099))

## [0.7.0](https://www.github.com/googleapis/python-dataproc/compare/v0.6.1...v0.7.0) (2020-03-05)


### Features

* add lifecycle config and reservation affinity support to v1 (via synth) ([#10](https://www.github.com/googleapis/python-dataproc/issues/10)) ([bb36194](https://www.github.com/googleapis/python-dataproc/commit/bb36194d4b0cfb6f2c5a0358625a17c629f71b21))

## 0.6.1

11-12-2019 08:24 PST

### Documentation
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

## 0.6.0

11-07-2019 16:34 PST


### Implementation Changes
- Tweak proto annotations (via synth). ([#9466](https://github.com/googleapis/google-cloud-python/pull/9466))
- Remove send/recv msg size limit (via synth). ([#8951](https://github.com/googleapis/google-cloud-python/pull/8951))

### New Features
- Add V1 autoscaling policy support; annotate protos (via synth). ([#9402](https://github.com/googleapis/google-cloud-python/pull/9402))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatibility badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.5.0

07-24-2019 16:02 PDT

### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8387](https://github.com/googleapis/google-cloud-python/pull/8387))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8505](https://github.com/googleapis/google-cloud-python/pull/8505))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version (via synth). ([#8579](https://github.com/googleapis/google-cloud-python/pull/8579))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8349](https://github.com/googleapis/google-cloud-python/pull/8349))
- Add disclaimer to auto-generated template files (via synth).  ([#8311](https://github.com/googleapis/google-cloud-python/pull/8311))
- Supress checking 'cov-fail-under' in nox default session (via synth). ([#8237](https://github.com/googleapis/google-cloud-python/pull/8237))

## 0.4.0

05-30-2019 05:52 PDT

### Implementation Changes
- Update docs/conf.py, add routing header to method metadata, fix docstrings (via synth). ([#7924](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7924))

### New Features
- Add new service features for v1, including autoscaling (via synth). ([#8152](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8152))
- Add new service features for v1beta2, including autoscaling (via synth). ([#8119](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8119))

### Documentation
- Add nox session `docs` ([#7429](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7429))
- Add clarifying comment to blacken nox target. ([#7388](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7388))

### Internal / Testing Changes
- Re-add import of 'operations.proto' to V1 'clusters.proto' (via synth). ([#8188](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8188))
- Add empty lines (via synth). ([#8054](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8054))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7535))
- Copy lintified proto files (via synth). ([#7465](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7465))

## 0.3.1

02-15-2019 12:36 PST


### Implementation Changes
- Remove unused message exports. ([#7266](https://github.com/googleapis/google-cloud-python/pull/7266))
- Protoc-generated serialization update.. ([#7079](https://github.com/googleapis/google-cloud-python/pull/7079))
- Trivial housekeeping change to .proto files. ([#7067](https://github.com/googleapis/google-cloud-python/pull/7067))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Pick up stub docstring fix in GAPIC generator. ([#6967](https://github.com/googleapis/google-cloud-python/pull/6967))

### Internal / Testing Changes
- Copy proto files alongside protoc versions.
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers

## 0.3.0

12-17-2018 18:20 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Update `cluster_controller_client` GAPIC config (via synth). ([#6659](https://github.com/googleapis/google-cloud-python/pull/6659))
- Add 'WorkflowTemplateServiceClient', optional args; update timeouts (via synth). ([#6655](https://github.com/googleapis/google-cloud-python/pull/6655))
- Pick up enum fixes in the GAPIC generator. ([#6609](https://github.com/googleapis/google-cloud-python/pull/6609))
- Pick up fixes in GAPIC generator. ([#6493](https://github.com/googleapis/google-cloud-python/pull/6493))
- Fix client_info bug, update docstrings. ([#6408](https://github.com/googleapis/google-cloud-python/pull/6408))
- Re-generate library using dataproc/synth.py ([#6056](https://github.com/googleapis/google-cloud-python/pull/6056))
- Re-generate library using dataproc/synth.py ([#5975](https://github.com/googleapis/google-cloud-python/pull/5975))
- Re-generate library using dataproc/synth.py ([#5949](https://github.com/googleapis/google-cloud-python/pull/5949))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Update Dataproc docs URL ([#6455](https://github.com/googleapis/google-cloud-python/pull/6455))
- Docs: fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Dataproc: harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6019](https://github.com/googleapis/google-cloud-python/pull/6019))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack dataproc gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6563](https://github.com/googleapis/google-cloud-python/pull/6563))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.2.0

### New Features
- Regenerate v1 endpoint. Add v1beta2 endpoint (#5717)

## 0.1.2

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Re-enable lint for tests, remove usage of pylint (#4921)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
