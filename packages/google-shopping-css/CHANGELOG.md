# Changelog

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.10...google-shopping-css-v0.1.11) (2024-12-12)


### Features

* Add support for opt-in debug logging ([74833d3](https://github.com/googleapis/google-cloud-python/commit/74833d3e77bb5869bd9f2290c23be7ccaa20193f))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([74833d3](https://github.com/googleapis/google-cloud-python/commit/74833d3e77bb5869bd9f2290c23be7ccaa20193f))


### Documentation

* fix comment on list account labels ([74833d3](https://github.com/googleapis/google-cloud-python/commit/74833d3e77bb5869bd9f2290c23be7ccaa20193f))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.9...google-shopping-css-v0.1.10) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.8...google-shopping-css-v0.1.9) (2024-10-24)


### Features

* [google-shopping-css] A new field `headline_offer_installment` is added to message `.google.shopping.css.v1.Attributes` ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))
* A new enum `SubscriptionPeriod` is added ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))
* A new field `headline_offer_subscription_cost` is added to message `.google.shopping.css.v1.Attributes` ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))
* A new message `HeadlineOfferInstallment` is added ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))
* A new message `HeadlineOfferSubscriptionCost` is added ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))
* Add support for Python 3.13 ([a58483b](https://github.com/googleapis/google-cloud-python/commit/a58483bb35af03727b6c7dec0dbb27dba4b62c1d))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.7...google-shopping-css-v0.1.8) (2024-08-22)


### Documentation

* [google-shopping-css] update `Certification` field descriptions ([#13027](https://github.com/googleapis/google-cloud-python/issues/13027)) ([70e2dd5](https://github.com/googleapis/google-cloud-python/commit/70e2dd5f024dd5c94a5e02b442bbab7e6e5f38fe))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.6...google-shopping-css-v0.1.7) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.5...google-shopping-css-v0.1.6) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.4...google-shopping-css-v0.1.5) (2024-06-19)


### Documentation

* Remove "in Google Shopping" from documentation comments ([3a0a439](https://github.com/googleapis/google-cloud-python/commit/3a0a439ce9e43f88959babfa267e14bae10f8538))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.3...google-shopping-css-v0.1.4) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12389](https://github.com/googleapis/google-cloud-python/issues/12389)) ([5db9352](https://github.com/googleapis/google-cloud-python/commit/5db93528a1ad20825d4d12dcf5fdf9624879f2ce))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.2...google-shopping-css-v0.1.3) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12311](https://github.com/googleapis/google-cloud-python/issues/12311)) ([e4c864b](https://github.com/googleapis/google-cloud-python/commit/e4c864b3e67c7f7f33dfb0d2107fa138492ad338))
* fix ValueError in test__validate_universe_domain ([f3974d4](https://github.com/googleapis/google-cloud-python/commit/f3974d46a9ba9f549e31251ebc2daeb6b9b4745a))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.1...google-shopping-css-v0.1.2) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-css-v0.1.0...google-shopping-css-v0.1.1) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12245](https://github.com/googleapis/google-cloud-python/issues/12245)) ([4fce462](https://github.com/googleapis/google-cloud-python/commit/4fce46283482bc303fd9bf8b25c3e74b2e619d6c))

## 0.1.0 (2023-12-12)


### Features

* add initial files for google.shopping.css.v1 ([#12114](https://github.com/googleapis/google-cloud-python/issues/12114)) ([94e63cb](https://github.com/googleapis/google-cloud-python/commit/94e63cbbfe85b11e5cf38cbaa3511be8833a86f1))

## Changelog
