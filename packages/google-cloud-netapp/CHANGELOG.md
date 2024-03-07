# Changelog

## [0.3.8](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.7...google-cloud-netapp-v0.3.8) (2024-03-07)


### Documentation

* change comments of the psa_range field to note it is currently not implemented ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))
* mark optional fields explicitly in Storage Pool ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))
* update comments of ServiceLevel and EncryptionType ([2a91b59](https://github.com/googleapis/google-cloud-python/commit/2a91b59c970c488afb8f728b3553e4317260d556))

## [0.3.7](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.6...google-cloud-netapp-v0.3.7) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12385](https://github.com/googleapis/google-cloud-python/issues/12385)) ([d50f4d0](https://github.com/googleapis/google-cloud-python/commit/d50f4d042774e2f12e9fe03459eae9ce91247df3))

## [0.3.6](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.5...google-cloud-netapp-v0.3.6) (2024-02-22)


### Bug Fixes

* **deps:** [Many APIs] Require `google-api-core&gt;=1.34.1` ([#12307](https://github.com/googleapis/google-cloud-python/issues/12307)) ([be87bc4](https://github.com/googleapis/google-cloud-python/commit/be87bc4a33fe32a512448a42246c9873da88269f))
* fix ValueError in test__validate_universe_domain ([7c2f2c2](https://github.com/googleapis/google-cloud-python/commit/7c2f2c29d74c9584efc42ddfe8bc098a594391a2))

## [0.3.5](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.4...google-cloud-netapp-v0.3.5) (2024-02-06)


### Bug Fixes

* Add google-auth as a direct dependency ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Add staticmethod decorator to _get_client_cert_source and _get_api_endpoint ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))
* Resolve AttributeError 'Credentials' object has no attribute 'universe_domain' ([27dceb9](https://github.com/googleapis/google-cloud-python/commit/27dceb901cb9bf28da82925ad382ce7c58e91f38))

## [0.3.4](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.3...google-cloud-netapp-v0.3.4) (2024-02-01)


### Features

* Allow users to explicitly configure universe domain ([#12241](https://github.com/googleapis/google-cloud-python/issues/12241)) ([aae72f5](https://github.com/googleapis/google-cloud-python/commit/aae72f5e6c7d48e777fdf68d1012b2b51b912bad))

## [0.3.3](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.2...google-cloud-netapp-v0.3.3) (2024-01-04)


### Features

* Add singular and plural annotations ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))
* Enable Backup, Backup Vault, and Backup Policy ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))
* Set field_behavior to IDENTIFIER on the "name" fields ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))


### Documentation

* Comments are updated for several fields/enums ([b21ac63](https://github.com/googleapis/google-cloud-python/commit/b21ac63d41113dfd9880b4e4ab1fe10928c7b72b))

## [0.3.2](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.1...google-cloud-netapp-v0.3.2) (2023-12-07)


### Features

* Add support for python 3.12 ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))
* Introduce compatibility with native namespace packages ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))


### Bug Fixes

* Require proto-plus &gt;= 1.22.3 ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))
* Use `retry_async` instead of `retry` in async client ([5cd98aa](https://github.com/googleapis/google-cloud-python/commit/5cd98aa0e8ead2eef82ecdcef4141b33a7da2b5a))

## [0.3.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.3.0...google-cloud-netapp-v0.3.1) (2023-09-19)


### Documentation

* Minor formatting ([1ae610b](https://github.com/googleapis/google-cloud-python/commit/1ae610bb3b321ceac7bd23a455a002e39645d84f))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.2.0...google-cloud-netapp-v0.3.0) (2023-08-09)


### Features

* add actions for Operations and Locations ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))
* add RestrictedAction to Volume ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))


### Documentation

* add comments to a few messages ([a3f4a23](https://github.com/googleapis/google-cloud-python/commit/a3f4a236b14bec15f0cbed7a2c40d81cb818efb4))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-netapp-v0.1.0...google-cloud-netapp-v0.2.0) (2023-08-03)


### Features

* add initial version of NetApp v1 APIs ([de53f0e](https://github.com/googleapis/google-cloud-python/commit/de53f0efe25e71d0aa5b57b0989c4f0a491fa2ec))


### Bug Fixes

* remove netapp_v1beta1 client ([#11534](https://github.com/googleapis/google-cloud-python/issues/11534)) ([e7b16ed](https://github.com/googleapis/google-cloud-python/commit/e7b16ed17e06fa42858e5fdd35953805b8ca7e90))
* update the default import to use `netapp_v1` ([de53f0e](https://github.com/googleapis/google-cloud-python/commit/de53f0efe25e71d0aa5b57b0989c4f0a491fa2ec))

## 0.1.0 (2023-07-20)


### Features

* add initial files for google.cloud.netapp.v1beta1 ([#11490](https://github.com/googleapis/google-cloud-python/issues/11490)) ([719a2d5](https://github.com/googleapis/google-cloud-python/commit/719a2d5d6e792b3d96dc72a1743dc7b4b4321edc))

## Changelog
