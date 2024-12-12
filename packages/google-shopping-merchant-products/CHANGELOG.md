# Changelog

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-products-v0.1.4...google-shopping-merchant-products-v0.2.0) (2024-12-12)


### ⚠ BREAKING CHANGES

* Changed repeated flag of an existing field `gtin` in message `.google.shopping.merchant.products.v1beta.Attributes`
* An existing field `gtin` is moved out of oneof in message `.google.shopping.merchant.products.v1beta.Attributes`

### Features

* A new field `member_price_effective_date` is added to message `.google.shopping.merchant.products.v1beta.LoyaltyProgram` ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A new field `shipping_label` is added to message `.google.shopping.merchant.products.v1beta.LoyaltyProgram` ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* Add support for opt-in debug logging ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))


### Bug Fixes

* An existing field `gtin` is moved out of oneof in message `.google.shopping.merchant.products.v1beta.Attributes` ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* Changed repeated flag of an existing field `gtin` in message `.google.shopping.merchant.products.v1beta.Attributes` ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* Fix typing issue with gRPC metadata when key ends in -bin ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))


### Documentation

* A comment for field `gtin` in message `.google.shopping.merchant.products.v1beta.Attributes` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `max_handling_time` in message `.google.shopping.merchant.products.v1beta.Shipping` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `max_transit_time` in message `.google.shopping.merchant.products.v1beta.Shipping` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `min_handling_time` in message `.google.shopping.merchant.products.v1beta.Shipping` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `min_transit_time` in message `.google.shopping.merchant.products.v1beta.Shipping` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `name` in message `.google.shopping.merchant.products.v1beta.DeleteProductInputRequest` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `name` in message `.google.shopping.merchant.products.v1beta.GetProductRequest` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `name` in message `.google.shopping.merchant.products.v1beta.Product` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `name` in message `.google.shopping.merchant.products.v1beta.ProductInput` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `page_size` in message `.google.shopping.merchant.products.v1beta.ListProductsRequest` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for field `tax_category` in message `.google.shopping.merchant.products.v1beta.Attributes` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for message `Product` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))
* A comment for message `ProductInput` is changed ([ce5c35a](https://github.com/googleapis/google-cloud-python/commit/ce5c35ad8b98f548a3dc8bd862646702b1d9974b))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-products-v0.1.3...google-shopping-merchant-products-v0.1.4) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13248](https://github.com/googleapis/google-cloud-python/issues/13248)) ([634f3e7](https://github.com/googleapis/google-cloud-python/commit/634f3e740926506654efa82a4f7a8d5f7e3cf6ba))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-products-v0.1.2...google-shopping-merchant-products-v0.1.3) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-products-v0.1.1...google-shopping-merchant-products-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([11c0629](https://github.com/googleapis/google-cloud-python/commit/11c06293cef3391f5fb433d5de26c066943082d0))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-products-v0.1.0...google-shopping-merchant-products-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([eb36e8a](https://github.com/googleapis/google-cloud-python/commit/eb36e8a5e779717977132f605aa2ebc3cad78517))

## 0.1.0 (2024-06-05)


### Features

* add initial files for google.shopping.merchant.products.v1beta ([#12776](https://github.com/googleapis/google-cloud-python/issues/12776)) ([e1e7dbb](https://github.com/googleapis/google-cloud-python/commit/e1e7dbb1e65883436fdc520f96caabfcf9ab7b46))

## Changelog
