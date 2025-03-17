# Changelog

## [0.3.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-audit-log-v0.3.1...google-cloud-audit-log-v0.3.2) (2025-03-15)


### Bug Fixes

* Allow protobuf 6.x ([b4d4551](https://github.com/googleapis/google-cloud-python/commit/b4d45514e4ab630334a54eb4201576062ecc1958))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))
* resolve issue where pre-release versions of dependencies are installed ([b4d4551](https://github.com/googleapis/google-cloud-python/commit/b4d45514e4ab630334a54eb4201576062ecc1958))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-audit-log-v0.3.0...google-cloud-audit-log-v0.3.1) (2025-03-06)


### Features

* Updates audit_log proto with PermissionType ([#13616](https://github.com/googleapis/google-cloud-python/issues/13616)) ([04ab652](https://github.com/googleapis/google-cloud-python/commit/04ab652a5bd70647217c839ebfddb0c99e659d7a))

## [0.3.0](https://github.com/googleapis/python-audit-log/compare/v0.2.5...v0.3.0) (2024-08-15)


### Features

* Add `google/cloud/audit/bigquery_audit_metadata_pb2.py` ([c6efc56](https://github.com/googleapis/python-audit-log/commit/c6efc56eec9627ecf1e139cc33d5815937f04dc6))
* Add PolicyViolation. this will only be present when access is denied due to Organization Policy [fc5be6f](https://github.com/googleapis/googleapis/commit/fc5be6f850e7989e912b40c6b79306c6dc9655bd) ([c6efc56](https://github.com/googleapis/python-audit-log/commit/c6efc56eec9627ecf1e139cc33d5815937f04dc6))
* Add support for Python 3.12 ([#113](https://github.com/googleapis/python-audit-log/issues/113)) ([08b0bca](https://github.com/googleapis/python-audit-log/commit/08b0bca0ee634d65bba18c7de102063be17d0958))
* Add the principal field to the ServiceAccountDelegationInfo [ba89dac](https://github.com/googleapis/googleapis/commit/ba89dace27923254d96ab8339b831dc996e2112f) ([c6efc56](https://github.com/googleapis/python-audit-log/commit/c6efc56eec9627ecf1e139cc33d5815937f04dc6))
* Introduce compatibility with native namespace packages ([#117](https://github.com/googleapis/python-audit-log/issues/117)) ([9007e8a](https://github.com/googleapis/python-audit-log/commit/9007e8af7f5300f866f42035c36a9d3fe36ef117))
* Update AuditLog proto to include all new changes in Audit Logging [40292fc](https://github.com/googleapis/googleapis/commit/40292fc8f271f3b8708f9c91c85d7240200893a6) ([c6efc56](https://github.com/googleapis/python-audit-log/commit/c6efc56eec9627ecf1e139cc33d5815937f04dc6))


### Bug Fixes

* **deps:** Require protobuf&gt;=3.20.2, protobuf&lt;6 ([bf1434a](https://github.com/googleapis/python-audit-log/commit/bf1434a7f4c0d03767c6f943de898d5562e874b1))
* Regenerate pb2 files for compatibility with protobuf 5.x ([bf1434a](https://github.com/googleapis/python-audit-log/commit/bf1434a7f4c0d03767c6f943de898d5562e874b1))

## [0.2.5](https://github.com/googleapis/python-audit-log/compare/v0.2.4...v0.2.5) (2023-01-07)


### Bug Fixes

* **deps:** Require protobuf &gt;= 3.19.5 ([#79](https://github.com/googleapis/python-audit-log/issues/79)) ([94e7044](https://github.com/googleapis/python-audit-log/commit/94e7044c66050e6a419bf694e25e677827aa6c13))

## [0.2.4](https://github.com/googleapis/python-audit-log/compare/v0.2.3...v0.2.4) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#67](https://github.com/googleapis/python-audit-log/issues/67)) ([e337e78](https://github.com/googleapis/python-audit-log/commit/e337e781951dea0fbbb6ef9c4ff9896fa3fce86a))

## [0.2.3](https://github.com/googleapis/python-audit-log/compare/v0.2.2...v0.2.3) (2022-07-16)


### Bug Fixes

* require python 3.7+ ([#63](https://github.com/googleapis/python-audit-log/issues/63)) ([c7d33f4](https://github.com/googleapis/python-audit-log/commit/c7d33f463e6dda2d24cc884f4049cfd437876812))

### [0.2.2](https://github.com/googleapis/python-audit-log/compare/v0.2.1...v0.2.2) (2022-05-26)


### Bug Fixes

* regenerate pb2 files using grpcio-tools ([#57](https://github.com/googleapis/python-audit-log/issues/57)) ([7058ada](https://github.com/googleapis/python-audit-log/commit/7058ada0cc89cac453b6d55d6a1529d7274784fd))

### [0.2.1](https://github.com/googleapis/python-audit-log/compare/v0.2.0...v0.2.1) (2022-05-26)


### Bug Fixes

* **deps:** require protobuf>= 3.6.0, <4.0.0dev ([#55](https://github.com/googleapis/python-audit-log/issues/55)) ([e84a2a9](https://github.com/googleapis/python-audit-log/commit/e84a2a9bb8efa13e53a9941580307dbaabec72b1))

## [0.2.0](https://www.github.com/googleapis/python-audit-log/compare/v0.1.1...v0.2.0) (2021-10-13)


### Features

* add trove classifier for python 3.10 ([#38](https://www.github.com/googleapis/python-audit-log/issues/38)) ([355cbf1](https://www.github.com/googleapis/python-audit-log/commit/355cbf14dbe67879395c068ff0192b9d21410c51))

### [0.1.1](https://www.github.com/googleapis/python-audit-log/compare/v0.1.0...v0.1.1) (2021-08-31)


### Bug Fixes

* remove deprecated call to Descriptor() ([#29](https://www.github.com/googleapis/python-audit-log/issues/29)) ([26f15be](https://www.github.com/googleapis/python-audit-log/commit/26f15be30432e61a6555c2cfe6643a83bf60def0))

## 0.1.0 (2020-07-30)


### Features

* publish audit_log.proto ([4ca63a0](https://www.github.com/googleapis/python-audit-log/commit/4ca63a097e68bbae3e0094f071b9ef122c0db696))
