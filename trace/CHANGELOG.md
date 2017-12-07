# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-trace/#history

## 0.17.0

### Notable Implementation Changes

- Default to use Stackdriver Trace V2 API if calling `from google.cloud import trace`.
  Using V1 API needs to be explicitly specified in the import.(#4437)

PyPI: https://pypi.org/project/google-cloud-trace/0.17.0/

## 0.16.0

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-trace/0.16.0/
