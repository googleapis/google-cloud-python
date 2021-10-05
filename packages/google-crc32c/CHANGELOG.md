# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-crc32c/#history

## [1.3.0](https://www.github.com/googleapis/python-crc32c/compare/v1.2.0...v1.3.0) (2021-10-05)


### Features

* add support for Python 3.10 ([#116](https://www.github.com/googleapis/python-crc32c/issues/116)) ([01ee9c0](https://www.github.com/googleapis/python-crc32c/commit/01ee9c0b4d6a992ddcf1fbbeaaea9d107c972b74))

## [1.2.0](https://www.github.com/googleapis/python-crc32c/compare/v1.1.5...v1.2.0) (2021-09-17)


### Features

* build wheels using CIBuildWheel ([#103](https://www.github.com/googleapis/python-crc32c/issues/103)) ([55eb731](https://www.github.com/googleapis/python-crc32c/commit/55eb7310b0a0f424da33f4b6d3b4b50e02c323eb))


### Documentation

* update list of supported wheel platforms / architectures ([#105](https://www.github.com/googleapis/python-crc32c/issues/105)) ([edc8d2d](https://www.github.com/googleapis/python-crc32c/commit/edc8d2dbe643f0c2bf1180f855e1585b0e81bdba))

### [1.1.5](https://www.github.com/googleapis/python-crc32c/compare/v1.1.4...v1.1.5) (2021-09-07)


### Bug Fixes

* revert to silent fallback to pure-Python build ([#93](https://www.github.com/googleapis/python-crc32c/issues/93)) ([789a420](https://www.github.com/googleapis/python-crc32c/commit/789a4203648d1b43f060332510177cf3867f82c4))
* fix segfault on MacOS 11 ("Big Sur") for Python < 3.9 ([#93](https://www.github.com/googleapis/python-crc32c/issues/93)) ([789a420](https://www.github.com/googleapis/python-crc32c/commit/789a4203648d1b43f060332510177cf3867f82c4))

### [1.1.4](https://www.github.com/googleapis/python-crc32c/compare/v1.1.4...v1.1.4) (2021-09-02)


### Bug Fixes

* advise setting 'CRC32C_PURE_PYTHON' after build failure ([#84](https://www.github.com/googleapis/python-crc32c/issues/84)) ([6aa1cd6](https://www.github.com/googleapis/python-crc32c/commit/6aa1cd69376b57fbc9bc2c470ed63a270279623d))
* restore building 'manylinux1' wheels ([#87](https://www.github.com/googleapis/python-crc32c/issues/87)) ([ebb9c68](https://www.github.com/googleapis/python-crc32c/commit/ebb9c68aca66e6b89d832e9e237679ac8b9ad344))
* use correct Python 3.10 specifier ([#88](https://www.github.com/googleapis/python-crc32c/issues/88)) ([0c1b740](https://www.github.com/googleapis/python-crc32c/commit/0c1b740c195caed8ac1e67fc38d87073223a6b3d))

### [1.1.4](https://www.github.com/googleapis/python-crc32c/compare/v1.1.3...v1.1.4) (2021-09-01)


### Bug Fixes

* advise setting 'CRC32C_PURE_PYTHON' after build failure ([#84](https://www.github.com/googleapis/python-crc32c/issues/84)) ([6aa1cd6](https://www.github.com/googleapis/python-crc32c/commit/6aa1cd69376b57fbc9bc2c470ed63a270279623d))
* restore building 'manylinux1' wheels ([#87](https://www.github.com/googleapis/python-crc32c/issues/87)) ([ebb9c68](https://www.github.com/googleapis/python-crc32c/commit/ebb9c68aca66e6b89d832e9e237679ac8b9ad344))

### [1.1.3](https://www.github.com/googleapis/python-crc32c/compare/v1.1.2...v1.1.3) (2021-08-30)


### Performance Improvements

* replace CFFI with a native C extension ([#76](https://www.github.com/googleapis/python-crc32c/issues/76)) ([b1bf461](https://www.github.com/googleapis/python-crc32c/commit/b1bf461cc0539962ac16a62860cae3cd2384cb4f))

### [1.1.2](https://www.github.com/googleapis/python-crc32c/compare/v1.1.1...v1.1.2) (2021-01-20)


### Bug Fixes

* add manylinux2014_aarch64 wheels ([#61](https://www.github.com/googleapis/python-crc32c/issues/61)) ([6387658](https://www.github.com/googleapis/python-crc32c/commit/63876582aec715100f61581657f9d994a1ace1bc))
* Add manylinux2014_x86_64 wheels ([#57](https://www.github.com/googleapis/python-crc32c/issues/57)) ([74cb457](https://www.github.com/googleapis/python-crc32c/commit/74cb457255a81d0aa5bee16425675140ed637410))


### Documentation

* add aarch64 to the readme as produced wheels ([#62](https://www.github.com/googleapis/python-crc32c/issues/62)) ([4ef317d](https://www.github.com/googleapis/python-crc32c/commit/4ef317d0efcd654842d17e03749b801303c8bc30))

### [1.1.1](https://www.github.com/googleapis/python-crc32c/compare/v1.1.0...v1.1.1) (2021-01-14)


### Bug Fixes

* Update CI to use GitHub actions and build for osx, windows, linux ([#51](https://www.github.com/googleapis/python-crc32c/issues/51)) ([66f49b8](https://www.github.com/googleapis/python-crc32c/commit/66f49b889ad66f7ecd5d6aeaf840f2c8f2ac131e))


### Documentation

* simplify main readme that is shown on pypi, add additional BUILDING.md ([#54](https://www.github.com/googleapis/python-crc32c/issues/54)) ([93e021f](https://www.github.com/googleapis/python-crc32c/commit/93e021fe8bc55fb046317b884ca21cb75e131e4f))

## [1.1.0](https://www.github.com/googleapis/python-crc32c/compare/v0.1.1...v1.1.0) (2020-12-14)


### Features

* add Python 3.9 support, drop Python 3.5 support ([#42](https://www.github.com/googleapis/python-crc32c/issues/42)) ([1d7fe63](https://www.github.com/googleapis/python-crc32c/commit/1d7fe6338fbcb0e74245f84c2034ac5371f7782a)), closes [#38](https://www.github.com/googleapis/python-crc32c/issues/38)


### Bug Fixes

* add LICENSE to package manifest ([#34](https://www.github.com/googleapis/python-crc32c/issues/34)) ([6c8883b](https://www.github.com/googleapis/python-crc32c/commit/6c8883b2c41aaa6f0dd5991896ad58e73f516182))

### [1.0.0](https://www.github.com/googleapis/python-crc32c/compare/v0.1.0...v1.0.0) (2020-08-07)

### Breaking Changes
* prefix module name with 'google_' to avoid conflict with ICRAR version ([#30](https://www.github.com/googleapis/python-crc32c/issues/30)) ([b50f43e](https://www.github.com/googleapis/python-crc32c/commit/b50f43e7bc40d91ccdade9ccc577a93c0ed05f3a)), closes [#29](https://www.github.com/googleapis/python-crc32c/issues/29)

### Documentation

* rewrap long line ([#32](https://www.github.com/googleapis/python-crc32c/issues/32)) ([30479d4](https://www.github.com/googleapis/python-crc32c/commit/30479d41997a09115aa0152b39ffef09bc97b13a))

## [0.1.0](https://www.github.com/googleapis/python-crc32c/compare/v0.0.2...v0.1.0) (2020-03-20)


### Features

* add pure python implementation ([#20](https://www.github.com/googleapis/python-crc32c/issues/20)) ([97cf381](https://www.github.com/googleapis/python-crc32c/commit/97cf3819035486628b2dcc2ad03e3b427fbf8046))


### Bug Fixes

* retrieve package version at runtime ([#24](https://www.github.com/googleapis/python-crc32c/issues/24)) ([f365e47](https://www.github.com/googleapis/python-crc32c/commit/f365e471c9ae90238ded65456635ccdb6cd33ca2))

## 0.0.2

03-09-2020 15:33 PDT


### Packaging Changes
- fix: add a manifest to specify other files ([#14](https://github.com/googleapis/python-crc32c/pull/14))

### Documentation
- docs: README.md improvements ([#15](https://github.com/googleapis/python-crc32c/pull/15))
