# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-tasks/#history

## 1.2.1

08-12-2019 13:50 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8971](https://github.com/googleapis/google-cloud-python/pull/8971))

### Documentation
- Fix links to googleapis.dev ([#8998](https://github.com/googleapis/google-cloud-python/pull/8998))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.2.0

07-24-2019 17:41 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8406](https://github.com/googleapis/google-cloud-python/pull/8406))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8660](https://github.com/googleapis/google-cloud-python/pull/8660))
- Add 'client_options' support, update list method docstrings (via synth). ([#8524](https://github.com/googleapis/google-cloud-python/pull/8524))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation

- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix typo in README. ([#8606](https://github.com/googleapis/google-cloud-python/pull/8606))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8366](https://github.com/googleapis/google-cloud-python/pull/8366))
- Add disclaimer to auto-generated template files (via synth).  ([#8330](https://github.com/googleapis/google-cloud-python/pull/8330))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8254](https://github.com/googleapis/google-cloud-python/pull/8254))
- Fix coverage in 'types.py' (via synth). ([#8166](https://github.com/googleapis/google-cloud-python/pull/8166))
- Blacken noxfile.py, setup.py (via synth). ([#8134](https://github.com/googleapis/google-cloud-python/pull/8134))
- Add empty lines (via synth). ([#8074](https://github.com/googleapis/google-cloud-python/pull/8074))

## 1.1.0

05-14-2019 15:30 PDT

### Implementation Changes
- Remove log_sampling_ratio, add stackdriver_logging_config (via synth). ([#7950](https://github.com/googleapis/google-cloud-python/pull/7950))

### Documentation
- Update docstrings (via synth). ([#7963](https://github.com/googleapis/google-cloud-python/pull/7963))
- Update docstrings (via synth). ([#7940](https://github.com/googleapis/google-cloud-python/pull/7940))

### Internal / Testing Changes
- Add nox session `docs`, reorder methods (via synth). ([#7783](https://github.com/googleapis/google-cloud-python/pull/7783))

## 1.0.0

04-29-2019 16:35 PDT

### Documentation
- Correct docs/index.rst. ([#7808](https://github.com/googleapis/google-cloud-python/pull/7808))

### Internal / Testing Changes
- Add smoke test. ([#7808](https://github.com/googleapis/google-cloud-python/pull/7808))

## 0.7.0

04-15-2019 10:21 PDT


### New Features
- Add auth and stackdriver logging configuration (via synth). ([#7666](https://github.com/googleapis/google-cloud-python/pull/7666))

### Documentation
- Tasks: Format docstrings for enums (via synth). ([#7601](https://github.com/googleapis/google-cloud-python/pull/7601))

## 0.6.0

03-26-2019 13:35 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Generate v2. ([#7547](https://github.com/googleapis/google-cloud-python/pull/7547))

## 0.5.0

03-06-2019 15:03 PST


### Implementation Changes
- Remove unused message exports (via synth). ([#7276](https://github.com/googleapis/google-cloud-python/pull/7276))
- Protoc-generated serialization update. ([#7096](https://github.com/googleapis/google-cloud-python/pull/7096))

### New Features
- Add 'Task.http_request' and associated message type (via synth). ([#7432](https://github.com/googleapis/google-cloud-python/pull/7432))
- Add 'Task.dispatch_deadline' via synth. ([#7211](https://github.com/googleapis/google-cloud-python/pull/7211))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Restore expanded example from PR [#7025](https://github.com/googleapis/google-cloud-python/pull/7025) after synth. ([#7062](https://github.com/googleapis/google-cloud-python/pull/7062))
- Add working example for 'create_queue'. ([#7025](https://github.com/googleapis/google-cloud-python/pull/7025))
- Pick up stub docstring fix in GAPIC generator. ([#6983](https://github.com/googleapis/google-cloud-python/pull/6983))

### Internal / Testing Changes
- Copy lintified proto files (via synth). ([#7471](https://github.com/googleapis/google-cloud-python/pull/7471))
- Add clarifying comment to blacken nox target. ([#7405](https://github.com/googleapis/google-cloud-python/pull/7405))
- Copy proto files alongside protoc versions
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.4.0

12-18-2018 09:50 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6616](https://github.com/googleapis/google-cloud-python/pull/6616))
- Fix `client_info` bug, update docstrings and timeouts. ([#6422](https://github.com/googleapis/google-cloud-python/pull/6422))
- Re-generate library using tasks/synth.py ([#5980](https://github.com/googleapis/google-cloud-python/pull/5980))

### New Features
- Pick up changes to GAPIC generator, drop 'Code' enum. ([#6509](https://github.com/googleapis/google-cloud-python/pull/6509))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Separate / distinguish API docs for different API versions. ([#6306](https://github.com/googleapis/google-cloud-python/pull/6306))
- Docstring tweaks from protos. ([#6261](https://github.com/googleapis/google-cloud-python/pull/6261))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Remove autosynth / tweaks for 'README.rst' / 'setup.py'. ([#5957](https://github.com/googleapis/google-cloud-python/pull/5957))
- Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Don't update nox in 'tasks/synth.py'. ([#6232](https://github.com/googleapis/google-cloud-python/pull/6232))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.3.0

### Implementation Changes
- Regenerate tasks to fix API enablement URL (#5579)

### New Features
- Tasks: Add v2beta3 endpoint (#5880)

### Documentation
- update Task library doc link (#5708)
- tasks missing from docs (#5656)

## 0.2.0

### Implementation Changes
- regenerate tasks v2beta2 (#5469)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

## 0.1.0

### New Features
- Add v2beta2 endpoint for Tasks

