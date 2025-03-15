# Changelog

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.8...google-shopping-merchant-datasources-v0.1.9) (2025-03-15)


### Features

* Add a new destinations field ([9e302ca](https://github.com/googleapis/google-cloud-python/commit/9e302ca598ebc2eddd92b34633c40ba4750e9cfc))


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([25ced24](https://github.com/googleapis/google-cloud-python/commit/25ced2444528a1dc6a22daa32b82b844961f1b75))


### Documentation

* A comment for field `channel` in message `.google.shopping.merchant.datasources.v1beta.PrimaryProductDataSource` is changed ([9e302ca](https://github.com/googleapis/google-cloud-python/commit/9e302ca598ebc2eddd92b34633c40ba4750e9cfc))
* A comment for field `promotion_data_source` in message `.google.shopping.merchant.datasources.v1beta.DataSource` is changed ([9e302ca](https://github.com/googleapis/google-cloud-python/commit/9e302ca598ebc2eddd92b34633c40ba4750e9cfc))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.7...google-shopping-merchant-datasources-v0.1.8) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))
* Add support for reading selective GAPIC generation methods from service YAML ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.6...google-shopping-merchant-datasources-v0.1.7) (2025-01-13)


### Features

* A new message `MerchantReviewDataSource` is added to specify the datasource of the merchant review ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A new message `ProductReviewDataSource` is added to specify the datasource of the product review ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* New field `merchant_review_data_source` added in message `.google.shopping.merchant.datasources.v1beta.DataSource` to specify the datasource of the merchant review ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* New field product_review_data_source added in message google.shopping.merchant.datasources.v1beta.DataSource to ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))


### Documentation

* A comment for enum value `FETCH` in enum `FileInputType` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for enum value `GOOGLE_SHEETS` in enum `FileInputType` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for field `feed_label` in message `.google.shopping.merchant.datasources.v1beta.SupplementalProductDataSource` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for field `password` in message `.google.shopping.merchant.datasources.v1beta.FileInput` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for field `take_from_data_sources` in message `.google.shopping.merchant.datasources.v1beta.PrimaryProductDataSource` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for field `username` in message `.google.shopping.merchant.datasources.v1beta.FileInput` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))
* A comment for message `SupplementalProductDataSource` is changed ([e89d3b2](https://github.com/googleapis/google-cloud-python/commit/e89d3b2c3ad57fb68a84b02d8683dbb556d5adda))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.5...google-shopping-merchant-datasources-v0.1.6) (2024-12-12)


### Features

* [Many APIs] Add support for opt-in debug logging ([#13349](https://github.com/googleapis/google-cloud-python/issues/13349)) ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.4...google-shopping-merchant-datasources-v0.1.5) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.3...google-shopping-merchant-datasources-v0.1.4) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.2...google-shopping-merchant-datasources-v0.1.3) (2024-10-08)


### Features

* Add FileUploads service ([c859d14](https://github.com/googleapis/google-cloud-python/commit/c859d14990dbdf2c59a09265b1c91479f134aaa6))
* adding some more information about supplemental data sources ([c859d14](https://github.com/googleapis/google-cloud-python/commit/c859d14990dbdf2c59a09265b1c91479f134aaa6))


### Documentation

* A comment for enum value `PRODUCTS` in enum `Channel` is changed ([c859d14](https://github.com/googleapis/google-cloud-python/commit/c859d14990dbdf2c59a09265b1c91479f134aaa6))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.1...google-shopping-merchant-datasources-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-datasources-v0.1.0...google-shopping-merchant-datasources-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## 0.1.0 (2024-06-05)


### Features

* add initial files for google.shopping.merchant.datasources.v1beta ([#12772](https://github.com/googleapis/google-cloud-python/issues/12772)) ([8aedd28](https://github.com/googleapis/google-cloud-python/commit/8aedd289e38b549d84fd7a2e19b3685fc377cc2a))

## Changelog
