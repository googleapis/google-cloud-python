# Changelog

## [1.0.1](https://github.com/googleapis/python-db-dtypes-pandas/compare/v1.0.0...v1.0.1) (2022-05-07)


### Bug Fixes

* **deps:** allow pyarrow v8 ([#109](https://github.com/googleapis/python-db-dtypes-pandas/issues/109)) ([fb30adf](https://github.com/googleapis/python-db-dtypes-pandas/commit/fb30adfd427d3df9919df00b096210ba1eb1b91d))

## [1.0.0](https://github.com/googleapis/python-db-dtypes-pandas/compare/v0.4.0...v1.0.0) (2022-03-25)


### Features

* label package as generally available ([#92](https://github.com/googleapis/python-db-dtypes-pandas/issues/92)) ([0363e87](https://github.com/googleapis/python-db-dtypes-pandas/commit/0363e8725b322881c1fe1e89bdeadd0f67317d22))

## [0.4.0](https://github.com/googleapis/python-db-dtypes-pandas/compare/v0.3.1...v0.4.0) (2022-03-24)


### ⚠ BREAKING CHANGES

* dbdate and dbtime dtypes return NaT instead of None for missing values

### Features

* dbdate and dbtime support numpy.datetime64 values in array constructor ([1db1357](https://github.com/googleapis/python-db-dtypes-pandas/commit/1db1357186b234a28b2ced10174bbd06e2f0ab73))


### Bug Fixes

* address failing 2D array compliance tests  in DateArray ([#64](https://github.com/googleapis/python-db-dtypes-pandas/issues/64)) ([b771e05](https://github.com/googleapis/python-db-dtypes-pandas/commit/b771e050acd2bdbf469a97f7477036c159b500f8))
* address failing tests with pandas 1.5.0 ([#82](https://github.com/googleapis/python-db-dtypes-pandas/issues/82)) ([38ac28d](https://github.com/googleapis/python-db-dtypes-pandas/commit/38ac28d8b16f9b86b5029c85e45e9f2e034159b7))
* allow comparison with scalar values ([#88](https://github.com/googleapis/python-db-dtypes-pandas/issues/88)) ([7495698](https://github.com/googleapis/python-db-dtypes-pandas/commit/7495698b3be3b7e8055ae450e24cd0e366b1b72a))
* avoid TypeError when using sorted search ([#84](https://github.com/googleapis/python-db-dtypes-pandas/issues/84)) ([42bc2d9](https://github.com/googleapis/python-db-dtypes-pandas/commit/42bc2d90174d152dfed782acf77016da55dbdaca))
* correct TypeError and comparison issues discovered in DateArray compliance tests ([#79](https://github.com/googleapis/python-db-dtypes-pandas/issues/79)) ([1e979cf](https://github.com/googleapis/python-db-dtypes-pandas/commit/1e979cf360eb586e77b415f7b710a8a41c22e981))
* dbdate and dbtime support set item with null values ([#85](https://github.com/googleapis/python-db-dtypes-pandas/issues/85)) ([1db1357](https://github.com/googleapis/python-db-dtypes-pandas/commit/1db1357186b234a28b2ced10174bbd06e2f0ab73))
* use `pandas.NaT` for missing values in dbdate and dbtime dtypes ([#67](https://github.com/googleapis/python-db-dtypes-pandas/issues/67)) ([f903c2c](https://github.com/googleapis/python-db-dtypes-pandas/commit/f903c2c68da1629241cf3bf37e1226babae669f4))
* use public pandas APIs where possible ([#60](https://github.com/googleapis/python-db-dtypes-pandas/issues/60)) ([e9d41d1](https://github.com/googleapis/python-db-dtypes-pandas/commit/e9d41d17b5d6a7d83c46e2497feb8e314545adcb))


### Tests

* add dbtime compliance tests ([#90](https://github.com/googleapis/python-db-dtypes-pandas/issues/90)) ([f14fb2b](https://github.com/googleapis/python-db-dtypes-pandas/commit/f14fb2bf78d8427b9546db4cdad1d893c1b1e5e1))
* add final dbdate compliance tests and sort ([#89](https://github.com/googleapis/python-db-dtypes-pandas/issues/89)) ([efe7e6d](https://github.com/googleapis/python-db-dtypes-pandas/commit/efe7e6d8953ebf8d2b4d9468c7c92638ea2ec9f9))

## [0.3.1](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.3.0...v0.3.1) (2021-12-04)


### Bug Fixes

* raise ValueError if date is out-of-bounds ([#46](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/46)) ([4253358](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/4253358b673965f7d2823b750f56553f6627e130))

## [0.3.0](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.2.0...v0.3.0) (2021-11-08)


### Features

* support conversion from pyarrow RecordBatch to pandas DataFrame ([#39](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/39)) ([facc7b0](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/facc7b0897e27c5ba99399b7d453818c5b4aeca7))
* support Python 3.10 ([#40](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/40)) ([a31d55d](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/a31d55db57b2f5655b1fee4230a930d5bee4b1c9))

## [0.2.0](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.1.1...v0.2.0) (2021-10-14)


### Features

* rename dbtime and dbdate dtypes to avoid future conflicts with pandas ([#32](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/32)) ([50ea0f7](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/50ea0f798548aa2f0516f6afc93ba6e80cc0e6d9))


### Documentation

* add how-to guide and include API reference ([#33](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/33)) ([878dce4](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/878dce48bd6714706a2a829775ce00e61724fc7a))

## [0.1.1](https://www.github.com/googleapis/python-db-dtypes-pandas/compare/v0.1.0...v0.1.1) (2021-10-04)


### Bug Fixes

* avoid rounding problems with microseconds ([#20](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/20)) ([0ff7371](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/0ff737120344602f49889596b1efa69a6a18a057))

## 0.1.0 (2021-09-29)


### Features

* add `time` and `date` dtypes ([f104171](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/f10417111642e8f5f4b9af790367af930d15a056))


### Bug Fixes

* support converting empty `time` Series to pyarrow Array ([#11](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/11)) ([7675b15](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/7675b157feb842628fa731cc6a472aa9e6b92903))
* support Pandas 0.24 ([#8](https://www.github.com/googleapis/python-db-dtypes-pandas/issues/8)) ([e996883](https://www.github.com/googleapis/python-db-dtypes-pandas/commit/e996883bc9c76fe5f593e9c19a9d2a1c13501f5e))
