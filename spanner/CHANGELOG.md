# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-spanner/#history

## 0.29.0

### Implementation Changes

- **Bugfix**: Clear `session._transaction` before calling
  `_delay_until_retry` (#4185)
- **Bugfix**: Be permissive about merging an empty list. (#4170,
  fixes #4164)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-spanner/0.29.0/
