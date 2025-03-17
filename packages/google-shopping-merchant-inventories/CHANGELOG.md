# Changelog

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.13...google-shopping-merchant-inventories-v0.1.14) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([25ced24](https://github.com/googleapis/google-cloud-python/commit/25ced2444528a1dc6a22daa32b82b844961f1b75))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.12...google-shopping-merchant-inventories-v0.1.13) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))
* Add support for reading selective GAPIC generation methods from service YAML ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.11...google-shopping-merchant-inventories-v0.1.12) (2024-12-12)


### Features

* [Many APIs] Add support for opt-in debug logging ([#13349](https://github.com/googleapis/google-cloud-python/issues/13349)) ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.10...google-shopping-merchant-inventories-v0.1.11) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.9...google-shopping-merchant-inventories-v0.1.10) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.8...google-shopping-merchant-inventories-v0.1.9) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.7...google-shopping-merchant-inventories-v0.1.8) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.6...google-shopping-merchant-inventories-v0.1.7) (2024-05-27)


### Documentation

* change in wording : feed specification -&gt; data specification ([995bdaf](https://github.com/googleapis/google-cloud-python/commit/995bdaf5d95fcbfae7ee63393fb394cc2dba687a))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.5...google-shopping-merchant-inventories-v0.1.6) (2024-04-15)


### Documentation

* Add `Immutable` in comment for field `region` in message `RegionalInventory` ([7b2fadf](https://github.com/googleapis/google-cloud-python/commit/7b2fadf9b68fd57adc0c9e17d4b44463d5eee68d))
* Add `Immutable` in comment for field `store_code` in message `LocalInventory` ([7b2fadf](https://github.com/googleapis/google-cloud-python/commit/7b2fadf9b68fd57adc0c9e17d4b44463d5eee68d))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.4...google-shopping-merchant-inventories-v0.1.5) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12389](https://github.com/googleapis/google-cloud-python/issues/12389)) ([5db9352](https://github.com/googleapis/google-cloud-python/commit/5db93528a1ad20825d4d12dcf5fdf9624879f2ce))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.3...google-shopping-merchant-inventories-v0.1.4) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12311](https://github.com/googleapis/google-cloud-python/issues/12311)) ([e4c864b](https://github.com/googleapis/google-cloud-python/commit/e4c864b3e67c7f7f33dfb0d2107fa138492ad338))
* fix ValueError in test__validate_universe_domain ([f3974d4](https://github.com/googleapis/google-cloud-python/commit/f3974d46a9ba9f549e31251ebc2daeb6b9b4745a))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.2...google-shopping-merchant-inventories-v0.1.3) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.1...google-shopping-merchant-inventories-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12245](https://github.com/googleapis/google-cloud-python/issues/12245)) ([4fce462](https://github.com/googleapis/google-cloud-python/commit/4fce46283482bc303fd9bf8b25c3e74b2e619d6c))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-inventories-v0.1.0...google-shopping-merchant-inventories-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Introduce compatibility with native namespace packages ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Use `retry_async` instead of `retry` in async client ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))

## 0.1.0 (2023-11-07)


### Features

* add initial files for google.shopping.merchant.inventories.v1beta ([#11991](https://github.com/googleapis/google-cloud-python/issues/11991)) ([0c1e8e2](https://github.com/googleapis/google-cloud-python/commit/0c1e8e2dd4b0683e67f3d637f3af977f3fe1510e))

## Changelog
