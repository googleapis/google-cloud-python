# Changelog

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.13...google-shopping-merchant-reports-v0.1.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([36e8ba1](https://github.com/googleapis/google-cloud-python/commit/36e8ba12eac92dd221ac3ddf1061da3845135791))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.12...google-shopping-merchant-reports-v0.1.13) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))
* Add support for reading selective GAPIC generation methods from service YAML ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.11...google-shopping-merchant-reports-v0.1.12) (2024-12-12)


### Features

* [Many APIs] Add support for opt-in debug logging ([#13349](https://github.com/googleapis/google-cloud-python/issues/13349)) ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.10...google-shopping-merchant-reports-v0.1.11) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13248](https://github.com/googleapis/google-cloud-python/issues/13248)) ([634f3e7](https://github.com/googleapis/google-cloud-python/commit/634f3e740926506654efa82a4f7a8d5f7e3cf6ba))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.9...google-shopping-merchant-reports-v0.1.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13212](https://github.com/googleapis/google-cloud-python/issues/13212)) ([94d00a1](https://github.com/googleapis/google-cloud-python/commit/94d00a126aa436513d23b25993b7fdc106809441))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.8...google-shopping-merchant-reports-v0.1.9) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([11c0629](https://github.com/googleapis/google-cloud-python/commit/11c06293cef3391f5fb433d5de26c066943082d0))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.7...google-shopping-merchant-reports-v0.1.8) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([eb36e8a](https://github.com/googleapis/google-cloud-python/commit/eb36e8a5e779717977132f605aa2ebc3cad78517))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.6...google-shopping-merchant-reports-v0.1.7) (2024-05-27)


### Features

* add a new enum `Effectiveness` ([0da7370](https://github.com/googleapis/google-cloud-python/commit/0da7370d5d21557bb0c04b8c9b1c46c9a583ad1d))
* add a new field `effectiveness` to message `.google.shopping.merchant.reports.v1beta.PriceInsightsProductView` ([0da7370](https://github.com/googleapis/google-cloud-python/commit/0da7370d5d21557bb0c04b8c9b1c46c9a583ad1d))
* add non_product_performance_view table to Reports sub-API ([0da7370](https://github.com/googleapis/google-cloud-python/commit/0da7370d5d21557bb0c04b8c9b1c46c9a583ad1d))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.5...google-shopping-merchant-reports-v0.1.6) (2024-04-15)


### Features

* [google-shopping-merchant-reports] Add click potential to Reports sub-API ([#12557](https://github.com/googleapis/google-cloud-python/issues/12557)) ([bd69999](https://github.com/googleapis/google-cloud-python/commit/bd69999f52d31437719c660fa2b0b389b0dfc23f))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.4...google-shopping-merchant-reports-v0.1.5) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12389](https://github.com/googleapis/google-cloud-python/issues/12389)) ([5db9352](https://github.com/googleapis/google-cloud-python/commit/5db93528a1ad20825d4d12dcf5fdf9624879f2ce))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.3...google-shopping-merchant-reports-v0.1.4) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12311](https://github.com/googleapis/google-cloud-python/issues/12311)) ([e4c864b](https://github.com/googleapis/google-cloud-python/commit/e4c864b3e67c7f7f33dfb0d2107fa138492ad338))
* fix ValueError in test__validate_universe_domain ([f3974d4](https://github.com/googleapis/google-cloud-python/commit/f3974d46a9ba9f549e31251ebc2daeb6b9b4745a))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.2...google-shopping-merchant-reports-v0.1.3) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.1...google-shopping-merchant-reports-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12245](https://github.com/googleapis/google-cloud-python/issues/12245)) ([4fce462](https://github.com/googleapis/google-cloud-python/commit/4fce46283482bc303fd9bf8b25c3e74b2e619d6c))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-reports-v0.1.0...google-shopping-merchant-reports-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Introduce compatibility with native namespace packages ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Use `retry_async` instead of `retry` in async client ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))

## 0.1.0 (2023-11-07)


### Features

* add initial files for google.shopping.merchant.reports.v1beta ([#11990](https://github.com/googleapis/google-cloud-python/issues/11990)) ([e0892fd](https://github.com/googleapis/google-cloud-python/commit/e0892fdc069b6c2a5b5c94a23f27482a63622fde))

## Changelog
