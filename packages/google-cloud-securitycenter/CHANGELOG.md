# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-securitycenter/#history

## [1.11.1](https://github.com/googleapis/python-securitycenter/compare/v1.11.0...v1.11.1) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#336](https://github.com/googleapis/python-securitycenter/issues/336)) ([b02e931](https://github.com/googleapis/python-securitycenter/commit/b02e93180914e21d0c0359a298f80c9bf6f22af0))


### Documentation

* fix changelog header to consistent size ([#338](https://github.com/googleapis/python-securitycenter/issues/338)) ([60c8d5f](https://github.com/googleapis/python-securitycenter/commit/60c8d5f8010e81f90dd6291ac2e4ba505aa8085a))

## [1.11.0](https://github.com/googleapis/python-securitycenter/compare/v1.10.0...v1.11.0) (2022-04-28)


### Features

* Add connection and description field to finding's list of attributes ([#323](https://github.com/googleapis/python-securitycenter/issues/323)) ([3a9e9bd](https://github.com/googleapis/python-securitycenter/commit/3a9e9bd2a622f6fab30c21b4cd5b918d1a1d27a1))
* Add next_steps field to finding's list of attributes ([#319](https://github.com/googleapis/python-securitycenter/issues/319)) ([35ab26e](https://github.com/googleapis/python-securitycenter/commit/35ab26ec21652af1f9d71e8e00f395020e716fcd))
* AuditConfig for IAM v1 ([35ab26e](https://github.com/googleapis/python-securitycenter/commit/35ab26ec21652af1f9d71e8e00f395020e716fcd))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([35ab26e](https://github.com/googleapis/python-securitycenter/commit/35ab26ec21652af1f9d71e8e00f395020e716fcd))


### Documentation

* fix type in docstring for map fields ([35ab26e](https://github.com/googleapis/python-securitycenter/commit/35ab26ec21652af1f9d71e8e00f395020e716fcd))
* **samples:** add bigquery export samples ([#315](https://github.com/googleapis/python-securitycenter/issues/315)) ([beec49d](https://github.com/googleapis/python-securitycenter/commit/beec49d6e1228c8a9f1c0ecfd3573cf08d1990ec))
* **samples:** added mute config samples ([#276](https://github.com/googleapis/python-securitycenter/issues/276)) ([3ac8eac](https://github.com/googleapis/python-securitycenter/commit/3ac8eac8ad53ed83097bcd66e27d039eccedaa58))
* **samples:** included snippet for unmute finding ([#308](https://github.com/googleapis/python-securitycenter/issues/308)) ([fe05cc3](https://github.com/googleapis/python-securitycenter/commit/fe05cc3f23f792c1060f28cc77495a50be4ccde0))

## [1.10.0](https://github.com/googleapis/python-securitycenter/compare/v1.9.0...v1.10.0) (2022-03-05)


### Features

* Add BigQuery export APIs ([#289](https://github.com/googleapis/python-securitycenter/issues/289)) ([0a29512](https://github.com/googleapis/python-securitycenter/commit/0a29512a1b1e22a2205311a39f40759bfeafe468))


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#293](https://github.com/googleapis/python-securitycenter/issues/293)) ([ae90fee](https://github.com/googleapis/python-securitycenter/commit/ae90feee4d04057b505b8dda7cd0b4c99b22e530))
* **deps:** require proto-plus>=1.15.0 ([ae90fee](https://github.com/googleapis/python-securitycenter/commit/ae90feee4d04057b505b8dda7cd0b4c99b22e530))

## [1.9.0](https://github.com/googleapis/python-securitycenter/compare/v1.8.0...v1.9.0) (2022-02-26)


### Features

* add access field in the v1 finding proto ([#279](https://github.com/googleapis/python-securitycenter/issues/279)) ([7fdd2a8](https://github.com/googleapis/python-securitycenter/commit/7fdd2a8013ad610d1e836f1327889ff187930e9d))
* add api key support ([#273](https://github.com/googleapis/python-securitycenter/issues/273)) ([96e1e0c](https://github.com/googleapis/python-securitycenter/commit/96e1e0c752f62faf4898f60e269dbbbb0d37887f))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([7fdd2a8](https://github.com/googleapis/python-securitycenter/commit/7fdd2a8013ad610d1e836f1327889ff187930e9d))


### Documentation

* added more clarification around what event_time means on a v1 finding ([7fdd2a8](https://github.com/googleapis/python-securitycenter/commit/7fdd2a8013ad610d1e836f1327889ff187930e9d))
* Update documentation for the Finding resource field "project_display_name" ([#282](https://github.com/googleapis/python-securitycenter/issues/282)) ([5e02432](https://github.com/googleapis/python-securitycenter/commit/5e02432f489f00d9f136cf6b86c159db8d1cd120))
* Update documentation for the Mute fields on Findings ([5e02432](https://github.com/googleapis/python-securitycenter/commit/5e02432f489f00d9f136cf6b86c159db8d1cd120))

## [1.8.0](https://github.com/googleapis/python-securitycenter/compare/v1.7.0...v1.8.0) (2022-01-14)


### Features

* add display_name to the resource which is surfaced in NotificationMessage ([f28a8fe](https://github.com/googleapis/python-securitycenter/commit/f28a8fe8a3732e327543255475cef997ffbfaba9))
* add support for python 3.10 ([#238](https://github.com/googleapis/python-securitycenter/issues/238)) ([7186526](https://github.com/googleapis/python-securitycenter/commit/718652639dafd4121391c642d55d9347c66bf5cb))
* Added a new API method UpdateExternalSystem ([#256](https://github.com/googleapis/python-securitycenter/issues/256)) ([8c988a6](https://github.com/googleapis/python-securitycenter/commit/8c988a6bb1f2d0814386916c51c64fb8c4c15345))
* Added mute related APIs, proto messages and fields ([#255](https://github.com/googleapis/python-securitycenter/issues/255)) ([6f3e1b2](https://github.com/googleapis/python-securitycenter/commit/6f3e1b2503906dd5f9583ac37ebdd1d9e4f11dd2))
* Added resource type and display_name field to the FindingResult ([#248](https://github.com/googleapis/python-securitycenter/issues/248)) ([f28a8fe](https://github.com/googleapis/python-securitycenter/commit/f28a8fe8a3732e327543255475cef997ffbfaba9))


### Bug Fixes

* **deps:** drop packaging dependency ([f28a8fe](https://github.com/googleapis/python-securitycenter/commit/f28a8fe8a3732e327543255475cef997ffbfaba9))
* **deps:** require google-api-core >= 1.28.0 ([f28a8fe](https://github.com/googleapis/python-securitycenter/commit/f28a8fe8a3732e327543255475cef997ffbfaba9))
* fix extras_require typo in setup.py ([#242](https://github.com/googleapis/python-securitycenter/issues/242)) ([d477b96](https://github.com/googleapis/python-securitycenter/commit/d477b96c4de26adc282b41c16240fe0e38689320))

## [1.7.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.6.0...v1.7.0) (2021-10-08)


### Features

* Added type field to the resource which is surfaced in NotificationMessage ([a233f7a](https://www.github.com/googleapis/python-securitycenter/commit/a233f7a0d85ba1a2932a1ee8305e48eda5aafa75))
* Added vulnerability field to Finding ([#235](https://www.github.com/googleapis/python-securitycenter/issues/235)) ([a233f7a](https://www.github.com/googleapis/python-securitycenter/commit/a233f7a0d85ba1a2932a1ee8305e48eda5aafa75))

## [1.6.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.5.2...v1.6.0) (2021-10-07)


### Features

* add context manager support in client ([#230](https://www.github.com/googleapis/python-securitycenter/issues/230)) ([740af33](https://www.github.com/googleapis/python-securitycenter/commit/740af33ce79a027c5592aabadb58cc367461d6ec))

## [1.5.2](https://www.github.com/googleapis/python-securitycenter/compare/v1.5.1...v1.5.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([cd17b59](https://www.github.com/googleapis/python-securitycenter/commit/cd17b5935c330d063ffe05d444ccd68b73b50bd3))

## [1.5.1](https://www.github.com/googleapis/python-securitycenter/compare/v1.5.0...v1.5.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([00fb3d3](https://www.github.com/googleapis/python-securitycenter/commit/00fb3d397d604977ef0dc32305ba27158d87f4bc))

## [1.5.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.4.0...v1.5.0) (2021-07-28)


### Features

* add finding_class and indicator fields in Finding ([#201](https://www.github.com/googleapis/python-securitycenter/issues/201)) ([4af011d](https://www.github.com/googleapis/python-securitycenter/commit/4af011d96bd84692a1474018675dcd616a1592bd))


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#194](https://www.github.com/googleapis/python-securitycenter/issues/194)) ([37af051](https://www.github.com/googleapis/python-securitycenter/commit/37af0515bbb5b9de9719baf3ff5bc5e51df0cb58))
* enable self signed jwt for grpc ([#199](https://www.github.com/googleapis/python-securitycenter/issues/199)) ([a00be7c](https://www.github.com/googleapis/python-securitycenter/commit/a00be7c6dd09f64a3def127cbe963abab939b464))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#195](https://www.github.com/googleapis/python-securitycenter/issues/195)) ([8f402c2](https://www.github.com/googleapis/python-securitycenter/commit/8f402c29d026132fdae448c1835b4da4dda4d186))



## [1.4.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.3.1...v1.4.0) (2021-07-12)


### Features

* add always_use_jwt_access ([#170](https://www.github.com/googleapis/python-securitycenter/issues/170)) ([421b7fc](https://www.github.com/googleapis/python-securitycenter/commit/421b7fc0ffcae152cc329a064d7e233f91a5775d))


### Bug Fixes

* disable always_use_jwt_access ([#174](https://www.github.com/googleapis/python-securitycenter/issues/174)) ([5431e8b](https://www.github.com/googleapis/python-securitycenter/commit/5431e8b61616d044288b10ca1c244210aa717124))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-securitycenter/issues/1127)) ([#164](https://www.github.com/googleapis/python-securitycenter/issues/164)) ([42a2f11](https://www.github.com/googleapis/python-securitycenter/commit/42a2f1175d022174c45f04726072935b8738e111)), closes [#1126](https://www.github.com/googleapis/python-securitycenter/issues/1126)

## [1.3.1](https://www.github.com/googleapis/python-securitycenter/compare/v1.3.0...v1.3.1) (2021-06-10)


### Documentation

* update currently supported Finding filter fields ([#159](https://www.github.com/googleapis/python-securitycenter/issues/159)) ([89ca24b](https://www.github.com/googleapis/python-securitycenter/commit/89ca24b49c93737569b428dd7ca883de6429a41c))

## [1.3.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.2.0...v1.3.0) (2021-05-28)


### Features

* bump release level to production/stable ([#147](https://www.github.com/googleapis/python-securitycenter/issues/147)) ([b9c892a](https://www.github.com/googleapis/python-securitycenter/commit/b9c892a16c15e89ca67687ce3a6b64490fc61c6f))


### Documentation

* remove unused region tags ([#108](https://www.github.com/googleapis/python-securitycenter/issues/108)) ([a983668](https://www.github.com/googleapis/python-securitycenter/commit/a9836680db5ca69ee8e3983dbf5a03414397e850))

## [1.2.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.1.0...v1.2.0) (2021-05-19)


### Features

* add canonical_name and folder fields ([16a33f4](https://www.github.com/googleapis/python-securitycenter/commit/16a33f4c994b80d9c50537f2e1299282d525171e))
* support self-signed JWT flow for service accounts ([16a33f4](https://www.github.com/googleapis/python-securitycenter/commit/16a33f4c994b80d9c50537f2e1299282d525171e))


### Bug Fixes

* add async client to %name_%version/init.py ([16a33f4](https://www.github.com/googleapis/python-securitycenter/commit/16a33f4c994b80d9c50537f2e1299282d525171e))
* fix retry deadlines ([#116](https://www.github.com/googleapis/python-securitycenter/issues/116)) ([15c28e8](https://www.github.com/googleapis/python-securitycenter/commit/15c28e88f5b52a6e4f608198446b0753bf48734e))


### Documentation

* Fix conflict tag introduced in PR 104 ([#106](https://www.github.com/googleapis/python-securitycenter/issues/106)) ([f4f14ee](https://www.github.com/googleapis/python-securitycenter/commit/f4f14ee32602aad7b7a4837e330919b4276d7b18))
* standardize new tag with existing tags from other languages ([#104](https://www.github.com/googleapis/python-securitycenter/issues/104)) ([55582ac](https://www.github.com/googleapis/python-securitycenter/commit/55582acd814f7cd290580d5caa531725d2ff58b8))

## [1.1.0](https://www.github.com/googleapis/python-securitycenter/compare/v1.0.0...v1.1.0) (2020-12-15)


### Features

* **v1:** add field severity to findings; add common resource helper; expose client tranport ([#87](https://www.github.com/googleapis/python-securitycenter/issues/87)) ([e28b8e2](https://www.github.com/googleapis/python-securitycenter/commit/e28b8e24ac8a01a3db95decf21a635b046ecce97)), closes [/github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py#L27-L32](https://www.github.com/googleapis//github.com/googleapis/python-talent/blob/ef045e8eb348db36d7a2a611e6f26b11530d273b/samples/snippets/noxfile_config.py/issues/L27-L32)


### Documentation

* add securitycenter prefix to samples, wrap published samples and repl… ([#85](https://www.github.com/googleapis/python-securitycenter/issues/85)) ([553dfbb](https://www.github.com/googleapis/python-securitycenter/commit/553dfbb89f7e72ad280aaa5d59cc4a054aa1948e))
* update documentation on severity ([#72](https://www.github.com/googleapis/python-securitycenter/issues/72)) ([4ba96b2](https://www.github.com/googleapis/python-securitycenter/commit/4ba96b268d92eb57b816593b1fb968f269ed188e))
* update snippets_findings tags ([#78](https://www.github.com/googleapis/python-securitycenter/issues/78)) ([c7e301f](https://www.github.com/googleapis/python-securitycenter/commit/c7e301f0d45d2e3d04263df63a515b52ce0391b3))
* update snippets_list_assets tags ([#77](https://www.github.com/googleapis/python-securitycenter/issues/77)) ([11aef56](https://www.github.com/googleapis/python-securitycenter/commit/11aef56a0a9cf281e0d647d64d72c921e4b837d0))

## [1.0.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.7.1...v1.0.0) (2020-10-08)


### ⚠ BREAKING CHANGES

* generate with microgenerator. See [Migration Guide](https://github.com/googleapis/python-securitycenter/blob/main/UPGRADING.md)(#49)

### Features

* generate with microgenerator ([#49](https://www.github.com/googleapis/python-securitycenter/issues/49)) ([838dbc8](https://www.github.com/googleapis/python-securitycenter/commit/838dbc8445046b755b775f96f654944ecb707e35))

## [0.7.1](https://www.github.com/googleapis/python-securitycenter/compare/v0.7.0...v0.7.1) (2020-09-18)


### Bug Fixes

* **sample:** fix a broken test ([#63](https://www.github.com/googleapis/python-securitycenter/issues/63)) ([7062b1c](https://www.github.com/googleapis/python-securitycenter/commit/7062b1c18a6f787275b325d2a7713cf0b2627094)), closes [#59](https://www.github.com/googleapis/python-securitycenter/issues/59)

## [0.7.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.6.0...v0.7.0) (2020-09-10)


### Features

* add field severity to findings; update retry configs ([#53](https://www.github.com/googleapis/python-securitycenter/issues/53)) ([80494a9](https://www.github.com/googleapis/python-securitycenter/commit/80494a915ca33d260862694be889b817869ff01a))


### Documentation

* Update Security Command Center UpdateNotificationConfig sample, adding filter to mutable field ([#39](https://www.github.com/googleapis/python-securitycenter/issues/39)) ([c70d790](https://www.github.com/googleapis/python-securitycenter/commit/c70d7904425ae5ac252ffa7317ec6d08234a6c27))

## [0.6.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.5.0...v0.6.0) (2020-07-01)


### Features

* add `security_marks_path` method; fix docstring links (via synth) ([#24](https://www.github.com/googleapis/python-securitycenter/issues/24)) ([80ce6e6](https://www.github.com/googleapis/python-securitycenter/commit/80ce6e6128abf106ef7c3631a426f99440a406d9))
* add Resource to the v1 NotificationMessage ([#33](https://www.github.com/googleapis/python-securitycenter/issues/33)) ([c930e6a](https://www.github.com/googleapis/python-securitycenter/commit/c930e6afc6aa701761f9966e1391ca2d3ebb30f4))


### Documentation

* Update notification samples to v1 ([#19](https://www.github.com/googleapis/python-securitycenter/issues/19)) ([5eba984](https://www.github.com/googleapis/python-securitycenter/commit/5eba984eefefd3d689d84d14a8078c28914307c8))

## [0.5.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.4.0...v0.5.0) (2020-03-10)


### Features

* add support for notification configs to v1 ([#15](https://www.github.com/googleapis/python-securitycenter/issues/15)) ([9720fa4](https://www.github.com/googleapis/python-securitycenter/commit/9720fa44dc6e785c60ee9af555b5fea0564f34e0))

## [0.4.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.3.0...v0.4.0) (2020-02-13)


### Features

* add v1p1beta1; add `resource_display_name, `resource_parent_display_name`, `resource_project_display_name` to `v1.Asset.SecurityCenterProperties`; add output only field `resource` to `v1.ListFindingsResponse.ListFindingsResult`; increase `initial_rpc_timeout_millis` in default config for v1; standardize use of 'required' and 'optional' in docstrings; add 2.7 deprecation warning; bump copyright year to 2020 ([#7](https://www.github.com/googleapis/python-securitycenter/issues/7)) ([03e172b](https://www.github.com/googleapis/python-securitycenter/commit/03e172b34c7cf9a92de10085f4f040cd0e5e85eb))

## 0.3.0

07-24-2019 17:29 PDT

### Implementation Changes
- Allow kwargs to be passed to create_channel, update templates (via synth). ([#8402](https://github.com/googleapis/google-cloud-python/pull/8402))
- Update return type of run_asset_discovery (via synth). ([#8032](https://github.com/googleapis/google-cloud-python/pull/8032))
- Security Center: Add routing header to method metadata (via synth). ([#7589](https://github.com/googleapis/google-cloud-python/pull/7589))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8658](https://github.com/googleapis/google-cloud-python/pull/8658))
- Add 'client_options' support, update list method docstrings (via synth). ([#8521](https://github.com/googleapis/google-cloud-python/pull/8521))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Update docstrings (via synth). ([#8711](https://github.com/googleapis/google-cloud-python/pull/8711))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Docstring changes (via synth). ([#7704](https://github.com/googleapis/google-cloud-python/pull/7704))
- Add Snippets for security center list_assets call ([#7538](https://github.com/googleapis/google-cloud-python/pull/7538))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8362](https://github.com/googleapis/google-cloud-python/pull/8362))
- Add disclaimer to auto-generated template files (via synth).([#8326](https://github.com/googleapis/google-cloud-python/pull/8326))
- Fix coverage in 'types.py' (via synth). ([#8163](https://github.com/googleapis/google-cloud-python/pull/8163))
- Add empty lines (via synth). ([#8070](https://github.com/googleapis/google-cloud-python/pull/8070))
- Add nox session `docs`, reorder methods (via synth). ([#7780](https://github.com/googleapis/google-cloud-python/pull/7780))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))
- Add Ruby package configuration in protos (via synth). ([#7741](https://github.com/googleapis/google-cloud-python/pull/7741))
- proto file housekeeping FBO PHP (via synth).

## 0.2.0

03-12-2019 17:09 PDT


### Implementation Changes
- Remove 'having' filter arguments from query methods (via synth). [#7511](https://github.com/googleapis/google-cloud-python/pull/7511))
- Remove unused message exports. ([#7274](https://github.com/googleapis/google-cloud-python/pull/7274))
- Trivial gapic-generator change. ([#7233](https://github.com/googleapis/google-cloud-python/pull/7233))
- Protoc-generated serialization update, docstring tweak. ([#7094](https://github.com/googleapis/google-cloud-python/pull/7094))

### New Features
- Add support for `v1` API. ([#7495](https://github.com/googleapis/google-cloud-python/pull/7495))

### Documentation
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Docstring update from .proto file. ([#7056](https://github.com/googleapis/google-cloud-python/pull/7056))
- Fix 404 for 'Client Library Documentation' link. ([#7041](https://github.com/googleapis/google-cloud-python/pull/7041))
- Pick up stub docstring fix in GAPIC generator. ([#6981](https://github.com/googleapis/google-cloud-python/pull/6981))

### Internal / Testing Changes
- Proto file housekeeping FBO C# (via synth). ([#7502](https://github.com/googleapis/google-cloud-python/pull/7502))
- Copy lintified proto files (via synth). ([#7470](https://github.com/googleapis/google-cloud-python/pull/7470))
- Add clarifying comment to blacken nox target. ([#7402](https://github.com/googleapis/google-cloud-python/pull/7402))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.1

12-18-2018 09:45 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up changes to GAPIC generator. ([#6506](https://github.com/googleapis/google-cloud-python/pull/6506))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings via synth. ([#6438](https://github.com/googleapis/google-cloud-python/pull/6438))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docstring changes via synth. ([#6473](https://github.com/googleapis/google-cloud-python/pull/6473))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Overlooked synth changes. ([#6439](https://github.com/googleapis/google-cloud-python/pull/6439))

## 0.1.0

11-01-2018 15:12 PDT

### New Features
- Generate Security Center Client Library ([#6356](https://github.com/googleapis/google-cloud-python/pull/6356))
