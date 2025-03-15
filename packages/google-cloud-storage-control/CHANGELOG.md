# Changelog

## [1.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.3.0...google-cloud-storage-control-v1.3.1) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([784a3ca](https://github.com/googleapis/google-cloud-python/commit/784a3ca7a180453320521753f5bce71de329d65c))
* Allow Protobuf 6.x ([#13651](https://github.com/googleapis/google-cloud-python/issues/13651)) ([1b8080e](https://github.com/googleapis/google-cloud-python/commit/1b8080e7069c9d0776e293bab06db54adf157aef))

## [1.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.2.0...google-cloud-storage-control-v1.3.0) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))
* Add support for reading selective GAPIC generation methods from service YAML ([87b5382](https://github.com/googleapis/google-cloud-python/commit/87b5382a05b7a0c9faeabaf3e2baa6f05c88bb8e))

## [1.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.1.1...google-cloud-storage-control-v1.2.0) (2024-12-12)


### Features

* Add support for opt-in debug logging ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))


### Bug Fixes

* Fix typing issue with gRPC metadata when key ends in -bin ([856e0f0](https://github.com/googleapis/google-cloud-python/commit/856e0f07bd5212d60ad64be4c16ac8fafd07850b))

## [1.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.1.0...google-cloud-storage-control-v1.1.1) (2024-11-11)


### Bug Fixes

* disable universe-domain validation  ([#13246](https://github.com/googleapis/google-cloud-python/issues/13246)) ([bcad563](https://github.com/googleapis/google-cloud-python/commit/bcad563acea541bb51f9fbd005f18e9f32e381f0))

## [1.1.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.0.3...google-cloud-storage-control-v1.1.0) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13209](https://github.com/googleapis/google-cloud-python/issues/13209)) ([5f2e30d](https://github.com/googleapis/google-cloud-python/commit/5f2e30d62eea6080f5707ee18755f2bb812ad00b))

## [1.0.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.0.2...google-cloud-storage-control-v1.0.3) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([9cdac77](https://github.com/googleapis/google-cloud-python/commit/9cdac77b20a8c9720aa668639e3ca6d1e759a2de))

## [1.0.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.0.1...google-cloud-storage-control-v1.0.2) (2024-07-08)


### Bug Fixes

* Allow Protobuf 5.x ([#12870](https://github.com/googleapis/google-cloud-python/issues/12870)) ([4d16761](https://github.com/googleapis/google-cloud-python/commit/4d16761640dd8e35410b3219b7d675d7668d2f88))

## [1.0.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v1.0.0...google-cloud-storage-control-v1.0.1) (2024-06-24)


### Documentation

* remove allowlist note from Folders RPCs ([41a3afd](https://github.com/googleapis/google-cloud-python/commit/41a3afda46a7c3f02bff3f92f15cd49daf92083e))

## [1.0.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v0.2.0...google-cloud-storage-control-v1.0.0) (2024-06-19)


### Features

* bump release level to production/stable ([4a15440](https://github.com/googleapis/google-cloud-python/commit/4a154403f07321af6ea051fa81b58ee2651de34f))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v0.1.3...google-cloud-storage-control-v0.2.0) (2024-05-07)


### ⚠ BREAKING CHANGES

* An existing resource pattern value `projects/{project}/buckets/{bucket}/managedFolders/{managedFolder=**}` to resource definition `[storage.googleapis.com/ManagedFolder](https://www.google.com/url?sa=D&q=http%3A%2F%2Fstorage.googleapis.com%2FManagedFolder)` is removed

### Features

* A new resource pattern value `projects/{project}/buckets/{bucket}/managedFolders/{managed_folder=**}` added to the resource definition `[storage.googleapis.com/ManagedFolder](https://www.google.com/url?sa=D&q=http%3A%2F%2Fstorage.googleapis.com%2FManagedFolder)` ([ddd1508](https://github.com/googleapis/google-cloud-python/commit/ddd15081a5fa9f844ffcafbc0136c1cd32582a39))


### Bug Fixes

* An existing resource pattern value `projects/{project}/buckets/{bucket}/managedFolders/{managedFolder=**}` to resource definition `[storage.googleapis.com/ManagedFolder](https://www.google.com/url?sa=D&q=http%3A%2F%2Fstorage.googleapis.com%2FManagedFolder)` is removed ([ddd1508](https://github.com/googleapis/google-cloud-python/commit/ddd15081a5fa9f844ffcafbc0136c1cd32582a39))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v0.1.2...google-cloud-storage-control-v0.1.3) (2024-04-19)


### Documentation

* [google-cloud-storage-control] update storage control documentation ([#12594](https://github.com/googleapis/google-cloud-python/issues/12594)) ([b593dd7](https://github.com/googleapis/google-cloud-python/commit/b593dd73c9a909c5df885324954681836492f837))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v0.1.1...google-cloud-storage-control-v0.1.2) (2024-04-04)


### Documentation

* Update README ([#12543](https://github.com/googleapis/google-cloud-python/issues/12543)) ([30b7a8f](https://github.com/googleapis/google-cloud-python/commit/30b7a8f3588ce0535a575739851ee8f8be216f73))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-storage-control-v0.1.0...google-cloud-storage-control-v0.1.1) (2024-04-03)


### Features

* Make Managed Folders operations public ([dfa5e69](https://github.com/googleapis/google-cloud-python/commit/dfa5e691c175e45c47b00975572add00fd7f3e28))

## 0.1.0 (2024-03-25)


### Features

* add initial files for google.cloud.storage.control.v2 ([#12485](https://github.com/googleapis/google-cloud-python/issues/12485)) ([3322d6b](https://github.com/googleapis/google-cloud-python/commit/3322d6b60679ad4a0a29d835e2ded0ad14e6ce71))

## Changelog
