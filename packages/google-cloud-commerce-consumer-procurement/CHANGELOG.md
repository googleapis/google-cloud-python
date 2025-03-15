# Changelog

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.12...google-cloud-commerce-consumer-procurement-v0.1.13) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([1e43e75](https://github.com/googleapis/google-cloud-python/commit/1e43e75e99445373785b11381e0e859fa14bb485))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.11...google-cloud-commerce-consumer-procurement-v0.1.12) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))
* Add support for reading selective GAPIC generation methods from service YAML ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.10...google-cloud-commerce-consumer-procurement-v0.1.11) (2024-12-12)


### Features

* Add support for opt-in debug logging ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.9...google-cloud-commerce-consumer-procurement-v0.1.10) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.8...google-cloud-commerce-consumer-procurement-v0.1.9) (2024-10-24)


### Features

* Add support for  Python 3.13 ([6252476](https://github.com/googleapis/google-cloud-python/commit/6252476e5938352fb2417d098a1edcc08558fe10))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.7...google-cloud-commerce-consumer-procurement-v0.1.8) (2024-10-08)


### Features

* add Order modification RPCs and License Management Service ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))


### Documentation

* A comment for enum value `LINE_ITEM_CHANGE_STATE_ABANDONED` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for enum value `LINE_ITEM_CHANGE_STATE_ACTIVATING` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for enum value `LINE_ITEM_CHANGE_STATE_APPROVED` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for enum value `LINE_ITEM_CHANGE_STATE_COMPLETED` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for enum value `LINE_ITEM_CHANGE_STATE_PENDING_APPROVAL` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for enum value `LINE_ITEM_CHANGE_STATE_REJECTED` in enum `LineItemChangeState` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for field `filter` in message `.google.cloud.commerce.consumer.procurement.v1.ListOrdersRequest` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))
* A comment for field `request_id` in message `.google.cloud.commerce.consumer.procurement.v1.PlaceOrderRequest` is changed ([852d797](https://github.com/googleapis/google-cloud-python/commit/852d797f21d4809c32d98b384c60bf9852b14216))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.6...google-cloud-commerce-consumer-procurement-v0.1.7) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([a6f7356](https://github.com/googleapis/google-cloud-python/commit/a6f7356f1549721f9fab83d4dcfa226cec1965d0))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.5...google-cloud-commerce-consumer-procurement-v0.1.6) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.4...google-cloud-commerce-consumer-procurement-v0.1.5) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12383](https://github.com/googleapis/google-cloud-python/issues/12383)) ([305f43f](https://github.com/googleapis/google-cloud-python/commit/305f43f7d6293e3316248f421fdc19c5d8405c21))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.3...google-cloud-commerce-consumer-procurement-v0.1.4) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12282](https://github.com/googleapis/google-cloud-python/issues/12282)) ([b985096](https://github.com/googleapis/google-cloud-python/commit/b985096d43add8214172ff993e00293e6c8757cb))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12305](https://github.com/googleapis/google-cloud-python/issues/12305)) ([2aa7f17](https://github.com/googleapis/google-cloud-python/commit/2aa7f17a5fd4f2249260225db91fb0414d06eaa7))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.2...google-cloud-commerce-consumer-procurement-v0.1.3) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([f3db074](https://github.com/googleapis/google-cloud-python/commit/f3db074e7bbf505d5989e4c353461ab6bef4905c))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.1...google-cloud-commerce-consumer-procurement-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12238](https://github.com/googleapis/google-cloud-python/issues/12238)) ([8701267](https://github.com/googleapis/google-cloud-python/commit/8701267fc9694844b9365024cd59354785247aa0))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-commerce-consumer-procurement-v0.1.0...google-cloud-commerce-consumer-procurement-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Introduce compatibility with native namespace packages ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))
* Use `retry_async` instead of `retry` in async client ([b96013d](https://github.com/googleapis/google-cloud-python/commit/b96013d2c31e3602bb885bf8d7296cc49c3a4642))

## 0.1.0 (2023-09-19)


### Features

* add initial files for google.cloud.commerce.consumer.procurement.v1 ([#11522](https://github.com/googleapis/google-cloud-python/issues/11522)) ([aa4f325](https://github.com/googleapis/google-cloud-python/commit/aa4f325dc08f24b925abd4be36f87851319c2542))
* add initial files for google.cloud.commerce.consumer.procurement.v1 ([#11669](https://github.com/googleapis/google-cloud-python/issues/11669)) ([247caea](https://github.com/googleapis/google-cloud-python/commit/247caeabca57b622fc14e18a7f7f1cb2ccb0c460))

## Changelog
