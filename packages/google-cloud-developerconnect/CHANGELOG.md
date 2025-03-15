# Changelog

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.7...google-cloud-developerconnect-v0.1.8) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([feb5353](https://github.com/googleapis/google-cloud-python/commit/feb53532240bb70a94b359b519f0f41f95875a33))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.6...google-cloud-developerconnect-v0.1.7) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([e92d527](https://github.com/googleapis/google-cloud-python/commit/e92d52797ffbce45d033eb81af24e0cad32baa55))
* Add support for reading selective GAPIC generation methods from service YAML ([e92d527](https://github.com/googleapis/google-cloud-python/commit/e92d52797ffbce45d033eb81af24e0cad32baa55))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.5...google-cloud-developerconnect-v0.1.6) (2024-12-12)


### Features

* Add support for opt-in debug logging ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([819e8fb](https://github.com/googleapis/google-cloud-python/commit/819e8fb3159c39f6c8eb6d7c0b75927134d6ceb2))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.4...google-cloud-developerconnect-v0.1.5) (2024-11-21)


### Features

* A new field `crypto_key_config` is added to message `.google.cloud.developerconnect.v1.Connection` ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new field `github_enterprise_config` is added to message `.google.cloud.developerconnect.v1.Connection` ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new field `gitlab_config` is added to message `.google.cloud.developerconnect.v1.Connection` ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new field `gitlab_enterprise_config` is added to message `.google.cloud.developerconnect.v1.Connection` ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new field `webhook_id` is added to message `.google.cloud.developerconnect.v1.GitRepositoryLink` ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `CryptoKeyConfig` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `GitHubEnterpriseConfig` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `GitLabConfig` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `GitLabEnterpriseConfig` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `ServiceDirectoryConfig` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new message `UserCredential` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new resource_definition `[cloudkms.googleapis.com/CryptoKey](https://www.google.com/url?sa=D&q=http%3A%2F%2Fcloudkms.googleapis.com%2FCryptoKey)` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))
* A new resource_definition `[servicedirectory.googleapis.com/Service](https://www.google.com/url?sa=D&q=http%3A%2F%2Fservicedirectory.googleapis.com%2FService)` is added ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))


### Documentation

* A comment for field `requested_cancellation` in message `.google.cloud.developerconnect.v1.OperationMetadata` is changed ([48f25db](https://github.com/googleapis/google-cloud-python/commit/48f25db7772c9d22edac1e743b4eec97929542ec))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.3...google-cloud-developerconnect-v0.1.4) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([53c951e](https://github.com/googleapis/google-cloud-python/commit/53c951e90ad1d702fa507495532086d5d2f6b3c0))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.2...google-cloud-developerconnect-v0.1.3) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13202](https://github.com/googleapis/google-cloud-python/issues/13202)) ([5b1f2f3](https://github.com/googleapis/google-cloud-python/commit/5b1f2f3a81ed171b643812e67a7ed179b9b703ea))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.1...google-cloud-developerconnect-v0.1.2) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([ba1064f](https://github.com/googleapis/google-cloud-python/commit/ba1064fd6a63ccbe8a390c0026f32c5772c728a5))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-developerconnect-v0.1.0...google-cloud-developerconnect-v0.1.1) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12866](https://github.com/googleapis/google-cloud-python/issues/12866)) ([40e1810](https://github.com/googleapis/google-cloud-python/commit/40e18101eaaeefe4baa090c3b4f7a96209ea5735))

## 0.1.0 (2024-06-05)


### Features

* add initial files for google.cloud.developerconnect.v1 ([#12777](https://github.com/googleapis/google-cloud-python/issues/12777)) ([3deb6c7](https://github.com/googleapis/google-cloud-python/commit/3deb6c728455ca41180527b268d2f18445136520))

## Changelog
