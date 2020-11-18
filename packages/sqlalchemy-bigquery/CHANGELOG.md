# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/pybigquery/#history

## 0.5.0

2020-11-18

### Features

- Support the `ARRAY` data type in generated DDL. ([#64](https://github.com/mxmzdlv/pybigquery/pull/64))
- Support project ID and dataset ID in `schema` argument. ([#63](https://github.com/mxmzdlv/pybigquery/pull/63]))
- Implement `get_view_names()` method. ([#62](https://github.com/mxmzdlv/pybigquery/pull/62), [#60](https://github.com/mxmzdlv/pybigquery/issues/60))

### Bug Fixes

- Ignore no-op nested labels. ([#47](https://github.com/mxmzdlv/pybigquery/pull/47))

### Development

- Use flake8 for code style checks. ([#71](https://github.com/mxmzdlv/pybigquery/pull/71))

## 0.4.15

2020-04-23

### Implementation Changes

- Prefer explicitly provided dataset over default dataset in lookup. ([#53](https://github.com/mxmzdlv/pybigquery/pull/53))
- Use the provided `project_id` when using a service account. ([#52](https://github.com/mxmzdlv/pybigquery/pull/52))
