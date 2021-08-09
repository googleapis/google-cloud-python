# Changelog

### [1.0.3](https://www.github.com/googleapis/python-functions/compare/v1.0.2...v1.0.3) (2021-08-07)


### Bug Fixes

* Updating behavior of source_upload_url during Get/List function calls ([#93](https://www.github.com/googleapis/python-functions/issues/93)) ([264984c](https://www.github.com/googleapis/python-functions/commit/264984cda2a6a1b75a4e5d78268b35d247ebdd99))

### [1.0.2](https://www.github.com/googleapis/python-functions/compare/v1.0.1...v1.0.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#90](https://www.github.com/googleapis/python-functions/issues/90)) ([03bd652](https://www.github.com/googleapis/python-functions/commit/03bd652e1016ab88dbb458311ad82828219637c9))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#86](https://www.github.com/googleapis/python-functions/issues/86)) ([a20de35](https://www.github.com/googleapis/python-functions/commit/a20de355fc32f6849c7ad5a9c5e16f436483fec5))


### Miscellaneous Chores

* release as 1.0.2 ([#91](https://www.github.com/googleapis/python-functions/issues/91)) ([a0f104c](https://www.github.com/googleapis/python-functions/commit/a0f104c51302a8065e35b3eff25b5031f5110162))

### [1.0.1](https://www.github.com/googleapis/python-functions/compare/v1.0.0...v1.0.1) (2021-07-20)


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

### [0.6.1](https://www.github.com/googleapis/python-functions/compare/v0.6.0...v0.6.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#69](https://www.github.com/googleapis/python-functions/issues/69)) ([c75b52b](https://www.github.com/googleapis/python-functions/commit/c75b52bcc46d13f8f5ad61b91d5b7ced9c1b1e15))

## [0.6.0](https://www.github.com/googleapis/python-functions/compare/v0.5.1...v0.6.0) (2021-05-28)


### Features

* support self-signed JWT flow for service accounts ([167f431](https://www.github.com/googleapis/python-functions/commit/167f43144f4f9c5ef88a68bd880ec47a3062a3b6))


### Bug Fixes

* add async client to %name_%version/init.py ([167f431](https://www.github.com/googleapis/python-functions/commit/167f43144f4f9c5ef88a68bd880ec47a3062a3b6))
* **deps:** add packaging requirement ([#62](https://www.github.com/googleapis/python-functions/issues/62)) ([1384f55](https://www.github.com/googleapis/python-functions/commit/1384f55b4e35f6263d42639667c4a38ab1689b16))
* use correct default retry and timeout ([#42](https://www.github.com/googleapis/python-functions/issues/42)) ([8c7db91](https://www.github.com/googleapis/python-functions/commit/8c7db919535193151ed52465a3038d3ac72d701e))

### [0.5.1](https://www.github.com/googleapis/python-functions/compare/v0.5.0...v0.5.1) (2021-02-08)


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
