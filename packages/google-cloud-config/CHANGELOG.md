# Changelog

## [0.1.17](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.16...google-cloud-config-v0.1.17) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([1e43e75](https://github.com/googleapis/google-cloud-python/commit/1e43e75e99445373785b11381e0e859fa14bb485))

## [0.1.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.15...google-cloud-config-v0.1.16) (2025-02-18)


### Bug Fixes

* **deps:** Require grpc-google-iam-v1&gt;=0.14.0 ([4571dff](https://github.com/googleapis/google-cloud-python/commit/4571dff9614843c6944c8568bd234c6ac5197218))

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.14...google-cloud-config-v0.1.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))
* Add support for reading selective GAPIC generation methods from service YAML ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.13...google-cloud-config-v0.1.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))
* added annotations ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))


### Bug Fixes

* Changed field behavior for an existing field `service_account` in message `.google.cloud.config.v1.Deployment` ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))
* Changed field behavior for an existing field `service_account` in message `.google.cloud.config.v1.Preview` ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))
* Fix typing issue with gRPC metadata when key ends in -bin ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))


### Documentation

* Service Account is a required field ([4795f26](https://github.com/googleapis/google-cloud-python/commit/4795f26b927cc138f5bdc92245848a8ca262ef86))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.12...google-cloud-config-v0.1.13) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.11...google-cloud-config-v0.1.12) (2024-10-24)


### Features

* Add support for  Python 3.13 ([6252476](https://github.com/googleapis/google-cloud-python/commit/6252476e5938352fb2417d098a1edcc08558fe10))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.10...google-cloud-config-v0.1.11) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([a6f7356](https://github.com/googleapis/google-cloud-python/commit/a6f7356f1549721f9fab83d4dcfa226cec1965d0))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.9...google-cloud-config-v0.1.10) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.8...google-cloud-config-v0.1.9) (2024-04-24)


### Features

* Annotations are now supported to help client tools identify deployments during automation ([765e198](https://github.com/googleapis/google-cloud-python/commit/765e198d31bb3d8c12ef1e67179e86ddffbedab5))
* Infrastructure manager supports 1.2.3, 1.3.10, 1.4.7, 1.5.7 versions of Terraform when creating a preview of a deployment ([765e198](https://github.com/googleapis/google-cloud-python/commit/765e198d31bb3d8c12ef1e67179e86ddffbedab5))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.7...google-cloud-config-v0.1.8) (2024-03-22)


### Features

* Infrastructure Manager can validate and enforce quota limits, preventing infrastructure that exceeds quota limits from being deployed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* Infrastructure Manager supports the deployment of infrastructure from Terraform configurations in a private Git repository ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* Infrastructure manager supports the following versions of Terraform when creating a deployment  Terraform version 1.2.3, 1.3.10, 1.4.7, 1.5.7 ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))


### Documentation

* A comment for field `page_size` in message `.google.cloud.config.v1.ListDeploymentsRequest` is changed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* A comment for field `page_size` in message `.google.cloud.config.v1.ListPreviewsRequest` is changed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* A comment for field `page_size` in message `.google.cloud.config.v1.ListResourcesRequest` is changed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* A comment for field `page_size` in message `.google.cloud.config.v1.ListRevisionsRequest` is changed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))
* A comment for field `service_account` in message `.google.cloud.config.v1.Preview` is changed ([b8abb5d](https://github.com/googleapis/google-cloud-python/commit/b8abb5dc7a51773039a9034cf845bd64d0221314))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.6...google-cloud-config-v0.1.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12383](https://github.com/googleapis/google-cloud-python/issues/12383)) ([305f43f](https://github.com/googleapis/google-cloud-python/commit/305f43f7d6293e3316248f421fdc19c5d8405c21))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.5...google-cloud-config-v0.1.6) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12282](https://github.com/googleapis/google-cloud-python/issues/12282)) ([b985096](https://github.com/googleapis/google-cloud-python/commit/b985096d43add8214172ff993e00293e6c8757cb))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12305](https://github.com/googleapis/google-cloud-python/issues/12305)) ([2aa7f17](https://github.com/googleapis/google-cloud-python/commit/2aa7f17a5fd4f2249260225db91fb0414d06eaa7))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.4...google-cloud-config-v0.1.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.3...google-cloud-config-v0.1.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12239](https://github.com/googleapis/google-cloud-python/issues/12239)) ([8004d15](https://github.com/googleapis/google-cloud-python/commit/8004d15d9e6baa4dc5bc3f09d528e176d54d9ec5))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.2...google-cloud-config-v0.1.3) (2024-01-19)


### Features

* [google-cloud-config] added Terraform Plan ([#12197](https://github.com/googleapis/google-cloud-python/issues/12197)) ([2de325b](https://github.com/googleapis/google-cloud-python/commit/2de325ba6aef85c98c9ebbe03fc6a4ebb2834a12))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.1...google-cloud-config-v0.1.2) (2023-12-07)


### Features

* Add support for python 3.12 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Introduce compatibility with native namespace packages ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Use `retry_async` instead of `retry` in async client ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-config-v0.1.0...google-cloud-config-v0.1.1) (2023-09-19)


### Documentation

* Minor formatting ([9487380](https://github.com/googleapis/google-cloud-python/commit/94873808ece8059b07644a0a49dedf8e2906900a))

## 0.1.0 (2023-08-31)


### Features

* add initial files for google.cloud.config.v1 ([#11608](https://github.com/googleapis/google-cloud-python/issues/11608)) ([c53680f](https://github.com/googleapis/google-cloud-python/commit/c53680f647738b8fc3f9cce86455dd3f195e4ff6))

## Changelog
