# Changelog

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.10...google-cloud-gdchardwaremanagement-v0.1.11) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([e06ee32](https://github.com/googleapis/google-cloud-python/commit/e06ee325de4125cdfcaf040a77dc9ccc82843260))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.9...google-cloud-gdchardwaremanagement-v0.1.10) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([908d742](https://github.com/googleapis/google-cloud-python/commit/908d7421a4adadd7407df7ec2a25e25688ff180f))
* Add support for reading selective GAPIC generation methods from service YAML ([908d742](https://github.com/googleapis/google-cloud-python/commit/908d7421a4adadd7407df7ec2a25e25688ff180f))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.8...google-cloud-gdchardwaremanagement-v0.1.9) (2024-12-12)


### Features

* Add support for opt-in debug logging ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.7...google-cloud-gdchardwaremanagement-v0.1.8) (2024-11-14)


### Features

* add DNS address, Kubernetes primary VLAN ID, and provisioning state to the Zone resource ([3c1e8b8](https://github.com/googleapis/google-cloud-python/commit/3c1e8b8173df97e15f247a9fbc892e29643bcb7e))
* add MAC address-associated IP address to the Hardware resource ([3c1e8b8](https://github.com/googleapis/google-cloud-python/commit/3c1e8b8173df97e15f247a9fbc892e29643bcb7e))
* add provisioning_state_signal field in SignalZoneState method request ([3c1e8b8](https://github.com/googleapis/google-cloud-python/commit/3c1e8b8173df97e15f247a9fbc892e29643bcb7e))


### Documentation

* change state_signal field in SignalZoneState method request as optional ([3c1e8b8](https://github.com/googleapis/google-cloud-python/commit/3c1e8b8173df97e15f247a9fbc892e29643bcb7e))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.6...google-cloud-gdchardwaremanagement-v0.1.7) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13243](https://github.com/googleapis/google-cloud-python/issues/13243)) ([d794dec](https://github.com/googleapis/google-cloud-python/commit/d794dec5eff5f23a1ff926012bf9e6cad719e020))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.5...google-cloud-gdchardwaremanagement-v0.1.6) (2024-10-28)


### Features

* add a DeleteSite method ([0846c97](https://github.com/googleapis/google-cloud-python/commit/0846c97aff11d282ea754f87d2f01870247b3ae3))
* add MAC address and disk info to the Hardware resource ([0846c97](https://github.com/googleapis/google-cloud-python/commit/0846c97aff11d282ea754f87d2f01870247b3ae3))


### Documentation

* annotate rack_location field as required; this was always enforced ([0846c97](https://github.com/googleapis/google-cloud-python/commit/0846c97aff11d282ea754f87d2f01870247b3ae3))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.4...google-cloud-gdchardwaremanagement-v0.1.5) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13206](https://github.com/googleapis/google-cloud-python/issues/13206)) ([eb980d5](https://github.com/googleapis/google-cloud-python/commit/eb980d55b2d01d776fa94c3ce408a11f6d366c8a))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.3...google-cloud-gdchardwaremanagement-v0.1.4) (2024-09-23)


### Features

* add an order type field to distinguish a fulfillment request from a sales inquiry ([e727cc0](https://github.com/googleapis/google-cloud-python/commit/e727cc0e98e37d55882215182f86c2a7d23154ef))
* add support to mark comments as read or unread ([e727cc0](https://github.com/googleapis/google-cloud-python/commit/e727cc0e98e37d55882215182f86c2a7d23154ef))
* rename zone state signal READY_FOR_SITE_TURNUP to FACTORY_TURNUP_CHECKS_PASSED ([e727cc0](https://github.com/googleapis/google-cloud-python/commit/e727cc0e98e37d55882215182f86c2a7d23154ef))


### Documentation

* clarify how access_times are used ([e727cc0](https://github.com/googleapis/google-cloud-python/commit/e727cc0e98e37d55882215182f86c2a7d23154ef))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.2...google-cloud-gdchardwaremanagement-v0.1.3) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([189922a](https://github.com/googleapis/google-cloud-python/commit/189922a0fbe969dedc7b0f78a62ccb2e5d3f29a9))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.1...google-cloud-gdchardwaremanagement-v0.1.2) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12866](https://github.com/googleapis/google-cloud-python/issues/12866)) ([40e1810](https://github.com/googleapis/google-cloud-python/commit/40e18101eaaeefe4baa090c3b4f7a96209ea5735))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-gdchardwaremanagement-v0.1.0...google-cloud-gdchardwaremanagement-v0.1.1) (2024-06-27)


### Features

* add additional zone states ([a4bfef9](https://github.com/googleapis/google-cloud-python/commit/a4bfef92d5b6f30e40ef257b33748ce4b708e2ff))

## 0.1.0 (2024-06-26)


### Features

* add initial files for google.cloud.gdchardwaremanagement.v1alpha ([#12824](https://github.com/googleapis/google-cloud-python/issues/12824)) ([6c02375](https://github.com/googleapis/google-cloud-python/commit/6c02375e05dba7005ec9137ed7c5959127a9be46))

## Changelog
