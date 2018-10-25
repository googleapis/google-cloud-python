# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history

## 1.1.0

10-05-2018 13:52 PDT

### Implementation Changes

- The library has been regenerated to pick up changes in the underlying API.
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))

### Documentation

- Translate / Logging / Language: restore detailed usage docs. ([#5999](https://github.com/googleapis/google-cloud-python/pull/5999))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Prep language docs for repo split. ([#5932](https://github.com/googleapis/google-cloud-python/pull/5932))

### Internal / Testing Changes

- Language: add 'synth.py'. ([#6080](https://github.com/googleapis/google-cloud-python/pull/6080))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Avoid overwriting '__module__' of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))

## 1.0.2

### Packaging
- Update setuptools before packaging (#5265)
- Update setup.py to use recommended method for python-verson specific dependencies (#5266)
- Fix bad trove classifier

## 1.0.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix coveragerc to correctly omit generated files (#4843)

## 1.0.0

[![release level](https://img.shields.io/badge/release%20level-general%20availability%20%28GA%29-brightgreen.svg?style&#x3D;flat)](https://cloud.google.com/terms/launch-stages)

### Features

##### General Availability

The `google-cloud-language` package is now supported at the **general availability** quality level. This means it is stable; the code and API surface will not change in backwards-incompatible ways unless absolutely necessary (e.g. because of critical security issues) or with an extensive deprecation period.

One exception to this: We will remove beta endpoints (as a semver-minor update) at whatever point the underlying endpoints go away.

## 0.31.0

### Release Candidate

  * This update is considered a final "release candidate", and
    the `google-cloud-language` package is preparing for a GA release
    in the near future.

### :warning: Breaking Changes!

  * Some rarely-used arguments to the `LanguageServiceClient` constructor
    have been removed (in favor of a subclass or a custom gRPC channel).
    It is unlikely that you used these, but if you did, then this update
    will represent a breaking change.
      * The removed arguments are: `client_config`, `lib_name`, `lib_version`
        `metrics_headers`, `ssl_credentials`, and `scopes`.

### Features

  * Added the `classify_text` method on the primary (`v1`) endpoint. (#4283)

## 0.30.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-language/0.30.0/
