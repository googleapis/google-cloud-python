# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datacatalog/#history

## [3.14.0](https://github.com/googleapis/google-cloud-python/compare/google-cloud-datacatalog-v3.13.1...google-cloud-datacatalog-v3.14.0) (2023-07-10)


### Features

* added Entry.usage_signal ([b279092](https://github.com/googleapis/google-cloud-python/commit/b279092e52184a5e67bd817248ccae726fc10cae))
* added rpc RenameTagTemplateFieldEnumValue ([b279092](https://github.com/googleapis/google-cloud-python/commit/b279092e52184a5e67bd817248ccae726fc10cae))
* returning approximate total size for SearchCatalog ([b279092](https://github.com/googleapis/google-cloud-python/commit/b279092e52184a5e67bd817248ccae726fc10cae))
* returning unreachable locations for SearchCatalog ([b279092](https://github.com/googleapis/google-cloud-python/commit/b279092e52184a5e67bd817248ccae726fc10cae))


### Documentation

* update docs of SearchCatalogRequest message ([b279092](https://github.com/googleapis/google-cloud-python/commit/b279092e52184a5e67bd817248ccae726fc10cae))

## [3.13.1](https://github.com/googleapis/google-cloud-python/compare/google-cloud-datacatalog-v3.13.0...google-cloud-datacatalog-v3.13.1) (2023-07-05)


### Bug Fixes

* Add async context manager return types ([#11445](https://github.com/googleapis/google-cloud-python/issues/11445)) ([98bddda](https://github.com/googleapis/google-cloud-python/commit/98bdddafc821e2fc6e86a31965da0c46899aa229))

## [3.13.0](https://github.com/googleapis/python-datacatalog/compare/v3.12.0...v3.13.0) (2023-05-29)


### Features

* Add support for entries associated with Spanner and CloudBigTable ([c057e0d](https://github.com/googleapis/python-datacatalog/commit/c057e0d27554b680ee097e3cc8fb656cdfca23d6))
* Expand SearchCatalogResponse with totalSize ([c057e0d](https://github.com/googleapis/python-datacatalog/commit/c057e0d27554b680ee097e3cc8fb656cdfca23d6))
* Extend ImportApiRequest with jobId parameter ([c057e0d](https://github.com/googleapis/python-datacatalog/commit/c057e0d27554b680ee097e3cc8fb656cdfca23d6))
* Modify documentation for FQN support ([c057e0d](https://github.com/googleapis/python-datacatalog/commit/c057e0d27554b680ee097e3cc8fb656cdfca23d6))

## [3.12.0](https://github.com/googleapis/python-datacatalog/compare/v3.11.1...v3.12.0) (2023-03-23)


### Features

* Add support for a ReconcileTags() API method ([423efa5](https://github.com/googleapis/python-datacatalog/commit/423efa530c48b8f8d397aa0a555c2c00729301b0))
* Add support for entries associated with Looker and CloudSQL ([423efa5](https://github.com/googleapis/python-datacatalog/commit/423efa530c48b8f8d397aa0a555c2c00729301b0))
* Add support for new ImportEntries() API, including format of the dump ([423efa5](https://github.com/googleapis/python-datacatalog/commit/423efa530c48b8f8d397aa0a555c2c00729301b0))


### Documentation

* Fix formatting of request arg in docstring ([#472](https://github.com/googleapis/python-datacatalog/issues/472)) ([99ea7ba](https://github.com/googleapis/python-datacatalog/commit/99ea7baf21f8beca897497e5b31ac4086c1d681f))

## [3.11.1](https://github.com/googleapis/python-datacatalog/compare/v3.11.0...v3.11.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([f9d47e0](https://github.com/googleapis/python-datacatalog/commit/f9d47e00d82bdddc19f35d59b7106e09c58cd9a4))


### Documentation

* Add documentation for enums ([f9d47e0](https://github.com/googleapis/python-datacatalog/commit/f9d47e00d82bdddc19f35d59b7106e09c58cd9a4))

## [3.11.0](https://github.com/googleapis/python-datacatalog/compare/v3.10.0...v3.11.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#454](https://github.com/googleapis/python-datacatalog/issues/454)) ([07d3519](https://github.com/googleapis/python-datacatalog/commit/07d351957d43180278705dc7ca59df343897ddd7))

## [3.10.0](https://github.com/googleapis/python-datacatalog/compare/v3.9.3...v3.10.0) (2022-12-14)


### Features

* Add support for `google.cloud.datacatalog.__version__` ([8a4f5f8](https://github.com/googleapis/python-datacatalog/commit/8a4f5f854d217723564f56451d2c19bad47a3734))
* Add typing to proto.Message based class attributes ([8a4f5f8](https://github.com/googleapis/python-datacatalog/commit/8a4f5f854d217723564f56451d2c19bad47a3734))


### Bug Fixes

* Add dict typing for client_options ([8a4f5f8](https://github.com/googleapis/python-datacatalog/commit/8a4f5f854d217723564f56451d2c19bad47a3734))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([9682965](https://github.com/googleapis/python-datacatalog/commit/968296505e81277bbeaa60c9fac78f3370a60abe))
* Drop usage of pkg_resources ([9682965](https://github.com/googleapis/python-datacatalog/commit/968296505e81277bbeaa60c9fac78f3370a60abe))
* Fix timeout default values ([9682965](https://github.com/googleapis/python-datacatalog/commit/968296505e81277bbeaa60c9fac78f3370a60abe))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([8a4f5f8](https://github.com/googleapis/python-datacatalog/commit/8a4f5f854d217723564f56451d2c19bad47a3734))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([9682965](https://github.com/googleapis/python-datacatalog/commit/968296505e81277bbeaa60c9fac78f3370a60abe))

## [3.9.3](https://github.com/googleapis/python-datacatalog/compare/v3.9.2...v3.9.3) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#437](https://github.com/googleapis/python-datacatalog/issues/437)) ([1f75417](https://github.com/googleapis/python-datacatalog/commit/1f75417169a894cdd22a35c3bc5b7d65b4b94fb3))

## [3.9.2](https://github.com/googleapis/python-datacatalog/compare/v3.9.1...v3.9.2) (2022-10-03)


### Bug Fixes

* **deps:** Require protobuf &gt;= 3.20.2 ([#433](https://github.com/googleapis/python-datacatalog/issues/433)) ([182a6e9](https://github.com/googleapis/python-datacatalog/commit/182a6e9c6afd62ee6da9a90d125dc713f5dc63a2))

## [3.9.1](https://github.com/googleapis/python-datacatalog/compare/v3.9.0...v3.9.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#412](https://github.com/googleapis/python-datacatalog/issues/412)) ([dadf9e7](https://github.com/googleapis/python-datacatalog/commit/dadf9e72bae8862b3125399049ad419e55646e1a))
* **deps:** require proto-plus >= 1.22.0 ([dadf9e7](https://github.com/googleapis/python-datacatalog/commit/dadf9e72bae8862b3125399049ad419e55646e1a))

## [3.9.0](https://github.com/googleapis/python-datacatalog/compare/v3.8.1...v3.9.0) (2022-07-16)


### Features

* add audience parameter ([624f2eb](https://github.com/googleapis/python-datacatalog/commit/624f2ebc431db8872c30f85b0afc0bfb01f9e02c))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#401](https://github.com/googleapis/python-datacatalog/issues/401)) ([624f2eb](https://github.com/googleapis/python-datacatalog/commit/624f2ebc431db8872c30f85b0afc0bfb01f9e02c))
* require python 3.7+ ([#403](https://github.com/googleapis/python-datacatalog/issues/403)) ([5a1b948](https://github.com/googleapis/python-datacatalog/commit/5a1b948b0ab10757a8c778bc9e44094347069d8b))

## [3.8.1](https://github.com/googleapis/python-datacatalog/compare/v3.8.0...v3.8.1) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#384](https://github.com/googleapis/python-datacatalog/issues/384)) ([f73208b](https://github.com/googleapis/python-datacatalog/commit/f73208b7022c35267e62bdb3ba8bb4de7bc51915))


### Documentation

* fix changelog header to consistent size ([#385](https://github.com/googleapis/python-datacatalog/issues/385)) ([7588b0b](https://github.com/googleapis/python-datacatalog/commit/7588b0bf7221c1c4b599fd9d196c3674828718b4))

## [3.8.0](https://github.com/googleapis/python-datacatalog/compare/v3.7.1...v3.8.0) (2022-05-09)


### Features

* added Dataplex specific fields ([9e33102](https://github.com/googleapis/python-datacatalog/commit/9e331027aa40dcbe4e7880d18043d89aa6af6b2a))
* AuditConfig for IAM v1 ([9e33102](https://github.com/googleapis/python-datacatalog/commit/9e331027aa40dcbe4e7880d18043d89aa6af6b2a))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([9e33102](https://github.com/googleapis/python-datacatalog/commit/9e331027aa40dcbe4e7880d18043d89aa6af6b2a))


### Documentation

* fix type in docstring for map fields ([9e33102](https://github.com/googleapis/python-datacatalog/commit/9e331027aa40dcbe4e7880d18043d89aa6af6b2a))
* update taxonomy display_name comment ([#338](https://github.com/googleapis/python-datacatalog/issues/338)) ([9e33102](https://github.com/googleapis/python-datacatalog/commit/9e331027aa40dcbe4e7880d18043d89aa6af6b2a))

## [3.7.1](https://github.com/googleapis/python-datacatalog/compare/v3.7.0...v3.7.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#311](https://github.com/googleapis/python-datacatalog/issues/311)) ([f2f3c7f](https://github.com/googleapis/python-datacatalog/commit/f2f3c7fbac3b07d40d7e61f747cc6e9688da71d1))
* **deps:** require proto-plus>=1.15.0 ([f2f3c7f](https://github.com/googleapis/python-datacatalog/commit/f2f3c7fbac3b07d40d7e61f747cc6e9688da71d1))

## [3.7.0](https://github.com/googleapis/python-datacatalog/compare/v3.6.2...v3.7.0) (2022-02-28)


### Features

* add api key support ([#291](https://github.com/googleapis/python-datacatalog/issues/291)) ([7d8c3bc](https://github.com/googleapis/python-datacatalog/commit/7d8c3bc9bf540d3e5c0b0bd80a619792162c4fe2))
* Add methods and messages related to business context feature ([650ad39](https://github.com/googleapis/python-datacatalog/commit/650ad39b6620c764ea64f5c0f2498a0ea387a834))
* Add methods and messages related to starring feature ([#297](https://github.com/googleapis/python-datacatalog/issues/297)) ([650ad39](https://github.com/googleapis/python-datacatalog/commit/650ad39b6620c764ea64f5c0f2498a0ea387a834))


### Bug Fixes

* **deps:** move libcst to extras ([#300](https://github.com/googleapis/python-datacatalog/issues/300)) ([eaf1ad6](https://github.com/googleapis/python-datacatalog/commit/eaf1ad6c4c15781b0a19a2dc5a3c67966279cbaa))
* resolve DuplicateCredentialArgs error when using credentials_file ([18b7f51](https://github.com/googleapis/python-datacatalog/commit/18b7f517abc8b15c64763c430b8c51bd2f7e993c))


### Documentation

* add autogenerated code snippets ([650ad39](https://github.com/googleapis/python-datacatalog/commit/650ad39b6620c764ea64f5c0f2498a0ea387a834))

## [3.6.2](https://www.github.com/googleapis/python-datacatalog/compare/v3.6.1...v3.6.2) (2022-01-10)


### Documentation

* convert UPGRADING guide to RST to fix table formatting ([#268](https://www.github.com/googleapis/python-datacatalog/issues/268)) ([571171e](https://www.github.com/googleapis/python-datacatalog/commit/571171e65fad5939ce3f20ec63ac35c8c80f2e2a))
* fixing upgrading guide v2 ([#277](https://www.github.com/googleapis/python-datacatalog/issues/277)) ([76f152a](https://www.github.com/googleapis/python-datacatalog/commit/76f152ac59e81d1ac02adcba2cbc8b1bec3ff888))
* **samples:** Add sample for PolicyTagManagerClient.create_taxonomy ([#37](https://www.github.com/googleapis/python-datacatalog/issues/37)) ([15feb5d](https://www.github.com/googleapis/python-datacatalog/commit/15feb5dba028faa153c72374eca20a72fa72705e))

## [3.6.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.6.0...v3.6.1) (2021-11-12)


### Documentation

* Improved formatting ([#260](https://www.github.com/googleapis/python-datacatalog/issues/260)) ([5bc3840](https://www.github.com/googleapis/python-datacatalog/commit/5bc3840a5e922b91069cc9003f1596a4633e3afc))

## [3.6.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.5.0...v3.6.0) (2021-11-08)


### Features

* Added BigQueryDateShardedSpec.latest_shard_resource field ([#256](https://www.github.com/googleapis/python-datacatalog/issues/256)) ([36019b6](https://www.github.com/googleapis/python-datacatalog/commit/36019b6218ed8153ef9cdcfc2d57434c6e7f0b25))
* Added SearchCatalogResult.description field ([36019b6](https://www.github.com/googleapis/python-datacatalog/commit/36019b6218ed8153ef9cdcfc2d57434c6e7f0b25))
* Added SearchCatalogResult.display_name field ([36019b6](https://www.github.com/googleapis/python-datacatalog/commit/36019b6218ed8153ef9cdcfc2d57434c6e7f0b25))


### Bug Fixes

* **deps:** drop packaging dependency ([0dcc0c3](https://www.github.com/googleapis/python-datacatalog/commit/0dcc0c36484ac8013ba911322d7641f5b73efe11))
* **deps:** require google-api-core >= 1.28.0 ([0dcc0c3](https://www.github.com/googleapis/python-datacatalog/commit/0dcc0c36484ac8013ba911322d7641f5b73efe11))


### Documentation

* attempt to fix table layout ([#249](https://www.github.com/googleapis/python-datacatalog/issues/249)) ([26c19ae](https://www.github.com/googleapis/python-datacatalog/commit/26c19ae8bbe96f7a82e4f36a251e7abea98ce2b1))
* list oneofs in docstring ([0dcc0c3](https://www.github.com/googleapis/python-datacatalog/commit/0dcc0c36484ac8013ba911322d7641f5b73efe11))

## [3.5.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.3...v3.5.0) (2021-10-28)


### Features

* add context manager support in client ([#240](https://www.github.com/googleapis/python-datacatalog/issues/240)) ([c403d1d](https://www.github.com/googleapis/python-datacatalog/commit/c403d1d5a637b23343b23e74debed5f8b4c5c12a))

## [3.4.3](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.2...v3.4.3) (2021-10-05)


### Bug Fixes

* improper types in pagers generation ([322cf9e](https://www.github.com/googleapis/python-datacatalog/commit/322cf9e543147b0b40e3b044e5822acf12e2d216))

## [3.4.2](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.1...v3.4.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([27fcefa](https://www.github.com/googleapis/python-datacatalog/commit/27fcefa6df0d9a3a1c0954dd908b9aa3ad1bf548))


### Documentation

* **samples:** add entry group greation to custom entry sample ([#215](https://www.github.com/googleapis/python-datacatalog/issues/215)) ([24d78cf](https://www.github.com/googleapis/python-datacatalog/commit/24d78cf44dd0a4e29aa66daec137e8a618b60f29))

## [3.4.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.0...v3.4.1) (2021-09-01)


### Bug Fixes

* make datacatalog == datacatalog_v1 ([#206](https://www.github.com/googleapis/python-datacatalog/issues/206)) ([aefe892](https://www.github.com/googleapis/python-datacatalog/commit/aefe892ab2cdb37b5f58faecd45758ea685c74ec))


### Documentation

* **samples:** add samples from docs & reorganize all samples for testing ([#78](https://www.github.com/googleapis/python-datacatalog/issues/78)) ([d34aca0](https://www.github.com/googleapis/python-datacatalog/commit/d34aca05a87aa75ad982612f57fe987a005f7896))

## [3.4.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.2...v3.4.0) (2021-07-28)


### Features

* Added ReplaceTaxonomy in Policy Tag Manager Serialization API ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for BigQuery connections entries ([#196](https://www.github.com/googleapis/python-datacatalog/issues/196)) ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for BigQuery routines entries ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for public tag templates ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for rich text tags ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added usage_signal field ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))


### Documentation

* Documentation improvements ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))

## [3.3.2](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.1...v3.3.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#192](https://www.github.com/googleapis/python-datacatalog/issues/192)) ([90a0be2](https://www.github.com/googleapis/python-datacatalog/commit/90a0be276e38e889a5086f8fd233d5b25e19965e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#187](https://www.github.com/googleapis/python-datacatalog/issues/187)) ([317b207](https://www.github.com/googleapis/python-datacatalog/commit/317b207ef03ecedb84bd4619da71859b9ec1d6db))


### Miscellaneous Chores

* release as 3.3.2 ([#193](https://www.github.com/googleapis/python-datacatalog/issues/193)) ([7f38774](https://www.github.com/googleapis/python-datacatalog/commit/7f38774e4831122f5b645b911eed0f673e0f182f))

## [3.3.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.0...v3.3.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#186](https://www.github.com/googleapis/python-datacatalog/issues/186)) ([915f387](https://www.github.com/googleapis/python-datacatalog/commit/915f3875bf8496203aa6bc4ee6ce11fde33f65e9))

## [3.3.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.2.1...v3.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#178](https://www.github.com/googleapis/python-datacatalog/issues/178)) ([2cb3cc2](https://www.github.com/googleapis/python-datacatalog/commit/2cb3cc2e062045b4b1f602c6e2ed79b3dc6f0014))


### Bug Fixes

* disable always_use_jwt_access ([#182](https://www.github.com/googleapis/python-datacatalog/issues/182)) ([1bef446](https://www.github.com/googleapis/python-datacatalog/commit/1bef4465d7c0f7f4e84afb664ca5d9f55e92ea14))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-datacatalog/issues/1127)) ([#173](https://www.github.com/googleapis/python-datacatalog/issues/173)) ([a3d17d4](https://www.github.com/googleapis/python-datacatalog/commit/a3d17d4b485e757480040783259da234abec69a0)), closes [#1126](https://www.github.com/googleapis/python-datacatalog/issues/1126)

## [3.2.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.2.0...v3.2.1) (2021-06-09)


### Bug Fixes

* **deps:** add packaging requirement ([#163](https://www.github.com/googleapis/python-datacatalog/issues/163)) ([1cfdb5a](https://www.github.com/googleapis/python-datacatalog/commit/1cfdb5a444cd6c845546b060da2e0a0f7d533a0c))

## [3.2.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.1.1...v3.2.0) (2021-05-18)


### Features

* support self-signed JWT flow for service accounts ([85e46e1](https://www.github.com/googleapis/python-datacatalog/commit/85e46e144d32a0d66bc2d7c056453951eb77d592))


### Bug Fixes

* add async client to %name_%version/init.py ([85e46e1](https://www.github.com/googleapis/python-datacatalog/commit/85e46e144d32a0d66bc2d7c056453951eb77d592))

## [3.1.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.1.0...v3.1.1) (2021-03-29)


### Bug Fixes

* use correct retry deadline ([#124](https://www.github.com/googleapis/python-datacatalog/issues/124)) ([0c69bc2](https://www.github.com/googleapis/python-datacatalog/commit/0c69bc2fbae593f62c543c5a15dbe810467b7510))

## [3.1.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.0.0...v3.1.0) (2021-03-22)


### Features

* add `client_cert_source_for_mtls` argument to transports ([#107](https://www.github.com/googleapis/python-datacatalog/issues/107)) ([59a44bc](https://www.github.com/googleapis/python-datacatalog/commit/59a44bc744a6322a2a23313c851eb77204110e79))


### Bug Fixes

* remove gRPC send/recv limit; add enums to `types/__init__.py` ([#87](https://www.github.com/googleapis/python-datacatalog/issues/87)) ([e0c40c7](https://www.github.com/googleapis/python-datacatalog/commit/e0c40c765242868570532b5074fd239aa2c259e9))


### Documentation

* document enum values with `undoc-members` option ([#93](https://www.github.com/googleapis/python-datacatalog/issues/93)) ([2dbb3ef](https://www.github.com/googleapis/python-datacatalog/commit/2dbb3ef062b52925ad421c5c469ed6e67671e878))
* fix `type_` attribute name in the migration guide ([#113](https://www.github.com/googleapis/python-datacatalog/issues/113)) ([2f98f22](https://www.github.com/googleapis/python-datacatalog/commit/2f98f2244271d92f79fdb26103478166958b8c8a))
* fix upgrade guide ([#114](https://www.github.com/googleapis/python-datacatalog/issues/114)) ([4bfa587](https://www.github.com/googleapis/python-datacatalog/commit/4bfa587903105cb3de2272618374df0b04156017))
* update the upgrade guide to be from 1.0 to 3.0 ([#77](https://www.github.com/googleapis/python-datacatalog/issues/77)) ([eed034a](https://www.github.com/googleapis/python-datacatalog/commit/eed034a3969913e40554300ae97c5e00e4fcc79a))

## [3.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v2.0.0...v3.0.0) (2020-11-17)


### ⚠ BREAKING CHANGES

* add common resource paths; expose client transport; rename ``type`` attributes to ``type_`` to avoid name collisions. (#64)

  Renamed attributes:
    * `TagTemplateField.type` -> `TagTemplatedField.type_`
    * `ColumnSchema.type` -> `ColumnSchema.type_`
    * `Entry.type` -> `Entry.type_`


### Features

* add common resource paths; expose client transport; rename ``type`` attributes to ``type_`` to avoid name collisions ([#64](https://www.github.com/googleapis/python-datacatalog/issues/64)) ([f8f797a](https://www.github.com/googleapis/python-datacatalog/commit/f8f797af757f643c4414e3c7a58b3423b3d80d6f))

## [2.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v1.0.0...v2.0.0) (2020-08-20)


### ⚠ BREAKING CHANGES

* This release has breaking changes. See the [2.0.0 Migration Guide](https://github.com/googleapis/python-datacatalog/blob/main/UPGRADING.md) for details.

### Features

* Migrate API client to Microgenerator ([#54](https://www.github.com/googleapis/python-datacatalog/issues/54)) ([14fbdb8](https://www.github.com/googleapis/python-datacatalog/commit/14fbdb811688296e3978b4dfe7d4c240b5b1da5d))


### Bug Fixes

* update retry config ([#47](https://www.github.com/googleapis/python-datacatalog/issues/47)) ([1c56be7](https://www.github.com/googleapis/python-datacatalog/commit/1c56be78f1aae8dd5cd93e81188135d72cc80fdc))


### Documentation

* fix readme link ([#58](https://www.github.com/googleapis/python-datacatalog/issues/58)) ([55da34c](https://www.github.com/googleapis/python-datacatalog/commit/55da34caac42dd5959c046a50ba79375f7a41788))

## [1.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.8.0...v1.0.0) (2020-06-17)


### Features

* release as production/stable ([#25](https://www.github.com/googleapis/python-datacatalog/issues/25)) ([6d4c3df](https://www.github.com/googleapis/python-datacatalog/commit/6d4c3df232ba933e16780231b92c830453206170)), closes [#24](https://www.github.com/googleapis/python-datacatalog/issues/24)

## [0.8.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.7.0...v0.8.0) (2020-05-20)


### Features

* add `restricted_locations` to v1; add `order` to `TagField` and `TagTemplateField` in v1beta1; rename `field_path` to `tag_template_field_path` in v1beta1; add pagination support to `list_taxonomies` in v1beta1 ([#20](https://www.github.com/googleapis/python-datacatalog/issues/20)) ([7a890c2](https://www.github.com/googleapis/python-datacatalog/commit/7a890c2f87ff37f610c7246bcbf369314d87b93d))

## [0.7.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.6.0...v0.7.0) (2020-04-09)


### Features

* add v1 ([#13](https://www.github.com/googleapis/python-datacatalog/issues/13)) ([21629fe](https://www.github.com/googleapis/python-datacatalog/commit/21629fed1f86bb1a2800b5213f59acc5d862e2f5))

## [0.6.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.5.0...v0.6.0) (2020-02-24)


### Features

* **datacatalog:** add sample for create a fileset entry quickstart ([#9977](https://www.github.com/googleapis/python-datacatalog/issues/9977)) ([16eaf4b](https://www.github.com/googleapis/python-datacatalog/commit/16eaf4b16cdc0ce7361afb1d8dac666cea2a9db0))
* **datacatalog:** undeprecate resource name helper methods, bump copyright year to 2020, tweak docstring formatting (via synth) ([#10228](https://www.github.com/googleapis/python-datacatalog/issues/10228)) ([84e5e7c](https://www.github.com/googleapis/python-datacatalog/commit/84e5e7c340fa189ce4cffca4fdee82cc7ded9f70))
* add `list_entry_groups`, `list_entries`, `update_entry_group` methods to v1beta1 (via synth) ([#6](https://www.github.com/googleapis/python-datacatalog/issues/6)) ([b51902e](https://www.github.com/googleapis/python-datacatalog/commit/b51902e26d590f52c9412756a178265850b7d516))


### Bug Fixes

* **datacatalog:** deprecate resource name helper methods (via synth) ([#9831](https://www.github.com/googleapis/python-datacatalog/issues/9831)) ([22db3f0](https://www.github.com/googleapis/python-datacatalog/commit/22db3f0683b8aca544cd96c0063dcc8157ad7335))

## 0.5.0

11-14-2019 12:54 PST

### New Features

- add policy tag manager clients ([#9804](https://github.com/googleapis/google-cloud-python/pull/9804))

### Documentation

- add python 2 sunset banner to documentation ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- add sample to create a fileset entry ([#9590](https://github.com/googleapis/google-cloud-python/pull/9590))
- add sample to create an entry group ([#9584](https://github.com/googleapis/google-cloud-python/pull/9584))

### Internal / Testing Changes

- change spacing in docs templates (via synth) ([#9743](https://github.com/googleapis/google-cloud-python/pull/9743))

## 0.4.0

10-23-2019 08:54 PDT

### Implementation Changes

- remove send/recv msg size limit (via synth) ([#8949](https://github.com/googleapis/google-cloud-python/pull/8949))

### New Features

- add entry group operations ([#9520](https://github.com/googleapis/google-cloud-python/pull/9520))

### Documentation

- fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- remove unused import from samples (via synth). ([#9110](https://github.com/googleapis/google-cloud-python/pull/9110))
- remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- add 'search' sample (via synth). ([#8793](https://github.com/googleapis/google-cloud-python/pull/8793))

## 0.3.0

07-24-2019 15:58 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8425](https://github.com/googleapis/google-cloud-python/pull/8425))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8654](https://github.com/googleapis/google-cloud-python/pull/8654))
- Add 'client_options' support, update list method docstrings (via synth). ([#8503](https://github.com/googleapis/google-cloud-python/pull/8503))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Add get_entry sample (via synth). ([#8725](https://github.com/googleapis/google-cloud-python/pull/8725))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add generated samples (via synth). ([#8710](https://github.com/googleapis/google-cloud-python/pull/8710))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Update docstrings (via synth). ([#8299](https://github.com/googleapis/google-cloud-python/pull/8299))

### Internal / Testing Changes
- Enable Sample Generator Tool for Data Catalog ([#8708](https://github.com/googleapis/google-cloud-python/pull/8708))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.2.0

06-12-2019 12:46 PDT

### New Features

- Add search capability, tags that match a query, and IAM policies ([#8266](https://github.com/googleapis/google-cloud-python/pull/8266))
- Add protos as an artifact to library (via synth). ([#8018](https://github.com/googleapis/google-cloud-python/pull/8018))

### Documentation

- Add nox session `docs`, reorder methods (via synth). ([#7766](https://github.com/googleapis/google-cloud-python/pull/7766))
- Fix broken link to client library docs in README ([#7713](https://github.com/googleapis/google-cloud-python/pull/7713))

### Internal / Testing Changes

- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8235](https://github.com/googleapis/google-cloud-python/pull/8235))
- Fix coverage in 'types.py' (via synth). ([#8150](https://github.com/googleapis/google-cloud-python/pull/8150))
- Blacken noxfile.py, setup.py (via synth). ([#8117](https://github.com/googleapis/google-cloud-python/pull/8117))
- Add empty lines (via synth). ([#8052](https://github.com/googleapis/google-cloud-python/pull/8052))

## 0.1.0

04-15-2019 15:46 PDT

### New Features

- Initial release of Cloud Data Catalog client. ([#7708](https://github.com/googleapis/google-cloud-python/pull/7708))
