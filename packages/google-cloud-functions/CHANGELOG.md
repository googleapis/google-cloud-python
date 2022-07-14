# Changelog

## [1.8.0](https://github.com/googleapis/python-functions/compare/v1.7.0...v1.8.0) (2022-07-14)


### Features

* add audience parameter ([10a61fa](https://github.com/googleapis/python-functions/commit/10a61fa9fd9b0f343a2acfab83dea95011984e34))
* generate v2 ([#195](https://github.com/googleapis/python-functions/issues/195)) ([10a61fa](https://github.com/googleapis/python-functions/commit/10a61fa9fd9b0f343a2acfab83dea95011984e34))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([10a61fa](https://github.com/googleapis/python-functions/commit/10a61fa9fd9b0f343a2acfab83dea95011984e34))
* require python 3.7+ ([#197](https://github.com/googleapis/python-functions/issues/197)) ([6ed2206](https://github.com/googleapis/python-functions/commit/6ed2206eabbdad9a297d19a8b6893cc00b839dcc))

## [1.7.0](https://github.com/googleapis/python-functions/compare/v1.6.0...v1.7.0) (2022-06-06)


### Features

* added support for CMEK ([#188](https://github.com/googleapis/python-functions/issues/188)) ([fa7d695](https://github.com/googleapis/python-functions/commit/fa7d695822e8dc6bb26a2d17800a312c3220fc4c))


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#184](https://github.com/googleapis/python-functions/issues/184)) ([d1e8907](https://github.com/googleapis/python-functions/commit/d1e8907c5862549a412424009a7621b1f321548a))


### Documentation

* fix changelog header to consistent size ([#183](https://github.com/googleapis/python-functions/issues/183)) ([b28c780](https://github.com/googleapis/python-functions/commit/b28c780a405faaf4b068a8e2860932bab4f2ebd9))

## [1.6.0](https://github.com/googleapis/python-functions/compare/v1.5.2...v1.6.0) (2022-04-14)


### Features

* AuditConfig for IAM v1 ([784539c](https://github.com/googleapis/python-functions/commit/784539cbe13583722195f21780781c682ba8c7ac))


### Bug Fixes

* **deps:** require grpc-google-iam-v1 >=0.12.4 ([784539c](https://github.com/googleapis/python-functions/commit/784539cbe13583722195f21780781c682ba8c7ac))

## [1.5.2](https://github.com/googleapis/python-functions/compare/v1.5.1...v1.5.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#157](https://github.com/googleapis/python-functions/issues/157)) ([68d56b4](https://github.com/googleapis/python-functions/commit/68d56b41fe472e30101030b8604d7c064acc33d6))
* **deps:** require proto-plus>=1.15.0 ([68d56b4](https://github.com/googleapis/python-functions/commit/68d56b41fe472e30101030b8604d7c064acc33d6))

## [1.5.1](https://github.com/googleapis/python-functions/compare/v1.5.0...v1.5.1) (2022-02-26)


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([80fe038](https://github.com/googleapis/python-functions/commit/80fe038f05f695177cb2366bb92063b485c2bc38))

## [1.5.0](https://github.com/googleapis/python-functions/compare/v1.4.0...v1.5.0) (2022-01-25)


### Features

* add api key support ([#146](https://github.com/googleapis/python-functions/issues/146)) ([258eb69](https://github.com/googleapis/python-functions/commit/258eb698ed1c1adb92b039661ba78b17dc2f5851))

## [1.4.0](https://www.github.com/googleapis/python-functions/compare/v1.3.1...v1.4.0) (2021-11-05)


### Features

* CMEK integration fields 'kms_key_name' and 'docker_repository' added ([47c99d0](https://www.github.com/googleapis/python-functions/commit/47c99d0ea2e5e7d74d10976ea1ec7d8d399e06a4))
* Secret Manager integration fields 'secret_environment_variables' and 'secret_volumes' added ([#130](https://www.github.com/googleapis/python-functions/issues/130)) ([47c99d0](https://www.github.com/googleapis/python-functions/commit/47c99d0ea2e5e7d74d10976ea1ec7d8d399e06a4))

## [1.3.1](https://www.github.com/googleapis/python-functions/compare/v1.3.0...v1.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([7076c62](https://www.github.com/googleapis/python-functions/commit/7076c62bf0d9ba93c1ad2726978224f1f7402ab9))
* **deps:** require google-api-core >= 1.28.0 ([7076c62](https://www.github.com/googleapis/python-functions/commit/7076c62bf0d9ba93c1ad2726978224f1f7402ab9))


### Documentation

* list oneofs in docstring ([7076c62](https://www.github.com/googleapis/python-functions/commit/7076c62bf0d9ba93c1ad2726978224f1f7402ab9))

## [1.3.0](https://www.github.com/googleapis/python-functions/compare/v1.2.0...v1.3.0) (2021-10-21)


### Features

* add support for python 3.10 ([#122](https://www.github.com/googleapis/python-functions/issues/122)) ([f7ceeeb](https://www.github.com/googleapis/python-functions/commit/f7ceeebc09d826394f9bb225a823ec504161ac1f))

## [1.2.0](https://www.github.com/googleapis/python-functions/compare/v1.1.1...v1.2.0) (2021-10-08)


### Features

* add context manager support in client ([#119](https://www.github.com/googleapis/python-functions/issues/119)) ([66772fa](https://www.github.com/googleapis/python-functions/commit/66772faffc88aeb6e84984f402902d51c2d786b2))

## [1.1.1](https://www.github.com/googleapis/python-functions/compare/v1.1.0...v1.1.1) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([ef050bd](https://www.github.com/googleapis/python-functions/commit/ef050bd15318cd9ca4481502411e16bf5c7f2c2e))

## [1.1.0](https://www.github.com/googleapis/python-functions/compare/v1.0.4...v1.1.0) (2021-09-16)


### Features

* add SecurityLevel option on HttpsTrigger ([#109](https://www.github.com/googleapis/python-functions/issues/109)) ([91aa229](https://www.github.com/googleapis/python-functions/commit/91aa229a10b7a6fcdfeb03b2566f4f5a2702636e))

## [1.0.4](https://www.github.com/googleapis/python-functions/compare/v1.0.3...v1.0.4) (2021-08-30)


### Documentation

* minor formatting fixes to Cloud Functions reference docs ([#98](https://www.github.com/googleapis/python-functions/issues/98)) ([05f10cf](https://www.github.com/googleapis/python-functions/commit/05f10cfc3d735d04806a25630875c5ecb3bad65d))

## [1.0.3](https://www.github.com/googleapis/python-functions/compare/v1.0.2...v1.0.3) (2021-08-07)


### Bug Fixes

* Updating behavior of source_upload_url during Get/List function calls ([#93](https://www.github.com/googleapis/python-functions/issues/93)) ([264984c](https://www.github.com/googleapis/python-functions/commit/264984cda2a6a1b75a4e5d78268b35d247ebdd99))

## [1.0.2](https://www.github.com/googleapis/python-functions/compare/v1.0.1...v1.0.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#90](https://www.github.com/googleapis/python-functions/issues/90)) ([03bd652](https://www.github.com/googleapis/python-functions/commit/03bd652e1016ab88dbb458311ad82828219637c9))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#86](https://www.github.com/googleapis/python-functions/issues/86)) ([a20de35](https://www.github.com/googleapis/python-functions/commit/a20de355fc32f6849c7ad5a9c5e16f436483fec5))


### Miscellaneous Chores

* release as 1.0.2 ([#91](https://www.github.com/googleapis/python-functions/issues/91)) ([a0f104c](https://www.github.com/googleapis/python-functions/commit/a0f104c51302a8065e35b3eff25b5031f5110162))

## [1.0.1](https://www.github.com/googleapis/python-functions/compare/v1.0.0...v1.0.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#85](https://www.github.com/googleapis/python-functions/issues/85)) ([5ad78fb](https://www.github.com/googleapis/python-functions/commit/5ad78fb363b8aa4057f8dc76ebac35dbdf5c39f7))

## [1.0.0](https://www.github.com/googleapis/python-functions/compare/v0.7.0...v1.0.0) (2021-06-30)


### Features

* bump release level to production/stable ([#65](https://www.github.com/googleapis/python-functions/issues/65)) ([b0f9d70](https://www.github.com/googleapis/python-functions/commit/b0f9d70287cf4c330523d052371793ad7faf33ae))

## [0.7.0](https://www.github.com/googleapis/python-functions/compare/v0.6.1...v0.7.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#77](https://www.github.com/googleapis/python-functions/issues/77)) ([d2005b7](https://www.github.com/googleapis/python-functions/commit/d2005b7770232d855f47b5037a176a7679b6366a))


### Bug Fixes

* disable always_use_jwt_access ([#81](https://www.github.com/googleapis/python-functions/issues/81)) ([81072d3](https://www.github.com/googleapis/python-functions/commit/81072d3225c9f7b17becd981b8bc0f53cdf8f613))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-functions/issues/1127)) ([#72](https://www.github.com/googleapis/python-functions/issues/72)) ([ec7129a](https://www.github.com/googleapis/python-functions/commit/ec7129a4ce543a08db862f30bc67d394d5a7ef9c)), closes [#1126](https://www.github.com/googleapis/python-functions/issues/1126)

## [0.6.1](https://www.github.com/googleapis/python-functions/compare/v0.6.0...v0.6.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#69](https://www.github.com/googleapis/python-functions/issues/69)) ([c75b52b](https://www.github.com/googleapis/python-functions/commit/c75b52bcc46d13f8f5ad61b91d5b7ced9c1b1e15))

## [0.6.0](https://www.github.com/googleapis/python-functions/compare/v0.5.1...v0.6.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([167f431](https://www.github.com/googleapis/python-functions/commit/167f43144f4f9c5ef88a68bd880ec47a3062a3b6))


### Bug Fixes

* add async client to %name_%version/init.py ([167f431](https://www.github.com/googleapis/python-functions/commit/167f43144f4f9c5ef88a68bd880ec47a3062a3b6))
* **deps:** add packaging requirement ([#62](https://www.github.com/googleapis/python-functions/issues/62)) ([1384f55](https://www.github.com/googleapis/python-functions/commit/1384f55b4e35f6263d42639667c4a38ab1689b16))
* use correct default retry and timeout ([#42](https://www.github.com/googleapis/python-functions/issues/42)) ([8c7db91](https://www.github.com/googleapis/python-functions/commit/8c7db919535193151ed52465a3038d3ac72d701e))

## [0.5.1](https://www.github.com/googleapis/python-functions/compare/v0.5.0...v0.5.1) (2021-02-08)


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([#26](https://www.github.com/googleapis/python-functions/issues/26)) ([207db35](https://www.github.com/googleapis/python-functions/commit/207db35e31d203120f66d384932e54fafec44a08))

## [0.5.0](https://www.github.com/googleapis/python-functions/compare/v0.4.0...v0.5.0) (2020-12-07)


### Features

* add common resource helper paths, expose client transport ([#17](https://www.github.com/googleapis/python-functions/issues/17)) ([e2660f2](https://www.github.com/googleapis/python-functions/commit/e2660f2c53055560c2e7848fa3969d1440aebb62))


### Documentation

* fix link to documentation ([#24](https://www.github.com/googleapis/python-functions/issues/24)) ([8f3ef44](https://www.github.com/googleapis/python-functions/commit/8f3ef446c1ffc5a3395773a70450624c0de99526)), closes [#22](https://www.github.com/googleapis/python-functions/issues/22)

## [0.4.0](https://www.github.com/googleapis/python-functions/compare/v0.1.0...v0.4.0) (2020-10-02)


### Features

* release 0.4.0 ([#7](https://www.github.com/googleapis/python-functions/issues/7)) ([e4e3997](https://www.github.com/googleapis/python-functions/commit/e4e3997cca3d8bdafe04e4931e73da5e934cb769))

## 0.1.0 (2020-07-20)


### Features

* generate v1 ([9a67e29](https://www.github.com/googleapis/python-functions/commit/9a67e29b73b6e653e1d9c5f7c83e44c7f312ab12))
