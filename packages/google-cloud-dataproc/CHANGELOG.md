# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dataproc/#history

## [4.0.3](https://github.com/googleapis/python-dataproc/compare/v4.0.2...v4.0.3) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#423](https://github.com/googleapis/python-dataproc/issues/423)) ([5d1a263](https://github.com/googleapis/python-dataproc/commit/5d1a263533c1812587a9668d6bd6d7d29ac82f2f))


### Documentation

* fix changelog header to consistent size ([#424](https://github.com/googleapis/python-dataproc/issues/424)) ([00162f0](https://github.com/googleapis/python-dataproc/commit/00162f07935cca365c41dcbf8be4e5a7681d680e))

## [4.0.2](https://github.com/googleapis/python-dataproc/compare/v4.0.1...v4.0.2) (2022-04-06)


### Bug Fixes

* resource quotas ([#377](https://github.com/googleapis/python-dataproc/issues/377)) ([122c2f7](https://github.com/googleapis/python-dataproc/commit/122c2f77a93228dda409a8fad22465f2d28c5e0d))
* updating submit_job_to_cluster.py ([#387](https://github.com/googleapis/python-dataproc/issues/387)) ([0719d2b](https://github.com/googleapis/python-dataproc/commit/0719d2b69661f9775c00a1fc0dade2e65b4e44e9))

## [4.0.1](https://github.com/googleapis/python-dataproc/compare/v4.0.0...v4.0.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#357](https://github.com/googleapis/python-dataproc/issues/357)) ([3c66f42](https://github.com/googleapis/python-dataproc/commit/3c66f4232d35f1e11807d29e169fe87e028c52eb))
* **deps:** require proto-plus>=1.15.0 ([3c66f42](https://github.com/googleapis/python-dataproc/commit/3c66f4232d35f1e11807d29e169fe87e028c52eb))

## [4.0.0](https://github.com/googleapis/python-dataproc/compare/v3.3.0...v4.0.0) (2022-02-26)


### ⚠ BREAKING CHANGES

* add support for Virtual Dataproc cluster running on GKE cluster (#344)

### Features

* add support for Virtual Dataproc cluster running on GKE cluster ([#344](https://github.com/googleapis/python-dataproc/issues/344)) ([116077b](https://github.com/googleapis/python-dataproc/commit/116077b45abaccb1814002284e05e34ef387e045))


### Bug Fixes

* move GkeClusterConfig to google.cloud.dataproc_v1.types.shared ([116077b](https://github.com/googleapis/python-dataproc/commit/116077b45abaccb1814002284e05e34ef387e045))
* remove namespaced_gke_deployment_target ([116077b](https://github.com/googleapis/python-dataproc/commit/116077b45abaccb1814002284e05e34ef387e045))

## [3.3.0](https://github.com/googleapis/python-dataproc/compare/v3.2.0...v3.3.0) (2022-02-18)


### Features

* add api key support ([#336](https://github.com/googleapis/python-dataproc/issues/336)) ([ac22d7e](https://github.com/googleapis/python-dataproc/commit/ac22d7ef7040e85035a8d3cfc9fe0f69a014f238))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([452460f](https://github.com/googleapis/python-dataproc/commit/452460fe8e6af9e1a99d9636c5531e489e1e4852))


### Documentation

* add generated snippets ([#342](https://github.com/googleapis/python-dataproc/issues/342)) ([98810a9](https://github.com/googleapis/python-dataproc/commit/98810a9bc7674ea81397823f5da871cd30adcbd7))

## [3.2.0](https://github.com/googleapis/python-dataproc/compare/v3.1.1...v3.2.0) (2022-01-17)


### Features

* add Spark runtime versioning for Spark batches ([#318](https://github.com/googleapis/python-dataproc/issues/318)) ([f2e35d9](https://github.com/googleapis/python-dataproc/commit/f2e35d9735cbd0dd5a0e32d78631d70820380846))
* auto-diagnostic of failed Spark batches ([f2e35d9](https://github.com/googleapis/python-dataproc/commit/f2e35d9735cbd0dd5a0e32d78631d70820380846))
* custom image containers for Spark batches ([f2e35d9](https://github.com/googleapis/python-dataproc/commit/f2e35d9735cbd0dd5a0e32d78631d70820380846))
* local SSD NVME interface support for GCE clusters ([f2e35d9](https://github.com/googleapis/python-dataproc/commit/f2e35d9735cbd0dd5a0e32d78631d70820380846))

## [3.1.1](https://www.github.com/googleapis/python-dataproc/compare/v3.1.0...v3.1.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([d4919c0](https://www.github.com/googleapis/python-dataproc/commit/d4919c029ad12b5ee44942b55c5560aaf441f5a9))
* **deps:** require google-api-core >= 1.28.0 ([d4919c0](https://www.github.com/googleapis/python-dataproc/commit/d4919c029ad12b5ee44942b55c5560aaf441f5a9))


### Documentation

* list oneofs in docstring ([d4919c0](https://www.github.com/googleapis/python-dataproc/commit/d4919c029ad12b5ee44942b55c5560aaf441f5a9))

## [3.1.0](https://www.github.com/googleapis/python-dataproc/compare/v3.0.0...v3.1.0) (2021-10-26)


### Features

* add context manager support in client ([#285](https://www.github.com/googleapis/python-dataproc/issues/285)) ([b54fb76](https://www.github.com/googleapis/python-dataproc/commit/b54fb7647deaea64fe6ad553514c9d0ad62a0cbc))
* add Dataproc Serverless for Spark Batches API ([#290](https://www.github.com/googleapis/python-dataproc/issues/290)) ([f0ed26c](https://www.github.com/googleapis/python-dataproc/commit/f0ed26c6ccd2e9f438d1d5f31c5512761b0e20b9))
* Add support for dataproc BatchController service ([#291](https://www.github.com/googleapis/python-dataproc/issues/291)) ([24a6f7d](https://www.github.com/googleapis/python-dataproc/commit/24a6f7defee1e0fd2d195f934c004769d8f1a2b7))
* add support for python 3.10 ([#289](https://www.github.com/googleapis/python-dataproc/issues/289)) ([229f919](https://www.github.com/googleapis/python-dataproc/commit/229f919e31c39bc028cd2e6062437b0a8d061556))

## [3.0.0](https://www.github.com/googleapis/python-dataproc/compare/v2.6.0...v3.0.0) (2021-10-04)


### Features

* delete deprecated Dataproc v1beta2 API client ([3bdeaa7](https://www.github.com/googleapis/python-dataproc/commit/3bdeaa7e707ec2af445bf7c0321959b927c9c245))


### Bug Fixes

* add 'dict' annotation type to 'request' ([be5c115](https://www.github.com/googleapis/python-dataproc/commit/be5c11554f7accfe60dd5cb8da7c4888f688c282))
* improper types in pagers generation ([1ae784b](https://www.github.com/googleapis/python-dataproc/commit/1ae784bc1610aeb389eaa2cc7a6dc6f10c96788b))


### Miscellaneous Chores

* release as 3.0.0 ([#273](https://www.github.com/googleapis/python-dataproc/issues/273)) ([3bdeaa7](https://www.github.com/googleapis/python-dataproc/commit/3bdeaa7e707ec2af445bf7c0321959b927c9c245))


### Documentation

* update cluster sample ([3bdeaa7](https://www.github.com/googleapis/python-dataproc/commit/3bdeaa7e707ec2af445bf7c0321959b927c9c245))

## [2.6.0](https://www.github.com/googleapis/python-dataproc/compare/v2.5.0...v2.6.0) (2021-09-21)


### Features

* delete deprecated Dataproc v1beta2 API client ([#253](https://www.github.com/googleapis/python-dataproc/issues/253)) ([b0db6da](https://www.github.com/googleapis/python-dataproc/commit/b0db6da6221ed37ab2d8903fff8befb788fa55d5))


### Documentation

* update cluster sample ([#218](https://www.github.com/googleapis/python-dataproc/issues/218)) ([80706f9](https://www.github.com/googleapis/python-dataproc/commit/80706f93b32007efe43ca4740a20f924fb6e9f54))

## [2.5.0](https://www.github.com/googleapis/python-dataproc/compare/v2.4.0...v2.5.0) (2021-07-24)


### Features

* add always_use_jwt_access ([#209](https://www.github.com/googleapis/python-dataproc/issues/209)) ([6aec13c](https://www.github.com/googleapis/python-dataproc/commit/6aec13ce39a2afc0f36878bd61cff1614ec66972))


### Bug Fixes

* Attribute error Name while executing the sample code ([#205](https://www.github.com/googleapis/python-dataproc/issues/205)) ([cb0328f](https://www.github.com/googleapis/python-dataproc/commit/cb0328f3bfec416be9aec34d027fe0f48aab4242))
* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#227](https://www.github.com/googleapis/python-dataproc/issues/227)) ([5acfcd0](https://www.github.com/googleapis/python-dataproc/commit/5acfcd019dede3684fdf23cbed8bfcebdce606af))
* disable always_use_jwt_access ([#215](https://www.github.com/googleapis/python-dataproc/issues/215)) ([a57e253](https://www.github.com/googleapis/python-dataproc/commit/a57e25388691335b6672613210ee566ed91dc97b))
* enable self signed jwt for grpc ([#233](https://www.github.com/googleapis/python-dataproc/issues/233)) ([7df4fef](https://www.github.com/googleapis/python-dataproc/commit/7df4fefdced730fffd9b994608575512efe8d72a))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-dataproc/issues/1127)) ([#201](https://www.github.com/googleapis/python-dataproc/issues/201)) ([feea064](https://www.github.com/googleapis/python-dataproc/commit/feea0642ea6dbd6e08d4e52c89789a6b17e4de97))
* add Samples section to CONTRIBUTING.rst ([#228](https://www.github.com/googleapis/python-dataproc/issues/228)) ([3e248c2](https://www.github.com/googleapis/python-dataproc/commit/3e248c29470d635abf0d6fa7ae84dc8370a86bef))


## [2.4.0](https://www.github.com/googleapis/python-dataproc/compare/v2.3.1...v2.4.0) (2021-05-20)


### Features

* add 'from_service_account_info' factory to clients ([6525f86](https://www.github.com/googleapis/python-dataproc/commit/6525f86b698242d77606cffb42713d18724a2526))
* support self-signed JWT flow for service accounts ([5137a6f](https://www.github.com/googleapis/python-dataproc/commit/5137a6fce856b22be884aae19ec814458fc4ce97))
* update the Dataproc V1 API client library ([5137a6f](https://www.github.com/googleapis/python-dataproc/commit/5137a6fce856b22be884aae19ec814458fc4ce97))


### Bug Fixes

* add async client to %name_%version/init.py ([5137a6f](https://www.github.com/googleapis/python-dataproc/commit/5137a6fce856b22be884aae19ec814458fc4ce97))
* fix sphinx identifiers ([6525f86](https://www.github.com/googleapis/python-dataproc/commit/6525f86b698242d77606cffb42713d18724a2526))
* use correct retry deadlines ([#122](https://www.github.com/googleapis/python-dataproc/issues/122)) ([6525f86](https://www.github.com/googleapis/python-dataproc/commit/6525f86b698242d77606cffb42713d18724a2526))

## [2.3.1](https://www.github.com/googleapis/python-dataproc/compare/v2.3.0...v2.3.1) (2021-03-27)


### Bug Fixes

* (samples) fixing samples for new machine types ([#150](https://www.github.com/googleapis/python-dataproc/issues/150)) ([3343665](https://www.github.com/googleapis/python-dataproc/commit/334366546501833149479556b55bfbc3c9562236))


### Documentation

* adding backoff to quickstart test ([#135](https://www.github.com/googleapis/python-dataproc/issues/135)) ([a22df4c](https://www.github.com/googleapis/python-dataproc/commit/a22df4c0a15b2fa51cbe0f0cc2782def1a74c198))

## [2.3.0](https://www.github.com/googleapis/python-dataproc/compare/v2.2.0...v2.3.0) (2021-03-01)


### Features

* **v1beta1:** BREAKING CHANGE: remove DOCKER/FLINK from Component enum; adds HBASE ([#108](https://www.github.com/googleapis/python-dataproc/issues/108)) ([ee093a8](https://www.github.com/googleapis/python-dataproc/commit/ee093a88841c7f9c9ea41b066993e56b4abe267d))


### Bug Fixes

* remove gRPC send/recv limits; expose client transport ([#117](https://www.github.com/googleapis/python-dataproc/issues/117)) ([6f27109](https://www.github.com/googleapis/python-dataproc/commit/6f27109faf03dd13f25294e57960f0d9e1a9fa27))

## [2.2.0](https://www.github.com/googleapis/python-dataproc/compare/v2.1.0...v2.2.0) (2020-11-16)


### Features

* add common resource paths, expose client transport ([#87](https://www.github.com/googleapis/python-dataproc/issues/87)) ([7ec92b7](https://www.github.com/googleapis/python-dataproc/commit/7ec92b71be9c1d0d305421bb1b1dce5d92377bba)), closes [/github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py#L27-L32](https://www.github.com/googleapis//github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py/issues/L27-L32) [#792](https://www.github.com/googleapis/python-dataproc/issues/792)

## [2.0.2](https://www.github.com/googleapis/python-dataproc/compare/v2.0.1...v2.0.2) (2020-09-16)


### Documentation

* add `submit_job` samples  ([#88](https://www.github.com/googleapis/python-dataproc/issues/88)) ([e7379b5](https://www.github.com/googleapis/python-dataproc/commit/e7379b5ab45a0c1e5b6944330c3e8ae4faa115e8))

## [2.0.1](https://www.github.com/googleapis/python-dataproc/compare/v2.0.0...v2.0.1) (2020-09-14)


### Documentation

* remove example usage from README ([#77](https://www.github.com/googleapis/python-dataproc/issues/77)) ([66c7af1](https://www.github.com/googleapis/python-dataproc/commit/66c7af157ca5f740ebfec95abb7267e361d855f6))

## [2.0.0](https://www.github.com/googleapis/python-dataproc/compare/v1.1.1...v2.0.0) (2020-08-10)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#71)

### Features

* migrate to use microgen ([#71](https://www.github.com/googleapis/python-dataproc/issues/71)) ([108d6ff](https://www.github.com/googleapis/python-dataproc/commit/108d6ff91c6442e743cdf449790f981709305a09))

## [1.1.1](https://www.github.com/googleapis/python-dataproc/compare/v1.1.0...v1.1.1) (2020-08-10)


### Documentation

* change relative URLs to absolute URLs to fix broken links ([#65](https://www.github.com/googleapis/python-dataproc/issues/65)) ([65c2771](https://www.github.com/googleapis/python-dataproc/commit/65c277120e136edd5648047fcb85f8d0cd104408))

## [1.1.0](https://www.github.com/googleapis/python-dataproc/compare/v1.0.1...v1.1.0) (2020-07-31)


### Features

* add support for temp_bucket, endpoint_config in clusters; add preemptibility for instance group configs ([#60](https://www.github.com/googleapis/python-dataproc/issues/60)) ([a80fc72](https://www.github.com/googleapis/python-dataproc/commit/a80fc727510c10c678caa125902c201c8280dcc1))

## [1.0.1](https://www.github.com/googleapis/python-dataproc/compare/v1.0.0...v1.0.1) (2020-07-16)


### Bug Fixes

* correct protobuf type for diagnose_cluster, update retry configs ([#55](https://www.github.com/googleapis/python-dataproc/issues/55)) ([822315e](https://www.github.com/googleapis/python-dataproc/commit/822315ec3f2517ebb6ca199b72156ebd50e0518b))

## [1.0.0](https://www.github.com/googleapis/python-dataproc/compare/v0.8.1...v1.0.0) (2020-06-17)


### Features

* release as production/stable ([#44](https://www.github.com/googleapis/python-dataproc/issues/44)) ([58f8c87](https://www.github.com/googleapis/python-dataproc/commit/58f8c87acc826e56b2e6271306c7a2078eed59ef))

## [0.8.1](https://www.github.com/googleapis/python-dataproc/compare/v0.8.0...v0.8.1) (2020-06-05)


### Bug Fixes

* increase timeout for `ClusterController` in v1 ([#36](https://www.github.com/googleapis/python-dataproc/issues/36)) ([3137bee](https://www.github.com/googleapis/python-dataproc/commit/3137bee846002fe6c1e40d410ed0310e3fe86c0c))

## [0.8.0](https://www.github.com/googleapis/python-dataproc/compare/v0.7.0...v0.8.0) (2020-05-19)


### Features

* add SparkR and Presto jobs to WorkflowTemplates; add new optional components; add submit_job_as_operation to v1 (via synth) ([#21](https://www.github.com/googleapis/python-dataproc/issues/21)) ([1cf10b6](https://www.github.com/googleapis/python-dataproc/commit/1cf10b6b127a63dbeb34958771c2cc8d8cb37099))

## [0.7.0](https://www.github.com/googleapis/python-dataproc/compare/v0.6.1...v0.7.0) (2020-03-05)


### Features

* add lifecycle config and reservation affinity support to v1 (via synth) ([#10](https://www.github.com/googleapis/python-dataproc/issues/10)) ([bb36194](https://www.github.com/googleapis/python-dataproc/commit/bb36194d4b0cfb6f2c5a0358625a17c629f71b21))

## 0.6.1

11-12-2019 08:24 PST

### Documentation
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

## 0.6.0

11-07-2019 16:34 PST


### Implementation Changes
- Tweak proto annotations (via synth). ([#9466](https://github.com/googleapis/google-cloud-python/pull/9466))
- Remove send/recv msg size limit (via synth). ([#8951](https://github.com/googleapis/google-cloud-python/pull/8951))

### New Features
- Add V1 autoscaling policy support; annotate protos (via synth). ([#9402](https://github.com/googleapis/google-cloud-python/pull/9402))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatibility badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.5.0

07-24-2019 16:02 PDT

### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8387](https://github.com/googleapis/google-cloud-python/pull/8387))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8505](https://github.com/googleapis/google-cloud-python/pull/8505))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version (via synth). ([#8579](https://github.com/googleapis/google-cloud-python/pull/8579))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8349](https://github.com/googleapis/google-cloud-python/pull/8349))
- Add disclaimer to auto-generated template files (via synth).  ([#8311](https://github.com/googleapis/google-cloud-python/pull/8311))
- Supress checking 'cov-fail-under' in nox default session (via synth). ([#8237](https://github.com/googleapis/google-cloud-python/pull/8237))

## 0.4.0

05-30-2019 05:52 PDT

### Implementation Changes
- Update docs/conf.py, add routing header to method metadata, fix docstrings (via synth). ([#7924](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7924))

### New Features
- Add new service features for v1, including autoscaling (via synth). ([#8152](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8152))
- Add new service features for v1beta2, including autoscaling (via synth). ([#8119](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8119))

### Documentation
- Add nox session `docs` ([#7429](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7429))
- Add clarifying comment to blacken nox target. ([#7388](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7388))

### Internal / Testing Changes
- Re-add import of 'operations.proto' to V1 'clusters.proto' (via synth). ([#8188](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8188))
- Add empty lines (via synth). ([#8054](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/8054))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7535))
- Copy lintified proto files (via synth). ([#7465](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/7465))

## 0.3.1

02-15-2019 12:36 PST


### Implementation Changes
- Remove unused message exports. ([#7266](https://github.com/googleapis/google-cloud-python/pull/7266))
- Protoc-generated serialization update.. ([#7079](https://github.com/googleapis/google-cloud-python/pull/7079))
- Trivial housekeeping change to .proto files. ([#7067](https://github.com/googleapis/google-cloud-python/pull/7067))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Pick up stub docstring fix in GAPIC generator. ([#6967](https://github.com/googleapis/google-cloud-python/pull/6967))

### Internal / Testing Changes
- Copy proto files alongside protoc versions.
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers

## 0.3.0

12-17-2018 18:20 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Update `cluster_controller_client` GAPIC config (via synth). ([#6659](https://github.com/googleapis/google-cloud-python/pull/6659))
- Add 'WorkflowTemplateServiceClient', optional args; update timeouts (via synth). ([#6655](https://github.com/googleapis/google-cloud-python/pull/6655))
- Pick up enum fixes in the GAPIC generator. ([#6609](https://github.com/googleapis/google-cloud-python/pull/6609))
- Pick up fixes in GAPIC generator. ([#6493](https://github.com/googleapis/google-cloud-python/pull/6493))
- Fix client_info bug, update docstrings. ([#6408](https://github.com/googleapis/google-cloud-python/pull/6408))
- Re-generate library using dataproc/synth.py ([#6056](https://github.com/googleapis/google-cloud-python/pull/6056))
- Re-generate library using dataproc/synth.py ([#5975](https://github.com/googleapis/google-cloud-python/pull/5975))
- Re-generate library using dataproc/synth.py ([#5949](https://github.com/googleapis/google-cloud-python/pull/5949))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Update Dataproc docs URL ([#6455](https://github.com/googleapis/google-cloud-python/pull/6455))
- Docs: fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Dataproc: harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6019](https://github.com/googleapis/google-cloud-python/pull/6019))

### Internal / Testing Changes
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack dataproc gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add synth metadata. ([#6563](https://github.com/googleapis/google-cloud-python/pull/6563))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.2.0

### New Features
- Regenerate v1 endpoint. Add v1beta2 endpoint (#5717)

## 0.1.2

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Re-enable lint for tests, remove usage of pylint (#4921)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
