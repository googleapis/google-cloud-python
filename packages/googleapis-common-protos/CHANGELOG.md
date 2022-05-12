# Changelog

### [1.56.1](https://github.com/googleapis/python-api-common-protos/compare/v1.56.0...v1.56.1) (2022-05-05)


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
