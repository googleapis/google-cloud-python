# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-core/#history

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
