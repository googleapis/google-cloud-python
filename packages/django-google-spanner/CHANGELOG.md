# Changelog

## [3.0.2](https://github.com/googleapis/python-spanner-django/compare/v3.0.1...v3.0.2) (2022-08-08)


### Bug Fixes

* override AutoField default value only for Spanner ([#780](https://github.com/googleapis/python-spanner-django/issues/780)) ([3bf2c77](https://github.com/googleapis/python-spanner-django/commit/3bf2c77bddf0ea1886ce096e2bd97f34afd5eb7f))


### Documentation

* Add limitations docs on spanner features not supported by spanner-django library. ([#758](https://github.com/googleapis/python-spanner-django/issues/758)) ([66469bf](https://github.com/googleapis/python-spanner-django/commit/66469bf72dd57555d6729f8863d7d401b7f6613e))

## [3.0.1](https://github.com/googleapis/python-spanner-django/compare/v3.0.0...v3.0.1) (2022-02-07)


### Bug Fixes

* downgrade google-cloud-spanner to v 3.11.1 ([#747](https://github.com/googleapis/python-spanner-django/issues/747)) ([a1f1cac](https://github.com/googleapis/python-spanner-django/commit/a1f1cac6a630cf71643b27580bb0f98c8f06d3ef))

## [3.0.0](https://www.github.com/googleapis/python-spanner-django/compare/v2.2.1-b4...v3.0.0) (2021-10-29)


### Documentation

* typo fixes in readme ([#732](https://www.github.com/googleapis/python-spanner-django/issues/732)) ([bb60a16](https://www.github.com/googleapis/python-spanner-django/commit/bb60a1621be50a12286b939e99e6390b0c4f1bab))
* update limitations about json query support and django version support. ([#729](https://www.github.com/googleapis/python-spanner-django/issues/729)) ([c3b111f](https://www.github.com/googleapis/python-spanner-django/commit/c3b111ff19d58f6ff67eb381a9efef042c70ec54))


### Miscellaneous Chores

* release 3.0.0 ([#734](https://www.github.com/googleapis/python-spanner-django/issues/734)) ([a285571](https://www.github.com/googleapis/python-spanner-django/commit/a285571ce2339a16acc922d82c013817659931f4))

## [2.2.1b4](https://www.github.com/googleapis/python-spanner-django/compare/v2.2.1-b3...v2.2.1b4) (2021-10-25)


### Features

* enable support for `get_key_columns` and cleanup tests with unknown failures to specific failures. ([#721](https://www.github.com/googleapis/python-spanner-django/issues/721)) ([1ec0784](https://www.github.com/googleapis/python-spanner-django/commit/1ec07849787dfcfeda7206e038e0a63c0b45d74c))
* merge django 2.2 and django 3.2 branches into 1 branch ([#717](https://www.github.com/googleapis/python-spanner-django/issues/717)) ([bfb2e20](https://www.github.com/googleapis/python-spanner-django/commit/bfb2e20e26ad63ae41bcc9a5442e9f3b3b383b31))


### Bug Fixes

* Bump version number after 2.2.1b3 release ([#696](https://www.github.com/googleapis/python-spanner-django/issues/696)) ([a8f2aac](https://www.github.com/googleapis/python-spanner-django/commit/a8f2aac06929152067e39b5aac1cebfd74ef5337))


### Documentation

* fix changelog link and sample examples. ([#700](https://www.github.com/googleapis/python-spanner-django/issues/700)) ([08b80ce](https://www.github.com/googleapis/python-spanner-django/commit/08b80cef7723819c22dae53c4ff7f45c4fc8c518))
* lint fix for samples ([#697](https://www.github.com/googleapis/python-spanner-django/issues/697)) ([ed404f5](https://www.github.com/googleapis/python-spanner-django/commit/ed404f57ed4a23c7b60f4f9c238f5b5fa9f81d0c))
* update dbapi location in overview asset file ([#702](https://www.github.com/googleapis/python-spanner-django/issues/702)) ([4643876](https://www.github.com/googleapis/python-spanner-django/commit/4643876219e8a54feb94bf14a79f0fe2fbe3971a))


### Miscellaneous Chores

* release 2.2.1b4 ([#724](https://www.github.com/googleapis/python-spanner-django/issues/724)) ([6581d7b](https://www.github.com/googleapis/python-spanner-django/commit/6581d7bdbe2dcbd204596b70043ab75f9932fcf5))

## 2.2.1b3 (2021-07-30)

### Miscellaneous Chores
- release 2.2.1b3 ([de23f65](https://www.github.com/googleapis/python-spanner-django/commit/de23f65))
- Update repo to say beta release instead of alpha ([#691](https://www.github.com/googleapis/python-spanner-django/issues/691)) ([2144d09](https://www.github.com/googleapis/python-spanner-django/commit/2144d09))


## 2.2.1b2 (2021-07-27)


### Features
- Added support for check constraint ([#679](https://www.github.com/googleapis/python-spanner-django/issues/679)) ([42352c0](https://www.github.com/googleapis/python-spanner-django/commit/42352c0))
- Add open telemetry trace in schema and related unit tests ([#648](https://www.github.com/googleapis/python-spanner-django/issues/648)) ([fc51086](https://www.github.com/googleapis/python-spanner-django/commit/fc51086))


### Bug Fixes
- updated assets to have text background so it works with dark mode ([#674](https://www.github.com/googleapis/python-spanner-django/issues/674)) ([306eeba](https://www.github.com/googleapis/python-spanner-django/commit/306eeba))
- updated assets to have text background so it works with dark mode ([#671](https://www.github.com/googleapis/python-spanner-django/issues/671)) ([0f99938](https://www.github.com/googleapis/python-spanner-django/commit/0f99938))
- bump version number after 2.2.1b1 release ([#652](https://www.github.com/googleapis/python-spanner-django/issues/652)) ([287b893](https://www.github.com/googleapis/python-spanner-django/commit/287b893))


### Documentation
- update docs to show decimal field support and check constraints but no support for unsigned data type ([#683](https://www.github.com/googleapis/python-spanner-django/issues/683)) ([74f2269](https://www.github.com/googleapis/python-spanner-django/commit/74f2269))
- Adding documentation for GA ([#665](https://www.github.com/googleapis/python-spanner-django/issues/665)) ([216c2e0](https://www.github.com/googleapis/python-spanner-django/commit/216c2e0))


### Miscellaneous Chores
- release 2.2.1b2 ([#685](https://www.github.com/googleapis/python-spanner-django/issues/685)) ([96a809d](https://www.github.com/googleapis/python-spanner-django/commit/96a809d))
- fix release build ([#659](https://www.github.com/googleapis/python-spanner-django/issues/659)) ([11bc9c2](https://www.github.com/googleapis/python-spanner-django/commit/11bc9c2))

## 2.2.1b1 (2021-06-17)


### Features
* Add support for open telemetry ([#633](https://www.github.com/googleapis/python-spanner-django/issues/633)) ([2ba879a](https://www.github.com/googleapis/python-spanner-django/commit/2ba879a))
* add decimal/numeric support ([#620](https://www.github.com/googleapis/python-spanner-django/issues/620)) ([d09ad61](https://www.github.com/googleapis/python-spanner-django/commit/d09ad61))
* added unit test with coverage of 68% ([#611](https://www.github.com/googleapis/python-spanner-django/issues/611)) ([92ad508](https://www.github.com/googleapis/python-spanner-django/commit/92ad508))
* update docs and nox file to compile it ([#610](https://www.github.com/googleapis/python-spanner-django/issues/610)) ([876f2fc](https://www.github.com/googleapis/python-spanner-django/commit/876f2fc))
* update workflow files to uniformly distribute the test modules by time taken by each test module ([#615](https://www.github.com/googleapis/python-spanner-django/issues/615)) ([c386123](https://www.github.com/googleapis/python-spanner-django/commit/c386123))
* move migrations test modules to run against different emulator ([#613](https://www.github.com/googleapis/python-spanner-django/issues/613)) ([5b3b2e4](https://www.github.com/googleapis/python-spanner-django/commit/5b3b2e4))


### Bug Fixes
* correct import path ([#649](https://www.github.com/googleapis/python-spanner-django/issues/649)) ([bc99bb5](https://www.github.com/googleapis/python-spanner-django/commit/bc99bb5))
* remove error msg check from test_decimal_precision_limit for non emulator test ([#647](https://www.github.com/googleapis/python-spanner-django/issues/647)) ([fe4a062](https://www.github.com/googleapis/python-spanner-django/commit/fe4a062))
* remove error msg check from test_decimal_precision_limit ([#646](https://www.github.com/googleapis/python-spanner-django/issues/646)) ([9be15c0](https://www.github.com/googleapis/python-spanner-django/commit/9be15c0))
* remove delete of instance if it already exists, as it might be in use by another test ([#641](https://www.github.com/googleapis/python-spanner-django/issues/641)) ([0544208](https://www.github.com/googleapis/python-spanner-django/commit/0544208))
* correct test case for sql_flush for multiple delete table commands ([#629](https://www.github.com/googleapis/python-spanner-django/issues/629)) ([3de1a81](https://www.github.com/googleapis/python-spanner-django/commit/3de1a81))
* iexact lookup with Transform expression crash issue when RHS is direct value and a transform function is involved ([#628](https://www.github.com/googleapis/python-spanner-django/issues/628)) ([2772b57](https://www.github.com/googleapis/python-spanner-django/commit/2772b57))
* Update links in comments to use googleapis repo ([#622](https://www.github.com/googleapis/python-spanner-django/issues/622)) ([3fa1aeb](https://www.github.com/googleapis/python-spanner-django/commit/3fa1aeb))
* Remove un necessary file from code base ([#608](https://www.github.com/googleapis/python-spanner-django/issues/608)) ([58b9969](https://www.github.com/googleapis/python-spanner-django/commit/58b9969))
* lint_setup_py was failing in Kokoro is now fixed ([#607](https://www.github.com/googleapis/python-spanner-django/issues/607)) ([d125148](https://www.github.com/googleapis/python-spanner-django/commit/d125148))
* Replace, fast-forward Django CI branch ([#598](https://www.github.com/googleapis/python-spanner-django/issues/598)) ([5d65e3f](https://www.github.com/googleapis/python-spanner-django/commit/5d65e3f))


### Code Refactoring
* update coverage score in nox file and cleanup imports in test_operations ([#638](https://www.github.com/googleapis/python-spanner-django/issues/638)) ([b1f49f7](https://www.github.com/googleapis/python-spanner-django/commit/b1f49f7))


### Documentation
* add docs build kokoro config for django spanner ([#644](https://www.github.com/googleapis/python-spanner-django/issues/644)) ([ecf241a](https://www.github.com/googleapis/python-spanner-django/commit/ecf241a))


### Miscellaneous Chores
* release 2.2.1b1 ([505d3ac](https://www.github.com/googleapis/python-spanner-django/commit/505d3ac))
* add SECURITY.md ([#616](https://www.github.com/googleapis/python-spanner-django/issues/616)) ([75f1a65](https://www.github.com/googleapis/python-spanner-django/commit/75f1a65))
* add a Code of Conduct ([#604](https://www.github.com/googleapis/python-spanner-django/issues/604)) ([c996400](https://www.github.com/googleapis/python-spanner-django/commit/c996400))
* Remove README note about Variance/StdDev ([#601](https://www.github.com/googleapis/python-spanner-django/issues/601)) ([4ec363f](https://www.github.com/googleapis/python-spanner-django/commit/4ec363f))
* Add contributing section to README ([#600](https://www.github.com/googleapis/python-spanner-django/issues/600)) ([2311854](https://www.github.com/googleapis/python-spanner-django/commit/2311854))
* README updates ([#599](https://www.github.com/googleapis/python-spanner-django/issues/599)) ([2c8fb24](https://www.github.com/googleapis/python-spanner-django/commit/2c8fb24))

## 2.2.1b0 (2021-01-29)


### ⚠ BREAKING CHANGES

* DBAPI code was moved into python-spanner in https://github.com/googleapis/python-spanner/pull/160. This change removes it from this repo and bumps the dependency on python-spanner to 2.0.0, the first released version to include DBAPI.
* Update python-spanner dep, drop py 3.5 (#557)

### Features

* [WIP] The first stage of `nox` implementation ([#468](https://www.github.com/googleapis/python-spanner-django/issues/468)) ([96f2223](https://www.github.com/googleapis/python-spanner-django/commit/96f2223e3389a0922e0f1db44df72c698cfa5263))
* Add dummy WHERE clause to certain statements ([#516](https://www.github.com/googleapis/python-spanner-django/issues/516)) ([af5d8e3](https://www.github.com/googleapis/python-spanner-django/commit/af5d8e3af808a8639e54c691c8f110be0a309d15))
* add PyPI release support ([#451](https://www.github.com/googleapis/python-spanner-django/issues/451)) ([da82c41](https://www.github.com/googleapis/python-spanner-django/commit/da82c417815e607611743c828f3525e71f9a46f4))
* clear session pool on connection close ([#543](https://www.github.com/googleapis/python-spanner-django/issues/543)) ([14e4cac](https://www.github.com/googleapis/python-spanner-django/commit/14e4cac77fd9ba5cf421c56c636528ec77b82451))
* cursor must detect if the parent connection is closed ([#463](https://www.github.com/googleapis/python-spanner-django/issues/463)) ([a9fd5a3](https://www.github.com/googleapis/python-spanner-django/commit/a9fd5a382463be47e34ec079a606fd9952048469))
* Implementing DB-API types according to the PEP-0249 specification ([#521](https://www.github.com/googleapis/python-spanner-django/issues/521)) ([62c22b1](https://www.github.com/googleapis/python-spanner-django/commit/62c22b113b470776cddacbab92c4428c6581c551))
* refactor connect() function, cover it with unit tests ([#462](https://www.github.com/googleapis/python-spanner-django/issues/462)) ([4fedcf1](https://www.github.com/googleapis/python-spanner-django/commit/4fedcf18a235c226d062ce7e61070477bfd3a107))
* Stage 2 of `nox` implementation - adding `docs` target ([#473](https://www.github.com/googleapis/python-spanner-django/issues/473)) ([45d6b97](https://www.github.com/googleapis/python-spanner-django/commit/45d6b970867627694684b628fb20900388f78663))
* Stage 3-4 of `nox` implementation - adding auto-format targets ([#478](https://www.github.com/googleapis/python-spanner-django/issues/478)) ([59e7c3f](https://www.github.com/googleapis/python-spanner-django/commit/59e7c3f2cb5ca8381a8674eb3f2aef59c37e9fa6))
* Stage 5 of `nox` implementation - adding coverage targets ([#479](https://www.github.com/googleapis/python-spanner-django/issues/479)) ([cec6b96](https://www.github.com/googleapis/python-spanner-django/commit/cec6b96d8b8ae662028d7f0901cacceeb2eb1c97))
* Stage 6 of `nox` implementation - enabling system tests ([#480](https://www.github.com/googleapis/python-spanner-django/issues/480)) ([dc73bf6](https://www.github.com/googleapis/python-spanner-django/commit/dc73bf65f9dbe0f9a62059ea23c6423dfcfd1901))
* support transactions management ([#535](https://www.github.com/googleapis/python-spanner-django/issues/535)) ([2f2cd86](https://www.github.com/googleapis/python-spanner-django/commit/2f2cd8631817c9f3d898c60e38778ae533c3f803))


### Bug Fixes

* add description for transaction autocommit ([#587](https://www.github.com/googleapis/python-spanner-django/issues/587)) ([8441edc](https://www.github.com/googleapis/python-spanner-django/commit/8441edcc161a5ad86f171dfc2cd4b9ccef19b2c0))
* add project env in readme file ([#586](https://www.github.com/googleapis/python-spanner-django/issues/586)) ([55b9d19](https://www.github.com/googleapis/python-spanner-django/commit/55b9d197f023067470f8769615a83e1a11df53ba))
* Bump version ahead of lateset release ([#571](https://www.github.com/googleapis/python-spanner-django/issues/571)) ([36e5b82](https://www.github.com/googleapis/python-spanner-django/commit/36e5b82facdc8e7a7286b2cf1ab20afa2e9e1aef))
* Change release script package name ([#489](https://www.github.com/googleapis/python-spanner-django/issues/489)) ([388ea6b](https://www.github.com/googleapis/python-spanner-django/commit/388ea6bc187bd5510e2aeab0fd5d6a6e46efb777))
* DatabaseWrapper method impl and potential bugfix ([#545](https://www.github.com/googleapis/python-spanner-django/issues/545)) ([d8453c7](https://www.github.com/googleapis/python-spanner-django/commit/d8453c7e458b0b476b91785d32ba234e333a4b9f))
* Fix black, isort compatibility  ([#469](https://www.github.com/googleapis/python-spanner-django/issues/469)) ([dd005d5](https://www.github.com/googleapis/python-spanner-django/commit/dd005d5a8f39634750a8c81b603782f1254dcccf))
* fix from-scratch tutorial ([#573](https://www.github.com/googleapis/python-spanner-django/issues/573)) ([59ce5e7](https://www.github.com/googleapis/python-spanner-django/commit/59ce5e7abd13a1793c7985ee4b4a092f6afdf770))
* fix healthchecks app tutorial ([#574](https://www.github.com/googleapis/python-spanner-django/issues/574)) ([65d2e9d](https://www.github.com/googleapis/python-spanner-django/commit/65d2e9dccf494c3283f1abcd936220b5f353c59e))
* Fix license classifier ([#507](https://www.github.com/googleapis/python-spanner-django/issues/507)) ([9244414](https://www.github.com/googleapis/python-spanner-django/commit/9244414d23fca9facdd05c0e10dde86891001001))
* Fix package name in README ([#556](https://www.github.com/googleapis/python-spanner-django/issues/556)) ([8b2329a](https://www.github.com/googleapis/python-spanner-django/commit/8b2329afca64863197790681d6bf8c64a9040823))
* fix typo in README ([#575](https://www.github.com/googleapis/python-spanner-django/issues/575)) ([d25fa86](https://www.github.com/googleapis/python-spanner-django/commit/d25fa86857409a4f0f17c9de3057465bef048df6))
* override django autocommit to spanner ([#583](https://www.github.com/googleapis/python-spanner-django/issues/583)) ([7ce685d](https://www.github.com/googleapis/python-spanner-django/commit/7ce685d76033fa8a46d4ccf8488af68ee8947ced))
* permanently broken date & time unit tests on Windows ([#524](https://www.github.com/googleapis/python-spanner-django/issues/524)) ([3f5db62](https://www.github.com/googleapis/python-spanner-django/commit/3f5db62863bd03c85b2a1b4614d5d782895b6d57))
* Replace repo name with pkg name ([#508](https://www.github.com/googleapis/python-spanner-django/issues/508)) ([fbba900](https://www.github.com/googleapis/python-spanner-django/commit/fbba9001344295a9e18cd153d7f8475bc3e1b684))
* s/installation/installation/ ([#509](https://www.github.com/googleapis/python-spanner-django/issues/509)) ([03c963a](https://www.github.com/googleapis/python-spanner-django/commit/03c963a7aaac61f3ea6575952c193e72c67f5bf2))
* s/useage/usage/ ([#511](https://www.github.com/googleapis/python-spanner-django/issues/511)) ([6b960ec](https://www.github.com/googleapis/python-spanner-django/commit/6b960ecea66cbe23fb7987763fbcd29ce0b8dc6d))
* update pypi package name ([#454](https://www.github.com/googleapis/python-spanner-django/issues/454)) ([47154d1](https://www.github.com/googleapis/python-spanner-django/commit/47154d1f6c7bf0b1d7150c24ba18e2f1dffd9cc1))
* Update README for alpha release ([#503](https://www.github.com/googleapis/python-spanner-django/issues/503)) ([3d31167](https://www.github.com/googleapis/python-spanner-django/commit/3d3116752acdc89ec90d56a9fa3b9d26d11ebf67))
* Update version to 2.2.0a1 ([#506](https://www.github.com/googleapis/python-spanner-django/issues/506)) ([a3a6344](https://www.github.com/googleapis/python-spanner-django/commit/a3a6344656d63e34d6110536aa6830b0db13343a))
* Use "any" default role in sphinx ([#550](https://www.github.com/googleapis/python-spanner-django/issues/550)) ([196c449](https://www.github.com/googleapis/python-spanner-django/commit/196c44949370fb818e610b21c3b00344fdc3d03a))


### Code Refactoring

* erase dbapi directory and all the related tests ([#554](https://www.github.com/googleapis/python-spanner-django/issues/554)) ([8183247](https://www.github.com/googleapis/python-spanner-django/commit/818324708e9ca46fbd80c47745bdf38e8a1a069c))
* Update python-spanner dep, drop py 3.5 ([#557](https://www.github.com/googleapis/python-spanner-django/issues/557)) ([5910833](https://www.github.com/googleapis/python-spanner-django/commit/5910833216288d2fd5cce57e98eb051d0cf82131))


### Documentation

* add a querying example into the main readme ([#515](https://www.github.com/googleapis/python-spanner-django/issues/515)) ([c477cc2](https://www.github.com/googleapis/python-spanner-django/commit/c477cc283ab1f036454eb446f0ca0599235b1e5c))
* minor fixes to README.md ([#448](https://www.github.com/googleapis/python-spanner-django/issues/448)) ([f969000](https://www.github.com/googleapis/python-spanner-django/commit/f9690007603c94f4c99b244a92c639adfd360a8f))
* move test suite information to CONTRIBUTING.md ([#442](https://www.github.com/googleapis/python-spanner-django/issues/442)) ([05280ae](https://www.github.com/googleapis/python-spanner-django/commit/05280aecdcbe933e113616b5705f4e76303d9637))
* Update docstrings for `django_spanner` ([#564](https://www.github.com/googleapis/python-spanner-django/issues/564)) ([7083f1d](https://www.github.com/googleapis/python-spanner-django/commit/7083f1d81dc8b412aab5a4e7d7f110152a87c5d9))
* updated `README.rst` file ([#563](https://www.github.com/googleapis/python-spanner-django/issues/563)) ([d70cb28](https://www.github.com/googleapis/python-spanner-django/commit/d70cb28c8a20511558fa47818103afb5e0492918))
* verify and comment the DB API exceptions ([#522](https://www.github.com/googleapis/python-spanner-django/issues/522)) ([5ed0845](https://www.github.com/googleapis/python-spanner-django/commit/5ed08453002a318245d9241cd1e24c222a588159))

## 2.2.0a1 (2020-09-29)


### Features

* [WIP] The first stage of `nox` implementation ([#468](https://www.github.com/googleapis/python-spanner-django/issues/468)) ([96f2223](https://www.github.com/googleapis/python-spanner-django/commit/96f2223e3389a0922e0f1db44df72c698cfa5263))
* add PyPI release support ([#451](https://www.github.com/googleapis/python-spanner-django/issues/451)) ([da82c41](https://www.github.com/googleapis/python-spanner-django/commit/da82c417815e607611743c828f3525e71f9a46f4)), closes [#449](https://www.github.com/googleapis/python-spanner-django/issues/449)
* cursor must detect if the parent connection is closed ([#463](https://www.github.com/googleapis/python-spanner-django/issues/463)) ([a9fd5a3](https://www.github.com/googleapis/python-spanner-django/commit/a9fd5a382463be47e34ec079a606fd9952048469))
* refactor connect() function, cover it with unit tests ([#462](https://www.github.com/googleapis/python-spanner-django/issues/462)) ([4fedcf1](https://www.github.com/googleapis/python-spanner-django/commit/4fedcf18a235c226d062ce7e61070477bfd3a107))
* Stage 2 of `nox` implementation - adding `docs` target ([#473](https://www.github.com/googleapis/python-spanner-django/issues/473)) ([45d6b97](https://www.github.com/googleapis/python-spanner-django/commit/45d6b970867627694684b628fb20900388f78663))
* Stage 3-4 of `nox` implementation - adding auto-format targets ([#478](https://www.github.com/googleapis/python-spanner-django/issues/478)) ([59e7c3f](https://www.github.com/googleapis/python-spanner-django/commit/59e7c3f2cb5ca8381a8674eb3f2aef59c37e9fa6))
* Stage 5 of `nox` implementation - adding coverage targets ([#479](https://www.github.com/googleapis/python-spanner-django/issues/479)) ([cec6b96](https://www.github.com/googleapis/python-spanner-django/commit/cec6b96d8b8ae662028d7f0901cacceeb2eb1c97))
* Stage 6 of `nox` implementation - enabling system tests ([#480](https://www.github.com/googleapis/python-spanner-django/issues/480)) ([dc73bf6](https://www.github.com/googleapis/python-spanner-django/commit/dc73bf65f9dbe0f9a62059ea23c6423dfcfd1901))


### Bug Fixes

* Change release script package name ([#489](https://www.github.com/googleapis/python-spanner-django/issues/489)) ([388ea6b](https://www.github.com/googleapis/python-spanner-django/commit/388ea6bc187bd5510e2aeab0fd5d6a6e46efb777))
* Fix black, isort compatibility  ([#469](https://www.github.com/googleapis/python-spanner-django/issues/469)) ([dd005d5](https://www.github.com/googleapis/python-spanner-django/commit/dd005d5a8f39634750a8c81b603782f1254dcccf))
* Fix license classifier ([#507](https://www.github.com/googleapis/python-spanner-django/issues/507)) ([9244414](https://www.github.com/googleapis/python-spanner-django/commit/9244414d23fca9facdd05c0e10dde86891001001))
* Replace repo name with pkg name ([#508](https://www.github.com/googleapis/python-spanner-django/issues/508)) ([fbba900](https://www.github.com/googleapis/python-spanner-django/commit/fbba9001344295a9e18cd153d7f8475bc3e1b684))
* s/installation/installation/ ([#509](https://www.github.com/googleapis/python-spanner-django/issues/509)) ([03c963a](https://www.github.com/googleapis/python-spanner-django/commit/03c963a7aaac61f3ea6575952c193e72c67f5bf2))
* s/useage/usage/ ([#511](https://www.github.com/googleapis/python-spanner-django/issues/511)) ([6b960ec](https://www.github.com/googleapis/python-spanner-django/commit/6b960ecea66cbe23fb7987763fbcd29ce0b8dc6d))
* update pypi package name ([#454](https://www.github.com/googleapis/python-spanner-django/issues/454)) ([47154d1](https://www.github.com/googleapis/python-spanner-django/commit/47154d1f6c7bf0b1d7150c24ba18e2f1dffd9cc1)), closes [#455](https://www.github.com/googleapis/python-spanner-django/issues/455)
* Update README for alpha release ([#503](https://www.github.com/googleapis/python-spanner-django/issues/503)) ([3d31167](https://www.github.com/googleapis/python-spanner-django/commit/3d3116752acdc89ec90d56a9fa3b9d26d11ebf67))
* Update version to 2.2.0a1 ([#506](https://www.github.com/googleapis/python-spanner-django/issues/506)) ([a3a6344](https://www.github.com/googleapis/python-spanner-django/commit/a3a6344656d63e34d6110536aa6830b0db13343a)), closes [#502](https://www.github.com/googleapis/python-spanner-django/issues/502)


### Reverts

* Revert "django_spanner: skip 57 expressions_case tests that assume serial pk" ([48909f6](https://www.github.com/googleapis/python-spanner-django/commit/48909f6aa2dc33aca6843de2d1ce18ab943294fe)), closes [#353](https://www.github.com/googleapis/python-spanner-django/issues/353)


### Documentation

* minor fixes to README.md ([#448](https://www.github.com/googleapis/python-spanner-django/issues/448)) ([f969000](https://www.github.com/googleapis/python-spanner-django/commit/f9690007603c94f4c99b244a92c639adfd360a8f))
* move test suite information to CONTRIBUTING.md ([#442](https://www.github.com/googleapis/python-spanner-django/issues/442)) ([05280ae](https://www.github.com/googleapis/python-spanner-django/commit/05280aecdcbe933e113616b5705f4e76303d9637))

## 2.2.0a1 (2020-09-15)


### Features

* [WIP] The first stage of `nox` implementation ([#468](https://www.github.com/googleapis/python-spanner-django/issues/468)) ([96f2223](https://www.github.com/googleapis/python-spanner-django/commit/96f2223e3389a0922e0f1db44df72c698cfa5263))
* add PyPI release support ([#451](https://www.github.com/googleapis/python-spanner-django/issues/451)) ([da82c41](https://www.github.com/googleapis/python-spanner-django/commit/da82c417815e607611743c828f3525e71f9a46f4)), closes [#449](https://www.github.com/googleapis/python-spanner-django/issues/449)
* cursor must detect if the parent connection is closed ([#463](https://www.github.com/googleapis/python-spanner-django/issues/463)) ([a9fd5a3](https://www.github.com/googleapis/python-spanner-django/commit/a9fd5a382463be47e34ec079a606fd9952048469))
* refactor connect() function, cover it with unit tests ([#462](https://www.github.com/googleapis/python-spanner-django/issues/462)) ([4fedcf1](https://www.github.com/googleapis/python-spanner-django/commit/4fedcf18a235c226d062ce7e61070477bfd3a107))
* Stage 2 of `nox` implementation - adding `docs` target ([#473](https://www.github.com/googleapis/python-spanner-django/issues/473)) ([45d6b97](https://www.github.com/googleapis/python-spanner-django/commit/45d6b970867627694684b628fb20900388f78663))
* Stage 3-4 of `nox` implementation - adding auto-format targets ([#478](https://www.github.com/googleapis/python-spanner-django/issues/478)) ([59e7c3f](https://www.github.com/googleapis/python-spanner-django/commit/59e7c3f2cb5ca8381a8674eb3f2aef59c37e9fa6))
* Stage 5 of `nox` implementation - adding coverage targets ([#479](https://www.github.com/googleapis/python-spanner-django/issues/479)) ([cec6b96](https://www.github.com/googleapis/python-spanner-django/commit/cec6b96d8b8ae662028d7f0901cacceeb2eb1c97))
* Stage 6 of `nox` implementation - enabling system tests ([#480](https://www.github.com/googleapis/python-spanner-django/issues/480)) ([dc73bf6](https://www.github.com/googleapis/python-spanner-django/commit/dc73bf65f9dbe0f9a62059ea23c6423dfcfd1901))


### Bug Fixes

* Change release script package name ([#489](https://www.github.com/googleapis/python-spanner-django/issues/489)) ([388ea6b](https://www.github.com/googleapis/python-spanner-django/commit/388ea6bc187bd5510e2aeab0fd5d6a6e46efb777))
* Fix black, isort compatibility  ([#469](https://www.github.com/googleapis/python-spanner-django/issues/469)) ([dd005d5](https://www.github.com/googleapis/python-spanner-django/commit/dd005d5a8f39634750a8c81b603782f1254dcccf))
* update pypi package name ([#454](https://www.github.com/googleapis/python-spanner-django/issues/454)) ([47154d1](https://www.github.com/googleapis/python-spanner-django/commit/47154d1f6c7bf0b1d7150c24ba18e2f1dffd9cc1)), closes [#455](https://www.github.com/googleapis/python-spanner-django/issues/455)
* Update README for alpha release ([#503](https://www.github.com/googleapis/python-spanner-django/issues/503)) ([3d31167](https://www.github.com/googleapis/python-spanner-django/commit/3d3116752acdc89ec90d56a9fa3b9d26d11ebf67))
* Update version to 2.2.0a1 ([#506](https://www.github.com/googleapis/python-spanner-django/issues/506)) ([a3a6344](https://www.github.com/googleapis/python-spanner-django/commit/a3a6344656d63e34d6110536aa6830b0db13343a)), closes [#502](https://www.github.com/googleapis/python-spanner-django/issues/502)


### Reverts

* Revert "django_spanner: skip 57 expressions_case tests that assume serial pk" ([48909f6](https://www.github.com/googleapis/python-spanner-django/commit/48909f6aa2dc33aca6843de2d1ce18ab943294fe)), closes [#353](https://www.github.com/googleapis/python-spanner-django/issues/353)


### Documentation

* minor fixes to README.md ([#448](https://www.github.com/googleapis/python-spanner-django/issues/448)) ([f969000](https://www.github.com/googleapis/python-spanner-django/commit/f9690007603c94f4c99b244a92c639adfd360a8f))
* move test suite information to CONTRIBUTING.md ([#442](https://www.github.com/googleapis/python-spanner-django/issues/442)) ([05280ae](https://www.github.com/googleapis/python-spanner-django/commit/05280aecdcbe933e113616b5705f4e76303d9637))
