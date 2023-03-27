# Changelog

## [0.6.1](https://github.com/googleapis/python-gke-multicloud/compare/v0.6.0...v0.6.1) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#66](https://github.com/googleapis/python-gke-multicloud/issues/66)) ([cabb6f7](https://github.com/googleapis/python-gke-multicloud/commit/cabb6f70c159dd06f34b03bff36f005d0cc08d35))

## [0.6.0](https://github.com/googleapis/python-gke-multicloud/compare/v0.5.1...v0.6.0) (2023-02-02)


### Features

* Added `reconciling` and `update_time` output fields to Azure Client resource. ([76ed673](https://github.com/googleapis/python-gke-multicloud/commit/76ed673d5438471fa90cf2a1cd3f721b1efdada1))
* Added support for Azure workload identity federation ([76ed673](https://github.com/googleapis/python-gke-multicloud/commit/76ed673d5438471fa90cf2a1cd3f721b1efdada1))

## [0.5.1](https://github.com/googleapis/python-gke-multicloud/compare/v0.5.0...v0.5.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([970b8d3](https://github.com/googleapis/python-gke-multicloud/commit/970b8d3a969d936e617d911de276816ec90a278a))


### Documentation

* Add documentation for enums ([970b8d3](https://github.com/googleapis/python-gke-multicloud/commit/970b8d3a969d936e617d911de276816ec90a278a))

## [0.5.0](https://github.com/googleapis/python-gke-multicloud/compare/v0.4.0...v0.5.0) (2023-01-12)


### Features

* Add support for python 3.11 ([#48](https://github.com/googleapis/python-gke-multicloud/issues/48)) ([e9ac58a](https://github.com/googleapis/python-gke-multicloud/commit/e9ac58ad64daa6ffdd0b346cbdff8a72a775908e))

## [0.4.0](https://github.com/googleapis/python-gke-multicloud/compare/v0.3.0...v0.4.0) (2023-01-04)


### Features

* Add AWS Autoscaling Group metrics collection for AWS nodepools ([3f1fa55](https://github.com/googleapis/python-gke-multicloud/commit/3f1fa55dcd74aa91dc4cf68302aa94720529e953))
* Add errors output fields for cluster and nodepool resources ([3f1fa55](https://github.com/googleapis/python-gke-multicloud/commit/3f1fa55dcd74aa91dc4cf68302aa94720529e953))
* Add monitoring config ([3f1fa55](https://github.com/googleapis/python-gke-multicloud/commit/3f1fa55dcd74aa91dc4cf68302aa94720529e953))
* Support AttachedClusters ([3f1fa55](https://github.com/googleapis/python-gke-multicloud/commit/3f1fa55dcd74aa91dc4cf68302aa94720529e953))

## [0.3.0](https://github.com/googleapis/python-gke-multicloud/compare/v0.2.2...v0.3.0) (2022-12-15)


### Features

* Add support for `google.cloud.gke_multicloud.__version__` ([de41e74](https://github.com/googleapis/python-gke-multicloud/commit/de41e74ea9308d01af05605d128d7feeea33b209))
* Add typing to proto.Message based class attributes ([de41e74](https://github.com/googleapis/python-gke-multicloud/commit/de41e74ea9308d01af05605d128d7feeea33b209))


### Bug Fixes

* Add dict typing for client_options ([de41e74](https://github.com/googleapis/python-gke-multicloud/commit/de41e74ea9308d01af05605d128d7feeea33b209))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([71ad415](https://github.com/googleapis/python-gke-multicloud/commit/71ad41570864c1617ee6d4d5e33f07c037a8dba2))
* Drop usage of pkg_resources ([71ad415](https://github.com/googleapis/python-gke-multicloud/commit/71ad41570864c1617ee6d4d5e33f07c037a8dba2))
* Fix timeout default values ([71ad415](https://github.com/googleapis/python-gke-multicloud/commit/71ad41570864c1617ee6d4d5e33f07c037a8dba2))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([de41e74](https://github.com/googleapis/python-gke-multicloud/commit/de41e74ea9308d01af05605d128d7feeea33b209))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([71ad415](https://github.com/googleapis/python-gke-multicloud/commit/71ad41570864c1617ee6d4d5e33f07c037a8dba2))

## [0.2.2](https://github.com/googleapis/python-gke-multicloud/compare/v0.2.1...v0.2.2) (2022-10-10)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#34](https://github.com/googleapis/python-gke-multicloud/issues/34)) ([36ffc90](https://github.com/googleapis/python-gke-multicloud/commit/36ffc90db52dfd0a90d26fd4c8c7bbac74269058))
* **deps:** require google-api-core&gt;=1.33.2 ([36ffc90](https://github.com/googleapis/python-gke-multicloud/commit/36ffc90db52dfd0a90d26fd4c8c7bbac74269058))

## [0.2.1](https://github.com/googleapis/python-gke-multicloud/compare/v0.2.0...v0.2.1) (2022-10-03)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#31](https://github.com/googleapis/python-gke-multicloud/issues/31)) ([8c73990](https://github.com/googleapis/python-gke-multicloud/commit/8c739901554b87048125d308ded429de4006b025))

## [0.2.0](https://github.com/googleapis/python-gke-multicloud/compare/v0.1.1...v0.2.0) (2022-09-16)


### Features

* Add support for REST transport ([#23](https://github.com/googleapis/python-gke-multicloud/issues/23)) ([763dbc4](https://github.com/googleapis/python-gke-multicloud/commit/763dbc4c4defe4888c815e7c8f6b42a6b8f63468))


### Bug Fixes

* **deps:** require google-api-core>=1.33.1,>=2.8.0 ([763dbc4](https://github.com/googleapis/python-gke-multicloud/commit/763dbc4c4defe4888c815e7c8f6b42a6b8f63468))
* **deps:** require protobuf >= 3.20.1 ([763dbc4](https://github.com/googleapis/python-gke-multicloud/commit/763dbc4c4defe4888c815e7c8f6b42a6b8f63468))

## [0.1.1](https://github.com/googleapis/python-gke-multicloud/compare/v0.1.0...v0.1.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#10](https://github.com/googleapis/python-gke-multicloud/issues/10)) ([d5f33a6](https://github.com/googleapis/python-gke-multicloud/commit/d5f33a6c9a3ecfe6c8eb1feacefe367bf8b92afb))
* **deps:** require proto-plus >= 1.22.0 ([d5f33a6](https://github.com/googleapis/python-gke-multicloud/commit/d5f33a6c9a3ecfe6c8eb1feacefe367bf8b92afb))

## 0.1.0 (2022-07-08)


### Features

* generate v1 ([eb3bd85](https://github.com/googleapis/python-gke-multicloud/commit/eb3bd8516f44889a652422961d38aa5cf4352074))
