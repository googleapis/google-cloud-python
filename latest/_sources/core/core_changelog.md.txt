# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-core/#history

## 1.0.3

07-26-2019 10:34 PDT


### Implementation Changes
- Make `Client.build_api_url` an instance method. ([#8747](https://github.com/googleapis/google-cloud-python/pull/8747))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Linkify the PR in the change log. ([#8790](https://github.com/googleapis/google-cloud-python/pull/8790))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Removing typing information for `**kwargs` in order to not conflict with type checkers. ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))

### Internal / Testing Changes
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 1.0.2

06/11/2019 15:19 PDT

### Internal Changes 
- Prevent requests from hanging on SSL handshake issue by adding a max timeout of 5 minutes. ([#8207](https://github.com/googleapis/google-cloud-python/pull/8207))

## 1.0.1

05-28-2019 11:22 PDT

### Dependencies
- Pin `grpcio < 2.0dev`. ([#8182](https://github.com/googleapis/google-cloud-python/pull/8182))

## 1.0.0

05-15-2019 13:09 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Refactor `client_info` support. ([#7849](https://github.com/googleapis/google-cloud-python/pull/7849))

### Dependencies
- Update dep on `api_core` >= 1.11.0. ([#7986](https://github.com/googleapis/google-cloud-python/pull/7986))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 0.29.1

12-17-2018 16:35 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 0.29.0

12-03-2018 15:54 PST

### Breaking Changes
- Remove iam module from core. This module is now available as part of google-api-core. ([#6775](https://github.com/googleapis/google-cloud-python/pull/6775))

### Implementation Changes
- Fix `_time_from_iso8601_time_naive` for values with micros. ([#5756](https://github.com/googleapis/google-cloud-python/pull/5756))
- Import stdlib ABCs from `collections.abc` rather than `collections`. ([#6451](https://github.com/googleapis/google-cloud-python/pull/6451))

### Dependencies
- Bump minimum `api_core` version to 1.0.0. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

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
