# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-core/#history

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
