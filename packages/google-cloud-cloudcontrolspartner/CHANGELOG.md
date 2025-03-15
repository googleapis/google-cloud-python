# Changelog

## [0.2.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.5...google-cloud-cloudcontrolspartner-v0.2.6) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([1e43e75](https://github.com/googleapis/google-cloud-python/commit/1e43e75e99445373785b11381e0e859fa14bb485))

## [0.2.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.4...google-cloud-cloudcontrolspartner-v0.2.5) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))
* Add support for reading selective GAPIC generation methods from service YAML ([e22e2bd](https://github.com/googleapis/google-cloud-python/commit/e22e2bde55d11d2f85e9d2caf1d152a4027f88cf))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.3...google-cloud-cloudcontrolspartner-v0.2.4) (2025-01-27)


### Features

* A new field `organization_domain` is added to message `.google.cloud.cloudcontrolspartner.v1beta.Customer` ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new message `CreateCustomerRequest` is added ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new message `DeleteCustomerRequest` is added ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new message `UpdateCustomerRequest` is added ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new method `CreateCustomer` is added to service `CloudControlsPartnerCore` ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new method `DeleteCustomer` is added to service `CloudControlsPartnerCore` ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A new method `UpdateCustomer` is added to service `CloudControlsPartnerCore` ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))


### Documentation

* A comment for enum value `VIRTRU` in enum `EkmSolution` is changed ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))
* A comment for field `requested_cancellation` in message `.google.cloud.cloudcontrolspartner.v1beta.OperationMetadata` is changed ([1913b6c](https://github.com/googleapis/google-cloud-python/commit/1913b6cc099c50650b2a35c2f05b7e0da1157791))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.2...google-cloud-cloudcontrolspartner-v0.2.3) (2024-12-12)


### Features

* Add support for opt-in debug logging ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([19ed3be](https://github.com/googleapis/google-cloud-python/commit/19ed3bec7fcbc09aa5828180778ffc828d3eafa3))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.1...google-cloud-cloudcontrolspartner-v0.2.2) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.2.0...google-cloud-cloudcontrolspartner-v0.2.1) (2024-10-24)


### Features

* Add support for  Python 3.13 ([6252476](https://github.com/googleapis/google-cloud-python/commit/6252476e5938352fb2417d098a1edcc08558fe10))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.1.3...google-cloud-cloudcontrolspartner-v0.2.0) (2024-09-16)


### ⚠ BREAKING CHANGES

* [google-cloud-cloudcontrolspartner] Field behavior for field display_name in message .google.cloud.cloudcontrolspartner.v1beta.Customer is changed

### Features

* A new value `ACCESS_TRANSPARENCY_LOGS_SUPPORT_CASE_VIEWER` is added to enum `.google.cloud.cloudcontrolspartner.v1beta.PartnerPermissions.Permission` ([c03c441](https://github.com/googleapis/google-cloud-python/commit/c03c4411287ee195fd5c99aff94d812381a908f3))
* Field behavior for field `customer_onboarding_state` in message `.google.cloud.cloudcontrolspartner.v1beta.Customer` is changed ([c03c441](https://github.com/googleapis/google-cloud-python/commit/c03c4411287ee195fd5c99aff94d812381a908f3))
* Field behavior for field `is_onboarded` in message `.google.cloud.cloudcontrolspartner.v1beta.Customer` is changed ([c03c441](https://github.com/googleapis/google-cloud-python/commit/c03c4411287ee195fd5c99aff94d812381a908f3))


### Bug Fixes

* [google-cloud-cloudcontrolspartner] Field behavior for field display_name in message .google.cloud.cloudcontrolspartner.v1beta.Customer is changed ([c03c441](https://github.com/googleapis/google-cloud-python/commit/c03c4411287ee195fd5c99aff94d812381a908f3))


### Documentation

* A comment for field `display_name` in message `.google.cloud.cloudcontrolspartner.v1beta.Customer` is changed ([c03c441](https://github.com/googleapis/google-cloud-python/commit/c03c4411287ee195fd5c99aff94d812381a908f3))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.1.2...google-cloud-cloudcontrolspartner-v0.1.3) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([a6f7356](https://github.com/googleapis/google-cloud-python/commit/a6f7356f1549721f9fab83d4dcfa226cec1965d0))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.1.1...google-cloud-cloudcontrolspartner-v0.1.2) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12865](https://github.com/googleapis/google-cloud-python/issues/12865)) ([7f9dedb](https://github.com/googleapis/google-cloud-python/commit/7f9dedb3abc7636cbcd97e21ac857844b885b599))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-cloudcontrolspartner-v0.1.0...google-cloud-cloudcontrolspartner-v0.1.1) (2024-06-24)


### Documentation

* Mark the accessApprovalRequests.list method as deprecated ([0520183](https://github.com/googleapis/google-cloud-python/commit/052018375c98534aca234c479e28d0bf1bd03857))

## 0.1.0 (2024-03-05)


### Features

* add initial files for google.cloud.cloudcontrolspartner.v1 ([#12402](https://github.com/googleapis/google-cloud-python/issues/12402)) ([7cd0f05](https://github.com/googleapis/google-cloud-python/commit/7cd0f0541ededa589eb76a6d8a965849834734c9))

## Changelog
