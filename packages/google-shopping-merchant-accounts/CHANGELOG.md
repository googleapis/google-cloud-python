# Changelog

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.1.3...google-shopping-merchant-accounts-v0.2.0) (2024-10-08)


### ⚠ BREAKING CHANGES

* The type of an existing field `time_zone` is changed from `message` to `string` in message `.google.shopping.merchant.accounts.v1beta.ListAccountIssuesRequest`
* An existing field `account_aggregation` is removed from message `.google.shopping.merchant.accounts.v1beta.CreateAndConfigureAccountRequest`
* Changed field behavior for an existing field `service` in message `.google.shopping.merchant.accounts.v1beta.CreateAndConfigureAccountRequest`
* Changed field behavior for an existing field `region_code` in message `.google.shopping.merchant.accounts.v1beta.RetrieveLatestTermsOfServiceRequest`
* Changed field behavior for an existing field `kind` in message `.google.shopping.merchant.accounts.v1beta.RetrieveLatestTermsOfServiceRequest`

### Features

* A new field `account_aggregation` is added to message `.google.shopping.merchant.accounts.v1beta.CreateAndConfigureAccountRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new field `korean_business_registration_number` is added to message `.google.shopping.merchant.accounts.v1beta.BusinessInfo` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new message `AccountAggregation` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new message `AutofeedSettings` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new message `GetAutofeedSettingsRequest` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new message `UpdateAutofeedSettingsRequest` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new resource_definition `[merchantapi.googleapis.com/AutofeedSettings](https://www.google.com/url?sa=D&q=http%3A%2F%2Fmerchantapi.googleapis.com%2FAutofeedSettings)` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* A new service `AutofeedSettingsService` is added ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* add 'force' parameter for accounts.delete method ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))


### Bug Fixes

* An existing field `account_aggregation` is removed from message `.google.shopping.merchant.accounts.v1beta.CreateAndConfigureAccountRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* Changed field behavior for an existing field `kind` in message `.google.shopping.merchant.accounts.v1beta.RetrieveLatestTermsOfServiceRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* Changed field behavior for an existing field `region_code` in message `.google.shopping.merchant.accounts.v1beta.RetrieveLatestTermsOfServiceRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* Changed field behavior for an existing field `service` in message `.google.shopping.merchant.accounts.v1beta.CreateAndConfigureAccountRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))
* The type of an existing field `time_zone` is changed from `message` to `string` in message `.google.shopping.merchant.accounts.v1beta.ListAccountIssuesRequest` ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))


### Documentation

* updated descriptions for the DeleteAccount and ListAccounts RPCs ([8d79ca8](https://github.com/googleapis/google-cloud-python/commit/8d79ca81a3f2f01a1f0c77231e77566860f1d4ab))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.1.2...google-shopping-merchant-accounts-v0.1.3) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.1.1...google-shopping-merchant-accounts-v0.1.2) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.1.0...google-shopping-merchant-accounts-v0.1.1) (2024-06-10)


### Documentation

* [google-shopping-merchant-accounts] Format comments in ListUsersRequest ([#12786](https://github.com/googleapis/google-cloud-python/issues/12786)) ([be7afbb](https://github.com/googleapis/google-cloud-python/commit/be7afbbffe243120fc616fd5d80a6d86197653cf))

## 0.1.0 (2024-06-05)


### Features

* add initial files for google.shopping.merchant.accounts.v1beta ([#12773](https://github.com/googleapis/google-cloud-python/issues/12773)) ([108875d](https://github.com/googleapis/google-cloud-python/commit/108875d1a38f31013ed98feddbef61cfb09e1d16))

## Changelog
