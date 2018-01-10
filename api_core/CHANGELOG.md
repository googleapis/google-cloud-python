# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-api-core/#history

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
