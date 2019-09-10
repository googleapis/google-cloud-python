# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-monitoring/#history

## 0.33.0

08-12-2019 13:54 PDT

### New Features
- Add notification channel verification; remove send/recv msg size limit (via synth). ([#8980](https://github.com/googleapis/google-cloud-python/pull/8980))

### Documentation
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.32.0

07-24-2019 16:52 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth).  ([#8397](https://github.com/googleapis/google-cloud-python/pull/8397))
- Add routing header to method metadata, update docs config (via synth).  ([#7642](https://github.com/googleapis/google-cloud-python/pull/7642))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7271](https://github.com/googleapis/google-cloud-python/pull/7271))
- Protoc-generated serialization update. ([#7089](https://github.com/googleapis/google-cloud-python/pull/7089))
- Pick up stub docstring fix in GAPIC generator. ([#6976](https://github.com/googleapis/google-cloud-python/pull/6976))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8516](https://github.com/googleapis/google-cloud-python/pull/8516))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fixes [#8545](https://github.com/googleapis/google-cloud-python/pull/8545) by removing typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))
- Update docstrings, copy lintified proto files (via synth). ([#7451](https://github.com/googleapis/google-cloud-python/pull/7451))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright: 2018 -> 2019. ([#7151](https://github.com/googleapis/google-cloud-python/pull/7151))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8358](https://github.com/googleapis/google-cloud-python/pull/8358))
- Add disclaimer to auto-generated template files (via synth). ([#8321](https://github.com/googleapis/google-cloud-python/pull/8321))
- Fix coverage in 'types.py' (via synth). ([#8159](https://github.com/googleapis/google-cloud-python/pull/8159))
- Add empty lines (via synth). ([#8065](https://github.com/googleapis/google-cloud-python/pull/8065))
- Add nox session `docs` (via synth). ([#7777](https://github.com/googleapis/google-cloud-python/pull/7777))
- Regenerate VPCSC tests to include NotificationChannelService and UptimeCheckService. ([#7853](https://github.com/googleapis/google-cloud-python/pull/7853))
- Set environment variables for VPCSC system tests. ([#7847](https://github.com/googleapis/google-cloud-python/pull/7847))
- Add VPCSC system test. ([#7791](https://github.com/googleapis/google-cloud-python/pull/7791))
- protobuf file housekeeping (no user-visible changes) (via synth).  ([#7588](https://github.com/googleapis/google-cloud-python/pull/7588))
- Add clarifying comment to blacken nox target. ([#7398](https://github.com/googleapis/google-cloud-python/pull/7398))
- Trivial gapic-generator change. ([#7231](https://github.com/googleapis/google-cloud-python/pull/7231))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.31.1

12-17-2018 16:51 PST


### Implementation Changes
- Import  `iam.policy` from `google.api_core.iam.policy`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))

## 0.31.0

11-29-2018 13:03 PST


### Implementation Changes
- Pick up enum fixes in the GAPIC generator. ([#6614](https://github.com/googleapis/google-cloud-python/pull/6614))
- Pick up fixes to the GAPIC generator. ([#6501](https://github.com/googleapis/google-cloud-python/pull/6501))
- Fix client_info bug, update docstrings and timeouts. ([#6416](https://github.com/googleapis/google-cloud-python/pull/6416))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Docstring changes, 'account' -> 'workspace', via synth. ([#6461](https://github.com/googleapis/google-cloud-python/pull/6461))
- Add 'dropped_labels', 'span_context', plus docstring changes. ([#6358](https://github.com/googleapis/google-cloud-python/pull/6358))
- Fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Harmonize / DRY 'monitoring/README.rst' / 'monitoring/docs/index.rst'. ([#6156](https://github.com/googleapis/google-cloud-python/pull/6156))

### Internal / Testing Changes
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Fix long lines from autosynth ([#5961](https://github.com/googleapis/google-cloud-python/pull/5961)
- Test pandas under all supported Python versions ([#5858](https://github.com/googleapis/google-cloud-python/pull/5858))

## 0.30.1

### Implementation Changes
- Monitoring: Add Transports Layer to clients (#5594)
- Remove gRPC size restrictions (4MB default) (#5594)

### Documentation
- Monitoring. Update documentation links. (#5557)

## 0.30.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Add aliases for new V3 service clients. (#5424)

### Documentation
- Remove link to `usage` on index of monitoring (#5272)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 0.29.0

### Implementation Changes
- Update monitoring library to use new generated client (#5212)
- Move aligner and reducer links from timeSeries.list to alertPolicies (#5011)

### Internal / Testing Changes
- Fix bad trove classifier

## 0.28.1

### Implementation changes

- Convert label values to str in client.metric() (#4910)

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-monitoring/0.28.0/
