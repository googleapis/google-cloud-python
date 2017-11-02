# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-language/#history

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
