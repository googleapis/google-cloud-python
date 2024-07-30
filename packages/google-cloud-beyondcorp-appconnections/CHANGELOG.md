# Changelog

## [0.4.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.10...google-cloud-beyondcorp-appconnections-v0.4.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.4.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.9...google-cloud-beyondcorp-appconnections-v0.4.10) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.4.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.8...google-cloud-beyondcorp-appconnections-v0.4.9) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12382](https://github.com/googleapis/google-cloud-python/issues/12382)) ([d5db265](https://github.com/googleapis/google-cloud-python/commit/d5db2656c011be2264bd778244caf8e23d288c75))

## [0.4.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.7...google-cloud-beyondcorp-appconnections-v0.4.8) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12304](https://github.com/googleapis/google-cloud-python/issues/12304)) ([c52e0cd](https://github.com/googleapis/google-cloud-python/commit/c52e0cdbddf44c96f642d8d596c5413c4006ba82))

## [0.4.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.6...google-cloud-beyondcorp-appconnections-v0.4.7) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))

## [0.4.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.5...google-cloud-beyondcorp-appconnections-v0.4.6) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([a0392ee](https://github.com/googleapis/google-cloud-python/commit/a0392eeb59fcc6ea7c55283110b92aa24a4d40a0))

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.4...google-cloud-beyondcorp-appconnections-v0.4.5) (2023-12-07)


### Features

* Add support for python 3.12 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Introduce compatibility with native namespace packages ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Use `retry_async` instead of `retry` in async client ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.3...google-cloud-beyondcorp-appconnections-v0.4.4) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-appconnections-v0.4.2...google-cloud-beyondcorp-appconnections-v0.4.3) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.4.2](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.4.1...v0.4.2) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#62](https://github.com/googleapis/python-beyondcorp-appconnections/issues/62)) ([a170ca2](https://github.com/googleapis/python-beyondcorp-appconnections/commit/a170ca2f7bf1587bab07a5f03726743d64c2ebe3))

## [0.4.1](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.4.0...v0.4.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([0058c52](https://github.com/googleapis/python-beyondcorp-appconnections/commit/0058c52a741e7cbe498ba95c332af827c6d9d146))


### Documentation

* Add documentation for enums ([0058c52](https://github.com/googleapis/python-beyondcorp-appconnections/commit/0058c52a741e7cbe498ba95c332af827c6d9d146))

## [0.4.0](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.3.0...v0.4.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#50](https://github.com/googleapis/python-beyondcorp-appconnections/issues/50)) ([1663612](https://github.com/googleapis/python-beyondcorp-appconnections/commit/16636128dfd54cf86b4b95efbf56cd21269a47f7))

## [0.3.0](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.2.2...v0.3.0) (2022-12-13)


### Features

* Add support for `google.cloud.beyondcorp_appconnections.__version__` ([4f606b1](https://github.com/googleapis/python-beyondcorp-appconnections/commit/4f606b170d837c28d4b8ac5cad25b24789fe60f3))
* Add typing to proto.Message based class attributes ([4f606b1](https://github.com/googleapis/python-beyondcorp-appconnections/commit/4f606b170d837c28d4b8ac5cad25b24789fe60f3))


### Bug Fixes

* Add dict typing for client_options ([4f606b1](https://github.com/googleapis/python-beyondcorp-appconnections/commit/4f606b170d837c28d4b8ac5cad25b24789fe60f3))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([f7717f8](https://github.com/googleapis/python-beyondcorp-appconnections/commit/f7717f822527139dec5b9efbf0d2dc90f8513e50))
* Drop usage of pkg_resources ([f7717f8](https://github.com/googleapis/python-beyondcorp-appconnections/commit/f7717f822527139dec5b9efbf0d2dc90f8513e50))
* Fix timeout default values ([f7717f8](https://github.com/googleapis/python-beyondcorp-appconnections/commit/f7717f822527139dec5b9efbf0d2dc90f8513e50))


### Documentation

* Fix minor docstring formatting ([4f606b1](https://github.com/googleapis/python-beyondcorp-appconnections/commit/4f606b170d837c28d4b8ac5cad25b24789fe60f3))
* **samples:** Snippetgen handling of repeated enum field ([4f606b1](https://github.com/googleapis/python-beyondcorp-appconnections/commit/4f606b170d837c28d4b8ac5cad25b24789fe60f3))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([f7717f8](https://github.com/googleapis/python-beyondcorp-appconnections/commit/f7717f822527139dec5b9efbf0d2dc90f8513e50))

## [0.2.2](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.2.1...v0.2.2) (2022-10-10)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#37](https://github.com/googleapis/python-beyondcorp-appconnections/issues/37)) ([cd3da8d](https://github.com/googleapis/python-beyondcorp-appconnections/commit/cd3da8d989143042e1132356946a83d5a042391a))
* **deps:** require google-api-core&gt;=1.33.2 ([cd3da8d](https://github.com/googleapis/python-beyondcorp-appconnections/commit/cd3da8d989143042e1132356946a83d5a042391a))

## [0.2.1](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.2.0...v0.2.1) (2022-10-03)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#34](https://github.com/googleapis/python-beyondcorp-appconnections/issues/34)) ([90c7162](https://github.com/googleapis/python-beyondcorp-appconnections/commit/90c7162776a0f8ab4fc5bc9a0d88f4f6e442f3a6))

## [0.2.0](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.1.1...v0.2.0) (2022-09-16)


### Features

* Add support for REST transport ([#27](https://github.com/googleapis/python-beyondcorp-appconnections/issues/27)) ([56764f7](https://github.com/googleapis/python-beyondcorp-appconnections/commit/56764f76d72480397a0d7efe3c65fcc2e5847d31))


### Bug Fixes

* **deps:** require google-api-core>=1.33.1,>=2.8.0 ([56764f7](https://github.com/googleapis/python-beyondcorp-appconnections/commit/56764f76d72480397a0d7efe3c65fcc2e5847d31))
* **deps:** require protobuf >= 3.20.1 ([56764f7](https://github.com/googleapis/python-beyondcorp-appconnections/commit/56764f76d72480397a0d7efe3c65fcc2e5847d31))

## [0.1.1](https://github.com/googleapis/python-beyondcorp-appconnections/compare/v0.1.0...v0.1.1) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#12](https://github.com/googleapis/python-beyondcorp-appconnections/issues/12)) ([b874c80](https://github.com/googleapis/python-beyondcorp-appconnections/commit/b874c80796c1a445887ee2671b130c4daca830a3))
* **deps:** require proto-plus >= 1.22.0 ([b874c80](https://github.com/googleapis/python-beyondcorp-appconnections/commit/b874c80796c1a445887ee2671b130c4daca830a3))

## 0.1.0 (2022-07-18)


### Features

* generate v1 ([2f76be4](https://github.com/googleapis/python-beyondcorp-appconnections/commit/2f76be4dfedacb3deb788d13007369f6ea174099))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#2](https://github.com/googleapis/python-beyondcorp-appconnections/issues/2)) ([38ae96b](https://github.com/googleapis/python-beyondcorp-appconnections/commit/38ae96bbb7d1498bbd951a682951a35c0a224c6c))
