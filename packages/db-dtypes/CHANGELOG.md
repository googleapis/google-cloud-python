# Changelog

## [0.3.0](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.2.0...v0.3.0) (2021-11-08)


### Features

* support conversion from pyarrow RecordBatch to pandas DataFrame ([#39](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/39)) ([facc7b0](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/facc7b0897e27c5ba99399b7d453818c5b4aeca7))
* support Python 3.10 ([#40](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/40)) ([a31d55d](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/a31d55db57b2f5655b1fee4230a930d5bee4b1c9))

## [0.2.0](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.1.1...v0.2.0) (2021-10-14)


### Features

* rename dbtime and dbdate dtypes to avoid future conflicts with pandas ([#32](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/32)) ([50ea0f7](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/50ea0f798548aa2f0516f6afc93ba6e80cc0e6d9))


### Documentation

* add how-to guide and include API reference ([#33](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/33)) ([878dce4](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/878dce48bd6714706a2a829775ce00e61724fc7a))

### [0.1.1](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.1.0...v0.1.1) (2021-10-04)


### Bug Fixes

* avoid rounding problems with microseconds ([#20](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/20)) ([0ff7371](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/0ff737120344602f49889596b1efa69a6a18a057))

## 0.1.0 (2021-09-29)


### Features

* add `time` and `date` dtypes ([f104171](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/f10417111642e8f5f4b9af790367af930d15a056))


### Bug Fixes

* support converting empty `time` Series to pyarrow Array ([#11](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/11)) ([7675b15](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/7675b157feb842628fa731cc6a472aa9e6b92903))
* support Pandas 0.24 ([#8](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/8)) ([e996883](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/e996883bc9c76fe5f593e9c19a9d2a1c13501f5e))
