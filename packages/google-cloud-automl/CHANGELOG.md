# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-automl/#history

### [2.7.2](https://github.com/googleapis/python-automl/compare/v2.7.1...v2.7.2) (2022-03-06)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#348](https://github.com/googleapis/python-automl/issues/348)) ([ec5e4e2](https://github.com/googleapis/python-automl/commit/ec5e4e2e2089b99b957f051c7bbd280457514f83))
* **deps:** require proto-plus>=1.15.0 ([ec5e4e2](https://github.com/googleapis/python-automl/commit/ec5e4e2e2089b99b957f051c7bbd280457514f83))

### [2.7.1](https://github.com/googleapis/python-automl/compare/v2.7.0...v2.7.1) (2022-02-26)


### Bug Fixes

* handle AttributeError in automl_v1beta1.TablesClient ([#338](https://github.com/googleapis/python-automl/issues/338)) ([0cd309f](https://github.com/googleapis/python-automl/commit/0cd309f33520043227bfc31b6570ccc025c1b252))

## [2.7.0](https://github.com/googleapis/python-automl/compare/v2.6.0...v2.7.0) (2022-02-11)


### Features

* add api key support ([#327](https://github.com/googleapis/python-automl/issues/327)) ([74c9531](https://github.com/googleapis/python-automl/commit/74c95311107acc41c60585b98f1c68e750298e85))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([c23e512](https://github.com/googleapis/python-automl/commit/c23e512657baa61eafd1b99a1fd9398f2cf03103))

## [2.6.0](https://github.com/googleapis/python-automl/compare/v2.5.2...v2.6.0) (2022-01-15)


### Features

* publish updated protos for cloud/automl/v1 service  ([#318](https://github.com/googleapis/python-automl/issues/318)) ([3bf0271](https://github.com/googleapis/python-automl/commit/3bf0271dce60fe9843711068e85978b627f77db6))


### Bug Fixes

* **deps:** allow google-cloud-storage < 3.0.0dev ([#316](https://github.com/googleapis/python-automl/issues/316)) ([ba271a8](https://github.com/googleapis/python-automl/commit/ba271a8cfea916f7fb3df536258cda2dca32a423))

### [2.5.2](https://www.github.com/googleapis/python-automl/compare/v2.5.1...v2.5.2) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([e50d4c9](https://www.github.com/googleapis/python-automl/commit/e50d4c928601f6a32b22dcd36338e820254451d4))
* **deps:** require google-api-core >= 1.28.0 ([e50d4c9](https://www.github.com/googleapis/python-automl/commit/e50d4c928601f6a32b22dcd36338e820254451d4))


### Documentation

* list oneofs in docstring ([e50d4c9](https://www.github.com/googleapis/python-automl/commit/e50d4c928601f6a32b22dcd36338e820254451d4))

### [2.5.1](https://www.github.com/googleapis/python-automl/compare/v2.5.0...v2.5.1) (2021-10-20)


### Bug Fixes

* remove unnecessary double quotes in strings ([#262](https://www.github.com/googleapis/python-automl/issues/262)) ([fb73bd7](https://www.github.com/googleapis/python-automl/commit/fb73bd7d5ab024aaec3bb0d892c587082911970b))

## [2.5.0](https://www.github.com/googleapis/python-automl/compare/v2.4.2...v2.5.0) (2021-10-08)


### Features

* add context manager support in client ([#264](https://www.github.com/googleapis/python-automl/issues/264)) ([83b7a3d](https://www.github.com/googleapis/python-automl/commit/83b7a3dc757b6313861e40422f10ac8ad636cd5b))


### Bug Fixes

* add 'dict' annotation type to 'request' ([a97f88b](https://www.github.com/googleapis/python-automl/commit/a97f88b2b13beb53088f3b94be674f31a93957ed))
* flaky test, issue 223 ([#250](https://www.github.com/googleapis/python-automl/issues/250)) ([efb9d0b](https://www.github.com/googleapis/python-automl/commit/efb9d0b3eff27364764aa5d6dc7fa57c3d4825e5))
* improper types in pagers generation ([5ae7bcf](https://www.github.com/googleapis/python-automl/commit/5ae7bcf39d4cd2733f46c0f38a47f92e676cfa45))

### [2.4.2](https://www.github.com/googleapis/python-automl/compare/v2.4.1...v2.4.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#217](https://www.github.com/googleapis/python-automl/issues/217)) ([20a72aa](https://www.github.com/googleapis/python-automl/commit/20a72aa0524fabb855cfda8589dd3722e4c65bdd))


### [2.4.1](https://www.github.com/googleapis/python-automl/compare/v2.4.0...v2.4.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#209](https://www.github.com/googleapis/python-automl/issues/209)) ([2cf09fa](https://www.github.com/googleapis/python-automl/commit/2cf09fa43fa62c340bfea3998c41184e191cbf81))

## [2.4.0](https://www.github.com/googleapis/python-automl/compare/v2.3.0...v2.4.0) (2021-07-12)


### Features

* add always_use_jwt_access ([#175](https://www.github.com/googleapis/python-automl/issues/175)) ([7da3fc7](https://www.github.com/googleapis/python-automl/commit/7da3fc7b4a8e648afad733cb2ee4e1dbe74fb736))
* support self-signed JWT flow for service accounts ([bfece77](https://www.github.com/googleapis/python-automl/commit/bfece7799fe6cf803d650c26e0d6e2a78e64f7c1))


### Bug Fixes

* add async client to %name_%version/init.py ([bfece77](https://www.github.com/googleapis/python-automl/commit/bfece7799fe6cf803d650c26e0d6e2a78e64f7c1))
* **deps:** add packaging requirement ([#162](https://www.github.com/googleapis/python-automl/issues/162)) ([dea0cc3](https://www.github.com/googleapis/python-automl/commit/dea0cc37794c57a4b0521c039dc251becf694021))
* disable always_use_jwt_access ([160a7ad](https://www.github.com/googleapis/python-automl/commit/160a7adad3f2d53ca6f733a21e72bfe866a5ebc1))
* disable always_use_jwt_access ([#181](https://www.github.com/googleapis/python-automl/issues/181)) ([160a7ad](https://www.github.com/googleapis/python-automl/commit/160a7adad3f2d53ca6f733a21e72bfe866a5ebc1))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-automl/issues/1127)) ([#172](https://www.github.com/googleapis/python-automl/issues/172)) ([2489e39](https://www.github.com/googleapis/python-automl/commit/2489e397c1fc66d5dc360f150935673a25537c02)), closes [#1126](https://www.github.com/googleapis/python-automl/issues/1126)

## [2.3.0](https://www.github.com/googleapis/python-automl/compare/v2.2.0...v2.3.0) (2021-04-14)


### Features

* add `from_service_account_info` ([4f6f1d6](https://www.github.com/googleapis/python-automl/commit/4f6f1d6fde69bd97dce51a1007c482d843ca8b5d))


### Bug Fixes

* use correct retry deadlines ([#119](https://www.github.com/googleapis/python-automl/issues/119)) ([4f6f1d6](https://www.github.com/googleapis/python-automl/commit/4f6f1d6fde69bd97dce51a1007c482d843ca8b5d))


### Documentation

* re-publish tables client documentation ([#146](https://www.github.com/googleapis/python-automl/issues/146)) ([9f3e73a](https://www.github.com/googleapis/python-automl/commit/9f3e73a7e45088c929ae86b5b90f0e4f31a7b278))

## [2.2.0](https://www.github.com/googleapis/python-automl/compare/v2.1.0...v2.2.0) (2021-02-16)


### Features

* add support for common resource paths and expose the client transport ([#93](https://www.github.com/googleapis/python-automl/issues/93)) ([4c910d3](https://www.github.com/googleapis/python-automl/commit/4c910d37dd882d8d4248c1b3716213e9aacbf5df))


### Bug Fixes

* Pass the 'params' parameter to the underlying 'BatchPredictRequest' object in 'batch_predict()' method ([#110](https://www.github.com/googleapis/python-automl/issues/110)) ([b89fb00](https://www.github.com/googleapis/python-automl/commit/b89fb0070fd4eeb0306d8f584e31da9d8b3fa52c))
* remove gRPC send/recv limits; add enums to `types/__init__.py` ([#108](https://www.github.com/googleapis/python-automl/issues/108)) ([4a2e2cf](https://www.github.com/googleapis/python-automl/commit/4a2e2cf997fa0eaa87177a8e3ccbaded549b683e))

## [2.1.0](https://www.github.com/googleapis/python-automl/compare/v2.0.0...v2.1.0) (2020-10-27)


### Features

* add text extraction health care option in create model ([#86](https://www.github.com/googleapis/python-automl/issues/86)) ([0233804](https://www.github.com/googleapis/python-automl/commit/0233804885846295508a5fc98929dba598172244))

### Bug Fixes
* **v1beta1**: Rename message attributes that conflict with built-ins. `type` ->`type_`, `min` -> `min_`, `max` -> `max_`

### Documentation

* fix supported Python versions in README ([#70](https://www.github.com/googleapis/python-automl/issues/70)) ([fc0ca41](https://www.github.com/googleapis/python-automl/commit/fc0ca41594c6aa86ffe32dee7834d1526cad0aab))

## [2.0.0](https://www.github.com/googleapis/python-automl/compare/v1.0.1...v2.0.0) (2020-09-16)


### ⚠ BREAKING CHANGES

* move to microgen. See [Migration Guide](https://github.com/googleapis/python-automl/blob/release-v2.0.0/UPGRADING.md) (#61)

### Features

* move to microgen ([#61](https://www.github.com/googleapis/python-automl/issues/61)) ([009085e](https://www.github.com/googleapis/python-automl/commit/009085e0a82d1d7729349746c2c8954d5d60e0a9))


### Bug Fixes

* **translate:** fix a broken test [([#4360](https://www.github.com/googleapis/python-automl/issues/4360))](https://github.com/GoogleCloudPlatform/python-docs-samples/issues/4360) ([5f7d141](https://www.github.com/googleapis/python-automl/commit/5f7d141afe732acf7458a9ac98618e93baa93d38)), closes [#4353](https://www.github.com/googleapis/python-automl/issues/4353)
* `update_column_spec` typo in TablesClient docstring ([#18](https://www.github.com/googleapis/python-automl/issues/18)) ([9feb4cc](https://www.github.com/googleapis/python-automl/commit/9feb4cc5e04a01a4199da43400457cca6c0bfa05)), closes [#17](https://www.github.com/googleapis/python-automl/issues/17)
* update retry configs ([#44](https://www.github.com/googleapis/python-automl/issues/44)) ([7df9059](https://www.github.com/googleapis/python-automl/commit/7df905910b86721a6ee3a3b6c916a4f8e27d0aa7))


### Documentation

* add cancel operation sample ([abc5070](https://www.github.com/googleapis/python-automl/commit/abc507005d5255ed5adf2c4b8e0b23042a0bdf47))
* add samples from tables/automl ([#54](https://www.github.com/googleapis/python-automl/issues/54)) ([d225a5f](https://www.github.com/googleapis/python-automl/commit/d225a5f97c2823218b91a79e77d3383132875231)), closes [#2090](https://www.github.com/googleapis/python-automl/issues/2090) [#2100](https://www.github.com/googleapis/python-automl/issues/2100) [#2102](https://www.github.com/googleapis/python-automl/issues/2102) [#2103](https://www.github.com/googleapis/python-automl/issues/2103) [#2101](https://www.github.com/googleapis/python-automl/issues/2101) [#2110](https://www.github.com/googleapis/python-automl/issues/2110) [#2115](https://www.github.com/googleapis/python-automl/issues/2115) [#2150](https://www.github.com/googleapis/python-automl/issues/2150) [#2145](https://www.github.com/googleapis/python-automl/issues/2145) [#2203](https://www.github.com/googleapis/python-automl/issues/2203) [#2340](https://www.github.com/googleapis/python-automl/issues/2340) [#2337](https://www.github.com/googleapis/python-automl/issues/2337) [#2336](https://www.github.com/googleapis/python-automl/issues/2336) [#2339](https://www.github.com/googleapis/python-automl/issues/2339) [#2338](https://www.github.com/googleapis/python-automl/issues/2338) [#2276](https://www.github.com/googleapis/python-automl/issues/2276) [#2257](https://www.github.com/googleapis/python-automl/issues/2257) [#2424](https://www.github.com/googleapis/python-automl/issues/2424) [#2407](https://www.github.com/googleapis/python-automl/issues/2407) [#2501](https://www.github.com/googleapis/python-automl/issues/2501) [#2459](https://www.github.com/googleapis/python-automl/issues/2459) [#2601](https://www.github.com/googleapis/python-automl/issues/2601) [#2523](https://www.github.com/googleapis/python-automl/issues/2523) [#2005](https://www.github.com/googleapis/python-automl/issues/2005) [#3033](https://www.github.com/googleapis/python-automl/issues/3033) [#2806](https://www.github.com/googleapis/python-automl/issues/2806) [#3750](https://www.github.com/googleapis/python-automl/issues/3750) [#3571](https://www.github.com/googleapis/python-automl/issues/3571) [#3929](https://www.github.com/googleapis/python-automl/issues/3929) [#4022](https://www.github.com/googleapis/python-automl/issues/4022) [#4127](https://www.github.com/googleapis/python-automl/issues/4127)

### [1.0.1](https://www.github.com/googleapis/python-automl/compare/v1.0.0...v1.0.1) (2020-06-18)


### Bug Fixes

* fixes release status trove classifier ([#39](https://www.github.com/googleapis/python-automl/issues/39)) ([5b5d6c3](https://www.github.com/googleapis/python-automl/commit/5b5d6c33178f4f052cba01cc08cf3023d4303d7a))

## [1.0.0](https://www.github.com/googleapis/python-automl/compare/v0.10.0...v1.0.0) (2020-06-18)


### Features

* release as production/stable ([#37](https://www.github.com/googleapis/python-automl/issues/37)) ([915c502](https://www.github.com/googleapis/python-automl/commit/915c5029a8c342871738b24395534fdaebb681bc))


### Bug Fixes

* make TablesClient.predict permissive to input data types ([#13](https://www.github.com/googleapis/python-automl/issues/13)) ([ddc9f71](https://www.github.com/googleapis/python-automl/commit/ddc9f7106eab91d4adea2db65e69e3a870a7cd46))

## [0.10.0](https://www.github.com/googleapis/python-automl/compare/v0.9.0...v0.10.0) (2020-01-31)


### Features

* **automl:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10037](https://www.github.com/googleapis/python-automl/issues/10037)) ([763a961](https://www.github.com/googleapis/python-automl/commit/763a9611d45d86b6024bcd74dfb8e93099a3f9e0))


### Bug Fixes

* **automl:** fix TablesClient.predict for array and struct ([#9991](https://www.github.com/googleapis/python-automl/issues/9991)) ([39f6f2a](https://www.github.com/googleapis/python-automl/commit/39f6f2a5f59b7f61096fb3f43c05501ebc19f676)), closes [#9887](https://www.github.com/googleapis/python-automl/issues/9887)
* **automl:** fix TypeError when passing a client_info to automl TablesClient ([#9949](https://www.github.com/googleapis/python-automl/issues/9949)) ([75783ec](https://www.github.com/googleapis/python-automl/commit/75783ec359871957253797cdbaa25042c8c02284))

## 0.9.0

11-18-2019 09:49 PST

### Implementation Changes
- Change proto imports (via synth). ([#9817](https://github.com/googleapis/google-cloud-python/pull/9817))
- Pass params passed to `tables_client` to underlying client. ([#9794](https://github.com/googleapis/google-cloud-python/pull/9794))

### New Features
- Add support for `feature_importance` to `TablesClient`. ([#9816](https://github.com/googleapis/google-cloud-python/pull/9816))

### Documentation
- Fix typo in code example for AutoML Tables. ([#9806](https://github.com/googleapis/google-cloud-python/pull/9806))
- Update docs templates (via synth). ([#9797](https://github.com/googleapis/google-cloud-python/pull/9797))

## 0.8.0

11-13-2019 13:44 PST

### Implementation Changes
- Fix uploading pandas dataframe to AutoML Tables. ([#9647](https://github.com/googleapis/google-cloud-python/pull/9647))

### New Features
- Add support for image classification, image object detection, text classification, text extraction. (via synth). ([#9628](https://github.com/googleapis/google-cloud-python/pull/9628))
- Add `batch_predict`. (via synth). ([#9628](https://github.com/googleapis/google-cloud-python/pull/9628))
- Add `deploy_model`, `undeploy_model`, `export_model`. (via synth). ([#9628](https://github.com/googleapis/google-cloud-python/pull/9628))
- Add annotation specs (via synth). ([#9628](https://github.com/googleapis/google-cloud-python/pull/9628))
- Expose `disable_early_stopping` option for `create_model`. ([#9779](https://github.com/googleapis/google-cloud-python/pull/9779))

### Documentation
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

### Internal / Testing Changes
- Normalize VPCSC configuration in systests. ([#9607](https://github.com/googleapis/google-cloud-python/pull/9607))
- Fix docstring formatting. ([#9793](https://github.com/googleapis/google-cloud-python/pull/9793))

## 0.7.1

10-29-2019 13:45 PDT


### Implementation Changes
- Pass credentials to underlying clients in TableClient ([#9491](https://github.com/googleapis/google-cloud-python/pull/9491))

## 0.7.0

10-04-2019 15:37 PDT

### Implementation Changes
-  Return operation future from `AutoMlClient.create_dataset` (via synth).([#9423](https://github.com/googleapis/google-cloud-python/pull/9423))


### New Features
- Add support for V1 API (via synth). ([#9388](https://github.com/googleapis/google-cloud-python/pull/9388))
- Add support for passing  project to 'GcsClient'. ([#9299](https://github.com/googleapis/google-cloud-python/pull/9299))

## 0.6.0

09-30-2019 10:40 PDT

### New Features
- Add 'image_classification_model_deployment_metadata' arg to 'AutoMlClient.deploy_model' (via synth). ([#9291](https://github.com/googleapis/google-cloud-python/pull/9291))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))

### Internal / Testing Changes
- Preserve GcsClient, 'pandas' extras in testing (via synth). ([#9179](https://github.com/googleapis/google-cloud-python/pull/9179))

## 0.5.0

08-28-2019 14:07 PDT

### Implementation Changes
- Catch exceptions in GcsClient when a same name bucket already exists in a different project ([#9139](https://github.com/googleapis/google-cloud-python/pull/9139))
- Log when LROs are kicked off. ([#9058](https://github.com/googleapis/google-cloud-python/pull/9058))
- Throw a ValueError when an ambiguous display_name is used ([#9089](https://github.com/googleapis/google-cloud-python/pull/9089))
- Remove send/recv msg size limit (via synth). ([#8944](https://github.com/googleapis/google-cloud-python/pull/8944))

### New Features
- Enable users to pass in Pandas Dataframe when calling import_data() and batch_predict() from AutoML Tables client ([#9116](https://github.com/googleapis/google-cloud-python/pull/9116))
- Add support for documents (via synth). ([#9039](https://github.com/googleapis/google-cloud-python/pull/9039))
- Add a TablesClient for automl-tables specific behavior. ([#8720](https://github.com/googleapis/google-cloud-python/pull/8720))
- Add 'ClassificationEvaluationMetrics.display_name'/'BatchPredictResult.metadata'/'TableSpec.valid_row_count' (via synth) ([#9004](https://github.com/googleapis/google-cloud-python/pull/9004))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Skip relevant system tests if in VPCSC ([#9111](https://github.com/googleapis/google-cloud-python/pull/9111))
- Fix synth replace to add TablesClient. ([#9033](https://github.com/googleapis/google-cloud-python/pull/9033))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.4.0

07-22-2019 17:39 PDT


### New Features
- Add support for 'TablesModelMetadata.{optimization_objective_recall_value,optimization_objective_precision_value}' (via synth). ([#8643](https://github.com/googleapis/google-cloud-python/pull/8643))
- Add 'client_options' support, update list method docstrings (via synth). ([#8533](https://github.com/googleapis/google-cloud-python/pull/8533))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version (via synth). ([#8573](https://github.com/googleapis/google-cloud-python/pull/8573))
- Update Ruby package name (via synth). ([#8485](https://github.com/googleapis/google-cloud-python/pull/8485))
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.3.0

06-20-2019 14:47 PDT


### New Features
- Add support for video object tracking (via synth). ([#8278](https://github.com/googleapis/google-cloud-python/pull/8278))

### Documentation
- Add proto files; add 'docs' session to 'nox'; update docstrings (via synth). ([#8029](https://github.com/googleapis/google-cloud-python/pull/8029))

### Internal / Testing Changes
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8233](https://github.com/googleapis/google-cloud-python/pull/8233))
- Fix coverage in 'types.py'. ([#8145](https://github.com/googleapis/google-cloud-python/pull/8145))
- Blacken noxfile.py, setup.py (via synth). ([#8115](https://github.com/googleapis/google-cloud-python/pull/8115))
- Add empty lines (via synth). ([#8048](https://github.com/googleapis/google-cloud-python/pull/8048))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))
- Include protos in synth. ([#8000](https://github.com/googleapis/google-cloud-python/pull/8000))

## 0.2.0

04-03-2019 09:16 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Sort generated classes (via synth). ([#7256](https://github.com/googleapis/google-cloud-python/pull/7256))
- Protoc-generated serialization update. ([#7074](https://github.com/googleapis/google-cloud-python/pull/7074))

### New Features
- Video Classification, Text Extraction, Text Sentiment, Tables support. ([#7650](https://github.com/googleapis/google-cloud-python/pull/7650))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- AutoML: pick up stub docstring fix in GAPIC generator. ([#6964](https://github.com/googleapis/google-cloud-python/pull/6964))

### Internal / Testing Changes
- Update copyright headers

## 0.1.2

12-17-2018 16:27 PST


### Implementation Changes
- Add protoc-generated descriptor changes from updated .proto files. ([#6899](https://github.com/googleapis/google-cloud-python/pull/6899))
- Import `iam.policy` from `google.api_core.iam.policy`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes in GAPIC generator. ([#6490](https://github.com/googleapis/google-cloud-python/pull/6490))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix client_info bug, update docstrings. ([#6404](https://github.com/googleapis/google-cloud-python/pull/6404))
- Re-generate library using automl/synth.py ([#5972](https://github.com/googleapis/google-cloud-python/pull/5972))
- Re-generate library using automl/synth.py ([#5946](https://github.com/googleapis/google-cloud-python/pull/5946))

### Dependencies
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Bump minimum `api_core`' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6005](https://github.com/googleapis/google-cloud-python/pull/6005))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack automl gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6561](https://github.com/googleapis/google-cloud-python/pull/6561))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.1.1

### Documentation
- Fix broken links (#5675)
- bad trove classifier (#5648)

## 0.1.0

### New Features
- Initial Release of AutoML v1beta1
