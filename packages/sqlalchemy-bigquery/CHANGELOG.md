# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/pybigquery/#history

## [0.9.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.8.0...v0.9.0) (2021-05-25)


### Features

* Alembic support ([#183](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/183)) ([4d5a17c](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/4d5a17c8f63328d4484ea7b2ccc58334a421ba81))
* Support parameterized NUMERIC, BIGNUMERIC, STRING, and BYTES types ([#180](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/180)) ([d118238](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/d1182385b9f1551e605acdc7e2dd45dff22c8064))

## [0.8.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.7.0...v0.8.0) (2021-05-21)


### Features

* Add support for SQLAlchemy 1.4 ([#177](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/177)) ([b7b6000](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/b7b60007c966cd548448d1d6fd5a14d1f89480cd))

## [0.7.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.6.1...v0.7.0) (2021-05-12)


### Features

* Comment/description support, bug fixes and better test coverage ([#138](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/138)) ([fb7c188](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/fb7c188fd1d61f2bb2b99742f62042576bff02a9))
  * Runs SQLAlchemy dialect-compliance tests (as system tests).
  * 100% unit-test coverage.
  * Support for table and column comments/descriptions (requiring SQLAlchemy 1.2 or higher).
  * When executing parameterized queries, the new BigQuery DB API parameter syntax is used to pass type information.  This is helpful when the DB API can't determine type information from values, or can't determine it correctly.

### Bug Fixes

* Select expressions no-longer force use of labels ([#129](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/129)) ([669b301](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/669b301359f9f37c5c7286a245080b8af2567186))

* Additional fixes, including:
  - Handling of `in` queries.
  - String literals with special characters.
  - Use BIGNUMERIC when necessary.
  - Missing types: BIGINT, SMALLINT, Boolean, REAL, CHAR, NCHAR, VARCHAR, NVARCHAR, TEXT, VARBINARY, DECIMAL
  - Literal bytes, dates, times, datetimes, timestamps, and arrays.
  - Get view definitions.


### [0.6.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.6.0...v0.6.1) (2021-04-12)


### Bug Fixes

* use `project_id` property from service account credentials ([#120](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/120)) ([ab2051d](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/ab2051de3097adb68503c01a87f9a91092711d2a))

## [0.6.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.5.1...v0.6.0) (2021-04-06)


### Features

* fetch table and column descriptions during reflection ([#115](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/115)) ([7b14a06](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/7b14a06f71f113af0e2970898bc0ec203e4e6464))


### Bug Fixes

* correct classifiers in `setup.py` ([#107](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/107)) ([0cfc5de](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/0cfc5de467823998ba72af1fee1d2a8aa865fabc))

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
