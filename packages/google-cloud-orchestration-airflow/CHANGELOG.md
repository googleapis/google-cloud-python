# Changelog

## [1.9.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-orchestration-airflow-v1.9.0...google-cloud-orchestration-airflow-v1.9.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11448](https://github.com/googleapis/google-cloud-python/issues/11448)) ([4d2c35a](https://github.com/googleapis/google-cloud-python/commit/4d2c35a1cd0b68b6d481d5611ff820451273e859))

## [1.9.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-orchestration-airflow-v1.8.0...google-cloud-orchestration-airflow-v1.9.0) (2023-06-14)


### Features

* added RPCs StopAirflowCommand, ExecuteAirflowCommand, PollAirflowCommand, DatabaseFailover, FetchDatabaseProperties ([#11400](https://github.com/googleapis/google-cloud-python/issues/11400)) ([b2dc3e5](https://github.com/googleapis/google-cloud-python/commit/b2dc3e585c8f942aac1c4db204792378a5ea72e8))

## [1.8.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.7.1...v1.8.0) (2023-05-25)


### Features

* Add airflow_byoid_uri field to Cloud Composer API ([#172](https://github.com/googleapis/python-orchestration-airflow/issues/172)) ([a402b20](https://github.com/googleapis/python-orchestration-airflow/commit/a402b20bed535b193b030ff077b76515aa27a81e))

## [1.7.1](https://github.com/googleapis/python-orchestration-airflow/compare/v1.7.0...v1.7.1) (2023-03-23)


### Documentation

* Fix formatting of request arg in docstring ([#170](https://github.com/googleapis/python-orchestration-airflow/issues/170)) ([91e315c](https://github.com/googleapis/python-orchestration-airflow/commit/91e315c66c77a6d9c37196a4362c9ddd94c85cc4))

## [1.7.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.6.1...v1.7.0) (2023-02-17)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#163](https://github.com/googleapis/python-orchestration-airflow/issues/163)) ([43b46e2](https://github.com/googleapis/python-orchestration-airflow/commit/43b46e2beb55748987a13dcbe8b3b9e339166b25))


### Bug Fixes

* Add service_yaml_parameters to py_gapic_library BUILD.bazel targets ([#165](https://github.com/googleapis/python-orchestration-airflow/issues/165)) ([e244bd5](https://github.com/googleapis/python-orchestration-airflow/commit/e244bd5b0221d348f39fc5f5c7e95c1e8b9e15fa))

## [1.6.1](https://github.com/googleapis/python-orchestration-airflow/compare/v1.6.0...v1.6.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([693d570](https://github.com/googleapis/python-orchestration-airflow/commit/693d570fd0aa7cb1287329fd233e266219302ec3))


### Documentation

* Add documentation for enums ([693d570](https://github.com/googleapis/python-orchestration-airflow/commit/693d570fd0aa7cb1287329fd233e266219302ec3))

## [1.6.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.5.0...v1.6.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#154](https://github.com/googleapis/python-orchestration-airflow/issues/154)) ([86db9d6](https://github.com/googleapis/python-orchestration-airflow/commit/86db9d6e0ae65d63a3dcad75a0dea61a69cf295f))

## [1.5.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.4.4...v1.5.0) (2022-12-13)


### Features

* add support for `google.cloud.orchestration.airflow.service.__version__` ([8edf594](https://github.com/googleapis/python-orchestration-airflow/commit/8edf5948c6a59e5172c042faf5c40d98066b52a0))
* Add typing to proto.Message based class attributes ([8edf594](https://github.com/googleapis/python-orchestration-airflow/commit/8edf5948c6a59e5172c042faf5c40d98066b52a0))
* added field enable_ip_masq_agent to NodeConfig ([6c8a0bf](https://github.com/googleapis/python-orchestration-airflow/commit/6c8a0bf722793353ca9311410f245451bbdf437c))
* added field scheduler_count to SoftwareConfig ([6c8a0bf](https://github.com/googleapis/python-orchestration-airflow/commit/6c8a0bf722793353ca9311410f245451bbdf437c))
* added fields cloud_composer_network_ipv4_cidr_block, cloud_composer_network_ipv4_reserved_range, enable_privately_used_public_ips, cloud_composer_connection_subnetwork, networking_config to PrivateEnvironmentConfig ([6c8a0bf](https://github.com/googleapis/python-orchestration-airflow/commit/6c8a0bf722793353ca9311410f245451bbdf437c))
* added fields maintenance_window, workloads_config, environment_size, master_authorized_networks_config, recovery_config to EnvironmentConfig ([6c8a0bf](https://github.com/googleapis/python-orchestration-airflow/commit/6c8a0bf722793353ca9311410f245451bbdf437c))
* Added LoadSnapshot, SaveSnapshot RPCs ([#150](https://github.com/googleapis/python-orchestration-airflow/issues/150)) ([6c8a0bf](https://github.com/googleapis/python-orchestration-airflow/commit/6c8a0bf722793353ca9311410f245451bbdf437c))


### Bug Fixes

* Add dict typing for client_options ([8edf594](https://github.com/googleapis/python-orchestration-airflow/commit/8edf5948c6a59e5172c042faf5c40d98066b52a0))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([9b1d61e](https://github.com/googleapis/python-orchestration-airflow/commit/9b1d61e4cb24023ca831e83799ccc61fc398d335))
* Drop usage of pkg_resources ([9b1d61e](https://github.com/googleapis/python-orchestration-airflow/commit/9b1d61e4cb24023ca831e83799ccc61fc398d335))
* Fix timeout default values ([9b1d61e](https://github.com/googleapis/python-orchestration-airflow/commit/9b1d61e4cb24023ca831e83799ccc61fc398d335))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([8edf594](https://github.com/googleapis/python-orchestration-airflow/commit/8edf5948c6a59e5172c042faf5c40d98066b52a0))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([9b1d61e](https://github.com/googleapis/python-orchestration-airflow/commit/9b1d61e4cb24023ca831e83799ccc61fc398d335))

## [1.4.4](https://github.com/googleapis/python-orchestration-airflow/compare/v1.4.3...v1.4.4) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#143](https://github.com/googleapis/python-orchestration-airflow/issues/143)) ([d6bc170](https://github.com/googleapis/python-orchestration-airflow/commit/d6bc1706098586ef9b4591a62caeb2bcb8177fca))

## [1.4.3](https://github.com/googleapis/python-orchestration-airflow/compare/v1.4.2...v1.4.3) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#141](https://github.com/googleapis/python-orchestration-airflow/issues/141)) ([ab36ee0](https://github.com/googleapis/python-orchestration-airflow/commit/ab36ee0f28e3528439a768b4ccfc51c7ef10eaa8))

## [1.4.2](https://github.com/googleapis/python-orchestration-airflow/compare/v1.4.1...v1.4.2) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#128](https://github.com/googleapis/python-orchestration-airflow/issues/128)) ([73fb0c2](https://github.com/googleapis/python-orchestration-airflow/commit/73fb0c22ff1da1b400141418e1034fad776fea0a))
* **deps:** require proto-plus >= 1.22.0 ([73fb0c2](https://github.com/googleapis/python-orchestration-airflow/commit/73fb0c22ff1da1b400141418e1034fad776fea0a))

## [1.4.1](https://github.com/googleapis/python-orchestration-airflow/compare/v1.4.0...v1.4.1) (2022-07-13)


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#120](https://github.com/googleapis/python-orchestration-airflow/issues/120)) ([3fcf6fc](https://github.com/googleapis/python-orchestration-airflow/commit/3fcf6fc44f0d58f7d9da00a434748be0723292b6))

## [1.4.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.3.2...v1.4.0) (2022-07-07)


### Features

* add audience parameter ([1e74b80](https://github.com/googleapis/python-orchestration-airflow/commit/1e74b80e426d74c36bd0792082d29e4e618d08a4))


### Bug Fixes

* **deps:** require google-api-core >= 2.8.0 ([#116](https://github.com/googleapis/python-orchestration-airflow/issues/116)) ([1e74b80](https://github.com/googleapis/python-orchestration-airflow/commit/1e74b80e426d74c36bd0792082d29e4e618d08a4))
* require python 3.7+ ([#118](https://github.com/googleapis/python-orchestration-airflow/issues/118)) ([891963c](https://github.com/googleapis/python-orchestration-airflow/commit/891963c483d34f285695e2b680ec798a0b70def4))

## [1.3.2](https://github.com/googleapis/python-orchestration-airflow/compare/v1.3.1...v1.3.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#108](https://github.com/googleapis/python-orchestration-airflow/issues/108)) ([9f4671f](https://github.com/googleapis/python-orchestration-airflow/commit/9f4671fd7282114fb3a91b29c63938a9c3a977a2))


### Documentation

* fix changelog header to consistent size ([#109](https://github.com/googleapis/python-orchestration-airflow/issues/109)) ([5d8f6a0](https://github.com/googleapis/python-orchestration-airflow/commit/5d8f6a0f400f77e31e23fb0f8398f70de6b30a74))

## [1.3.1](https://github.com/googleapis/python-orchestration-airflow/compare/v1.3.0...v1.3.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#70](https://github.com/googleapis/python-orchestration-airflow/issues/70)) ([5847489](https://github.com/googleapis/python-orchestration-airflow/commit/58474891762075088806b1da8894da5ed4dd6741))

## [1.3.0](https://github.com/googleapis/python-orchestration-airflow/compare/v1.2.1...v1.3.0) (2022-02-26)


### Features

* add api key support ([#60](https://github.com/googleapis/python-orchestration-airflow/issues/60)) ([8e05a90](https://github.com/googleapis/python-orchestration-airflow/commit/8e05a905ea8a5c760eeb65d15cea73da41eac4ab))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([#63](https://github.com/googleapis/python-orchestration-airflow/issues/63)) ([d2bd1b9](https://github.com/googleapis/python-orchestration-airflow/commit/d2bd1b9c76fe16f180f55b4c046c719ee1fbec46))

## [1.2.1](https://www.github.com/googleapis/python-orchestration-airflow/compare/v1.2.0...v1.2.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([be8de44](https://www.github.com/googleapis/python-orchestration-airflow/commit/be8de448aa7b0bdfb40edf5c41b0a2d5a411b9cc))
* **deps:** require google-api-core >= 1.28.0 ([be8de44](https://www.github.com/googleapis/python-orchestration-airflow/commit/be8de448aa7b0bdfb40edf5c41b0a2d5a411b9cc))


### Documentation

* list oneofs in docstring ([be8de44](https://www.github.com/googleapis/python-orchestration-airflow/commit/be8de448aa7b0bdfb40edf5c41b0a2d5a411b9cc))

## [1.2.0](https://www.github.com/googleapis/python-orchestration-airflow/compare/v1.1.0...v1.2.0) (2021-10-18)


### Features

* add support for python 3.10 ([#36](https://www.github.com/googleapis/python-orchestration-airflow/issues/36)) ([f8a94e1](https://www.github.com/googleapis/python-orchestration-airflow/commit/f8a94e19edea767411f863587bf9e4ebfc8d001c))

## [1.1.0](https://www.github.com/googleapis/python-orchestration-airflow/compare/v1.0.0...v1.1.0) (2021-10-08)


### Features

* add context manager support in client ([#32](https://www.github.com/googleapis/python-orchestration-airflow/issues/32)) ([e88a664](https://www.github.com/googleapis/python-orchestration-airflow/commit/e88a6643be39c3cdbf4be3718e101ba0cb36f6f9))

## [1.0.0](https://www.github.com/googleapis/python-orchestration-airflow/compare/v0.1.3...v1.0.0) (2021-10-05)


### Features

* bump release level to production/stable ([#12](https://www.github.com/googleapis/python-orchestration-airflow/issues/12)) ([9034947](https://www.github.com/googleapis/python-orchestration-airflow/commit/90349471b64fa702618c7da394d212cc31126a33))

## [0.1.3](https://www.github.com/googleapis/python-orchestration-airflow/compare/v0.1.2...v0.1.3) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([b9b7a2f](https://www.github.com/googleapis/python-orchestration-airflow/commit/b9b7a2fe76906c0056c1a4bba1ff576dc7e339a3))

## [0.1.2](https://www.github.com/googleapis/python-orchestration-airflow/compare/v0.1.1...v0.1.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([7d5d4de](https://www.github.com/googleapis/python-orchestration-airflow/commit/7d5d4de6ec0ae72fad49db1bb47334b2da0494b4))

## [0.1.1](https://www.github.com/googleapis/python-orchestration-airflow/compare/v0.1.0...v0.1.1) (2021-07-28)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#9](https://www.github.com/googleapis/python-orchestration-airflow/issues/9)) ([b4ef804](https://www.github.com/googleapis/python-orchestration-airflow/commit/b4ef804d16f4b312e0485e9107f32ef3ee0a7a97))

## 0.1.0 (2021-07-28)


### Features

* generate v1 and v1beta1 ([87d29da](https://www.github.com/googleapis/python-orchestration-airflow/commit/87d29da7d280a41c109ff30231a2e53d514d4eeb))
