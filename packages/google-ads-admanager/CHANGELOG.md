# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-ads-admanager/#history

## [0.8.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.7.0...google-ads-admanager-v0.8.0) (2026-01-08)


### Features

* auto-enable mTLS when supported certificates are detected ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))
* check Python and dependency versions in generated GAPICs ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))

## [0.7.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.6.0...google-ads-admanager-v0.7.0) (2025-12-11)


### Documentation

* Updated documentation for Report metrics and dimensions ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Made `status` optional for SearchAdReviewCenterAds ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Updated documentation for `ad_review_center_ad_id` filter ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))


### Features

* Added write methods for AdUnits ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Added write methods for CustomTargetingKeys ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Added LineItem service ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Added additional Report metrics and dimensions ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))


### Bug Fixes

* Renamed `USER_MESSAGES_CCPA_MESSAGES_SHOWN` `Metric` to `USER_MESSAGES_US_STATES_MESSAGES_SHOWN` ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Added proto3 optional to Network primitive fields ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))
* Added pagination to ListNetworks ([4927067384eb6ed2018bb886f90265b7bcfc800e](https://github.com/googleapis/google-cloud-python/commit/4927067384eb6ed2018bb886f90265b7bcfc800e))

## [0.6.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.5.0...google-ads-admanager-v0.6.0) (2025-10-28)


### Documentation

* Clarified pagination defaults for List methods  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))


### Features

* Added DeviceCapability resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added CmsMetadataValue resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added Application resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added AdReviewCenterAd methods  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added BrowserLanguage resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added CreativeTemplate resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added required field `displayName` to Team  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added additional Report dimensions and metrics  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added required fields `displayName` and `company` to Contact  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added Site resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added DeviceManufacturer resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added Team resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added Browser resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added MobileCarrier resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added MobileDeviceSubmodel resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added AudienceSegment resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added CmsMetadataKey resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added ContentBundle resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added ContentLabel resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added Content resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added methods for reading and writing Contact resources  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Added MobileDevice resource  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))


### Bug Fixes

* Made Label fields proto3 optional  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Made Company fields proto3 optional  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Renamed ReportDefinition.Dimensions PROGRAMMATIC_BUYER_ID and PROGRAMMATIC_BUYER_NAME to DEAL_BUYER_ID and DEAL_BUYER_NAME  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Moved multiple Report messages and submessages  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Made Contact fields proto3 optional  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Made AdUnitSize fields proto3 optional  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))
* Renamed ReportDefinition.Dimension AD_SERVER_UNFILTERED_IMPRESSIONS to AD_SERVER_UNFILTERED_DOWNLOADED_IMPRESSIONS  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))

## [0.5.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.4.0...google-ads-admanager-v0.5.0) (2025-10-16)


### Features

* Add support for Python 3.14  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))


### Bug Fixes

* Deprecate credentials_file argument  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.3.0...google-ads-admanager-v0.4.0) (2025-09-24)


### Bug Fixes

* Moved Company enums to a separate file (#14455)  ([f9fc5fccd48d87af3edb9668e5e962d097457d58](https://github.com/googleapis/google-cloud-python/commit/f9fc5fccd48d87af3edb9668e5e962d097457d58))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.6...google-ads-admanager-v0.3.0) (2025-07-02)


### ⚠ BREAKING CHANGES

* Added proto3 optional modifier to all primitive type fields
* Moved Company enums to a separate file
* Moved Report messages to a separate file
* Changed canonical resource name format for CustomTargetingValue resource
* New required field customTargetingKey added to CustomTargetingValue resource

### Features

* Added support for AdBreak resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for BandwidthGroup resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for DeviceCategory resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for GeoTarget resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for OperatingSystem resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for OperatingSystemVersion resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for PrivateAuction resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Added support for ProgrammaticBuyer ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* New required field customTargetingKey added to CustomTargetingValue resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))


### Bug Fixes

* Added proto3 optional modifier to all primitive type fields ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Changed canonical resource name format for CustomTargetingValue resource ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Moved Company enums to a separate file ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))
* Moved Report messages to a separate file ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))


### Documentation

* Updated documentation for multiple Report enums ([8bd8937](https://github.com/googleapis/google-cloud-python/commit/8bd893714d28ef47ecb76aad6abc06158b0815b4))

## [0.2.6](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.5...google-ads-admanager-v0.2.6) (2025-06-11)


### Documentation

* Update import statement example in README ([1562bb7](https://github.com/googleapis/google-cloud-python/commit/1562bb740c7cd56179e52185dde3c32af861de5e))

## [0.2.5](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.4...google-ads-admanager-v0.2.5) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.3...google-ads-admanager-v0.2.4) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.2...google-ads-admanager-v0.2.3) (2024-12-12)


### Features

* Add support for opt-in debug logging ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.1...google-ads-admanager-v0.2.2) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.2.0...google-ads-admanager-v0.2.1) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.1.2...google-ads-admanager-v0.2.0) (2024-10-08)


### ⚠ BREAKING CHANGES

* Removed closed beta services that had data discrepancies with the SOAP API

### Features

* Added support for Interactive Reporting  ([6db79dc](https://github.com/googleapis/google-cloud-python/commit/6db79dc964b540f1c9c21d96122e4916aca66d98))


### Bug Fixes

* Removed closed beta services that had data discrepancies with the SOAP API ([6db79dc](https://github.com/googleapis/google-cloud-python/commit/6db79dc964b540f1c9c21d96122e4916aca66d98))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.1.1...google-ads-admanager-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-ads-admanager-v0.1.0...google-ads-admanager-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))

## 0.1.0 (2024-03-26)


### Features

* add initial files for google.ads.admanager.v1 ([#12509](https://github.com/googleapis/google-cloud-python/issues/12509)) ([e065361](https://github.com/googleapis/google-cloud-python/commit/e065361a844934ffd35689a1992e962c97a32ecc))

## Changelog
