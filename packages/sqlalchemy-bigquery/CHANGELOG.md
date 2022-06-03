# Changelog

Older versions of this project were distributed as [pybigquery][0].

[0]: https://pypi.org/project/pybigquery

[sqlalchemy-bigquery PyPI History][1]

[1]: https://pypi.org/project/sqlalchemy-bigquery/#history


[pybigquery PyPI History][2]

[2]: https://pypi.org/project/pybigquery/#history


## [1.4.3](https://github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.4.2...v1.4.3) (2022-03-22)


### Bug Fixes

* correct license text from Apache to MIT ([#436](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/436)) ([dbf7501](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/dbf7501c26157d3776f5a68254898758ee43a667))

## [1.4.2](https://github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.4.1...v1.4.2) (2022-03-22)


### Bug Fixes

* use explicit rather than implicit relative imports ([#433](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/433)) ([ca20d3d](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/ca20d3d20939b780abe49dfc833375eecd31ae04))
* use faux_conn rather than engine in unit tests ([#431](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/431)) ([275506f](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/275506f0c9b7ac0e67410dbd7ceab8c9f593a259))


### Dependencies

* require google-cloud-bigquery-storage to avoid performance warning ([#414](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/414)) ([ff3273f](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/ff3273feacfa1f34bb9090f28f11c2ac470759fc))

## [1.4.1](https://github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.4.0...v1.4.1) (2022-03-07)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#419](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/419)) ([52339f7](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/52339f70340eb8f497c816f36f71c8232928e57b))

## [1.4.0](https://github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.3.0...v1.4.0) (2022-02-22)


### Features

* Allow base64 encoded credentials in URI ([#410](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/410)) ([e2f9821](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/e2f9821e66507ee3ac3260d9c1b0ba899cf2efc4))


### Bug Fixes

* POSTCOMPILE expansion in SQLAlchemy 1.4.27+ ([#408](https://github.com/googleapis/python-bigquery-sqlalchemy/issues/408)) ([7844813](https://github.com/googleapis/python-bigquery-sqlalchemy/commit/7844813c6eb3a52cc9d3e91e88d5f8ecebba08c5))

## [1.3.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.2.2...v1.3.0) (2021-12-31)


### Features

* Enable support for 3.10 ([#381](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/381)) ([4b3505b](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/4b3505b3d3a4293ea127fc3c483e3e7de04fbd04))

## [1.2.2](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.2.1...v1.2.2) (2021-10-29)


### Bug Fixes

* avoid aliasing known tables used in CTEs ([#369](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/369)) ([4b05d21](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/4b05d21b8dc89339a69df87183f8893bf02459c5))

## [1.2.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.2.0...v1.2.1) (2021-10-27)


### Bug Fixes

* avoid creating aliases for already-known tables ([#361](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/361)) ([1ce4e14](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/1ce4e14c81a4b378dfcfba808507e6c545f34841))
* avoid scribbling on (reused) bind param ([#365](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/365)) ([d28cac5](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/d28cac5864f183c0ca503854973d837b17783d52))
* include external tables in 'get_table_names' ([#363](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/363)) ([5e158fe](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/5e158fe8bb2394369c020337092b5cfdb01880e0))

## [1.2.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.1.0...v1.2.0) (2021-09-09)


### Features

* STRUCT and ARRAY support ([#318](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/318)) ([6624b10](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/6624b10ded73bbca6f40af73aaeaceb95c381b63))


### Bug Fixes

* the unnest function lost needed type information ([#298](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/298)) ([1233182](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/123318269876e7f76c7f0f2daa5f5b365026cd3f))

## [1.1.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.0.0...v1.1.0) (2021-08-25)


### Features

* Add geography support ([#228](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/228)) ([da7a403](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/da7a40309de6ca8063d6dcf6678de96a463344e6))
* Handle passing of arrays to in statements more efficiently in SQLAlchemy 1.4 and higher ([#253](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/253)) ([7692704](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/76927044aa4d2be9d0f2ec47e917b28b97c18425))


### Bug Fixes

* dialect atribute wasn't provided ([#291](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/291)) ([2cf05a0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/2cf05a0f37e32344b29ba2e92d709f7e51b20916))
* distinct doesn't work as a column wrapper ([#275](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/275)) ([ad5baf8](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/ad5baf8a5351b9cdac4eda243e4042aeb551b937))
* in-operator literal binds not handled properly ([#285](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/285)) ([e06bf74](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/e06bf74310fa27d5bc775e13beed4ab3a520e1aa))
* supports_multivalues_insert dialect option was mispelled ([#278](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/278)) ([ec36a12](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/ec36a120c1607d9769105e873550bb727c504c93))
* unnest failed in some cases (with table references failed when there were no other references to refrenced tables in a query) ([#290](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/290)) ([9b5b002](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/9b5b0025ec0b65177c0df02013ac387b3d3de472))

## [1.0.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v1.0.0-a1...v1.0.0) (2021-08-17)


### Miscellaneous Chores

* release 1.0.0 ([#249](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/249)) ([d23ae1d](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/d23ae1d2a8ad3c466e08b03f167c8c49b39579d0))

## [1.0.0-a1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.10.1...v1.0.0-a1) (2021-08-11)


### Features

* Rename pybigquery to sqlalchemy-bigquery ([#198](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/198)) ([a6f0a5d](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/a6f0a5d77053be528a6b6805cb1ff3c8ec465f5e))


### Miscellaneous Chores

* release 1.0.0-a1 ([#238](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/238)) ([b630293](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/b6302937b0c5e2314de7e90c02d74af08e5b17a0))

## [pybigquery 0.10.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.10.0...v0.10.1) (2021-07-30)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#220](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/220)) ([bf1f47c](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/bf1f47c794e747a2ea878347322c040636e8c2d4))

## [pybigquery 0.10.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.9.1...v0.10.0) (2021-07-06)


### Features

* There's a new `page_size` option to control the page size used when listing tables. ([#174](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/174)) ([e0f1496](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/e0f1496c99dd627e0ed04a0c4e89ca5b14611be2))

## [pybigquery 0.9.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.9.0...v0.9.1) (2021-06-25)


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([d52334c](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/d52334c3290d8356a26e1c9fc54dae75854410c9))

## [pybigquery 0.9.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.8.0...v0.9.0) (2021-05-25)


### Features

* Alembic support ([#183](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/183)) ([4d5a17c](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/4d5a17c8f63328d4484ea7b2ccc58334a421ba81))
* Support parameterized NUMERIC, BIGNUMERIC, STRING, and BYTES types ([#180](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/180)) ([d118238](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/d1182385b9f1551e605acdc7e2dd45dff22c8064))

## [pybigquery 0.8.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.7.0...v0.8.0) (2021-05-21)


### Features

* Add support for SQLAlchemy 1.4 ([#177](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/177)) ([b7b6000](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/b7b60007c966cd548448d1d6fd5a14d1f89480cd))

## [pybigquery 0.7.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.6.1...v0.7.0) (2021-05-12)


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


## [pybigquery 0.6.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.6.0...v0.6.1) (2021-04-12)


### Bug Fixes

* use `project_id` property from service account credentials ([#120](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/120)) ([ab2051d](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/ab2051de3097adb68503c01a87f9a91092711d2a))

## [pybigquery 0.6.0](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.5.1...v0.6.0) (2021-04-06)


### Features

* fetch table and column descriptions during reflection ([#115](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/115)) ([7b14a06](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/7b14a06f71f113af0e2970898bc0ec203e4e6464))


### Bug Fixes

* correct classifiers in `setup.py` ([#107](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/107)) ([0cfc5de](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/0cfc5de467823998ba72af1fee1d2a8aa865fabc))

## [pybigquery 0.5.1](https://www.github.com/googleapis/python-bigquery-sqlalchemy/compare/v0.5.0...v0.5.1) (2021-04-01)


### Bug Fixes

* avoid 404 if dataset is deleted while listing tables or views ([#106](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/106)) ([db379d8](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/db379d850b916149db5976689d6f2323d2281f7a))


### Documentation

* add templates for move to googleapis/python-bigquery-sqlalchemy repo ([#88](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/88)) ([37e584e](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/37e584e05db6316b4abd41ebc08486047d2c49b8))
* build documentation with Sphinx ([#97](https://www.github.com/googleapis/python-bigquery-sqlalchemy/issues/97)) ([1707737](https://www.github.com/googleapis/python-bigquery-sqlalchemy/commit/1707737c60997e9714387c8077727eb5918626bb))

## pybigquery 0.5.0 (2020-11-18)

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

## pybigquery 0.4.15 (2020-04-23)

### Implementation Changes

- Prefer explicitly provided dataset over default dataset in lookup. ([#53](https://github.com/mxmzdlv/pybigquery/pull/53))
- Use the provided `project_id` when using a service account. ([#52](https://github.com/mxmzdlv/pybigquery/pull/52))
