# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-monitoring/#history

## [2.9.2](https://github.com/googleapis/python-monitoring/compare/v2.9.1...v2.9.2) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#441](https://github.com/googleapis/python-monitoring/issues/441)) ([87a8660](https://github.com/googleapis/python-monitoring/commit/87a8660538bfeac00eedadf2be17633ffe370f22))


### Documentation

* fix changelog header to consistent size ([#439](https://github.com/googleapis/python-monitoring/issues/439)) ([ce27cb4](https://github.com/googleapis/python-monitoring/commit/ce27cb462c4ae74572015f027c9b4b0cd44d069d))

## [2.9.1](https://github.com/googleapis/python-monitoring/compare/v2.9.0...v2.9.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#286](https://github.com/googleapis/python-monitoring/issues/286)) ([e77a5cd](https://github.com/googleapis/python-monitoring/commit/e77a5cd8b8a6c928faedd52a31b76ec6e645403c))

## [2.9.0](https://github.com/googleapis/python-monitoring/compare/v2.8.0...v2.9.0) (2022-02-26)


### Features

* add api key support ([#270](https://github.com/googleapis/python-monitoring/issues/270)) ([412b9fc](https://github.com/googleapis/python-monitoring/commit/412b9fc844b8be1a5c763c02a244c2cbecb8091d))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([c58bcce](https://github.com/googleapis/python-monitoring/commit/c58bcce924ff8603bc5596f5c7dc5afd0517216f))


### Documentation

* add generated snippets ([#276](https://github.com/googleapis/python-monitoring/issues/276)) ([2340cc9](https://github.com/googleapis/python-monitoring/commit/2340cc959bbde2de885f2fce9b36cfc884a1341e))

## [2.8.0](https://www.github.com/googleapis/python-monitoring/compare/v2.7.0...v2.8.0) (2021-11-16)


### Features

* Added support for auto-close configurations ([#253](https://www.github.com/googleapis/python-monitoring/issues/253)) ([0541c7a](https://www.github.com/googleapis/python-monitoring/commit/0541c7acc69465030077b5ce3b1d9c40cea7b634))

## [2.7.0](https://www.github.com/googleapis/python-monitoring/compare/v2.6.0...v2.7.0) (2021-11-09)


### Features

* add CreateServiceTimeSeries RPC ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))


### Bug Fixes

* **deps:** drop packaging dependency ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))
* **deps:** require google-api-core >= 1.28.0 ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))
* Reintroduce deprecated field/enum `ServiceTier` for backward compatibility ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))


### Miscellaneous Chores

