# Changelog

## [0.4.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.9...google-cloud-beyondcorp-clientgateways-v0.4.10) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([6e83a37](https://github.com/googleapis/google-cloud-python/commit/6e83a37612d9eb951cb0ef1e372ef4241f8afa59))

## [0.4.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.8...google-cloud-beyondcorp-clientgateways-v0.4.9) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12864](https://github.com/googleapis/google-cloud-python/issues/12864)) ([728b307](https://github.com/googleapis/google-cloud-python/commit/728b307ed0cc497685507a219e913f002f097132))

## [0.4.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.7...google-cloud-beyondcorp-clientgateways-v0.4.8) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12382](https://github.com/googleapis/google-cloud-python/issues/12382)) ([d5db265](https://github.com/googleapis/google-cloud-python/commit/d5db2656c011be2264bd778244caf8e23d288c75))

## [0.4.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.6...google-cloud-beyondcorp-clientgateways-v0.4.7) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12281](https://github.com/googleapis/google-cloud-python/issues/12281)) ([62cf934](https://github.com/googleapis/google-cloud-python/commit/62cf934b140173d7b39e6c9ffa66e218b98260d4))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12304](https://github.com/googleapis/google-cloud-python/issues/12304)) ([c52e0cd](https://github.com/googleapis/google-cloud-python/commit/c52e0cdbddf44c96f642d8d596c5413c4006ba82))

## [0.4.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.5...google-cloud-beyondcorp-clientgateways-v0.4.6) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([8465244](https://github.com/googleapis/google-cloud-python/commit/8465244deff230202eebab526092c780c6b60f4e))

## [0.4.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.4...google-cloud-beyondcorp-clientgateways-v0.4.5) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## [0.4.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.3...google-cloud-beyondcorp-clientgateways-v0.4.4) (2023-12-07)


### Features

* Add support for python 3.12 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Introduce compatibility with native namespace packages ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))
* Use `retry_async` instead of `retry` in async client ([0d1a592](https://github.com/googleapis/google-cloud-python/commit/0d1a59258112158cea5e55b554b0fe6b6b71fc75))

## [0.4.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.2...google-cloud-beyondcorp-clientgateways-v0.4.3) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.4.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-beyondcorp-clientgateways-v0.4.1...google-cloud-beyondcorp-clientgateways-v0.4.2) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.4.1](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.4.0...v0.4.1) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#52](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/52)) ([dc78c21](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/dc78c21ea076651a573139560174479bd0bf6f67))

## [0.4.0](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.3.1...v0.4.0) (2023-02-09)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#46](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/46)) ([7aa95be](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/7aa95bec1669017ce7a4936e10f724fe5c0c0431))

## [0.3.1](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.3.0...v0.3.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([b0c6c49](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/b0c6c4997e8b2a74fc8094d23604a2a638066b70))


### Documentation

* Add documentation for enums ([b0c6c49](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/b0c6c4997e8b2a74fc8094d23604a2a638066b70))

## [0.3.0](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.2.0...v0.3.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#37](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/37)) ([8521176](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/8521176cafcd1af761d687116fdc26f1725aef38))

## [0.2.0](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.1.3...v0.2.0) (2022-12-15)


### Features

* Add support for `google.cloud.beyondcorp_clientgateways.__version__` ([41cfb6a](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/41cfb6ab9ac28b33e69cc2e1bede18796a42e18a))
* Add typing to proto.Message based class attributes ([41cfb6a](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/41cfb6ab9ac28b33e69cc2e1bede18796a42e18a))


### Bug Fixes

* Add dict typing for client_options ([41cfb6a](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/41cfb6ab9ac28b33e69cc2e1bede18796a42e18a))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([d290938](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/d2909387abcfe245b2e54939662934b4cb3dcc09))
* Drop usage of pkg_resources ([d290938](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/d2909387abcfe245b2e54939662934b4cb3dcc09))
* Fix timeout default values ([d290938](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/d2909387abcfe245b2e54939662934b4cb3dcc09))


### Documentation

* Fix minor docstring formatting ([41cfb6a](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/41cfb6ab9ac28b33e69cc2e1bede18796a42e18a))
* **samples:** Snippetgen handling of repeated enum field ([41cfb6a](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/41cfb6ab9ac28b33e69cc2e1bede18796a42e18a))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([d290938](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/d2909387abcfe245b2e54939662934b4cb3dcc09))

## [0.1.3](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.1.2...v0.1.3) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#27](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/27)) ([bc1256d](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/bc1256d0991f13ac78197b8575f276f4c58cd176))

## [0.1.2](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.1.1...v0.1.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#25](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/25)) ([a218def](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/a218def33193241404ddc08dc7389395efc43123))

## [0.1.1](https://github.com/googleapis/python-beyondcorp-clientgateways/compare/v0.1.0...v0.1.1) (2022-08-15)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#11](https://github.com/googleapis/python-beyondcorp-clientgateways/issues/11)) ([ea422f3](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/ea422f3053969c627d99fee5a822b86777fece98))
* **deps:** require proto-plus >= 1.22.0 ([ea422f3](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/ea422f3053969c627d99fee5a822b86777fece98))

## 0.1.0 (2022-07-20)


### Features

* generate v1 ([4d3ecda](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/4d3ecda6e5f00cb0b429fc3d29f7174676db713f))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([19d5ff1](https://github.com/googleapis/python-beyondcorp-clientgateways/commit/19d5ff173167dede07ec500db88f0a7eab81c977))
