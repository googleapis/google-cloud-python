# Changelog

### [2.2.2](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v2.2.1...v2.2.2) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#93](https://www.github.com/googleapis/python-monitoring-dashboards/issues/93)) ([eef0a3e](https://www.github.com/googleapis/python-monitoring-dashboards/commit/eef0a3e274d29c1c7aad0799763c935b2ff4feb1))
* enable self signed jwt for grpc ([#99](https://www.github.com/googleapis/python-monitoring-dashboards/issues/99)) ([0a8b547](https://www.github.com/googleapis/python-monitoring-dashboards/commit/0a8b547f8692e2158bbb1de539db7efc4bb96c4c))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#94](https://www.github.com/googleapis/python-monitoring-dashboards/issues/94)) ([017fcbd](https://www.github.com/googleapis/python-monitoring-dashboards/commit/017fcbd4ac623c25e56ab2161f651a3999442f9d))


### Miscellaneous Chores

* release as 2.2.2 ([#98](https://www.github.com/googleapis/python-monitoring-dashboards/issues/98)) ([3266da2](https://www.github.com/googleapis/python-monitoring-dashboards/commit/3266da2924b0b56ef7892c78700ccf7242efab0a))

### [2.2.1](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v2.2.0...v2.2.1) (2021-07-14)


### Documentation

* fixed broken links ([#90](https://www.github.com/googleapis/python-monitoring-dashboards/issues/90)) ([59cd222](https://www.github.com/googleapis/python-monitoring-dashboards/commit/59cd222eb61b03b421ceb07b9506571ae17826ae))

## [2.2.0](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v2.1.0...v2.2.0) (2021-07-09)


### Features

* add always_use_jwt_access ([#80](https://www.github.com/googleapis/python-monitoring-dashboards/issues/80)) ([a907b7d](https://www.github.com/googleapis/python-monitoring-dashboards/commit/a907b7dcf6d7b5013950e4f3457ce6a11ebb382c))
* added alert chart widget ([509abf5](https://www.github.com/googleapis/python-monitoring-dashboards/commit/509abf5b4354225b9383a59b748ca4498b524757))
* added validation only mode when writing dashboards ([#86](https://www.github.com/googleapis/python-monitoring-dashboards/issues/86)) ([509abf5](https://www.github.com/googleapis/python-monitoring-dashboards/commit/509abf5b4354225b9383a59b748ca4498b524757))


### Bug Fixes

* disable always_use_jwt_access ([#84](https://www.github.com/googleapis/python-monitoring-dashboards/issues/84)) ([d9b1482](https://www.github.com/googleapis/python-monitoring-dashboards/commit/d9b148215d701339263cf515dafc255f1ddf0b7e))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-monitoring-dashboards/issues/1127)) ([#75](https://www.github.com/googleapis/python-monitoring-dashboards/issues/75)) ([f267b35](https://www.github.com/googleapis/python-monitoring-dashboards/commit/f267b356fefab3bc79c8d001ae14158a75b95f72)), closes [#1126](https://www.github.com/googleapis/python-monitoring-dashboards/issues/1126)

## [2.1.0](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v2.0.0...v2.1.0) (2021-05-22)


### Features

* add `from_service_account_info` ([bd08227](https://www.github.com/googleapis/python-monitoring-dashboards/commit/bd08227d21ddc68afa3622328ea6660630c3087c))
* add MosaicLayout  ([#47](https://www.github.com/googleapis/python-monitoring-dashboards/issues/47)) ([bd08227](https://www.github.com/googleapis/python-monitoring-dashboards/commit/bd08227d21ddc68afa3622328ea6660630c3087c))


### Bug Fixes

* **deps:** add packaging requirement ([#67](https://www.github.com/googleapis/python-monitoring-dashboards/issues/67)) ([80c2b62](https://www.github.com/googleapis/python-monitoring-dashboards/commit/80c2b6279611c3051aa2bc1b7013919f2587780f))

## [2.0.0](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v1.0.0...v2.0.0) (2021-02-11)


### ⚠ BREAKING CHANGES

* move API to python microgenerator. See [Migration Guide](https://github.com/googleapis/python-monitoring-dashboards/blob/main/UPGRADING.md). (#26)

### Features

* add common resource helper methods; expose client transport ([#34](https://www.github.com/googleapis/python-monitoring-dashboards/issues/34)) ([8e00d80](https://www.github.com/googleapis/python-monitoring-dashboards/commit/8e00d80b19618d42e79833cff20e2f62c08fcede))
* add support for secondary aggregation and Monitoring Query Language ([#22](https://www.github.com/googleapis/python-monitoring-dashboards/issues/22)) ([8ed9094](https://www.github.com/googleapis/python-monitoring-dashboards/commit/8ed9094df80db87caa9852279be76d69783dc9c3))
* move API to python microgenerator ([#26](https://www.github.com/googleapis/python-monitoring-dashboards/issues/26)) ([b5c1549](https://www.github.com/googleapis/python-monitoring-dashboards/commit/b5c15496bea5442524df67c56c0680f38cd8eb79))


### Bug Fixes

* remove client recv msg limit fix: add enums to `types/__init__.py` ([#37](https://www.github.com/googleapis/python-monitoring-dashboards/issues/37)) ([774660a](https://www.github.com/googleapis/python-monitoring-dashboards/commit/774660a7f4aafece9fa6d49a806efd431f509ab3))

## [1.0.0](https://www.github.com/googleapis/python-monitoring-dashboards/compare/v0.1.0...v1.0.0) (2020-05-19)


### Features

* release as production/stable ([#17](https://www.github.com/googleapis/python-monitoring-dashboards/issues/17)) ([613dd31](https://www.github.com/googleapis/python-monitoring-dashboards/commit/613dd31d05ba1d0c7075778520c7b9fd3f49bc29)), closes [#16](https://www.github.com/googleapis/python-monitoring-dashboards/issues/16)

## 0.1.0 (2020-01-15)


### Features

* initial generation of library ([1a6e4ea](https://www.github.com/googleapis/python-monitoring-dashboards/commit/1a6e4ea8c4e73d05f165f12f334590b79a14f041))


### Bug Fixes

* add setup.py ([3e2cc60](https://www.github.com/googleapis/python-monitoring-dashboards/commit/3e2cc60ce843ea3d51dfb83d4fec5d578fe59cef))
