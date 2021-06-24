# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-spanner/#history

## [3.6.0](https://www.github.com/googleapis/python-spanner/compare/v3.5.0...v3.6.0) (2021-06-23)


### Features

* add RPC priority support ([#324](https://www.github.com/googleapis/python-spanner/issues/324)) ([51533b8](https://www.github.com/googleapis/python-spanner/commit/51533b812b68004eafeb402641b974e76bf9a837))
* add support for low-cost instances ([#313](https://www.github.com/googleapis/python-spanner/issues/313)) ([44aa7cc](https://www.github.com/googleapis/python-spanner/commit/44aa7cc79769b6b7870b9de7204094f816150a25))
* **spanner:** add processing_units to Instance resource ([#364](https://www.github.com/googleapis/python-spanner/issues/364)) ([113505c](https://www.github.com/googleapis/python-spanner/commit/113505c58dc52509973f4199330a8983e3c5d848))
* update query stats samples ([#373](https://www.github.com/googleapis/python-spanner/issues/373)) ([c1ee8c2](https://www.github.com/googleapis/python-spanner/commit/c1ee8c2685a794f9f89329e16f7c461e135114af))


### Bug Fixes

* **db_api:** use sqlparse to split DDL statements ([#372](https://www.github.com/googleapis/python-spanner/issues/372)) ([ed9e124](https://github.com/googleapis/python-spanner/commit/ed9e124aa74e44778104e45eae1e577978d6b866))
* **db_api:** classify batched DDL statements ([#360](https://www.github.com/googleapis/python-spanner/issues/360)) ([b8b24e1](https://www.github.com/googleapis/python-spanner/commit/b8b24e17a74c1296ca5de75798a1a32597691b53))
* **deps:** add packaging requirement ([#368](https://www.github.com/googleapis/python-spanner/issues/368)) ([89c126c](https://www.github.com/googleapis/python-spanner/commit/89c126ceca327fcf9f344dace691522e7351dde7))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-spanner/issues/1127)) ([#374](https://www.github.com/googleapis/python-spanner/issues/374)) ([b7b3c38](https://www.github.com/googleapis/python-spanner/commit/b7b3c383abcca99dcbae6d92b27c49ca6707010a)), closes [#1126](https://www.github.com/googleapis/python-spanner/issues/1126)

## [3.5.0](https://www.github.com/googleapis/python-spanner/compare/v3.4.0...v3.5.0) (2021-06-11)


### Features

* add decimal validation for numeric precision and scale supported by Spanner ([#340](https://www.github.com/googleapis/python-spanner/issues/340)) ([aa36c5e](https://www.github.com/googleapis/python-spanner/commit/aa36c5ecf5b0decc6c5c3316cc5bc6b6981d9bf9))
* add progress field to UpdateDatabaseDdlMetadata ([#361](https://www.github.com/googleapis/python-spanner/issues/361)) ([1c03dcc](https://www.github.com/googleapis/python-spanner/commit/1c03dcc182fc96a2ca85b23da99cbcaebfb3fe09))
* add query statistics package support ([#129](https://www.github.com/googleapis/python-spanner/issues/129)) ([6598dea](https://www.github.com/googleapis/python-spanner/commit/6598deade66c8887514a1a6571fffb1bd7b16fd0))


### Bug Fixes

* an Aborted exception isn't properly retried ([#345](https://www.github.com/googleapis/python-spanner/issues/345)) ([e69e6ab](https://www.github.com/googleapis/python-spanner/commit/e69e6ab5cffd02bc9af6c08dbe9b5f229847d86d))
* correctly classify select statements that begin with brackets ([#351](https://www.github.com/googleapis/python-spanner/issues/351)) ([d526acc](https://www.github.com/googleapis/python-spanner/commit/d526acca4795ebf34867ab4a256413a728fccd93))
* update to support the open-telemetry status code spec change ([#358](https://www.github.com/googleapis/python-spanner/issues/358)) ([0f894f1](https://www.github.com/googleapis/python-spanner/commit/0f894f12622cfa6e38b838eb91e49f256d8d857d))

## [3.4.0](https://www.github.com/googleapis/python-spanner/compare/v3.3.0...v3.4.0) (2021-04-29)


### Features

* add samples for CMEK support ([#275](https://www.github.com/googleapis/python-spanner/issues/275)) ([f8d9bd3](https://www.github.com/googleapis/python-spanner/commit/f8d9bd33e04675a8dca148c2fae4a9133beebbca))
* added support for numeric field for python decimal value ([#316](https://www.github.com/googleapis/python-spanner/issues/316)) ([070a171](https://www.github.com/googleapis/python-spanner/commit/070a1712dc34afb68105194060bb2fe6177fbac5))
* **dbapi:** remove string conversion for numeric fields ([#317](https://www.github.com/googleapis/python-spanner/issues/317)) ([772aa3c](https://www.github.com/googleapis/python-spanner/commit/772aa3c2ffbdf3f863c09db176697b3ad70adbcf))


### Bug Fixes

* correctly set resume token when restarting streams ([#314](https://www.github.com/googleapis/python-spanner/issues/314)) ([0fcfc23](https://www.github.com/googleapis/python-spanner/commit/0fcfc2301246d3f20b6fbffc1deae06f16721ec7))
* support INSERT from SELECT clause with args ([#306](https://www.github.com/googleapis/python-spanner/issues/306)) ([0dcda5e](https://www.github.com/googleapis/python-spanner/commit/0dcda5e21f8fb30ee611fddf0829684d86ced0ef))


### Performance Improvements

* use protobuf for metadata to reduce type conversions ([#325](https://www.github.com/googleapis/python-spanner/issues/325)) ([5110b9b](https://www.github.com/googleapis/python-spanner/commit/5110b9bc31804db9777a23fca60360119840640c))

## [3.3.0](https://www.github.com/googleapis/python-spanner/compare/v3.2.0...v3.3.0) (2021-03-25)


### Features

* add encryption_info to Database ([#284](https://www.github.com/googleapis/python-spanner/issues/284)) ([2fd0352](https://www.github.com/googleapis/python-spanner/commit/2fd0352f695d7ab85e57d8c4388f42f91cf39435))
* add support for CMEK ([#105](https://www.github.com/googleapis/python-spanner/issues/105)) ([e990ff7](https://www.github.com/googleapis/python-spanner/commit/e990ff70342e7c2e27059e82c8d74cce39eb85d0))
* add support for custom timeout and retry parameters in execute_update method in transactions ([#251](https://www.github.com/googleapis/python-spanner/issues/251)) ([8abaebd](https://www.github.com/googleapis/python-spanner/commit/8abaebd9edac198596e7bd51d068d50147d0391d))
* added retry and timeout params to partition read in database and snapshot class ([#278](https://www.github.com/googleapis/python-spanner/issues/278)) ([1a7c9d2](https://www.github.com/googleapis/python-spanner/commit/1a7c9d296c23dfa7be7b07ea511a4a8fc2c0693f))
* **db_api:** support executing several DDLs separated by semicolon ([#277](https://www.github.com/googleapis/python-spanner/issues/277)) ([801ddc8](https://www.github.com/googleapis/python-spanner/commit/801ddc87434ff9e3c86b1281ebfeac26195c06e8))


### Bug Fixes

* avoid consuming pending null values when merging ([#286](https://www.github.com/googleapis/python-spanner/issues/286)) ([c6cba9f](https://www.github.com/googleapis/python-spanner/commit/c6cba9fbe4c717f1f8e2a97e3f76bfe6b956e55b))
* **db_api:** allow file path for credentials ([#221](https://www.github.com/googleapis/python-spanner/issues/221)) ([1de0284](https://www.github.com/googleapis/python-spanner/commit/1de028430b779a50d38242fe70567e92b560df5a))
* **db_api:** ensure DDL statements are being executed ([#290](https://www.github.com/googleapis/python-spanner/issues/290)) ([baa02ee](https://www.github.com/googleapis/python-spanner/commit/baa02ee1a352f7c509a3e169927cf220913e521f))
* **db_api:** revert Mutations API usage ([#285](https://www.github.com/googleapis/python-spanner/issues/285)) ([e5d4901](https://www.github.com/googleapis/python-spanner/commit/e5d4901e9b7111b39dfec4c56032875dc7c6e74c))


### Documentation

* fix docstring types and typos ([#259](https://www.github.com/googleapis/python-spanner/issues/259)) ([1b0ce1d](https://www.github.com/googleapis/python-spanner/commit/1b0ce1d2986085ce4033cf773eb6c5d3b904473c))
* fix snapshot usage ([#291](https://www.github.com/googleapis/python-spanner/issues/291)) ([eee2181](https://www.github.com/googleapis/python-spanner/commit/eee218164c3177586b73278aa21495280984af89))

## [3.2.0](https://www.github.com/googleapis/python-spanner/compare/v3.1.0...v3.2.0) (2021-03-02)


### Features

* add `Database.list_tables` method ([#219](https://www.github.com/googleapis/python-spanner/issues/219)) ([28bde8c](https://www.github.com/googleapis/python-spanner/commit/28bde8c18fd76b25ec1b64c44db7c1600255256f))
* add sample for commit stats ([#241](https://www.github.com/googleapis/python-spanner/issues/241)) ([1343656](https://www.github.com/googleapis/python-spanner/commit/1343656ad43dbc41c119b652d8fe9360fa2b0e78))
* add samples for PITR ([#222](https://www.github.com/googleapis/python-spanner/issues/222)) ([da146b7](https://www.github.com/googleapis/python-spanner/commit/da146b7a5d1d2ab6795c53301656d39e5594962f))


### Bug Fixes

* remove print statement ([#245](https://www.github.com/googleapis/python-spanner/issues/245)) ([1c2a64f](https://www.github.com/googleapis/python-spanner/commit/1c2a64fd06404bb7c2dfb4a8f65edd64c7710340))

## [3.1.0](https://www.github.com/googleapis/python-spanner/compare/v3.0.0...v3.1.0) (2021-02-23)


### Features

* add support for Point In Time Recovery (PITR) ([#148](https://www.github.com/googleapis/python-spanner/issues/148)) ([a082e5d](https://www.github.com/googleapis/python-spanner/commit/a082e5d7d2195ab9429a8e0bef4a664b59fdf771))
* add support to log commit stats ([#205](https://www.github.com/googleapis/python-spanner/issues/205)) ([434967e](https://www.github.com/googleapis/python-spanner/commit/434967e3a433b6516f5792dcbfef7ba950f091c5))


### Bug Fixes

* connection attribute of connection class and include related unit tests ([#228](https://www.github.com/googleapis/python-spanner/issues/228)) ([4afea77](https://www.github.com/googleapis/python-spanner/commit/4afea77812e021859377216cd950e1d9fc965ba8))
* **db_api:** add dummy lastrowid attribute ([#227](https://www.github.com/googleapis/python-spanner/issues/227)) ([0375914](https://www.github.com/googleapis/python-spanner/commit/0375914342de98e3903bae2097142325028d18d9))
* fix execute insert for homogeneous statement ([#233](https://www.github.com/googleapis/python-spanner/issues/233)) ([36b12a7](https://www.github.com/googleapis/python-spanner/commit/36b12a7b53cdbedf543d2b3bb132fb9e13cefb65))
* use datetime timezone info when generating timestamp strings ([#236](https://www.github.com/googleapis/python-spanner/issues/236)) ([539f145](https://www.github.com/googleapis/python-spanner/commit/539f14533afd348a328716aa511d453ca3bb19f5))


### Performance Improvements

* improve streaming performance ([#240](https://www.github.com/googleapis/python-spanner/issues/240)) ([3e35d4a](https://www.github.com/googleapis/python-spanner/commit/3e35d4a0217081bcab4ee31b642cd3bff5e6f4b5))

## [3.0.0](https://www.github.com/googleapis/python-spanner/compare/v2.1.0...v3.0.0) (2021-01-15)


### ⚠ BREAKING CHANGES

* convert operations pbs into Operation objects when listing operations (#186)

### Features

* add support for instance labels ([#193](https://www.github.com/googleapis/python-spanner/issues/193)) ([ed462b5](https://www.github.com/googleapis/python-spanner/commit/ed462b567a1a33f9105ffb37ba1218f379603614))
* add support for ssl credentials; add throttled field to UpdateDatabaseDdlMetadata ([#161](https://www.github.com/googleapis/python-spanner/issues/161)) ([2faf01b](https://www.github.com/googleapis/python-spanner/commit/2faf01b135360586ef27c66976646593fd85fd1e))
* adding missing docstrings for functions & classes  ([#188](https://www.github.com/googleapis/python-spanner/issues/188)) ([9788cf8](https://www.github.com/googleapis/python-spanner/commit/9788cf8678d882bd4ccf551f828050cbbb8c8f3a))
* autocommit sample ([#172](https://www.github.com/googleapis/python-spanner/issues/172)) ([4ef793c](https://www.github.com/googleapis/python-spanner/commit/4ef793c9cd5d6dec6e92faf159665e11d63762ad))


### Bug Fixes

* convert operations pbs into Operation objects when listing operations ([#186](https://www.github.com/googleapis/python-spanner/issues/186)) ([ed7152a](https://www.github.com/googleapis/python-spanner/commit/ed7152adc37290c63e59865265f36c593d9b8da3))
* Convert PBs in system test cleanup ([#199](https://www.github.com/googleapis/python-spanner/issues/199)) ([ede4343](https://www.github.com/googleapis/python-spanner/commit/ede4343e518780a4ab13ae83017480d7046464d6))
* **dbapi:** autocommit enabling fails if no transactions begun ([#177](https://www.github.com/googleapis/python-spanner/issues/177)) ([e981adb](https://www.github.com/googleapis/python-spanner/commit/e981adb3157bb06e4cb466ca81d74d85da976754))
* **dbapi:** executemany() hiding all the results except the last ([#181](https://www.github.com/googleapis/python-spanner/issues/181)) ([020dc17](https://www.github.com/googleapis/python-spanner/commit/020dc17c823dfb65bfaacace14d2c9f491c97e11))
* **dbapi:** Spanner protobuf changes causes KeyError's ([#206](https://www.github.com/googleapis/python-spanner/issues/206)) ([f1e21ed](https://www.github.com/googleapis/python-spanner/commit/f1e21edbf37aab93615fd415d61f829d2574916b))
* remove client side gRPC receive limits ([#192](https://www.github.com/googleapis/python-spanner/issues/192)) ([90effc4](https://www.github.com/googleapis/python-spanner/commit/90effc4d0f4780b7a7c466169f9fc1e45dab8e7f))
* Rename to fix "Mismatched region tag" check ([#201](https://www.github.com/googleapis/python-spanner/issues/201)) ([c000ec4](https://www.github.com/googleapis/python-spanner/commit/c000ec4d9b306baa0d5e9ed95f23c0273d9adf32))


### Documentation

* homogenize region tags ([#194](https://www.github.com/googleapis/python-spanner/issues/194)) ([1501022](https://www.github.com/googleapis/python-spanner/commit/1501022239dfa8c20290ca0e0cf6a36e9255732c))
* homogenize region tags pt 2 ([#202](https://www.github.com/googleapis/python-spanner/issues/202)) ([87789c9](https://www.github.com/googleapis/python-spanner/commit/87789c939990794bfd91f5300bedc449fd74bd7e))
* update CHANGELOG breaking change comment ([#180](https://www.github.com/googleapis/python-spanner/issues/180)) ([c7b3b9e](https://www.github.com/googleapis/python-spanner/commit/c7b3b9e4be29a199618be9d9ffa1d63a9d0f8de7))

## [2.1.0](https://www.github.com/googleapis/python-spanner/compare/v2.0.0...v2.1.0) (2020-11-24)


### Features

* **dbapi:** add aborted transactions retry support ([#168](https://www.github.com/googleapis/python-spanner/issues/168)) ([d59d502](https://www.github.com/googleapis/python-spanner/commit/d59d502590f618c8b13920ae05ab11add78315b5)), closes [#34](https://www.github.com/googleapis/python-spanner/issues/34) [googleapis/python-spanner-django#544](https://www.github.com/googleapis/python-spanner-django/issues/544)
* remove adding a dummy WHERE clause into UPDATE and DELETE statements ([#169](https://www.github.com/googleapis/python-spanner/issues/169)) ([7f4d478](https://www.github.com/googleapis/python-spanner/commit/7f4d478fd9812c965cdb185c52aa9a8c9e599bed))


### Bug Fixes

* Add sqlparse dependency ([#171](https://www.github.com/googleapis/python-spanner/issues/171)) ([e801a2e](https://www.github.com/googleapis/python-spanner/commit/e801a2e014fcff66a69cb9da83abedb218cda2ab))


### Reverts

* Revert "test: unskip list_backup_operations sample test (#170)" (#174) ([6053f4a](https://www.github.com/googleapis/python-spanner/commit/6053f4ab0fc647a9cfc181e16c246141483c2397)), closes [#170](https://www.github.com/googleapis/python-spanner/issues/170) [#174](https://www.github.com/googleapis/python-spanner/issues/174)

## [2.0.0](https://www.github.com/googleapis/python-spanner/compare/v1.19.1...v2.0.0) (2020-11-11)


### ⚠ BREAKING CHANGES

* list_instances, list_databases, list_instance_configs, and list_backups will now return protos rather than the handwritten wrapper (#147)

### Features

* DB-API driver + unit tests ([#160](https://www.github.com/googleapis/python-spanner/issues/160)) ([2493fa1](https://www.github.com/googleapis/python-spanner/commit/2493fa1725d2d613f6c064637a4e215ee66255e3))
* migrate to v2.0.0 ([#147](https://www.github.com/googleapis/python-spanner/issues/147)) ([bf4b278](https://www.github.com/googleapis/python-spanner/commit/bf4b27827494e3dc33b1e4333dfe147a36a486b3))

### [1.19.1](https://www.github.com/googleapis/python-spanner/compare/v1.19.0...v1.19.1) (2020-10-13)


### Bug Fixes

* handle Unmergable errors when merging struct responses ([#152](https://www.github.com/googleapis/python-spanner/issues/152)) ([d132409](https://www.github.com/googleapis/python-spanner/commit/d132409dd4300cb2dca7c4bc7dbdd4d429d2fa7c))


### Documentation

* update samples dep to 'google-cloud-spanner==1.19.0' ([#137](https://www.github.com/googleapis/python-spanner/issues/137)) ([0fba41a](https://www.github.com/googleapis/python-spanner/commit/0fba41a5c19b02b0424705618dd1e2e5ca12238f))
* update samples from python-docs-samples ([#146](https://www.github.com/googleapis/python-spanner/issues/146)) ([7549383](https://www.github.com/googleapis/python-spanner/commit/754938386c96814a3546d30d38d874734d1c201c))

## [1.19.0](https://www.github.com/googleapis/python-spanner/compare/v1.18.0...v1.19.0) (2020-09-08)


### Features

* add support for NUMERIC type ([#86](https://www.github.com/googleapis/python-spanner/issues/86)) ([a79786e](https://www.github.com/googleapis/python-spanner/commit/a79786ec3620da21aa3ce1c8bc820dab5983531d))


### Bug Fixes

* list_instances() uses filter_ arg ([#143](https://www.github.com/googleapis/python-spanner/issues/143)) ([340028c](https://www.github.com/googleapis/python-spanner/commit/340028c8eafcb715e6e440c6d98048ecea802807))
* Remove stray bigquery lines ([#138](https://www.github.com/googleapis/python-spanner/issues/138)) ([cbfcc8b](https://www.github.com/googleapis/python-spanner/commit/cbfcc8b06e1a5803a9b9a943a3bbf29467d9f2ed))

## [1.18.0](https://www.github.com/googleapis/python-spanner/compare/v1.17.1...v1.18.0) (2020-08-25)


### Features

* add client_options to base class ([#132](https://www.github.com/googleapis/python-spanner/issues/132)) ([6851bb8](https://www.github.com/googleapis/python-spanner/commit/6851bb86c21ca489a1982bda0d6e97cbccde341c))
* add OpenTelemetry tracing to spanner calls ([#107](https://www.github.com/googleapis/python-spanner/issues/107)) ([4069c37](https://www.github.com/googleapis/python-spanner/commit/4069c37bc7ac3c71c97fcd963e1d46c5fe15b3e6))


### Bug Fixes

* resume iterator on EOS internal error ([#122](https://www.github.com/googleapis/python-spanner/issues/122)) ([45a1538](https://www.github.com/googleapis/python-spanner/commit/45a15382bc1e62dedc944f6484c15ba929338670))


### Documentation

* add install reference for cloud trace exporter (opentelemetry) ([#127](https://www.github.com/googleapis/python-spanner/issues/127)) ([23fcd4c](https://www.github.com/googleapis/python-spanner/commit/23fcd4c91d908f00eda5ff57f6ccea3dfe936b57))
* add instructions for using a Cloud Spanner emulator ([#136](https://www.github.com/googleapis/python-spanner/issues/136)) ([808837b](https://www.github.com/googleapis/python-spanner/commit/808837b5afb34ba7d745b83e53274b5709a9ef63))
* add samples from spanner/cloud-client ([#117](https://www.github.com/googleapis/python-spanner/issues/117)) ([8910771](https://www.github.com/googleapis/python-spanner/commit/891077105d5093a73caf96683d10afef2cd17823)), closes [#804](https://www.github.com/googleapis/python-spanner/issues/804) [#815](https://www.github.com/googleapis/python-spanner/issues/815) [#818](https://www.github.com/googleapis/python-spanner/issues/818) [#887](https://www.github.com/googleapis/python-spanner/issues/887) [#914](https://www.github.com/googleapis/python-spanner/issues/914) [#922](https://www.github.com/googleapis/python-spanner/issues/922) [#928](https://www.github.com/googleapis/python-spanner/issues/928) [#962](https://www.github.com/googleapis/python-spanner/issues/962) [#992](https://www.github.com/googleapis/python-spanner/issues/992) [#1004](https://www.github.com/googleapis/python-spanner/issues/1004) [#1035](https://www.github.com/googleapis/python-spanner/issues/1035) [#1055](https://www.github.com/googleapis/python-spanner/issues/1055) [#1063](https://www.github.com/googleapis/python-spanner/issues/1063) [#1093](https://www.github.com/googleapis/python-spanner/issues/1093) [#1107](https://www.github.com/googleapis/python-spanner/issues/1107) [#1121](https://www.github.com/googleapis/python-spanner/issues/1121) [#1158](https://www.github.com/googleapis/python-spanner/issues/1158) [#1138](https://www.github.com/googleapis/python-spanner/issues/1138) [#1186](https://www.github.com/googleapis/python-spanner/issues/1186) [#1192](https://www.github.com/googleapis/python-spanner/issues/1192) [#1207](https://www.github.com/googleapis/python-spanner/issues/1207) [#1254](https://www.github.com/googleapis/python-spanner/issues/1254) [#1316](https://www.github.com/googleapis/python-spanner/issues/1316) [#1354](https://www.github.com/googleapis/python-spanner/issues/1354) [#1376](https://www.github.com/googleapis/python-spanner/issues/1376) [#1377](https://www.github.com/googleapis/python-spanner/issues/1377) [#1402](https://www.github.com/googleapis/python-spanner/issues/1402) [#1406](https://www.github.com/googleapis/python-spanner/issues/1406) [#1425](https://www.github.com/googleapis/python-spanner/issues/1425) [#1441](https://www.github.com/googleapis/python-spanner/issues/1441) [#1464](https://www.github.com/googleapis/python-spanner/issues/1464) [#1519](https://www.github.com/googleapis/python-spanner/issues/1519) [#1548](https://www.github.com/googleapis/python-spanner/issues/1548) [#1633](https://www.github.com/googleapis/python-spanner/issues/1633) [#1742](https://www.github.com/googleapis/python-spanner/issues/1742) [#1836](https://www.github.com/googleapis/python-spanner/issues/1836) [#1846](https://www.github.com/googleapis/python-spanner/issues/1846) [#1872](https://www.github.com/googleapis/python-spanner/issues/1872) [#1980](https://www.github.com/googleapis/python-spanner/issues/1980) [#2068](https://www.github.com/googleapis/python-spanner/issues/2068) [#2153](https://www.github.com/googleapis/python-spanner/issues/2153) [#2224](https://www.github.com/googleapis/python-spanner/issues/2224) [#2198](https://www.github.com/googleapis/python-spanner/issues/2198) [#2251](https://www.github.com/googleapis/python-spanner/issues/2251) [#2295](https://www.github.com/googleapis/python-spanner/issues/2295) [#2356](https://www.github.com/googleapis/python-spanner/issues/2356) [#2392](https://www.github.com/googleapis/python-spanner/issues/2392) [#2439](https://www.github.com/googleapis/python-spanner/issues/2439) [#2535](https://www.github.com/googleapis/python-spanner/issues/2535) [#2005](https://www.github.com/googleapis/python-spanner/issues/2005) [#2721](https://www.github.com/googleapis/python-spanner/issues/2721) [#3093](https://www.github.com/googleapis/python-spanner/issues/3093) [#3101](https://www.github.com/googleapis/python-spanner/issues/3101) [#2806](https://www.github.com/googleapis/python-spanner/issues/2806) [#3377](https://www.github.com/googleapis/python-spanner/issues/3377)
* typo fix ([#109](https://www.github.com/googleapis/python-spanner/issues/109)) ([63b4324](https://www.github.com/googleapis/python-spanner/commit/63b432472613bd80e234ee9c9f73906db2f0a52b))

### [1.17.1](https://www.github.com/googleapis/python-spanner/compare/v1.17.0...v1.17.1) (2020-06-24)


### Documentation

* remove client-usage sections that no longer apply ([#95](https://www.github.com/googleapis/python-spanner/issues/95)) ([16a812f](https://www.github.com/googleapis/python-spanner/commit/16a812fd32320f139213e752eb8210933081015b))
* update batch-usage reflect the correct usage ([#93](https://www.github.com/googleapis/python-spanner/issues/93)) ([6ec64d8](https://www.github.com/googleapis/python-spanner/commit/6ec64d8c001af9e53ff71a2940ec2a81964e6e7f))
* update documentation for database-usage ([#96](https://www.github.com/googleapis/python-spanner/issues/96)) ([44e398c](https://www.github.com/googleapis/python-spanner/commit/44e398c3aa9c1af661fecf2beed481484dd05713))
* update documentation for snapshot usage ([#94](https://www.github.com/googleapis/python-spanner/issues/94)) ([613d9c8](https://www.github.com/googleapis/python-spanner/commit/613d9c820b1c87d2e86ef4084dfe9f767eb70079))

## [1.17.0](https://www.github.com/googleapis/python-spanner/compare/v1.16.0...v1.17.0) (2020-05-26)


### Features

* add support for using the emulator programatically ([#87](https://www.github.com/googleapis/python-spanner/issues/87)) ([b22630b](https://www.github.com/googleapis/python-spanner/commit/b22630b8e2b543207c6f4d9a13e2925e8692c8c5))


### Bug Fixes

* update backup timeouts (via synth) ([#82](https://www.github.com/googleapis/python-spanner/issues/82)) ([f5d74a0](https://www.github.com/googleapis/python-spanner/commit/f5d74a03d5cc84befa3817f83ad2655af6fe5741))

## [1.16.0](https://www.github.com/googleapis/python-spanner/compare/v1.15.1...v1.16.0) (2020-05-05)


### Features

* add support for retrying aborted partitioned DML statements ([#66](https://www.github.com/googleapis/python-spanner/issues/66)) ([8a3d700](https://www.github.com/googleapis/python-spanner/commit/8a3d700134a6380c033a879cff0616a648df709b))


### Bug Fixes

* add keepalive changes to synth.py ([#55](https://www.github.com/googleapis/python-spanner/issues/55)) ([805bbb7](https://www.github.com/googleapis/python-spanner/commit/805bbb766fd9c019f528e2f8ed1379d997622d03))
* pass gRPC config options to gRPC channel creation ([#26](https://www.github.com/googleapis/python-spanner/issues/26)) ([6c9a1ba](https://www.github.com/googleapis/python-spanner/commit/6c9a1badfed610a18454137e1b45156872914e7e))

### [1.15.1](https://www.github.com/googleapis/python-spanner/compare/v1.15.0...v1.15.1) (2020-04-08)


### Bug Fixes

* add keepalive to gRPC channel ([#49](https://www.github.com/googleapis/python-spanner/issues/49)) ([dfbc656](https://www.github.com/googleapis/python-spanner/commit/dfbc656891c687bc077f811f8490ae92818307f8))
* increment seqno before execute calls to prevent InvalidArgument … ([#19](https://www.github.com/googleapis/python-spanner/issues/19)) ([adeacee](https://www.github.com/googleapis/python-spanner/commit/adeacee3cc07260fa9fcd496b3187402f02bf157))
* Pin Sphnix version to last working release ([#51](https://www.github.com/googleapis/python-spanner/issues/51)) ([430ca32](https://www.github.com/googleapis/python-spanner/commit/430ca32fcbedebdfdb00366008a72d8229e4df98))

## [1.15.0](https://www.github.com/googleapis/python-spanner/compare/v1.14.0...v1.15.0) (2020-03-17)


### Features

* Add emulator support ([#14](https://www.github.com/googleapis/python-spanner/issues/14)) ([b315593](https://www.github.com/googleapis/python-spanner/commit/b315593bd3e473d96cc3033f5bbf0da7487e38eb))
* Export transaction._rolled_back as transaction.rolled_back ([#16](https://www.github.com/googleapis/python-spanner/issues/16)) ([974ee92](https://www.github.com/googleapis/python-spanner/commit/974ee925df1962f559d6cb43318ee301e330e8f2))
* Add support for backups ([#35](https://www.github.com/googleapis/python-spanner/issues/35)) ([39288e7](https://www.github.com/googleapis/python-spanner/commit/39288e784826c5accca71096be11f99ad7f930f4))
* Implement query options versioning support ([#30](https://www.github.com/googleapis/python-spanner/issues/30)) ([5147921](https://www.github.com/googleapis/python-spanner/commit/514792151c2fe4fc7a6cf4ad0dd141c9090a634b))


### Bug Fixes

* Remove erroneous timeouts for batch_create_session calls ([#18](https://www.github.com/googleapis/python-spanner/issues/18)) ([997a034](https://www.github.com/googleapis/python-spanner/commit/997a03477b07ec39c718480d9bfe729404bf5748))

## [1.14.0](https://www.github.com/googleapis/python-spanner/compare/v1.13.0...v1.14.0) (2020-01-31)


### Features

* Add deprecation warnings; add field_mask to get_instance; add endpoint_uris to Instance proto; update timeouts; make mutations optional for commits (via synth) ([62edbe1](https://www.github.com/googleapis/python-spanner/commit/62edbe12a0c5a74eacb8d87ca265a19e6d27f890))
* Add resource based routing implementation ([#10183](https://www.github.com/googleapis/google-cloud-python/issues/10183)) ([e072d5d](https://www.github.com/googleapis/python-spanner/commit/e072d5dd04d58fff7f62ce19ce42e906dfd11012))
* Un-deprecate resource name helper functions, add 3.8 tests (via synth) ([#10062](https://www.github.com/googleapis/google-cloud-python/issues/10062)) ([dbb79b0](https://www.github.com/googleapis/python-spanner/commit/dbb79b0d8b0c79f6ed1772f28e4eedb9d986b108))


### Bug Fixes

* Be permssive about merging an empty struct ([#10079](https://www.github.com/googleapis/google-cloud-python/issues/10079)) ([cfae63d](https://www.github.com/googleapis/python-spanner/commit/cfae63d5a8b8332f8875307283da6075a544c838))
* Fix imports for doc samples ([#10283](https://www.github.com/googleapis/google-cloud-python/issues/10283)) ([55a21d9](https://www.github.com/googleapis/python-spanner/commit/55a21d97d0c863cbbbb2d973b6faa4aeba8e38bb))

## 1.13.0

11-11-2019 15:59 PST


### Implementation Changes
Fix TransactionPingingPool to stop thowing ''NoneType' object is not callable' error. ([#9609](https://github.com/googleapis/google-cloud-python/pull/9609))
Return sessions from pool in LIFO order. ([#9454](https://github.com/googleapis/google-cloud-python/pull/9454))

### Documentation
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Update description of the `timeout_secs` parameter. ([#9381](https://github.com/googleapis/google-cloud-python/pull/9381))

### Internal / Testing Changes
- Harden `test_transaction_batch_update*` systests against partial success + abort. ([#9579](https://github.com/googleapis/google-cloud-python/pull/9579))

## 1.12.0

10-23-2019 19:09 PDT


### Implementation Changes
- Add `batch_create_session` calls to session pools. ([#9488](https://github.com/googleapis/google-cloud-python/pull/9488))

### New Features
- Add `client_options` to client constructor. ([#9151](https://github.com/googleapis/google-cloud-python/pull/9151))

### Internal / Testing Changes
- Harden 'test_reload_instance' systest against eventual consistency failures. ([#9394](https://github.com/googleapis/google-cloud-python/pull/9394))
- Harden 'test_transaction_batch_update_w_syntax_error' systest. ([#9395](https://github.com/googleapis/google-cloud-python/pull/9395))
- Propagate errors from 'Transaction.batch_update' in systest. ([#9393](https://github.com/googleapis/google-cloud-python/pull/9393))

## 1.11.0

10-15-2019 06:55 PDT


### Implementation Changes
- Adjust gRPC timeouts (via synth). ([#9330](https://github.com/googleapis/google-cloud-python/pull/9330))
- Make `session_count` optional for `SpannerClient.batch_create_sessions` (via synth). ([#9280](https://github.com/googleapis/google-cloud-python/pull/9280))
- Remove send / receive message size limit, update docstrings (via synth). ([#8968](https://github.com/googleapis/google-cloud-python/pull/8968))

### New Features
- Add `batch_create_sessions` method to generated client (via synth). ([#9087](https://github.com/googleapis/google-cloud-python/pull/9087))

### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

### Documentation
- Remove references to old authentication credentials in docs. ([#9456](https://github.com/googleapis/google-cloud-python/pull/9456))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Fix `run_in_transaction` return value docs. ([#9264](https://github.com/googleapis/google-cloud-python/pull/9264))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Add DML insert and update examples to README. ([#8698](https://github.com/googleapis/google-cloud-python/pull/8698))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.10.0

07-24-2019 17:32 PDT


### Implementation Changes
- Add backoff for `run_in_transaction` when backend does not provide 'RetryInfo' in response. ([#8461](https://github.com/googleapis/google-cloud-python/pull/8461))
- Adjust gRPC timeouts (via synth). ([#8445](https://github.com/googleapis/google-cloud-python/pull/8445))
- Allow kwargs to be passed to create_channel (via synth). ([#8403](https://github.com/googleapis/google-cloud-python/pull/8403))

### New Features
- Add 'options\_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8659](https://github.com/googleapis/google-cloud-python/pull/8659))
- Add 'client_options' support, update list method docstrings (via synth). ([#8522](https://github.com/googleapis/google-cloud-python/pull/8522))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Fixes [#8545](https://github.com/googleapis/google-cloud-python/pull/8545) by removing typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8363](https://github.com/googleapis/google-cloud-python/pull/8363))
- Add disclaimer to auto-generated template files (via synth). ([#8327](https://github.com/googleapis/google-cloud-python/pull/8327))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8251](https://github.com/googleapis/google-cloud-python/pull/8251))
- Blacken noxfile.py, setup.py (via synth). ([#8131](https://github.com/googleapis/google-cloud-python/pull/8131))
- Harden synth replacement against template adding whitespace. ([#8103](https://github.com/googleapis/google-cloud-python/pull/8103))

## 1.9.0

05-16-2019 12:54 PDT


### Implementation Changes
- Add routing header to method metadata (via synth). ([#7750](https://github.com/googleapis/google-cloud-python/pull/7750))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to client. ([#7878](https://github.com/googleapis/google-cloud-python/pull/7878))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Expand API reference for snapshot / transaction. ([#7618](https://github.com/googleapis/google-cloud-python/pull/7618))

### Internal / Testing Changes
- Add nox session `docs`, remove retries for DEADLINE_EXCEEDED (via synth). ([#7781](https://github.com/googleapis/google-cloud-python/pull/7781))
- Added matching END tags to Spanner Tests ([#7529](https://github.com/googleapis/google-cloud-python/pull/7529))

## 1.8.0

03-05-2019 12:57 PST


### Implementation Changes
- Protoc-generated serialization update. ([#7095](https://github.com/googleapis/google-cloud-python/pull/7095))
- Fix typo in exported param type name. ([#7295](https://github.com/googleapis/google-cloud-python/pull/7295))

### New Features
- Add Batch DML support. ([#7485](https://github.com/googleapis/google-cloud-python/pull/7485))

### Documentation
- Copy lintified proto files, update docstrings (via synth). ([#7453](https://github.com/googleapis/google-cloud-python/pull/7453))
- Fix Batch object creation instructions. ([#7341](https://github.com/googleapis/google-cloud-python/pull/7341))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Fix README to install spanner instead of datastore. ([#7301](https://github.com/googleapis/google-cloud-python/pull/7301))

### Internal / Testing Changes
- Add clarifying comment to blacken nox target. ([#7403](https://github.com/googleapis/google-cloud-python/pull/7403))
- Ensure that GRPC config file is included in MANIFEST.in after templating. ([#7046](https://github.com/googleapis/google-cloud-python/pull/7046))
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers.

## 1.7.1

12-14-2018 15:18 PST


### Documentation
- Announce Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize documentation for 'page_size' / 'max_results' / 'page_token' ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

### Internal / Testing Changes
- Include grpc config in manifest ([#6928](https://github.com/googleapis/google-cloud-python/pull/6928))

## 1.7.0

12-10-2018 13:10 PST


### Implementation Changes
- Add PingingPool and TransactionPingingPool to toplevel module ([#6886](https://github.com/googleapis/google-cloud-python/pull/6886))
- Add `operation_id` parameter to `Database.update_ddl`. ([#6825](https://github.com/googleapis/google-cloud-python/pull/6825))
- Pick up changes to GAPIC method configuration ([#6615](https://github.com/googleapis/google-cloud-python/pull/6615))
- Add timeout + retry settings to Sessions/Snapshots ([#6536](https://github.com/googleapis/google-cloud-python/pull/6536))
- Pick up fixes to GAPIC generator. ([#6576](https://github.com/googleapis/google-cloud-python/pull/6576))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Blacken. ([#6846](https://github.com/googleapis/google-cloud-python/pull/6846))
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add tags to DML system tests ([#6580](https://github.com/googleapis/google-cloud-python/pull/6580))

## 1.6.1

11-09-2018 14:49 PST

### Implementation Changes
- Fix client_info bug, update docstrings. ([#6420](https://github.com/googleapis/google-cloud-python/pull/6420))

### Documentation
- Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Fix typo in spanner usage documentation ([#6209](https://github.com/googleapis/google-cloud-python/pull/6209))

### Internal / Testing Changes
- Rationalize 'all_types' round-trip systest ([#6379](https://github.com/googleapis/google-cloud-python/pull/6379))
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Add systest for returning empty array struct ([#4449](https://github.com/googleapis/google-cloud-python/pull/4449))
- Add systests not needing tables ([#6308](https://github.com/googleapis/google-cloud-python/pull/6308))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 1.6.0

10-08-2018 08:25 PDT

### New Features
- Add support for DML/PDML. ([#6151](https://github.com/googleapis/google-cloud-python/pull/6151))

### Implementation Changes
- Add 'synth.py' and regen GAPIC code. ([#6040](https://github.com/googleapis/google-cloud-python/pull/6040))

### Documentation
- Remove invalid examples of `database.transaction()`. ([#6032](https://github.com/googleapis/google-cloud-python/pull/6032))
- Redirect renamed `usage.html`/`client.html` -> `index.html`. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Fix leakage of sections into sidebar menu. ([#5986](https://github.com/googleapis/google-cloud-python/pull/5986))
- Prepare documentation for repo split. ([#5938](https://github.com/googleapis/google-cloud-python/pull/5938))

### Internal / Testing Changes
- Remove extra `grpc_gcp` system tests. ([#6049](https://github.com/googleapis/google-cloud-python/pull/6049))

## 1.5.0

### New Features

- Add support for session / pool labels ([#5734](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5734))
- Add support for gRPC connection management ([#5553](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5553))

### Dependencies

- Add `grpcio-gcp` dependency for Cloud Spanner ([#5904](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5904))

### Internal / Testing Changes

- Don't hardcode endpoint URL in grpc_gcp unit tests. ([#5893](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5893))
- Run `grpc_gcp` unit tests only with Python 2.7 / 3.6. ([#5871](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5871))
- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))
- Benchmarks: print() is a function in Python 3 ([#5862](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5862))
- Retry `test_transaction_read_and_insert_then_rollback` when aborted. ([#5737](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5737))
- Skip the flaky `test_update_database_ddl` systest. ([#5704](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5704))

## 1.4.0

### Implementation Changes
- Ensure that initial resume token is bytes, not text. (#5450)
- Prevent process_read_batch from mutating params (#5416)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Add support for Python 3.7 (#5288)
- Add support for Spanner struct params. (#5463)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)

## 1.3.0

### Interface additions

- Added `spanner_v1.COMMIT_TIMESTAMP`. (#5102)

## 1.2.0

### New features

- Added batch query support (#4938)

### Implementation changes

- Removed custom timestamp class in favor of the one in google-api-core. (#4980)

### Dependencies

- Update minimum version for google-api-core to 1.1.0 (#5030)

### Documentation

- Update package metadata release status to 'Stable' (#5031)

## 1.1.0

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Testing and internal changes

- Fix load_keys() in YCSB-like benchmark for cloud spanner. (#4919)
- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix system test util to populate streaming (#4888)
- Retry conflict errors in system test (#4850)

## 1.0.0

### Breaking Changes

- `to_pb` has now been made private (`_to_pb`) in `KeySet`
  and `KeyRange` (#4740)

### Documentation Changes
- Database update_ddl missing param in documentation (#4749)

## 0.30.0

### Breaking Changes

- The underlying autogenerated client library was re-generated to pick up new 
  features and resolve bugs, this may change the exceptions raised from various
  methods. (#4695)
- Made `StreamedResultSet`'s `row`, `consume_all`, and `consume_next` members
  private (#4492)

### Implementation Changes

- `Keyset` can now infer defaults to `start_closed` or `end_closed` when only one argument is specified. (#4735)

### Documentation

- Brought Spanner README more in line with others. (#4306, #4317)

### Testing

- Added several new system tests and fixed minor issues with existing tests. (
  #4631, #4569, #4573, #4572, #4416, #4411, #4407, #4386, #4419, #4489,
  #4678, #4620, #4418, #4403, #4397, #4383, #4371, #4372, #4374, #4370, #4285,
  #4321)
- Excluded generated code from linting. (#4375)
- Added a `nox -s default` session for all packages. (#4324)

## 0.29.0

### Implementation Changes

- **Bugfix**: Clear `session._transaction` before calling
  `_delay_until_retry` (#4185)
- **Bugfix**: Be permissive about merging an empty list. (#4170,
  fixes #4164)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos` dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-spanner/0.29.0/
