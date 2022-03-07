# Changelog

### [1.2.1](https://github.com/googleapis/python-service-management/compare/v1.2.0...v1.2.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#107](https://github.com/googleapis/python-service-management/issues/107)) ([4fc6a16](https://github.com/googleapis/python-service-management/commit/4fc6a16ac804b65cf5a9443b07a3522cbfbf68af))

## [1.2.0](https://github.com/googleapis/python-service-management/compare/v1.1.1...v1.2.0) (2022-02-18)


### Features

* add api key support ([#91](https://github.com/googleapis/python-service-management/issues/91)) ([ad49299](https://github.com/googleapis/python-service-management/commit/ad49299424aefbaaef686c79af533058d5fa5b66))


### Bug Fixes

* **deps:** remove unused dependency libcst ([#97](https://github.com/googleapis/python-service-management/issues/97)) ([b2b62f1](https://github.com/googleapis/python-service-management/commit/b2b62f156e0ca50d10c0941af7e4fedcd42d8e4c))
* Remove EnableService and DisableService RPC methods and related modules ([#98](https://github.com/googleapis/python-service-management/issues/98)) ([9a2d72c](https://github.com/googleapis/python-service-management/commit/9a2d72c0eb27238925634b1950f40a90ff4d64a0))
* resolve DuplicateCredentialArgs error when using credentials_file ([21f9f5d](https://github.com/googleapis/python-service-management/commit/21f9f5deb04992ecc683afda5c4dd3cae5ffffd3))

### [1.1.1](https://www.github.com/googleapis/python-service-management/compare/v1.1.0...v1.1.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([f00ac02](https://www.github.com/googleapis/python-service-management/commit/f00ac02469bd7b8b5462ffcf2028fa25d33369cb))
* **deps:** require google-api-core >= 1.28.0 ([f00ac02](https://www.github.com/googleapis/python-service-management/commit/f00ac02469bd7b8b5462ffcf2028fa25d33369cb))


### Documentation

* list oneofs in docstring ([f00ac02](https://www.github.com/googleapis/python-service-management/commit/f00ac02469bd7b8b5462ffcf2028fa25d33369cb))

## [1.1.0](https://www.github.com/googleapis/python-service-management/compare/v1.0.4...v1.1.0) (2021-10-26)


### Features

* add context manager support in client ([#63](https://www.github.com/googleapis/python-service-management/issues/63)) ([71186c1](https://www.github.com/googleapis/python-service-management/commit/71186c1256a9bfbd65f2fcd9ed639f724400eeaf))

### [1.0.4](https://www.github.com/googleapis/python-service-management/compare/v1.0.3...v1.0.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([538b500](https://www.github.com/googleapis/python-service-management/commit/538b5005bac38276ffaaa3c6a2d82f9d7bff3477))

### [1.0.3](https://www.github.com/googleapis/python-service-management/compare/v1.0.2...v1.0.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([7547e3a](https://www.github.com/googleapis/python-service-management/commit/7547e3a53a6a437e56cbc832d62aecc627cb4cd6))

### [1.0.2](https://www.github.com/googleapis/python-service-management/compare/v1.0.1...v1.0.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#41](https://www.github.com/googleapis/python-service-management/issues/41)) ([a995bbb](https://www.github.com/googleapis/python-service-management/commit/a995bbb11f53bfd2a224155d0665c141aababc1e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#37](https://www.github.com/googleapis/python-service-management/issues/37)) ([87472ed](https://www.github.com/googleapis/python-service-management/commit/87472ed593f442e7b73a3aa2ee45a4357094d290))


### Miscellaneous Chores

* release as 1.0.2 ([#42](https://www.github.com/googleapis/python-service-management/issues/42)) ([27b79f7](https://www.github.com/googleapis/python-service-management/commit/27b79f7d63ae01e2ba6553eaeedb20b86e878f88))

### [1.0.1](https://www.github.com/googleapis/python-service-management/compare/v1.0.0...v1.0.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#36](https://www.github.com/googleapis/python-service-management/issues/36)) ([84e2ee4](https://www.github.com/googleapis/python-service-management/commit/84e2ee48eaf4605bb445ac01479c4aada420679a))

## [1.0.0](https://www.github.com/googleapis/python-service-management/compare/v0.1.0...v1.0.0) (2021-07-10)


### Features

* add always_use_jwt_access ([#31](https://www.github.com/googleapis/python-service-management/issues/31)) ([8d76ae3](https://www.github.com/googleapis/python-service-management/commit/8d76ae37bb3186e8aa0991fa89a4852dd0798280))
* bump release level to production/stable ([#17](https://www.github.com/googleapis/python-service-management/issues/17)) ([f521883](https://www.github.com/googleapis/python-service-management/commit/f52188344dea468736855dd357570d6a428b2f62))
* support self-signed JWT flow for service accounts ([cb785b5](https://www.github.com/googleapis/python-service-management/commit/cb785b5b6885a7063f49de76ab2ff0145a83e4fe))


### Bug Fixes

* add async client ([cb785b5](https://www.github.com/googleapis/python-service-management/commit/cb785b5b6885a7063f49de76ab2ff0145a83e4fe))
* **deps:** add packaging requirement ([#18](https://www.github.com/googleapis/python-service-management/issues/18)) ([d7084d9](https://www.github.com/googleapis/python-service-management/commit/d7084d9a4d019d54d2a7e5ded04d9d3996f0cc4c))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-service-management/issues/1127)) ([#25](https://www.github.com/googleapis/python-service-management/issues/25)) ([78f33d1](https://www.github.com/googleapis/python-service-management/commit/78f33d18edec8caa2c014258307289c9aef3d609))


### Miscellaneous Chores

* release as 1.0.0 ([#22](https://www.github.com/googleapis/python-service-management/issues/22)) ([028b5a1](https://www.github.com/googleapis/python-service-management/commit/028b5a15fd80dfd62ae708a53cdef6de95ecbe92))

## 0.1.0 (2021-03-24)


### Features

* generate v1 ([1088a47](https://www.github.com/googleapis/python-service-management/commit/1088a4726aa3e5bd8b04e37db2a9e99329d1e5a5))
