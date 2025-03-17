# Changelog

## [0.1.25](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.24...google-maps-places-v0.1.25) (2025-03-15)


### Features

* Add postal_address and time_zone to Place ([bde4694](https://github.com/googleapis/google-cloud-python/commit/bde469472b1a74a39c8d8607c3c834e988bb0a7e))


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([25ced24](https://github.com/googleapis/google-cloud-python/commit/25ced2444528a1dc6a22daa32b82b844961f1b75))


### Documentation

* [google-maps-places] Change comments in some fields in Places API ([#13635](https://github.com/googleapis/google-cloud-python/issues/13635)) ([bde4694](https://github.com/googleapis/google-cloud-python/commit/bde469472b1a74a39c8d8607c3c834e988bb0a7e))

## [0.1.24](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.23...google-maps-places-v0.1.24) (2025-02-27)


### Features

* [google-maps-places] add NACS EVCS connector type support ([#13555](https://github.com/googleapis/google-cloud-python/issues/13555)) ([fdff960](https://github.com/googleapis/google-cloud-python/commit/fdff960cd7bf521e2c19e2e7ad1d17bf01fefefb))

## [0.1.23](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.22...google-maps-places-v0.1.23) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([24b5afe](https://github.com/googleapis/google-cloud-python/commit/24b5afe41f5b62be671301e19a1ddc6ee97a24f2))
* Add support for reading selective GAPIC generation methods from service YAML ([24b5afe](https://github.com/googleapis/google-cloud-python/commit/24b5afe41f5b62be671301e19a1ddc6ee97a24f2))


### Bug Fixes

* add oauth scopes to Places proto ([24b5afe](https://github.com/googleapis/google-cloud-python/commit/24b5afe41f5b62be671301e19a1ddc6ee97a24f2))

## [0.1.22](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.21...google-maps-places-v0.1.22) (2025-01-27)


### Features

* add more fuel type enum values ([254b142](https://github.com/googleapis/google-cloud-python/commit/254b14252f7f22f0d47aa4038fc77252ca138ba6))


### Documentation

* A comment for enum value `LPG` in enum `FuelType` is changed to be clearer. ([254b142](https://github.com/googleapis/google-cloud-python/commit/254b14252f7f22f0d47aa4038fc77252ca138ba6))

## [0.1.21](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.20...google-maps-places-v0.1.21) (2024-12-12)


### Features

* [Many APIs] Add support for opt-in debug logging ([#13349](https://github.com/googleapis/google-cloud-python/issues/13349)) ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8b9c7bf](https://github.com/googleapis/google-cloud-python/commit/8b9c7bf3bb1c4f0beabd71a45c469fcedb19a2c8))

## [0.1.20](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.19...google-maps-places-v0.1.20) (2024-11-11)


### Features

* [google-maps-places] update attributes in Places API ([#13259](https://github.com/googleapis/google-cloud-python/issues/13259)) ([450fa0b](https://github.com/googleapis/google-cloud-python/commit/450fa0bbfc511c8532928925a24ae36c8ef4cd75))


### Bug Fixes

* disable universe-domain validation  ([#13247](https://github.com/googleapis/google-cloud-python/issues/13247)) ([5adc8b7](https://github.com/googleapis/google-cloud-python/commit/5adc8b7d2cc8ab9707ab5a65f15270c125cee051))

## [0.1.19](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.18...google-maps-places-v0.1.19) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13211](https://github.com/googleapis/google-cloud-python/issues/13211)) ([f712162](https://github.com/googleapis/google-cloud-python/commit/f712162c01f065da29fffbbed1e856a1f3876b1b))

## [0.1.18](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.17...google-maps-places-v0.1.18) (2024-09-23)


### Features

* action for publishing data profiles to SecOps (formelly known as Chronicle) ([2cc1550](https://github.com/googleapis/google-cloud-python/commit/2cc1550492a2b78ed7240aab84a8449de5e5afa2))
* action for publishing data profiles to Security Command Center ([2cc1550](https://github.com/googleapis/google-cloud-python/commit/2cc1550492a2b78ed7240aab84a8449de5e5afa2))
* discovery configs for AWS S3 buckets ([2cc1550](https://github.com/googleapis/google-cloud-python/commit/2cc1550492a2b78ed7240aab84a8449de5e5afa2))


### Documentation

* small improvements and clarifications ([2cc1550](https://github.com/googleapis/google-cloud-python/commit/2cc1550492a2b78ed7240aab84a8449de5e5afa2))

## [0.1.17](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.16...google-maps-places-v0.1.17) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([4adddf4](https://github.com/googleapis/google-cloud-python/commit/4adddf4d90634e454ee006774bfc631fc12c1700))

## [0.1.16](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.15...google-maps-places-v0.1.16) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12871](https://github.com/googleapis/google-cloud-python/issues/12871)) ([73b35d5](https://github.com/googleapis/google-cloud-python/commit/73b35d56f8626d99ce7c3902a8c223cc09b4ca74))

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.14...google-maps-places-v0.1.15) (2024-05-27)


### Features

* add `generative_summary` and `area_summary` for place summaries ([46d0d9f](https://github.com/googleapis/google-cloud-python/commit/46d0d9f863049c257b8bfa15cfce0ea0f3530c5a))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.13...google-maps-places-v0.1.14) (2024-05-07)


### Documentation

* update comment of Places API ([272fb7d](https://github.com/googleapis/google-cloud-python/commit/272fb7d877a98c989c577bb7757bc25dc182340e))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.12...google-maps-places-v0.1.13) (2024-04-22)


### Documentation

* [google-maps-places] slightly improved documentation for EVOptions in SearchTextRequest ([#12599](https://github.com/googleapis/google-cloud-python/issues/12599)) ([3ef0fe0](https://github.com/googleapis/google-cloud-python/commit/3ef0fe07dc2c1b719a8a1ae6302f35bc910e6097))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.11...google-maps-places-v0.1.12) (2024-04-15)


### Documentation

* Fix designation of Text Search ([8b87391](https://github.com/googleapis/google-cloud-python/commit/8b87391ebcd2a5daac50195fcc31a10a007a1c5c))
* Update field mask guidance ([8b87391](https://github.com/googleapis/google-cloud-python/commit/8b87391ebcd2a5daac50195fcc31a10a007a1c5c))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.10...google-maps-places-v0.1.11) (2024-04-03)


### Documentation

* Correct requirements on Autocomplete and Details session token field ([b7a50a2](https://github.com/googleapis/google-cloud-python/commit/b7a50a218314784a619986c910a50618b551fe14))
* Document the maximum number of reviews and photos returned ([b7a50a2](https://github.com/googleapis/google-cloud-python/commit/b7a50a218314784a619986c910a50618b551fe14))
* Fix typo in PriceLevel enum ([b7a50a2](https://github.com/googleapis/google-cloud-python/commit/b7a50a218314784a619986c910a50618b551fe14))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.9...google-maps-places-v0.1.10) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12389](https://github.com/googleapis/google-cloud-python/issues/12389)) ([5db9352](https://github.com/googleapis/google-cloud-python/commit/5db93528a1ad20825d4d12dcf5fdf9624879f2ce))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.8...google-maps-places-v0.1.9) (2024-02-22)


### Features

* add AutoComplete API ([86743c8](https://github.com/googleapis/google-cloud-python/commit/86743c8a2c8e326e7f2b21d550faec822de9dd4e))
* add Searchable EV feature to TextSearch API ([86743c8](https://github.com/googleapis/google-cloud-python/commit/86743c8a2c8e326e7f2b21d550faec822de9dd4e))


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12311](https://github.com/googleapis/google-cloud-python/issues/12311)) ([e4c864b](https://github.com/googleapis/google-cloud-python/commit/e4c864b3e67c7f7f33dfb0d2107fa138492ad338))
* fix ValueError in test__validate_universe_domain ([f3974d4](https://github.com/googleapis/google-cloud-python/commit/f3974d46a9ba9f549e31251ebc2daeb6b9b4745a))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.7...google-maps-places-v0.1.8) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Add staticmethod decorator to `_get_client_cert_source` and `_get_api_endpoint` ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([d7d730a](https://github.com/googleapis/google-cloud-python/commit/d7d730acd3b1da86b996fa18c81272f1c9a00406))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.6...google-maps-places-v0.1.7) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12244](https://github.com/googleapis/google-cloud-python/issues/12244)) ([8d6b772](https://github.com/googleapis/google-cloud-python/commit/8d6b7729d93c1347529a3d34ed6266af55225578))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.5...google-maps-places-v0.1.6) (2023-12-07)


### Features

* Add new primary type fields ([a74938f](https://github.com/googleapis/google-cloud-python/commit/a74938fa2ed19348d703d23ffb13545423e8b736))
* Add new short formatted address field ([a74938f](https://github.com/googleapis/google-cloud-python/commit/a74938fa2ed19348d703d23ffb13545423e8b736))
* Add new wheelchair accessibility fields ([a74938f](https://github.com/googleapis/google-cloud-python/commit/a74938fa2ed19348d703d23ffb13545423e8b736))


### Documentation

* Change comments for some fields in Places API ([a74938f](https://github.com/googleapis/google-cloud-python/commit/a74938fa2ed19348d703d23ffb13545423e8b736))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.4...google-maps-places-v0.1.5) (2023-12-07)


### Features

* Add support for python 3.12 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Introduce compatibility with native namespace packages ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))
* Use `retry_async` instead of `retry` in async client ([31d043d](https://github.com/googleapis/google-cloud-python/commit/31d043de5a0b8bd329e8d5a36e7811d5ea7bd7a1))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.3...google-maps-places-v0.1.4) (2023-11-02)


### Features

* new features for Places GA ([#11909](https://github.com/googleapis/google-cloud-python/issues/11909)) ([9cd4ccb](https://github.com/googleapis/google-cloud-python/commit/9cd4ccbaebb43f27d406463e139c1a8bcfdf0577))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.2...google-maps-places-v0.1.3) (2023-09-19)


### Documentation

* Minor formatting ([77bf61a](https://github.com/googleapis/google-cloud-python/commit/77bf61a36539bc2e6317dca1f954189d5241e4f1))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.1...google-maps-places-v0.1.2) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11449](https://github.com/googleapis/google-cloud-python/issues/11449)) ([3885820](https://github.com/googleapis/google-cloud-python/commit/388582082828e22a517c4f794901ee5dcbc31bd9))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-maps-places-v0.1.0...google-maps-places-v0.1.1) (2023-06-03)


### Documentation

* fix broken client library documentation links ([#11192](https://github.com/googleapis/google-cloud-python/issues/11192)) ([5e17f7a](https://github.com/googleapis/google-cloud-python/commit/5e17f7a901bbbae8ff9a44ed62f1abd2386da2c8))

## 0.1.0 (2023-05-09)


### Features

* add initial files for google.maps.places.v1 ([#11154](https://github.com/googleapis/google-cloud-python/issues/11154)) ([81503bd](https://github.com/googleapis/google-cloud-python/commit/81503bda94fee7fe5c2fe27a13a478efb0591636))

## Changelog
