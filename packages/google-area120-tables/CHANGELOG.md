# Changelog

## [0.11.16](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.15...google-area120-tables-v0.11.16) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))
* remove setup.cfg configuration for creating universal wheels ([#13659](https://github.com/googleapis/google-cloud-python/issues/13659)) ([59bfd42](https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce))

## [0.11.15](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.14...google-area120-tables-v0.11.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.11.14](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.13...google-area120-tables-v0.11.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))

## [0.11.13](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.12...google-area120-tables-v0.11.13) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.11.12](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.11...google-area120-tables-v0.11.12) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.11.11](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.10...google-area120-tables-v0.11.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.11.10](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.9...google-area120-tables-v0.11.10) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))

## [0.11.9](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.8...google-area120-tables-v0.11.9) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12381](https://github.com/googleapis/google-cloud-python/issues/12381)) ([48ae8ab](https://github.com/googleapis/google-cloud-python/commit/48ae8aba7ec71a382e001b3a659022f942c3b436))

## [0.11.8](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.7...google-area120-tables-v0.11.8) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12280](https://github.com/googleapis/google-cloud-python/issues/12280)) ([2d75d0e](https://github.com/googleapis/google-cloud-python/commit/2d75d0e67ca4cccddc688bd37c14ac80564a2e65))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12303](https://github.com/googleapis/google-cloud-python/issues/12303)) ([fbb80c3](https://github.com/googleapis/google-cloud-python/commit/fbb80c32f7db91e25bd1cc30966f630728ff6d6a))

## [0.11.7](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.6...google-area120-tables-v0.11.7) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))

## [0.11.6](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.5...google-area120-tables-v0.11.6) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([a0392ee](https://github.com/googleapis/google-cloud-python/commit/a0392eeb59fcc6ea7c55283110b92aa24a4d40a0))

## [0.11.5](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.4...google-area120-tables-v0.11.5) (2023-12-07)


### Features

* Add support for python 3.12 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Introduce compatibility with native namespace packages ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))
* Use `retry_async` instead of `retry` in async client ([ea6cfc2](https://github.com/googleapis/google-cloud-python/commit/ea6cfc2f86e77757b8cb05f7fd0d9c0b7ccaf7cf))

## [0.11.4](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.3...google-area120-tables-v0.11.4) (2023-09-30)


### Documentation

* Minor formatting ([#11630](https://github.com/googleapis/google-cloud-python/issues/11630)) ([b176996](https://github.com/googleapis/google-cloud-python/commit/b176996309cb5b3e9c257caaebde8884bd556824))

## [0.11.3](https://github.com/googleapis/google-cloud-python/compare/google-area120-tables-v0.11.2...google-area120-tables-v0.11.3) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11444](https://github.com/googleapis/google-cloud-python/issues/11444)) ([9aa301a](https://github.com/googleapis/google-cloud-python/commit/9aa301ae6ca3080cae286a19de9cdc1b796ab37d))

## [0.11.2](https://github.com/googleapis/python-area120-tables/compare/v0.11.1...v0.11.2) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#230](https://github.com/googleapis/python-area120-tables/issues/230)) ([2ad5d77](https://github.com/googleapis/python-area120-tables/commit/2ad5d77309bc8e7eb63af60b796d85e1306c2278))

## [0.11.1](https://github.com/googleapis/python-area120-tables/compare/v0.11.0...v0.11.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([a9d18ca](https://github.com/googleapis/python-area120-tables/commit/a9d18cac29a6607520ba25e6d8ad2ad862f4710c))


### Documentation

* Add documentation for enums ([a9d18ca](https://github.com/googleapis/python-area120-tables/commit/a9d18cac29a6607520ba25e6d8ad2ad862f4710c))

## [0.11.0](https://github.com/googleapis/python-area120-tables/compare/v0.10.1...v0.11.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#219](https://github.com/googleapis/python-area120-tables/issues/219)) ([332bff3](https://github.com/googleapis/python-area120-tables/commit/332bff3f50052a41fcc44d7c6ee56652540a60ba))

## [0.10.1](https://github.com/googleapis/python-area120-tables/compare/v0.10.0...v0.10.1) (2022-12-14)


### Bug Fixes

* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([4392d33](https://github.com/googleapis/python-area120-tables/commit/4392d33bf965c7a8db803d0fac9af4df02391a97))
* Drop usage of pkg_resources ([4392d33](https://github.com/googleapis/python-area120-tables/commit/4392d33bf965c7a8db803d0fac9af4df02391a97))
* Fix timeout default values ([4392d33](https://github.com/googleapis/python-area120-tables/commit/4392d33bf965c7a8db803d0fac9af4df02391a97))


### Documentation

* **samples:** Snippetgen should call await on the operation coroutine before calling result ([4392d33](https://github.com/googleapis/python-area120-tables/commit/4392d33bf965c7a8db803d0fac9af4df02391a97))

## [0.10.0](https://github.com/googleapis/python-area120-tables/compare/v0.9.0...v0.10.0) (2022-11-16)


### Features

* Add typing to proto.Message based class attributes ([dddcfad](https://github.com/googleapis/python-area120-tables/commit/dddcfade3932b8aa9f303a299200175e4f8547b1))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([dddcfad](https://github.com/googleapis/python-area120-tables/commit/dddcfade3932b8aa9f303a299200175e4f8547b1))

## [0.9.0](https://github.com/googleapis/python-area120-tables/compare/v0.8.2...v0.9.0) (2022-11-08)


### Features

* add support for `google.area120.tables.__version__` ([fc87e8b](https://github.com/googleapis/python-area120-tables/commit/fc87e8bb6bd449ad5fe498b361c53f6e0cf51dc4))


### Bug Fixes

* Add dict typing for client_options ([fc87e8b](https://github.com/googleapis/python-area120-tables/commit/fc87e8bb6bd449ad5fe498b361c53f6e0cf51dc4))

## [0.8.2](https://github.com/googleapis/python-area120-tables/compare/v0.8.1...v0.8.2) (2022-10-10)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#201](https://github.com/googleapis/python-area120-tables/issues/201)) ([9bf9172](https://github.com/googleapis/python-area120-tables/commit/9bf91729e41f11b3e2979690f768e708a8ee936a))
* **deps:** require google-api-core&gt;=1.33.2 ([9bf9172](https://github.com/googleapis/python-area120-tables/commit/9bf91729e41f11b3e2979690f768e708a8ee936a))

## [0.8.1](https://github.com/googleapis/python-area120-tables/compare/v0.8.0...v0.8.1) (2022-10-03)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#198](https://github.com/googleapis/python-area120-tables/issues/198)) ([5813086](https://github.com/googleapis/python-area120-tables/commit/58130869fcf96d129dd0a72cada69df9ad868e19))

## [0.8.0](https://github.com/googleapis/python-area120-tables/compare/v0.7.1...v0.8.0) (2022-09-16)


### Features

* Add support for REST transport ([#194](https://github.com/googleapis/python-area120-tables/issues/194)) ([14bab6c](https://github.com/googleapis/python-area120-tables/commit/14bab6c92a74aa27b2dac80543171082a7c4c189))


### Bug Fixes

* **deps:** require google-api-core>=1.33.1,>=2.8.0 ([14bab6c](https://github.com/googleapis/python-area120-tables/commit/14bab6c92a74aa27b2dac80543171082a7c4c189))
* **deps:** require protobuf >= 3.20.1 ([14bab6c](https://github.com/googleapis/python-area120-tables/commit/14bab6c92a74aa27b2dac80543171082a7c4c189))

## [0.7.1](https://github.com/googleapis/python-area120-tables/compare/v0.7.0...v0.7.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#181](https://github.com/googleapis/python-area120-tables/issues/181)) ([6c45184](https://github.com/googleapis/python-area120-tables/commit/6c451840d2e6169c108ad6e455289e9d81c6c317))
* **deps:** require proto-plus >= 1.22.0 ([6c45184](https://github.com/googleapis/python-area120-tables/commit/6c451840d2e6169c108ad6e455289e9d81c6c317))

## [0.7.0](https://github.com/googleapis/python-area120-tables/compare/v0.6.2...v0.7.0) (2022-07-18)


### Features

* add audience parameter ([64ffe58](https://github.com/googleapis/python-area120-tables/commit/64ffe58e32298fd0a9305bfe0f142374062e39e2))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#173](https://github.com/googleapis/python-area120-tables/issues/173)) ([64ffe58](https://github.com/googleapis/python-area120-tables/commit/64ffe58e32298fd0a9305bfe0f142374062e39e2))
* require python 3.7+ ([#175](https://github.com/googleapis/python-area120-tables/issues/175)) ([0cab642](https://github.com/googleapis/python-area120-tables/commit/0cab642e514072540128d3df941281ccef2e776c))

## [0.6.2](https://github.com/googleapis/python-area120-tables/compare/v0.6.1...v0.6.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#165](https://github.com/googleapis/python-area120-tables/issues/165)) ([4475608](https://github.com/googleapis/python-area120-tables/commit/44756082f10cf31ed691d5345216de396efae88c))


### Documentation

* fix changelog header to consistent size ([#166](https://github.com/googleapis/python-area120-tables/issues/166)) ([bb33737](https://github.com/googleapis/python-area120-tables/commit/bb3373758f17d092bd65510107cd162d24e696fe))

## [0.6.1](https://github.com/googleapis/python-area120-tables/compare/v0.6.0...v0.6.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#130](https://github.com/googleapis/python-area120-tables/issues/130)) ([0e565da](https://github.com/googleapis/python-area120-tables/commit/0e565da03fe9a5f32c9e08435e0674ca4ef0e0ae))
* **deps:** require proto-plus>=1.15.0 ([0e565da](https://github.com/googleapis/python-area120-tables/commit/0e565da03fe9a5f32c9e08435e0674ca4ef0e0ae))

## [0.6.0](https://github.com/googleapis/python-area120-tables/compare/v0.5.1...v0.6.0) (2022-02-26)


### Features

* add api key support ([#116](https://github.com/googleapis/python-area120-tables/issues/116)) ([48c0ead](https://github.com/googleapis/python-area120-tables/commit/48c0ead49612fc58ea39ed55745abd73a83f3732))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([6474a00](https://github.com/googleapis/python-area120-tables/commit/6474a00180d134ab4c2d1d0a2328531758ae140d))


### Documentation

* add autogenerated code snippets ([ae17805](https://github.com/googleapis/python-area120-tables/commit/ae17805b6ea2307947129caba2185ade52a5e74c))

## [0.5.1](https://www.github.com/googleapis/python-area120-tables/compare/v0.5.0...v0.5.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([76b9cba](https://www.github.com/googleapis/python-area120-tables/commit/76b9cba55f3ba56dd015591820c34f59b68c796d))
* **deps:** require google-api-core >= 1.28.0 ([76b9cba](https://www.github.com/googleapis/python-area120-tables/commit/76b9cba55f3ba56dd015591820c34f59b68c796d))


### Documentation

* list oneofs in docstring ([76b9cba](https://www.github.com/googleapis/python-area120-tables/commit/76b9cba55f3ba56dd015591820c34f59b68c796d))

## [0.5.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.4...v0.5.0) (2021-10-11)


### Features

* add context manager support in client ([#96](https://www.github.com/googleapis/python-area120-tables/issues/96)) ([8990f1b](https://www.github.com/googleapis/python-area120-tables/commit/8990f1b4539f8bf0d3a327c4327a12d486447cbf))
* add trove classifier for python 3.9 and python 3.10 ([#99](https://www.github.com/googleapis/python-area120-tables/issues/99)) ([c9cee0f](https://www.github.com/googleapis/python-area120-tables/commit/c9cee0f8cb1bf6ddb4b7bcedfd88494e9cedcf32))

## [0.4.4](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.3...v0.4.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([18767c6](https://www.github.com/googleapis/python-area120-tables/commit/18767c6fe872942866266c0530a95a8d5160b8e5))

## [0.4.3](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.2...v0.4.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([ee57f81](https://www.github.com/googleapis/python-area120-tables/commit/ee57f81534ac3cc21ced61659ee1796dbe5b4210))

## [0.4.2](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.1...v0.4.2) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#69](https://www.github.com/googleapis/python-area120-tables/issues/69)) ([954f6c7](https://www.github.com/googleapis/python-area120-tables/commit/954f6c7ef550d502cb75edb1f981de8eb67849b1))
* enable self signed jwt for grpc ([#75](https://www.github.com/googleapis/python-area120-tables/issues/75)) ([75f29fc](https://www.github.com/googleapis/python-area120-tables/commit/75f29fc84173a1c9497d261fc74d71cb068a41af))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#70](https://www.github.com/googleapis/python-area120-tables/issues/70)) ([15716f3](https://www.github.com/googleapis/python-area120-tables/commit/15716f32094df082a6536513699e68ab308aaf17))


### Miscellaneous Chores

* release as 0.4.2 ([#74](https://www.github.com/googleapis/python-area120-tables/issues/74)) ([682d5dd](https://www.github.com/googleapis/python-area120-tables/commit/682d5dd57c6f752595401bd2d5d232f875bc163b))

## [0.4.1](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.0...v0.4.1) (2021-06-30)


### Bug Fixes

* disable always_use_jwt_access ([5c043fa](https://www.github.com/googleapis/python-area120-tables/commit/5c043fa62bd8e7cdb27a2392a72a74bb15d2e9f4))
* disable always_use_jwt_access ([#65](https://www.github.com/googleapis/python-area120-tables/issues/65)) ([5c043fa](https://www.github.com/googleapis/python-area120-tables/commit/5c043fa62bd8e7cdb27a2392a72a74bb15d2e9f4))

## [0.4.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.3.1...v0.4.0) (2021-06-23)


### Features

* add always_use_jwt_access ([#61](https://www.github.com/googleapis/python-area120-tables/issues/61)) ([91c6f3a](https://www.github.com/googleapis/python-area120-tables/commit/91c6f3adf14a642aba2c0e18158536e9f3031f59))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-area120-tables/issues/1127)) ([#56](https://www.github.com/googleapis/python-area120-tables/issues/56)) ([4bf2bae](https://www.github.com/googleapis/python-area120-tables/commit/4bf2baea55b617393487c2ae6866f04ef073378d)), closes [#1126](https://www.github.com/googleapis/python-area120-tables/issues/1126)

## [0.3.1](https://www.github.com/googleapis/python-area120-tables/compare/v0.3.0...v0.3.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#52](https://www.github.com/googleapis/python-area120-tables/issues/52)) ([da319aa](https://www.github.com/googleapis/python-area120-tables/commit/da319aa3611e82602a4085a7b4472b2ad074b0a7))

## [0.3.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.2.0...v0.3.0) (2021-05-28)


### Features

* Added ListWorkspaces, GetWorkspace, BatchDeleteRows APIs ([#25](https://www.github.com/googleapis/python-area120-tables/issues/25)) ([99c6918](https://www.github.com/googleapis/python-area120-tables/commit/99c691819824ab6cc1915ba23867a5051b94b8a2))
* support self-signed JWT flow for service accounts ([fe5836e](https://www.github.com/googleapis/python-area120-tables/commit/fe5836e050cc3f548c9a98af73d01466e23e8404))


### Bug Fixes

* add async client to %name_%version/init.py ([fe5836e](https://www.github.com/googleapis/python-area120-tables/commit/fe5836e050cc3f548c9a98af73d01466e23e8404))
* **deps:** add packaging requirement ([#47](https://www.github.com/googleapis/python-area120-tables/issues/47)) ([c7cee0b](https://www.github.com/googleapis/python-area120-tables/commit/c7cee0bd0252560e603f1456bdc577b26d477c87))

## [0.2.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.1.0...v0.2.0) (2021-01-29)


### Features

* add common resource paths, expose client transport ([#4](https://www.github.com/googleapis/python-area120-tables/issues/4)) ([e2367d0](https://www.github.com/googleapis/python-area120-tables/commit/e2367d0be19e5e8e353ad9757a5b2ba730168b4c))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([#13](https://www.github.com/googleapis/python-area120-tables/issues/13)) ([302c071](https://www.github.com/googleapis/python-area120-tables/commit/302c071a8493f24b85938b48b66ff6eb83203eda))

## 0.1.0 (2020-09-14)


### Features

* add v1alpha1 ([fc837f9](https://www.github.com/googleapis/python-area120-tables/commit/fc837f99e01228db2cb844376e2f27be6bff3cd6))
* generate v1alpha1 ([7c9b3c5](https://www.github.com/googleapis/python-area120-tables/commit/7c9b3c552c3e99934c71bc64f6f6421343470875))
