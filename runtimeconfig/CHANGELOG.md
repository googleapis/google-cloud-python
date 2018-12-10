# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-runtimeconfig/#history

## 0.28.2

12-10-2018 13:05 PST


### Implementation Changes
- Use moved `iam.policy` now at `google.api_core.iam.policy` ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Fix variable nanosecond timestamp `update_time` from response ([#4819](https://github.com/googleapis/google-cloud-python/pull/4819))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix [#6321](https://github.com/googleapis/google-cloud-python/pull/6321) Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Prep docs for repo split. ([#6023](https://github.com/googleapis/google-cloud-python/pull/6023))

### Internal / Testing Changes
- Add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Add tests with microseconds and nanoseconds ([#5150](https://github.com/googleapis/google-cloud-python/pull/5150))
- Fix bad trove classifier

## 0.28.1

### Implementation changes

- Set default variable state to Unspecified (#4738)

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
- Fix example in `Config.get_variable()` (#3910)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-runtimeconfig/0.28.0/