* release as 2.7.0 ([#247](https://www.github.com/googleapis/python-monitoring/issues/247)) ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))


### Documentation

* list oneofs in docstring ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))
* Use absolute link targets in comments ([b347e70](https://www.github.com/googleapis/python-monitoring/commit/b347e7083ff04c04e287b7afc79c425a1d04f731))

## [2.6.0](https://www.github.com/googleapis/python-monitoring/compare/v2.5.2...v2.6.0) (2021-11-01)


### Features

* add context manager support in client ([#230](https://www.github.com/googleapis/python-monitoring/issues/230)) ([954dd18](https://www.github.com/googleapis/python-monitoring/commit/954dd18966520dbc623470ef528166d83d3e19ba))
* add CreateServiceTimeSeries RPC ([#235](https://www.github.com/googleapis/python-monitoring/issues/235)) ([2970b22](https://www.github.com/googleapis/python-monitoring/commit/2970b22ca5b4959ee1d3e1e883cdb00951e3917f))


### Bug Fixes

* **deps:** drop packaging dependency ([22d4eab](https://www.github.com/googleapis/python-monitoring/commit/22d4eabbafbdc16b0f4faf66f966442691de7666))
* **deps:** require google-api-core >= 1.28.0 ([22d4eab](https://www.github.com/googleapis/python-monitoring/commit/22d4eabbafbdc16b0f4faf66f966442691de7666))
* Reintroduce deprecated field/enum `ServiceTier` for backward compatibility ([#240](https://www.github.com/googleapis/python-monitoring/issues/240)) ([eeb0534](https://www.github.com/googleapis/python-monitoring/commit/eeb05347eaf6e7a0794e679d83fe70a0db6a02a3))


### Documentation

* list oneofs in docstring ([22d4eab](https://www.github.com/googleapis/python-monitoring/commit/22d4eabbafbdc16b0f4faf66f966442691de7666))
* Use absolute link targets in comments ([eeb0534](https://www.github.com/googleapis/python-monitoring/commit/eeb05347eaf6e7a0794e679d83fe70a0db6a02a3))

## [2.6.0](https://www.github.com/googleapis/python-monitoring/compare/v2.5.2...v2.6.0) (2021-10-07)


### Features

* add context manager support in client ([#230](https://www.github.com/googleapis/python-monitoring/issues/230)) ([954dd18](https://www.github.com/googleapis/python-monitoring/commit/954dd18966520dbc623470ef528166d83d3e19ba))

## [2.5.2](https://www.github.com/googleapis/python-monitoring/compare/v2.5.1...v2.5.2) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([4a8b823](https://www.github.com/googleapis/python-monitoring/commit/4a8b823061a03fd0e5c385c1fa0ac964b9a5597a))

## [2.5.1](https://www.github.com/googleapis/python-monitoring/compare/v2.5.0...v2.5.1) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([ffae24c](https://www.github.com/googleapis/python-monitoring/commit/ffae24c816a3e1645464098cf86fdaf54a3064a9))

## [2.5.0](https://www.github.com/googleapis/python-monitoring/compare/v2.4.2...v2.5.0) (2021-08-27)


### Features

* Added support for log-based alerts ([#204](https://www.github.com/googleapis/python-monitoring/issues/204)) ([b56a78c](https://www.github.com/googleapis/python-monitoring/commit/b56a78c50780e778f8ce1ad956e621433d1c451b))
* Added support for user-defined labels on cloud monitoring's Service object ([b56a78c](https://www.github.com/googleapis/python-monitoring/commit/b56a78c50780e778f8ce1ad956e621433d1c451b))
* Added support for user-defined labels on cloud monitoring's ServiceLevelObjective object ([b56a78c](https://www.github.com/googleapis/python-monitoring/commit/b56a78c50780e778f8ce1ad956e621433d1c451b))


### Bug Fixes

* mark required fields in QueryTimeSeriesRequest as required by the backend ([b56a78c](https://www.github.com/googleapis/python-monitoring/commit/b56a78c50780e778f8ce1ad956e621433d1c451b))


### Documentation

* **samples:** include example writing of label data ([#202](https://www.github.com/googleapis/python-monitoring/issues/202)) ([f5e8cf8](https://www.github.com/googleapis/python-monitoring/commit/f5e8cf8b51812b9e79bb5312f84e29b3f8c2c81e))

## [2.4.2](https://www.github.com/googleapis/python-monitoring/compare/v2.4.1...v2.4.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#190](https://www.github.com/googleapis/python-monitoring/issues/190)) ([502487a](https://www.github.com/googleapis/python-monitoring/commit/502487a6c40322b5d8a9d38e9bd0783c0db9d756))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#184](https://www.github.com/googleapis/python-monitoring/issues/184)) ([5b7b07b](https://www.github.com/googleapis/python-monitoring/commit/5b7b07b263e2e86f0b504b721c4295f7d8bb542a))


### Miscellaneous Chores

* release as 2.4.2 ([#191](https://www.github.com/googleapis/python-monitoring/issues/191)) ([6f183dd](https://www.github.com/googleapis/python-monitoring/commit/6f183ddeef540be4f47ee553e2b2ee8424508968))

## [2.4.1](https://www.github.com/googleapis/python-monitoring/compare/v2.4.0...v2.4.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#183](https://www.github.com/googleapis/python-monitoring/issues/183)) ([fdc5b07](https://www.github.com/googleapis/python-monitoring/commit/fdc5b0729cb3cb7e204c36569f253fb57728b740))

## [2.4.0](https://www.github.com/googleapis/python-monitoring/compare/v2.3.0...v2.4.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#165](https://www.github.com/googleapis/python-monitoring/issues/165)) ([064f1e0](https://www.github.com/googleapis/python-monitoring/commit/064f1e0a8df02c04bdae6b13c645f2b399c2c1ef))


### Bug Fixes

* disable always_use_jwt_access ([#171](https://www.github.com/googleapis/python-monitoring/issues/171)) ([c194a00](https://www.github.com/googleapis/python-monitoring/commit/c194a00031763153bcc67346328a02b85fabc359))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-monitoring/issues/1127)) ([#159](https://www.github.com/googleapis/python-monitoring/issues/159)) ([adc82c9](https://www.github.com/googleapis/python-monitoring/commit/adc82c9d1812fb0efe00cbfa09f19e8c04277881)), closes [#1126](https://www.github.com/googleapis/python-monitoring/issues/1126)

## [2.3.0](https://www.github.com/googleapis/python-monitoring/compare/v2.2.1...v2.3.0) (2021-06-18)


### Features

* support self-signed JWT flow for service accounts ([ffa4b1f](https://www.github.com/googleapis/python-monitoring/commit/ffa4b1fb529824a5c408880ca5d1e80149bb5a8c))


### Bug Fixes

* add async client to %name_%version/init.py ([ffa4b1f](https://www.github.com/googleapis/python-monitoring/commit/ffa4b1fb529824a5c408880ca5d1e80149bb5a8c))

## [2.2.1](https://www.github.com/googleapis/python-monitoring/compare/v2.2.0...v2.2.1) (2021-03-29)


### Bug Fixes

* fix minimum required versions of proto-plus and pandas ([#102](https://www.github.com/googleapis/python-monitoring/issues/102)) ([782b3b2](https://www.github.com/googleapis/python-monitoring/commit/782b3b29a93f5f6aa0fc027fd9863d753f604dc9))

## [2.2.0](https://www.github.com/googleapis/python-monitoring/compare/v2.1.0...v2.2.0) (2021-03-25)


### Features

* add `client_cert_source_for_mtls` ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added `IstioCanonicalService` for service monitoring. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added `total_size` to the response of `ListAlertPolicies`. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added creation and mutation records to notification channels. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added support for Monitoring Query Language ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added support for Monitoring Query Language ([#101](https://www.github.com/googleapis/python-monitoring/issues/101)) ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added support for querying metrics for folders and organizations. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added support for secondary aggregation when querying metrics. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Added support for units in the `MetricService` ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))


### Bug Fixes

* Extended the default deadline for `UpdateGroup` to 180s. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* Un-deprecated `cluster_istio` for service monitoring. ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))
* use correct retry deadline ([0eb2ca6](https://www.github.com/googleapis/python-monitoring/commit/0eb2ca6b5044553c11d5f5e0f4859bf65387909b))

## [2.1.0](https://www.github.com/googleapis/python-monitoring/compare/v2.0.1...v2.1.0) (2021-03-12)


### Features

* Adding labels to the metric descriptor in the snippets.py ([#88](https://www.github.com/googleapis/python-monitoring/issues/88)) ([811f9aa](https://www.github.com/googleapis/python-monitoring/commit/811f9aa409ec922402cb83a6753812518b7a0d4b))


### Bug Fixes

* fix `as_dataframe` ([#91](https://www.github.com/googleapis/python-monitoring/issues/91)) ([f135202](https://www.github.com/googleapis/python-monitoring/commit/f135202f1dd7866c4be2d709b522beb2710f5cda))


### Documentation

* remove code snippet and 'Stackdriver' ([#71](https://www.github.com/googleapis/python-monitoring/issues/71)) ([4cdb1ff](https://www.github.com/googleapis/python-monitoring/commit/4cdb1ff439154409c94e347dd5f3b6e2bc40e998))

## [2.0.1](https://www.github.com/googleapis/python-monitoring/compare/v2.0.0...v2.0.1) (2021-02-18)


### Bug Fixes

* allow any set query_params to work with `query.iter()` ([#83](https://www.github.com/googleapis/python-monitoring/issues/83)) ([4279c92](https://www.github.com/googleapis/python-monitoring/commit/4279c9252c21e24a43d2613de7fdb1af35dc30fc))
* remove gRPC send/recv limits and expose client transport ([#62](https://www.github.com/googleapis/python-monitoring/issues/62)) ([bec9e87](https://www.github.com/googleapis/python-monitoring/commit/bec9e87551baf9ef5d60c81810e3efa01e96377f))

## [2.0.0](https://www.github.com/googleapis/python-monitoring/compare/v1.1.0...v2.0.0) (2020-10-06)


### ⚠ BREAKING CHANGES

* move to use microgen (#54). See [Migration Guide](https://github.com/googleapis/python-monitoring/blob/main/UPGRADING.md).

### Features

* move to use microgen ([#54](https://www.github.com/googleapis/python-monitoring/issues/54)) ([d25e49f](https://www.github.com/googleapis/python-monitoring/commit/d25e49f13e6f880e77fcb0dc5ef4e3c61fba079a))

## [1.1.0](https://www.github.com/googleapis/python-monitoring/compare/v1.0.0...v1.1.0) (2020-08-20)


### Features

* add "not equal" support to the query filter ([#11](https://www.github.com/googleapis/python-monitoring/issues/11)) ([e293f7f](https://www.github.com/googleapis/python-monitoring/commit/e293f7f90b0d1ccb285c16a32251e442fda06a8e))

## [1.0.0](https://www.github.com/googleapis/python-monitoring/compare/v0.36.0...v1.0.0) (2020-06-03)


### Features

* set release_status to Production/Stable ([#8](https://www.github.com/googleapis/python-monitoring/issues/8)) ([a99d67a](https://www.github.com/googleapis/python-monitoring/commit/a99d67a4f1399b9a74f189c6332cd85e56149fac))

## [0.36.0](https://www.github.com/googleapis/python-monitoring/compare/v0.35.0...v0.36.0) (2020-05-13)


### Features

* BREAKING CHANGE: drop support for TimeSeriesQueryLanguageCondition as an alert condition type ([#22](https://www.github.com/googleapis/python-monitoring/issues/22)) ([e4bc568](https://www.github.com/googleapis/python-monitoring/commit/e4bc5682d39f7e5938868497496f5d49318cee43))

## [0.35.0](https://www.github.com/googleapis/python-monitoring/compare/v0.34.0...v0.35.0) (2020-04-21)


### Features

* add uptime check feature; increase default timeout (via synth) ([#15](https://www.github.com/googleapis/python-monitoring/issues/15)) ([dcf074a](https://www.github.com/googleapis/python-monitoring/commit/dcf074aed9922982f7324d4f2943d9435778d46c))

## 0.34.0

11-19-2019 14:27 PST

### Implementation Changes
- Deprecate resource name helper methods; update docs configuration (via synth). ([#9838](https://github.com/googleapis/google-cloud-python/pull/9838))

### New Features
- Add service monitoring (via synth). ([#9799](https://github.com/googleapis/google-cloud-python/pull/9799))
- Add `monitoring.v3.InternalChecker.state` (via synth). ([#9546](https://github.com/googleapis/google-cloud-python/pull/9546))
- Add `monitoring.v3.UptimeCheckConfig.ContentMatcher.ContentMatcherOption` (via synth). ([#9546](https://github.com/googleapis/google-cloud-python/pull/9546))
- Add `recursive` parameter to `delete_group` (via synth). ([#9546](https://github.com/googleapis/google-cloud-python/pull/9546))
- Add read-only `validity` field to `monitoring.v3.AlertPolicy` (via synth). ([#9546](https://github.com/googleapis/google-cloud-python/pull/9546))
- Add `validate_ssl` parameter to `monitoring.v3.UptimeCheckConfig.HttpCheck` (via synth). ([#9546](https://github.com/googleapis/google-cloud-python/pull/9546))

### Documentation
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Revert change to docs/conf.py. ([#9803](https://github.com/googleapis/google-cloud-python/pull/9803))
- Normalize VPCSC configuration in systests. ([#9615](https://github.com/googleapis/google-cloud-python/pull/9615))
- Make VPCSC env comparison case-insensitive. ([#9564](https://github.com/googleapis/google-cloud-python/pull/9564))
- Refresh VPCSC tests. ([#9437](https://github.com/googleapis/google-cloud-python/pull/9437))
- Fix environment variables for VPC tests. ([#8302](https://github.com/googleapis/google-cloud-python/pull/8302))

## 0.33.0

08-12-2019 13:54 PDT

### New Features
- Add notification channel verification; remove send/recv msg size limit (via synth). ([#8980](https://github.com/googleapis/google-cloud-python/pull/8980))

### Documentation
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.32.0

07-24-2019 16:52 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth).  ([#8397](https://github.com/googleapis/google-cloud-python/pull/8397))
- Add routing header to method metadata, update docs config (via synth).  ([#7642](https://github.com/googleapis/google-cloud-python/pull/7642))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7271](https://github.com/googleapis/google-cloud-python/pull/7271))
- Protoc-generated serialization update. ([#7089](https://github.com/googleapis/google-cloud-python/pull/7089))
- Pick up stub docstring fix in GAPIC generator. ([#6976](https://github.com/googleapis/google-cloud-python/pull/6976))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8516](https://github.com/googleapis/google-cloud-python/pull/8516))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fixes [#8545](https://github.com/googleapis/google-cloud-python/pull/8545) by removing typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))
- Update docstrings, copy lintified proto files (via synth). ([#7451](https://github.com/googleapis/google-cloud-python/pull/7451))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright: 2018 -> 2019. ([#7151](https://github.com/googleapis/google-cloud-python/pull/7151))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8358](https://github.com/googleapis/google-cloud-python/pull/8358))
- Add disclaimer to auto-generated template files (via synth). ([#8321](https://github.com/googleapis/google-cloud-python/pull/8321))
- Fix coverage in 'types.py' (via synth). ([#8159](https://github.com/googleapis/google-cloud-python/pull/8159))
- Add empty lines (via synth). ([#8065](https://github.com/googleapis/google-cloud-python/pull/8065))
- Add nox session `docs` (via synth). ([#7777](https://github.com/googleapis/google-cloud-python/pull/7777))
- Regenerate VPCSC tests to include NotificationChannelService and UptimeCheckService. ([#7853](https://github.com/googleapis/google-cloud-python/pull/7853))
- Set environment variables for VPCSC system tests. ([#7847](https://github.com/googleapis/google-cloud-python/pull/7847))
- Add VPCSC system test. ([#7791](https://github.com/googleapis/google-cloud-python/pull/7791))
- protobuf file housekeeping (no user-visible changes) (via synth).  ([#7588](https://github.com/googleapis/google-cloud-python/pull/7588))
- Add clarifying comment to blacken nox target. ([#7398](https://github.com/googleapis/google-cloud-python/pull/7398))
- Trivial gapic-generator change. ([#7231](https://github.com/googleapis/google-cloud-python/pull/7231))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.31.1

12-17-2018 16:51 PST


### Implementation Changes
- Import  `iam.policy` from `google.api_core.iam.policy`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))

## 0.31.0

11-29-2018 13:03 PST


### Implementation Changes
- Pick up enum fixes in the GAPIC generator. ([#6614](https://github.com/googleapis/google-cloud-python/pull/6614))
- Pick up fixes to the GAPIC generator. ([#6501](https://github.com/googleapis/google-cloud-python/pull/6501))
- Fix client_info bug, update docstrings and timeouts. ([#6416](https://github.com/googleapis/google-cloud-python/pull/6416))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Docstring changes, 'account' -> 'workspace', via synth. ([#6461](https://github.com/googleapis/google-cloud-python/pull/6461))
- Add 'dropped_labels', 'span_context', plus docstring changes. ([#6358](https://github.com/googleapis/google-cloud-python/pull/6358))
- Fix GAX fossils ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Harmonize / DRY 'monitoring/README.rst' / 'monitoring/docs/index.rst'. ([#6156](https://github.com/googleapis/google-cloud-python/pull/6156))

### Internal / Testing Changes
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Fix long lines from autosynth ([#5961](https://github.com/googleapis/google-cloud-python/pull/5961)
- Test pandas under all supported Python versions ([#5858](https://github.com/googleapis/google-cloud-python/pull/5858))

## 0.30.1

### Implementation Changes
- Monitoring: Add Transports Layer to clients (#5594)
- Remove gRPC size restrictions (4MB default) (#5594)

### Documentation
- Monitoring. Update documentation links. (#5557)

## 0.30.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Add aliases for new V3 service clients. (#5424)

### Documentation
- Remove link to `usage` on index of monitoring (#5272)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 0.29.0

### Implementation Changes
- Update monitoring library to use new generated client (#5212)
- Move aligner and reducer links from timeSeries.list to alertPolicies (#5011)

### Internal / Testing Changes
- Fix bad trove classifier

## 0.28.1

### Implementation changes

- Convert label values to str in client.metric() (#4910)

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-monitoring/0.28.0/
