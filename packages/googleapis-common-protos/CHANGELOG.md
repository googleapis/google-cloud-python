# Changelog

## [1.63.2](https://github.com/googleapis/python-api-common-protos/compare/v1.63.1...v1.63.2) (2024-06-19)


### Bug Fixes

* **deps:** Require protobuf&gt;=3.20.2 ([c77c0dc](https://github.com/googleapis/python-api-common-protos/commit/c77c0dc5d29ef780d781a3c5d757736a9ed09674))
* Regenerate pb2 files for compatibility with protobuf 5.x ([c77c0dc](https://github.com/googleapis/python-api-common-protos/commit/c77c0dc5d29ef780d781a3c5d757736a9ed09674))

## [1.63.1](https://github.com/googleapis/python-api-common-protos/compare/v1.63.0...v1.63.1) (2024-05-30)


### Bug Fixes

* Increase upper limit for protobuf 5.X versions ([#212](https://github.com/googleapis/python-api-common-protos/issues/212)) ([28fc17a](https://github.com/googleapis/python-api-common-protos/commit/28fc17a9208aa98782acc6bee6c40ec12b959706))

## [1.63.0](https://github.com/googleapis/python-api-common-protos/compare/v1.62.0...v1.63.0) (2024-03-08)


### Features

* Add `api_version` field to `ServiceOptions` in `google/api/client.proto` ([6f9c4d2](https://github.com/googleapis/python-api-common-protos/commit/6f9c4d2b4b787d9ed2b447d7b99281aa3dcf97b5))
* Add `LOCATION_POLICY_VIOLATED` enum to `ErrorReason` in `google/api/error_reason.proto` ([6f9c4d2](https://github.com/googleapis/python-api-common-protos/commit/6f9c4d2b4b787d9ed2b447d7b99281aa3dcf97b5))
* Add `rest_reference_documentation_uri` field to `ServiceOptions` in `google/api/client.proto` ([6f9c4d2](https://github.com/googleapis/python-api-common-protos/commit/6f9c4d2b4b787d9ed2b447d7b99281aa3dcf97b5))

## [1.62.0](https://github.com/googleapis/python-api-common-protos/compare/v1.61.0...v1.62.0) (2023-12-01)


### Features

* Add `auto_populated_fields` field of `MethodSettings` in `google/api/client_pb2` ([#194](https://github.com/googleapis/python-api-common-protos/issues/194)) ([4b0c73a](https://github.com/googleapis/python-api-common-protos/commit/4b0c73a40f9bf5337fe451c0210f73eadd196b99))
* Add support for Python 3.12 ([#192](https://github.com/googleapis/python-api-common-protos/issues/192)) ([336cdf3](https://github.com/googleapis/python-api-common-protos/commit/336cdf351d4e87891d735837817d2cfc4e5a9fc7))


### Bug Fixes

* Migrate to native namespace packages ([#187](https://github.com/googleapis/python-api-common-protos/issues/187)) ([713e388](https://github.com/googleapis/python-api-common-protos/commit/713e3887a3293aea314060e84bdcf8a12eda3d6c))

## [1.61.0](https://github.com/googleapis/python-api-common-protos/compare/v1.60.0...v1.61.0) (2023-10-09)


### Features

* Add `google/api/field_info.proto` ([2d39f37](https://github.com/googleapis/python-api-common-protos/commit/2d39f37212fe886b3029e1043ca28789e2d66876))
* Add `IDENTIFIER` to `FieldBehavior` enum ([2d39f37](https://github.com/googleapis/python-api-common-protos/commit/2d39f37212fe886b3029e1043ca28789e2d66876))

## [1.60.0](https://github.com/googleapis/python-api-common-protos/compare/v1.59.1...v1.60.0) (2023-07-27)


### Features

* Add `google/api/policy.proto` ([b2cb5c2](https://github.com/googleapis/python-api-common-protos/commit/b2cb5c257ae8d0869d33581b116995620ddae0b2))
* Add `method_policies` to `Control` ([b2cb5c2](https://github.com/googleapis/python-api-common-protos/commit/b2cb5c257ae8d0869d33581b116995620ddae0b2))

## [1.59.1](https://github.com/googleapis/python-api-common-protos/compare/v1.59.0...v1.59.1) (2023-06-06)


### Bug Fixes

* Invalid `dev` version identifiers in `setup.py` ([#166](https://github.com/googleapis/python-api-common-protos/issues/166)) ([c38e03a](https://github.com/googleapis/python-api-common-protos/commit/c38e03aa06eedf65373c283f16e7bbbd5622f37b)), closes [#165](https://github.com/googleapis/python-api-common-protos/issues/165)

## [1.59.0](https://github.com/googleapis/python-api-common-protos/compare/v1.58.0...v1.59.0) (2023-03-20)


### Features

* Add overrides_by_request_protocol to BackendRule in google/api/backend.proto ([77376dd](https://github.com/googleapis/python-api-common-protos/commit/77376dd02af0a1c9255a50516550d2474536fa9d))
* Add proto_reference_documentation_uri to Publishing in google/api/client.proto ([77376dd](https://github.com/googleapis/python-api-common-protos/commit/77376dd02af0a1c9255a50516550d2474536fa9d))
* Add SERVICE_NOT_VISIBLE and GCP_SUSPENDED to ErrorReason in google/api/error_reason.proto ([77376dd](https://github.com/googleapis/python-api-common-protos/commit/77376dd02af0a1c9255a50516550d2474536fa9d))


### Documentation

* Use rst syntax in readme  ([77376dd](https://github.com/googleapis/python-api-common-protos/commit/77376dd02af0a1c9255a50516550d2474536fa9d))

## [1.58.0](https://github.com/googleapis/python-api-common-protos/compare/v1.57.1...v1.58.0) (2023-01-06)


### Features

* Add google/rpc/context/audit_context.proto ([41f1529](https://github.com/googleapis/python-api-common-protos/commit/41f1529500e535ec83e2d72f8e97dfda5469cb72))
* Add google/rpc/http.proto ([41f1529](https://github.com/googleapis/python-api-common-protos/commit/41f1529500e535ec83e2d72f8e97dfda5469cb72))

## [1.57.1](https://github.com/googleapis/python-api-common-protos/compare/v1.57.0...v1.57.1) (2022-12-08)


### Bug Fixes

* Mark reference_docs_uri field in google/api/client.proto as deprecated ([#150](https://github.com/googleapis/python-api-common-protos/issues/150)) ([52b5018](https://github.com/googleapis/python-api-common-protos/commit/52b5018abf0902a1e582a406c993b51e0d2aa3cd))

## [1.57.0](https://github.com/googleapis/python-api-common-protos/compare/v1.56.4...v1.57.0) (2022-11-15)


### Features

* Add support for Python 3.10 ([#143](https://github.com/googleapis/python-api-common-protos/issues/143)) ([63ca888](https://github.com/googleapis/python-api-common-protos/commit/63ca888512be84508fcf95e4d5d40df036a85e18))
* Add support for Python 3.11 ([#145](https://github.com/googleapis/python-api-common-protos/issues/145)) ([b9dbb21](https://github.com/googleapis/python-api-common-protos/commit/b9dbb219ea46abd9851af1fc41ea37f9d5631c0b))
* added google.api.JwtLocation.cookie ([6af2132](https://github.com/googleapis/python-api-common-protos/commit/6af21322879cba158e0a5992c9799e68c1744fac))
* added google.api.Service.publishing and client libraries settings ([6af2132](https://github.com/googleapis/python-api-common-protos/commit/6af21322879cba158e0a5992c9799e68c1744fac))
* new fields in enum google.api.ErrorReason ([6af2132](https://github.com/googleapis/python-api-common-protos/commit/6af21322879cba158e0a5992c9799e68c1744fac))


### Bug Fixes

* deprecate google.api.BackendRule.min_deadline ([6af2132](https://github.com/googleapis/python-api-common-protos/commit/6af21322879cba158e0a5992c9799e68c1744fac))
* **deps:** Require protobuf &gt;=3.19.5 ([#141](https://github.com/googleapis/python-api-common-protos/issues/141)) ([9ea3530](https://github.com/googleapis/python-api-common-protos/commit/9ea3530b459269e964fcc98db1c5025e05d6495f))


### Documentation

* minor updates to comments ([6af2132](https://github.com/googleapis/python-api-common-protos/commit/6af21322879cba158e0a5992c9799e68c1744fac))

## [1.56.4](https://github.com/googleapis/python-api-common-protos/compare/v1.56.3...v1.56.4) (2022-07-12)


### Bug Fixes

* require python 3.7+ ([#119](https://github.com/googleapis/python-api-common-protos/issues/119)) ([507b58d](https://github.com/googleapis/python-api-common-protos/commit/507b58dfa0516aedf57880b384e92cda97152398))

## [1.56.3](https://github.com/googleapis/python-api-common-protos/compare/v1.56.2...v1.56.3) (2022-06-21)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#112](https://github.com/googleapis/python-api-common-protos/issues/112)) ([67b0231](https://github.com/googleapis/python-api-common-protos/commit/67b02313bf47d86ac84917756ff026e331665637))


### Documentation

* fix changelog header to consistent size ([#108](https://github.com/googleapis/python-api-common-protos/issues/108)) ([d315b9f](https://github.com/googleapis/python-api-common-protos/commit/d315b9f23f5dbbce27c965a2b692a8d1dcf03d60))

## [1.56.2](https://github.com/googleapis/python-api-common-protos/compare/v1.56.1...v1.56.2) (2022-05-26)


### Bug Fixes

* **deps:** require grpcio >= 1.0.0, <2.0.0dev ([4a402ce](https://github.com/googleapis/python-api-common-protos/commit/4a402ce798c8364679e69eefdaadcf61fc289308))
* **deps:** require protobuf>= 3.15.0, <4.0.0dev ([#105](https://github.com/googleapis/python-api-common-protos/issues/105)) ([4a402ce](https://github.com/googleapis/python-api-common-protos/commit/4a402ce798c8364679e69eefdaadcf61fc289308))

## [1.56.1](https://github.com/googleapis/python-api-common-protos/compare/v1.56.0...v1.56.1) (2022-05-05)


### Bug Fixes

* **deps:** require protobuf >=1.15.0 ([f04ed64](https://github.com/googleapis/python-api-common-protos/commit/f04ed64b233e1ff95370ef412ad5ecb92cb5780e))
* include tests directory ([#103](https://github.com/googleapis/python-api-common-protos/issues/103)) ([72e5df1](https://github.com/googleapis/python-api-common-protos/commit/72e5df15ce63012f7d5c7781a51687e85a2cf63c))
* regenerate pb2 files using the latest version of grpcio-tools ([f04ed64](https://github.com/googleapis/python-api-common-protos/commit/f04ed64b233e1ff95370ef412ad5ecb92cb5780e))

## [1.56.0](https://github.com/googleapis/python-api-common-protos/compare/v1.55.0...v1.56.0) (2022-03-17)


### Features

* add google/api/error_reason.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* add google/api/visibility.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* add google/type/decimal.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* add google/type/interval.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* add google/type/localized_text.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* add google/type/phone_number.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))
* update all protos and pb2 files ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))


### Bug Fixes

* expose all names in longrunning _pb2's ([#90](https://github.com/googleapis/python-api-common-protos/issues/90)) ([09e9ccd](https://github.com/googleapis/python-api-common-protos/commit/09e9ccd86c21dceb3a5add66cc4bf5009cb255a9))
* re-generate pb2 files ([#87](https://github.com/googleapis/python-api-common-protos/issues/87)) ([6260547](https://github.com/googleapis/python-api-common-protos/commit/6260547506f122ca9ee833aca0669d1650304a11))
* re-generate pb2 files using grpcio-tools<1.44.0 ([#93](https://github.com/googleapis/python-api-common-protos/issues/93)) ([76bb9f6](https://github.com/googleapis/python-api-common-protos/commit/76bb9f66f9674ad4c3a7fdc8812dadfb25b170a6))
* remove deprecated fields `aliases` and `features` from google/api/endpoint.proto ([62c04b8](https://github.com/googleapis/python-api-common-protos/commit/62c04b83ef9ce972760407d8e9e9e0d77bbb071c))

## [1.55.0](https://github.com/googleapis/python-api-common-protos/compare/v1.54.0...v1.55.0) (2022-02-15)


### Features

* add location proto files. ([#84](https://github.com/googleapis/python-api-common-protos/issues/84)) ([9a33e56](https://github.com/googleapis/python-api-common-protos/commit/9a33e56ac6a07a2e717edc55a39fa7cf2f9eec15))

## [1.54.0](https://www.github.com/googleapis/python-api-common-protos/compare/v1.53.0...v1.54.0) (2021-12-07)


### Features

* add extended_operations.proto ([#77](https://www.github.com/googleapis/python-api-common-protos/issues/77)) ([bc85849](https://www.github.com/googleapis/python-api-common-protos/commit/bc85849e21494b267d87cd6dc5d0a0e23e012470))
* add google/api/routing.proto ([#75](https://www.github.com/googleapis/python-api-common-protos/issues/75)) ([1ae0bbc](https://www.github.com/googleapis/python-api-common-protos/commit/1ae0bbcc9747af4dd467e7a246c1a2a4cd5ef2ec))

## [1.53.0](https://www.github.com/googleapis/python-api-common-protos/compare/v1.52.0...v1.53.0) (2021-02-25)


### Features

* add `google.api.ResourceDescriptor.Style` ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))
* add API method signatures to longrunning operations ([8de7ae2](https://www.github.com/googleapis/python-api-common-protos/commit/8de7ae28dfe5dd4d0cb99dd3b89a8f1e614bbe6d))
* add gapic_metadata_pb2 ([#38](https://www.github.com/googleapis/python-api-common-protos/issues/38)) ([8de7ae2](https://www.github.com/googleapis/python-api-common-protos/commit/8de7ae28dfe5dd4d0cb99dd3b89a8f1e614bbe6d))
* add UNORDERED_LIST to field options ([8de7ae2](https://www.github.com/googleapis/python-api-common-protos/commit/8de7ae28dfe5dd4d0cb99dd3b89a8f1e614bbe6d))
* add WaitOperation method to longrunning operations ([8de7ae2](https://www.github.com/googleapis/python-api-common-protos/commit/8de7ae28dfe5dd4d0cb99dd3b89a8f1e614bbe6d))
* require python >=3.6 and   ([#31](https://www.github.com/googleapis/python-api-common-protos/issues/31)) ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))


### Bug Fixes

* add `create_key` to FieldDescriptors ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))
* Generate gRPC files for long-running operations ([#13](https://www.github.com/googleapis/python-api-common-protos/issues/13)) ([a9ce288](https://www.github.com/googleapis/python-api-common-protos/commit/a9ce28840ddfec712da5b296f43e6c3131840db4))


### Documentation

* add link to PyPI ([#10](https://www.github.com/googleapis/python-api-common-protos/issues/10)) ([3f79402](https://www.github.com/googleapis/python-api-common-protos/commit/3f7940226b0e22aef31b82c8dc2196aa25b48a3f))

## [1.53.0dev1](https://www.github.com/googleapis/python-api-common-protos/compare/v1.52.0...v1.53.0dev1) (2021-01-27)


### Features

* add `google.api.ResourceDescriptor.Style` ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))
* require python >=3.6 and   ([#31](https://www.github.com/googleapis/python-api-common-protos/issues/31)) ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))


### Bug Fixes

* add `create_key` to FieldDescriptors ([4ce679c](https://www.github.com/googleapis/python-api-common-protos/commit/4ce679cd49771946bf781108e92e07cdf04a61eb))
* Generate gRPC files for long-running operations ([#13](https://www.github.com/googleapis/python-api-common-protos/issues/13)) ([a9ce288](https://www.github.com/googleapis/python-api-common-protos/commit/a9ce28840ddfec712da5b296f43e6c3131840db4))


### Documentation

* add link to PyPI ([#10](https://www.github.com/googleapis/python-api-common-protos/issues/10)) ([3f79402](https://www.github.com/googleapis/python-api-common-protos/commit/3f7940226b0e22aef31b82c8dc2196aa25b48a3f))

## 1.52.0 (2020-06-04)


### Features

* create api-common-protos repo for python common protos ([4ef4b0d](https://www.github.com/googleapis/python-api-common-protos/commit/4ef4b0d177136bfbd19f4c00ccf2f6d7eaccb153))
