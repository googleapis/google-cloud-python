# Changelog

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
