# Changelog

### [1.0.2](https://www.github.com/googleapis/python-security-private-ca/compare/v1.0.1...v1.0.2) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#83](https://www.github.com/googleapis/python-security-private-ca/issues/83)) ([cd5390c](https://www.github.com/googleapis/python-security-private-ca/commit/cd5390cf5fff50419b000c71431d8ede0de35833))

### [1.0.1](https://www.github.com/googleapis/python-security-private-ca/compare/v1.0.0...v1.0.1) (2021-07-16)


### Bug Fixes

* correct response type of DeleteCaPool ([13e54bf](https://www.github.com/googleapis/python-security-private-ca/commit/13e54bf5ad66f85f1e2165b2cf67604af50ccd0c))
* make allow_config_based_issuance bool optional ([#80](https://www.github.com/googleapis/python-security-private-ca/issues/80)) ([13e54bf](https://www.github.com/googleapis/python-security-private-ca/commit/13e54bf5ad66f85f1e2165b2cf67604af50ccd0c))
* make allow_csr_based_issuance bool optional ([13e54bf](https://www.github.com/googleapis/python-security-private-ca/commit/13e54bf5ad66f85f1e2165b2cf67604af50ccd0c))
* make publish_ca_cert bool optional ([13e54bf](https://www.github.com/googleapis/python-security-private-ca/commit/13e54bf5ad66f85f1e2165b2cf67604af50ccd0c))
* make publish_crl bool optional ([13e54bf](https://www.github.com/googleapis/python-security-private-ca/commit/13e54bf5ad66f85f1e2165b2cf67604af50ccd0c))

## [1.0.0](https://www.github.com/googleapis/python-security-private-ca/compare/v0.4.0...v1.0.0) (2021-07-12)


### Features

* bump release level to production/stable ([#60](https://www.github.com/googleapis/python-security-private-ca/issues/60)) ([170f9be](https://www.github.com/googleapis/python-security-private-ca/commit/170f9be92448278064fd58f2a9302ca2f8c43b04))


### Documentation

* correct links to product documentation ([#77](https://www.github.com/googleapis/python-security-private-ca/issues/77)) ([97821d7](https://www.github.com/googleapis/python-security-private-ca/commit/97821d774f6f3ff0c889e0ad16ef627549e8e28e))

## [0.4.0](https://www.github.com/googleapis/python-security-private-ca/compare/v0.3.0...v0.4.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#70](https://www.github.com/googleapis/python-security-private-ca/issues/70)) ([9b3584d](https://www.github.com/googleapis/python-security-private-ca/commit/9b3584dcf00f50ceab9529f758da3e4ddd5a602c))


### Bug Fixes

* disable always_use_jwt_access ([#74](https://www.github.com/googleapis/python-security-private-ca/issues/74)) ([5cda9ac](https://www.github.com/googleapis/python-security-private-ca/commit/5cda9acc4f7b1aa83bc73700f9cef4f84cc2306a))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-security-private-ca/issues/1127)) ([#65](https://www.github.com/googleapis/python-security-private-ca/issues/65)) ([a82b1ab](https://www.github.com/googleapis/python-security-private-ca/commit/a82b1abdaf8d55f6b6cbf71d6fb7a416e3307888)), closes [#1126](https://www.github.com/googleapis/python-security-private-ca/issues/1126)

## [0.3.0](https://www.github.com/googleapis/python-security-private-ca/compare/v0.2.0...v0.3.0) (2021-05-17)


### Features

* Import v1 by default instead of v1beta1 ([c4c8624](https://www.github.com/googleapis/python-security-private-ca/commit/c4c862426fb5b7b931dd0de4d26d1ac27ce05f1a))
* Make CertificateTemplate bools optional to indicate unset values ([#54](https://www.github.com/googleapis/python-security-private-ca/issues/54)) ([c4c8624](https://www.github.com/googleapis/python-security-private-ca/commit/c4c862426fb5b7b931dd0de4d26d1ac27ce05f1a))
* support self-signed JWT flow for service accounts ([c4c8624](https://www.github.com/googleapis/python-security-private-ca/commit/c4c862426fb5b7b931dd0de4d26d1ac27ce05f1a))


### Bug Fixes

* add async client to %name_%version/init.py ([c4c8624](https://www.github.com/googleapis/python-security-private-ca/commit/c4c862426fb5b7b931dd0de4d26d1ac27ce05f1a))
* **deps:** add packaging requirement ([#56](https://www.github.com/googleapis/python-security-private-ca/issues/56)) ([5877dda](https://www.github.com/googleapis/python-security-private-ca/commit/5877dda559311e87de8f9f06f8174a0e1d4c62bc))

### [0.1.1](https://www.github.com/googleapis/python-security-private-ca/compare/v0.1.0...v0.1.1) (2020-10-02)


### Documentation

* don't treat warnings as errors ([ca0837a](https://www.github.com/googleapis/python-security-private-ca/commit/ca0837a9798d0bf6f3c93dcc003aa38f86eddd5c))

## 0.1.0 (2020-10-02)


### Features

* generate v1beta1 ([9cd5bfa](https://www.github.com/googleapis/python-security-private-ca/commit/9cd5bfaee208396ca5b27590bf09c05ad372d953))
