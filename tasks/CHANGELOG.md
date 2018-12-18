# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-tasks/#history

## 0.4.0

12-18-2018 09:50 PST


### Implementation Changes
- Use moved iam.policy now at google.api_core.iam.policy ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6616](https://github.com/googleapis/google-cloud-python/pull/6616))
- Fix client_info bug, update docstrings and timeouts. ([#6422](https://github.com/googleapis/google-cloud-python/pull/6422))
- Re-generate library using tasks/synth.py ([#5980](https://github.com/googleapis/google-cloud-python/pull/5980))

### New Features
- Pick up changes to GAPIC generator, drop 'Code' enum. ([#6509](https://github.com/googleapis/google-cloud-python/pull/6509))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Separate / distinguish API docs for different API versions. ([#6306](https://github.com/googleapis/google-cloud-python/pull/6306))
- Docstring tweaks from protos. ([#6261](https://github.com/googleapis/google-cloud-python/pull/6261))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Remove autosynth / tweaks for 'README.rst' / 'setup.py'. ([#5957](https://github.com/googleapis/google-cloud-python/pull/5957))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

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

