# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery-storage/#history

## [2.19.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.18.1...v2.19.0) (2023-03-01)


### Features

* Add default_value_expression to TableFieldSchema ([#571](https://github.com/googleapis/python-bigquery-storage/issues/571)) ([277ed54](https://github.com/googleapis/python-bigquery-storage/commit/277ed5437d63f18b9a46eb89d28cfa3704ecb24e))

## [2.18.1](https://github.com/googleapis/python-bigquery-storage/compare/v2.18.0...v2.18.1) (2023-01-20)


### Bug Fixes

* Add context manager return types ([ec04714](https://github.com/googleapis/python-bigquery-storage/commit/ec04714195a1fd13db626631d69124a6415977d3))


### Documentation

* Add documentation for enums ([ec04714](https://github.com/googleapis/python-bigquery-storage/commit/ec04714195a1fd13db626631d69124a6415977d3))

## [2.18.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.17.0...v2.18.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#547](https://github.com/googleapis/python-bigquery-storage/issues/547)) ([7201f67](https://github.com/googleapis/python-bigquery-storage/commit/7201f67733d831622f36f454465f1a95ff42d17a))

## [2.17.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.16.2...v2.17.0) (2022-12-14)


### Features

* Add estimated number of rows to CreateReadSession response ([#542](https://github.com/googleapis/python-bigquery-storage/issues/542)) ([16c19a4](https://github.com/googleapis/python-bigquery-storage/commit/16c19a45b8172e64fb8e7c1d68ecf6a1c73048f9))
* Add missing_value_interpretations to AppendRowsRequest ([#529](https://github.com/googleapis/python-bigquery-storage/issues/529)) ([2ba8bae](https://github.com/googleapis/python-bigquery-storage/commit/2ba8bae95356f04010bd099b1cebe38d0a6378d5))


### Bug Fixes

* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([5e2fc1e](https://github.com/googleapis/python-bigquery-storage/commit/5e2fc1e8db4f76110aa70413838d710e64093b13))
* Drop usage of pkg_resources ([5e2fc1e](https://github.com/googleapis/python-bigquery-storage/commit/5e2fc1e8db4f76110aa70413838d710e64093b13))
* Fix timeout default values ([5e2fc1e](https://github.com/googleapis/python-bigquery-storage/commit/5e2fc1e8db4f76110aa70413838d710e64093b13))


### Documentation

* **samples:** Snippetgen should call await on the operation coroutine before calling result ([5e2fc1e](https://github.com/googleapis/python-bigquery-storage/commit/5e2fc1e8db4f76110aa70413838d710e64093b13))

## [2.16.2](https://github.com/googleapis/python-bigquery-storage/compare/v2.16.1...v2.16.2) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#522](https://github.com/googleapis/python-bigquery-storage/issues/522)) ([cbe3fef](https://github.com/googleapis/python-bigquery-storage/commit/cbe3fef5b1df55bb8b58fb399d119a0439c872c6))

## [2.16.1](https://github.com/googleapis/python-bigquery-storage/compare/v2.16.0...v2.16.1) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#517](https://github.com/googleapis/python-bigquery-storage/issues/517)) ([53d72c7](https://github.com/googleapis/python-bigquery-storage/commit/53d72c7bf8fbe63bc1ea769ed4d8f6e1daad5b87))

## [2.16.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.15.0...v2.16.0) (2022-09-19)


### Features

* Add location to WriteStream and add WriteStreamView support ([#507](https://github.com/googleapis/python-bigquery-storage/issues/507)) ([20371ef](https://github.com/googleapis/python-bigquery-storage/commit/20371ef91b2071cbdf0000a5fbecb7db71184fae))
* add proto annotation for non-ascii field mapping ([7eba58c](https://github.com/googleapis/python-bigquery-storage/commit/7eba58c13a770a2876b75a520f5222528f848b89))

## [2.15.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.14.2...v2.15.0) (2022-09-06)


### Features

* Allow users to set Apache Avro output format options through avro_serialization_options param in TableReadOptions message ([#490](https://github.com/googleapis/python-bigquery-storage/issues/490)) ([0c1264d](https://github.com/googleapis/python-bigquery-storage/commit/0c1264d47b6d412b11524fee484cff6473480890))

## [2.14.2](https://github.com/googleapis/python-bigquery-storage/compare/v2.14.1...v2.14.2) (2022-08-12)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#486](https://github.com/googleapis/python-bigquery-storage/issues/486)) ([e96a352](https://github.com/googleapis/python-bigquery-storage/commit/e96a3529c3fc0f971a34aa9a8e51634eb4e1ee5d))
* **deps:** drop freezegun dependency in extras ([#481](https://github.com/googleapis/python-bigquery-storage/issues/481)) ([7ba7953](https://github.com/googleapis/python-bigquery-storage/commit/7ba7953dd7b5f0fd676871064946fae8d1ceb57e))
* **deps:** require proto-plus >= 1.22.0 ([e96a352](https://github.com/googleapis/python-bigquery-storage/commit/e96a3529c3fc0f971a34aa9a8e51634eb4e1ee5d))


### Documentation

* clarify size limitations for AppendRowsRequest ([#474](https://github.com/googleapis/python-bigquery-storage/issues/474)) ([7132617](https://github.com/googleapis/python-bigquery-storage/commit/7132617ec15eba7855dac33b4757f6d63cc80aba))

## [2.14.1](https://github.com/googleapis/python-bigquery-storage/compare/v2.14.0...v2.14.1) (2022-07-13)


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#469](https://github.com/googleapis/python-bigquery-storage/issues/469)) ([42f7a0d](https://github.com/googleapis/python-bigquery-storage/commit/42f7a0db343a47aa9fe4f3c55688480a8537def4))

## [2.14.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.13.2...v2.14.0) (2022-07-08)


### Features

* add audience parameter ([346c719](https://github.com/googleapis/python-bigquery-storage/commit/346c7199e2bd85c77403f1288988c2d64b435ee8))
* add fields to eventually contain row level errors ([346c719](https://github.com/googleapis/python-bigquery-storage/commit/346c7199e2bd85c77403f1288988c2d64b435ee8))


### Bug Fixes

* **deps:** require google-api-core >= 2.8.0 ([346c719](https://github.com/googleapis/python-bigquery-storage/commit/346c7199e2bd85c77403f1288988c2d64b435ee8))
* handle AttributeError in bigquery_storage writer ([#414](https://github.com/googleapis/python-bigquery-storage/issues/414)) ([2cb641a](https://github.com/googleapis/python-bigquery-storage/commit/2cb641a7e0e8bfde23693b4f59f6b914520d7364))
* Modify client lib retry policy for CreateWriteStream with longer backoff, more error code and longer overall time ([346c719](https://github.com/googleapis/python-bigquery-storage/commit/346c7199e2bd85c77403f1288988c2d64b435ee8))
* require python 3.7+ ([#468](https://github.com/googleapis/python-bigquery-storage/issues/468)) ([c13b1e5](https://github.com/googleapis/python-bigquery-storage/commit/c13b1e5e59e8ce2794b339809ce9f6a0ba66439c))

## [2.13.2](https://github.com/googleapis/python-bigquery-storage/compare/v2.13.1...v2.13.2) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#456](https://github.com/googleapis/python-bigquery-storage/issues/456)) ([b5e7719](https://github.com/googleapis/python-bigquery-storage/commit/b5e771965088f645aab3ea01f00a50ee768bbb29))


### Documentation

* fix changelog header to consistent size ([#457](https://github.com/googleapis/python-bigquery-storage/issues/457)) ([143dac9](https://github.com/googleapis/python-bigquery-storage/commit/143dac9253501bb8f88dff93bc5924148d8c5a95))

## [2.13.1](https://github.com/googleapis/python-bigquery-storage/compare/v2.13.0...v2.13.1) (2022-04-04)


### Bug Fixes

* Deprecate format specific `row_count` field in Read API ([#424](https://github.com/googleapis/python-bigquery-storage/issues/424)) ([d52dbba](https://github.com/googleapis/python-bigquery-storage/commit/d52dbba8dd406b3432d9a151e6d80aabe45f086c))

## [2.13.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.12.0...v2.13.0) (2022-03-07)


### Features

* expose additional StorageError enum values ([4657e2f](https://github.com/googleapis/python-bigquery-storage/commit/4657e2f819febf9601dc671fda9f0b04bbcfdebe))
* update default timeout/retry information ([4657e2f](https://github.com/googleapis/python-bigquery-storage/commit/4657e2f819febf9601dc671fda9f0b04bbcfdebe))
* update parent annotation for BatchCommitWriteStreamsRequest ([4657e2f](https://github.com/googleapis/python-bigquery-storage/commit/4657e2f819febf9601dc671fda9f0b04bbcfdebe))


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#404](https://github.com/googleapis/python-bigquery-storage/issues/404)) ([99f51e0](https://github.com/googleapis/python-bigquery-storage/commit/99f51e0bbc8615e7e3caad272a5bffd0d6c57d2f))


### Documentation

* improve documentation for write client ([#403](https://github.com/googleapis/python-bigquery-storage/issues/403)) ([4657e2f](https://github.com/googleapis/python-bigquery-storage/commit/4657e2f819febf9601dc671fda9f0b04bbcfdebe))

## [2.12.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.11.0...v2.12.0) (2022-02-22)


### Features

* add api key support ([#387](https://github.com/googleapis/python-bigquery-storage/issues/387)) ([5e7b502](https://github.com/googleapis/python-bigquery-storage/commit/5e7b5023ab9d9bcfa7661a19a79f05c07cded77e))
* add trace_id for Read API ([#396](https://github.com/googleapis/python-bigquery-storage/issues/396)) ([5d7f918](https://github.com/googleapis/python-bigquery-storage/commit/5d7f9188a9ae3db7b3cfb6cc6789dcb071723166))


### Bug Fixes

* remove bigquery.readonly auth scope ([#394](https://github.com/googleapis/python-bigquery-storage/issues/394)) ([e08d2fd](https://github.com/googleapis/python-bigquery-storage/commit/e08d2fd146153709ce09af751c9437b2365313f0))
* remove libcst as a required dependency ([#389](https://github.com/googleapis/python-bigquery-storage/issues/389)) ([92b503a](https://github.com/googleapis/python-bigquery-storage/commit/92b503a4ec17f8fc8dabfc24b58ac58fe10eb57f))
* resolve DuplicateCredentialArgs error when using credentials_file ([16520e3](https://github.com/googleapis/python-bigquery-storage/commit/16520e3c3386c412bdaf545994264d66ee641588))


### Documentation

* add generated snippets ([e08d2fd](https://github.com/googleapis/python-bigquery-storage/commit/e08d2fd146153709ce09af751c9437b2365313f0))

## [2.11.0](https://github.com/googleapis/python-bigquery-storage/compare/v2.10.1...v2.11.0) (2022-01-12)


### Features

* add `write_mode` property to BigQuery Storage Write API v1 ([#360](https://github.com/googleapis/python-bigquery-storage/issues/360)) ([aa9740d](https://github.com/googleapis/python-bigquery-storage/commit/aa9740d352b2359171a3a99811f88e24ae927189))
* retryable resource exhausted handling ([#366](https://github.com/googleapis/python-bigquery-storage/issues/366)) ([33757d8](https://github.com/googleapis/python-bigquery-storage/commit/33757d88c968fef65332f5ebe0b876758f978ab0))

## [2.10.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.10.0...v2.10.1) (2021-11-11)


### Documentation

* show that Python 3.9 and 3.10 are supported in classifiers ([#351](https://www.github.com/googleapis/python-bigquery-storage/issues/351)) ([1faa16f](https://www.github.com/googleapis/python-bigquery-storage/commit/1faa16f4dbeac461ebc816949a3f88f5da97540b))

## [2.10.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.9.1...v2.10.0) (2021-11-05)


### Features

* add context manager support in client ([#328](https://www.github.com/googleapis/python-bigquery-storage/issues/328)) ([afcf3dc](https://www.github.com/googleapis/python-bigquery-storage/commit/afcf3dcece980698d4b12545bf1a0d45289e41d5))


### Bug Fixes

* **deps:** drop packaging dependency ([5390146](https://www.github.com/googleapis/python-bigquery-storage/commit/5390146e7bf83038a55755f53b119504ce000d62))
* **deps:** require google-api-core >= 1.28.0 ([5390146](https://www.github.com/googleapis/python-bigquery-storage/commit/5390146e7bf83038a55755f53b119504ce000d62))


### Documentation

* list oneofs in docstring ([5390146](https://www.github.com/googleapis/python-bigquery-storage/commit/5390146e7bf83038a55755f53b119504ce000d62))

## [2.9.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.9.0...v2.9.1) (2021-10-06)


### Documentation

* **samples:** Add minimal sample to show Write API in pending mode ([#322](https://www.github.com/googleapis/python-bigquery-storage/issues/322)) ([db51469](https://www.github.com/googleapis/python-bigquery-storage/commit/db5146980bd1a358413c56f6e090c07277bfac26))

## [2.9.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.8.0...v2.9.0) (2021-09-27)


### Features

* add `AppendRowsStream` to use write API from v1 endpoint ([#309](https://www.github.com/googleapis/python-bigquery-storage/issues/309)) ([9fc3c08](https://www.github.com/googleapis/python-bigquery-storage/commit/9fc3c08cdeebfbd69bc815f951a07b2d086b0a69))
* add BigQuery Storage Write API v1 ([#301](https://www.github.com/googleapis/python-bigquery-storage/issues/301)) ([69e3fb8](https://www.github.com/googleapis/python-bigquery-storage/commit/69e3fb8ec2ecac0417b6a4bc954004a064ae04b7))


### Bug Fixes

* add 'dict' annotation type to 'request' ([a778080](https://www.github.com/googleapis/python-bigquery-storage/commit/a7780805d7350855fccdcf2aefa596851ee83923))
* add missing read api retry setting on SplitReadStream ([#311](https://www.github.com/googleapis/python-bigquery-storage/issues/311)) ([66c09c0](https://www.github.com/googleapis/python-bigquery-storage/commit/66c09c01d643844117e3e35d2d90a6cc0491349e))
* avoid failure if closing `AppendRowsStream` before opening ([#304](https://www.github.com/googleapis/python-bigquery-storage/issues/304)) ([9f145f8](https://www.github.com/googleapis/python-bigquery-storage/commit/9f145f87d6a54e757044ff4110d2cafd57ce08fa))
* avoid opening write stream more than once, make open method private ([#305](https://www.github.com/googleapis/python-bigquery-storage/issues/305)) ([58ec844](https://www.github.com/googleapis/python-bigquery-storage/commit/58ec8444420d29c2915ec5b148de780a36eaf3e2))

## [2.8.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.7.0...v2.8.0) (2021-09-10)


### Features

* add `AppendRowsStream` helper to append rows with a `BigQueryWriteClient` ([#284](https://www.github.com/googleapis/python-bigquery-storage/issues/284)) ([2461f63](https://www.github.com/googleapis/python-bigquery-storage/commit/2461f63d37f707c2d634a95d87b8ffc3e4af3686))

## [2.7.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.3...v2.7.0) (2021-09-02)


### Features

* **v1beta2:** Align ReadRows timeout with other versions of the API ([#293](https://www.github.com/googleapis/python-bigquery-storage/issues/293)) ([43e36a1](https://www.github.com/googleapis/python-bigquery-storage/commit/43e36a13ece8d876763d88bad0252a1b2421c52a))


### Documentation

* **v1beta2:** Align session length with public documentation ([43e36a1](https://www.github.com/googleapis/python-bigquery-storage/commit/43e36a13ece8d876763d88bad0252a1b2421c52a))

## [2.6.3](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.2...v2.6.3) (2021-08-06)


### Bug Fixes

* resume read stream on `Unknown` transport-layer exception ([#263](https://www.github.com/googleapis/python-bigquery-storage/issues/263)) ([127caa0](https://www.github.com/googleapis/python-bigquery-storage/commit/127caa06144b9cec04b23914b561be6a264bcb36))

## [2.6.2](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.1...v2.6.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#249](https://www.github.com/googleapis/python-bigquery-storage/issues/249)) ([a7e8d91](https://www.github.com/googleapis/python-bigquery-storage/commit/a7e8d913fc3de67a3f38ecbd35af2f9d1a33aa8d))


### Documentation

* remove duplicate code samples ([#246](https://www.github.com/googleapis/python-bigquery-storage/issues/246)) ([303f273](https://www.github.com/googleapis/python-bigquery-storage/commit/303f2732ced38e491df92e965dd37bac24a61d2f))
* add Samples section to CONTRIBUTING.rst ([#241](https://www.github.com/googleapis/python-bigquery-storage/issues/241)) ([5d02358](https://www.github.com/googleapis/python-bigquery-storage/commit/5d02358fbd397cafcc1169d829859fe2dd568645))


## [2.6.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.0...v2.6.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#240](https://www.github.com/googleapis/python-bigquery-storage/issues/240)) ([8f848e1](https://www.github.com/googleapis/python-bigquery-storage/commit/8f848e18379085160492cdd2d12dc8de50a46c8e))


### Documentation

* pandas DataFrame samples are more standalone ([#224](https://www.github.com/googleapis/python-bigquery-storage/issues/224)) ([4026997](https://www.github.com/googleapis/python-bigquery-storage/commit/4026997d7a286b63ed2b969c0bd49de59635326d))

## [2.6.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.5.0...v2.6.0) (2021-07-09)


### Features

* `read_session` optional to `ReadRowsStream.rows()` ([#228](https://www.github.com/googleapis/python-bigquery-storage/issues/228)) ([4f56029](https://www.github.com/googleapis/python-bigquery-storage/commit/4f5602950a0c1959e332aa2964245b9caf4828c8))
* add always_use_jwt_access ([#223](https://www.github.com/googleapis/python-bigquery-storage/issues/223)) ([fd82417](https://www.github.com/googleapis/python-bigquery-storage/commit/fd824174fb044fbacc83c647f619fda556333e26))

## [2.5.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.4.0...v2.5.0) (2021-06-29)


### ⚠ BREAKING CHANGES

* remove default deadline for AppendRows API (#205)

### Features

* Add ZSTD compression as an option for Arrow ([#197](https://www.github.com/googleapis/python-bigquery-storage/issues/197)) ([f941446](https://www.github.com/googleapis/python-bigquery-storage/commit/f9414469fac37bf05db28230a1a6c1e3f7342e8d))
* new JSON type through BigQuery Write ([#178](https://www.github.com/googleapis/python-bigquery-storage/issues/178)) ([a6d6afa](https://www.github.com/googleapis/python-bigquery-storage/commit/a6d6afa8654907701aab2724f940be8f63edd0ea))


### Bug Fixes

* **deps:** add packaging requirement ([#200](https://www.github.com/googleapis/python-bigquery-storage/issues/200)) ([f2203fe](https://www.github.com/googleapis/python-bigquery-storage/commit/f2203fefe36dd043a258adb85e970fef14cf6ebc))
* remove default deadline for AppendRows API ([#205](https://www.github.com/googleapis/python-bigquery-storage/issues/205)) ([cd4e637](https://www.github.com/googleapis/python-bigquery-storage/commit/cd4e637c4c74f21be50c3b0ebdfeebb1dfb88cbb))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-bigquery-storage/issues/1127)) ([#212](https://www.github.com/googleapis/python-bigquery-storage/issues/212)) ([8bcc4cd](https://www.github.com/googleapis/python-bigquery-storage/commit/8bcc4cd298eb0f5da03ecf66670982ab41e35c88))


### Miscellaneous Chores

* release 2.5.0 ([#220](https://www.github.com/googleapis/python-bigquery-storage/issues/220)) ([946c8a9](https://www.github.com/googleapis/python-bigquery-storage/commit/946c8a91c2d74c6bf37b333a4d0483f4483dcbce))

## [2.4.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.3.0...v2.4.0) (2021-04-07)


### Features

* add a Arrow compression options (Only LZ4 for now) ([#166](https://www.github.com/googleapis/python-bigquery-storage/issues/166)) ([1c91a27](https://www.github.com/googleapis/python-bigquery-storage/commit/1c91a276289a0e319f93b136836f81ee943f661c))
* updates for v1beta2 storage API - Updated comments on BatchCommitWriteStreams - Added new support Bigquery types BIGNUMERIC and INTERVAL to TableSchema - Added read rows schema in ReadRowsResponse - Misc comment updates ([#172](https://www.github.com/googleapis/python-bigquery-storage/issues/172)) ([bef63fb](https://www.github.com/googleapis/python-bigquery-storage/commit/bef63fbb3b7e41e1c0d73f91a2c86d4d24e42151))


### Dependencies

* update minimum pandas to 0.21.1 ([#165](https://www.github.com/googleapis/python-bigquery-storage/issues/165)) ([8a97763](https://www.github.com/googleapis/python-bigquery-storage/commit/8a977633a81d080f03f6922752adbf4284199dd4))

## [2.3.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.2.1...v2.3.0) (2021-02-18)


### Features

* add `client_cert_source_for_mtls` argument to transports ([#135](https://www.github.com/googleapis/python-bigquery-storage/issues/135)) ([072850d](https://www.github.com/googleapis/python-bigquery-storage/commit/072850dd341909fdc22f330117a17e48da12fdd1))


### Documentation

* update python contributing guide ([#140](https://www.github.com/googleapis/python-bigquery-storage/issues/140)) ([1671056](https://www.github.com/googleapis/python-bigquery-storage/commit/1671056bfe181660440b1bf4415005e3eed01eb2))

## [2.2.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.2.0...v2.2.1) (2021-01-25)


### Documentation

* remove required session variable to fix publish ([#124](https://www.github.com/googleapis/python-bigquery-storage/issues/124)) ([19a105c](https://www.github.com/googleapis/python-bigquery-storage/commit/19a105cb9c868bb1a9e63966609a2488876f511b))

## [2.2.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.1.0...v2.2.0) (2021-01-22)


### Features

* add clients for v1beta2 endpoint ([#113](https://www.github.com/googleapis/python-bigquery-storage/issues/113)) ([e5f6198](https://www.github.com/googleapis/python-bigquery-storage/commit/e5f6198262cf9a593c62219cf5f6632c5a2a811e))
* add manual wrapper for v1beta2 read client ([#117](https://www.github.com/googleapis/python-bigquery-storage/issues/117)) ([798cd34](https://www.github.com/googleapis/python-bigquery-storage/commit/798cd341fbe0734f99b9c2ac3c50ae09886d1c90))


### Bug Fixes

* skip some system tests for mtls testing ([#106](https://www.github.com/googleapis/python-bigquery-storage/issues/106)) ([89ba292](https://www.github.com/googleapis/python-bigquery-storage/commit/89ba292281970cbdee5bb43b45a9dac69e29ff0a))


### Documentation

* add note about Arrow blocks to README ([#73](https://www.github.com/googleapis/python-bigquery-storage/issues/73)) ([d9691f1](https://www.github.com/googleapis/python-bigquery-storage/commit/d9691f1714bf34b3119d4e457293a723c2fb9120))
* request only a single stream in dataframe example ([#114](https://www.github.com/googleapis/python-bigquery-storage/issues/114)) ([3518624](https://www.github.com/googleapis/python-bigquery-storage/commit/35186247018b0c93a4af1fcde52fa739efa803c4))

## [2.1.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.0.1...v2.1.0) (2020-11-04)


### Features

* add public transport property and path formatting methods to client ([#80](https://www.github.com/googleapis/python-bigquery-storage/issues/80)) ([fbbb439](https://www.github.com/googleapis/python-bigquery-storage/commit/fbbb439b8c77fa9367a4b5bea725dd0b0f26b769))


### Documentation

* add intersphinx to proto-plus library ([#86](https://www.github.com/googleapis/python-bigquery-storage/issues/86)) ([4cd35d2](https://www.github.com/googleapis/python-bigquery-storage/commit/4cd35d21de4486f659b7efc4ff4dcb9b4eee6c9e))
* show inheritance in types reference ([#91](https://www.github.com/googleapis/python-bigquery-storage/issues/91)) ([e5fd4e6](https://www.github.com/googleapis/python-bigquery-storage/commit/e5fd4e62de2768a49d633dc3a81e03d64df9fe1f))

## [2.0.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.0.0...v2.0.1) (2020-10-21)


### Bug Fixes

* don't fail with 429 when downloading wide tables ([#79](https://www.github.com/googleapis/python-bigquery-storage/issues/79)) ([45faf97](https://www.github.com/googleapis/python-bigquery-storage/commit/45faf9712b25bd63d962ca7e5afc8b8d3a0d8353))


### Documentation

* update to_dataframe sample to latest dependencies ([#72](https://www.github.com/googleapis/python-bigquery-storage/issues/72)) ([a7fe762](https://www.github.com/googleapis/python-bigquery-storage/commit/a7fe7626312a5b9fe1e7bd0e0fe5601ae97605c7))

## 2.0.0

09-24-2020 08:21 PDT

### Implementation Changes

- Transition the library to microgenerator. ([#62](https://github.com/googleapis/python-bigquery-storage/pull/62))
  This is a **breaking change** that introduces several **method signature changes** and **drops support
  for Python 2.7 and 3.5**. See [migration guide](https://googleapis.dev/python/bigquerystorage/latest/UPGRADING.html)
  for more info.

## 1.1.0

09-14-2020 08:51 PDT


### Implementation Changes

- Change default retry policies timeouts (via synth). ([#53](https://github.com/googleapis/python-bigquery-storage/pull/53))


### New Features

- Add resource path helper methods. ([#40](https://github.com/googleapis/python-bigquery-storage/pull/40))


### Documentation

- Move code samples from the common [samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/) to this library. ([#50](https://github.com/googleapis/python-bigquery-storage/pull/50))
- Fix `read_rows()` docstring sample. ([#44](https://github.com/googleapis/python-bigquery-storage/pull/44))


### Internal / Testing Changes

- Update CODEOWNERS for samples and library code. ([#56](https://github.com/googleapis/python-bigquery-storage/pull/56))
- Update language of py2 admonition, add 3.8 unit tests. ([#45](https://github.com/googleapis/python-bigquery-storage/pull/45))
- Install google-cloud-testutils (via synth). ([#26](https://github.com/googleapis/python-bigquery-storage/pull/26))

## [1.0.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v0.8.0...v1.0.0) (2020-06-04)


### Bug Fixes

* handle consuming streams with no data ([#29](https://www.github.com/googleapis/python-bigquery-storage/issues/29)) ([56d1b1f](https://www.github.com/googleapis/python-bigquery-storage/commit/56d1b1fd75965669f5a4d10e5b00671c276eda88))
* update pyarrow references that are warning ([#31](https://www.github.com/googleapis/python-bigquery-storage/issues/31)) ([5302481](https://www.github.com/googleapis/python-bigquery-storage/commit/5302481d9f0ee07630ae62ed7268e510bcaa5d84))

## [0.8.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v0.7.0...v0.8.0) (2020-03-03)


### Features

* add manual layer for v1 endpoint ([#16](https://www.github.com/googleapis/python-bigquery-storage/issues/16)) ([a0fc0af](https://www.github.com/googleapis/python-bigquery-storage/commit/a0fc0af5b4447ce8b50c365d4d081b9443b8490e))
* update synth to generate v1beta2, v1 endpoints for bigquerystorage ([#10](https://www.github.com/googleapis/python-bigquery-storage/issues/10)) ([2ea5ac4](https://www.github.com/googleapis/python-bigquery-storage/commit/2ea5ac46035f38bdacf2976541a0af2dc0880660))


### Bug Fixes

* **bigquerystorage:** resume reader connection on `EOS` internal error ([#9994](https://www.github.com/googleapis/python-bigquery-storage/issues/9994)) ([acbd57f](https://www.github.com/googleapis/python-bigquery-storage/commit/acbd57f01cc8b338d9264aeedba117f7f1e48369))
* **bigquerystorage:** to_dataframe on an arrow stream uses 2x faster to_arrow + to_pandas, internally ([#9997](https://www.github.com/googleapis/python-bigquery-storage/issues/9997)) ([fdfb21e](https://www.github.com/googleapis/python-bigquery-storage/commit/fdfb21ec82278dbc5e6e9f7f16e4a22eb812b1be))
* pass snapshot_millis to the main function ([#8](https://www.github.com/googleapis/python-bigquery-storage/issues/8)) ([e522bf8](https://www.github.com/googleapis/python-bigquery-storage/commit/e522bf8327420d852352180ebfc0f816f269f22e))

## 0.7.0

07-31-2019 17:48 PDT


### New Features
- Support faster Arrow data format in `to_dataframe` and `to_arrow` when using BigQuery Storage API. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pins of 'googleapis-common-protos. ([#8688](https://github.com/googleapis/google-cloud-python/pull/8688))

### Documentation
- Update quickstart sample with data format and sharding options. ([#8665](https://github.com/googleapis/google-cloud-python/pull/8665))
- Fix links to bigquery storage documentation. ([#8859](https://github.com/googleapis/google-cloud-python/pull/8859))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version. (via synth). ([#8672](https://github.com/googleapis/google-cloud-python/pull/8672))

## 0.6.0

07-11-2019 13:15 PDT

### New Features

- Add `to_arrow` with support for Arrow data format. ([#8644](https://github.com/googleapis/google-cloud-python/pull/8644))
- Add 'client_options' support (via synth). ([#8536](https://github.com/googleapis/google-cloud-python/pull/8536))
- Add sharding strategy, stream splitting, Arrow support (via synth). ([#8477](https://github.com/googleapis/google-cloud-python/pull/8477))

### Documentation

- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

### Internal / Testing Changes

- Allow kwargs to be passed to create_channel (via synth). ([#8441](https://github.com/googleapis/google-cloud-python/pull/8441))
- Add encoding declaration to protoc-generated files (via synth). ([#8345](https://github.com/googleapis/google-cloud-python/pull/8345))
- Refactor `reader.ReadRowsPage` to use `_StreamParser`. ([#8262](https://github.com/googleapis/google-cloud-python/pull/8262))
- Fix coverage in 'types.py' (via synth). ([#8148](https://github.com/googleapis/google-cloud-python/pull/8148))
- Add empty lines, remove coverage exclusions (via synth). ([#8051](https://github.com/googleapis/google-cloud-python/pull/8051))

## 0.5.0

05-20-2019 09:23 PDT

### Implementation Changes

- Increase default deadline on ReadRows. ([#8030](https://github.com/googleapis/google-cloud-python/pull/8030))
- Respect timeout on `client.read_rows`. Don't resume on `DEADLINE_EXCEEDED` errors. ([#8025](https://github.com/googleapis/google-cloud-python/pull/8025))

### Documentation

- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

## 0.4.0

04-16-2019 13:46 PDT

### Implementation Changes

- Remove gRPC size limit in the transport options ([#7664](https://github.com/googleapis/google-cloud-python/pull/7664))
- Add retry params for create_read_session (via synth). ([#7658](https://github.com/googleapis/google-cloud-python/pull/7658))

### New Features

- Add page iterator to ReadRowsStream ([#7680](https://github.com/googleapis/google-cloud-python/pull/7680))

### Internal / Testing Changes

- Remove system test for split rows ([#7673](https://github.com/googleapis/google-cloud-python/pull/7673))

## 0.3.0

04-02-2019 15:22 PDT

### Dependencies

- Add dependency for resource proto. ([#7585](https://github.com/googleapis/google-cloud-python/pull/7585))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### Documentation

- Fix links to BigQuery Storage API docs ([#7647](https://github.com/googleapis/google-cloud-python/pull/7647))
- Update proto / docstrings (via synth). ([#7461](https://github.com/googleapis/google-cloud-python/pull/7461))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Blacken new quickstart snippet. ([#7242](https://github.com/googleapis/google-cloud-python/pull/7242))
- Add quickstart demonstrating most BQ Storage API read features ([#7223](https://github.com/googleapis/google-cloud-python/pull/7223))
- Add bigquery_storage to docs ([#7222](https://github.com/googleapis/google-cloud-python/pull/7222))

### Internal / Testing Changes

- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Copy lintified proto files (via synth). ([#7475](https://github.com/googleapis/google-cloud-python/pull/7475))
- Add annotations to protocol buffers indicating request parameters (via synth). ([#7550](https://github.com/googleapis/google-cloud-python/pull/7550))

## 0.2.0

01-25-2019 13:54 PST

### New Features

- Add option to choose dtypes by column in to_dataframe. ([#7126](https://github.com/googleapis/google-cloud-python/pull/7126))

### Internal / Testing Changes

- Update copyright headers
- Protoc-generated serialization update. ([#7076](https://github.com/googleapis/google-cloud-python/pull/7076))
- BigQuery Storage: run 'blacken' during synth ([#7047](https://github.com/googleapis/google-cloud-python/pull/7047))

## 0.1.1

12-17-2018 18:03 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes in GAPIC generator. ([#6708](https://github.com/googleapis/google-cloud-python/pull/6708))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Correct release_status for bigquery_storage ([#6767](https://github.com/googleapis/google-cloud-python/pull/6767))

## 0.1.0

11-29-2018 13:45 PST

- Initial release of BigQuery Storage API client.
