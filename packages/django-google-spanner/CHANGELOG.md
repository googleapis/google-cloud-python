# Changelog

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
