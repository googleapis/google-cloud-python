# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-api-core/#history

## [1.19.0](https://www.github.com/googleapis/python-api-core/compare/v1.18.0...v1.19.0) (2020-06-05)


### Features

* **client_options:** add new client options 'quota_project_id', 'scopes', and 'credentials_file' ([a582936](https://www.github.com/googleapis/python-api-core/commit/a58293601d6da90c499d404e634a979a6cae9708))

## [1.18.0](https://www.github.com/googleapis/python-api-core/compare/v1.17.0...v1.18.0) (2020-06-04)


### Features

* [CBT-6 helper] Exposing Retry._deadline as a property ([#20](https://www.github.com/googleapis/python-api-core/issues/20)) ([7be1e59](https://www.github.com/googleapis/python-api-core/commit/7be1e59e9d75c112f346d2b76dce3dd60e3584a1))
* add client_encryped_cert_source to ClientOptions ([#31](https://www.github.com/googleapis/python-api-core/issues/31)) ([e4eaec0](https://www.github.com/googleapis/python-api-core/commit/e4eaec0ff255114138d3715280f86d34d861a6fa))
* AsyncIO Integration [Part 2] ([#28](https://www.github.com/googleapis/python-api-core/issues/28)) ([dd9b2f3](https://www.github.com/googleapis/python-api-core/commit/dd9b2f38a70e85952cc05552ec8070cdf29ddbb4)), closes [#23](https://www.github.com/googleapis/python-api-core/issues/23)
* First batch of AIO integration ([#26](https://www.github.com/googleapis/python-api-core/issues/26)) ([a82f289](https://www.github.com/googleapis/python-api-core/commit/a82f2892b8f219b82e120e6ed9f4070869c28be7))
* third batch of AsyncIO integration ([#29](https://www.github.com/googleapis/python-api-core/issues/29)) ([7d8d580](https://www.github.com/googleapis/python-api-core/commit/7d8d58075a92e93662747d36a2d55b5e9f0943e1))

## [1.17.0](https://www.github.com/googleapis/python-api-core/compare/v1.16.0...v1.17.0) (2020-04-14)


### Features

* **api_core:** add retry param into PollingFuture() and it's inheritors ([#9923](https://www.github.com/googleapis/python-api-core/issues/9923)) ([14f1f34](https://www.github.com/googleapis/python-api-core/commit/14f1f34e013c90fed2da2918625083d299fda557)), closes [#6197](https://www.github.com/googleapis/python-api-core/issues/6197)
* **api-core:** add client_cert_source to ClientOptions ([#17](https://www.github.com/googleapis/python-api-core/issues/17)) ([748c935](https://www.github.com/googleapis/python-api-core/commit/748c935d4cf03a1f04fba9139c3c3150fd694d88))


### Bug Fixes

* consume part of StreamingResponseIterator to support failure while under a retry context ([#10206](https://www.github.com/googleapis/python-api-core/issues/10206)) ([2b103b6](https://www.github.com/googleapis/python-api-core/commit/2b103b60ece16a1e1bc98cfda7ec375191a90f75))

## 1.16.0

01-13-2020 14:19 PST

### New Features

- feat(storage): support optionsRequestedPolicyVersion ([#9989](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9989))
- feat(api_core): support version 3 policy bindings ([#9869](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9869))

## 1.15.0

12-16-2019 15:27 PST

### New Features
- Make the last retry happen at deadline. ([#9873](https://github.com/googleapis/google-cloud-python/pull/9873))
- Add a repr method for ClientOptions. ([#9849](https://github.com/googleapis/google-cloud-python/pull/9849))
- Simplify `from_rfc3339` methods. ([#9641](https://github.com/googleapis/google-cloud-python/pull/9641))
- Provide a `raw_page` field for `page_iterator.Page`. ([#9486](https://github.com/googleapis/google-cloud-python/pull/9486))

### Documentation
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Remove references to the old authentication credentials. ([#9456](https://github.com/googleapis/google-cloud-python/pull/9456))

## 1.14.3

10-07-2019 10:35 PDT


### Implementation Changes
- Finalize during close of 'ResumableBidiRpc' ([#9337](https://github.com/googleapis/google-cloud-python/pull/9337))
- add on_error to Retry.__init__ ([#8892](https://github.com/googleapis/google-cloud-python/pull/8892))
- Fix race in 'BackgroundConsumer._thread_main'. ([#8883](https://github.com/googleapis/google-cloud-python/pull/8883))

### Documentation
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Fix broken links in docs. ([#9148](https://github.com/googleapis/google-cloud-python/pull/9148))
- About of time -> amount of time ([#9052](https://github.com/googleapis/google-cloud-python/pull/9052))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 1.14.2

07-30-2019 14:08 PDT


### Documentation
- Add client_options documentation. ([#8834](https://github.com/googleapis/google-cloud-python/pull/8834))

## 1.14.1

07-30-2019 12:24 PDT


### Implementation Changes
- Remove error log entry on clean BiDi shutdown. ([#8806](https://github.com/googleapis/google-cloud-python/pull/8806))
- Forward 'timeout' arg from 'exception' to `_blocking_poll`. ([#8735](https://github.com/googleapis/google-cloud-python/pull/8735))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 1.14.0

07-17-2019 13:16 PDT


### New Features
- Firestore: Add `should_terminate` predicate for clean BiDi shutdown. ([#8650](https://github.com/googleapis/google-cloud-python/pull/8650))

### Dependencies
- Update pins of 'googleapis-common-protos. ([#8688](https://github.com/googleapis/google-cloud-python/pull/8688))

### Documentation
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 1.13.0

06-24-2019 10:34 PDT

### New Features
- Add `client_options.ClientOptions` object. ([#8265](https://github.com/googleapis/google-cloud-python/pull/8265))

## 1.12.0

06-18-2019 12:37 PDT


### New Features
- Add Throttling to Bidi Reopening. Mitigates ResumableBidiRpc consuming 100% CPU ([#8193](https://github.com/googleapis/google-cloud-python/pull/8193))

## 1.11.1

05-28-2019 11:19 PDT


### Implementation Changes
- Classify 503 Service Unavailable errors as transient. ([#8182](https://github.com/googleapis/google-cloud-python/pull/8182))

### Dependencies
- Pin `grpcio < 2.0dev`. ([#8182](https://github.com/googleapis/google-cloud-python/pull/8182))

### Internal / Testing Changes
- Add parameterized test for `from_rfc3339` with nanos ([#7675](https://github.com/googleapis/google-cloud-python/pull/7675))
- Unbreak pytype by silencing a false positive. ([#8106](https://github.com/googleapis/google-cloud-python/pull/8106))

## 1.11.0

05-15-2019 10:29 PDT

### New Features

- Refactor 'client_info' support. ([#7849](https://github.com/googleapis/google-cloud-python/pull/7849))

## 1.10.0

04-29-2019 10:12 PDT

### Implementation Changes

- Append leading zeros for nanosecond precision DateTimes
  ([#7663](https://github.com/googleapis/google-cloud-python/pull/7663))

### New Features

- Add `user_agent` property to `ClientInfo`
  ([#7799](https://github.com/googleapis/google-cloud-python/pull/7799))

## 1.9.0

04-05-2019 10:38 PDT


### Implementation Changes
- Allow passing metadata as part of creating a bidi ([#7514](https://github.com/googleapis/google-cloud-python/pull/7514))

### Internal / Testing Changes
- Update setup.py
- API Core: specify a pytype output directory in setup.cfg. ([#7639](https://github.com/googleapis/google-cloud-python/pull/7639))

## 1.8.2

03-22-2019 16:27 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### Internal / Testing Changes
- When re-opening a `ResumableBidiRPC` set `_request_queue_generator` to `None`. ([#7548](https://github.com/googleapis/google-cloud-python/pull/7548))

## 1.8.1

03-12-2019 12:45 PDT

### Implementation Changes
- Protect the creation of a background thread in BackgroundConsumer and wait on it starting. ([#7499](https://github.com/googleapis/google-cloud-python/pull/7499))

## 1.8.0

02-23-2019 15:46 PST


### New Features
- Add support to unwrap Anys into wrapped pb2 objects. ([#7430](https://github.com/googleapis/google-cloud-python/pull/7430))
- Add `Operation.deserialize`. ([#7427](https://github.com/googleapis/google-cloud-python/pull/7427))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes
- Fix new lint failure. ([#7382](https://github.com/googleapis/google-cloud-python/pull/7382))

## 1.7.0

12-17-2018 13:56 PST

### New Features
- Support converting `DatetimeWithNanos` to / from `google.protobuf.timestamp_pb2.Timestamp`. ([#6919](https://github.com/googleapis/google-cloud-python/pull/6919))

### Documentation
- Document Python 2 deprecation. ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Add usage example for `google.api_core.iam.Polcy`. ([#6855](https://github.com/googleapis/google-cloud-python/pull/6855))

### Internal / Testing Changes
- Work around pytype big for `ABCMeta.register`. ([#6873](https://github.com/googleapis/google-cloud-python/pull/6873))

## 1.6.0

11-30-2018 12:45 PST


### Implementation Changes
- Import stdlib ABCs from 'collections.abc' rather than 'collections'. ([#6451](https://github.com/googleapis/google-cloud-python/pull/6451))

### New Features
- Move google.cloud.iam (core) to google.api_core.iam ([#6740](https://github.com/googleapis/google-cloud-python/pull/6740))
- Add bidi support to api_core. ([#6191](https://github.com/googleapis/google-cloud-python/pull/6191))

### Documentation
- Fix typo ([#6532](https://github.com/googleapis/google-cloud-python/pull/6532))

### Internal / Testing Changes
- blacken api_core and core ([#6668](https://github.com/googleapis/google-cloud-python/pull/6668))

## 1.5.2

11-09-2018 14:22 PST


### Implementation Changes
- Retry transient errors in 'PollingFuture.result'. ([#6305](https://github.com/googleapis/google-cloud-python/pull/6305))

### Dependencies
- Remove hyphen from named extra in api_core. ([#6468](https://github.com/googleapis/google-cloud-python/pull/6468))
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

## 1.5.1

10-29-2018 13:29 PDT

### Implementation Changes
- Don't URL-encode slashes in gRPC request headers. ([#6310](https://github.com/googleapis/google-cloud-python/pull/6310))

### Internal / Testing Changes
- Back out changes from [#6267](https://github.com/googleapis/google-cloud-python/pull/6267) / `api_core-1.6.0a1` release. ([#6328](https://github.com/googleapis/google-cloud-python/pull/6328))

## 1.5.0

### New Features
- Add bidi, Bidirection Streaming, to api-core ([#6211](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6211))

### Internal / Testing Changes
- Use new Nox ([#6175](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6175))

## 1.4.1

### Dependencies
- Pin minimum protobuf dependency to 3.4.0. ([#6132](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6132))

### Internal / Testing Changes
- Add type-checking via pytype to api_core. ([#6116](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6116))

## 1.4.0

### Dependencies

- Add support for gRPC connection management (available when using optional grpc_gcp dependency) ([#5553](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5553)) ([#5904](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5904))
- Update classifiers to drop Python 3.4 and add Python 3.7 ([#5702](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5702))

## 1.3.0

### New Features

- Add protobuf_helpers.field_mask to calculate a field mask from two messages (#5320)

## 1.2.1

### Implementation Changes
- Make client_info work without gRPC installed. (#5075)
- Rename `x-goog-header-params` to `x-goog-request-params` (#5495)

## 1.2.0

### Implementation Changes
- Add close method to grpc Channel (#5333)

### Internal / Testing Changes
- Fix tests after grpcio update (#5333)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 1.1.2

### Packaging
- Update setuptools before packaging (#5265)

## 1.1.1

### Internal / Testing Changes
- Use `install_requires` for platform dependencies instead of `extras_require` (#4991)
- Update trove classifer to '5 - Production/Stable'

## 1.1.0

### Interface additions

- Add `datetime_helpers.DatetimeWithNanoSeconds` (#4979)

### Implementation changes

- Use a class to wrap grpc streaming errors instead of monkey-patching (#4995)

## 1.0.0

This is the stable v1.0.0 release of google-api-core for Python. Releases after
this will not contain breaking changes.

### Interface changes and additions

- Made `api_core.page_iterator.PageIterator.item_to_value` public
- Added ability to specify retry for `Operation` and `polling.Future`. (#4922)

## 0.1.4

### New Features

- Add `ChannelStub` to `grpc_helpers` for testing gRPC-based clients. (#4705)

### Notable Implementation Changes

- Fix handling of gapic metadata when specified as `None`. (#4701)

## 0.1.3

### Notable Implementation Changes

- Apply scopes to explicitly provided credentials if needed (#4594).
- Removing `google.api_core.gapic_v1.method.METRICS_METADATA_KEY`. It
  can be accessed via
  `google.api_core.gapic_v1.client_info.METRICS_METADATA_KEY` (#4588).

### Dependencies

- Upgrading to latest `grpcio==1.8.2` (#4642). For details, see
  related gRPC [bug](https://github.com/grpc/grpc/issues/9688)
  and [fix](https://github.com/grpc/grpc/pull/13665).

PyPI: https://pypi.org/project/google-api-core/0.1.3/

## 0.1.2

- Upgrading `concurrent.futures` backport from `>= 3.0.0`
  to `>= 3.2.0` (#4521).
- Moved `datetime`-related helpers from `google.cloud.core` to
  `google.api_core.datetime_helpers` (#4399).
- Added missing `client_info` to `gapic_v1/__init__.py`'s
  `__all__` (#4567).
- Added helpers for routing headers to `gapic_v1` (#4336).

PyPI: https://pypi.org/project/google-api-core/0.1.2/

## 0.1.1

### Dependencies

- Upgrading `grpcio` dependency from `1.2.0, < 1.6dev` to `>= 1.7.0` (#4280)

PyPI: https://pypi.org/project/google-api-core/0.1.1/

## 0.1.0

Initial release

Prior to being separated, this package was developed in `google-cloud-core`, so
relevant changes from that package are included here.

- Add google.api.core.gapic_v1.config (#4022)
- Add google.api.core.helpers.grpc_helpers (#4041)
- Add google.api.core.gapic_v1.method (#4057)
- Add wrap_with_paging (#4067)
- Add grpc_helpers.create_channel (#4069)
- Add DEFAULT sentinel for gapic_v1.method (#4079)
- Remove `googleapis-common-protos` from deps in non-`core` packages. (#4098)
- Add google.api.core.operations_v1 (#4081)
- Fix test assertion in test_wrap_method_with_overriding_retry_deadline (#4131)
- Add google.api.core.helpers.general_helpers.wraps (#4166)
- Update Docs with Python Setup Guide (#4187)
- Move modules in google.api.core.helpers up one level, delete google.api.core.helpers. (#4196)
- Clarify that PollingFuture timeout is in seconds. (#4201)
- Add api_core package (#4210)
- Replace usage of google.api.core with google.api_core (#4221)
- Add google.api_core.gapic_v2.client_info (#4225)
- Fix how api_core.operation populates exception errors (#4231)
- Fix bare except (#4250)
- Fix parsing of API errors with Unicode err message (#4251)
- Port gax proto helper methods (#4249)
- Remove gapic_v1.method.wrap_with_paging (#4257)
- Add final set of protobuf helpers to api_core (#4259)

PyPI: https://pypi.org/project/google-api-core/0.1.0/
