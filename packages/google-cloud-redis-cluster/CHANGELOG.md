# Changelog

## [0.1.15](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.14...google-cloud-redis-cluster-v0.1.15) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([7295cbb](https://github.com/googleapis/google-cloud-python/commit/7295cbb7c3122eeff1042c3c543bfc9b8b3ca913))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.13...google-cloud-redis-cluster-v0.1.14) (2025-02-18)


### Features

* Add REST Interceptors which support reading metadata ([c8e0760](https://github.com/googleapis/google-cloud-python/commit/c8e0760e8088950c62279335216ad1d17716ce59))
* Add support for reading selective GAPIC generation methods from service YAML ([c8e0760](https://github.com/googleapis/google-cloud-python/commit/c8e0760e8088950c62279335216ad1d17716ce59))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.12...google-cloud-redis-cluster-v0.1.13) (2025-01-20)


### Features

* [Memorystore for Redis Cluster] Added support for Backups and Backup Collections ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* [Memorystore for Redis Cluster] Added support for CMEK ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* [Memorystore for Redis Cluster] Added support for Cross Cluster Replication ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* [Memorystore for Redis Cluster] Added support for maintenance window and rescheduling maintenance ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* [Memorystore for Redis Cluster] Added support for Multiple VPCs ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* New REQUIRED field `service_attachment` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))


### Bug Fixes

* Changed field behavior for an existing field `address` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* Changed field behavior for an existing field `forwarding_rule` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* Changed field behavior for an existing field `network` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* Changed field behavior for an existing field `psc_connection_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))


### Documentation

* A comment for enum value `ALWAYS` in enum `AppendFsync` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for enum value `NODE_TYPE_UNSPECIFIED` in enum `NodeType` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `address` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `forwarding_rule` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `name` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `network` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `project_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `psc_configs` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `psc_connection_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `psc_connections` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))
* A comment for field `shard_count` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([2d3d9c9](https://github.com/googleapis/google-cloud-python/commit/2d3d9c9fe375a1280c6ac9e4eb253eefe7d73d75))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.11...google-cloud-redis-cluster-v0.1.12) (2025-01-14)


### Features

* [Memorystore for Redis Cluster] Added support for Backups and Backup Collections ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* [Memorystore for Redis Cluster] Added support for CMEK ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* [Memorystore for Redis Cluster] Added support for Cross Cluster Replication ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* [Memorystore for Redis Cluster] Added support for maintenance window and rescheduling maintenance ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* [Memorystore for Redis Cluster] Added support for Multiple VPCs ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* New REQUIRED field `service_attachment` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))


### Bug Fixes

* Changed field behavior for an existing field `address` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* Changed field behavior for an existing field `forwarding_rule` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* Changed field behavior for an existing field `network` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* Changed field behavior for an existing field `psc_connection_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))


### Documentation

