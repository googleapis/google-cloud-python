# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-api-core/#history

## 0.1.1

- Upgrading `grpcio` dependency from `1.2.0, < 1.6dev` to `>= 1.7.0` (#4280)

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
