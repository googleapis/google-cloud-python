# Changelog

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.3.0...google-shopping-merchant-accounts-v0.3.1) (2025-03-15)


### Features

* [google-shopping-merchant-accounts] Add AutomaticImprovements service ([#13654](https://github.com/googleapis/google-cloud-python/issues/13654)) ([de91574](https://github.com/googleapis/google-cloud-python/commit/de91574cdaeb557fcfce2dde03e633df96392012))


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([25ced24](https://github.com/googleapis/google-cloud-python/commit/25ced2444528a1dc6a22daa32b82b844961f1b75))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.2.4...google-shopping-merchant-accounts-v0.3.0) (2025-03-06)


### ⚠ BREAKING CHANGES

* An existing optional field `type` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy
* An existing optional field `label` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy
* An existing optional field `countries` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy
* An existing optional field `return_policy_uri` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy

### Features

* A new field `seasonal_overrides` is added to message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* A new message `SeasonalOverride` is added ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))


### Bug Fixes

* An existing optional field `countries` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* An existing optional field `label` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* An existing optional field `return_policy_uri` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* An existing optional field `type` is converted to required field in message .google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))


### Documentation

* The documentation for field `countries` in message `.google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for field `label` in message `.google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for field `parent` in message `.google.shopping.merchant.accounts.v1beta.ListOnlineReturnPoliciesRequest` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for field `return_policy_uri` in message `.google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for field `type` in message `.google.shopping.merchant.accounts.v1beta.OnlineReturnPolicy` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for method `GetOnlineReturnPolicy` in service `OnlineReturnPolicyService` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))
* The documentation for method `ListOnlineReturnPolicies` in service `OnlineReturnPolicyService` is improved ([0d67a43](https://github.com/googleapis/google-cloud-python/commit/0d67a43217055096adcc825455011e4a7dfa40e7))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.2.3...google-shopping-merchant-accounts-v0.2.4) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))
* Add support for reading selective GAPIC generation methods from service YAML ([30b675e](https://github.com/googleapis/google-cloud-python/commit/30b675e7e9eaee87f9e7bdf4dc910b01f6a3044f))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.2.2...google-shopping-merchant-accounts-v0.2.3) (2024-12-12)


### Features

* [Many APIs] Add support for opt-in debug logging ([#13349](https://github.com/googleapis/google-cloud-python/issues/13349)) ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.2.1...google-shopping-merchant-accounts-v0.2.2) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-shopping-merchant-accounts-v0.2.0...google-shopping-merchant-accounts-v0.2.1) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

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
