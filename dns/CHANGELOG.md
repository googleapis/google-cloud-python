# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dns/#history

## 0.29.1

12-10-2018 12:50 PST


### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix 'Datastore' in text as well as examples / links

### Internal / Testing Changes
- add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Fix copy-pasta from datastore README. ([#6208](https://github.com/googleapis/google-cloud-python/pull/6208))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Prep dns docs for repo split. ([#6020](https://github.com/googleapis/google-cloud-python/pull/6020))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier

## 0.29.0

### Implementation changes

- Renaming `makeResource` -> `make_resource`. (#4355)

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

PyPI: https://pypi.org/project/google-cloud-dns/0.28.0/
