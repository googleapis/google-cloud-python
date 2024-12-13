# Changelog

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.10...google-apps-meet-v0.1.11) (2024-12-12)


### Features

* Add support for opt-in debug logging ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([b1dfc55](https://github.com/googleapis/google-cloud-python/commit/b1dfc556d4652a48564ff37becb31d5a06ee2b5b))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.9...google-apps-meet-v0.1.10) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.8...google-apps-meet-v0.1.9) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.7...google-apps-meet-v0.1.8) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.6...google-apps-meet-v0.1.7) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.5...google-apps-meet-v0.1.6) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12381](https://github.com/googleapis/google-cloud-python/issues/12381)) ([48ae8ab](https://github.com/googleapis/google-cloud-python/commit/48ae8aba7ec71a382e001b3a659022f942c3b436))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.4...google-apps-meet-v0.1.5) (2024-02-22)


### Features

* Add outh_scope values to services ([7c4dc23](https://github.com/googleapis/google-cloud-python/commit/7c4dc2318ae2c946967cb6f36490f4b3fff63d4e))


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12280](https://github.com/googleapis/google-cloud-python/issues/12280)) ([2d75d0e](https://github.com/googleapis/google-cloud-python/commit/2d75d0e67ca4cccddc688bd37c14ac80564a2e65))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12303](https://github.com/googleapis/google-cloud-python/issues/12303)) ([fbb80c3](https://github.com/googleapis/google-cloud-python/commit/fbb80c32f7db91e25bd1cc30966f630728ff6d6a))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.3...google-apps-meet-v0.1.4) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([780c5f1](https://github.com/googleapis/google-cloud-python/commit/780c5f15d4099da6b5c3b966267bc7d7c63d6303))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.2...google-apps-meet-v0.1.3) (2024-02-01)


### Features

* Added v2 libraries for the Meet API GA release ([b7cf5a9](https://github.com/googleapis/google-cloud-python/commit/b7cf5a9a22b0798be485d5b58288f24a50aff6b6))
* Set google.apps.meet_v2 as the default import ([b7cf5a9](https://github.com/googleapis/google-cloud-python/commit/b7cf5a9a22b0798be485d5b58288f24a50aff6b6))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.1...google-apps-meet-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([a0392ee](https://github.com/googleapis/google-cloud-python/commit/a0392eeb59fcc6ea7c55283110b92aa24a4d40a0))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-meet-v0.1.0...google-apps-meet-v0.1.1) (2024-01-04)


### Features

* [google-apps-meet] added start and end time fields to Recording and Transcript resources ([#12130](https://github.com/googleapis/google-cloud-python/issues/12130)) ([6679d16](https://github.com/googleapis/google-cloud-python/commit/6679d16e0fa93219c62ccbec2641dc68fbd7265b))

## 0.1.0 (2023-12-07)


### Features

* add initial files for google.apps.meet.v2beta ([#12100](https://github.com/googleapis/google-cloud-python/issues/12100)) ([d99f5b0](https://github.com/googleapis/google-cloud-python/commit/d99f5b0ec5dcaa254bfa30dbf0495063a7a82374))

## Changelog
