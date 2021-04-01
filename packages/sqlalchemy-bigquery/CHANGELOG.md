# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/pybigquery/#history

### [0.5.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.5.0...v0.5.1) (2021-04-01)


### Bug Fixes

* avoid 404 if dataset is deleted while listing tables or views ([#106](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/106)) ([db379d8](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/db379d850b916149db5976689d6f2323d2281f7a))


### Documentation

* add templates for move to googleapis/python-bigquery-sqlalchemy repo ([#88](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/88)) ([37e584e](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/37e584e05db6316b4abd41ebc08486047d2c49b8))
* build documentation with Sphinx ([#97](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/97)) ([1707737](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/1707737c60997e9714387c8077727eb5918626bb))

## 0.5.0

2020-11-18

### ⚠️ Breaking Changes ⚠️ 

- `get_table_names()` no longer returns views. ([#62](https://github.com/mxmzdlv/pybigquery/pull/62), [#60](https://github.com/mxmzdlv/pybigquery/issues/60))

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
