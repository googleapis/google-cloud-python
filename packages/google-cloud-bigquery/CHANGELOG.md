# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery/#history


## [3.7.0](https://github.com/googleapis/python-bigquery/compare/v3.6.0...v3.7.0) (2023-03-06)


### Features

* Add `connection_properties` and `create_session` to `LoadJobConfig` ([#1509](https://github.com/googleapis/python-bigquery/issues/1509)) ([cd0aaa1](https://github.com/googleapis/python-bigquery/commit/cd0aaa15960e9ca7a0aaf411c8e4990f95421816))
* Add default_query_job_config property and property setter to BQ client ([#1511](https://github.com/googleapis/python-bigquery/issues/1511)) ([a23092c](https://github.com/googleapis/python-bigquery/commit/a23092cad834c6a016f455d46fefa13bb6cdbf0f))


### Documentation

* Remove &lt; 3.11 reference from README ([#1502](https://github.com/googleapis/python-bigquery/issues/1502)) ([c7417f4](https://github.com/googleapis/python-bigquery/commit/c7417f43563e20a3e6f1a57f46925fb274b28b07))

## [3.6.0](https://github.com/googleapis/python-bigquery/compare/v3.5.0...v3.6.0) (2023-02-22)


### Features

* Adding preserveAsciiControlCharacter to CSVOptions ([#1491](https://github.com/googleapis/python-bigquery/issues/1491)) ([f832e7a](https://github.com/googleapis/python-bigquery/commit/f832e7a0b79f3567a0773ff11630e2f48bed60db))


### Bug Fixes

* Annotate optional integer parameters with optional type ([#1487](https://github.com/googleapis/python-bigquery/issues/1487)) ([a190aaa](https://github.com/googleapis/python-bigquery/commit/a190aaa09ae73e8b6a83b7b213247f95fde57615))
* Loosen ipywidget dependency ([#1504](https://github.com/googleapis/python-bigquery/issues/1504)) ([20d3276](https://github.com/googleapis/python-bigquery/commit/20d3276cc29e9467eef9476d5fd572099d9a3f6f))
* Removes scope to avoid unnecessary duplication ([#1503](https://github.com/googleapis/python-bigquery/issues/1503)) ([665d7ba](https://github.com/googleapis/python-bigquery/commit/665d7ba74a1b45de1ef51cc75b6860125afc5fe6))


### Dependencies

* Update minimum google-cloud-core  to 1.6.0 ([a190aaa](https://github.com/googleapis/python-bigquery/commit/a190aaa09ae73e8b6a83b7b213247f95fde57615))

## [3.5.0](https://github.com/googleapis/python-bigquery/compare/v3.4.2...v3.5.0) (2023-01-31)


### Features

* Add __str__ method to DatasetReference ([#1477](https://github.com/googleapis/python-bigquery/issues/1477)) ([f32df1f](https://github.com/googleapis/python-bigquery/commit/f32df1fb74e4aea24cd8a4099040ad2f7436e54d))
* Add preserveAsciiControlCharacter to LoadJobConfig ([#1484](https://github.com/googleapis/python-bigquery/issues/1484)) ([bd1da9a](https://github.com/googleapis/python-bigquery/commit/bd1da9aa0a40b02b7d5409a0b094d8380e255c91))


### Documentation

* Adds snippet for creating table with external data config ([#1420](https://github.com/googleapis/python-bigquery/issues/1420)) ([f0ace2a](https://github.com/googleapis/python-bigquery/commit/f0ace2ac2307ef359511a235f80f5ce9e46264c1))
* Revise delete label table code sample, add TODO to clean up sni… ([#1466](https://github.com/googleapis/python-bigquery/issues/1466)) ([0dab7d2](https://github.com/googleapis/python-bigquery/commit/0dab7d25ace4b63d2984485e7b0c5bb38f20476f))
* **samples:** Table variable fix ([#1287](https://github.com/googleapis/python-bigquery/issues/1287)) ([a71888a](https://github.com/googleapis/python-bigquery/commit/a71888a60d1e5e5815ab459fe24368ad5b0d032a))

## [3.4.2](https://github.com/googleapis/python-bigquery/compare/v3.4.1...v3.4.2) (2023-01-13)


### Bug Fixes

* Add support for python 3.11 ([#1463](https://github.com/googleapis/python-bigquery/issues/1463)) ([730a1de](https://github.com/googleapis/python-bigquery/commit/730a1dec8be49df26a3d805ebd4ad185ba72170d))
* Require grpcio &gt;= 1.49.1 for python 3.11 ([72b25c5](https://github.com/googleapis/python-bigquery/commit/72b25c52bc4b9a92c4cb187b6230b280d4af905c))


### Dependencies

* Remove upper bound on packaging dependency ([#1440](https://github.com/googleapis/python-bigquery/issues/1440)) ([6088129](https://github.com/googleapis/python-bigquery/commit/60881296a35067e7aa025d92b2425572f10fd4ec))


### Documentation

* Create sample to write schema file from table ([#1439](https://github.com/googleapis/python-bigquery/issues/1439)) ([093cc68](https://github.com/googleapis/python-bigquery/commit/093cc6852ada29898c4a4d047fd216544ef15bba))
* Created samples for load table and create table from schema file ([#1436](https://github.com/googleapis/python-bigquery/issues/1436)) ([8ad2e5b](https://github.com/googleapis/python-bigquery/commit/8ad2e5bc1c04bf16fffe4c8773e722b68117c916))
* Revise create table cmek sample ([#1452](https://github.com/googleapis/python-bigquery/issues/1452)) ([57740e4](https://github.com/googleapis/python-bigquery/commit/57740e49af7418449aec73a6fdd307fcb588c655))
* Revise get table labels code sample, add TODO to clean up snipp… ([#1464](https://github.com/googleapis/python-bigquery/issues/1464)) ([b5ccbfe](https://github.com/googleapis/python-bigquery/commit/b5ccbfe4eee91d7f481d9708084cd29d0c85e666))
* Revise label table code samples ([#1451](https://github.com/googleapis/python-bigquery/issues/1451)) ([14ae1f2](https://github.com/googleapis/python-bigquery/commit/14ae1f20538ea00829a1325f91f5e8524234bd0c))
* Revise sample for nested schema ([#1446](https://github.com/googleapis/python-bigquery/issues/1446)) ([a097631](https://github.com/googleapis/python-bigquery/commit/a0976318fc5ad1620a68250c3e059e2a51d4946d))

## [3.4.1](https://github.com/googleapis/python-bigquery/compare/v3.4.0...v3.4.1) (2022-12-09)


### Documentation

* Add info about streaming quota limits to `insert_rows*` methods ([#1409](https://github.com/googleapis/python-bigquery/issues/1409)) ([0f08e9a](https://github.com/googleapis/python-bigquery/commit/0f08e9a8ff638e78006d71acd974de2dff89b5d9))


### Dependencies

* make pyarrow and BQ Storage optional dependencies ([e1aa921](https://github.com/googleapis/python-bigquery/commit/e1aa9218ad22f85c9a6cab8b61d013779376a582))

## [3.4.0](https://github.com/googleapis/python-bigquery/compare/v3.3.6...v3.4.0) (2022-11-17)


### Features

* Add `reference_file_schema_uri` to LoadJobConfig, ExternalConfig ([#1399](https://github.com/googleapis/python-bigquery/issues/1399)) ([931285f](https://github.com/googleapis/python-bigquery/commit/931285ff85842ab07a0ef2ff9db808181ea3c5e4))
* Add default value expression ([#1408](https://github.com/googleapis/python-bigquery/issues/1408)) ([207aa50](https://github.com/googleapis/python-bigquery/commit/207aa506ab634bdb13256fa5bd8745ec9de23290))
* Add More Specific Type Annotations for Row Dictionaries ([#1295](https://github.com/googleapis/python-bigquery/issues/1295)) ([eb49873](https://github.com/googleapis/python-bigquery/commit/eb49873176dee478617eb50472d44703abca53b5))

## [3.3.6](https://github.com/googleapis/python-bigquery/compare/v3.3.4...v3.3.6) (2022-11-02)


### Features

* Reconfigure tqdm progress bar in %%bigquery magic ([#1355](https://github.com/googleapis/python-bigquery/issues/1355)) ([506f781](https://github.com/googleapis/python-bigquery/commit/506f781c2dd775193336ab9432f32148250ed81d))


### Bug Fixes

* Corrects test for non-existent attribute ([#1395](https://github.com/googleapis/python-bigquery/issues/1395)) ([a80f436](https://github.com/googleapis/python-bigquery/commit/a80f436f2e75a8fb680316f17a22eecb31a7101d))
* **deps:** Allow protobuf 3.19.5 ([#1379](https://github.com/googleapis/python-bigquery/issues/1379)) ([3e4a074](https://github.com/googleapis/python-bigquery/commit/3e4a074a981eb2920c5f9a711c253565d4844858))
* **deps:** Allow pyarrow &lt; 11 ([#1393](https://github.com/googleapis/python-bigquery/issues/1393)) ([c898546](https://github.com/googleapis/python-bigquery/commit/c898546d3292f9ec1ba6120cd3f9e2805aa087bb))
* **deps:** Require requests&gt;=2.21.0 ([#1388](https://github.com/googleapis/python-bigquery/issues/1388)) ([e398336](https://github.com/googleapis/python-bigquery/commit/e39833673582e4a7a34103cfc45603932c9c33b3))
* Refactor to adapt to changes to shapely dependency ([#1376](https://github.com/googleapis/python-bigquery/issues/1376)) ([2afd278](https://github.com/googleapis/python-bigquery/commit/2afd278febe1eb247adc6278ab59903962a5bb6c))


### Documentation

* Fix typos ([#1372](https://github.com/googleapis/python-bigquery/issues/1372)) ([21cc525](https://github.com/googleapis/python-bigquery/commit/21cc525a86a06acfe73e5c5a74ec5f0b61e410f2))


### Miscellaneous Chores

* release 3.3.6 ([4fce1d9](https://github.com/googleapis/python-bigquery/commit/4fce1d93b1763703b115a0480a2b97021786aff7))

## [3.3.4](https://github.com/googleapis/python-bigquery/compare/v3.3.3...v3.3.4) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#1369](https://github.com/googleapis/python-bigquery/issues/1369)) ([f13383a](https://github.com/googleapis/python-bigquery/commit/f13383a22d7b1a0a714dc1b1210ad970146bd094))

## [3.3.3](https://github.com/googleapis/python-bigquery/compare/v3.3.2...v3.3.3) (2022-09-28)


### Bug Fixes

* Refactors code to account for a tdqm code deprecation ([#1357](https://github.com/googleapis/python-bigquery/issues/1357)) ([1369a9d](https://github.com/googleapis/python-bigquery/commit/1369a9d937b85d6a2a6bf9a672c71620648b1e3e))
* Validate opentelemetry span job attributes have values ([#1327](https://github.com/googleapis/python-bigquery/issues/1327)) ([8287af1](https://github.com/googleapis/python-bigquery/commit/8287af1299169546f847126f03ae04e48890139e))


### Documentation

* **samples:** uses function (create_job) more appropriate to the described sample intent ([5aeedaa](https://github.com/googleapis/python-bigquery/commit/5aeedaa2f4e6a0200d50521dfd90f39f9a24d0cc))

## [3.3.2](https://github.com/googleapis/python-bigquery/compare/v3.3.1...v3.3.2) (2022-08-16)


### Bug Fixes

* **deps:** require proto-plus >= 1.22.0 ([1de7a52](https://github.com/googleapis/python-bigquery/commit/1de7a52cb85d4876e4aa87346aff5725c8294c4e))
* **deps:** require protobuf >=3.19, < 5.0.0 ([#1311](https://github.com/googleapis/python-bigquery/issues/1311)) ([1de7a52](https://github.com/googleapis/python-bigquery/commit/1de7a52cb85d4876e4aa87346aff5725c8294c4e))

## [3.3.1](https://github.com/googleapis/python-bigquery/compare/v3.3.0...v3.3.1) (2022-08-09)


### Bug Fixes

* **deps:** allow pyarrow < 10 ([#1304](https://github.com/googleapis/python-bigquery/issues/1304)) ([13616a9](https://github.com/googleapis/python-bigquery/commit/13616a910ba2e9b7bc3595847229b56e70c99f84))

## [3.3.0](https://github.com/googleapis/python-bigquery/compare/v3.2.0...v3.3.0) (2022-07-25)


### Features

* add destination_expiration_time property to copy job ([#1277](https://github.com/googleapis/python-bigquery/issues/1277)) ([728b07c](https://github.com/googleapis/python-bigquery/commit/728b07c9177532bbbbfd1890f23e98950aea3f02))


### Bug Fixes

* require python 3.7+ ([#1284](https://github.com/googleapis/python-bigquery/issues/1284)) ([52d9f14](https://github.com/googleapis/python-bigquery/commit/52d9f14fb1d183f64a62fee1fddc0bf576a0a3e9))


### Documentation

* **samples:** add table snapshot sample ([#1274](https://github.com/googleapis/python-bigquery/issues/1274)) ([e760d1b](https://github.com/googleapis/python-bigquery/commit/e760d1bcb76561b4247adde2fd06ae0b686befb9))
* **samples:** explicitly add bq to samples reqs, upgrade grpc to fix bug on m1 ([#1290](https://github.com/googleapis/python-bigquery/issues/1290)) ([9b7e3e4](https://github.com/googleapis/python-bigquery/commit/9b7e3e424cbd08af8b08c91e6397a3f1b7811064))

## [3.2.0](https://github.com/googleapis/python-bigquery/compare/v3.1.0...v3.2.0) (2022-06-06)


### Features

* add support for table clones ([#1235](https://github.com/googleapis/python-bigquery/issues/1235)) ([176fb2a](https://github.com/googleapis/python-bigquery/commit/176fb2afc9888c6b0cd74d590065b3002bdbf533))


### Bug Fixes

* **deps:** proto-plus >= 1.15.0, <2.0.0dev ([ba58d3a](https://github.com/googleapis/python-bigquery/commit/ba58d3af80ca796be09c813529d3aadb79e0413c))
* **deps:** require packaging >= 14.3, <22.0.0dev ([ba58d3a](https://github.com/googleapis/python-bigquery/commit/ba58d3af80ca796be09c813529d3aadb79e0413c))
* **deps:** require protobuf>= 3.12.0, <4.0.0dev ([#1263](https://github.com/googleapis/python-bigquery/issues/1263)) ([ba58d3a](https://github.com/googleapis/python-bigquery/commit/ba58d3af80ca796be09c813529d3aadb79e0413c))


### Documentation

* fix changelog header to consistent size ([#1268](https://github.com/googleapis/python-bigquery/issues/1268)) ([d03e2a2](https://github.com/googleapis/python-bigquery/commit/d03e2a29ecfa5d2ccd5599f5c0faac55286e52e7))

## [3.1.0](https://github.com/googleapis/python-bigquery/compare/v3.0.1...v3.1.0) (2022-05-09)


### Features

* add str method to table ([#1199](https://github.com/googleapis/python-bigquery/issues/1199)) ([8da4fa9](https://github.com/googleapis/python-bigquery/commit/8da4fa9e77bcfd2b68818b5d65b38ccc59899a01))
* refactor AccessEntry to use _properties pattern ([#1125](https://github.com/googleapis/python-bigquery/issues/1125)) ([acd5612](https://github.com/googleapis/python-bigquery/commit/acd5612d2fc469633936dbc463ce4d70951e7fdd))
* support using BIGQUERY_EMULATOR_HOST environment variable ([#1222](https://github.com/googleapis/python-bigquery/issues/1222)) ([39294b4](https://github.com/googleapis/python-bigquery/commit/39294b4950896b084573bedb4c5adc2b8d371eac))


### Bug Fixes

* **deps:** allow pyarrow v8 ([#1245](https://github.com/googleapis/python-bigquery/issues/1245)) ([d258690](https://github.com/googleapis/python-bigquery/commit/d258690dbf01108e1426f0e28d792c418a88bce0))
* export bigquery.HivePartitioningOptions ([#1217](https://github.com/googleapis/python-bigquery/issues/1217)) ([8eb757b](https://github.com/googleapis/python-bigquery/commit/8eb757bcded7a3ef3b2264f47ec080c0a8fca579))
* Skip geography_as_object conversion for REPEATED fields ([#1220](https://github.com/googleapis/python-bigquery/issues/1220)) ([4d3d6ec](https://github.com/googleapis/python-bigquery/commit/4d3d6ec9e667a781f8cb4a3aee0376c6179d5ce1))


### Documentation

* updated variable typo in comment in code sample ([#1239](https://github.com/googleapis/python-bigquery/issues/1239)) ([e420112](https://github.com/googleapis/python-bigquery/commit/e4201128bdb7f49cb732e12609448bbdbc122736))

## [3.0.1](https://github.com/googleapis/python-bigquery/compare/v3.0.0...v3.0.1) (2022-03-30)


### Bug Fixes

* **deps:** raise exception when pandas is installed but db-dtypes is not ([#1191](https://github.com/googleapis/python-bigquery/issues/1191)) ([4333910](https://github.com/googleapis/python-bigquery/commit/433391097bae57dd12a93db18fc2bab573d8f128))
* **deps:** restore dependency on python-dateutil ([#1187](https://github.com/googleapis/python-bigquery/issues/1187)) ([212d7ec](https://github.com/googleapis/python-bigquery/commit/212d7ec1f0740d04c26fb3ceffc9a4dd9eed6756))

## [3.0.0](https://github.com/googleapis/python-bigquery/compare/v2.34.3...v3.0.0) (2022-03-29)


### ⚠ BREAKING CHANGES

* BigQuery Storage and pyarrow are required dependencies (#776)
* use nullable `Int64` and `boolean` dtypes in `to_dataframe` (#786)
* destination tables are no-longer removed by `create_job` (#891)
* In `to_dataframe`, use `dbdate` and `dbtime` dtypes from db-dtypes package for BigQuery DATE and TIME columns (#972)
* automatically convert out-of-bounds dates in `to_dataframe`, remove `date_as_object` argument (#972)
* mark the package as type-checked (#1058)
* default to DATETIME type when loading timezone-naive datetimes from Pandas (#1061)
* remove out-of-date BigQuery ML protocol buffers (#1178)

### Features

* add `api_method` parameter to `Client.query` to select `INSERT` or `QUERY` API ([#967](https://github.com/googleapis/python-bigquery/issues/967)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* default to DATETIME type when loading timezone-naive datetimes from Pandas ([#1061](https://github.com/googleapis/python-bigquery/issues/1061)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* destination tables are no-longer removed by `create_job` ([#891](https://github.com/googleapis/python-bigquery/issues/891)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* In `to_dataframe`, use `dbdate` and `dbtime` dtypes from db-dtypes package for BigQuery DATE and TIME columns ([#972](https://github.com/googleapis/python-bigquery/issues/972)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* mark the package as type-checked ([#1058](https://github.com/googleapis/python-bigquery/issues/1058)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* use `StandardSqlField` class for `Model.feature_columns` and `Model.label_columns` ([#1117](https://github.com/googleapis/python-bigquery/issues/1117)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))


### Bug Fixes

* automatically convert out-of-bounds dates in `to_dataframe`, remove `date_as_object` argument ([#972](https://github.com/googleapis/python-bigquery/issues/972)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* improve type annotations for mypy validation ([#1081](https://github.com/googleapis/python-bigquery/issues/1081)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* remove out-of-date BigQuery ML protocol buffers ([#1178](https://github.com/googleapis/python-bigquery/issues/1178)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))
* use nullable `Int64` and `boolean` dtypes in `to_dataframe` ([#786](https://github.com/googleapis/python-bigquery/issues/786)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))


### Documentation

* Add migration guide from version 2.x to 3.x ([#1027](https://github.com/googleapis/python-bigquery/issues/1027)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))


### Dependencies

* BigQuery Storage and pyarrow are required dependencies ([#776](https://github.com/googleapis/python-bigquery/issues/776)) ([76d88fb](https://github.com/googleapis/python-bigquery/commit/76d88fbb1316317a61fa1a63c101bc6f42f23af8))

## [2.34.3](https://github.com/googleapis/python-bigquery/compare/v2.34.2...v2.34.3) (2022-03-29)


### Bug Fixes

* update content-type header ([#1171](https://github.com/googleapis/python-bigquery/issues/1171)) ([921b440](https://github.com/googleapis/python-bigquery/commit/921b440fdd151e88ee5b3e0d9fb90177877dc11a))

## [2.34.2](https://github.com/googleapis/python-bigquery/compare/v2.34.1...v2.34.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#1157](https://github.com/googleapis/python-bigquery/issues/1157)) ([0c15790](https://github.com/googleapis/python-bigquery/commit/0c15790720ff573a501cfe760dd74ee166e1a353))
* **deps:** require proto-plus>=1.15.0 ([0c15790](https://github.com/googleapis/python-bigquery/commit/0c15790720ff573a501cfe760dd74ee166e1a353))

## [2.34.1](https://github.com/googleapis/python-bigquery/compare/v2.34.0...v2.34.1) (2022-03-02)


### Dependencies

* add "extra" for IPython, exclude bad IPython release ([#1151](https://github.com/googleapis/python-bigquery/issues/1151)) ([0fbe12d](https://github.com/googleapis/python-bigquery/commit/0fbe12d1ababa45aa774b026a93c0af9e8f343d9))
* allow pyarrow 7.0 ([#1112](https://github.com/googleapis/python-bigquery/issues/1112)) ([57f8ea9](https://github.com/googleapis/python-bigquery/commit/57f8ea95e152dc238e7a4941f96c54be53f7eaf3))

## [2.34.0](https://github.com/googleapis/python-bigquery/compare/v2.33.0...v2.34.0) (2022-02-18)


### Features

* support BI Engine statistics in query job ([#1144](https://github.com/googleapis/python-bigquery/issues/1144)) ([7482549](https://github.com/googleapis/python-bigquery/commit/7482549cb42ed5302634ab4fb7b4efcd97b35c68))

## [2.33.0](https://github.com/googleapis/python-bigquery/compare/v2.32.0...v2.33.0) (2022-02-16)


### Features

* add `--no_query_cache` option to `%%bigquery` magics to disable query cache ([#1141](https://github.com/googleapis/python-bigquery/issues/1141)) ([7dd30af](https://github.com/googleapis/python-bigquery/commit/7dd30af41b8a595b96176c964ba14aa41645ef0d))


### Bug Fixes

* return 403 when VPC-SC violation happens ([#1131](https://github.com/googleapis/python-bigquery/issues/1131)) ([f5daa9b](https://github.com/googleapis/python-bigquery/commit/f5daa9b41377a58cb3220bb2ab7c72adc6462196))


### Documentation

* reference BigQuery REST API defaults in `LoadJobConfig` descrip… ([#1132](https://github.com/googleapis/python-bigquery/issues/1132)) ([18d9580](https://github.com/googleapis/python-bigquery/commit/18d958062721d6be81e7bd7a5bd66f277344a864))
* show common job properties in `get_job` and `cancel_job` samples ([#1137](https://github.com/googleapis/python-bigquery/issues/1137)) ([8edc10d](https://github.com/googleapis/python-bigquery/commit/8edc10d019bd96defebc4f92a47774901e9b956f))

## [2.32.0](https://github.com/googleapis/python-bigquery/compare/v2.31.0...v2.32.0) (2022-01-12)


### Features

* support authorized dataset entity ([#1075](https://github.com/googleapis/python-bigquery/issues/1075)) ([c098cd0](https://github.com/googleapis/python-bigquery/commit/c098cd01c755633bfaba7193dd5c044a489a5b61))


### Bug Fixes

* remove query text from exception message, use `exception.debug_message` instead ([#1105](https://github.com/googleapis/python-bigquery/issues/1105)) ([e23114c](https://github.com/googleapis/python-bigquery/commit/e23114ce362e09ac72f733a640e53a561cc9ce69))

## [2.31.0](https://www.github.com/googleapis/python-bigquery/compare/v2.30.1...v2.31.0) (2021-11-24)


### Features

* allow cell magic body to be a $variable ([#1053](https://www.github.com/googleapis/python-bigquery/issues/1053)) ([3a681e0](https://www.github.com/googleapis/python-bigquery/commit/3a681e046819df18118aa0b2b5733416d004c9b3))
* promote `RowIterator.to_arrow_iterable` to public method ([#1073](https://www.github.com/googleapis/python-bigquery/issues/1073)) ([21cd710](https://www.github.com/googleapis/python-bigquery/commit/21cd71022d60c32104f8f90ee2ca445fbb43f7f3))


### Bug Fixes

* apply timeout to all resumable upload requests ([#1070](https://www.github.com/googleapis/python-bigquery/issues/1070)) ([3314dfb](https://www.github.com/googleapis/python-bigquery/commit/3314dfbed62488503dc41b11e403a672fcf71048))


### Dependencies

* support OpenTelemetry >= 1.1.0 ([#1050](https://www.github.com/googleapis/python-bigquery/issues/1050)) ([4616cd5](https://www.github.com/googleapis/python-bigquery/commit/4616cd58d3c6da641fb881ce99a87dcdedc20ba2))

## [2.30.1](https://www.github.com/googleapis/python-bigquery/compare/v2.30.0...v2.30.1) (2021-11-04)


### Bug Fixes

* error if eval()-ing repr(SchemaField) ([#1046](https://www.github.com/googleapis/python-bigquery/issues/1046)) ([13ac860](https://www.github.com/googleapis/python-bigquery/commit/13ac860de689ea13b35932c67042bc35e388cb30))


### Documentation

* show gcloud command to authorize against sheets ([#1045](https://www.github.com/googleapis/python-bigquery/issues/1045)) ([20c9024](https://www.github.com/googleapis/python-bigquery/commit/20c9024b5760f7ae41301f4da54568496922cbe2))
* use stable URL for pandas intersphinx links ([#1048](https://www.github.com/googleapis/python-bigquery/issues/1048)) ([73312f8](https://www.github.com/googleapis/python-bigquery/commit/73312f8f0f22ff9175a4f5f7db9bb438a496c164))

## [2.30.0](https://www.github.com/googleapis/python-bigquery/compare/v2.29.0...v2.30.0) (2021-11-03)


### Features

* accept TableListItem where TableReference is accepted ([#1016](https://www.github.com/googleapis/python-bigquery/issues/1016)) ([fe16adc](https://www.github.com/googleapis/python-bigquery/commit/fe16adc86a170d0992c32091b349b036f8b43884))
* support Python 3.10 ([#1043](https://www.github.com/googleapis/python-bigquery/issues/1043)) ([5bbb832](https://www.github.com/googleapis/python-bigquery/commit/5bbb832a83ebb66db4b5ee740cdfc53f4df8430b))


### Documentation

* add code samples for Jupyter/IPython magics ([#1013](https://www.github.com/googleapis/python-bigquery/issues/1013)) ([61141ee](https://www.github.com/googleapis/python-bigquery/commit/61141ee0634024ad261d1595c95cd14a896fb87e))
* **samples:** add create external table with hive partitioning  ([#1033](https://www.github.com/googleapis/python-bigquery/issues/1033)) ([d64f5b6](https://www.github.com/googleapis/python-bigquery/commit/d64f5b682854a2293244426316890df4ab1e079e))

## [2.29.0](https://www.github.com/googleapis/python-bigquery/compare/v2.28.1...v2.29.0) (2021-10-27)


### Features

* add `QueryJob.schema` property for dry run queries ([#1014](https://www.github.com/googleapis/python-bigquery/issues/1014)) ([2937fa1](https://www.github.com/googleapis/python-bigquery/commit/2937fa1386898766c561579fd39d42958182d260))
* add session and connection properties to QueryJobConfig ([#1024](https://www.github.com/googleapis/python-bigquery/issues/1024)) ([e4c94f4](https://www.github.com/googleapis/python-bigquery/commit/e4c94f446c27eb474f30b033c1b62d11bd0acd98))
* add support for INTERVAL data type to `list_rows` ([#840](https://www.github.com/googleapis/python-bigquery/issues/840)) ([e37380a](https://www.github.com/googleapis/python-bigquery/commit/e37380a959cbd5bb9cbbf6807f0a8ea147e0a713))
* allow queryJob.result() to be called on a dryRun ([#1015](https://www.github.com/googleapis/python-bigquery/issues/1015)) ([685f06a](https://www.github.com/googleapis/python-bigquery/commit/685f06a5e7b5df17a53e9eb340ff04ecd1e51d1d))


### Documentation

* document ScriptStatistics and other missing resource classes ([#1023](https://www.github.com/googleapis/python-bigquery/issues/1023)) ([6679109](https://www.github.com/googleapis/python-bigquery/commit/66791093c61f262ea063d2a7950fc643915ee693))
* fix formatting of generated client docstrings ([#1009](https://www.github.com/googleapis/python-bigquery/issues/1009)) ([f7b0ee4](https://www.github.com/googleapis/python-bigquery/commit/f7b0ee45a664295ccc9f209eeeac122af8de3c80))


### Dependencies

* allow pyarrow 6.x ([#1031](https://www.github.com/googleapis/python-bigquery/issues/1031)) ([1c2de74](https://www.github.com/googleapis/python-bigquery/commit/1c2de74a55046a343bcf9474f67100a82fb05401))

## [2.28.1](https://www.github.com/googleapis/python-bigquery/compare/v2.28.0...v2.28.1) (2021-10-07)


### Bug Fixes

* support ARRAY data type when loading from DataFrame with Parquet ([#980](https://www.github.com/googleapis/python-bigquery/issues/980)) ([1e59083](https://www.github.com/googleapis/python-bigquery/commit/1e5908302d36e15442013af6f46b1c20af28255e))

## [2.28.0](https://www.github.com/googleapis/python-bigquery/compare/v2.27.1...v2.28.0) (2021-09-30)


### Features

* add `AvroOptions` to configure AVRO external data ([#994](https://www.github.com/googleapis/python-bigquery/issues/994)) ([1a9431d](https://www.github.com/googleapis/python-bigquery/commit/1a9431d9e02eeb99e4712b61c623f9cca80134a6))


### Documentation

* link to stable pandas docs ([#990](https://www.github.com/googleapis/python-bigquery/issues/990)) ([ea50e80](https://www.github.com/googleapis/python-bigquery/commit/ea50e8031fc035b3772a338bc00982de263cefad))

## [2.27.1](https://www.github.com/googleapis/python-bigquery/compare/v2.27.0...v2.27.1) (2021-09-27)


### Bug Fixes

* remove py.typed since package fails mypy check ([#988](https://www.github.com/googleapis/python-bigquery/issues/988)) ([39030f2](https://www.github.com/googleapis/python-bigquery/commit/39030f26ce081cfacd456b84694c68e3f04ed48d))

## [2.27.0](https://www.github.com/googleapis/python-bigquery/compare/v2.26.0...v2.27.0) (2021-09-24)


### Features

* Add py.typed for PEP 561 compliance ([#976](https://www.github.com/googleapis/python-bigquery/issues/976)) ([96e6bee](https://www.github.com/googleapis/python-bigquery/commit/96e6beef3c63b663b7e5879b1458f4dd1a47a5b5))
* include key metadata in Job representation ([#964](https://www.github.com/googleapis/python-bigquery/issues/964)) ([acca1cb](https://www.github.com/googleapis/python-bigquery/commit/acca1cb7baaa3b00508246c994ade40314d421c3))


### Bug Fixes

* Arrow extension-type metadata was not set when calling the REST API or when there are no rows ([#946](https://www.github.com/googleapis/python-bigquery/issues/946)) ([864383b](https://www.github.com/googleapis/python-bigquery/commit/864383bc01636b3774f7da194587b8b7edd0383d))
* disambiguate missing policy tags from explicitly unset policy tags ([#983](https://www.github.com/googleapis/python-bigquery/issues/983)) ([f83c00a](https://www.github.com/googleapis/python-bigquery/commit/f83c00acead70fc0ce9959eefb133a672d816277))
* remove default timeout ([#974](https://www.github.com/googleapis/python-bigquery/issues/974)) ([1cef0d4](https://www.github.com/googleapis/python-bigquery/commit/1cef0d4664bf448168b26487a71795144b7f4d6b))


### Documentation

* simplify destination table sample with f-strings ([#966](https://www.github.com/googleapis/python-bigquery/issues/966)) ([ab6e76f](https://www.github.com/googleapis/python-bigquery/commit/ab6e76f9489262fd9c1876a1c4f93d7e139aa999))

## [2.26.0](https://www.github.com/googleapis/python-bigquery/compare/v2.25.2...v2.26.0) (2021-09-01)


### Features

* set the X-Server-Timeout header when timeout is set ([#927](https://www.github.com/googleapis/python-bigquery/issues/927)) ([ba02f24](https://www.github.com/googleapis/python-bigquery/commit/ba02f248ba9c449c34859579a4011f4bfd2f4a93))


### Bug Fixes

* guard imports against unsupported pyarrow versions ([#934](https://www.github.com/googleapis/python-bigquery/issues/934)) ([b289076](https://www.github.com/googleapis/python-bigquery/commit/b28907693bbe889becc1b9c8963f0a7e1ee6c35a))

## [2.25.2](https://www.github.com/googleapis/python-bigquery/compare/v2.25.1...v2.25.2) (2021-08-31)


### Bug Fixes

* error inserting DataFrame with REPEATED field ([#925](https://www.github.com/googleapis/python-bigquery/issues/925)) ([656d2fa](https://www.github.com/googleapis/python-bigquery/commit/656d2fa6f870573a21235c83463752a2d084caba))
* underscores weren't allowed in struct field names when passing parameters to the DB API ([#930](https://www.github.com/googleapis/python-bigquery/issues/930)) ([fcb0bc6](https://www.github.com/googleapis/python-bigquery/commit/fcb0bc68c972c2c98bb8542f54e9228308177ecb))


### Documentation

* update docstring for bigquery_create_routine sample ([#883](https://www.github.com/googleapis/python-bigquery/issues/883)) ([#917](https://www.github.com/googleapis/python-bigquery/issues/917)) ([e2d12b7](https://www.github.com/googleapis/python-bigquery/commit/e2d12b795ef2dc51b0ee36f1b3000edb1e64ce05))

## [2.25.1](https://www.github.com/googleapis/python-bigquery/compare/v2.25.0...v2.25.1) (2021-08-25)


### Bug Fixes

* populate default `timeout` and retry after client-side timeout ([#896](https://www.github.com/googleapis/python-bigquery/issues/896)) ([b508809](https://www.github.com/googleapis/python-bigquery/commit/b508809c0f887575274309a463e763c56ddd017d))
* use REST API in cell magic when requested ([#892](https://www.github.com/googleapis/python-bigquery/issues/892)) ([1cb3e55](https://www.github.com/googleapis/python-bigquery/commit/1cb3e55253e824e3a1da5201f6ec09065fb6b627))

## [2.25.0](https://www.github.com/googleapis/python-bigquery/compare/v2.24.1...v2.25.0) (2021-08-24)


### Features

* Support using GeoPandas for GEOGRAPHY columns ([#848](https://www.github.com/googleapis/python-bigquery/issues/848)) ([16f65e6](https://www.github.com/googleapis/python-bigquery/commit/16f65e6ae15979217ceea6c6d398c9057a363a13))

## [2.24.1](https://www.github.com/googleapis/python-bigquery/compare/v2.24.0...v2.24.1) (2021-08-13)


### Bug Fixes

* remove pytz dependency and require pyarrow>=3.0.0 ([#875](https://www.github.com/googleapis/python-bigquery/issues/875)) ([2cb3563](https://www.github.com/googleapis/python-bigquery/commit/2cb3563ee863edef7eaf5d04d739bcfe7bc6438e))

## [2.24.0](https://www.github.com/googleapis/python-bigquery/compare/v2.23.3...v2.24.0) (2021-08-11)


### Features

* add support for transaction statistics ([#849](https://www.github.com/googleapis/python-bigquery/issues/849)) ([7f7b1a8](https://www.github.com/googleapis/python-bigquery/commit/7f7b1a808d50558772a0deb534ca654da65d629e))
* make the same `Table*` instances equal to each other ([#867](https://www.github.com/googleapis/python-bigquery/issues/867)) ([c1a3d44](https://www.github.com/googleapis/python-bigquery/commit/c1a3d4435739a21d25aa154145e36d3a7c42eeb6))
* retry failed query jobs in `result()` ([#837](https://www.github.com/googleapis/python-bigquery/issues/837)) ([519d99c](https://www.github.com/googleapis/python-bigquery/commit/519d99c20e7d1101f76981f3de036fdf3c7a4ecc))
* support `ScalarQueryParameterType` for `type_` argument in `ScalarQueryParameter` constructor ([#850](https://www.github.com/googleapis/python-bigquery/issues/850)) ([93d15e2](https://www.github.com/googleapis/python-bigquery/commit/93d15e2e5405c2cc6d158c4e5737361344193dbc))


### Bug Fixes

* make unicode characters working well in load_table_from_json ([#865](https://www.github.com/googleapis/python-bigquery/issues/865)) ([ad9c802](https://www.github.com/googleapis/python-bigquery/commit/ad9c8026f0e667f13dd754279f9dc40d06f4fa78))

## [2.23.3](https://www.github.com/googleapis/python-bigquery/compare/v2.23.2...v2.23.3) (2021-08-06)


### Bug Fixes

* increase default retry deadline to 10 minutes ([#859](https://www.github.com/googleapis/python-bigquery/issues/859)) ([30770fd](https://www.github.com/googleapis/python-bigquery/commit/30770fd0575fbd5aaa70c14196a4cc54627aecd2))

## [2.23.2](https://www.github.com/googleapis/python-bigquery/compare/v2.23.1...v2.23.2) (2021-07-29)


### Dependencies

* expand pyarrow pins to support 5.x releases ([#833](https://www.github.com/googleapis/python-bigquery/issues/833)) ([80e3a61](https://www.github.com/googleapis/python-bigquery/commit/80e3a61c60419fb19b70b664c6415cd01ba82f5b))

## [2.23.1](https://www.github.com/googleapis/python-bigquery/compare/v2.23.0...v2.23.1) (2021-07-28)


### Bug Fixes

* `insert_rows()` accepts float column values as strings again ([#824](https://www.github.com/googleapis/python-bigquery/issues/824)) ([d9378af](https://www.github.com/googleapis/python-bigquery/commit/d9378af13add879118a1d004529b811f72c325d6))

## [2.23.0](https://www.github.com/googleapis/python-bigquery/compare/v2.22.1...v2.23.0) (2021-07-27)


### Features

* Update proto definitions for bigquery/v2 to support new proto fields for BQML. ([#817](https://www.github.com/googleapis/python-bigquery/issues/817)) ([fe7a902](https://www.github.com/googleapis/python-bigquery/commit/fe7a902e8b3e723ace335c9b499aea6d180a025b))


### Bug Fixes

* no longer raise a warning in `to_dataframe` if `max_results` set ([#815](https://www.github.com/googleapis/python-bigquery/issues/815)) ([3c1be14](https://www.github.com/googleapis/python-bigquery/commit/3c1be149e76b1d1d8879fdcf0924ddb1c1839e94))
* retry ChunkedEncodingError by default ([#802](https://www.github.com/googleapis/python-bigquery/issues/802)) ([419d36d](https://www.github.com/googleapis/python-bigquery/commit/419d36d6b1887041e5795dbc8fc808890e91ab11))


### Documentation

* correct docs for `LoadJobConfig.destination_table_description` ([#810](https://www.github.com/googleapis/python-bigquery/issues/810)) ([da87fd9](https://www.github.com/googleapis/python-bigquery/commit/da87fd921cc8067b187d7985c978aac8eb58d107))

## [2.22.1](https://www.github.com/googleapis/python-bigquery/compare/v2.22.0...v2.22.1) (2021-07-22)


### Bug Fixes

* issue a warning if buggy pyarrow is detected ([#787](https://www.github.com/googleapis/python-bigquery/issues/787)) ([e403721](https://www.github.com/googleapis/python-bigquery/commit/e403721af1373eb1f1a1c7be5b2182e3819ed1f9))
* use a larger chunk size when loading data ([#799](https://www.github.com/googleapis/python-bigquery/issues/799)) ([b804373](https://www.github.com/googleapis/python-bigquery/commit/b804373277c1c1baa3370ebfb4783503b7ff360f))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#785](https://www.github.com/googleapis/python-bigquery/issues/785)) ([e587029](https://www.github.com/googleapis/python-bigquery/commit/e58702967d572e83b4c774278818302594a511b7))
* add sample to delete job metadata ([#798](https://www.github.com/googleapis/python-bigquery/issues/798)) ([be9b242](https://www.github.com/googleapis/python-bigquery/commit/be9b242f2180f5b795dfb3a168a97af1682999fd))

## [2.22.0](https://www.github.com/googleapis/python-bigquery/compare/v2.21.0...v2.22.0) (2021-07-19)


### Features

* add `LoadJobConfig.projection_fields` to select DATASTORE_BACKUP fields ([#736](https://www.github.com/googleapis/python-bigquery/issues/736)) ([c45a738](https://www.github.com/googleapis/python-bigquery/commit/c45a7380871af3dfbd3c45524cb606c60e1a01d1))
* add standard sql table type, update scalar type enums ([#777](https://www.github.com/googleapis/python-bigquery/issues/777)) ([b8b5433](https://www.github.com/googleapis/python-bigquery/commit/b8b5433898ec881f8da1303614780a660d94733a))
* add support for more detailed DML stats ([#758](https://www.github.com/googleapis/python-bigquery/issues/758)) ([36fe86f](https://www.github.com/googleapis/python-bigquery/commit/36fe86f41c1a8f46167284f752a6d6bbf886a04b))
* add support for user defined Table View Functions ([#724](https://www.github.com/googleapis/python-bigquery/issues/724)) ([8c7b839](https://www.github.com/googleapis/python-bigquery/commit/8c7b839a6ac1491c1c3b6b0e8755f4b70ed72ee3))


### Bug Fixes

* avoid possible job already exists error ([#751](https://www.github.com/googleapis/python-bigquery/issues/751)) ([45b9308](https://www.github.com/googleapis/python-bigquery/commit/45b93089f5398740413104285cc8acfd5ebc9c08))


### Dependencies

* allow 2.x versions of `google-api-core`, `google-cloud-core`, `google-resumable-media` ([#770](https://www.github.com/googleapis/python-bigquery/issues/770)) ([87a09fa](https://www.github.com/googleapis/python-bigquery/commit/87a09fa3f2a9ab35728a1ac925f9d5f2e6616c65))


### Documentation

* add loading data from Firestore backup sample ([#737](https://www.github.com/googleapis/python-bigquery/issues/737)) ([22fd848](https://www.github.com/googleapis/python-bigquery/commit/22fd848cae4af1148040e1faa31dd15a4d674687))

## [2.21.0](https://www.github.com/googleapis/python-bigquery/compare/v2.20.0...v2.21.0) (2021-07-12)


### Features

* Add max_results parameter to some of the `QueryJob` methods. ([#698](https://www.github.com/googleapis/python-bigquery/issues/698)) ([2a9618f](https://www.github.com/googleapis/python-bigquery/commit/2a9618f4daaa4a014161e1a2f7376844eec9e8da))
* Add support for decimal target types. ([#735](https://www.github.com/googleapis/python-bigquery/issues/735)) ([7d2d3e9](https://www.github.com/googleapis/python-bigquery/commit/7d2d3e906a9eb161911a198fb925ad79de5df934))
* Add support for table snapshots. ([#740](https://www.github.com/googleapis/python-bigquery/issues/740)) ([ba86b2a](https://www.github.com/googleapis/python-bigquery/commit/ba86b2a6300ae5a9f3c803beeb42bda4c522e34c))
* Enable unsetting policy tags on schema fields. ([#703](https://www.github.com/googleapis/python-bigquery/issues/703)) ([18bb443](https://www.github.com/googleapis/python-bigquery/commit/18bb443c7acd0a75dcb57d9aebe38b2d734ff8c7))
* Make it easier to disable best-effort deduplication with streaming inserts. ([#734](https://www.github.com/googleapis/python-bigquery/issues/734)) ([1246da8](https://www.github.com/googleapis/python-bigquery/commit/1246da86b78b03ca1aa2c45ec71649e294cfb2f1))
* Support passing struct data to the DB API. ([#718](https://www.github.com/googleapis/python-bigquery/issues/718)) ([38b3ef9](https://www.github.com/googleapis/python-bigquery/commit/38b3ef96c3dedc139b84f0ff06885141ae7ce78c))


### Bug Fixes

* Inserting non-finite floats with `insert_rows()`. ([#728](https://www.github.com/googleapis/python-bigquery/issues/728)) ([d047419](https://www.github.com/googleapis/python-bigquery/commit/d047419879e807e123296da2eee89a5253050166))
* Use `pandas` function to check for `NaN`. ([#750](https://www.github.com/googleapis/python-bigquery/issues/750)) ([67bc5fb](https://www.github.com/googleapis/python-bigquery/commit/67bc5fbd306be7cdffd216f3791d4024acfa95b3))


### Documentation

* Add docs for all enums in module. ([#745](https://www.github.com/googleapis/python-bigquery/issues/745)) ([145944f](https://www.github.com/googleapis/python-bigquery/commit/145944f24fedc4d739687399a8309f9d51d43dfd))
* Omit mention of Python 2.7 in `CONTRIBUTING.rst`. ([#706](https://www.github.com/googleapis/python-bigquery/issues/706)) ([27d6839](https://www.github.com/googleapis/python-bigquery/commit/27d6839ee8a40909e4199cfa0da8b6b64705b2e9))

## [2.20.0](https://www.github.com/googleapis/python-bigquery/compare/v2.19.0...v2.20.0) (2021-06-07)


### Features

* support script options in query job config ([#690](https://www.github.com/googleapis/python-bigquery/issues/690)) ([1259e16](https://www.github.com/googleapis/python-bigquery/commit/1259e16394784315368e8be959c1ac097782b62e))

## [2.19.0](https://www.github.com/googleapis/python-bigquery/compare/v2.18.0...v2.19.0) (2021-06-06)


### Features

* list_tables, list_projects, list_datasets, list_models, list_routines, and list_jobs now accept a page_size parameter to control page size  ([#686](https://www.github.com/googleapis/python-bigquery/issues/686)) ([1f1c4b7](https://www.github.com/googleapis/python-bigquery/commit/1f1c4b7ba4390fc4c5c8186bc22b83b45304ca06))

## [2.18.0](https://www.github.com/googleapis/python-bigquery/compare/v2.17.0...v2.18.0) (2021-06-02)


### Features

* add support for Parquet options ([#679](https://www.github.com/googleapis/python-bigquery/issues/679)) ([d792ce0](https://www.github.com/googleapis/python-bigquery/commit/d792ce09388a6ee3706777915dd2818d4c854f79))

## [2.17.0](https://www.github.com/googleapis/python-bigquery/compare/v2.16.1...v2.17.0) (2021-05-21)


### Features

* detect obsolete BQ Storage extra at runtime ([#666](https://www.github.com/googleapis/python-bigquery/issues/666)) ([bd7dbda](https://www.github.com/googleapis/python-bigquery/commit/bd7dbdae5c972b16bafc53c67911eeaa3255a880))
* Support parameterized NUMERIC, BIGNUMERIC, STRING, and BYTES types ([#673](https://www.github.com/googleapis/python-bigquery/issues/673)) ([45421e7](https://www.github.com/googleapis/python-bigquery/commit/45421e73bfcddb244822e6a5cd43be6bd1ca2256))


### Bug Fixes

* **tests:** invalid path to strptime() ([#672](https://www.github.com/googleapis/python-bigquery/issues/672)) ([591cdd8](https://www.github.com/googleapis/python-bigquery/commit/591cdd851bb1321b048a05a378a0ef48d3ade462))

## [2.16.1](https://www.github.com/googleapis/python-bigquery/compare/v2.16.0...v2.16.1) (2021-05-12)


### Bug Fixes

* executemany rowcount only reflected the last execution ([#660](https://www.github.com/googleapis/python-bigquery/issues/660)) ([aeadc8c](https://www.github.com/googleapis/python-bigquery/commit/aeadc8c2d614bb9f0883ec901fca48930f3aaf19))

## [2.16.0](https://www.github.com/googleapis/python-bigquery/compare/v2.15.0...v2.16.0) (2021-05-05)


### Features

* add with_name() to ScalarQueryParameterType ([#644](https://www.github.com/googleapis/python-bigquery/issues/644)) ([6cc6876](https://www.github.com/googleapis/python-bigquery/commit/6cc6876eb0e5bf49fdc047256a945dcf1b289576))


### Dependencies

* expand supported pyarrow versions to v4 ([#643](https://www.github.com/googleapis/python-bigquery/issues/643)) ([9e1d386](https://www.github.com/googleapis/python-bigquery/commit/9e1d3869c2024fe7a8af57ff59838d904ca5db03))

## [2.15.0](https://www.github.com/googleapis/python-bigquery/compare/v2.14.0...v2.15.0) (2021-04-29)


### Features

* Extended DB API parameter syntax to optionally provide parameter types ([#626](https://www.github.com/googleapis/python-bigquery/issues/626)) ([8bcf397](https://www.github.com/googleapis/python-bigquery/commit/8bcf397fbe2527e06317741875a059b109cfcd9c))


### Bug Fixes

* add DECIMAL and BIGDECIMAL as aliases for NUMERIC and BIGNUMERIC ([#638](https://www.github.com/googleapis/python-bigquery/issues/638)) ([aa59023](https://www.github.com/googleapis/python-bigquery/commit/aa59023317b1c63720fb717b3544f755652da58d))
* The DB API Binary function accepts bytes data ([#630](https://www.github.com/googleapis/python-bigquery/issues/630)) ([4396e70](https://www.github.com/googleapis/python-bigquery/commit/4396e70771af6889d3242c37c5ff2e80241023a2))

## [2.14.0](https://www.github.com/googleapis/python-bigquery/compare/v2.13.1...v2.14.0) (2021-04-26)


### Features

* accept DatasetListItem where DatasetReference is accepted ([#597](https://www.github.com/googleapis/python-bigquery/issues/597)) ([c8b5581](https://www.github.com/googleapis/python-bigquery/commit/c8b5581ea3c94005d69755c4a3b5a0d8900f3fe2))
* accept job object as argument to `get_job` and `cancel_job` ([#617](https://www.github.com/googleapis/python-bigquery/issues/617)) ([f75dcdf](https://www.github.com/googleapis/python-bigquery/commit/f75dcdf3943b87daba60011c9a3b42e34ff81910))
* add `Client.delete_job_metadata` method to remove job metadata ([#610](https://www.github.com/googleapis/python-bigquery/issues/610)) ([0abb566](https://www.github.com/googleapis/python-bigquery/commit/0abb56669c097c59fbffce007c702e7a55f2d9c1))
* add `max_queue_size` argument to `RowIterator.to_dataframe_iterable` ([#575](https://www.github.com/googleapis/python-bigquery/issues/575)) ([f95f415](https://www.github.com/googleapis/python-bigquery/commit/f95f415d3441b3928f6cc705cb8a75603d790fd6))
* add type hints for public methods ([#613](https://www.github.com/googleapis/python-bigquery/issues/613)) ([f8d4aaa](https://www.github.com/googleapis/python-bigquery/commit/f8d4aaa335a0eef915e73596fc9b43b11d11be9f))
* DB API cursors are now iterable ([#618](https://www.github.com/googleapis/python-bigquery/issues/618)) ([e0b373d](https://www.github.com/googleapis/python-bigquery/commit/e0b373d0e721a70656ed8faceb7f5c70f642d144))
* retry google.auth TransportError by default ([#624](https://www.github.com/googleapis/python-bigquery/issues/624)) ([34ecc3f](https://www.github.com/googleapis/python-bigquery/commit/34ecc3f1ca0ff073330c0c605673d89b43af7ed9))
* use pyarrow stream compression, if available ([#593](https://www.github.com/googleapis/python-bigquery/issues/593)) ([dde9dc5](https://www.github.com/googleapis/python-bigquery/commit/dde9dc5114c2311fb76fafc5b222fff561e8abf1))


### Bug Fixes

* consistent percents handling in DB API query ([#619](https://www.github.com/googleapis/python-bigquery/issues/619)) ([6502a60](https://www.github.com/googleapis/python-bigquery/commit/6502a602337ae562652a20b20270949f2c9d5073))
* missing license headers in new test files ([#604](https://www.github.com/googleapis/python-bigquery/issues/604)) ([df48cc5](https://www.github.com/googleapis/python-bigquery/commit/df48cc5a0be99ad39d5835652d1b7422209afc5d))
* unsetting clustering fields on Table is now possible ([#622](https://www.github.com/googleapis/python-bigquery/issues/622)) ([33a871f](https://www.github.com/googleapis/python-bigquery/commit/33a871f06329f9bf5a6a92fab9ead65bf2bee75d))


### Documentation

* add sample to run DML query ([#591](https://www.github.com/googleapis/python-bigquery/issues/591)) ([ff2ec3a](https://www.github.com/googleapis/python-bigquery/commit/ff2ec3abe418a443cd07751c08e654f94e8b3155))
* update the description of the return value of `_QueryResults.rows()` ([#594](https://www.github.com/googleapis/python-bigquery/issues/594)) ([8f4c0b8](https://www.github.com/googleapis/python-bigquery/commit/8f4c0b84dac3840532d7865247b8ad94b625b897))

## [2.13.1](https://www.github.com/googleapis/python-bigquery/compare/v2.13.0...v2.13.1) (2021-03-23)


### Bug Fixes

* add ConnectionError to default retry ([#571](https://www.github.com/googleapis/python-bigquery/issues/571)) ([a3edb8b](https://www.github.com/googleapis/python-bigquery/commit/a3edb8b921e029e2c03d33302d408ad5d4e9d4ad))

## [2.13.0](https://www.github.com/googleapis/python-bigquery/compare/v2.12.0...v2.13.0) (2021-03-22)


### Features

* add `ExternalConfig.connection_id` property to connect to external sources ([#560](https://www.github.com/googleapis/python-bigquery/issues/560)) ([d93986e](https://www.github.com/googleapis/python-bigquery/commit/d93986e0259952257f2571f60719b52099c29c0c))


### Bug Fixes

* avoid overly strict dependency on pyarrow 3.x ([#564](https://www.github.com/googleapis/python-bigquery/issues/564)) ([97ee6ec](https://www.github.com/googleapis/python-bigquery/commit/97ee6ec6cd4bc9f833cd506dc6d244d103654cfd))
* avoid policy tags 403 error in `load_table_from_dataframe` ([#557](https://www.github.com/googleapis/python-bigquery/issues/557)) ([84e646e](https://www.github.com/googleapis/python-bigquery/commit/84e646e6b7087a1626e56ad51eeb130f4ddfa2fb))

## [2.12.0](https://www.github.com/googleapis/python-bigquery/compare/v2.11.0...v2.12.0) (2021-03-16)


### Features

* make QueryJob.done() method more performant ([#544](https://www.github.com/googleapis/python-bigquery/issues/544)) ([a3ab9ef](https://www.github.com/googleapis/python-bigquery/commit/a3ab9efdd0758829845cfcb6ca0ac1f03ab44f64))


### Bug Fixes

* remove DB-API dependency on pyarrow with decimal query parameters ([#551](https://www.github.com/googleapis/python-bigquery/issues/551)) ([1b946ba](https://www.github.com/googleapis/python-bigquery/commit/1b946ba23ee7df86114c6acb338ec34e6c92af6d))

## [2.11.0](https://www.github.com/googleapis/python-bigquery/compare/v2.10.0...v2.11.0) (2021-03-09)


### Features

* add context manager support to client ([#540](https://www.github.com/googleapis/python-bigquery/issues/540)) ([d5c7e11](https://www.github.com/googleapis/python-bigquery/commit/d5c7e11a1dc2a149d74294bfadbae62d70573e69))

## [2.10.0](https://www.github.com/googleapis/python-bigquery/compare/v2.9.0...v2.10.0) (2021-02-25)


### Features

* add BIGNUMERIC support ([#527](https://www.github.com/googleapis/python-bigquery/issues/527)) ([cc3394f](https://www.github.com/googleapis/python-bigquery/commit/cc3394f80934419eb00c2029bb81c92a696e7d88))


### Bug Fixes

* error using empty array of structs parameter ([#474](https://www.github.com/googleapis/python-bigquery/issues/474)) ([c1d15f4](https://www.github.com/googleapis/python-bigquery/commit/c1d15f4e5da4b7e10c00afffd59a5c7f3ded027a))
* QueryJob.exception() *returns* the errors, not raises them ([#467](https://www.github.com/googleapis/python-bigquery/issues/467)) ([d763279](https://www.github.com/googleapis/python-bigquery/commit/d7632799769248b09a8558ba18f5025ebdd9675a))


### Documentation

* **bigquery:** Add alternative approach to setting credentials ([#517](https://www.github.com/googleapis/python-bigquery/issues/517)) ([60fbf28](https://www.github.com/googleapis/python-bigquery/commit/60fbf287b0d34d5db2e61cce7a5b42735ed43d0e))
* explain retry behavior for DONE jobs ([#532](https://www.github.com/googleapis/python-bigquery/issues/532)) ([696c443](https://www.github.com/googleapis/python-bigquery/commit/696c443f0a6740be0767e12b706a7771bc1460c3))

## [2.9.0](https://www.github.com/googleapis/python-bigquery/compare/v2.8.0...v2.9.0) (2021-02-18)


### Features

* add determinism level for javascript UDFs ([#522](https://www.github.com/googleapis/python-bigquery/issues/522)) ([edd3328](https://www.github.com/googleapis/python-bigquery/commit/edd3328fffa3040b2cd3a3c668c90a0e43e4c94c))
* expose reservation usage stats on jobs ([#524](https://www.github.com/googleapis/python-bigquery/issues/524)) ([4ffb4e0](https://www.github.com/googleapis/python-bigquery/commit/4ffb4e067abdaa54dad6eff49a7fbdb0fa358637))


### Documentation

* clarify `%%bigquery`` magics and fix broken link ([#508](https://www.github.com/googleapis/python-bigquery/issues/508)) ([eedf93b](https://www.github.com/googleapis/python-bigquery/commit/eedf93b6636c5ff1bd810c6038cfeaea8ccb64d8))
* update python contributing guide ([#514](https://www.github.com/googleapis/python-bigquery/issues/514)) ([01e851d](https://www.github.com/googleapis/python-bigquery/commit/01e851d00fc17a780375580776753d78f6d74174))

## [2.8.0](https://www.github.com/googleapis/python-bigquery/compare/v2.7.0...v2.8.0) (2021-02-08)


### Features

* Add mTLS support to client. ([#492](https://www.github.com/googleapis/python-bigquery/issues/492)) ([1823cad](https://www.github.com/googleapis/python-bigquery/commit/1823cadee3acf95c516d0479400e4175349ea199))


### Bug Fixes

* Don't try to close closed cursors. ([#498](https://www.github.com/googleapis/python-bigquery/issues/498)) ([bf44e7b](https://www.github.com/googleapis/python-bigquery/commit/bf44e7b67d2de41c13053a4550484b9ea049db3e))

## [2.7.0](https://www.github.com/googleapis/python-bigquery/compare/v2.6.2...v2.7.0) (2021-01-27)


### Bug Fixes

* invalid conversion of timezone-aware datetime values to JSON ([#480](https://www.github.com/googleapis/python-bigquery/issues/480)) ([61b4385](https://www.github.com/googleapis/python-bigquery/commit/61b438523d305ce66a68fde7cb49e9abbf0a8d1d))
* reading the labels attribute on Job instances ([#471](https://www.github.com/googleapis/python-bigquery/issues/471)) ([80944f0](https://www.github.com/googleapis/python-bigquery/commit/80944f080bcc4fda870a6daf1d884de616d39ae7))
* use explicitly given project over the client's default project for load jobs ([#482](https://www.github.com/googleapis/python-bigquery/issues/482)) ([530e1e8](https://www.github.com/googleapis/python-bigquery/commit/530e1e8d8fe8939e914a78ff1b220907c1b87af7))


### Dependencies

* declare support for Python 3.9 ([#488](https://www.github.com/googleapis/python-bigquery/issues/488)) ([55daa7d](https://www.github.com/googleapis/python-bigquery/commit/55daa7da9857a8a2fb14a80a4efa3f466386a85f))

## [2.6.2](https://www.github.com/googleapis/python-bigquery/compare/v2.6.1...v2.6.2) (2021-01-11)


### Bug Fixes

* add minimum timeout to getQueryResults API requests ([#444](https://www.github.com/googleapis/python-bigquery/issues/444)) ([015a73e](https://www.github.com/googleapis/python-bigquery/commit/015a73e1839e3427408ef6e0f879717d9ddbdb61))
* use debug logging level for OpenTelemetry message ([#442](https://www.github.com/googleapis/python-bigquery/issues/442)) ([7ea6b7c](https://www.github.com/googleapis/python-bigquery/commit/7ea6b7c2469d2415192cfdacc379e38e49d24775))


### Documentation

* add GEOGRAPHY data type code samples ([#428](https://www.github.com/googleapis/python-bigquery/issues/428)) ([dbc68b3](https://www.github.com/googleapis/python-bigquery/commit/dbc68b3d1f325f80d24a2da5f028b0f653fb0317))
* fix Shapely import in GEOGRAPHY sample ([#431](https://www.github.com/googleapis/python-bigquery/issues/431)) ([96a1c5b](https://www.github.com/googleapis/python-bigquery/commit/96a1c5b3c72855ba6ae8c88dfd0cdb02d2faf909))
* move and refresh view samples ([#420](https://www.github.com/googleapis/python-bigquery/issues/420)) ([079b6a1](https://www.github.com/googleapis/python-bigquery/commit/079b6a162f6929bf801366d92f8daeb3318426c4))

## [2.6.1](https://www.github.com/googleapis/python-bigquery/compare/v2.6.0...v2.6.1) (2020-12-09)


### Bug Fixes

* handle null values in array query parameters ([#426](https://www.github.com/googleapis/python-bigquery/issues/426)) ([78fde4a](https://www.github.com/googleapis/python-bigquery/commit/78fde4a92e61a89d0b490b93acc90fff9635d1bf))


### Documentation

* add examples of `fields` argument to update methods ([#418](https://www.github.com/googleapis/python-bigquery/issues/418)) ([8c7e02b](https://www.github.com/googleapis/python-bigquery/commit/8c7e02b0de2c92ee965414e7c430eb57d1877326))

## [2.6.0](https://www.github.com/googleapis/python-bigquery/compare/v2.5.0...v2.6.0) (2020-12-07)


### Features

* add support for materialized views ([#408](https://www.github.com/googleapis/python-bigquery/issues/408)) ([57ffc66](https://www.github.com/googleapis/python-bigquery/commit/57ffc665319331e0a00583d5d652fd14a510cf2a)), closes [#407](https://www.github.com/googleapis/python-bigquery/issues/407)
* convert `BIGNUMERIC` values to decimal objects ([#414](https://www.github.com/googleapis/python-bigquery/issues/414)) ([d472d2d](https://www.github.com/googleapis/python-bigquery/commit/d472d2d2b33e40b954652d31476dea8c90e6a2dc)), closes [#367](https://www.github.com/googleapis/python-bigquery/issues/367)
* support CSV format in `load_table_from_dataframe` pandas connector ([#399](https://www.github.com/googleapis/python-bigquery/issues/399)) ([0046742](https://www.github.com/googleapis/python-bigquery/commit/0046742abdd2b5eab3c3e935316f91e7eef44d44))


### Bug Fixes

* preserve timestamp microsecond precision with rows from REST API ([#402](https://www.github.com/googleapis/python-bigquery/issues/402)) ([04510a7](https://www.github.com/googleapis/python-bigquery/commit/04510a7dc7570466550bbdf500d7020bef2af44d))


### Documentation

* update intersphinx links ([#404](https://www.github.com/googleapis/python-bigquery/issues/404)) ([a9d8ae8](https://www.github.com/googleapis/python-bigquery/commit/a9d8ae8a920dec655b77dca9d9128e569f1d07a7))

## [2.5.0](https://www.github.com/googleapis/python-bigquery/compare/v2.4.0...v2.5.0) (2020-12-02)


### Features

* add `TableReference.__str__` to get table ID in standard SQL ([#405](https://www.github.com/googleapis/python-bigquery/issues/405)) ([53dff2a](https://www.github.com/googleapis/python-bigquery/commit/53dff2ad3889af04369a22437e6ab9b92c5755b6)), closes [#354](https://www.github.com/googleapis/python-bigquery/issues/354)
* add progress bar for magics ([#396](https://www.github.com/googleapis/python-bigquery/issues/396)) ([04d0273](https://www.github.com/googleapis/python-bigquery/commit/04d027317a99e3f353e0b7a18076da9b6ba4d8d3))
* add support for unrecognized model types ([#401](https://www.github.com/googleapis/python-bigquery/issues/401)) ([168f035](https://www.github.com/googleapis/python-bigquery/commit/168f0354c4815bd1aeadbd4e388dcc9b32f97d6b))


### Bug Fixes

* avoid floating point for timestamp in `insert_rows` ([#393](https://www.github.com/googleapis/python-bigquery/issues/393)) ([a1949ae](https://www.github.com/googleapis/python-bigquery/commit/a1949ae20ec4f9c771b0cffbcd70792dd6a30dbf))


### Performance Improvements

* don't fetch rows when waiting for query to finish ([#400](https://www.github.com/googleapis/python-bigquery/issues/400)) ([730df17](https://www.github.com/googleapis/python-bigquery/commit/730df17ae1ab0b0bb2454f3c134c8f62665bc51b)), closes [#374](https://www.github.com/googleapis/python-bigquery/issues/374) [#394](https://www.github.com/googleapis/python-bigquery/issues/394)


### Documentation

* **samples:** add more clustering code snippets ([#330](https://www.github.com/googleapis/python-bigquery/issues/330)) ([809e4a2](https://www.github.com/googleapis/python-bigquery/commit/809e4a27b94ba30c10e0c9a7e89576a9de9fda2b)), closes [#329](https://www.github.com/googleapis/python-bigquery/issues/329)


### Dependencies

* update required version of opentelementry for opentelemetry-exporter-google-cloud ([#398](https://www.github.com/googleapis/python-bigquery/issues/398)) ([673a9cb](https://www.github.com/googleapis/python-bigquery/commit/673a9cb51c577c1dd016e76f3634b1e9e21482c5))

## [2.4.0](https://www.github.com/googleapis/python-bigquery/compare/v2.3.1...v2.4.0) (2020-11-16)


### Features

* add progress bar to `QueryJob.to_dataframe` and `to_arrow` ([#352](https://www.github.com/googleapis/python-bigquery/issues/352)) ([dc78edd](https://www.github.com/googleapis/python-bigquery/commit/dc78eddde7a6a312c8fed7bace7d64036837ab1a))
* allow routine references ([#378](https://www.github.com/googleapis/python-bigquery/issues/378)) ([f9480dc](https://www.github.com/googleapis/python-bigquery/commit/f9480dc2a1bc58367083176bd74725aa8b903301))


### Bug Fixes

* **dbapi:** allow rows to be fetched from scripts ([#387](https://www.github.com/googleapis/python-bigquery/issues/387)) ([b899ad1](https://www.github.com/googleapis/python-bigquery/commit/b899ad12e17cb87c58d3ae46b4388d917c5743f2)), closes [#377](https://www.github.com/googleapis/python-bigquery/issues/377)


### Performance Improvements

* avoid extra API calls from `to_dataframe` if all rows are cached ([#384](https://www.github.com/googleapis/python-bigquery/issues/384)) ([c52b317](https://www.github.com/googleapis/python-bigquery/commit/c52b31789998fc0dfde07c3296650c85104d719d))
* cache first page of `jobs.getQueryResults` rows ([#374](https://www.github.com/googleapis/python-bigquery/issues/374)) ([86f6a51](https://www.github.com/googleapis/python-bigquery/commit/86f6a516d1c7c5dc204ab085ea2578793e6561ff))
* use `getQueryResults` from DB-API ([#375](https://www.github.com/googleapis/python-bigquery/issues/375)) ([30de15f](https://www.github.com/googleapis/python-bigquery/commit/30de15f7255de5ea221df4e8db7991d279e0ea28))


### Dependencies

* expand pyarrow dependencies to include version 2 ([#368](https://www.github.com/googleapis/python-bigquery/issues/368)) ([cd9febd](https://www.github.com/googleapis/python-bigquery/commit/cd9febd20c34983781386c3bf603e5fca7135695))

## 2.3.1

11-05-2020 09:27 PST

### Internal / Testing Changes

- update `google.cloud.bigquery.__version__`

## [2.3.0](https://www.github.com/googleapis/python-bigquery/compare/v2.2.0...v2.3.0) (2020-11-04)


### Features

* add `reload` argument to `*Job.done()` functions ([#341](https://www.github.com/googleapis/python-bigquery/issues/341)) ([e51fd45](https://www.github.com/googleapis/python-bigquery/commit/e51fd45fdb0481ac5d59cc0edbfa0750928b2596))
* pass retry from Job.result() to Job.done() ([#41](https://www.github.com/googleapis/python-bigquery/issues/41)) ([284e17a](https://www.github.com/googleapis/python-bigquery/commit/284e17a17adf6844a17db2c6fed54a649b1f997e))


### Bug Fixes

* add missing spaces in opentelemetry log message ([#360](https://www.github.com/googleapis/python-bigquery/issues/360)) ([4f326b1](https://www.github.com/googleapis/python-bigquery/commit/4f326b1ca4411cfbf5ded86955a963d3e05a409f))
* **dbapi:** avoid running % format with no query parameters ([#348](https://www.github.com/googleapis/python-bigquery/issues/348)) ([5dd1a5e](https://www.github.com/googleapis/python-bigquery/commit/5dd1a5e77f13b8e576e917069e247c5390a81900))
* create_job method accepts dictionary arguments ([#300](https://www.github.com/googleapis/python-bigquery/issues/300)) ([155bacc](https://www.github.com/googleapis/python-bigquery/commit/155bacc156f181384ca6dba699ab83d0398176d1))


### Performance Improvements

* use `jobs.getQueryResults` to download result sets ([#363](https://www.github.com/googleapis/python-bigquery/issues/363)) ([0c3476d](https://www.github.com/googleapis/python-bigquery/commit/0c3476d56380d70115f6fd765bf5c5261967052f))


### Documentation

* add documents for QueryPlanEntry and QueryPlanEntryStep ([#344](https://www.github.com/googleapis/python-bigquery/issues/344)) ([dca2e4c](https://www.github.com/googleapis/python-bigquery/commit/dca2e4ca7c2ae183ac4bb60f653d425a43a86bea))

## [2.2.0](https://www.github.com/googleapis/python-bigquery/compare/v2.1.0...v2.2.0) (2020-10-19)


### Features

* add method api_repr for table list item ([#299](https://www.github.com/googleapis/python-bigquery/issues/299)) ([07c70f0](https://www.github.com/googleapis/python-bigquery/commit/07c70f0292f9212f0c968cd5c9206e8b0409c0da))
* add support for listing arima, automl, boosted tree, DNN, and matrix factorization models ([#328](https://www.github.com/googleapis/python-bigquery/issues/328)) ([502a092](https://www.github.com/googleapis/python-bigquery/commit/502a0926018abf058cb84bd18043c25eba15a2cc))
* add timeout paramter to load_table_from_file and it dependent methods ([#327](https://www.github.com/googleapis/python-bigquery/issues/327)) ([b0dd892](https://www.github.com/googleapis/python-bigquery/commit/b0dd892176e31ac25fddd15554b5bfa054299d4d))
* add to_api_repr method to Model ([#326](https://www.github.com/googleapis/python-bigquery/issues/326)) ([fb401bd](https://www.github.com/googleapis/python-bigquery/commit/fb401bd94477323bba68cf252dd88166495daf54))
* allow client options to be set in magics context ([#322](https://www.github.com/googleapis/python-bigquery/issues/322)) ([5178b55](https://www.github.com/googleapis/python-bigquery/commit/5178b55682f5e264bfc082cde26acb1fdc953a18))


### Bug Fixes

* make TimePartitioning repr evaluable ([#110](https://www.github.com/googleapis/python-bigquery/issues/110)) ([20f473b](https://www.github.com/googleapis/python-bigquery/commit/20f473bfff5ae98377f5d9cdf18bfe5554d86ff4)), closes [#109](https://www.github.com/googleapis/python-bigquery/issues/109)
* use version.py instead of pkg_resources.get_distribution ([#307](https://www.github.com/googleapis/python-bigquery/issues/307)) ([b8f502b](https://www.github.com/googleapis/python-bigquery/commit/b8f502b14f21d1815697e4d57cf1225dfb4a7c5e))


### Performance Improvements

* add size parameter for load table from dataframe and json methods ([#280](https://www.github.com/googleapis/python-bigquery/issues/280)) ([3be78b7](https://www.github.com/googleapis/python-bigquery/commit/3be78b737add7111e24e912cd02fc6df75a07de6))


### Documentation

* update clustering field docstrings ([#286](https://www.github.com/googleapis/python-bigquery/issues/286)) ([5ea1ece](https://www.github.com/googleapis/python-bigquery/commit/5ea1ece2d911cdd1f3d9549ee01559ce8ed8269a)), closes [#285](https://www.github.com/googleapis/python-bigquery/issues/285)
* update snippets samples to support version 2.0 ([#309](https://www.github.com/googleapis/python-bigquery/issues/309)) ([61634be](https://www.github.com/googleapis/python-bigquery/commit/61634be9bf9e3df7589fc1bfdbda87288859bb13))


### Dependencies

* add protobuf dependency ([#306](https://www.github.com/googleapis/python-bigquery/issues/306)) ([cebb5e0](https://www.github.com/googleapis/python-bigquery/commit/cebb5e0e911e8c9059bc8c9e7fce4440e518bff3)), closes [#305](https://www.github.com/googleapis/python-bigquery/issues/305)
* require pyarrow for pandas support ([#314](https://www.github.com/googleapis/python-bigquery/issues/314)) ([801e4c0](https://www.github.com/googleapis/python-bigquery/commit/801e4c0574b7e421aa3a28cafec6fd6bcce940dd)), closes [#265](https://www.github.com/googleapis/python-bigquery/issues/265)

## [2.1.0](https://www.github.com/googleapis/python-bigquery/compare/v2.0.0...v2.1.0) (2020-10-08)


### Features

* add constants for MONTH and YEAR time partitioning types ([#283](https://www.github.com/googleapis/python-bigquery/issues/283)) ([9090e1c](https://www.github.com/googleapis/python-bigquery/commit/9090e1ccd8825a97835325b4829f6e7ecfd9ea88))


### Bug Fixes

* remove unnecessary dependency on libcst ([#308](https://www.github.com/googleapis/python-bigquery/issues/308)) ([c055930](https://www.github.com/googleapis/python-bigquery/commit/c05593094c1405f752b2c51b15202a6dbb5cb83f))


### Performance Improvements

* remove redundant array deepcopy ([#26](https://www.github.com/googleapis/python-bigquery/issues/26)) ([b54f867](https://www.github.com/googleapis/python-bigquery/commit/b54f86769c982ce5c8fcbf3889f82450428bb40c))


### Documentation

* **samples:** add create_table_clustered code snippet ([#291](https://www.github.com/googleapis/python-bigquery/issues/291)) ([d1eb8b3](https://www.github.com/googleapis/python-bigquery/commit/d1eb8b3dcc789916c5d3ba8464f62b1f8bef35ff))

## 2.0.0

09-30-2020 14:51 PDT


### Implementation Changes

- Transition the library to microgenerator. ([#278](https://github.com/googleapis/python-bigquery/pull/278))
  This is a **breaking change** that **drops support for Python 2.7 and 3.5** and brings a few other changes.
  See [migration guide](https://googleapis.dev/python/bigquery/latest/UPGRADING.html) for more info.



### Internal / Testing Changes

- Update protoc-generated comments (via synth). ([#270](https://github.com/googleapis/python-bigquery/pull/270))
- Add CI secrets manager (via synth). ([#271](https://github.com/googleapis/python-bigquery/pull/271))

## [1.28.0](https://www.github.com/googleapis/python-bigquery/compare/v1.27.2...v1.28.0) (2020-09-22)


### Features

* add custom cell magic parser to handle complex `--params` values ([#213](https://www.github.com/googleapis/python-bigquery/issues/213)) ([dcfbac2](https://www.github.com/googleapis/python-bigquery/commit/dcfbac267fbf66d189b0cc7e76f4712122a74b7b))
* add instrumentation to list methods ([#239](https://www.github.com/googleapis/python-bigquery/issues/239)) ([fa9f9ca](https://www.github.com/googleapis/python-bigquery/commit/fa9f9ca491c3f9954287102c567ec483aa6151d4))
* add opentelemetry tracing ([#215](https://www.github.com/googleapis/python-bigquery/issues/215)) ([a04996c](https://www.github.com/googleapis/python-bigquery/commit/a04996c537e9d8847411fcbb1b05da5f175b339e))
* expose require_partition_filter for hive_partition ([#257](https://www.github.com/googleapis/python-bigquery/issues/257)) ([aa1613c](https://www.github.com/googleapis/python-bigquery/commit/aa1613c1bf48c7efb999cb8b8c422c80baf1950b))


### Bug Fixes

* fix dependency issue in fastavro ([#241](https://www.github.com/googleapis/python-bigquery/issues/241)) ([2874abf](https://www.github.com/googleapis/python-bigquery/commit/2874abf4827f1ea529519d4b138511d31f732a50))
* update minimum dependency versions ([#263](https://www.github.com/googleapis/python-bigquery/issues/263)) ([1be66ce](https://www.github.com/googleapis/python-bigquery/commit/1be66ce94a32b1f924bdda05d068c2977631af9e))
* validate job_config.source_format in load_table_from_dataframe ([#262](https://www.github.com/googleapis/python-bigquery/issues/262)) ([6160fee](https://www.github.com/googleapis/python-bigquery/commit/6160fee4b1a79b0ea9031cc18caf6322fe4c4084))


### Documentation

* recommend insert_rows_json to avoid call to tables.get ([#258](https://www.github.com/googleapis/python-bigquery/issues/258)) ([ae647eb](https://www.github.com/googleapis/python-bigquery/commit/ae647ebd68deff6e30ca2cffb5b7422c6de4940b))

## [1.27.2](https://www.github.com/googleapis/python-bigquery/compare/v1.27.1...v1.27.2) (2020-08-18)


### Bug Fixes

* rationalize platform constraints for 'pyarrow' extra ([#235](https://www.github.com/googleapis/python-bigquery/issues/235)) ([c9a0567](https://www.github.com/googleapis/python-bigquery/commit/c9a0567f59491b769a9e2fd535430423e39d4fa8))

## [1.27.1](https://www.github.com/googleapis/python-bigquery/compare/v1.27.0...v1.27.1) (2020-08-18)


### Bug Fixes

* tweak pyarrow extra to soothe PyPI ([#230](https://www.github.com/googleapis/python-bigquery/issues/230)) ([c15efbd](https://www.github.com/googleapis/python-bigquery/commit/c15efbd1ee4488898fc862768eef701443f492f6))

## [1.27.0](https://www.github.com/googleapis/python-bigquery/compare/v1.26.1...v1.27.0) (2020-08-15)


### Features

* add support and tests for struct fields ([#146](https://www.github.com/googleapis/python-bigquery/issues/146)) ([fee2ba8](https://www.github.com/googleapis/python-bigquery/commit/fee2ba80e338d093ee61565359268da91a5c9913))
* add support for getting and setting table IAM policy ([#144](https://www.github.com/googleapis/python-bigquery/issues/144)) ([f59fc9a](https://www.github.com/googleapis/python-bigquery/commit/f59fc9a482d9f9ae63e2b2bfc80b9a3481d09bde))
* **bigquery:** add client_options to base class ([#216](https://www.github.com/googleapis/python-bigquery/issues/216)) ([478597a](https://www.github.com/googleapis/python-bigquery/commit/478597a38167fa57b60ae7f65b581f3fe75ddc7c))


### Bug Fixes

* converting to dataframe with out of bounds timestamps ([#209](https://www.github.com/googleapis/python-bigquery/issues/209)) ([8209203](https://www.github.com/googleapis/python-bigquery/commit/8209203e967f0624ad306166c0af6f6f1027c550)), closes [#168](https://www.github.com/googleapis/python-bigquery/issues/168)
* raise error if inserting rows with unknown fields ([#163](https://www.github.com/googleapis/python-bigquery/issues/163)) ([8fe7254](https://www.github.com/googleapis/python-bigquery/commit/8fe725429541eed34ddc01cffc8b1ee846c14162))

## [1.26.1](https://www.github.com/googleapis/python-bigquery/compare/v1.26.0...v1.26.1) (2020-07-25)

### Documentation

* Migrated code samples from
  https://github.com/GoogleCloudPlatform/python-docs-samples

### Bug Fixes

* RowIterator.to_arrow() error when BQ Storage client cannot be created ([#181](https://www.github.com/googleapis/python-bigquery/issues/181)) ([7afa3d7](https://www.github.com/googleapis/python-bigquery/commit/7afa3d70f8564dcdacda2b9acbbd7207b50b186e))

### Dependencies

* Updated version constraints on grmp dependency in anticipation of 1.0.0 release
  ([#189](https://github.com/googleapis/python-bigquery/pull/189))

## [1.26.0](https://www.github.com/googleapis/python-bigquery/compare/v1.25.0...v1.26.0) (2020-07-20)


### Features

* use BigQuery Storage client by default (if dependencies available) ([#55](https://www.github.com/googleapis/python-bigquery/issues/55)) ([e75ff82](https://www.github.com/googleapis/python-bigquery/commit/e75ff8297c65981545b097f75a17cf9e78ac6772)), closes [#91](https://www.github.com/googleapis/python-bigquery/issues/91)
* **bigquery:** add __eq__ method for class PartitionRange and RangePartitioning ([#162](https://www.github.com/googleapis/python-bigquery/issues/162)) ([0d2a88d](https://www.github.com/googleapis/python-bigquery/commit/0d2a88d8072154cfc9152afd6d26a60ddcdfbc73))
* **bigquery:** expose date_as_object parameter to users ([#150](https://www.github.com/googleapis/python-bigquery/issues/150)) ([a2d5ce9](https://www.github.com/googleapis/python-bigquery/commit/a2d5ce9e97992318d7dc85c51c053cab74e25a11))
* **bigquery:** expose date_as_object parameter to users ([#150](https://www.github.com/googleapis/python-bigquery/issues/150)) ([cbd831e](https://www.github.com/googleapis/python-bigquery/commit/cbd831e08024a67148723afd49e1db085e0a862c))


### Bug Fixes

* dry run queries with DB API cursor ([#128](https://www.github.com/googleapis/python-bigquery/issues/128)) ([bc33a67](https://www.github.com/googleapis/python-bigquery/commit/bc33a678a765f0232615aa2038b8cc67c88468a0))
* omit `NaN` values when uploading from `insert_rows_from_dataframe` ([#170](https://www.github.com/googleapis/python-bigquery/issues/170)) ([f9f2f45](https://www.github.com/googleapis/python-bigquery/commit/f9f2f45bc009c03cd257441bd4b6beb1754e2177))


### Documentation

* **bigquery:** add client thread-safety documentation ([#132](https://www.github.com/googleapis/python-bigquery/issues/132)) ([fce76b3](https://www.github.com/googleapis/python-bigquery/commit/fce76b3776472b1da798df862a3405e659e35bab))
* **bigquery:** add docstring for conflict exception ([#171](https://www.github.com/googleapis/python-bigquery/issues/171)) ([9c3409b](https://www.github.com/googleapis/python-bigquery/commit/9c3409bb06218bf499620544f8e92802df0cce47))
* **bigquery:** consistent use of optional keyword ([#153](https://www.github.com/googleapis/python-bigquery/issues/153)) ([79d8c61](https://www.github.com/googleapis/python-bigquery/commit/79d8c61064cca18b596a24b6f738c7611721dd5c))
* **bigquery:** fix the broken docs ([#139](https://www.github.com/googleapis/python-bigquery/issues/139)) ([3235255](https://www.github.com/googleapis/python-bigquery/commit/3235255cc5f483949f34d2e8ef13b372e8713782))

## [1.25.0](https://www.github.com/googleapis/python-bigquery/compare/v1.24.0...v1.25.0) (2020-06-06)


### Features

* add BigQuery storage client support to DB API ([#36](https://www.github.com/googleapis/python-bigquery/issues/36)) ([ba9b2f8](https://www.github.com/googleapis/python-bigquery/commit/ba9b2f87e36320d80f6f6460b77e6daddb0fa214))
* **bigquery:** add create job method ([#32](https://www.github.com/googleapis/python-bigquery/issues/32)) ([2abdef8](https://www.github.com/googleapis/python-bigquery/commit/2abdef82bed31601d1ca1aa92a10fea1e09f5297))
* **bigquery:** add support of model for extract job ([#71](https://www.github.com/googleapis/python-bigquery/issues/71)) ([4a7a514](https://www.github.com/googleapis/python-bigquery/commit/4a7a514659a9f6f9bbd8af46bab3f8782d6b4b98))
* add HOUR support for time partitioning interval ([#91](https://www.github.com/googleapis/python-bigquery/issues/91)) ([0dd90b9](https://www.github.com/googleapis/python-bigquery/commit/0dd90b90e3714c1d18f8a404917a9454870e338a))
* add support for policy tags ([#77](https://www.github.com/googleapis/python-bigquery/issues/77)) ([38a5c01](https://www.github.com/googleapis/python-bigquery/commit/38a5c01ca830daf165592357c45f2fb4016aad23))
* make AccessEntry objects hashable ([#93](https://www.github.com/googleapis/python-bigquery/issues/93)) ([23a173b](https://www.github.com/googleapis/python-bigquery/commit/23a173bc5a25c0c8200adc5af62eb05624c9099e))
* **bigquery:** expose start index parameter for query result ([#121](https://www.github.com/googleapis/python-bigquery/issues/121)) ([be86de3](https://www.github.com/googleapis/python-bigquery/commit/be86de330a3c3801653a0ccef90e3d9bdb3eee7a))
* **bigquery:** unit and system test for dataframe with int column with Nan values  ([#39](https://www.github.com/googleapis/python-bigquery/issues/39)) ([5fd840e](https://www.github.com/googleapis/python-bigquery/commit/5fd840e9d4c592c4f736f2fd4792c9670ba6795e))


### Bug Fixes

* allow partial streaming_buffer statistics ([#37](https://www.github.com/googleapis/python-bigquery/issues/37)) ([645f0fd](https://www.github.com/googleapis/python-bigquery/commit/645f0fdb35ee0e81ee70f7459e796a42a1f03210))
* distinguish server timeouts from transport timeouts ([#43](https://www.github.com/googleapis/python-bigquery/issues/43)) ([a17be5f](https://www.github.com/googleapis/python-bigquery/commit/a17be5f01043f32d9fbfb2ddf456031ea9205c8f))
* improve cell magic error message on missing query ([#58](https://www.github.com/googleapis/python-bigquery/issues/58)) ([6182cf4](https://www.github.com/googleapis/python-bigquery/commit/6182cf48aef8f463bb96891cfc44a96768121dbc))
* **bigquery:** fix repr of model reference ([#66](https://www.github.com/googleapis/python-bigquery/issues/66)) ([26c6204](https://www.github.com/googleapis/python-bigquery/commit/26c62046f4ec8880cf6561cc90a8b821dcc84ec5))
* **bigquery:** fix start index with page size for list rows ([#27](https://www.github.com/googleapis/python-bigquery/issues/27)) ([400673b](https://www.github.com/googleapis/python-bigquery/commit/400673b5d0f2a6a3d828fdaad9d222ca967ffeff))

## 1.24.0

02-03-2020 01:38 PST

### Implementation Changes

- Fix inserting missing repeated fields. ([#10196](https://github.com/googleapis/google-cloud-python/pull/10196))
- Deprecate `client.dataset()` in favor of `DatasetReference`. ([#7753](https://github.com/googleapis/google-cloud-python/pull/7753))
- Use faster `to_arrow` + `to_pandas` in `to_dataframe()` when `pyarrow` is available. ([#10027](https://github.com/googleapis/google-cloud-python/pull/10027))
- Write pandas `datetime[ns]` columns to BigQuery TIMESTAMP columns. ([#10028](https://github.com/googleapis/google-cloud-python/pull/10028))

### New Features

- Check `rows` argument type in `insert_rows()`. ([#10174](https://github.com/googleapis/google-cloud-python/pull/10174))
- Check `json_rows` arg type in `insert_rows_json()`. ([#10162](https://github.com/googleapis/google-cloud-python/pull/10162))
- Make `RowIterator.to_dataframe_iterable()` method public. ([#10017](https://github.com/googleapis/google-cloud-python/pull/10017))
- Add retry parameter to public methods where missing. ([#10026](https://github.com/googleapis/google-cloud-python/pull/10026))
- Add timeout parameter to Client and Job public methods. ([#10002](https://github.com/googleapis/google-cloud-python/pull/10002))
- Add timeout parameter to `QueryJob.done()` method. ([#9875](https://github.com/googleapis/google-cloud-python/pull/9875))
- Add `create_bqstorage_client` parameter to `to_dataframe()` and `to_arrow()` methods. ([#9573](https://github.com/googleapis/google-cloud-python/pull/9573))

### Dependencies

- Fix minimum versions of `google-cloud-core` and `google-resumable-media` dependencies. ([#10016](https://github.com/googleapis/google-cloud-python/pull/10016))

### Documentation

- Fix a comment typo in `job.py`. ([#10209](https://github.com/googleapis/google-cloud-python/pull/10209))
- Update code samples of load table file and load table URI. ([#10175](https://github.com/googleapis/google-cloud-python/pull/10175))
- Uncomment `Client` constructor and imports in samples. ([#10058](https://github.com/googleapis/google-cloud-python/pull/10058))
- Remove unused query code sample. ([#10024](https://github.com/googleapis/google-cloud-python/pull/10024))
- Update code samples to use strings for table and dataset IDs. ([#9974](https://github.com/googleapis/google-cloud-python/pull/9974))

### Internal / Testing Changes

- Bump copyright year to 2020, tweak docstring formatting (via synth). [#10225](https://github.com/googleapis/google-cloud-python/pull/10225)
- Add tests for concatenating categorical columns. ([#10180](https://github.com/googleapis/google-cloud-python/pull/10180))
- Adjust test assertions to the new default timeout. ([#10222](https://github.com/googleapis/google-cloud-python/pull/10222))
- Use Python 3.6 for the nox blacken session (via synth). ([#10012](https://github.com/googleapis/google-cloud-python/pull/10012))

## 1.23.1

12-16-2019 09:39 PST


### Implementation Changes

- Add `iamMember` entity type to allowed access classes. ([#9973](https://github.com/googleapis/google-cloud-python/pull/9973))
- Fix typo in import error message (pandas -> pyarrow). ([#9955](https://github.com/googleapis/google-cloud-python/pull/9955))

### Dependencies

- Add `six` as an explicit dependency. ([#9979](https://github.com/googleapis/google-cloud-python/pull/9979))

### Documentation

- Add sample to read from query destination table. ([#9964](https://github.com/googleapis/google-cloud-python/pull/9964))

## 1.23.0

12-11-2019 13:31 PST

### New Features

- Add `close()` method to client for releasing open sockets. ([#9894](https://github.com/googleapis/google-cloud-python/pull/9894))
- Add support of `use_avro_logical_types` for extract jobs. ([#9642](https://github.com/googleapis/google-cloud-python/pull/9642))
- Add support for hive partitioning options configuration. ([#9626](https://github.com/googleapis/google-cloud-python/pull/9626))
- Add description for routine entities. ([#9785](https://github.com/googleapis/google-cloud-python/pull/9785))

### Documentation

- Update code samples to use strings for table and dataset IDs. ([#9495](https://github.com/googleapis/google-cloud-python/pull/9495))

### Internal / Testing Changes

- Run unit tests with Python 3.8. ([#9880](https://github.com/googleapis/google-cloud-python/pull/9880))
- Import `Mapping` from `collections.abc` not from `collections`. ([#9826](https://github.com/googleapis/google-cloud-python/pull/9826))

## 1.22.0

11-13-2019 12:23 PST


### Implementation Changes
- Preserve job config passed to Client methods. ([#9735](https://github.com/googleapis/google-cloud-python/pull/9735))
- Use pyarrow fallback for improved schema detection. ([#9321](https://github.com/googleapis/google-cloud-python/pull/9321))
- Add TypeError if wrong `job_config type` is passed to client job methods. ([#9506](https://github.com/googleapis/google-cloud-python/pull/9506))
- Fix arrow deprecation warning. ([#9504](https://github.com/googleapis/google-cloud-python/pull/9504))

### New Features
- Add `--destination_table` parameter to IPython magic. ([#9599](https://github.com/googleapis/google-cloud-python/pull/9599))
- Allow passing schema as a sequence of dicts. ([#9550](https://github.com/googleapis/google-cloud-python/pull/9550))
- Implement defaultEncryptionConfiguration on datasets. ([#9489](https://github.com/googleapis/google-cloud-python/pull/9489))
- Add range partitioning to tables, load jobs, and query jobs. ([#9477](https://github.com/googleapis/google-cloud-python/pull/9477))

### Dependencies
- Pin `google-resumable-media` to includ 0.5.x. ([#9572](https://github.com/googleapis/google-cloud-python/pull/9572))

### Documentation
- Fix link anchors in external config docstrings. ([#9627](https://github.com/googleapis/google-cloud-python/pull/9627))
- Add python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Add table create sample using integer range partitioning. ([#9478](https://github.com/googleapis/google-cloud-python/pull/9478))
- Document how to achieve higher write limit and add tests. ([#9574](https://github.com/googleapis/google-cloud-python/pull/9574))
- Add code sample for scripting. ([#9537](https://github.com/googleapis/google-cloud-python/pull/9537))
- Rewrite docs in Google style, part 2. ([#9481](https://github.com/googleapis/google-cloud-python/pull/9481))
- Use multi-regional key path for CMEK in snippets. ([#9523](https://github.com/googleapis/google-cloud-python/pull/9523))

### Internal / Testing Changes
- Fix undelete table system test to use milliseconds in snapshot decorator. ([#9649](https://github.com/googleapis/google-cloud-python/pull/9649))
- Format code with latest version of black. ([#9556](https://github.com/googleapis/google-cloud-python/pull/9556))
- Remove duplicate test dependencies. ([#9503](https://github.com/googleapis/google-cloud-python/pull/9503))

## 1.21.0

10-16-2019 10:33 PDT


### New Features

- add ability to pass in a table ID instead of a query to the `%%bigquery` magic ([#9170](https://github.com/googleapis/google-cloud-python/pull/9170))
- add support for custom `QueryJobConfig` in `BigQuery.cursor.execute` method ([#9278](https://github.com/googleapis/google-cloud-python/pull/9278))
- store `QueryJob` to destination var on error in `%%bigquery` magic ([#9245](https://github.com/googleapis/google-cloud-python/pull/9245))
- add script statistics to job resource ([#9428](https://github.com/googleapis/google-cloud-python/pull/9428))
- add support for sheets ranges ([#9416](https://github.com/googleapis/google-cloud-python/pull/9416))
- add support for listing jobs by parent job ([#9225](https://github.com/googleapis/google-cloud-python/pull/9225))
- expose customer managed encryption key for ML models ([#9302](https://github.com/googleapis/google-cloud-python/pull/9302))
- add `Dataset.default_partition_expiration_ms` and `Table.require_partition_filter` properties ([#9464](https://github.com/googleapis/google-cloud-python/pull/9464))

### Dependencies

- restrict version range of `google-resumable-media` ([#9243](https://github.com/googleapis/google-cloud-python/pull/9243))

### Documentation

- document how to load data as JSON string ([#9231](https://github.com/googleapis/google-cloud-python/pull/9231))
- standardize comments and formatting in existing code samples ([#9212](https://github.com/googleapis/google-cloud-python/pull/9212))
- rewrite docstrings in Google style ([#9326](https://github.com/googleapis/google-cloud-python/pull/9326))
- fix incorrect links to REST API in reference docs ([#9436](https://github.com/googleapis/google-cloud-python/pull/9436))

### Internal / Testing Changes

- add code samples to lint check ([#9277](https://github.com/googleapis/google-cloud-python/pull/9277))
- update code samples to use strings for table and dataset IDs ([#9136](https://github.com/googleapis/google-cloud-python/pull/9136))
- simplify scripting system test to reduce flakiness ([#9458](https://github.com/googleapis/google-cloud-python/pull/9458))

## 1.20.0

09-13-2019 11:22 PDT


### Implementation Changes
- Change default endpoint to bigquery.googleapis.com ([#9213](https://github.com/googleapis/google-cloud-python/pull/9213))
- Change the default value of Cursor instances' `arraysize` attribute to None ([#9199](https://github.com/googleapis/google-cloud-python/pull/9199))
- Deprecate automatic schema conversion. ([#9176](https://github.com/googleapis/google-cloud-python/pull/9176))
- Fix `list_rows()` max results with BQ storage client ([#9178](https://github.com/googleapis/google-cloud-python/pull/9178))

### New Features
- Add `Model.encryption_config`. (via synth) ([#9214](https://github.com/googleapis/google-cloud-python/pull/9214))
- Add `Client.insert_rows_from_dataframe()` method ([#9162](https://github.com/googleapis/google-cloud-python/pull/9162))
- Add support for array parameters to `Cursor.execute()`. ([#9189](https://github.com/googleapis/google-cloud-python/pull/9189))
- Add support for project IDs with org prefix to `Table.from_string()` factory. ([#9161](https://github.com/googleapis/google-cloud-python/pull/9161))
- Add `--max_results` option to Jupyter magics ([#9169](https://github.com/googleapis/google-cloud-python/pull/9169))
- Autofetch table schema on load if not provided. ([#9108](https://github.com/googleapis/google-cloud-python/pull/9108))
- Add `max_results` parameter to `QueryJob.result()`. ([#9167](https://github.com/googleapis/google-cloud-python/pull/9167))

### Documentation
- Fix doc link. ([#9200](https://github.com/googleapis/google-cloud-python/pull/9200))

### Internal / Testing Changes
- Revert "Disable failing snippets test ([#9156](https://github.com/googleapis/google-cloud-python/pull/9156))." ([#9220](https://github.com/googleapis/google-cloud-python/pull/9220))

## 1.19.0

09-03-2019 14:33 PDT

### Implementation Changes

- Raise when unexpected fields are present in the `LoadJobConfig.schema` when calling `load_table_from_dataframe`. ([#9096](https://github.com/googleapis/google-cloud-python/pull/9096))
- Determine the schema in `load_table_from_dataframe` based on dtypes. ([#9049](https://github.com/googleapis/google-cloud-python/pull/9049))
- Raise helpful error when loading table from dataframe with `STRUCT` columns. ([#9053](https://github.com/googleapis/google-cloud-python/pull/9053))
- Fix schema recognition of struct field types. ([#9001](https://github.com/googleapis/google-cloud-python/pull/9001))
- Fix deserializing `None` in `QueryJob` for queries with parameters. ([#9029](https://github.com/googleapis/google-cloud-python/pull/9029))

### New Features

- Include indexes in table written by `load_table_from_dataframe`, only if
  fields corresponding to indexes are present in `LoadJobConfig.schema`.
  ([#9084](https://github.com/googleapis/google-cloud-python/pull/9084))
- Add `client_options` to constructor. ([#8999](https://github.com/googleapis/google-cloud-python/pull/8999))
- Add `--dry_run` option to `%%bigquery` magic. ([#9067](https://github.com/googleapis/google-cloud-python/pull/9067))
- Add `load_table_from_json()` method to create a table from a list of dictionaries. ([#9076](https://github.com/googleapis/google-cloud-python/pull/9076))
- Allow subset of schema to be passed into `load_table_from_dataframe`. ([#9064](https://github.com/googleapis/google-cloud-python/pull/9064))
- Add support for unsetting `LoadJobConfig.schema`. ([#9077](https://github.com/googleapis/google-cloud-python/pull/9077))
- Add support to `Dataset` for project IDs containing an org prefix. ([#8877](https://github.com/googleapis/google-cloud-python/pull/8877))
- Add enum with SQL type names allowed to be used in `SchemaField`. ([#9040](https://github.com/googleapis/google-cloud-python/pull/9040))

### Documentation

- Fix the reference URL for `Client.create_dataset()`. ([#9149](https://github.com/googleapis/google-cloud-python/pull/9149))
- Update code samples to use strings for table names instead of `client.dataset()`. ([#9032](https://github.com/googleapis/google-cloud-python/pull/9032))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Fix Pandas DataFrame load example under Python 2.7. ([#9022](https://github.com/googleapis/google-cloud-python/pull/9022))

### Internal / Testing Changes

- Disable failing snippets test for copying CMEK-protected tables. ([#9156](https://github.com/googleapis/google-cloud-python/pull/9156))
- Fix BigQuery client unit test assertions ([#9112](https://github.com/googleapis/google-cloud-python/pull/9112))
- Replace avro with arrow schemas in `test_table.py` ([#9056](https://github.com/googleapis/google-cloud-python/pull/9056))

## 1.18.0

08-08-2019 12:28 PDT

### New Features

- Add `bqstorage_client` param to `QueryJob.to_arrow()` ([#8693](https://github.com/googleapis/google-cloud-python/pull/8693))
- Include SQL query and job ID in exception messages. ([#8748](https://github.com/googleapis/google-cloud-python/pull/8748))
- Allow using TableListItem to construct a Table object. ([#8738](https://github.com/googleapis/google-cloud-python/pull/8738))
- Add StandardSqlDataTypes enum to BigQuery ([#8782](https://github.com/googleapis/google-cloud-python/pull/8782))
- Add `to_standard_sql()` method to SchemaField ([#8880](https://github.com/googleapis/google-cloud-python/pull/8880))
- Add debug logging statements to track when BQ Storage API is used. ([#8838](https://github.com/googleapis/google-cloud-python/pull/8838))
- Hide error traceback in BigQuery cell magic ([#8808](https://github.com/googleapis/google-cloud-python/pull/8808))
- Allow choice of compression when loading from dataframe ([#8938](https://github.com/googleapis/google-cloud-python/pull/8938))
- Additional clustering metrics for BQML K-means models (via synth). ([#8945](https://github.com/googleapis/google-cloud-python/pull/8945))

### Documentation

- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Remove redundant service account key code sample. ([#8891](https://github.com/googleapis/google-cloud-python/pull/8891))

### Internal / Testing Changes

- Fix several pytest "skip if" markers ([#8694](https://github.com/googleapis/google-cloud-python/pull/8694))
- Update tests to support conversion of NaN as NULL in pyarrow `0.14.*`. ([#8785](https://github.com/googleapis/google-cloud-python/pull/8785))
- Mock external calls in one of BigQuery unit tests ([#8727](https://github.com/googleapis/google-cloud-python/pull/8727))
- Set IPython user agent when running queries with IPython cell magic ([#8713](https://github.com/googleapis/google-cloud-python/pull/8713))
- Use configurable bucket name for GCS samples data in systems tests. ([#8783](https://github.com/googleapis/google-cloud-python/pull/8783))
- Move `maybe_fail_import()` to top level test utils ([#8840](https://github.com/googleapis/google-cloud-python/pull/8840))
- Set BQ Storage client user-agent when in Jupyter cell ([#8734](https://github.com/googleapis/google-cloud-python/pull/8734))

## 1.17.0

07-12-2019 07:56 PDT

### New Features

- Support faster Arrow data format in `to_dataframe` when using BigQuery Storage API. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))
- Add `to_arrow` to get a `pyarrow.Table` from query results. ([#8609](https://github.com/googleapis/google-cloud-python/pull/8609))

### Dependencies

- Exclude bad 0.14.0 `pyarrow` release. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))

## 1.16.0

07-01-2019 10:22 PDT

### New Features

- Add Routines API. ([#8491](https://github.com/googleapis/google-cloud-python/pull/8491))
- Add more stats to Models API, such as `optimization_strategy` (via synth). ([#8344](https://github.com/googleapis/google-cloud-python/pull/8344))

### Documentation

- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Add sample demonstrating how to create a job. ([#8422](https://github.com/googleapis/google-cloud-python/pull/8422))
- Use autodetected location in code samples. ([#8340](https://github.com/googleapis/google-cloud-python/pull/8340), [#8341](https://github.com/googleapis/google-cloud-python/pull/8341))

### Internal / Testing Changes

- Refactor `to_dataframe` to deterministicly update progress bar. ([#8303](https://github.com/googleapis/google-cloud-python/pull/8303))

## 1.15.0

06-14-2019 10:10 PDT

### Implementation Changes

- Fix bug where `load_table_from_dataframe` could not append to REQUIRED fields. ([#8230](https://github.com/googleapis/google-cloud-python/pull/8230))

### New Features

- Add `page_size` parameter to `QueryJob.result`. ([#8206](https://github.com/googleapis/google-cloud-python/pull/8206))

## 1.14.0

06-04-2019 11:11 PDT


### New Features
- Add `maximum_bytes_billed` argument and `context.default_query_job_config` property to magics. ([#8179](https://github.com/googleapis/google-cloud-python/pull/8179))

### Dependencies
- Don't pin `google-api-core` in libs using `google-cloud-core`. ([#8213](https://github.com/googleapis/google-cloud-python/pull/8213))

## 1.13.0

05-31-2019 10:22 PDT

### New Features

- Use `job_config.schema` for data type conversion if specified in `load_table_from_dataframe`. ([#8105](https://github.com/googleapis/google-cloud-python/pull/8105))

### Internal / Testing Changes

- Adds private `_connection` object to magics context. ([#8192](https://github.com/googleapis/google-cloud-python/pull/8192))
- Fix coverage in 'types.py' (via synth). ([#8146](https://github.com/googleapis/google-cloud-python/pull/8146))

## 1.12.1

05-21-2019 11:16 PDT

### Implementation Changes

- Don't raise error when encountering unknown fields in Models API. ([#8083](https://github.com/googleapis/google-cloud-python/pull/8083))

### Documentation

- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

### Internal / Testing Changes

- Add empty lines (via synth). ([#8049](https://github.com/googleapis/google-cloud-python/pull/8049))

## 1.12.0

05-16-2019 11:25 PDT

### Implementation Changes
- Remove duplicates from index on pandas DataFrames returned by `to_dataframe()`. ([#7953](https://github.com/googleapis/google-cloud-python/pull/7953))
- Prevent error when time partitioning is populated with empty dict ([#7904](https://github.com/googleapis/google-cloud-python/pull/7904))
- Preserve order in `to_dataframe` with BQ Storage from queries containing `ORDER BY` ([#7793](https://github.com/googleapis/google-cloud-python/pull/7793))
- Respect `progress_bar_type` in `to_dataframe` when used with BQ Storage API ([#7697](https://github.com/googleapis/google-cloud-python/pull/7697))
- Refactor QueryJob.query to read from resource dictionary ([#7763](https://github.com/googleapis/google-cloud-python/pull/7763))
- Close the `to_dataframe` progress bar when finished. ([#7757](https://github.com/googleapis/google-cloud-python/pull/7757))
- Ensure that `KeyboardInterrupt` during `to_dataframe`no longer hangs. ([#7698](https://github.com/googleapis/google-cloud-python/pull/7698))
- Raise ValueError when BQ Storage is required but missing ([#7726](https://github.com/googleapis/google-cloud-python/pull/7726))
- Make `total_rows` available on RowIterator before iteration ([#7622](https://github.com/googleapis/google-cloud-python/pull/7622))
- Avoid masking auth errors in `to_dataframe` with BQ Storage API ([#7674](https://github.com/googleapis/google-cloud-python/pull/7674))

### New Features
- Add support for passing `client_info`. ([#7849](https://github.com/googleapis/google-cloud-python/pull/7849) and ([#7806](https://github.com/googleapis/google-cloud-python/pull/7806))
- Phase 1 for storing schemas for later use. ([#7761](https://github.com/googleapis/google-cloud-python/pull/7761))
- Add `destination` and related properties to LoadJob. ([#7710](https://github.com/googleapis/google-cloud-python/pull/7710))
- Add `clustering_fields` property to TableListItem ([#7692](https://github.com/googleapis/google-cloud-python/pull/7692))
- Add `created` and `expires` properties to TableListItem ([#7684](https://github.com/googleapis/google-cloud-python/pull/7684))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))
- Add `[all]` extras to install all extra dependencies ([#7610](https://github.com/googleapis/google-cloud-python/pull/7610))

### Documentation
- Move table and dataset snippets to samples/ directory ([#7683](https://github.com/googleapis/google-cloud-python/pull/7683))

### Internal / Testing Changes
- Blacken unit tests. ([#7960](https://github.com/googleapis/google-cloud-python/pull/7960))
- Cleanup client tests with method to create minimal table resource ([#7802](https://github.com/googleapis/google-cloud-python/pull/7802))

## 1.11.2

04-05-2019 08:16 PDT

### Dependencies

- Add dependency on protobuf. ([#7668](https://github.com/googleapis/google-cloud-python/pull/7668))

## 1.11.1

04-04-2019 09:19 PDT

### Internal / Testing Changes

- Increment version number in `setup.py`.

## 1.11.0

04-03-2019 19:33 PDT

### Implementation Changes

- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features

- Enable fastparquet support by using temporary file in `load_table_from_dataframe` ([#7545](https://github.com/googleapis/google-cloud-python/pull/7545))
- Allow string for copy sources, query destination, and default dataset ([#7560](https://github.com/googleapis/google-cloud-python/pull/7560))
- Add `progress_bar_type` argument to `to_dataframe` to use `tqdm` to display a progress bar ([#7552](https://github.com/googleapis/google-cloud-python/pull/7552))
- Call `get_table` in `list_rows` if the schema is not available ([#7621](https://github.com/googleapis/google-cloud-python/pull/7621))
- Fallback to BQ API when there are problems reading from BQ Storage. ([#7633](https://github.com/googleapis/google-cloud-python/pull/7633))
- Add methods for Models API ([#7562](https://github.com/googleapis/google-cloud-python/pull/7562))
- Add option to use BigQuery Storage API from IPython magics ([#7640](https://github.com/googleapis/google-cloud-python/pull/7640))

### Documentation

- Remove typo in `Table.from_api_repr` docstring. ([#7509](https://github.com/googleapis/google-cloud-python/pull/7509))
- Add docs session to nox configuration for BigQuery ([#7541](https://github.com/googleapis/google-cloud-python/pull/7541))

### Internal / Testing Changes

- Refactor `table()` methods into shared implementation. ([#7516](https://github.com/googleapis/google-cloud-python/pull/7516))
- Blacken noxfile and setup file in nox session ([#7619](https://github.com/googleapis/google-cloud-python/pull/7619))
- Actually use the `progress_bar_type` argument in `QueryJob.to_dataframe()`. ([#7616](https://github.com/googleapis/google-cloud-python/pull/7616))

## 1.10.0

03-06-2019 15:20 PST

### Implementation Changes

- Harden 'ArrayQueryParameter.from_api_repr' against missing 'parameterValue'. ([#7311](https://github.com/googleapis/google-cloud-python/pull/7311))
- Allow nested records w/ null values. ([#7297](https://github.com/googleapis/google-cloud-python/pull/7297))

### New Features

- Add `exists_ok` and `not_found_ok` options to ignore errors when creating/deleting datasets/tables. ([#7491](https://github.com/googleapis/google-cloud-python/pull/7491))
- Accept a string in Table and Dataset constructors. ([#7483](https://github.com/googleapis/google-cloud-python/pull/7483))

### Documentation

- Update docstring of RowIterator's to_dataframe ([#7306](https://github.com/googleapis/google-cloud-python/pull/7306))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes

- Fix lint. ([#7383](https://github.com/googleapis/google-cloud-python/pull/7383))

## 1.9.0

02-04-2019 13:28 PST

### New Features

- Add arguments to select `dtypes` and use BQ Storage API to `QueryJob.to_dataframe()`. ([#7241](https://github.com/googleapis/google-cloud-python/pull/7241))

### Documentation

- Add sample for fetching `total_rows` from query results. ([#7217](https://github.com/googleapis/google-cloud-python/pull/7217))

## 1.8.1

12-17-2018 17:53 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for 'page_size' / 'max_results' / 'page_token' ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 1.8.0

12-10-2018 12:39 PST


### Implementation Changes
- Add option to use BQ Storage API with `to_dataframe` ([#6854](https://github.com/googleapis/google-cloud-python/pull/6854))
- Fix exception type in comment ([#6847](https://github.com/googleapis/google-cloud-python/pull/6847))
- Add `to_bqstorage` to convert from Table[Reference] google-cloud-bigquery-storage reference ([#6840](https://github.com/googleapis/google-cloud-python/pull/6840))
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Add avro logical type control for load jobs. ([#6827](https://github.com/googleapis/google-cloud-python/pull/6827))
- Allow setting partition expiration to 'None'. ([#6823](https://github.com/googleapis/google-cloud-python/pull/6823))
- Add `retry` argument to `_AsyncJob.result`. ([#6302](https://github.com/googleapis/google-cloud-python/pull/6302))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))

### Documentation
- Add avro load samples ([#6832](https://github.com/googleapis/google-cloud-python/pull/6832))

### Internal / Testing Changes
- Blacken libraries ([#6794](https://github.com/googleapis/google-cloud-python/pull/6794))
- Fix copy/paste typos in noxfile comments ([#6831](https://github.com/googleapis/google-cloud-python/pull/6831))

## 1.7.0

11-05-2018 16:41 PST

### Implementation Changes

- Add destination table properties to `LoadJobConfig`. ([#6202](https://github.com/googleapis/google-cloud-python/pull/6202))
- Allow strings or references in `create_dataset` and `create_table` ([#6199](https://github.com/googleapis/google-cloud-python/pull/6199))
- Fix swallowed error message ([#6168](https://github.com/googleapis/google-cloud-python/pull/6168))

### New Features

- Add `--params option` to `%%bigquery` magic ([#6277](https://github.com/googleapis/google-cloud-python/pull/6277))
- Expose `to_api_repr` method for jobs. ([#6176](https://github.com/googleapis/google-cloud-python/pull/6176))
- Allow string in addition to DatasetReference / TableReference in Client methods. ([#6164](https://github.com/googleapis/google-cloud-python/pull/6164))
- Add keyword arguments to job config constructors for setting properties ([#6397](https://github.com/googleapis/google-cloud-python/pull/6397))

### Documentation

- Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Move usage guides to their own docs. ([#6238](https://github.com/googleapis/google-cloud-python/pull/6238))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes

- Deprecation cleanups ([#6304](https://github.com/googleapis/google-cloud-python/pull/6304))
- Use `_get_sub_prop` helper so missing load stats don't raise. ([#6269](https://github.com/googleapis/google-cloud-python/pull/6269))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Harden snippets against transient GCS errors. ([#6184](https://github.com/googleapis/google-cloud-python/pull/6184))

## 1.6.0

### New Features
- Add support for `GEOGRAPHY` type ([#6147](https://github.com/googleapis/google-cloud-python/pull/6147))
- Add default QueryJobConfig to Client ([#6088](https://github.com/googleapis/google-cloud-python/pull/6088))

### Documentation
- Remove unused "append" samples ([#6100](https://github.com/googleapis/google-cloud-python/pull/6100))

### Internal / Testing Changes
- Address dataset leaks, conflicts in systests ([#6099](https://github.com/googleapis/google-cloud-python/pull/6099))
- Harden bucket teardown against `429 Too Many Requests`. ([#6101](https://github.com/googleapis/google-cloud-python/pull/6101))

## 1.5.1

### Implementation Changes

- Retry '502 Bad Gateway' errors by default. (#5930)
- Avoid pulling entire result set into memory when constructing dataframe. (#5870)
- Add support for retrying unstructured 429 / 500 / 502 responses. (#6011)
- Populate the jobReference from the API response. (#6044)

### Documentation

- Prepare documentation for repo split (#5955)
- Fix leakage of bigquery/spanner sections into sidebar menu. (#5986)

### Internal / Testing Changes

- Test pandas support under Python 3.7. (#5857)
- Nox: use inplace installs (#5865)
- Update system test to use test data in bigquery-public-data. (#5965)

## 1.5.0

### Implementation Changes

- Make 'Table.location' read-only. (#5687)

### New Features

- Add 'clustering_fields' properties. (#5630)
- Add support for job labels (#5654)
- Add 'QueryJob.estimated_bytes_processed' property (#5655)
- Add support/tests for loading tables from 'gzip.GzipFile'. (#5711)
- Add 'ExternalSourceFormat' enum. (#5674)
- Add default location to client (#5678)

### Documentation

- Fix typo in CopyJob sources docstring (#5690)

### Internal / Testing Changes

- Add/refactor snippets for managing BigQuery jobs (#5631)
- Reenable systests for 'dataset.update'/'table.update'. (#5732)

## 1.4.0

### Implementation Changes

- Add 'internalError' to retryable error reasons. (#5599)
- Don't raise exception if viewing CREATE VIEW DDL results (#5602)

### New Features

- Add Orc source format support and samples (#5500)
- Move 'DEFAULT_RETRY' (w/ its predicate) to a new public 'retry' module. (#5552)
- Allow listing rows on an empty table. (#5584)

### Documentation

- Add load_table_from_dataframe() to usage docs and changelog and dedents snippets in usage page (#5501)
- Add samples for query external data sources (GCS & Sheets) (#5491)
- Add BigQuery authorized view samples (#5515)
- Update docs to show pyarrow as the only dependency of load_table_from_dataframe() (#5582)

### Internal / Testing Changes

- Add missing explict coverage for '_helpers' (#5550)
- Skip update_table and update_dataset tests until etag issue is resolved. (#5590)

## 1.3.0

### New Features

- NUMERIC type support (#5331)
- Add timeline and top-level slot-millis to query statistics. (#5312)
- Add additional statistics to query plan stages. (#5307)
- Add `client.load_table_from_dataframe()` (#5387)

### Documentation

- Use autosummary to split up API reference docs (#5340)
- Fix typo in Client docstrings (#5342)

### Internal / Testing Changes

- Prune systests identified as reduntant to snippets. (#5365)
- Modify system tests to use prerelease versions of grpcio (#5304)
- Improve system test performance (#5319)

## 1.2.0

### Implementation Changes
- Switch `list_partitions` helper to a direct metatable read (#5273)
- Fix typo in `Encoding.ISO_8859_1` enum value (#5211)

### New Features
- Add UnknownJob type for redacted jobs. (#5281)
- Add project parameter to `list_datasets` and `list_jobs` (#5217)
- Add from_string factory methods to Dataset and Table (#5255)
- Add column based time partitioning (#5267)

### Documentation
- Standardize docstrings for constants (#5289)
- Fix docstring / impl of `ExtractJob.destination_uri_file_counts`. (#5245)

### Internal / Testing Changes
- Add testing support for Python 3.7; remove testing support for Python 3.4. (#5295)

## 1.1.0

### New Features
- Add `client.get_service_account_email` (#5203)

### Documentation
- Update samples and standardize region tags (#5195)

### Internal / Testing Changes
- Fix trove classifier to be Production/Stable
- Don't suppress 'dots' output on test (#5202)

## 1.0.0

### Implementation Changes
- Remove deprecated Client methods (#5182)

## 0.32.0

### :warning: Interface changes

- Use `job.configuration` resource for XXXJobConfig classes (#5036)

### Interface additions

- Add `page_size` parameter for `list_rows` and use in DB-API for `arraysize` (#4931)
- Add IPython magics for running queries (#4983)

### Documentation

- Add job string constant parameters in init and snippets documentation (#4987)

### Internal / Testing changes

- Specify IPython version 5.5 when running Python 2.7 tests (#5145)
- Move all Dataset property conversion logic into properties (#5130)
- Remove unnecessary _Table class from test_job.py (#5126)
- Use explicit bytes to initialize 'BytesIO'. (#5116)
- Make SchemaField be able to include description via from_api_repr method (#5114)
- Remove _ApiResourceProperty class (#5107)
- Add dev version for 0.32.0 release (#5105)
- StringIO to BytesIO (#5101)
- Shorten snippets test name (#5091)
- Don't use `selected_fields` for listing query result rows (#5072)
- Add location property to job classes. (#5071)
- Use autospec for Connection in tests. (#5066)
- Add Parquet SourceFormat and samples (#5057)
- Remove test_load_table_from_uri_w_autodetect_schema_then_get_job because of duplicate test in snippets (#5004)
- Fix encoding variable and strings UTF-8 and ISO-8859-1 difference documentation (#4990)

## 0.31.0

### Interface additions

- Add support for `EncryptionConfiguration` (#4845)

### Implementation changes

- Allow listing/getting jobs even when there is an "invalid" job. (#4786)

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Documentation

- Update format in `Table.full_table_id` and `TableListItem.full_table_id` docstrings. (#4906)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Remove unnecessary debug print from tests (#4907)
- Use constant strings for job properties in tests (#4833)

## 0.30.0

This is the release candidate for v1.0.0.

### Interface changes / additions

- Add `delete_contents` to `delete_dataset`. (#4724)

### Bugfixes

- Add handling of missing properties in `SchemaField.from_api_repr()`. (#4754)
- Fix missing return value in `LoadJobConfig.from_api_repr`. (#4727)

### Documentation

- Minor documentation and typo fixes. (#4782, #4718, #4784, #4835, #4836)

## 0.29.0

### Interface changes / additions

-   Add `to_dataframe()` method to row iterators. When Pandas is installed this
    method returns a `DataFrame` containing the query's or table's rows.
    ([#4354](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4354))
-   Iterate over a `QueryJob` to wait for and get the query results.
    ([#4350](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4350))
-   Add `Table.reference` and `Dataset.reference` properties to get the
    `TableReference` or `DatasetReference` corresponding to that `Table` or
    `Dataset`, respectively.
    ([#4405](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4405))
-   Add `Row.keys()`, `Row.items()`, and `Row.get()`. This makes `Row` act
    more like a built-in dictionary.
    ([#4393](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4393),
    [#4413](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4413))

### Interface changes / breaking changes

-   Add `Client.insert_rows()` and `Client.insert_rows_json()`, deprecate
    `Client.create_rows()` and `Client.create_rows_json()`.
    ([#4657](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4657))
-   Add `Client.list_tables`, deprecate `Client.list_dataset_tables`.
    ([#4653](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4653))
-   `Client.list_tables` returns an iterators of `TableListItem`. The API
    only returns a subset of properties of a table when listing.
    ([#4427](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4427))
-   Remove `QueryJob.query_results()`. Use `QueryJob.result()` instead.
    ([#4652](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4652))
-   Remove `Client.query_rows()`. Use `Client.query()` instead.
    ([#4429](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4429))
-   `Client.list_datasets` returns an iterator of `DatasetListItem`. The API
    only returns a subset of properties of a dataset when listing.
    ([#4439](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/4439))

## 0.28.0

**0.28.0 significantly changes the interface for this package.** For examples
of the differences between 0.28.0 and previous versions, see
[Migrating to the BigQuery Python client library 0.28][2].
These changes can be summarized as follows:

-   Query and view operations default to the standard SQL dialect. (#4192)
-   Client functions related to
    [jobs](https://cloud.google.com/bigquery/docs/jobs-overview), like running
    queries, immediately start the job.
-   Functions to create, get, update, delete datasets and tables moved to the
    client class.

[2]: https://cloud.google.com/bigquery/docs/python-client-migration

### Fixes

- Populate timeout parameter correctly for queries (#4209)
- Automatically retry idempotent RPCs (#4148, #4178)
- Parse timestamps in query parameters using canonical format (#3945)
- Parse array parameters that contain a struct type. (#4040)
- Support Sub Second Datetimes in row data (#3901, #3915, #3926), h/t @page1

### Interface changes / additions

- Support external table configuration (#4182) in query jobs (#4191) and
  tables (#4193).
- New `Row` class allows for access by integer index like a tuple, string
  index like a dictionary, or attribute access like an object. (#4149)
- Add option for job ID generation with user-supplied prefix (#4198)
- Add support for update of dataset access entries (#4197)
- Add support for atomic read-modify-write of a dataset using etag (#4052)
- Add support for labels to `Dataset` (#4026)
- Add support for labels to `Table` (#4207)
- Add `Table.streaming_buffer` property (#4161)
- Add `TableReference` class (#3942)
- Add `DatasetReference` class (#3938, #3942, #3993)
- Add `ExtractJob.destination_uri_file_counts` property. (#3803)
- Add `client.create_rows_json()` to bypass conversions on streaming writes.
  (#4189)
- Add `client.get_job()` to get arbitrary jobs. (#3804, #4213)
- Add filter to `client.list_datasets()` (#4205)
- Add `QueryJob.undeclared_query_parameters` property. (#3802)
- Add `QueryJob.referenced_tables` property. (#3801)
- Add new scalar statistics properties to `QueryJob` (#3800)
- Add `QueryJob.query_plan` property. (#3799)

### Interface changes / breaking changes

- Remove `client.run_async_query()`, use `client.query()` instead. (#4130)
- Remove `client.run_sync_query()`, use `client.query_rows()` instead. (#4065, #4248)
- Make `QueryResults` read-only. (#4094, #4144)
- Make `get_query_results` private. Return rows for `QueryJob.result()` (#3883)
- Move `*QueryParameter` and `UDFResource` classes to `query` module (also
  exposed in `bigquery` module). (#4156)

#### Changes to tables

- Remove `client` from `Table` class (#4159)
- Remove `table.exists()` (#4145)
- Move `table.list_parations` to `client.list_partitions` (#4146)
- Move `table.upload_from_file` to `client.load_table_from_file` (#4136)
- Move `table.update()` and `table.patch()` to `client.update_table()` (#4076)
- Move `table.insert_data()` to `client.create_rows()`. Automatically
  generates row IDs if not supplied. (#4151, #4173)
- Move `table.fetch_data()` to `client.list_rows()` (#4119, #4143)
- Move `table.delete()` to `client.delete_table()` (#4066)
- Move `table.create()` to `client.create_table()` (#4038, #4043)
- Move `table.reload()` to `client.get_table()` (#4004)
- Rename `Table.name` attribute to `Table.table_id` (#3959)
- `Table` constructor takes a `TableReference` as parameter (#3997)

#### Changes to datasets

- Remove `client` from `Dataset` class (#4018)
- Remove `dataset.exists()` (#3996)
- Move `dataset.list_tables()` to `client.list_dataset_tables()` (#4013)
- Move `dataset.delete()` to `client.delete_dataset()` (#4012)
- Move `dataset.patch()` and `dataset.update()` to `client.update_dataset()` (#4003)
- Move `dataset.create()` to `client.create_dataset()` (#3982)
- Move `dataset.reload()` to `client.get_dataset()` (#3973)
- Rename `Dataset.name` attribute to `Dataset.dataset_id` (#3955)
- `client.dataset()` returns a `DatasetReference` instead of `Dataset`. (#3944)
- Rename class: `dataset.AccessGrant -> dataset.AccessEntry`. (#3798)
- `dataset.table()` returns a `TableReference` instead of a `Table` (#4014)
- `Dataset` constructor takes a DatasetReference (#4036)

#### Changes to jobs

- Make `job.begin()` method private. (#4242)
- Add `LoadJobConfig` class and modify `LoadJob` (#4103, #4137)
- Add `CopyJobConfig` class and modify `CopyJob` (#4051, #4059)
- Type of Job's and Query's `default_dataset` changed from `Dataset` to
  `DatasetReference` (#4037)
- Rename `client.load_table_from_storage()` to `client.load_table_from_uri()`
  (#4235)
- Rename `client.extract_table_to_storage` to `client.extract_table()`.
  Method starts the extract job immediately. (#3991, #4177)
- Rename `XJob.name` to `XJob.job_id`. (#3962)
- Rename job classes. `LoadTableFromStorageJob -> LoadJob` and
  `ExtractTableToStorageJob -> jobs.ExtractJob` (#3797)

### Dependencies

- Updating to `google-cloud-core ~= 0.28`, in particular, the
  `google-api-core` package has been moved out of `google-cloud-core`. (#4221)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.28.0/


## 0.27.0

- Remove client-side enum validation. (#3735)
- Add `Table.row_from_mapping` helper. (#3425)
- Move `google.cloud.future` to `google.api.core` (#3764)
- Fix `__eq__` and `__ne__`. (#3765)
- Move `google.cloud.iterator` to `google.api.core.page_iterator` (#3770)
- `nullMarker` support for BigQuery Load Jobs (#3777), h/t @leondealmeida
- Allow `job_id` to be explicitly specified in DB-API. (#3779)
- Add support for a custom null marker. (#3776)
- Add `SchemaField` serialization and deserialization. (#3786)
- Add `get_query_results` method to the client. (#3838)
- Poll for query completion via `getQueryResults` method. (#3844)
- Allow fetching more than the first page when `max_results` is set. (#3845)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.27.0/

## 0.26.0

### Notable implementation changes

- Using the `requests` transport attached to a Client for for resumable media
  (i.e. downloads and uploads) (#3705) (this relates to the `httplib2` to
  `requests` switch)

### Interface changes / additions

- Adding `autodetect` property on `LoadTableFromStorageJob` to enable schema
  autodetection. (#3648)
- Implementing the Python Futures interface for Jobs. Call `job.result()` to
  wait for jobs to complete instead of polling manually on the job status.
  (#3626)
- Adding `is_nullable` property on `SchemaField`. Can be used to check if a
  column is nullable. (#3620)
- `job_name` argument added to `Table.upload_from_file` for setting the job
  ID. (#3605)
- Adding `google.cloud.bigquery.dbapi` package, which implements PEP-249
  DB-API specification. (#2921)
- Adding `Table.view_use_legacy_sql` property. Can be used to create views
  with legacy or standard SQL. (#3514)

### Interface changes / breaking changes

- Removing `results()` method from the `QueryJob` class. Use
  `query_results()` instead. (#3661)
- `SchemaField` is now immutable. It is also hashable so that it can be used
  in sets. (#3601)

### Dependencies

- Updating to `google-cloud-core ~= 0.26`, in particular, the underlying HTTP
  transport switched from `httplib2` to `requests` (#3654, #3674)
- Adding dependency on `google-resumable-media` for loading BigQuery tables
  from local files. (#3555)

### Packaging

- Fix inclusion of `tests` (vs. `unit_tests`) in `MANIFEST.in` (#3552)
- Updating `author_email` in `setup.py` to `googleapis-publisher@google.com`.
  (#3598)

PyPI: https://pypi.org/project/google-cloud-bigquery/0.26.0/
