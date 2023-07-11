# Changelog

## [1.11.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-deploy-v1.10.1...google-cloud-deploy-v1.11.0) (2023-07-11)


### Features

* added support routeUpdateWaitTime field for Deployment Strategies ([#11478](https://github.com/googleapis/google-cloud-python/issues/11478)) ([c1ebd34](https://github.com/googleapis/google-cloud-python/commit/c1ebd34e3ed674ba1058e5aa01600814edbd0727))

## [1.10.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-deploy-v1.10.0...google-cloud-deploy-v1.10.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## [1.10.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-deploy-v1.9.0...google-cloud-deploy-v1.10.0) (2023-06-21)


### Features

* Add deploy parameters for cloud deploy ([1fcd772](https://github.com/googleapis/google-cloud-python/commit/1fcd7721b34232b07eb69e92ec13f20f103b224f))
* Add support for disabling Pod overprovisioning in the progressive deployment strategy configuration for a Kubernetes Target ([1fcd772](https://github.com/googleapis/google-cloud-python/commit/1fcd7721b34232b07eb69e92ec13f20f103b224f))

## [1.9.0](https://github.com/googleapis/python-deploy/compare/v1.8.0...v1.9.0) (2023-05-25)


### Features

* Added support for DeployArtifacts ([3c6733e](https://github.com/googleapis/python-deploy/commit/3c6733ea3523bde28ac43a0e1e443e5d5ae4dc32))
* Added support for in cluster verification ([3c6733e](https://github.com/googleapis/python-deploy/commit/3c6733ea3523bde28ac43a0e1e443e5d5ae4dc32))

## [1.8.0](https://github.com/googleapis/python-deploy/compare/v1.7.0...v1.8.0) (2023-03-24)


### Features

* Added supported for Cloud Deploy Progressive Deployment Strategy ([f8f2a5e](https://github.com/googleapis/python-deploy/commit/f8f2a5eda3069e85716fea58987485374e60fa49))


### Documentation

* Deprecate TYPE_RENDER_STATUES_CHANGE, use RELEASE_RENDER log type instead ([f8f2a5e](https://github.com/googleapis/python-deploy/commit/f8f2a5eda3069e85716fea58987485374e60fa49))
* Fix formatting of request arg in docstring ([f8f2a5e](https://github.com/googleapis/python-deploy/commit/f8f2a5eda3069e85716fea58987485374e60fa49))

## [1.7.0](https://github.com/googleapis/python-deploy/compare/v1.6.1...v1.7.0) (2023-02-16)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#155](https://github.com/googleapis/python-deploy/issues/155)) ([3d6d5fe](https://github.com/googleapis/python-deploy/commit/3d6d5fe5c742361a9b00c4826e98d1d450743931))

## [1.6.1](https://github.com/googleapis/python-deploy/compare/v1.6.0...v1.6.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([24facad](https://github.com/googleapis/python-deploy/commit/24facade12e7fa2fc41bc58ca9570acf3877e3f3))


### Documentation

* Add documentation for enums ([24facad](https://github.com/googleapis/python-deploy/commit/24facade12e7fa2fc41bc58ca9570acf3877e3f3))

## [1.6.0](https://github.com/googleapis/python-deploy/compare/v1.5.0...v1.6.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#147](https://github.com/googleapis/python-deploy/issues/147)) ([13de673](https://github.com/googleapis/python-deploy/commit/13de6730b4471d62fdeb17ab07b381d96004d194))

## [1.5.0](https://github.com/googleapis/python-deploy/compare/v1.4.1...v1.5.0) (2022-12-15)


### Features

* Add support for `google.cloud.deploy.__version__` ([7e8512a](https://github.com/googleapis/python-deploy/commit/7e8512ae846ec1e356e3a99d64b1664f3c23e268))
* Add typing to proto.Message based class attributes ([7e8512a](https://github.com/googleapis/python-deploy/commit/7e8512ae846ec1e356e3a99d64b1664f3c23e268))


### Bug Fixes

* Add dict typing for client_options ([7e8512a](https://github.com/googleapis/python-deploy/commit/7e8512ae846ec1e356e3a99d64b1664f3c23e268))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([2e193c3](https://github.com/googleapis/python-deploy/commit/2e193c3e0369a02bd0feba4f7d0fb4a65a3df935))
* Drop usage of pkg_resources ([2e193c3](https://github.com/googleapis/python-deploy/commit/2e193c3e0369a02bd0feba4f7d0fb4a65a3df935))
* Fix timeout default values ([2e193c3](https://github.com/googleapis/python-deploy/commit/2e193c3e0369a02bd0feba4f7d0fb4a65a3df935))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([7e8512a](https://github.com/googleapis/python-deploy/commit/7e8512ae846ec1e356e3a99d64b1664f3c23e268))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([2e193c3](https://github.com/googleapis/python-deploy/commit/2e193c3e0369a02bd0feba4f7d0fb4a65a3df935))

## [1.4.1](https://github.com/googleapis/python-deploy/compare/v1.4.0...v1.4.1) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#137](https://github.com/googleapis/python-deploy/issues/137)) ([045381a](https://github.com/googleapis/python-deploy/commit/045381a445a610629d06016b0637b365f1299983))

## [1.4.0](https://github.com/googleapis/python-deploy/compare/v1.3.1...v1.4.0) (2022-09-29)


### Features

* Publish new JobRun resource and associated methods for Google Cloud Deploy ([#133](https://github.com/googleapis/python-deploy/issues/133)) ([03ab410](https://github.com/googleapis/python-deploy/commit/03ab410ee01e20e3d1051fa8d8003300c871d82c))


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#135](https://github.com/googleapis/python-deploy/issues/135)) ([c271ac1](https://github.com/googleapis/python-deploy/commit/c271ac1163bda6cc415c41c0a2651a7f72dd40fe))

## [1.3.1](https://github.com/googleapis/python-deploy/compare/v1.3.0...v1.3.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#118](https://github.com/googleapis/python-deploy/issues/118)) ([8afd6d3](https://github.com/googleapis/python-deploy/commit/8afd6d3ba9171ab957547245294305dd78101767))
* **deps:** require proto-plus >= 1.22.0 ([8afd6d3](https://github.com/googleapis/python-deploy/commit/8afd6d3ba9171ab957547245294305dd78101767))

## [1.3.0](https://github.com/googleapis/python-deploy/compare/v1.2.1...v1.3.0) (2022-07-14)


### Features

* add audience parameter ([580906e](https://github.com/googleapis/python-deploy/commit/580906ef7eb335df2de5802c29fac08c3a231b80))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#109](https://github.com/googleapis/python-deploy/issues/109)) ([580906e](https://github.com/googleapis/python-deploy/commit/580906ef7eb335df2de5802c29fac08c3a231b80))
* require python 3.7+ ([#111](https://github.com/googleapis/python-deploy/issues/111)) ([5d60fe9](https://github.com/googleapis/python-deploy/commit/5d60fe95eda61d86cd08b1173ee2551594d6f94d))

## [1.2.1](https://github.com/googleapis/python-deploy/compare/v1.2.0...v1.2.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#99](https://github.com/googleapis/python-deploy/issues/99)) ([5f58f57](https://github.com/googleapis/python-deploy/commit/5f58f5744097cfb9bfbe933e2e56bc198a0436b3))


### Documentation

* fix changelog header to consistent size ([#100](https://github.com/googleapis/python-deploy/issues/100)) ([d13fd2d](https://github.com/googleapis/python-deploy/commit/d13fd2dd4bd260879e9795174465639d5dcd4108))

## [1.2.0](https://github.com/googleapis/python-deploy/compare/v1.1.1...v1.2.0) (2022-05-06)


### Features

* Add support for Anthos worker pool ([#61](https://github.com/googleapis/python-deploy/issues/61)) ([f5105a4](https://github.com/googleapis/python-deploy/commit/f5105a425f4f164aa7db948b3c82e2aa59dd64ce))

## [1.1.1](https://github.com/googleapis/python-deploy/compare/v1.1.0...v1.1.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#49](https://github.com/googleapis/python-deploy/issues/49)) ([248b59b](https://github.com/googleapis/python-deploy/commit/248b59b841ba0f665e63a7f99bd9adc55a7c9aa7))

## [1.1.0](https://github.com/googleapis/python-deploy/compare/v1.0.0...v1.1.0) (2022-02-26)


### Features

* add api key support ([#35](https://github.com/googleapis/python-deploy/issues/35)) ([aaa957f](https://github.com/googleapis/python-deploy/commit/aaa957f2673db673c3a8e38275d4689323ded044))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([9bd690d](https://github.com/googleapis/python-deploy/commit/9bd690d27c07159059aa26a86df44e304dc431fd))

## [1.0.0](https://www.github.com/googleapis/python-deploy/compare/v0.3.0...v1.0.0) (2021-11-01)


### Features

* bump release level to production/stable ([#3](https://www.github.com/googleapis/python-deploy/issues/3)) ([8bf3167](https://www.github.com/googleapis/python-deploy/commit/8bf31670c8a488d9c2eb39eae558e043e70d880e))


### Bug Fixes

* **deps:** drop packaging dependency ([17baf34](https://www.github.com/googleapis/python-deploy/commit/17baf34008aa7a2afffe8bba6d8cc6df6d064678))
* **deps:** require google-api-core >= 1.28.0 ([17baf34](https://www.github.com/googleapis/python-deploy/commit/17baf34008aa7a2afffe8bba6d8cc6df6d064678))


### Documentation

* list oneofs in docstring ([17baf34](https://www.github.com/googleapis/python-deploy/commit/17baf34008aa7a2afffe8bba6d8cc6df6d064678))

## [0.3.0](https://www.github.com/googleapis/python-deploy/compare/v0.2.0...v0.3.0) (2021-10-18)


### Features

* add trove classifier for python 3.10 ([#12](https://www.github.com/googleapis/python-deploy/issues/12)) ([4838541](https://www.github.com/googleapis/python-deploy/commit/48385418dbea54dee65432f5e0255f305c246bbe))


### Documentation

* fix docstring formatting ([#16](https://www.github.com/googleapis/python-deploy/issues/16)) ([27d0cbe](https://www.github.com/googleapis/python-deploy/commit/27d0cbe3603e459392480c641e08eb1cff839d4d))

## [0.2.0](https://www.github.com/googleapis/python-deploy/compare/v0.1.1...v0.2.0) (2021-10-08)


### Features

* add context manager support in client ([#9](https://www.github.com/googleapis/python-deploy/issues/9)) ([bdcf454](https://www.github.com/googleapis/python-deploy/commit/bdcf454b8d976004caa7ef5bcccf9f928cfbfe63))

## [0.1.1](https://www.github.com/googleapis/python-deploy/compare/v0.1.0...v0.1.1) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([699cbdc](https://www.github.com/googleapis/python-deploy/commit/699cbdcb91e93045c6c8bc4cfbd6fe92f59e739b))

## 0.1.0 (2021-09-27)


### Features

* generate v1 ([7435abf](https://www.github.com/googleapis/python-deploy/commit/7435abff524e45f2ed0f90f479f1ca5e9cba1730))