* A comment for enum value `ALWAYS` in enum `AppendFsync` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for enum value `NODE_TYPE_UNSPECIFIED` in enum `NodeType` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `address` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `forwarding_rule` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `name` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `network` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `project_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `psc_configs` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `psc_connection_id` in message `.google.cloud.redis.cluster.v1beta1.PscConnection` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `psc_connections` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))
* A comment for field `shard_count` in message `.google.cloud.redis.cluster.v1beta1.Cluster` is changed ([f551999](https://github.com/googleapis/google-cloud-python/commit/f5519995e4e4d4c6acc42f31b501854a1c76be27))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.10...google-cloud-redis-cluster-v0.1.11) (2024-12-12)


### Features

* Add support for opt-in debug logging ([8e6b0cc](https://github.com/googleapis/google-cloud-python/commit/8e6b0cca8709ae8c7f0c722c5ebf0707358d3359))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([8e6b0cc](https://github.com/googleapis/google-cloud-python/commit/8e6b0cca8709ae8c7f0c722c5ebf0707358d3359))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.9...google-cloud-redis-cluster-v0.1.10) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13245](https://github.com/googleapis/google-cloud-python/issues/13245)) ([875f712](https://github.com/googleapis/google-cloud-python/commit/875f712265a36919409964f5ade218330f1d0147))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.8...google-cloud-redis-cluster-v0.1.9) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13209](https://github.com/googleapis/google-cloud-python/issues/13209)) ([5f2e30d](https://github.com/googleapis/google-cloud-python/commit/5f2e30d62eea6080f5707ee18755f2bb812ad00b))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.7...google-cloud-redis-cluster-v0.1.8) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([42c4d04](https://github.com/googleapis/google-cloud-python/commit/42c4d04ee1362ba0ed0f1b6a134ac8e409875b63))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.6...google-cloud-redis-cluster-v0.1.7) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12869](https://github.com/googleapis/google-cloud-python/issues/12869)) ([e42edbc](https://github.com/googleapis/google-cloud-python/commit/e42edbcf7f4d8ed66b6645c96a01c55fb8cd7666))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.5...google-cloud-redis-cluster-v0.1.6) (2024-06-05)


### Features

* [Memorystore for Redis Cluster] Add persistence support ([6a70a4b](https://github.com/googleapis/google-cloud-python/commit/6a70a4b7c968ba28af488f6ab5ac78c66a8c2b98))
* [Memorystore for Redis Cluster] Add support for different node types ([6a70a4b](https://github.com/googleapis/google-cloud-python/commit/6a70a4b7c968ba28af488f6ab5ac78c66a8c2b98))
* [Memorystore for Redis Cluster] Get details of certificate authority from redis cluster ([6a70a4b](https://github.com/googleapis/google-cloud-python/commit/6a70a4b7c968ba28af488f6ab5ac78c66a8c2b98))


### Documentation

* [Memorystore for Redis Cluster] size_gb field shows the size of the cluster rounded up to the next integer, precise_size_gb field will show the exact size of the cluster ([6a70a4b](https://github.com/googleapis/google-cloud-python/commit/6a70a4b7c968ba28af488f6ab5ac78c66a8c2b98))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.4...google-cloud-redis-cluster-v0.1.5) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12386](https://github.com/googleapis/google-cloud-python/issues/12386)) ([edcad16](https://github.com/googleapis/google-cloud-python/commit/edcad1661973ae1677c69b3fc1c03c3069ec0e71))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.3...google-cloud-redis-cluster-v0.1.4) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12309](https://github.com/googleapis/google-cloud-python/issues/12309)) ([c23398a](https://github.com/googleapis/google-cloud-python/commit/c23398a48d23d48e7f96971dd504ff184841666b))
* fix ValueError in test__validate_universe_domain ([89c1b05](https://github.com/googleapis/google-cloud-python/commit/89c1b054f321b90ab4eed0139a3a2a79c369730d))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.2...google-cloud-redis-cluster-v0.1.3) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([e75fcf6](https://github.com/googleapis/google-cloud-python/commit/e75fcf6e389fd2e90ec00b87a625b208837c72dc))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([e75fcf6](https://github.com/googleapis/google-cloud-python/commit/e75fcf6e389fd2e90ec00b87a625b208837c72dc))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([e75fcf6](https://github.com/googleapis/google-cloud-python/commit/e75fcf6e389fd2e90ec00b87a625b208837c72dc))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.1...google-cloud-redis-cluster-v0.1.2) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([4368029](https://github.com/googleapis/google-cloud-python/commit/436802904bfdafa7e90f94b128813506525e1605))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-redis-cluster-v0.1.0...google-cloud-redis-cluster-v0.1.1) (2023-12-07)


### Features

* Add support for python 3.12 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Introduce compatibility with native namespace packages ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))
* Use `retry_async` instead of `retry` in async client ([9a629e1](https://github.com/googleapis/google-cloud-python/commit/9a629e1c9f7858f55c82ac21e60f22acf781db15))

## 0.1.0 (2023-11-07)


### Features

* add initial files for google.cloud.redis.cluster.v1 ([#11984](https://github.com/googleapis/google-cloud-python/issues/11984)) ([432e1fd](https://github.com/googleapis/google-cloud-python/commit/432e1fd3f7be7eb84c2f846a9fa81cef3463b5c8))

## Changelog
