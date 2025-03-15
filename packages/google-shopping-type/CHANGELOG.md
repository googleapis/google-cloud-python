# Changelog

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.10...google-shopping-type-v0.1.11) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([36e8ba1](https://github.com/googleapis/google-cloud-python/commit/36e8ba12eac92dd221ac3ddf1061da3845135791))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.9...google-shopping-type-v0.1.10) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))
* Add support for reading selective GAPIC generation methods from service YAML ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.8...google-shopping-type-v0.1.9) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13212](https://github.com/googleapis/google-cloud-python/issues/13212)) ([94d00a1](https://github.com/googleapis/google-cloud-python/commit/94d00a126aa436513d23b25993b7fdc106809441))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.7...google-shopping-type-v0.1.8) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([11c0629](https://github.com/googleapis/google-cloud-python/commit/11c06293cef3391f5fb433d5de26c066943082d0))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.6...google-shopping-type-v0.1.7) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([eb36e8a](https://github.com/googleapis/google-cloud-python/commit/eb36e8a5e779717977132f605aa2ebc3cad78517))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.5...google-shopping-type-v0.1.6) (2024-05-07)


### Features

* add Weight to common types for Shopping APIs to be used for accounts bundle ([0e5f93b](https://github.com/googleapis/google-cloud-python/commit/0e5f93b64a30a39f2110163d00d4e845e7731cd4))


### Documentation

* A comment for field amount_micros in message .google.shopping.type.Price is changed ([0e5f93b](https://github.com/googleapis/google-cloud-python/commit/0e5f93b64a30a39f2110163d00d4e845e7731cd4))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.4...google-shopping-type-v0.1.5) (2024-03-27)


### Features

* Add DEMAND_GEN_ADS and DEMAND_GEN_ADS_DISCOVER_SURFACE in ReportingContextEnum ([42b7bb4](https://github.com/googleapis/google-cloud-python/commit/42b7bb4f5ecfa377d391adfa4dab855e134b69dc))


### Documentation

* Deprecate DISCOVERY_ADS and document the new enum values ([42b7bb4](https://github.com/googleapis/google-cloud-python/commit/42b7bb4f5ecfa377d391adfa4dab855e134b69dc))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.3...google-shopping-type-v0.1.4) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12389](https://github.com/googleapis/google-cloud-python/issues/12389)) ([5db9352](https://github.com/googleapis/google-cloud-python/commit/5db93528a1ad20825d4d12dcf5fdf9624879f2ce))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.2...google-shopping-type-v0.1.3) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12311](https://github.com/googleapis/google-cloud-python/issues/12311)) ([e4c864b](https://github.com/googleapis/google-cloud-python/commit/e4c864b3e67c7f7f33dfb0d2107fa138492ad338))
* fix ValueError in test__validate_universe_domain ([f3974d4](https://github.com/googleapis/google-cloud-python/commit/f3974d46a9ba9f549e31251ebc2daeb6b9b4745a))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.1...google-shopping-type-v0.1.2) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-type-v0.1.0...google-shopping-type-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([f920d22](https://github.com/googleapis/google-cloud-python/commit/f920d22f59fbd31822252b9677416a6cd436eba2))
* Introduce compatibility with native namespace packages ([f920d22](https://github.com/googleapis/google-cloud-python/commit/f920d22f59fbd31822252b9677416a6cd436eba2))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([f920d22](https://github.com/googleapis/google-cloud-python/commit/f920d22f59fbd31822252b9677416a6cd436eba2))
* Use `retry_async` instead of `retry` in async client ([f920d22](https://github.com/googleapis/google-cloud-python/commit/f920d22f59fbd31822252b9677416a6cd436eba2))

## 0.1.0 (2023-11-02)


### Features

* add initial files for google.shopping.type ([#11962](https://github.com/googleapis/google-cloud-python/issues/11962)) ([a27b282](https://github.com/googleapis/google-cloud-python/commit/a27b282db23cfca969c7572dfabef09bfe759387))

## Changelog
