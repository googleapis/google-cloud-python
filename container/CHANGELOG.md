# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-container/#history

## 0.2.0

12-04-2018 11:28 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core.iam.policy` ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes to GAPIC generator. ([#6634](https://github.com/googleapis/google-cloud-python/pull/6634))
- Fix `client_info` bug, update docstrings. ([#6407](https://github.com/googleapis/google-cloud-python/pull/6407))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))
- Fix bad trove classifier

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Container: harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6018](https://github.com/googleapis/google-cloud-python/pull/6018))
- Rename releases to changelog and include from CHANGELOG.md ([#5191](https://github.com/googleapis/google-cloud-python/pull/5191))

### Internal / Testing Changes
- Update noxfile.
- blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local dependencies from coverage. ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack container gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Pass posargs to py.test ([#6653](https://github.com/googleapis/google-cloud-python/pull/6653))
- Update synth.py yaml location ([#6480](https://github.com/googleapis/google-cloud-python/pull/6480))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Container: add 'synth.py'. ([#6084](https://github.com/googleapis/google-cloud-python/pull/6084))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Replacing references to `stable/` docs with `latest/`. (#4638)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- nox unittest updates (#4646)

## 0.1.0

[![release level](https://img.shields.io/badge/release%20level-alpha-orange.svg?style&#x3D;flat)](https://cloud.google.com/terms/launch-stages)

Google Kubernetes Engine is a managed environment for deploying containerized
applications. It brings our latest innovations in developer productivity,
resource efficiency, automated operations, and open source flexibility to
accelerate your time to market.

PyPI: https://pypi.org/project/google-cloud-container/0.1.0/
