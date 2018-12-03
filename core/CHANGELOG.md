# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-core/#history

## 0.29.0

12-03-2018 15:54 PST

### Breaking Changes
- Remove iam module from core. ([#6775](https://github.com/googleapis/google-cloud-python/pull/6775))

### Implementation Changes
- Fix '_time_from_iso8601_time_naive' for values with micros. ([#5756](https://github.com/googleapis/google-cloud-python/pull/5756))
- Import stdlib ABCs from 'collections.abc' rather than 'collections'. ([#6451](https://github.com/googleapis/google-cloud-python/pull/6451))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Internal / Testing Changes
- Blacken api_core and core. ([#6668](https://github.com/googleapis/google-cloud-python/pull/6668))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox. ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Use inplace installs for nox ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Fix bad trove classifier.
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))

## 0.28.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- Requiring 'grpcio >= 1.8.2'. (#4642)

### Documentation

- DefaultCredentialsError could be raised if credentials not supplied (#4688)
- Unreachable links in the readme files have been fixed. (#4406)
- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Notable Implementation Changes

- A large portion of the implementation has moved into
  [`google-api-core`][2] (#4022, #4041, #4057, #4067,
  #4069, #4079, #4081, #4166, #4221)

### Dependencies

- Explicit depending on `google-api-core` and upgrading to
  `grpcio >= 1.7.0` (see #4096, #4280 and
  https://github.com/grpc/grpc/issues/12455)

### Interface changes / additions

- Rename `google.cloud.obselete` module to
  `obsolete` (#3913, h/t to @dimaqq)

PyPI: https://pypi.org/project/google-cloud-core/0.28.0/

[2]: https://pypi.org/project/google-api-core/
