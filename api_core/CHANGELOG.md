# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-api-core/#history

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
