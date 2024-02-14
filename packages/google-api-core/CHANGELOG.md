# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-api-core/#history

## [2.17.1](https://github.com/googleapis/python-api-core/compare/v2.17.0...v2.17.1) (2024-02-13)


### Bug Fixes

* Resolve issue handling protobuf responses in rest streaming ([#604](https://github.com/googleapis/python-api-core/issues/604)) ([bcebc92](https://github.com/googleapis/python-api-core/commit/bcebc92eca69dae81c5e546d526c92b164a6b3b4))

## [2.17.0](https://github.com/googleapis/python-api-core/compare/v2.16.2...v2.17.0) (2024-02-06)


### Features

* Add attempt_direct_path argument to create_channel ([#583](https://github.com/googleapis/python-api-core/issues/583)) ([94726e7](https://github.com/googleapis/python-api-core/commit/94726e739698035b00667983f854c600252abd28))


### Bug Fixes

* Retry constructors methods support None ([#592](https://github.com/googleapis/python-api-core/issues/592)) ([416203c](https://github.com/googleapis/python-api-core/commit/416203c1888934670bfeccafe5f5469f87314512))

## [2.16.2](https://github.com/googleapis/python-api-core/compare/v2.16.1...v2.16.2) (2024-02-02)


### Bug Fixes

* Spelling error `a,out` -&gt; `amount` ([#596](https://github.com/googleapis/python-api-core/issues/596)) ([88688b1](https://github.com/googleapis/python-api-core/commit/88688b1625c4dab0df6124a0560f550eb322500f))

## [2.16.1](https://github.com/googleapis/python-api-core/compare/v2.16.0...v2.16.1) (2024-01-30)


### Bug Fixes

* Fix broken import for google.api_core.retry_async.AsyncRetry ([#587](https://github.com/googleapis/python-api-core/issues/587)) ([ac012c0](https://github.com/googleapis/python-api-core/commit/ac012c04c69b8bbe72962f0d0d9e9536c0b4a524))

## [2.16.0](https://github.com/googleapis/python-api-core/compare/v2.15.0...v2.16.0) (2024-01-29)


### Features

* Retry and retry_async support streaming rpcs ([#495](https://github.com/googleapis/python-api-core/issues/495)) ([17ff5f1](https://github.com/googleapis/python-api-core/commit/17ff5f1d83a9a6f50a0226fb0e794634bd584f17))

## [2.15.0](https://github.com/googleapis/python-api-core/compare/v2.14.0...v2.15.0) (2023-12-07)


### Features

* Add support for Python 3.12 ([#557](https://github.com/googleapis/python-api-core/issues/557)) ([091b4f1](https://github.com/googleapis/python-api-core/commit/091b4f1c7fcc59c3f2a02ee44fd3c30b78423f12))
* Add type annotations to wrapped grpc calls ([#554](https://github.com/googleapis/python-api-core/issues/554)) ([fc12b40](https://github.com/googleapis/python-api-core/commit/fc12b40bfc6e0c4bb313196e2e3a9c9374ce1c45))
* Add universe_domain argument to ClientOptions ([3069ef4](https://github.com/googleapis/python-api-core/commit/3069ef4b9123ddb64841cbb7bbb183b53d502e0a))
* Introduce compatibility with native namespace packages ([#561](https://github.com/googleapis/python-api-core/issues/561)) ([bd82827](https://github.com/googleapis/python-api-core/commit/bd82827108f1eeb6c05cfacf6c044b2afacc18a2))


### Bug Fixes

* Fix regression in `bidi` causing `Thread-ConsumeBidirectionalStream caught unexpected exception  and will exit` ([#562](https://github.com/googleapis/python-api-core/issues/562)) ([40c8ae0](https://github.com/googleapis/python-api-core/commit/40c8ae0cf1f797e31e106461164e22db4fb2d3d9))
* Replace deprecated `datetime.datetime.utcnow()` ([#552](https://github.com/googleapis/python-api-core/issues/552)) ([448923a](https://github.com/googleapis/python-api-core/commit/448923acf277a70e8704c949311bf4feaef8cab6)), closes [#540](https://github.com/googleapis/python-api-core/issues/540)

## [2.14.0](https://github.com/googleapis/python-api-core/compare/v2.13.1...v2.14.0) (2023-11-09)


### Features

* Support with_call for wrapped rpcs ([#550](https://github.com/googleapis/python-api-core/issues/550)) ([01a57a7](https://github.com/googleapis/python-api-core/commit/01a57a745f4c8345c9c93412c27dd416b49f5953))

## [2.13.1](https://github.com/googleapis/python-api-core/compare/v2.13.0...v2.13.1) (2023-11-09)


### Bug Fixes

* Update async client to use async retry ([#544](https://github.com/googleapis/python-api-core/issues/544)) ([f21bb32](https://github.com/googleapis/python-api-core/commit/f21bb32b8e6310116a642a6e6b6dd8e44e30e656))

## [2.13.0](https://github.com/googleapis/python-api-core/compare/v2.12.0...v2.13.0) (2023-11-03)


### Features

* Add caching to routing header calculation ([#526](https://github.com/googleapis/python-api-core/issues/526)) ([6251eab](https://github.com/googleapis/python-api-core/commit/6251eab3fca5f7e509cb9b6e476ce1184094b711))


### Bug Fixes

* Add warning to retry target to avoid incorrect usage ([#543](https://github.com/googleapis/python-api-core/issues/543)) ([bfb40e6](https://github.com/googleapis/python-api-core/commit/bfb40e6929ef47be7a6464d2f1e0d06595736b8d))
* Drop usage of distutils ([#541](https://github.com/googleapis/python-api-core/issues/541)) ([4bd9e10](https://github.com/googleapis/python-api-core/commit/4bd9e10f20eea227c88e3e1496010cca6dd8a270))
* Ensure exception is available when BackgroundConsumer open stream fails ([#357](https://github.com/googleapis/python-api-core/issues/357)) ([405272c](https://github.com/googleapis/python-api-core/commit/405272c05f8c6d20e242c6172b01f78f0fd3bf32))

## [2.12.0](https://github.com/googleapis/python-api-core/compare/v2.11.1...v2.12.0) (2023-09-07)


### Features

* Add a little bit of typing to google.api_core.retry ([#453](https://github.com/googleapis/python-api-core/issues/453)) ([2477ab9](https://github.com/googleapis/python-api-core/commit/2477ab9ea5c2e863a493fb7ebebaa429a44ea096))
* Add grpc Compression argument to channels and methods ([#451](https://github.com/googleapis/python-api-core/issues/451)) ([bdebd63](https://github.com/googleapis/python-api-core/commit/bdebd6331f9c0d3d1a8ceaf274f07d2ed75bfe92))


### Documentation

* Fix a typo in google/api_core/page_iterator.py ([#511](https://github.com/googleapis/python-api-core/issues/511)) ([c0ce73c](https://github.com/googleapis/python-api-core/commit/c0ce73c4de53ad694fe36d17408998aa1230398f))

## [2.11.1](https://github.com/googleapis/python-api-core/compare/v2.11.0...v2.11.1) (2023-06-12)


### Bug Fixes

* Add actionable errors for GCE long running operations ([#498](https://github.com/googleapis/python-api-core/issues/498)) ([7dfc3a7](https://github.com/googleapis/python-api-core/commit/7dfc3a7a439243f05238a11b68a31720fde1769e))
* Invalid `dev` version identifiers in `setup.py` ([#505](https://github.com/googleapis/python-api-core/issues/505)) ([8844edb](https://github.com/googleapis/python-api-core/commit/8844edb1e802040810918a12bc9ff89104da38d4))

## [2.11.0](https://github.com/googleapis/python-api-core/compare/v2.10.2...v2.11.0) (2022-11-10)


### Features

* Add support for Python 3.11 ([#466](https://github.com/googleapis/python-api-core/issues/466)) ([ff379e3](https://github.com/googleapis/python-api-core/commit/ff379e304c353bcab734e1c4706b74b356a1e932))
* Allow representing enums with their unqualified symbolic names in headers ([#465](https://github.com/googleapis/python-api-core/issues/465)) ([522b98e](https://github.com/googleapis/python-api-core/commit/522b98ecc1ebd1c2280d3d7c73a02f6e4fb528d4))


### Bug Fixes

* Major refactoring of Polling, Retry and Timeout logic ([#462](https://github.com/googleapis/python-api-core/issues/462)) ([434253d](https://github.com/googleapis/python-api-core/commit/434253de16d9efdf984ddb64c409706cda1d5f82))
* Require google-auth &gt;= 2.14.1 ([#463](https://github.com/googleapis/python-api-core/issues/463)) ([7cc329f](https://github.com/googleapis/python-api-core/commit/7cc329fe1498b0a4285123448e4ea80c6a780d47))

## [2.10.2](https://github.com/googleapis/python-api-core/compare/v2.10.1...v2.10.2) (2022-10-08)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#459](https://github.com/googleapis/python-api-core/issues/459)) ([e949364](https://github.com/googleapis/python-api-core/commit/e949364ce3a2c4c3cdb2658054d4793aa942d999))

## [2.10.1](https://github.com/googleapis/python-api-core/compare/v2.10.0...v2.10.1) (2022-09-14)


### Bug Fixes

* Improve transcoding error message ([#442](https://github.com/googleapis/python-api-core/issues/442)) ([538df80](https://github.com/googleapis/python-api-core/commit/538df80ed6d21f43b512a73853935f7a7b9bdf52))

## [2.10.0](https://github.com/googleapis/python-api-core/compare/v2.9.0...v2.10.0) (2022-09-02)


### Features

* Add 'strict' to flatten_query_params to lower-case bools ([#433](https://github.com/googleapis/python-api-core/issues/433)) ([83678e9](https://github.com/googleapis/python-api-core/commit/83678e94e1081f9087b19c43f26fad4774184d66))

## [2.9.0](https://github.com/googleapis/python-api-core/compare/v2.8.2...v2.9.0) (2022-09-01)


### Features

* Make grpc transcode logic work in terms of protobuf python objects ([#428](https://github.com/googleapis/python-api-core/issues/428)) ([c3ad8ea](https://github.com/googleapis/python-api-core/commit/c3ad8ea67447e3d8a1154d7a9221e116f60d425a))


### Bug Fixes

* Require python 3.7+ ([#410](https://github.com/googleapis/python-api-core/issues/410)) ([7ddb8c0](https://github.com/googleapis/python-api-core/commit/7ddb8c00e6be7ab6905a9a802ad1c3063fbfa46c))
* Restore support for grpcio-gcp ([#418](https://github.com/googleapis/python-api-core/issues/418)) ([8c19609](https://github.com/googleapis/python-api-core/commit/8c19609d6244930bd91fd5f40ef9b5b65584c4a5))

## [2.8.2](https://github.com/googleapis/python-api-core/compare/v2.8.1...v2.8.2) (2022-06-13)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#400](https://github.com/googleapis/python-api-core/issues/400)) ([8f73d2e](https://github.com/googleapis/python-api-core/commit/8f73d2ee2d3af2201f877aa7e2f7361147759dc7))
* drop support for grpc-gcp ([#401](https://github.com/googleapis/python-api-core/issues/401)) ([5da6733](https://github.com/googleapis/python-api-core/commit/5da6733a475c436efc11b14889af73b3a0e20379))


### Documentation

* fix changelog header to consistent size ([#394](https://github.com/googleapis/python-api-core/issues/394)) ([ac266e9](https://github.com/googleapis/python-api-core/commit/ac266e935bc4e7c6dff250384407e7a60d8dba90))
* Fix typo in the BackgroundConsumer docstring ([#395](https://github.com/googleapis/python-api-core/issues/395)) ([0eb727f](https://github.com/googleapis/python-api-core/commit/0eb727f92314db3c4383754514f75a49ba02e27b))

## [2.8.1](https://github.com/googleapis/python-api-core/compare/v2.8.0...v2.8.1) (2022-05-26)


### Bug Fixes

* **deps:** require googleapis-common-protos >= 1.56.2 ([d84d66c](https://github.com/googleapis/python-api-core/commit/d84d66c2a4107f5f9a20c53e870a27fb1250ea3d))
* **deps:** require protobuf>= 3.15.0, <4.0.0dev ([#385](https://github.com/googleapis/python-api-core/issues/385)) ([d84d66c](https://github.com/googleapis/python-api-core/commit/d84d66c2a4107f5f9a20c53e870a27fb1250ea3d))

## [2.8.0](https://github.com/googleapis/python-api-core/compare/v2.7.3...v2.8.0) (2022-05-18)


### Features

* adds support for audience in client_options ([#379](https://github.com/googleapis/python-api-core/issues/379)) ([c97c498](https://github.com/googleapis/python-api-core/commit/c97c4980125a86f384cdf12720df7bb1a2adf9d2))
* adds support for audience in client_options. ([c97c498](https://github.com/googleapis/python-api-core/commit/c97c4980125a86f384cdf12720df7bb1a2adf9d2))

## [2.7.3](https://github.com/googleapis/python-api-core/compare/v2.7.2...v2.7.3) (2022-04-29)


### Bug Fixes

* Avoid AttributeError if grpcio-status is not installed ([#370](https://github.com/googleapis/python-api-core/issues/370)) ([022add1](https://github.com/googleapis/python-api-core/commit/022add16266f9c07f0f88eea13472cc2e0bfc991))

## [2.7.2](https://github.com/googleapis/python-api-core/compare/v2.7.1...v2.7.2) (2022-04-13)


### Bug Fixes

* allow grpc without grpcio-status ([#355](https://github.com/googleapis/python-api-core/issues/355)) ([112049e](https://github.com/googleapis/python-api-core/commit/112049e79f5a5b0a989d85d438a1bd29485f46f7))
* remove dependency on pkg_resources ([#361](https://github.com/googleapis/python-api-core/issues/361)) ([523dbd0](https://github.com/googleapis/python-api-core/commit/523dbd0b10d37ffcf83fa751f0bad313f162abf1))

## [2.7.1](https://github.com/googleapis/python-api-core/compare/v2.7.0...v2.7.1) (2022-03-09)


### Bug Fixes

* add more context to error message. ([#340](https://github.com/googleapis/python-api-core/issues/340)) ([0680fb4](https://github.com/googleapis/python-api-core/commit/0680fb4d3e013fe2de27e0a2ae2cd9896479e596))

## [2.7.0](https://github.com/googleapis/python-api-core/compare/v2.6.1...v2.7.0) (2022-03-08)


### Features

* expose extra fields in ExtendedOperation ([#351](https://github.com/googleapis/python-api-core/issues/351)) ([9abc6f4](https://github.com/googleapis/python-api-core/commit/9abc6f48f23c87b9771dca3c96b4f6af39620a50))

## [2.6.1](https://github.com/googleapis/python-api-core/compare/v2.6.0...v2.6.1) (2022-03-05)


### Bug Fixes

* Remove py2 tag from wheel ([#343](https://github.com/googleapis/python-api-core/issues/343)) ([7e21e9e](https://github.com/googleapis/python-api-core/commit/7e21e9e34892472a34f9b44175fa761f0e3fd9ed))

## [2.6.0](https://github.com/googleapis/python-api-core/compare/v2.5.0...v2.6.0) (2022-03-03)


### Features

* initial support for Extended Operations ([#344](https://github.com/googleapis/python-api-core/issues/344)) ([021bb7d](https://github.com/googleapis/python-api-core/commit/021bb7d5bf0a1d8ac58dbf0c738fac309135ba7d))

## [2.5.0](https://github.com/googleapis/python-api-core/compare/v2.4.0...v2.5.0) (2022-02-02)


### Features

* add api_key to client options ([#248](https://github.com/googleapis/python-api-core/issues/248)) ([5e5ad37](https://github.com/googleapis/python-api-core/commit/5e5ad37b8161109d65b0fab43636f7424e570fa3))


### Bug Fixes

* **deps:** remove setuptools from dependencies ([#339](https://github.com/googleapis/python-api-core/issues/339)) ([c782f29](https://github.com/googleapis/python-api-core/commit/c782f294b50b078f01959627fb82aa4c5efec333))


### Documentation

* fix typo in library name ([#332](https://github.com/googleapis/python-api-core/issues/332)) ([f267111](https://github.com/googleapis/python-api-core/commit/f267111823545a6c67ef5f10b85cd8c2fab8a612))

## [2.4.0](https://www.github.com/googleapis/python-api-core/compare/v2.3.2...v2.4.0) (2022-01-11)


### Features

* add support for 'error_info' ([#315](https://www.github.com/googleapis/python-api-core/issues/315)) ([cc46aa6](https://www.github.com/googleapis/python-api-core/commit/cc46aa68ec184871330d16a6c767f57a4f0eb633))
* iterator for processing JSON responses in REST streaming. ([#317](https://www.github.com/googleapis/python-api-core/issues/317)) ([f9f2696](https://www.github.com/googleapis/python-api-core/commit/f9f26969842b456ea372bed941d712b7a9ab7239))

## [2.3.2](https://www.github.com/googleapis/python-api-core/compare/v2.3.1...v2.3.2) (2021-12-16)


### Bug Fixes

* address broken wheels in version 2.3.1

## [2.3.1](https://www.github.com/googleapis/python-api-core/compare/v2.3.0...v2.3.1) (2021-12-15)


### Bug Fixes
* exclude function target from retry deadline exceeded exception message ([#318](https://www.github.com/googleapis/python-api-core/issues/318)) ([34ebdcc](https://www.github.com/googleapis/python-api-core/commit/34ebdcc251d4f3d7d496e8e0b78847645a06650b))

## [2.3.0](https://www.github.com/googleapis/python-api-core/compare/v2.2.2...v2.3.0) (2021-11-25)


### Features

* add operations rest client to support long-running operations. ([#311](https://www.github.com/googleapis/python-api-core/issues/311)) ([ce1adf3](https://www.github.com/googleapis/python-api-core/commit/ce1adf395982ede157c0f25a920946bb52789873))


### Bug Fixes

* handle bare 'grpc.Call' in 'from_grpc_error' ([#298](https://www.github.com/googleapis/python-api-core/issues/298)) ([060b339](https://www.github.com/googleapis/python-api-core/commit/060b339e3af296dd1772bfc1b4a0d2b4264cae1f))

## [2.2.2](https://www.github.com/googleapis/python-api-core/compare/v2.2.1...v2.2.2) (2021-11-02)


### Bug Fixes

* make 'gapic_v1.method.DEFAULT' a typed object ([#292](https://www.github.com/googleapis/python-api-core/issues/292)) ([ffc51f0](https://www.github.com/googleapis/python-api-core/commit/ffc51f03c7ce5d9f009ba859b8df385d52925578))

## [2.2.1](https://www.github.com/googleapis/python-api-core/compare/v2.2.0...v2.2.1) (2021-10-26)


### Bug Fixes

* revert "fix: do not error on LROs with no response or error" ([#294](https://www.github.com/googleapis/python-api-core/issues/294)) ([9e6091e](https://www.github.com/googleapis/python-api-core/commit/9e6091ee59a30e72a6278b369f6a08e7aef32f22))

## [2.2.0](https://www.github.com/googleapis/python-api-core/compare/v2.1.1...v2.2.0) (2021-10-25)


### Features

* add 'GoogleAPICallError.error_details' property ([#286](https://www.github.com/googleapis/python-api-core/issues/286)) ([ef6f0fc](https://www.github.com/googleapis/python-api-core/commit/ef6f0fcfdfe771172056e35e3c990998b3b00416))

## [2.1.1](https://www.github.com/googleapis/python-api-core/compare/v2.1.0...v2.1.1) (2021-10-13)


### Bug Fixes

* add mypy checking + 'py.typed' file ([#290](https://www.github.com/googleapis/python-api-core/issues/290)) ([0023ee1](https://www.github.com/googleapis/python-api-core/commit/0023ee1fe0e8b80c7a9e8987e0f322a829e5d613))

## [2.1.0](https://www.github.com/googleapis/python-api-core/compare/v2.0.1...v2.1.0) (2021-10-05)


### Features

* add grpc transcoding + tests ([#259](https://www.github.com/googleapis/python-api-core/issues/259)) ([afe0fa1](https://www.github.com/googleapis/python-api-core/commit/afe0fa14c21289c8244606a9f81544cff8ac5f7c))
* Add helper function to format query_params for rest transport. ([#275](https://www.github.com/googleapis/python-api-core/issues/275)) ([1c5eb4d](https://www.github.com/googleapis/python-api-core/commit/1c5eb4df93d78e791082d9282330ebf0faacd222))
* add support for Python 3.10 ([#284](https://www.github.com/googleapis/python-api-core/issues/284)) ([a422a5d](https://www.github.com/googleapis/python-api-core/commit/a422a5d72cb6f363d57e7a4effe421ba8e049cde))

## [2.0.1](https://www.github.com/googleapis/python-api-core/compare/v2.0.0...v2.0.1) (2021-08-31)


### Bug Fixes

* do not error on LROs with no response or error ([#258](https://www.github.com/googleapis/python-api-core/issues/258)) ([618f192](https://www.github.com/googleapis/python-api-core/commit/618f19201af729205892fcecd9c8e315ba3174a3))

## [2.0.0](https://www.github.com/googleapis/python-api-core/compare/v2.0.0-b1...v2.0.0) (2021-08-18)

### ⚠ BREAKING CHANGES

* drop support for Python 2.7 / 3.5 ([#212](https://www.github.com/googleapis/python-api-core/issues/212)) ([a30f004](https://www.github.com/googleapis/python-api-core/commit/a30f004e74f709d46e905dd819c71f43354e9ac9))

### Bug Fixes

* bump grpcio version to use stable aio API ([#234](https://www.github.com/googleapis/python-api-core/issues/234)) ([bdbf889](https://www.github.com/googleapis/python-api-core/commit/bdbf889210b709d7c1945f2160bcba9161b4dd2e))
* strip trailing _ from field mask paths ([#228](https://www.github.com/googleapis/python-api-core/issues/228)) ([ff6ef1b](https://www.github.com/googleapis/python-api-core/commit/ff6ef1bd07fa68307b7c82c910416d770e7b3416))

## [2.0.0b1](https://www.github.com/googleapis/python-api-core/compare/v1.31.1...v2.0.0b1) (2021-08-03)


### ⚠ BREAKING CHANGES

* drop support for Python 2.7 / 3.5 ([#212](https://www.github.com/googleapis/python-api-core/issues/212)) ([a30f004](https://www.github.com/googleapis/python-api-core/commit/a30f004e74f709d46e905dd819c71f43354e9ac9))

### Bug Fixes

* strip trailing _ from field mask paths ([#228](https://www.github.com/googleapis/python-api-core/issues/228)) ([ff6ef1b](https://www.github.com/googleapis/python-api-core/commit/ff6ef1bd07fa68307b7c82c910416d770e7b3416))

## [1.31.1](https://www.github.com/googleapis/python-api-core/compare/v1.31.0...v1.31.1) (2021-07-26)


### Bug Fixes

* add 'requests.exceptions.ChunkedEncodingError' to retryable exceptions ([#237](https://www.github.com/googleapis/python-api-core/issues/237)) ([5e540f2](https://www.github.com/googleapis/python-api-core/commit/5e540f28493cc3e13260458a8d1c6a1abb2ed313))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#229](https://www.github.com/googleapis/python-api-core/issues/229)) ([a12c051](https://www.github.com/googleapis/python-api-core/commit/a12c0516c42918b05415835029717814353b883b))

## [1.31.0](https://www.github.com/googleapis/python-api-core/compare/v1.30.0...v1.31.0) (2021-07-07)


### Features

* add ServiceUnavailable exception to polling retries ([#184](https://www.github.com/googleapis/python-api-core/issues/184)) ([11032cf](https://www.github.com/googleapis/python-api-core/commit/11032cf08ecc16dd252a6cda8b33b0b28ec4f4ba))


### Bug Fixes

* undprecate entity factory helpers ([#101](https://www.github.com/googleapis/python-api-core/issues/101)) ([1fbee03](https://www.github.com/googleapis/python-api-core/commit/1fbee03495a136eef3d6aaa5ea0aadd6e4b58e8b)), closes [#100](https://www.github.com/googleapis/python-api-core/issues/100)

## [1.30.0](https://www.github.com/googleapis/python-api-core/compare/v1.29.0...v1.30.0) (2021-06-08)


### Features

* add iterator capability to paged iterators ([#200](https://www.github.com/googleapis/python-api-core/issues/200)) ([3487d68](https://www.github.com/googleapis/python-api-core/commit/3487d68bdab6f20e2ab931c8283f63c94862cf31))

## [1.29.0](https://www.github.com/googleapis/python-api-core/compare/v1.28.0...v1.29.0) (2021-06-02)


### Features

* HTTPIterator now accepts a page_size parameter to control page … ([#197](https://www.github.com/googleapis/python-api-core/issues/197)) ([a421913](https://www.github.com/googleapis/python-api-core/commit/a4219137a5bfcf2a6f44780ecdbf475c1129e461))


### Documentation

* fix broken links in multiprocessing.rst ([#195](https://www.github.com/googleapis/python-api-core/issues/195)) ([8d8bc51](https://www.github.com/googleapis/python-api-core/commit/8d8bc5150ee5543b4aeb2c271da034a5305d1436))

## [1.28.0](https://www.github.com/googleapis/python-api-core/compare/v1.27.0...v1.28.0) (2021-05-20)


### Bug Fixes

* require google-auth>=1.25.0 ([#190](https://www.github.com/googleapis/python-api-core/issues/190)) ([155da5e](https://www.github.com/googleapis/python-api-core/commit/155da5e18cc2fdcfa57de6f956b7d078e79cd4b7))


### Miscellaneous Chores

* release 1.28.0 ([#192](https://www.github.com/googleapis/python-api-core/issues/192)) ([11b5da4](https://www.github.com/googleapis/python-api-core/commit/11b5da426a842541ca2b861d3387fc312b3f5b60))

## [1.27.0](https://www.github.com/googleapis/python-api-core/compare/v1.26.3...v1.27.0) (2021-05-18)


### Features

* Add support for `rest/` token in `x-goog-api-client` header ([#189](https://www.github.com/googleapis/python-api-core/issues/189)) ([15aca6b](https://www.github.com/googleapis/python-api-core/commit/15aca6b288b2ec5ce0251e442e1dfa7f52e1b124))
* retry google.auth TransportError and requests ConnectionError ([#178](https://www.github.com/googleapis/python-api-core/issues/178)) ([6ae04a8](https://www.github.com/googleapis/python-api-core/commit/6ae04a8d134fffe13f06081e15f9723c1b2ea334))

## [1.26.3](https://www.github.com/googleapis/python-api-core/compare/v1.26.2...v1.26.3) (2021-03-25)


### Bug Fixes

* skip empty policy bindings in `len()` and `iter()` ([#159](https://www.github.com/googleapis/python-api-core/issues/159)) ([9eaa786](https://www.github.com/googleapis/python-api-core/commit/9eaa7868164a7e98792de24d2be97f79fba22322))


### Documentation

* update python contributing guide ([#147](https://www.github.com/googleapis/python-api-core/issues/147)) ([1d76b57](https://www.github.com/googleapis/python-api-core/commit/1d76b57d1f218f7885f85dc7c052bad1ad3857ac))

## [1.26.2](https://www.github.com/googleapis/python-api-core/compare/v1.26.1...v1.26.2) (2021-03-23)


### Bug Fixes

* save empty IAM policy bindings ([#155](https://www.github.com/googleapis/python-api-core/issues/155)) ([536c2ca](https://www.github.com/googleapis/python-api-core/commit/536c2cad814b8fa8cd346a3d7bd5f6b9889c4a6f))

## [1.26.1](https://www.github.com/googleapis/python-api-core/compare/v1.26.0...v1.26.1) (2021-02-12)


### Bug Fixes

* add operation name to x-goog-request-params in async client ([#137](https://www.github.com/googleapis/python-api-core/issues/137)) ([7271b23](https://www.github.com/googleapis/python-api-core/commit/7271b23afddb032e49e957525704d0cd5bfa4c65))

## [1.26.0](https://www.github.com/googleapis/python-api-core/compare/v1.25.1...v1.26.0) (2021-02-08)


### Features

* allow default_host and default_scopes to be passed to create_channel ([#134](https://www.github.com/googleapis/python-api-core/issues/134)) ([94c76e0](https://www.github.com/googleapis/python-api-core/commit/94c76e0873e5b2f42331d5b1ad286c1e63b61395))

## [1.25.1](https://www.github.com/googleapis/python-api-core/compare/v1.25.0...v1.25.1) (2021-01-25)


### Bug Fixes

* add operation name to x-goog-request-params ([#133](https://www.github.com/googleapis/python-api-core/issues/133)) ([97cef4a](https://www.github.com/googleapis/python-api-core/commit/97cef4ad1db55938715f9ac8000d1b0ad1e71873))


### Documentation

* fix spelling errors in retry ([#131](https://www.github.com/googleapis/python-api-core/issues/131)) ([232dab0](https://www.github.com/googleapis/python-api-core/commit/232dab0ad3ef2cca0edfe707d8f90ca0ea200ba2))

## [1.25.0](https://www.github.com/googleapis/python-api-core/compare/v1.24.1...v1.25.0) (2021-01-14)


### Features

* allow gRPC metadata to be passed to operations client ([#127](https://www.github.com/googleapis/python-api-core/issues/127)) ([73854e8](https://www.github.com/googleapis/python-api-core/commit/73854e897b885e9be290f2676a8a1466b4f041e4))


### Documentation

* **python:** document adding Python 3.9 support, dropping 3.5 support ([#120](https://www.github.com/googleapis/python-api-core/issues/120)) ([b51b7f5](https://www.github.com/googleapis/python-api-core/commit/b51b7f587042fe9340371c1b5c8e9adf8001c43a)), closes [#787](https://www.github.com/googleapis/python-api-core/issues/787)

## [1.24.1](https://www.github.com/googleapis/python-api-core/compare/v1.24.0...v1.24.1) (2020-12-16)


### Bug Fixes

* support 'retry' for ops built from HTTP/gRPC responses ([#115](https://www.github.com/googleapis/python-api-core/issues/115)) ([7a38243](https://www.github.com/googleapis/python-api-core/commit/7a38243c351b228d103eee81fc5ae521ad1c930e)), closes [#87](https://www.github.com/googleapis/python-api-core/issues/87)

## [1.24.0](https://www.github.com/googleapis/python-api-core/compare/v1.23.0...v1.24.0) (2020-12-14)


### Features

* add support for Python 3.9, drop support for Python 3.5 ([#111](https://www.github.com/googleapis/python-api-core/issues/111)) ([fdbed0f](https://www.github.com/googleapis/python-api-core/commit/fdbed0f0cbae8de21c73338a6817f8aa79cef4c9)), closes [#110](https://www.github.com/googleapis/python-api-core/issues/110)


### Documentation

* explain how to create credentials from dict ([#109](https://www.github.com/googleapis/python-api-core/issues/109)) ([5dce6d6](https://www.github.com/googleapis/python-api-core/commit/5dce6d61e7324a415c1b3ceaeec1ce1b5f1ea189))

## [1.23.0](https://www.github.com/googleapis/python-api-core/compare/v1.22.4...v1.23.0) (2020-10-16)


### Features

* **api-core:** pass retry from result() to done() ([#9](https://www.github.com/googleapis/python-api-core/issues/9)) ([6623b31](https://www.github.com/googleapis/python-api-core/commit/6623b31a2040b834be808d711fa397dc428f1837))


### Bug Fixes

*  map LRO errors to library exception types ([#86](https://www.github.com/googleapis/python-api-core/issues/86)) ([a855339](https://www.github.com/googleapis/python-api-core/commit/a85533903c57be4809fe76435e298409e0903931)), closes [#15](https://www.github.com/googleapis/python-api-core/issues/15)
* harden install to use full paths, and windows separators on windows ([#88](https://www.github.com/googleapis/python-api-core/issues/88)) ([db8e636](https://www.github.com/googleapis/python-api-core/commit/db8e636f545a8872f959e3f403cfec30ffed6c34))
* update out-of-date comment in exceptions.py ([#93](https://www.github.com/googleapis/python-api-core/issues/93)) ([70ebe42](https://www.github.com/googleapis/python-api-core/commit/70ebe42601b3d088b3421233ef7d8245229b7265))

## [1.22.4](https://www.github.com/googleapis/python-api-core/compare/v1.22.3...v1.22.4) (2020-10-05)


### Bug Fixes

* use version.py instead of pkg_resources.get_distribution ([#80](https://www.github.com/googleapis/python-api-core/issues/80)) ([d480d97](https://www.github.com/googleapis/python-api-core/commit/d480d97e41cd6705325b3b649360553a83c23f47))

## [1.22.3](https://www.github.com/googleapis/python-api-core/compare/v1.22.2...v1.22.3) (2020-10-02)


### Bug Fixes

* **deps:** require six >= 1.13.0 ([#78](https://www.github.com/googleapis/python-api-core/issues/78)) ([a7a8b98](https://www.github.com/googleapis/python-api-core/commit/a7a8b98602a3eb277fdc607ac69f3bcb147f3351)), closes [/github.com/benjaminp/six/blob/c0be8815d13df45b6ae471c4c436cce8c192245d/CHANGES#L30-L31](https://www.github.com/googleapis//github.com/benjaminp/six/blob/c0be8815d13df45b6ae471c4c436cce8c192245d/CHANGES/issues/L30-L31)

## [1.22.2](https://www.github.com/googleapis/python-api-core/compare/v1.22.1...v1.22.2) (2020-09-03)


### Bug Fixes

* only add quota project id if supported ([#75](https://www.github.com/googleapis/python-api-core/issues/75)) ([8f8ee78](https://www.github.com/googleapis/python-api-core/commit/8f8ee7879e4f834f3c676e535ffc41b5b9b2de62))

## [1.22.1](https://www.github.com/googleapis/python-api-core/compare/v1.22.0...v1.22.1) (2020-08-12)


### Documentation

* fix spelling errors for amount in retry ([#69](https://www.github.com/googleapis/python-api-core/issues/69)) ([7bb713d](https://www.github.com/googleapis/python-api-core/commit/7bb713d13b1fe3cca58263f5e499136a84abc456))

## [1.22.0](https://www.github.com/googleapis/python-api-core/compare/v1.21.0...v1.22.0) (2020-07-21)


### Features

* allow quota project to be passed to create_channel ([#58](https://www.github.com/googleapis/python-api-core/issues/58)) ([e2d9a7b](https://www.github.com/googleapis/python-api-core/commit/e2d9a7b209b7dfab300dc848fabbae8f42a2ab19))


### Bug Fixes

* _determine_timeout problem handling float type timeout ([#64](https://www.github.com/googleapis/python-api-core/issues/64)) ([2010373](https://www.github.com/googleapis/python-api-core/commit/2010373b27536d1191175624b297a709d70153fa))


### Documentation

* change the documentation for using 'six.moves.collections_abc.Mapping' instead of 'dict' in 'client_options.from_dict()' ([#53](https://www.github.com/googleapis/python-api-core/issues/53)) ([c890675](https://www.github.com/googleapis/python-api-core/commit/c890675dc9ebc084f105be81dc81c048f4f599ea))

## [1.21.0](https://www.github.com/googleapis/python-api-core/compare/v1.20.1...v1.21.0) (2020-06-18)


### Features

* allow credentials files to be passed for channel creation ([#50](https://www.github.com/googleapis/python-api-core/issues/50)) ([ded92d0](https://www.github.com/googleapis/python-api-core/commit/ded92d0acdcde4295d0e5df05fda0d83783a3991))

## [1.20.1](https://www.github.com/googleapis/python-api-core/compare/v1.20.0...v1.20.1) (2020-06-16)


### Bug Fixes

* **dependencies:** increase protobuf version ([#49](https://www.github.com/googleapis/python-api-core/issues/49)) ([1ba6095](https://www.github.com/googleapis/python-api-core/commit/1ba609592968c9d828449b89a3ade3bcaf5edd7f)), closes [#48](https://www.github.com/googleapis/python-api-core/issues/48)

## [1.20.0](https://www.github.com/googleapis/python-api-core/compare/v1.19.1...v1.20.0) (2020-06-09)


### Features

* allow disabling response stream pre-fetch ([#30](https://www.github.com/googleapis/python-api-core/issues/30)) ([74e0b0f](https://www.github.com/googleapis/python-api-core/commit/74e0b0f8387207933c120af15b2bb5d175dd8f84)), closes [#25](https://www.github.com/googleapis/python-api-core/issues/25)

## [1.19.1](https://www.github.com/googleapis/python-api-core/compare/v1.19.0...v1.19.1) (2020-06-06)


### Bug Fixes

* bump up grpcio minimum version to 1.29.0 ([#41](https://www.github.com/googleapis/python-api-core/issues/41)) ([4b11422](https://www.github.com/googleapis/python-api-core/commit/4b114221b3ae01eee540bedf47381c3b7c214b0c))

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
