# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-automl/#history

## 0.5.0

08-28-2019 14:07 PDT

### Implementation Changes
- Catch exceptions in GcsClient when a same name bucket already exists in a different project ([#9139](https://github.com/googleapis/google-cloud-python/pull/9139))
- Log when LROs are kicked off. ([#9058](https://github.com/googleapis/google-cloud-python/pull/9058))
- Throw a ValueError when an ambiguous display_name is used ([#9089](https://github.com/googleapis/google-cloud-python/pull/9089))
- Remove send/recv msg size limit (via synth). ([#8944](https://github.com/googleapis/google-cloud-python/pull/8944))

### New Features
- Enable users to pass in Pandas Dataframe when calling import_data() and batch_predict() from AutoML Tables client ([#9116](https://github.com/googleapis/google-cloud-python/pull/9116))
- Add support for documents (via synth). ([#9039](https://github.com/googleapis/google-cloud-python/pull/9039))
- Add a TablesClient for automl-tables specific behavior. ([#8720](https://github.com/googleapis/google-cloud-python/pull/8720))
- Add 'ClassificationEvaluationMetrics.display_name'/'BatchPredictResult.metadata'/'TableSpec.valid_row_count' (via synth) ([#9004](https://github.com/googleapis/google-cloud-python/pull/9004))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Skip relevant system tests if in VPCSC ([#9111](https://github.com/googleapis/google-cloud-python/pull/9111))
- Fix synth replace to add TablesClient. ([#9033](https://github.com/googleapis/google-cloud-python/pull/9033))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.4.0

07-22-2019 17:39 PDT


### New Features
- Add support for 'TablesModelMetadata.{optimization_objective_recall_value,optimization_objective_precision_value}' (via synth). ([#8643](https://github.com/googleapis/google-cloud-python/pull/8643))
- Add 'client_options' support, update list method docstrings (via synth). ([#8533](https://github.com/googleapis/google-cloud-python/pull/8533))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version (via synth). ([#8573](https://github.com/googleapis/google-cloud-python/pull/8573))
- Update Ruby package name (via synth). ([#8485](https://github.com/googleapis/google-cloud-python/pull/8485))
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.3.0

06-20-2019 14:47 PDT


### New Features
- Add support for video object tracking (via synth). ([#8278](https://github.com/googleapis/google-cloud-python/pull/8278))

### Documentation
- Add proto files; add 'docs' session to 'nox'; update docstrings (via synth). ([#8029](https://github.com/googleapis/google-cloud-python/pull/8029))

### Internal / Testing Changes
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8233](https://github.com/googleapis/google-cloud-python/pull/8233))
- Fix coverage in 'types.py'. ([#8145](https://github.com/googleapis/google-cloud-python/pull/8145))
- Blacken noxfile.py, setup.py (via synth). ([#8115](https://github.com/googleapis/google-cloud-python/pull/8115))
- Add empty lines (via synth). ([#8048](https://github.com/googleapis/google-cloud-python/pull/8048))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))
- Include protos in synth. ([#8000](https://github.com/googleapis/google-cloud-python/pull/8000))

## 0.2.0

04-03-2019 09:16 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Sort generated classes (via synth). ([#7256](https://github.com/googleapis/google-cloud-python/pull/7256))
- Protoc-generated serialization update. ([#7074](https://github.com/googleapis/google-cloud-python/pull/7074))

### New Features
- Video Classification, Text Extraction, Text Sentiment, Tables support. ([#7650](https://github.com/googleapis/google-cloud-python/pull/7650))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- AutoML: pick up stub docstring fix in GAPIC generator. ([#6964](https://github.com/googleapis/google-cloud-python/pull/6964))

### Internal / Testing Changes
- Update copyright headers

## 0.1.2

12-17-2018 16:27 PST


### Implementation Changes
- Add protoc-generated descriptor changes from updated .proto files. ([#6899](https://github.com/googleapis/google-cloud-python/pull/6899))
- Import `iam.policy` from `google.api_core.iam.policy`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes in GAPIC generator. ([#6490](https://github.com/googleapis/google-cloud-python/pull/6490))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix client_info bug, update docstrings. ([#6404](https://github.com/googleapis/google-cloud-python/pull/6404))
- Re-generate library using automl/synth.py ([#5972](https://github.com/googleapis/google-cloud-python/pull/5972))
- Re-generate library using automl/synth.py ([#5946](https://github.com/googleapis/google-cloud-python/pull/5946))

### Dependencies
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Bump minimum `api_core`' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6005](https://github.com/googleapis/google-cloud-python/pull/6005))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack automl gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6561](https://github.com/googleapis/google-cloud-python/pull/6561))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.1.1

### Documentation
- Fix broken links (#5675)
- bad trove classifier (#5648)

## 0.1.0

### New Features
- Initial Release of AutoML v1beta1

