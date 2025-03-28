# Changelog

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.8...google-cloud-managedkafka-v0.1.9) (2025-03-19)


### Features

* [google-cloud-managedkafka] add Managed Kafka Connect API ([887357d](https://github.com/googleapis/google-cloud-python/commit/887357da2ede1d41f14258fc44275f5f592f2478))
* Add Managed Kafka Connect API ([#13677](https://github.com/googleapis/google-cloud-python/issues/13677)) ([887357d](https://github.com/googleapis/google-cloud-python/commit/887357da2ede1d41f14258fc44275f5f592f2478))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.7...google-cloud-managedkafka-v0.1.8) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([c8bbf32](https://github.com/googleapis/google-cloud-python/commit/c8bbf32606e790b559b261bf96700c76b6e2bfce))
* An existing google.api.http annotation `http_uri` is changed for method `DeleteConsumerGroup` in service `ManagedKafka` ([6a10ce5](https://github.com/googleapis/google-cloud-python/commit/6a10ce547d22f48b7e95dc7dd0bad06f62aae67d))
* An existing google.api.http annotation `http_uri` is changed for method `UpdateConsumerGroup` in service `ManagedKafka` ([6a10ce5](https://github.com/googleapis/google-cloud-python/commit/6a10ce547d22f48b7e95dc7dd0bad06f62aae67d))
* An existing google.api.http annotation http_uri is changed for method `GetConsumerGroup` in service `ManagedKafka` ([6a10ce5](https://github.com/googleapis/google-cloud-python/commit/6a10ce547d22f48b7e95dc7dd0bad06f62aae67d))


### Documentation

* A comment for field `subnet` in message `.google.cloud.managedkafka.v1.NetworkConfig` is changed ([6a10ce5](https://github.com/googleapis/google-cloud-python/commit/6a10ce547d22f48b7e95dc7dd0bad06f62aae67d))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.6...google-cloud-managedkafka-v0.1.7) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))
* Add support for reading selective GAPIC generation methods from service YAML ([a0910dd](https://github.com/googleapis/google-cloud-python/commit/a0910dd51541d238bc5fcf10159066ddfd928579))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.5...google-cloud-managedkafka-v0.1.6) (2024-12-12)


### Features

* A new field `satisfies_pzi` is added to message `.google.cloud.managedkafka.v1.Cluster` ([a9d60f4](https://github.com/googleapis/google-cloud-python/commit/a9d60f40dff04f6240dbc8ed46a284830de77ad3))
* A new field `satisfies_pzs` is added to message `.google.cloud.managedkafka.v1.Cluster` ([a9d60f4](https://github.com/googleapis/google-cloud-python/commit/a9d60f40dff04f6240dbc8ed46a284830de77ad3))
* Add support for opt-in debug logging ([a9d60f4](https://github.com/googleapis/google-cloud-python/commit/a9d60f40dff04f6240dbc8ed46a284830de77ad3))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([a9d60f4](https://github.com/googleapis/google-cloud-python/commit/a9d60f40dff04f6240dbc8ed46a284830de77ad3))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.4...google-cloud-managedkafka-v0.1.5) (2024-11-11)


### Bug Fixes

* disable universe-domain validation ([#13243](https://github.com/googleapis/google-cloud-python/issues/13243)) ([d794dec](https://github.com/googleapis/google-cloud-python/commit/d794dec5eff5f23a1ff926012bf9e6cad719e020))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.3...google-cloud-managedkafka-v0.1.4) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13207](https://github.com/googleapis/google-cloud-python/issues/13207)) ([ceb9be8](https://github.com/googleapis/google-cloud-python/commit/ceb9be8f89ac7355d842bac1d77b2926eb0b649c))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.2...google-cloud-managedkafka-v0.1.3) (2024-08-19)


### Documentation

* [google-cloud-managedkafka] changed API title to official name ([#13010](https://github.com/googleapis/google-cloud-python/issues/13010)) ([5e6b4ce](https://github.com/googleapis/google-cloud-python/commit/5e6b4ce92614cc9a169c530f9a23d3934f4868cc))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.1...google-cloud-managedkafka-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([d95af77](https://github.com/googleapis/google-cloud-python/commit/d95af77248f0935a5fe3dba1fccc75124c8b1451))


### Documentation

* [google-cloud-managedkafka] update values allowed in kms_key ([c28cdc3](https://github.com/googleapis/google-cloud-python/commit/c28cdc330ce43c35cb87f0c881ed78a60ad657bc))
* [google-cloud-managedkafka] update values allowed in kms_key ([#12922](https://github.com/googleapis/google-cloud-python/issues/12922)) ([c28cdc3](https://github.com/googleapis/google-cloud-python/commit/c28cdc330ce43c35cb87f0c881ed78a60ad657bc))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-managedkafka-v0.1.0...google-cloud-managedkafka-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12867](https://github.com/googleapis/google-cloud-python/issues/12867)) ([3362176](https://github.com/googleapis/google-cloud-python/commit/33621762b989106ccf85adb538cf531c513a746c))

## 0.1.0 (2024-06-10)


### Features

* add initial files for google.cloud.managedkafka.v1 ([#12781](https://github.com/googleapis/google-cloud-python/issues/12781)) ([e05d380](https://github.com/googleapis/google-cloud-python/commit/e05d380453ee3555ecbde870a82c27023910e066))

## Changelog
