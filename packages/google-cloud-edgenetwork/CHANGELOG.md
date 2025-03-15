# Changelog

## [0.1.16](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.15...google-cloud-edgenetwork-v0.1.16) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([e06ee32](https://github.com/googleapis/google-cloud-python/commit/e06ee325de4125cdfcaf040a77dc9ccc82843260))

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.14...google-cloud-edgenetwork-v0.1.15) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e92d527](https://github.com/googleapis/google-cloud-python/commit/e92d52797ffbce45d033eb81af24e0cad32baa55))
* Add support for reading selective GAPIC generation methods from service YAML ([e92d527](https://github.com/googleapis/google-cloud-python/commit/e92d52797ffbce45d033eb81af24e0cad32baa55))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.13...google-cloud-edgenetwork-v0.1.14) (2024-12-12)


### Features

* Add support for opt-in debug logging ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.12...google-cloud-edgenetwork-v0.1.13) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13242](https://github.com/googleapis/google-cloud-python/issues/13242)) ([b479ff8](https://github.com/googleapis/google-cloud-python/commit/b479ff841ed93a18393a188ee1d72edf9fb729ec))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.11...google-cloud-edgenetwork-v0.1.12) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13206](https://github.com/googleapis/google-cloud-python/issues/13206)) ([eb980d5](https://github.com/googleapis/google-cloud-python/commit/eb980d55b2d01d776fa94c3ce408a11f6d366c8a))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.10...google-cloud-edgenetwork-v0.1.11) (2024-09-03)


### Documentation

* swap comments on `BONDED` and `NON_BONDED` enums in `BondingType` ([308de6b](https://github.com/googleapis/google-cloud-python/commit/308de6b266e24a8996875736b66485d92f299401))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.9...google-cloud-edgenetwork-v0.1.10) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([ba1064f](https://github.com/googleapis/google-cloud-python/commit/ba1064fd6a63ccbe8a390c0026f32c5772c728a5))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.8...google-cloud-edgenetwork-v0.1.9) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12866](https://github.com/googleapis/google-cloud-python/issues/12866)) ([40e1810](https://github.com/googleapis/google-cloud-python/commit/40e18101eaaeefe4baa090c3b4f7a96209ea5735))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.7...google-cloud-edgenetwork-v0.1.8) (2024-06-27)


### Features

* [google-cloud-edgenetwork] A new field `bonding_type` is added to message `.google.cloud.edgenetwork.v1.Subnet` ([#12842](https://github.com/googleapis/google-cloud-python/issues/12842)) ([5f272b3](https://github.com/googleapis/google-cloud-python/commit/5f272b3293fe54dd7d73930cdd2e634b15ed3e2f))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.6...google-cloud-edgenetwork-v0.1.7) (2024-03-22)


### Bug Fixes

* [google-cloud-edgenetwork] deprecate unimplemented Zone fields and methods ([#12473](https://github.com/googleapis/google-cloud-python/issues/12473)) ([6f26fe8](https://github.com/googleapis/google-cloud-python/commit/6f26fe81c667c6bedfd405caeed90f72feb7ce9d))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.5...google-cloud-edgenetwork-v0.1.6) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12384](https://github.com/googleapis/google-cloud-python/issues/12384)) ([c69966f](https://github.com/googleapis/google-cloud-python/commit/c69966fa7aac2cba4e22513e4a053b3754f8ea5e))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.4...google-cloud-edgenetwork-v0.1.5) (2024-02-22)


### Bug Fixes

* [Many APIs] fix `ValueError` in `test__validate_universe_domain` ([#12283](https://github.com/googleapis/google-cloud-python/issues/12283)) ([f20b41a](https://github.com/googleapis/google-cloud-python/commit/f20b41ac35b02a40135b83edfe819ff7a355ab21))
* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12306](https://github.com/googleapis/google-cloud-python/issues/12306)) ([1e787f2](https://github.com/googleapis/google-cloud-python/commit/1e787f2079ac41ce634c7b90f02a6597cecb64be))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.3...google-cloud-edgenetwork-v0.1.4) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([c721248](https://github.com/googleapis/google-cloud-python/commit/c721248accc77f0b1fba9605a65ea95a86f023a5))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([c721248](https://github.com/googleapis/google-cloud-python/commit/c721248accc77f0b1fba9605a65ea95a86f023a5))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([c721248](https://github.com/googleapis/google-cloud-python/commit/c721248accc77f0b1fba9605a65ea95a86f023a5))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.2...google-cloud-edgenetwork-v0.1.3) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12240](https://github.com/googleapis/google-cloud-python/issues/12240)) ([d51f832](https://github.com/googleapis/google-cloud-python/commit/d51f83298f89dbae23af1a146411b296eba6bba2))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.1...google-cloud-edgenetwork-v0.1.2) (2024-01-24)


### Features

* [google-cloud-edgenetwork] add MACsec status for internal links ([#12213](https://github.com/googleapis/google-cloud-python/issues/12213)) ([313f567](https://github.com/googleapis/google-cloud-python/commit/313f5672c1d16681dd4db2c4a995c5668259ea7d))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-edgenetwork-v0.1.0...google-cloud-edgenetwork-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([fb6f9db](https://github.com/googleapis/google-cloud-python/commit/fb6f9dbfadfe1a8ca3b236e0cae5c85cf2862f3e))
* Introduce compatibility with native namespace packages ([fb6f9db](https://github.com/googleapis/google-cloud-python/commit/fb6f9dbfadfe1a8ca3b236e0cae5c85cf2862f3e))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([fb6f9db](https://github.com/googleapis/google-cloud-python/commit/fb6f9dbfadfe1a8ca3b236e0cae5c85cf2862f3e))
* Use `retry_async` instead of `retry` in async client ([fb6f9db](https://github.com/googleapis/google-cloud-python/commit/fb6f9dbfadfe1a8ca3b236e0cae5c85cf2862f3e))

## 0.1.0 (2023-11-07)


### Features

* Add initial files for `google.cloud.edgenetwork.v1` ([2de8e4a](https://github.com/googleapis/google-cloud-python/commit/2de8e4a22f60aef4f02c51e1543d4100926295d3))

## Changelog
